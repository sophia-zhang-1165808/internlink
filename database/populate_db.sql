USE internlink_db;

-- Add Admin Users
INSERT INTO users (username, email, password_hash, role, status, full_name)
VALUES
('admin1', 'admin1@example.com', '$2b$12$i6RCMb4ytrEa.SaZfp7se8GSSoDVm7730BxwScqMQUaaGIR5w4e', 'admin', 'active', 'Alice Admin'),
('admin2', 'admin2@example.com', '$2b$12$i6RCMb4ytrEa.SaZfp7se8GSSoDVm7730BxwScqMQUaaGIR5w4e', 'admin', 'active', 'Bob Admin');


-- Add Employers
INSERT INTO users (username, email, password, role, status, full_name)
VALUES
('employer1', 'employer1@example.com', '$2b$12$h9C3O7Y4BBdPCPpK.n6qte/ZkRm5jhKxrRAx6bUixPbE2/o/K1lm', 'employer', 'active', 'Company One'),
('employer2', 'employer2@example.com', '$2b$12$h9C3O7Y4BBdPCPpK.n6qte/ZkRm5jhKxrRAx6bUixPbE2/o/K1lm', 'employer', 'active', 'Company Two'),
('employer3', 'employer3@example.com', '$2b$12$h9C3O7Y4BBdPCPpK.n6qte/ZkRm5jhKxrRAx6bUixPbE2/o/K1lm', 'employer', 'active', 'Company Three'),
('employer4', 'employer4@example.com', '$2b$12$h9C3O7Y4BBdPCPpK.n6qte/ZkRm5jhKxrRAx6bUixPbE2/o/K1lm', 'employer', 'active', 'Company Four'),
('employer5', 'employer5@example.com', '$2b$12$h9C3O7Y4BBdPCPpK.n6qte/ZkRm5jhKxrRAx6bUixPbE2/o/K1lm', 'employer', 'active', 'Company Five');



-- Add Students (first 5 for now; we'll add more via UI later)
INSERT INTO users (username, email, password, role, status, full_name)
VALUES
('student1', 'student1@example.com', '$2b$12$sZsfQ8ClSgcBC4USsgDcQAcn.r1kvx3j0hCmpxAJFsbam3xHlGxyI', 'student', 'active', 'Student One'),
('student2', 'student2@example.com', '$2b$12$jkPVPjX1DxS3AFaPcX1evg.2wTBb02dkqpxa7tVwaSs2qvToBuNWR', 'student', 'active', 'Student Two'),
('student3', 'student3@example.com', '$2b$12$hkK5jjb7tWkRm/7yfum5K1OMJ5Ctmp3.pDVq/VLNs1wy.utNaSp/k', 'student', 'active', 'Student Three'),
('student4', 'student4@example.com', '$2b$12$ybIb47nB3Dy/tTr6tT2fE.9oXs/WG1r2P6KWpM3NtXbb5Hjv9f4m', 'student', 'active', 'Student Four'),
('student5', 'student5@example.com', '$2b$12$8Hf8UzVjJDSMVaBoJ2TvAuB8r5A02qZvLf/1oSn31765PyYJXp2K', 'student', 'active', 'Student Five');

