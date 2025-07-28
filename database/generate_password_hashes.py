from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# List of passwords you want to hash
passwords = [
    "Admin123!", "Employer123!", "Student123!",
    "Student123!", "Student123!", "Student123!", "Student123!", "Student123!"
]

for i, plain_password in enumerate(passwords, 1):
    hashed = bcrypt.generate_password_hash(plain_password).decode('utf-8')
    print(f"Password {i} ({plain_password}): {hashed}")
