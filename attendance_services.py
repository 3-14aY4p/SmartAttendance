from db import get_connection
from datetime import datetime, date

IRREGULAR_IDS = {
    '2024-4329-A', '2024-8088-I', '2024-2219-I', '2024-4548-A',
    '2024-6012-A', '2024-8045-A', '2024-6325-I', '2024-6609-I',
    '2024-4620-I', '2024-4418-A', '2024-8224-I', '2024-7159-A',
    '2024-0117-I', '2024-2695-I', '2024-0730-I'
}

IRREGULAR_BLOCKED_SUBJECTS = ['ICT-107', 'ICT-110', 'ICT-111']


def mark_attendance(student_id, class_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT subject_id, instructor_id
            FROM subjects_enrolled
            WHERE id = %s
        """, (class_id,))
        row = cur.fetchone()

        if not row:
            print(f"[ERROR] No class found with id={class_id}")
            conn.close()
            return False

        subject_id    = row[0]
        instructor_id = row[1]

        # Block irregular students from ICT-107, ICT-110, ICT-111
        if student_id in IRREGULAR_IDS and subject_id in IRREGULAR_BLOCKED_SUBJECTS:
            print(f"[BLOCKED] {student_id} is irregular and cannot attend {subject_id}")
            conn.close()
            return False

        today    = str(date.today())
        time_now = datetime.now().strftime("%H:%M:%S")

        cur.execute("""
            SELECT attendance_id FROM attendance
            WHERE student_id = %s AND subject_id = %s AND date = %s
        """, (student_id, subject_id, today))
        existing = cur.fetchone()

        if existing:
            cur.execute("""
                UPDATE attendance SET is_present = 1, time = %s
                WHERE attendance_id = %s
            """, (time_now, existing[0]))
            print(f"[UPDATED] Attendance updated for {student_id} in {subject_id}")
        else:
            cur.execute("""
                INSERT INTO attendance (subject_id, instructor_id, student_id, date, time, is_present)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (subject_id, instructor_id, student_id, today, time_now, 1))
            print(f"[SAVED] Attendance saved for {student_id} in {subject_id}")

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(f"[ERROR] mark_attendance failed: {e}")
        return False