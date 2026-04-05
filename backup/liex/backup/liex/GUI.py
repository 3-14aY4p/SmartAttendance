# required for streaming + JSON
from flask import Flask, render_template, Response, jsonify
# connects backend logic
# from CVHandler import generate_frames, get_scan_data

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("MainDashboard.html")

@app.route("/camera")
def camera_page():
    return render_template("CameraPreview.html")

@app.route("/view-attendance")
def view_attendance():
    return render_template("ViewAttendance.html")

@app.route("/attendance-list")
def attendance_list():
    return render_template("AttendanceList.html")

# # serves camera stream
# @app.route("/video_feed")
# def video_feed():
#     return Response(
#         generate_frames(),
#         mimetype="multipart/x-mixed-replace; boundary=frame"
#     )

# # serves OCR results as JSON
# @app.route("/scan_data")
# def scan_data():
#     return jsonify(get_scan_data())

if __name__ == "__main__":
    app.run(debug=True)
