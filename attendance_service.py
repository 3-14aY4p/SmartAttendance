from datetime import datetime
from db import get_connection
import mysql.connector


def mark_attendance(student_id, class_id):
    # Using 'with' ensures the connection closes even if an error occurs
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)  # Returns results as a dictionary

        # 1. Validate student existence
        cursor.execute("SELECT name FROM students WHERE student_id = %s", (student_id,))
        student = cursor.fetchone()

        if not student:
            return {"success": False, "message": f"Student ID {student_id} not found!"}

        # 2. Check if already marked (prevents double-marking for the same day)
        today = datetime.now().date()
        cursor.execute("""
                       SELECT attendance_id
                       FROM attendance
                       WHERE student_id = %s
                         AND class_id = %s
                         AND DATE (datetime) = %s
                       """, (student_id, class_id, today))

        if cursor.fetchone():
            return {"success": False, "message": "Attendance already marked for today!"}

        # 3. Insert as "Present"
        sql = """
              INSERT INTO attendance (class_id, student_id, datetime, status)
              VALUES (%s, %s, %s, %s) \
              """
        # Ensure the date format matches your SQL column (usually 'YYYY-MM-DD HH:MM:SS')
        cursor.execute(sql, (class_id, student_id, datetime.now(), "Present"))
        conn.commit()

        return {"success": True, "message": f"Success! {student['name']} is marked Present."}

    except mysql.connector.Error as err:
        return {"success": False, "message": f"Database error: {err}"}

    finally:
        # Final cleanup to prevent "Too many connections" errors
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()