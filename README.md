# InternLink - COMP639 Web Application

## Overview
InternLink is a Flask-based web application developed for the COMP639 course. It enables students to apply for internships, employers to manage applications, and administrators to oversee all activities.

## Features are below:
- **Students**: View and apply for internships
- **Employers**: View internship applications received
- **Administrators**: Access all student and internship data

## Tech Stack
- Python & Flask
- HTML / Bootstrap (Jinja templates)
- MySQL (via `connect.py`)
- GitHub for version control

## Setup Instructions

1. **Clone this repository**:
   ```bash
   git clone https://github.com/sophia-zhang-1165808/internlink.git
   cd internlink
2. **Create virtual environment: python -m venv venv
   - Activate the virtual environment:
3. **Install required packages: pip install -r requirements.txt
4. **Setup the database
   - Use the provided SQL scripts inside the /database folder to create and populate tables.
   - Refer to connect.py for database schema and setup logic.

5.**Run the app
  - python app.py
  - Then open your browser and go to: http://localhost:5000

## Project Structure
 - InternLink/
├── app.py
├── connect.py
├── generate_password_hashes.py
├── requirements.txt
├── README.md
├── templates/
│   └── *.html
├── static/
│   ├── css/
│   └── images/
├── database/
│   └── *.sql
├── venv/ (not included in repo)
└── .gitignore

Author: Sophia Zhang – 1165808
