import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',           # replace with your MySQL username
        password='Godblessbaby',  # replace with your MySQL password
        database='internlink'
    )
    return conn


