from app import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_blacklisted = db.Column(db.Boolean, default=False)

class company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(300), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)

    drives = db.relationship('drive', backref=db.backref('company', lazy=True))

class drive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    salary = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    job_role = db.Column(db.String(120), nullable=False)
    job_discription = db.Column(db.String(300), nullable=False)
    no_of_vacancies = db.Column(db.Integer, nullable=False)
    last_date = db.Column(db.String(120), nullable=False)
    

    candidates = db.relationship('candidate',backref=db.backref('drives', lazy=True))

class candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    department = db.Column(db.String(120), nullable=False)
    resume = db.Column(db.String(300), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('drive.id'), nullable=False)
    

class candidate_drive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('drive.id'), nullable=False)

    candidate = db.relationship('candidate', backref=db.backref('candidate_drives', lazy=True))
    drive = db.relationship('drive', backref=db.backref('candidate_drives', lazy=True))

class candidate_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('drive.id'), nullable=False)
    status = db.Column(db.String(120), nullable=False)
    interview_date = db.Column(db.String(120), nullable=True)
    interview_type = db.Column(db.String(120), nullable=True)

    drive = db.relationship('drive', backref=db.backref('history', lazy=True))
    candidate = db.relationship('candidate', backref=db.backref('history', lazy=True))


with app.app_context(): 
    db.create_all()

    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', password=generate_password_hash('admin123'), is_admin=True, is_blacklisted=False)
        db.session.add(admin)
        db.session.commit()