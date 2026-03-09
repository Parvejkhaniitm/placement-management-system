# Placement Portal Application

This repository contains a **Flask-based Placement Portal Application** designed for institutions to manage campus recruitment activities. The system supports three primary roles—**Admin (Institute)**, **Company**, and **Student**—each with tailored functionalities to handle registrations, placement drives, applications, and history tracking.

---

## 🚀 Frameworks & Technologies

- **Flask** – backend web framework
- **SQLite** – embedded database (automatically created via models)
- **Jinja2, HTML, CSS, Bootstrap** – front-end templating and styling
- **Werkzeug Security** – password hashing and verification
- No JavaScript is used for core requirements per project guidelines.

> ⚠️ All database structures are created programmatically; manual creation is not allowed.

---

## 🔑 Key Terminology

1. **Admin (Institute)**: Highest access user who manages companies, students, and placement drives. Admin accounts are pre‑seeded in the database; registration is disabled for them.
2. **Company**: Organizations registering to conduct placement drives and recruit students.
3. **Student**: Users who apply for drives, view application statuses, and maintain their placement history.
4. **Placement Drive**: Recruitment event created by an approved company.

---

## 📋 Core Features

### 1. Authentication
- Separate login for Admin, Company, and Student.
- Registration only for Company and Student accounts.

### 2. Admin Functionalities
- Dashboard showing totals: students, companies, applications, drives.
- Approve/reject company registrations and drives.
- View and search all students (by name, ID, contact) and companies (by name).
- Manage (blacklist/deactivate) student and company accounts.
- Access full list of drives and applications.

### 3. Company Functionalities
- Register and manage profile (after admin approval).
- Dashboard listing company details, drives, and applicants per drive.
- Create, edit, remove, or close drives (post-approval).
- View student applications; shortlist and update selection status.

### 4. Student Functionalities
- Self-registration and login.
- Dashboard displays approved drives, applied drives, and application status.
- Apply for drives, view application statuses, and resume upload.
- Edit profile and track past placement history.

### 5. Other Core Functionalities
- Prevent duplicate applications by the same student for a drive.
- Only approved companies can create drives; only approved drives are visible to students.
- Dynamic application status updates.
- Full application and placement history for each student.

---

## 🗂 Database Models
The application defines models for `User`, `Company`, `Drive`, `Candidate`, `CandidateDrive`, and `CandidateHistory`. These are created automatically upon first run and include relationships as required.

```python
# models excerpt in repository
from flask_sqlalchemy import SQLAlchemy

# ... definitions for User, Company, Drive, Candidate, CandidateDrive, CandidateHistory ...
```

An initial admin user (`admin` / `admin123`) is seeded during setup if not already present.

---

## 🛠️ Setup Instructions
1. Create a Python virtual environment and activate it.
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the Flask server:
   ```bash
   flask run
   ```
4. Access the application at `http://127.0.0.1:5000/`.

The SQLite database file (`db.sqlite3`) is stored under `instance/` and is generated automatically on first run.

---

## 📁 Project Structure
```
app.py
config.py
models.py
routes.py
templates/      # HTML templates
static/         # CSS and resume uploads
instance/       # SQLite database
```

---

## 📌 Notes
- All demonstrations should run locally without external dependencies.
- Use of external databases or manual DB editing is prohibited.
- The application adheres strictly to project requirements as outlined in project documentation.

---

## Folder Structure 

MAD1 PROJECT/
│
├── app/
│
├── instance/
│   └── db.sqlite3
│
├── static/
│   └── resumes/
│       ├── parvej_khan_1.pdf
│       └── parvej_khan_2.pdf
│
├── templates/
│   ├── admin_dashboard.html
│   ├── application_form.html
│   ├── candidate.html
│   ├── candidate_details.html
│   ├── candidate_drive_details.html
│   ├── candidate_history.html
│   ├── company_dashboard.html
│   ├── company_details.html
│   ├── company_review_application.html
│   ├── drive.html
│   ├── drive_details.html
│   ├── drive_details_company.html
│   ├── edit_drive.html
│   ├── edit_profile.html
│   ├── layout.html
│   ├── login.html
│   ├── login_company.html
│   ├── login_register.html
│   ├── navbar.html
│   ├── profile.html
│   ├── register.html
│   ├── register_company.html
│   └── update_status_company.html
│
├── venv/        # virtual environment (optional to show)
│
├── requirements.txt
├── app.py
└── README.md

