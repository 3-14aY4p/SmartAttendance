from Database.db_connector import get_connection
import csv

def export_attendance(class_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.student_id, s.name, c.class_code,
               a.attendance_log, a.student_status
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        JOIN classes c ON a.class_id = c.class_id
        WHERE a.class_id = %s
        ORDER BY a.attendance_log DESC
    """, (class_id,))

    records = cursor.fetchall()

    with open("attendance.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Student ID", "Name", "Class", "DateTime", "Status"])
        writer.writerows(records)

    conn.close()
    return "CSV exported successfully."