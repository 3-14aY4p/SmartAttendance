from datetime import datetime
import time
import platform
import re
import pytesseract
import cv2

from handlers import DBHandler as dh

if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

color_grn = (0, 255, 0)
color_red = (0, 0, 255)

scan_interval = 1.0
current_time = 0.0
last_scanned = 0.0

previous_roi = None
last_detected_id = None
curr_detected_id = None

STABLE_SCAN_THRESHOLD = 2
legal_scans = 0

conf = r"--psm 7 --oem 1 tessedit_char_whitelist=0123456789-AI"

scan_data = {
    "student_id": "",
    "student_name": "",
    "status": "Waiting for scan...",
}

subject_id = "ICT-110"
instructor_id = "005"
class_start = "13:00"
class_end = "16:00"

camera = None


def get_camera():
    # Functionality:
    # Opens the camera only when needed and reuses the same object.
    global camera

    if camera is None or not camera.isOpened():
        # OLD CODE KEPT FOR REFERENCE
        # camera = cv2.VideoCapture(0)

        # CHANGED: Windows-friendly camera open with retry
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if not camera.isOpened():
            camera.release()
            camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)

        if not camera.isOpened():
            camera.release()
            camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            camera.release()
            camera = cv2.VideoCapture(1)

    return camera


def release_camera():
    # Functionality:
    # Releases the active camera safely.
    global camera

    if camera is not None and camera.isOpened():
        camera.release()

    camera = None


def get_scan_data():
    # Functionality:
    # Returns the most recent scan result for the desktop UI.
    return scan_data


def convert(time_text):
    # Functionality:
    # Converts a 24-hour time string into a Python time object.
    return datetime.strptime(time_text, "%H:%M").time()


def get_rect(frame):
    # Functionality:
    # Computes the scan box coordinates on the current frame.
    h, w, _ = frame.shape
    x1 = int(w * 0.3)
    y1 = int(h * 0.55)
    x2 = int(w * 0.7)
    y2 = int(h * 0.7)
    return x1, y1, x2, y2


def draw_rect(frame, color):
    # Functionality:
    # Draws the scanning guide corners on the frame.
    x1, y1, x2, y2 = get_rect(frame)

    cv2.line(frame, (x1, y1), (x1 + 15, y1), color, 2)
    cv2.line(frame, (x1, y1), (x1, y1 + 15), color, 2)
    cv2.line(frame, (x1, y2), (x1 + 15, y2), color, 2)
    cv2.line(frame, (x1, y2), (x1, y2 - 15), color, 2)
    cv2.line(frame, (x2, y1), (x2 - 15, y1), color, 2)
    cv2.line(frame, (x2, y1), (x2, y1 + 15), color, 2)
    cv2.line(frame, (x2, y2), (x2 - 15, y2), color, 2)
    cv2.line(frame, (x2, y2), (x2, y2 - 15), color, 2)


def scan_for_id(roi):
    # Functionality:
    # Runs OCR on the ROI and extracts a matching ID pattern.
    rz = 3

    p_img = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    p_img = cv2.resize(p_img, None, fx=rz, fy=rz, interpolation=cv2.INTER_CUBIC)
    p_img = cv2.GaussianBlur(p_img, (5, 5), 0)
    _, p_img = cv2.threshold(p_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    text = pytesseract.image_to_string(p_img, config=conf).strip()

    if re.match(r"\d{4}-\d{4}4", text):
        text = text[:-1] + "-I"

    match = re.search(r"\d{4}-\d{4}-[A-Z]", text)
    return match.group() if match else None


def validate_attendance(frame, roi, instructor_id_value="005", class_start_value="07:30", class_end_value="09:00"):
    # Functionality:
    # Validates scan results and records attendance after stable repeated detection.
    global current_time, last_scanned, curr_detected_id, last_detected_id, previous_roi, legal_scans

    td_date = datetime.now().date()

    if legal_scans > 0:
        draw_rect(frame, color_grn)
    else:
        draw_rect(frame, color_red)

    current_time = time.time()
    if current_time - last_scanned > scan_interval:
        curr_detected_id = scan_for_id(roi)
        previous_roi = roi.copy()
        last_scanned = current_time

        if curr_detected_id:
            student = dh.query_student_id(curr_detected_id)

            if student.get("success"):
                student_name = student.get("name", "")
                has_record = dh.query_attendance(curr_detected_id, subject_id, td_date)
                enrolled = dh.query_subject_enrollment(curr_detected_id, subject_id)

                if curr_detected_id == last_detected_id:
                    legal_scans += 1
                else:
                    legal_scans = 1
                    last_detected_id = curr_detected_id

                if not enrolled.get("success"):
                    legal_scans = 0
                    last_detected_id = None
                    scan_data["student_id"] = curr_detected_id
                    scan_data["student_name"] = student_name
                    scan_data["status"] = "Student is not enrolled in this subject."

                elif has_record:
                    legal_scans = 0
                    last_detected_id = None
                    scan_data["student_id"] = curr_detected_id
                    scan_data["student_name"] = student_name
                    scan_data["status"] = "Attendance record found."

                else:
                    scan_data["student_id"] = curr_detected_id
                    scan_data["student_name"] = student_name
                    scan_data["status"] = "HOLD ID Card in place."

                    if legal_scans >= STABLE_SCAN_THRESHOLD:
                        saved = dh.record_attendance(
                            curr_detected_id,
                            subject_id,
                            instructor_id_value,
                            convert(class_start_value),
                            convert(class_end_value)
                        )

                        if saved:
                            scan_data["status"] = "Attendance successfully recorded."
                        else:
                            scan_data["status"] = "Failed to record attendance."

                        legal_scans = 0
                        last_detected_id = None

            else:
                legal_scans = 0
                last_detected_id = None
                scan_data["student_id"] = curr_detected_id
                scan_data["student_name"] = ""
                scan_data["status"] = "Student ID not found."

        else:
            legal_scans = 0
            last_detected_id = None
            scan_data["student_id"] = ""
            scan_data["student_name"] = ""
            scan_data["status"] = "Waiting for scan..."


def get_processed_frame():
    # Functionality:
    # Reads one frame from the camera, processes attendance scanning, and returns the frame.
    cam = get_camera()

    if cam is None or not cam.isOpened():
        return None

    ret, frame = cam.read()
    if not ret or frame is None:
        return None

    x1, y1, x2, y2 = get_rect(frame)
    roi = frame[y1:y2, x1:x2]

    validate_attendance(frame, roi, instructor_id, class_start, class_end)
    return frame


def frame_to_jpeg_bytes(frame):
    # Functionality:
    # Converts an OpenCV frame to JPEG bytes for UI display.
    if frame is None:
        return None

    ret, buffer = cv2.imencode(".jpg", frame)
    if not ret:
        return None

    return buffer.tobytes()