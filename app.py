from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
import mysql.connector


app = Flask(__name__)
app.secret_key = 'supersecretkey'  # for sessions
bcrypt = Bcrypt(app)


# Step 1: Function to connect to your MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',  # or your MySQL username
        password='Godblessbaby',  # replace with your real MySQL password
        database='internlink'  # make sure this matches your DB name
    )

# Step 2: API route to get students
@app.route("/students")
def get_students():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return jsonify({"students": students})

# Step 3: API route to get employers
@app.route("/employers")
def get_employers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employers")
    employers = cursor.fetchall()
    conn.close()
    return jsonify({"employers": employers})

# Step 4: API route to get internships
@app.route("/api/internships")
def get_internships():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM internships")
    internships = cursor.fetchall()
    conn.close()
    return jsonify({"internships": internships})

# Step 4.1: API route to apply for an internship
@app.route("/api/apply", methods=["POST"])
def apply_for_internship():
    # TEMPORARY: Simulate a logged-in student
    session['user_id'] = 1  # replace with a real student ID from your DB
    session['role'] = 'student'

    print("Session at apply:", session) # Debugging line to check session state
    if 'user_id' not in session or session.get('role') != 'student':
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()
    internship_id = data.get("internship_id")
    student_id = session["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO applications (student_id, internship_id) VALUES (%s, %s)",
            (student_id, internship_id)
        )
        conn.commit()
        return jsonify({"message": "Application submitted successfully!"})
    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"Error: {str(e)}"}), 500
    finally:
        conn.close()


# Step 5: API route to get applications
@app.route('/applications_detailed')
def get_applications_detailed():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT 
            a.id,
            s.name AS student_name,
            s.email AS student_email,
            i.title AS internship_title,
            e.name AS employer_name,
            a.application_date,
            a.status
        FROM applications a
        JOIN students s ON a.student_id = s.id
        JOIN internships i ON a.internship_id = i.id
        JOIN employers e ON i.employer_id = e.id
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({'applications': results})

# Optional: Home route
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['role'] = 'student' # Assuming role is student for this example
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard_student'))  # You can change this target
        else:
            flash('Invalid credentials.', 'danger')

    return render_template('login.html')

from flask import request
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/api/login", methods=["POST"])
def student_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE email = %s", (email,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()

    if student and bcrypt.check_password_hash(student["password_hash"], password):
        return jsonify({"message": "Login successful", "student_id": student["id"]})
    else:
        return jsonify({"message": "Invalid email or password"}), 401

@app.route('/api/dashboard_student')
def api_dashboard_student():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    return jsonify({
        'message': f"Welcome, {session.get('user_name')}!",
        'user_id': session.get('user_id')
    })

@app.route("/test_api_login")
def test_api_login():
    return render_template("login_api_test.html")

@app.route("/internship_list")
def internship_list():
    return render_template("internship_list.html")

@app.route('/api/apply', methods=['POST'])
def apply_internship():
    if 'student_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()
    internship_id = data.get('internship_id')
    student_id = session['student_id']

    if not internship_id:
        return jsonify({"message": "Internship ID required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Optional: Check for duplicate applications
    cursor.execute(
        "SELECT id FROM applications WHERE student_id = %s AND internship_id = %s",
        (student_id, internship_id)
    )
    if cursor.fetchone():
        conn.close()
        return jsonify({"message": "Already applied"}), 409

    # Insert new application
    cursor.execute(
        "INSERT INTO applications (student_id, internship_id) VALUES (%s, %s)",
        (student_id, internship_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Application submitted successfully"}), 201

@app.route("/student/applications")
def student_applications():
    # Skip session check for now
    student_id = 1  # Simulating a logged-in student with ID 1

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT internships.title, internships.description, employers.name AS employer_name
        FROM applications
        JOIN internships ON applications.internship_id = internships.id
        JOIN employers ON internships.employer_id = employers.id
        WHERE applications.student_id = %s
    """, (student_id,))

    applications = cursor.fetchall()
    conn.close()

    return render_template("student_applications.html", applications=applications)

@app.route('/employer/applications')
def view_employer_applications():
    # TEMP: Hardcoded employer_id for testing
    employer_id = 1  # Replace with session['user_id'] once login works

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT a.id AS application_id, s.name AS student_name, s.email AS student_email,
           i.title AS internship_title, i.description
    FROM applications a
    JOIN students s ON a.student_id = s.id
    JOIN internships i ON a.internship_id = i.id
    WHERE i.employer_id = %s
    """
    cursor.execute(query, (employer_id,))
    applications = cursor.fetchall()

    conn.close()
    return render_template('employer_applications.html', applications=applications)

# Step 6: Admin route to see all internships with application counts
@app.route("/admin/internships")
def admin_internships():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT i.id, i.title, i.description, COUNT(a.id) AS application_count
        FROM internships i
        LEFT JOIN applications a ON i.id = a.internship_id
        GROUP BY i.id
    """)
    internships = cursor.fetchall()
    conn.close()

    return render_template("admin_internships.html", internships=internships)

# Step 6: Run the app
if __name__ == "__main__":
    app.run(debug=True)

