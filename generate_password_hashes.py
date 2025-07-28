from flask_bcrypt import Bcrypt
import mysql.connector

# Initialize bcrypt
bcrypt = Bcrypt()

# Define plain passwords for each student (for demo purposes)
passwords = {
    'alice@example.com': 'alice123',
    'bob@example.com': 'bob123'
}

# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Godblessbaby',  # your real MySQL password
    database='internlink'
)

cursor = conn.cursor()

# Hash and update passwords
# Hash and update passwords using email instead of id
for email, plain_password in passwords.items():
    hashed = bcrypt.generate_password_hash(plain_password).decode('utf-8')
    cursor.execute(
        "UPDATE students SET password_hash = %s WHERE email = %s",
        (hashed, email)
    )


conn.commit()
cursor.close()
conn.close()

print("Password hashes updated.")
