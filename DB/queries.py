from db import get_connection

IRREGULAR_IDS = {
    '2024-4329-A', '2024-8088-I', '2024-2219-I', '2024-4548-A',
    '2024-6012-A', '2024-8045-A', '2024-6325-I', '2024-6609-I',
    '2024-4620-I', '2024-4418-A', '2024-8224-I', '2024-7159-A',
    '2024-0117-I', '2024-2695-I', '2024-0730-I'
}

IRREGULAR_SUBJECTS = ['ICT-107', 'ICT-110', 'ICT-111']


def get_all_subjects():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT subject_id FROM subjects_enrolled ORDER BY subject_id")
    subjects = [r[0] for r in cur.fetchall()]
    conn.close()
    return subjects


def get_students_for_subject(subject_id):
    conn = get_connection()
    cur = conn.cursor()

    if subject_id in IRREGULAR_SUBJECTS:
        cur.execute("""
            SELECT e.student_id, s.student_name
            FROM enrollment e
            JOIN student s ON e.student_id = s.student_id
            WHERE e.student_id NOT IN (
                '2024-4329-A','2024-8088-I','2024-2219-I',
                '2024-4548-A','2024-6012-A','2024-8045-A',
                '2024-6325-I','2024-6609-I','2024-4620-I',
                '2024-4418-A','2024-8224-I','2024-7159-A',
                '2024-0117-I','2024-2695-I','2024-0730-I'
            )
            ORDER BY s.student_name
        """)
    else:
        cur.execute("""
            SELECT e.student_id, s.student_name
            FROM enrollment e
            JOIN student s ON e.student_id = s.student_id
            ORDER BY s.student_name
        """)

    students = cur.fetchall()
    conn.close()
    return students


def get_all_students(filter_text=""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.student_id, s.student_name
        FROM student s
        JOIN enrollment e ON s.student_id = e.student_id
        ORDER BY s.student_name
    """)
    all_students = cur.fetchall()
    conn.close()

    if filter_text:
        all_students = [
            (sid, sname) for sid, sname in all_students
            if filter_text.lower() in sid.lower() or
               filter_text.lower() in sname.lower()
        ]
    return all_students


def get_instructor_for_subject(subject_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT instructor_id FROM subjects_enrolled WHERE subject_id=%s LIMIT 1",
        (subject_id,)
    )
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def get_existing_attendance(student_id, subject_id, att_date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT attendance_id FROM attendance
        WHERE student_id=%s AND subject_id=%s AND date=%s
    """, (student_id, subject_id, att_date))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def get_attendance_report(subject_id=None, date_from=None, date_to=None):
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT a.student_id, s.student_name, a.subject_id, a.date, a.is_present
        FROM attendance a
        JOIN student s ON a.student_id = s.student_id
        WHERE 1=1
    """
    params = []
    if subject_id and subject_id != "ALL":
        query += " AND a.subject_id = %s"
        params.append(subject_id)
    if date_from:
        query += " AND a.date >= %s"
        params.append(date_from)
    if date_to:
        query += " AND a.date <= %s"
        params.append(date_to)
    query += " ORDER BY a.date DESC, s.student_name"

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_all_attendance_for_export():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.student_id, s.student_name, a.subject_id,
               a.instructor_id, a.date, a.time,
               IF(a.is_present, 'Present', 'Absent') as status
        FROM attendance a
        JOIN student s ON a.student_id = s.student_id
        ORDER BY a.date DESC, s.student_name
    """)
    rows = cur.fetchall()
    conn.close()
    return rows