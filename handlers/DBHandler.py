import mysql.connector, csv
from mysql.connector import Error
from datetime import datetime, date, time


# connect to database
def get_connection():
    # Functionality:
    # Opens and returns a MySQL connection for the attendance database.
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


# OLD CODE KEPT FOR REFERENCE
# def close_connection():
#     if 'conn' in locals() and conn.is_connected():
#             curs.close()
#             conn.close()

# close connection to the database
def close_connection(conn=None, curs=None):
    # Functionality:
    # Safely closes the cursor and database connection created by the query functions.
    try:
        if curs is not None:
            curs.close()
    except Error as e:
        print(f"ERR closing cursor: {e}")

    try:
        if conn is not None and conn.is_connected():
            conn.close()
    except Error as e:
        print(f"ERR closing connection: {e}")


# validate existence of student_id
def query_student_id(student_id: str) -> dict:
    # Functionality:
    # Checks if the given student ID exists and returns the student name when found.
    conn = None
    curs = None

    try:
        conn = get_connection()
        if conn is None:
            return {"success": False, "name": ""}

        curs = conn.cursor(dictionary=True)

        # validate student existence
        curs.execute("SELECT student_name FROM tbl_student WHERE student_id = %s", (student_id,))
        student = curs.fetchone()

        if not student:
            return {"success": False, "name": ""}
        else:
            # OLD CODE KEPT FOR REFERENCE
            # return {"success": True, "name": student}
            # CHANGED: return only the actual student_name string
            return {"success": True, "name": student["student_name"]}

    except mysql.connector.Error as e:
        print(f"ERR: {e}")
        return {"success": False, "name": ""}

    finally:
        close_connection(conn, curs)


# validates if student is enrolled in a subject
def query_subject_enrollment(student_id: str, subject_id: str) -> dict:
    # Functionality:
    # Checks if the student is enrolled in the specified subject.
    conn = None
    curs = None
    
    try:
        conn = get_connection()
        if conn is None:
            return {"success": False, "name": ""}

        curs = conn.cursor(dictionary=True)

        curs.execute("""
            SELECT s.student_name
            FROM tbl_enrollment e
            JOIN tbl_student s ON e.student_id = s.student_id
            JOIN tbl_subjects_enrolled se ON se.enrollment_id = e.enrollment_id
            WHERE se.subject_id = %s 
                AND e.student_id = %s
        """, (subject_id, student_id,))
        student = curs.fetchone()

        if not student:
            return {"success": False, "name": ""}
        else:
            return {"success": True, "name": student["student_name"]}

    except mysql.connector.Error as e:
        print(f"ERR: {e}")
        return {"success": False, "name": ""}

    finally:
        close_connection(conn, curs)


# validates if student has has already recorded PRESENT or LATE for the day
def query_attendance(student_id: str, subject_id: str, date: date) -> bool:
    # Functionality:
    # Checks if the student already has a non-absent attendance record for the same subject and date.
    conn = None
    curs = None
    
    try:
        conn = get_connection()
        if conn is None:
            return False

        curs = conn.cursor()

        curs.execute("""
               SELECT a.attendance_id
               FROM tbl_attendance a
               JOIN tbl_enrollment e ON a.student_id = e.student_id
               JOIN tbl_subjects_enrolled se ON a.subject_id = se.subject_id
               WHERE a.student_id = %s
                    AND a.subject_id = %s
                    AND a.date = %s
                    AND a.attendance_status NOT IN ('Absent')
               """, (student_id, subject_id, date))

        if curs.fetchone():
            return True

        return False

    except mysql.connector.Error as e:
        print(f"ERR: {e}")
        return False

    finally:
        close_connection(conn, curs)


# for writing into database
def record_attendance(student_id: str, subject_id: str, instructor_id: str, class_start: time, class_end: time) -> bool:
    # Functionality:
    # Inserts a new attendance record and determines whether the student is Present, Late, or Absent.
    conn = None
    curs = None
    
    try:
        conn = get_connection()
        if conn is None:
            return False

        curs = conn.cursor()

        current_date = datetime.now().date()
        current_time = datetime.now().time()
        status: str = ""

        # OLD CODE KEPT FOR REFERENCE
        # date = datetime.now().date()
        # time = datetime.now().time()
        # if class_start <= time <= class_end:
        #     status = "Present"
        # elif time >= class_start:
        #     status = "Late"
        # elif time > class_end:
        #     status = "Absent"

        # CHANGED: fixed attendance status order and logic
        if current_time > class_end:
            status = "Absent"
        elif current_time > class_start:
            status = "Late"
        else:
            status = "Present"

        # date and time is set to input current date and time upon recording
        sql = """
              INSERT INTO tbl_attendance
              (subject_id, instructor_id, student_id, date, class_start, class_end, attendance_status)
              VALUES (%s, %s, %s, %s, %s, %s, %s)
              """

        # CHANGED: added date because tbl_attendance has a date column in the SQL schema
        curs.execute(sql, (subject_id, instructor_id, student_id, current_date, class_start, class_end, status))
        conn.commit()
        return True

    except mysql.connector.Error as e:
        print(f"ERR: {e}")
        return False

    finally:
        close_connection(conn, curs)