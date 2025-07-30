from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
import mysql.connector

app = Flask(__name__)
app.secret_key = 'supersecretkey'
bcrypt = Bcrypt(app)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Godblessbaby',
        database='internlink'
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        table = None
        dashboard = None

        if role == 'student':
            table = 'students'
            dashboard = 'student_applications'
        elif role == 'employer':
            table = 'employers'
            dashboard = 'view_employer_applications'
        elif role == 'admin':
            table = 'admins'
            dashboard = 'admin_internships'
        else:
            flash('Invalid role selected.', 'danger')
            return redirect(url_for('login'))

        cursor.execute(f"SELECT * FROM {table} WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_name'] = user.get('name') or user.get('email')
            session['role'] = role
            flash(f'Logged in as {role.capitalize()}!', 'success')
            return redirect(url_for(dashboard))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')



@app.route("/login_submit", methods=["POST"])
def login_submit():
    email = request.form["email"]
    password = request.form["password"]
    user_type = request.form["user_type"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if user_type == "student":
        cursor.execute("SELECT * FROM students WHERE email = %s", (email,))
    elif user_type == "admin":
        cursor.execute("SELECT * FROM admins WHERE email = %s", (email,))
    else:
        flash("Invalid user type", "danger")
        return redirect(url_for("login", user_type=user_type))

    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.check_password_hash(user["password_hash"], password):
        session["user_id"] = user["id"]
        session["role"] = user_type
        session["user_name"] = user.get("name", email)

        flash("Login successful", "success")

        if user_type == "student":
            return redirect(url_for("dashboard_student"))
        else:
            return redirect(url_for("admin_internships"))
    else:
        flash("Invalid credentials", "danger")
        return redirect(url_for("login", user_type=user_type))

@app.route("/dashboard_student")
def dashboard_student():
    if session.get("role") != "student":
        return jsonify({"message": "Unauthorized"}), 401
    return jsonify({
        "message": f"Welcome, {session.get('user_name')}!",
        "user_id": session.get("user_id")
    })

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

@app.route("/internship_list")
def internship_list():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT internships.id, internships.title, internships.description, employers.name AS employer_name
        FROM internships
        JOIN employers ON internships.employer_id = employers.id
    """
    cursor.execute(query)
    internships = cursor.fetchall()
    conn.close()

    return render_template("internship_list.html", internships=internships)

@app.route("/student/applications")
def student_applications():
    student_id = 1  # Simulate logged-in student

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

@app.route('/logout')
def logout():
    session.clear()
    flash

# Add any additional routes (e.g. /students, /employers, /internships) as needed

if __name__ == "__main__":
    app.run(debug=True)
