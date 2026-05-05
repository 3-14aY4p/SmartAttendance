import cv2
import base64
import time
import pytesseract
import re
import os


# ── Tesseract path (Windows) ──────────────────────────────────────────────────
# If tesseract.exe is not on your system PATH, set the full path here.
_TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if os.path.isfile(_TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = _TESSERACT_PATH

# color tuples for the roi rect
color_red = (0, 0, 255)
color_grn = (0, 255, 0)

# tesseract config — note the leading '-c' before tessedit_char_whitelist
conf = r"--psm 7 --oem 1 -c tessedit_char_whitelist=0123456789-AI"


# ── camera lifecycle ──────────────────────────────────────────────────────────

_camera: cv2.VideoCapture | None = None

def open_camera(index: int = 0) -> bool:
    global _camera
    _camera = cv2.VideoCapture(index)
    _camera.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
    _camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    _camera.set(cv2.CAP_PROP_FPS, 30)
    return _camera.isOpened()

def close_camera() -> None:
    global _camera
    if _camera and _camera.isOpened():
        _camera.release()
    _camera = None


# ── ROI helpers ───────────────────────────────────────────────────────────────

def get_roi_rect(frame):
    h, w = frame.shape[:2]
    box_w, box_h = 320, 80
    x1 = (w - box_w) // 2
    y1 = (h - box_h) // 2
    x2 = x1 + box_w
    y2 = y1 + box_h
    return x1, x2, y1, y2


def draw_roi_rect(frame, color) -> None:
    x1, x2, y1, y2 = get_roi_rect(frame)
    arm = 15  # corner arm length

    # top-left
    cv2.line(frame, (x1, y1), (x1 + arm, y1), color, 2)
    cv2.line(frame, (x1, y1), (x1, y1 + arm), color, 2)
    # bottom-left
    cv2.line(frame, (x1, y2), (x1 + arm, y2), color, 2)
    cv2.line(frame, (x1, y2), (x1, y2 - arm), color, 2)
    # top-right
    cv2.line(frame, (x2, y1), (x2 - arm, y1), color, 2)
    cv2.line(frame, (x2, y1), (x2, y1 + arm), color, 2)
    # bottom-right
    cv2.line(frame, (x2, y2), (x2 - arm, y2), color, 2)
    cv2.line(frame, (x2, y2), (x2, y2 - arm), color, 2)


# ── OCR ───────────────────────────────────────────────────────────────────────

# Expected format: DDDD-DDDD-A  (4 digits, dash, 4 digits, dash, one letter)
_ID_PATTERN = re.compile(r"\d{4}-\d{4}-[A-Z]")

def extract_id(roi) -> str | None:
    rz = 5  # upscale multiplier for better OCR accuracy

    p_img = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    p_img = cv2.resize(p_img, None, fx=rz, fy=rz, interpolation=cv2.INTER_CUBIC)
    p_img = cv2.GaussianBlur(p_img, (5, 5), 0)
    _, p_img = cv2.threshold(p_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    text = pytesseract.image_to_string(p_img, config=conf).strip()

    # Tesseract sometimes reads the trailing '-I' suffix as '4'
    # e.g. "1234-56784" should be "1234-5678-I"
    text = re.sub(r"(\d{4}-\d{4})4$", r"\1-I", text)

    match = _ID_PATTERN.search(text)
    return match.group() if match else None


# ── main capture loop ─────────────────────────────────────────────────────────

def capture_frames(page, image_control, on_scan) -> None:
    """
    Runs the camera loop.  Call this in a background thread.
    - on_scan(detected_id: str, success: bool) is called ONLY when the
      detected ID changes (new scan) or when a previously detected ID is
      lost (called once with ("", False)).
    """
    global _camera

    if _camera is None or not _camera.isOpened():
        if not open_camera():
            print("ERR [capture_frames]: could not open camera")
            return

    last_detected_id: str | None = None
    no_detect_reported = True   # True = we've already told the caller there's nothing

    while True:
        retv, frame = _camera.read()
        if not retv:
            time.sleep(1 / 30)
            continue

        x1, x2, y1, y2 = get_roi_rect(frame)
        roi = frame[y1:y2, x1:x2]
        detected_id = extract_id(roi)

        if detected_id:
            draw_roi_rect(frame, color_grn)
            no_detect_reported = False

            if detected_id != last_detected_id:
                # New ID scanned — notify caller
                last_detected_id = detected_id
                on_scan(detected_id, True)

        else:
            draw_roi_rect(frame, color_red)

            if last_detected_id is not None and not no_detect_reported:
                # ID just disappeared — notify caller once
                last_detected_id = None
                no_detect_reported = True
                on_scan("", False)

        # Encode frame and push to Flet UI
        ret, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
        if ret:
            frame_b64 = base64.b64encode(buffer).decode()

            async def update_frame(b64=frame_b64):
                image_control.src = f"data:image/jpeg;base64,{b64}"
                image_control.update()

            page.run_task(update_frame)

        time.sleep(1 / 30)