import time, platform
import re, cv2, pytesseract
import numpy as np

# for Windows (I use Linux; I don't need this -Pia)
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

camera = cv2.VideoCapture(0)

previous_roi = None

curr_time: float = 0.0
last_scan_time: float = 0.0
sc_interval: float = 1.0

detected_id = None
last_detected_id = None

legal_scans: int = 0
STABLE_SCAN_THRESHOLD: int = 3

# replace this with Attendance Entity DB
attendance_list = set()

# tesseract config for OCR
conf = r"--psm 7 --oem 1 tessedit_char_whitelist=0123456789-AI"


def run_ocr(roi):
    # preprocessing stuffs idk
    rz = 3  # resize multiplier

    processed_img = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.resize(processed_img, None, fx=rz, fy=rz, interpolation=cv2.INTER_CUBIC)
    processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0)
    _, processed_img = cv2.threshold(
        processed_img, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # text extraction
    text = pytesseract.image_to_string(processed_img, config=conf)
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


def roi_changed(curr_roi, prev_roi, threshold=50000):
    if previous_roi is None:
        return True

    # gets the difference of the pixel values compared
    diff = cv2.absdiff(curr_roi, prev_roi)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    motion_score = np.sum(gray)

    if motion_score > threshold:
        return True
    else:
        return False


# MAIN CAMERA AND DETECTION LOOP
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
    curr_time = time.time()

    # only scans after the specified interval
    if curr_time - last_scan_time > sc_interval and roi_changed(roi, previous_roi):
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        detected_id = run_ocr(roi)
        previous_roi = roi.copy()
        last_scan_time = curr_time

        if detected_id:
            if detected_id in attendance_list:
                legal_scans = 0
                last_detected_id = None
            elif detected_id == last_detected_id:
                legal_scans += 1
            else:
                legal_scans = 1
                last_detected_id = detected_id

            if legal_scans >= STABLE_SCAN_THRESHOLD:
                attendance_list.add(detected_id)

                legal_scans = 0
                last_detected_id = None

        else:
            legal_scans = 0

    # these can be removed after GUI integration;
    # camera preview and user hinting
    cv2.putText(frame,
            f"Detected ID: {detected_id}",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2)

    if detected_id in attendance_list:
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
                f"< stabilizes in {STABLE_SCAN_THRESHOLD - legal_scans}s >",
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