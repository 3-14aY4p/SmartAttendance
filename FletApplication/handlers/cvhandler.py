import cv2
import base64
import time
import pytesseract
import re

def extract_id(text):
    text = text.upper().replace(" ", "")
    match = re.search(r"\d{4}-\d{4}-[A-Z]", text)
    return match.group(0) if match else None

def update_frames(page, image_control, on_detect):
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera.set(cv2.CAP_PROP_FPS, 15)

    last_detected = None

    while True:
        ret, frame = camera.read()
        if not ret:
            time.sleep(0.033)
            continue

        h, w = frame.shape[:2]

        # Scan box — wide and short
        box_w, box_h = 320, 80
        x1 = (w - box_w) // 2
        y1 = (h - box_h) // 2
        x2 = x1 + box_w
        y2 = y1 + box_h

        # Crop region inside box and run OCR
        roi = frame[y1:y2, x1:x2]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        text = pytesseract.image_to_string(thresh, config="--psm 7")
        detected = extract_id(text)

        if detected and detected != last_detected:
            last_detected = detected
            on_detect(detected)

        # Draw red scan box on frame
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

        ok, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
        if ok:
            frame_b64 = base64.b64encode(buffer).decode()

            async def do_update(b64=frame_b64):
                image_control.src = f"data:image/jpeg;base64,{b64}"
                image_control.update()

            page.run_task(do_update)

        time.sleep(0.066)