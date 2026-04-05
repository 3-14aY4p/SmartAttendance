# prebuilt modules
from datetime import datetime
import time, platform, re
import pytesseract, cv2
import numpy as np

# custom modules
import DatabaseHandler as dh


# for Windows (I use Linux; I don't need this -Pia)
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# time variables
current_time: float = 0.0
last_scanned: float = 0.0
scan_interval: float = 1.0

# ID capture variables
previous_roi = None
last_detected_id = None
curr_detected_id = None

# scan counters
STABLE_SCAN_THRESHOLD: int = 3
legal_scans: int = 0

# tesseract config for OCR
conf = r"--psm 7 --oem 1 tessedit_char_whitelist=0123456789-AI"

# shared state for frontend
scan_data = {
    "student_id": "",
    "student_name": "",
    "status": "Waiting for scan..."
}

camera = cv2.VideoCapture(0) # change to (1) if external camera

# read ROI and process OCR
def ocr(roi):
    # preprocessing stuffs; cleaning up the image
    rz = 3  # resize multiplier

    p_img = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    p_img = cv2.resize(p_img, None, fx=rz, fy=rz, interpolation=cv2.INTER_CUBIC)
    p_img = cv2.GaussianBlur(p_img, (5, 5), 0)
    _, p_img = cv2.threshold(p_img, 0, 255,
         cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # text extraction
    text = pytesseract.image_to_string(p_img, config=conf)
    text = text.strip()

    # to correct the program mistaking -I as 4
    if re.match(r"\d{4}-\d{4}4", text):
        text = text[:-1] + "-I"

    # return match result if it exists
    match = re.search(r"\d{4}-\d{4}-[A-Z]", text)
    if match:
        return match.group()
    else:
        return None

# returns scan data to Flask
def get_scan_data():
    return scan_data

# camera streaming (replaces cv2.imshow for web)
def generate_frames():
    global current_time, last_scanned, curr_detected_id, last_detected_id, previous_roi, legal_scans, scan_data

    # TEMPORARY; make this modifiable for next time
    subject_id = 1
    today = datetime.now().date()

    while True:
        # read camera frames
        retval, frame = camera.read()
        if not retval:
            break

        # draw id_area/roi rectangle
        h, w, _ = frame.shape
        x1 = int(w * 0.3)
        y1 = int(h * 0.55)
        x2 = int(w * 0.7)
        y2 = int(h * 0.7)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

        roi = frame[y1:y2, x1:x2]
        current_time = time.time()

        # scans only after each interval has passed; saves on resources
        if current_time - last_scanned > scan_interval:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            curr_detected_id = ocr(roi)
            previous_roi = roi.copy()
            last_scanned = current_time

            # guard before DB queries
            if curr_detected_id:
                # reused query result
                student_result = dh.query_student_id(curr_detected_id)

                # changed stored query result first so it can also be reused for frontend data
                if student_result.get("success"):
                    # added attempt to read name if available from database result
                    student_name = (
                        student_result.get("student_name")
                        or student_result.get("name")
                        or student_result.get("full_name")
                        or ""
                    )

                    # need to transfer these into the GUI so we can add the schedule
                    # changed this condition to preserve your original logic exactly
                    if dh.query_subject_enrollment(curr_detected_id, subject_id):
                        legal_scans += 1
                        scan_data["student_id"] = curr_detected_id
                        scan_data["student_name"] = student_name
                        scan_data["status"] = f"< please HOLD for {STABLE_SCAN_THRESHOLD - legal_scans}s >"
                    elif dh.query_attendance(curr_detected_id, subject_id, today):
                        legal_scans = 0
                        scan_data["student_id"] = curr_detected_id
                        scan_data["student_name"] = student_name
                        scan_data["status"] = "ATTENDANCE RECORDED."
                    else:
                        legal_scans = 1
                        last_detected_id = curr_detected_id
                        scan_data["student_id"] = curr_detected_id
                        scan_data["student_name"] = student_name
                        scan_data["status"] = f"< please HOLD for {STABLE_SCAN_THRESHOLD - legal_scans}s >"

                    if legal_scans >= STABLE_SCAN_THRESHOLD:
                        dh.record_attendance(curr_detected_id, subject_id)

                        scan_data["student_id"] = curr_detected_id
                        scan_data["student_name"] = student_name
                        scan_data["status"] = "ATTENDANCE RECORDED."

                        legal_scans = 0
                        last_detected_id = None
                else:
                    legal_scans = 0
                    scan_data["student_id"] = curr_detected_id
                    scan_data["student_name"] = ""
                    scan_data["status"] = "Student ID not found."
            else:
                legal_scans = 0
                scan_data["student_id"] = ""
                scan_data["student_name"] = ""
                scan_data["status"] = "Waiting for scan..."

        # CAN BE REMOVED AFTER Frontend INTEGRATION;
        # camera preview and user hinting
        cv2.putText(frame,
            f"Detected ID: {curr_detected_id}",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2)

        # changed this part to use scan_data status so HTML and frame text match
        cv2.putText(frame,
            scan_data["status"],
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2)

        # converts frames for browser streaming
        ret, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
        )

