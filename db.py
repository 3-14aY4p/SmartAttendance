import mysql.connector

def get_connection():
    # Replace these with your actual database credentials
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="smart_attendance"
    )