import os

from flask import Flask, flash, redirect, render_template, request, session, url_for
from app import app
from models import User, company, drive, candidate, candidate_drive, candidate_history, db
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


 


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if not username or not password:
        flash("Please enter both username and password.")
        return redirect(url_for('login'))
    
    if not user:
        flash('Username does not exist. Please register first.') 
        return redirect(url_for('register'))
    
    if not check_password_hash(user.password, password):
        flash('Incorrect password. Please try again.')
        return redirect(url_for('login'))
    
    session['user_id'] = user.id
    flash('Login successful!') 
    return redirect(url_for('candidate_dashboard'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if not username or not password or not confirm_password:
        flash('Please fill out all fields.')
        return redirect(url_for('register'))

    if password != confirm_password:
        flash('Passwords do not match. Please try again.')
        return redirect(url_for('register'))
    
    user = User.query.filter_by(username=username).first()
    if user:
        flash('Username already exists. Please choose a different one.')
        return redirect(url_for('register'))
    
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    flash('Registration successful!')
    return redirect(url_for('login'))
    

def auth_rquired(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            flash('Login to continue')
            return redirect(url_for('login'))
    return inner


@app.route('/')
@auth_rquired
def candidate_dashboard():
    user = User.query.filter_by(id=session['user_id']).first()
    company_user = company.query.filter_by(is_approved=True).all()

    if user.is_admin:
        return redirect(url_for('admin_dashboard'))

    candidate_obj = candidate.query.filter_by(user_id=session['user_id']).first()
    candidate_drives = candidate_drive.query.filter_by(candidate_id=candidate_obj.id).all() if candidate_obj else []

    return render_template('candidate.html', user=user, companies=company_user, candidate_drives=candidate_drives)


@app.route('/profile')
@auth_rquired
def profile():
    return render_template("profile.html", user=User.query.get(session["user_id"]))

@app.route('/edit_profile',methods=['GET','POST'])
@auth_rquired
def edit_profile():
    user = User.query.get(session['user_id'])

    if request.method == "GET":
        return render_template("edit_profile.html",user=user)

    username = request.form.get("username")
    password = request.form.get("password")
    new_password = request.form.get("new_password")

    if not username or not password or not new_password:
        flash("Please enter all the fields")
        return redirect(url_for("edit_profile"))
    

    if not check_password_hash(user.password,password):
        flash("Incorrect Password")
        return redirect(url_for("edit_profile"))
    
    if username != user.username:
        new_user = User.query.filter_by(username=username).first()
        if new_user:
            flash("Username already exists. please enter different username")
            return redirect(url_for("edit_profile"))
        
    new_password_hash = generate_password_hash(new_password)
    user.username = username
    user.password = new_password_hash
    db.session.commit()
    flash("Profile updated sucessfully")
    return redirect(url_for("profile"))

    
    
@app.route('/logout')
@auth_rquired
def logout():
    session.pop("user_id")
    return redirect(url_for('login'))

@app.route('/login_register')
def login_register():
    return render_template('login_register.html')

# @app.route('/register_company')
# def register_company():
#     return render_template('register_company.html')

@app.route('/register_company', methods=['GET','POST'])
def register_company():

    if request.method == 'GET':
        return render_template('register_company.html')

    name = request.form.get('name')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    description = request.form.get('description')
    location = request.form.get('location')

    if not name or not password or not confirm_password or not description or not location:
        flash('Please fill out all fields.')
        return redirect(url_for('register_company'))
    
    if password != confirm_password:
        flash('Passwords do not match. Please try again.')
        return redirect(url_for('register_company'))
    
    company_exists = company.query.filter_by(name=name).first()
    if company_exists:
        flash('Company name already exists. Please choose a different one.')
        return redirect(url_for('register_company'))
    
    hashed_password = generate_password_hash(password)
    new_company = company(name=name, password=hashed_password, description=description, location=location)
    db.session.add(new_company)
    db.session.commit()
    flash('Company registration successful!')
    return redirect(url_for('login_register'))

@app.route('/company_login', methods=['GET','POST'])
def company_login():

    if request.method == 'GET':
        return render_template('login_company.html')
    
    name = request.form.get('name')
    password = request.form.get('password')

    if not name or not password:
        flash('Please enter both company name and password.')
        return redirect(url_for('login_company'))
    
    company_user = company.query.filter_by(name=name).first()
    if not company_user:
        flash('Company not found.')
        return redirect(url_for('login_company'))
    

    if not check_password_hash(company_user.password, password):
        flash('Incorrect password.')
        return redirect(url_for('login_company'))
    
    session['company_id'] = company_user.id
    flash('Company login successful!')
    return redirect(url_for('company_dashboard'))

@app.route('/company_dashboard')

def company_dashboard():
    if 'company_id' not in session:
        flash('Please log in to access the company dashboard.')
        return redirect(url_for('company_login'))
    
    company_user = company.query.get(session['company_id'])
    drives = drive.query.filter_by(company_id=company_user.id).all()
    return render_template('company_dashboard.html', company=company_user, drives=drives)


@app.route('/admin')
@auth_rquired
def admin_dashboard():
    approved_companies = company.query.filter_by(is_approved=True).all()
    drives=drive.query.all()
    # drive_candidates_name = 
    search = request.args.get('search', '')

    if search:
        companies = company.query.filter(company.name.contains(search)).all()
        users = User.query.filter(User.username.contains(search)).all()
        drives_list = drive.query.filter(drive.name.contains(search)).all()
        approved_companies = company.query.filter(company.name.contains(search), company.is_approved==True).all()
        candidate_drives_list = candidate_drive.query.join(candidate).filter(candidate.name.contains(search)).all()
    else:
        companies = company.query.all()
        users = User.query.all()
        drives_list = drive.query.all()
        approved_companies = company.query.filter_by(is_approved=True).all()
        candidate_drives_list = candidate_drive.query.all()

    return render_template('admin_dashboard.html',
        users=users,
        companies=companies,
        drives=drives_list,
        candidates=candidate.query.all(),
        candidate_drives=candidate_drives_list,
        approved_companies=approved_companies,
        search=search
    )
    
   
@app.route('/blacklist_user/<int:user_id>')
@auth_rquired
def blacklist_user(user_id):
    candidate_user = User.query.get(user_id)
    if not candidate_user:
        flash('User not found.')
        return redirect(url_for('admin_dashboard'))
    
    candidate_user.is_blacklisted = True
    db.session.commit()
    flash('User blacklisted successfully.')
    return redirect(url_for('admin_dashboard'))

@app.route('/company_details/<int:company_id>/',methods=['GET','POST'])
@auth_rquired
def company_details(company_id):
    company_user = company.query.get(company_id)
    
    if not company_user:
        flash('Company not found.')
        return redirect(url_for('admin_dashboard'))
    
    company_drives = company_user.drives
    return render_template('company_details.html', company=company_user,drives=company_drives)

@app.route('/approve_company/<int:company_id>')
@auth_rquired
def approve_company(company_id):
    company_user = company.query.get(company_id)
    if not company_user:
        flash('Company not found.')
        return redirect(url_for('admin_dashboard'))
    company_user.is_approved = True
    db.session.commit()
    flash('Company approved successfully.')
    return redirect(url_for('admin_dashboard'))

@app.route('/blacklist_company/<int:company_id>')
@auth_rquired
def blacklist_company(company_id):
    company_user = company.query.filter_by(id=company_id).first()
    if not company_user:
        flash('Company not found.')
        return redirect(url_for('admin_dashboard'))
    
    if company_user.is_approved == False:
        flash('Company is already blacklisted.')
        return redirect(url_for('admin_dashboard'))
    
    company_user.is_approved = False
    db.session.commit()
    flash('Company blacklisted successfully.')
    return redirect(url_for('admin_dashboard'))

@app.route('/create_drive', methods=['GET','POST'])
def create_drive():
   
        if request.method == 'GET': 
            return render_template('drive.html')
        
        title = request.form.get('title')
        job_role = request.form.get('job_role')
        description = request.form.get('description')
        vacancies = request.form.get('vacancies')
        last_date = request.form.get('last_date')
        salary = request.form.get('salary')
        location = request.form.get('location')

        company_user = company.query.get(session['company_id'])
        if not all([title, job_role, description, vacancies, last_date, salary, location]):
            flash('Please fill in all fields.')
            return redirect(url_for('create_drive'))

        if not company_user.is_approved:
            flash('Your company is not approved yet. Please wait for admin approval.')
            return redirect(url_for('company_dashboard'))

    
        new_drive = drive(name=title, company_id=session['company_id'], job_role=job_role, job_discription=description, no_of_vacancies=int(vacancies), last_date=last_date, salary=salary, location=location)
        db.session.add(new_drive)
        db.session.commit()
        flash('Drive created successfully!')
        return redirect(url_for('company_dashboard'))

@app.route('/logout_company')
def logout_company():
    session.pop('company_id')
    flash('You have been logged out.')
    return redirect(url_for('login_register'))   

@app.route('/drive_details/<int:drive_id>')
def drive_details(drive_id):
    drive_obj = drive.query.get(drive_id)
    candidate_drives = candidate_drive.query.filter_by(drive_id=drive_id).all()
    if not drive_obj:
        flash('Drive not found.')
        return redirect(url_for('company_dashboard'))
    return render_template('drive_details.html', drive=drive_obj, candidate_drives=candidate_drives)

@app.route('/update_drive/<int:drive_id>', methods=['GET', 'POST'])
def update_drive(drive_id):
    drive_obj = drive.query.get(drive_id)
    if not drive_obj:
        flash('Drive not found.')
        return redirect(url_for('company_dashboard'))
    
    if request.method == 'GET':
        return render_template('edit_drive.html', drive=drive_obj)
    
    if request.method == 'POST':
        title = request.form.get('title')
        job_role = request.form.get('job_role')
        description = request.form.get('description')
        vacancies = request.form.get('vacancies')
        last_date = request.form.get('last_date')

    if drive_obj.name != title:
        new_drive = drive.query.filter_by(name=title).first()
        if new_drive:
            flash("Drive title already exists. try different title")
            return redirect(url_for('update_drive', drive_id=drive_obj.id))
            
    drive_obj.name = title
    drive_obj.job_role = job_role
    drive_obj.company_id = session["company_id"]
    drive_obj.job_description = description
    drive_obj.no_of_vacancies = int(vacancies)
    drive_obj.last_date = last_date
    db.session.commit()
    flash('Drive updated successfully')
    return redirect(url_for("company_dashboard"))

@app.route('/delete_drive/<int:drive_id>', methods=['GET', 'POST'])
def delete_drive(drive_id):
    drive_obj = drive.query.get(drive_id)
    if not drive_obj:
        flash('Drive not found.')
        return redirect(url_for('company_dashboard'))

    db.session.delete(drive_obj)
    db.session.commit()
    flash('Drive deleted successfully.')
    return redirect(url_for('company_dashboard'))

@app.route('/candidate_drive_details/<int:drive_id>')
@auth_rquired
def candidate_drive_details(drive_id):
    drive_obj = drive.query.get(drive_id)
    if not drive_obj:
        flash('Drive not found.')
        return redirect(url_for('candidate_dashboard'))
    return render_template('candidate_drive_details.html', drive=drive_obj)



@app.route('/apply_drive/<int:drive_id>', methods=['GET','POST'])
@auth_rquired  
def apply_drive(drive_id):
    drive_obj = drive.query.get(drive_id)
    current_user = User.query.get(session['user_id'])

    if current_user.is_blacklisted:
        flash("You are blacklisted. You cannot apply for drives.")
        return redirect(url_for("candidate_dashboard"))

    if not drive_obj:
        flash("Drive not found")
        return redirect(url_for("candidate_dashboard"))
    
    if request.method == 'POST':  
        name = request.form.get("name")
        department = request.form.get("department")
        resume = request.files.get("resume")

        

        if not all([name, department]):
            flash("Please fill all the fields")
            return render_template("application_form.html", drive=drive_obj)
        
        
        exist_candidate = candidate.query.filter_by(name=name, department=department).first()

        
        if exist_candidate and exist_candidate.is_blacklisted:
            flash("You are blacklisted.")
            return redirect(url_for("candidate_dashboard"))
        
        if exist_candidate:
            already_applied = candidate_drive.query.filter_by(drive_id=drive_id,candidate_id=exist_candidate.id).first()

            if already_applied:
                flash("You have aleady applied in this Drive")
                return redirect(url_for("candidate_dashboard"))
            
            new_application = candidate_drive(
                candidate_id=exist_candidate.id,
                drive_id=drive_id
            )
            db.session.add(new_application)
            db.session.commit()
            flash("Application submitted successfully!")
            return redirect(url_for("candidate_dashboard"))
        
        else:
        
            resume_filename = None
            if resume and resume.filename:
                file_extension = resume.filename.split('.')[-1]
                resume_filename = f"{name.replace(' ', '_')}_{drive_id}.{file_extension}"

                resume.save(f"static/resumes/{resume_filename}")

            new_candidate = candidate(
                name=name, 
                department=department, 
                resume=resume_filename, 
                drive_id=drive_id,
                user_id=session['user_id']
            )
            db.session.add(new_candidate)
            db.session.flush()

            new_application = candidate_drive(
            candidate_id=new_candidate.id,
            drive_id=drive_id
            )
        
        
            db.session.add(new_application)
            db.session.commit()
        
            flash("Application submitted successfully!")
            return redirect(url_for("candidate_dashboard"))  
        
   
    return render_template("application_form.html", drive=drive_obj)

@app.route('/drive_details_company/<int:drive_id>')
def drive_details_company(drive_id):
    drive_obj = drive.query.get(drive_id)
    candidate_drives = candidate_drive.query.filter_by(drive_id=drive_id).all()
    if not drive_obj:
        flash('Drive not found.')
        return redirect(url_for('company_dashboard'))
    return render_template('drive_details_company.html', drive=drive_obj, candidate_drives=candidate_drives)

@app.route('/review_application/<int:candidate_id>')
def review_application(candidate_id):
    candidate_obj = candidate.query.filter_by(id=candidate_id).first()
    if not candidate_obj:
        flash('Candidate not found.')
        return redirect(url_for('admin_dashboard'))
    return render_template('candidate_details.html', candidate=candidate_obj)

@app.route('/company_review_application/<int:candidate_drive_id>')
def company_review_application(candidate_drive_id):
    candidate_drives = candidate_drive.query.filter_by(id=candidate_drive_id).first()
    return render_template('company_review_application.html', candidates=candidate_drives)

@app.route('/candidate_history', methods=['GET','POST'])
@auth_rquired
def candidate_history_page():

    candidate_obj = candidate.query.filter_by(user_id=session['user_id']).first()
    
    histories = candidate_history.query.filter_by(candidate_id=candidate_obj.id).all()
    
    return render_template("candidate_history.html", histories=histories, user=candidate_obj)
    

@app.route('/update_status_company/<int:candidate_drive_id>', methods=['GET','POST'])
def update_status_company(candidate_drive_id):


    if request.method == 'GET':
        return render_template('update_status_company.html', candidate_drive_id=candidate_drive_id)


    interview_date = request.form.get('interview_date')
    interview_type = request.form.get('interview_type')
    status = request.form.get('status')

    if not all([interview_date, interview_type, status]):
        flash('Please fill in all fields.')
        return redirect(url_for('company_review_application', candidate_drive_id=candidate_drive_id))
    

    cd_record = candidate_drive.query.filter_by(id=candidate_drive_id).first()

    new_history = candidate_history(
        candidate_id=cd_record.candidate_id,
        drive_id=cd_record.drive_id,
        status=status,
        interview_date=interview_date,
        interview_type=interview_type
        )
    db.session.add(new_history)
    db.session.commit()
    flash("Updated Successfully")

    return redirect(url_for("company_review_application", candidate_drive_id=candidate_drive_id))