import mysql.connector, csv
from mysql.connector import Error
from datetime import datetime



# connect to database
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="Admin-110",
            password="attendance",
            database="db_SmartAttendance"
        )
        if conn.is_connected():
            return conn

    except Error as e:
        print(f"ERR: {e}")
        return None

# close connection to the database
def close_connection():
    if 'conn' in locals() and conn.is_connected():
            curs.close()
            conn.close()



# validate existence of student_id
def query_student_id(student_id: str) -> dict:
    conn = None
    curs = None

    try:
        conn = get_connection()
        curs = conn.cursor(dictionary=True)

        # validate student existence
        curs.execute("SELECT student_name FROM tbl_student WHERE student_id = %s", (student_id))
        student = curs.fetchone()

        if not student:
            return {"success": False}
        else:
            return {"success": True, "name": student}

    except mysql.connector.Error as e:
        print(f"ERR: {e}")
        return {"success": False}

# validates if student is enrolled in a subject
def query_subject_enrollment(student_id: str, subject_id: str) -> dict:
    conn = None
    curs = None

    try:
        conn = get_connection()
        curs = conn.cursor(dictionary=True)

        curs.execute("""
            SELECT s.student_name
            FROM tbl_enrollment e
            JOIN tbl_student s ON e.student_id = s.student_id
            JOIN tbl_subjects_enrolled se ON se.enrollment_id = e.enrollment_id
            WHERE se.subject_id = %s 
                AND e.student_id = %s
        """, (subject_id, student_id))
        student = curs.fetchone()

        if not student:
            return {"success": False}
        else:
            return {"success": True, "name": student}

    except mysql.connector.Error as e:
        print(f"ERR: {e}")
        return False

# validates if student has has already recorded attendance for the day
def query_attendance(student_id: str, subject_id: str, date: str):
    conn = None
    curs = None

    try:
        conn = get_connection()
        curs = conn.cursor(dictionary=True)

        curs.execute("""
               SELECT a.attendance_id
               FROM tbl_attendance a
               JOIN tbl_enrollment e ON a.student_id = e.student_id
               JOIN tbl_subjects_enrollment se ON a.subject_id = se.subject_id
               WHERE a.student_id = %s
                    AND a.subject_id = %s
                    AND a.date = %s
               """, (student_id,  subject_id, date))

        if curs.fetchone():
            return True

    except mysql.connector.Error as e:
        print(f"ERR: {e}")
        return False



# for writing into database
def record_attendance(student_id: str, subject_id: str, instructor_id: str, class_start: str, class_end: str):
    conn = None
    curs = None

    try:
        conn = get_connection()
        curs = conn.cursor(dictionary=True)

        # date = datetime.now().strftime('%Y-%m-%d')
        time = datetime.now().strftime('%H:%M:%S')
        status: str = ""

        # command to alter attendance_status
        # this determines if student is LATE
        if class_start <= time <= class_end - 10:
            status = "Present"
        elif time >= class_start + 10:
            status = "Late"
        elif time > class_end:
            status = "Absent"

        # date and time is set to input current date and time upon recording
        sql = """
              INSERT INTO tbl_attendance (subject_id, instructor_id, student_id, class_start, class_end, attendance_status)
              VALUES (%s, %s, %s, %s, %s, %s) \
              """

        curs.execute(sql, (subject_id, instructor_id, student_id, class_start, class_end, status))
        conn.commit()

    except mysql.connector.Error as e:
        print(f"ERR: {e}")
        return False