import csv
import os
from datetime import date
from models import get_attendance_report, get_all_attendance_for_export


def generate_report(subject_id=None, date_from=None, date_to=None):
    """
    Fetch attendance records filtered by subject and date range.
    Returns list of tuples and summary counts.
    """
    rows = get_attendance_report(subject_id, date_from, date_to)
    present_count = sum(1 for r in rows if r[4])
    absent_count  = sum(1 for r in rows if not r[4])
    return rows, present_count, absent_count


def export_to_csv():
    """
    Export all attendance records to CSV on the Desktop.
    Returns (success: bool, message: str)
    """
    rows = get_all_attendance_for_export()

    if not rows:
        return False, "No attendance data to export."

    filename = f"attendance_report_{date.today()}.csv"
    filepath = os.path.join(os.path.expanduser("~"), "Desktop", filename)

    try:
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Student ID", "Student Name", "Subject",
                "Instructor ID", "Date", "Time", "Status"
            ])
            writer.writerows(rows)
        return True, f"✅ Saved to Desktop:\n{filename}\n\n{len(rows)} records exported."
    except Exception as e:
        return False, f"Export failed: {e}"