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


# validate existence of student_id
def query_student_id(student_id) -> dict:
    conn = None
    curs = None

    try:
        conn = get_connection()
        curs = conn.cursor(dictionary=True)

        # validate student existence
        curs.execute("SELECT name FROM students WHERE student_id = %s", (student_id,))
        student = curs.fetchone()

        if not student:
            return {"success": False}
        else:
            return {"success": True, "name": student}

    except mysql.connector.Error as e:
        print(f"ERR: {e}")
        return {"success": False}

    finally:
        if 'conn' in locals() and conn.is_connected():
            curs.close()
            conn.close()

# TBI: def query_enrollment(student_id, class_code, section):
# for checking if the student is enrolled in the class
def query_enrollment(student_id, class_id) -> bool:
    conn = None
    curs = None

    try:
        conn = get_connection()
        curs = conn.cursor(dictionary=True)

        # validate student existence
        curs.execute("SELECT student_id AND class_id FROM enrollments WHERE student_id = %s AND class_id = %s", (student_id, class_id))
        student = curs.fetchone()

        if not student:
            return False
        else:
            return True

    except mysql.connector.Error as e:
        print(f"ERR: {e}")
        return False

    finally:
        if 'conn' in locals() and conn.is_connected():
            curs.close()
            conn.close()

# checks if student has already logged in
def query_attendance(student_id, class_id, date_logged):
    conn = None
    curs = None

    try:
        conn = get_connection()
        curs = conn.cursor(dictionary=True)

        curs.execute("""
               SELECT attendance_id
               FROM attendance
               WHERE student_id = %s
                 AND class_id = %s
                 AND DATE (datetime) = %s
               """, (student_id, class_id, date_logged))

        if curs.fetchone():
            return True

    except mysql.connector.Error as e:
        print(f"ERR: {e}")
        return False

    # commented it because of an error; might fix later if needed
    # finally:
    #     if 'conn' in locals() and conn.is_connected():
    #         curs.close()
    #         conn.close()

# for writing into database
def record_attendance(student_id, class_id):
    conn = None
    curs = None

    try:
        conn = get_connection()
        curs = conn.cursor(dictionary=True)

        sql = """
              INSERT INTO attendance (class_id, student_id, datetime, status)
              VALUES (%s, %s, %s, %s) \
              """
        # ensures the date format matches the SQL column ('YYYY-MM-DD HH:MM:SS')
        curs.execute(sql, (class_id, student_id, datetime.now(), "Present"))
        conn.commit()

    except mysql.connector.Error as e:
        print(f"ERR: {e}")
        return False

    finally:
        if 'conn' in locals() and conn.is_connected():
            curs.close()
            conn.close()

# for exporting into csv
def export_attendance(class_id, date):
    pass