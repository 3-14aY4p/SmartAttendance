from flask import Flask, render_template, Response, jsonify
from CVHandler import generate_frames, get_scan_data

app = Flask(__name__)


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/scanner")
def camera_page():
    return render_template("scanner.html")


@app.route("/attendance-log")
def view_attendance():
    return render_template("attendance_log.html")


@app.route("/class-list")
def attendance_list():
    return render_template("class_list.html")


@app.route("/class-item")
def class_item():
    return render_template("class_item.html")


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/scan_data")
def scan_data():
    return jsonify(get_scan_data())


if __name__ == "__main__":
    app.run()