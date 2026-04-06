# prebuilt modules
from datetime import datetime
import time, platform, re, pytesseract, cv2
import numpy as np

# custom modules
import DBHandler as dh



# for Windows (I use Linux; I don't need this -Pia)
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# color
color_grn = (0, 255, 0)
color_red = (0, 0, 255)

# time variables
scan_interval: float = 1.0
current_time: float = 0.0
last_scanned: float = 0.0

# ID capture variables
previous_roi = None
last_detected_id = None
curr_detected_id = None

# scan counters
STABLE_SCAN_THRESHOLD: int = 2
legal_scans: int = 0

# tesseract config for OCR
conf = r"--psm 7 --oem 1 tessedit_char_whitelist=0123456789-AI"

# scan_data for HTML/FLask frontend
scan_data = {
    "student_id": "",
    "student_name": "",
    "status": "Waiting for scan...",
}

# should be editable through GUI
subject_id = "ICT-110"
instructor_id = "005"
class_start = "13:00"
class_end = "16:00"




camera = cv2.VideoCapture(0) # change to (1) if external camera

# return scan_data to flask
def get_scan_data() -> dict:
    return scan_data

def convert(time):
    format = '%I:%M%p'
    time_str = datetime.strptime(time, "%H:%M").time()

    return time_str

def get_rect(frame):
    h, w, _ = frame.shape
    x1 = int(w * 0.3)
    y1 = int(h * 0.55)
    x2 = int(w * 0.7)
    y2 = int(h * 0.7)

    return x1, y1, x2, y2

def draw_rect(frame, color: tuple):
    x1, y1, x2, y2 = get_rect(frame)

    # cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    
    cv2.line(frame, (x1,y1), (x1+15,y1), color, 2)
    cv2.line(frame, (x1,y1), (x1,y1+15), color, 2)
    cv2.line(frame, (x1,y2), (x1+15,y2), color, 2)
    cv2.line(frame, (x1,y2), (x1,y2-15), color, 2)
    cv2.line(frame, (x2,y1), (x2-15,y1), color, 2)
    cv2.line(frame, (x2,y1), (x2,y1+15), color, 2)
    cv2.line(frame, (x2,y2), (x2-15,y2), color, 2)
    cv2.line(frame, (x2,y2), (x2,y2-15), color, 2)

# read ROI and run the OCR to detect the ID in frame
def scan_for_id(roi) -> str:
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

    # COOMON ISSUE!! - bandaid/temporary fix -
    # correct the program in mistaking -I as 4
    if re.match(r"\d{4}-\d{4}4", text):
        text = text[:-1] + "-I"

    # return match result if it exists
    match = re.search(r"\d{4}-\d{4}-[A-Z]", text)
    if match:
        return match.group()
    else:
        return None

# scan and validate existence of student and attendance
def validate_attendance(frame, roi, instructor_id: str = '005', class_start: str = "07:30", class_end: str = "9:00") -> void:
    global current_time, last_scanned, curr_detected_id, last_detected_id, previous_roi, legal_scans
    
    # date and time today
    td_date = datetime.now().date()
    td_time = datetime.now().time()
    
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
            # validate existence of the student
            student = dh.query_student_id(curr_detected_id)

            if student.get("success"):
                student_name = (
                    student.get("name")
                    or ""
                )

                has_record = False
                if dh.query_attendance(curr_detected_id, subject_id, td_date):
                    has_record = True
                
                # validate student's enrollment on a subject
                if dh.query_subject_enrollment(curr_detected_id, subject_id):
                    if has_record:
                        legal_scans = 0
                        scan_data["student_id"] = curr_detected_id
                        scan_data["student_name"] = student_name
                        scan_data["status"] = "Attendance record found."
                    else:
                        legal_scans += 1
                        scan_data["student_id"] = curr_detected_id
                        scan_data["student_name"] = student_name
                        scan_data["status"] = "HOLD ID Card in place."
                
                else:
                    legal_scans = 1
                    last_detected_id = curr_detected_id
                    scan_data["student_id"] = curr_detected_id
                    scan_data["student_name"] = student_name
                    scan_data["status"] = "HOLD ID Card in place."

                if legal_scans >= STABLE_SCAN_THRESHOLD and not has_record:
                    dh.record_attendance(curr_detected_id, subject_id, instructor_id, convert(class_start), convert(class_end))

                    scan_data["student_id"] = curr_detected_id
                    scan_data["student_name"] = student_name
                    scan_data["status"] = "Attendance successfully recorded."

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



# MAIN CAMERA LOOP
def generate_frames():
    while True:
        # read camera frames
        ret, frame = camera.read()
        if not ret:
            break

        # draw id_area/roi rectangle
        x1, y1, x2, y2 = get_rect(frame)
        roi = frame[y1:y2, x1:x2]
        
        validate_attendance(frame, roi)

        # converts frames for browser streaming
        ret, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
        )
    
#         cv2.imshow("camera preview", frame)

#         # end loop manually
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     camera.release()
#     cv2.destroyAllWindows()

# generate_frames()
