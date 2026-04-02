# Smart Attendance System – GUI Branch (Frontend Integration)

## Project Structure

SmartAttendance/<br>
│<br>
├── GUI.py<br>
│<br>
├── templates/<br>
│ ├── MainDashboard.html<br>
│ ├── CameraPreview.html<br>
│ ├── ViewAttendance.html<br>
│ └── AttendanceList.html<br>
│<br>
└── static/<br>
├── Styles.css<br>
└── App.js<br>

## Running the System

### 1. Open the Project Folder
Open terminal or Git CMD inside the project directory where `GUI.py` is located.
Example:
cd path/to/SmartAttendance

---

### 2. Install Flask (only once)
pip install flask

---

### 3. Run the Application
python GUI.py
Expected output:
Running on http://127.0.0.1:5000/

---

### 4. Open in Browser
Go to:
http://127.0.0.1:5000/
This loads the Dashboard.

---

### 5. Navigate the System

Use the topbar:
- Dashboard
- Camera
- View Attendance
- Attendance List

Navigation is handled by Flask routes, not file links.

---

## Important Behavior

- Pages will NOT work if opened directly (double-click HTML)
- The system must always run through Flask
- All navigation depends on `GUI.py`

---

## Common Issues

### Blank Page / CSS Not Loading
Cause: Incorrect static paths  
# Fix: Ensure this is used in HTML:
{{ url_for('static', filename='Styles.css') }}
---

### Page Not Found (404)
Cause: Wrong route link  
# Fix: Use these routes:
/
/camera
/view-attendance
/attendance-list

---

### Flask Not Found
Cause: Flask not installed  
# Fix:
pip install flask

---

### Port Already in Use
#Fix:
python GUI.py --port 5001
Then open:
http://127.0.0.1:5001/