# MAIN LOOP
def scanner():
    global current_time, last_scanned, curr_detected_id, last_detected_id, previous_roi, legal_scans, scan_data

    # TEMPORARY; make this modifiable for next time
    subject_id = 1
    today = datetime.now().date()

    while True:
        # read camera frames
        retval, frame = camera.read()
        if not retval:
            break

        # draw id_area/roi rectangle
        h, w, _ = frame.shape
        x1 = int(w * 0.3)
        y1 = int(h * 0.55)
        x2 = int(w * 0.7)
        y2 = int(h * 0.7)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

        roi = frame[y1:y2, x1:x2]
        current_time = time.time()

        # scans only after each interval has passed; saves on resources
        if current_time - last_scanned > scan_interval:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            curr_detected_id = ocr(roi)
            previous_roi = roi.copy()
            last_scanned = current_time

            # changed added guard so database is not queried with None
            if curr_detected_id:
                student_result = dh.query_student_id(curr_detected_id)

                # need to transfer these into the GUI so we can add the schedule
                if student_result.get("success"):
                    # added attempt to read name if available from database result
                    student_name = (
                        student_result.get("student_name")
                        or student_result.get("name")
                        or student_result.get("full_name")
                        or ""
                    )

                    if dh.query_subject_enrollment(curr_detected_id, subject_id):
                        legal_scans += 1
                        scan_data["student_id"] = curr_detected_id
                        scan_data["student_name"] = student_name
                        scan_data["status"] = f"< please HOLD for {STABLE_SCAN_THRESHOLD - legal_scans}s >"
                    elif dh.query_attendance(curr_detected_id, subject_id, today):
                        legal_scans = 0
                        scan_data["student_id"] = curr_detected_id
                        scan_data["student_name"] = student_name
                        scan_data["status"] = "ATTENDANCE RECORDED."
                    else:
                        legal_scans = 1
                        last_detected_id = curr_detected_id
                        scan_data["student_id"] = curr_detected_id
                        scan_data["student_name"] = student_name
                        scan_data["status"] = f"< please HOLD for {STABLE_SCAN_THRESHOLD - legal_scans}s >"

                    if legal_scans >= STABLE_SCAN_THRESHOLD:
                        dh.record_attendance(curr_detected_id, subject_id)

                        scan_data["student_id"] = curr_detected_id
                        scan_data["student_name"] = student_name
                        scan_data["status"] = "ATTENDANCE RECORDED."

                        legal_scans = 0
                        last_detected_id = None
                else:
                    legal_scans = 0
                    scan_data["student_id"] = curr_detected_id
                    scan_data["student_name"] = ""
                    scan_data["status"] = "Student ID not found."
            else:
                legal_scans = 0
                scan_data["student_id"] = ""
                scan_data["student_name"] = ""
                scan_data["status"] = "Waiting for scan..."

        # CAN BE REMOVED AFTER Frontend INTEGRATION;
        # camera preview and user hinting
        cv2.putText(frame,
            f"Detected ID: {curr_detected_id}",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2)

        # changed this block to avoid querying attendance with None and to keep GUI data synced
        if scan_data["status"] == "ATTENDANCE RECORDED.":
            cv2.putText(frame,
                "ATTENDANCE RECORDED.",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2)
        else:
            if legal_scans != 0:
                cv2.putText(frame,
                    f"< please HOLD for {STABLE_SCAN_THRESHOLD - legal_scans}s >",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2)

        cv2.imshow("camera preview", frame)

        # end loop manually
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()