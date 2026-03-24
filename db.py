import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",  # Add your MySQL password here if you have one
    "database": "smart_attendance"
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)