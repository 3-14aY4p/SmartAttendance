import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Ensure your password is correct
            database="smart_attendance"
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None