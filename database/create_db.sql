-- Create the InternLink database
CREATE DATABASE IF NOT EXISTS internlink_db;
USE internlink_db;

-- Users Table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) NOT NULL,
    password_hash CHAR(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    role ENUM('student', 'employer', 'admin') NOT NULL DEFAULT 'student',
    status ENUM('active', 'inactive') DEFAULT 'active',
    full_name VARCHAR(100) NOT NULL,
    university VARCHAR(100),
    course VARCHAR(100),
    profile_image VARCHAR(255),
    resume_filename VARCHAR(255),
    company_name VARCHAR(100),
    company_description TEXT,
    company_website VARCHAR(255),
    company_logo VARCHAR(255)
);

-- Internships Table
CREATE TABLE internships (
    internship_id INT AUTO_INCREMENT PRIMARY KEY,
    employer_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50),
    location VARCHAR(100),
    duration VARCHAR(50),
    application_deadline DATE,
    FOREIGN KEY (employer_id) REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- Applications Table
CREATE TABLE applications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    internship_id INT NOT NULL,
    status ENUM('Pending', 'Accepted', 'Rejected') DEFAULT 'Pending',
    resume_filename VARCHAR(255),
    cover_letter TEXT,
    feedback TEXT,
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(user_id)
        ON DELETE CASCADE,
    FOREIGN KEY (internship_id) REFERENCES internships(internship_id)
        ON DELETE CASCADE
);
