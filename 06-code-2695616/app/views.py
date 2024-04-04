from flask import render_template, redirect, url_for, flash
from app import app, db
from datetime import datetime
from app.forms import LoginForm, RegistrationForm, AddStudentForm, BorrowForm, ReturnForm, LoanedDevices
from app.models import Student, Loan


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/datetime')
def date_time():
    now = datetime.now()
    return render_template('datetime.html', title='Date & Time', now=now)

@app.route('/Loan List')
def loan_list():
    loans = LoanedDevices()
    return render_template('loanlist.html', title='Loan List')



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login for {form.username.data}', 'success')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Registration for {form.username.data} received', 'success')
        return redirect(url_for('index'))
    return render_template('registration.html', title='Register', form=form)


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    form = AddStudentForm()
    if form.validate_on_submit():
        new_student = Student(username=form.username.data, firstname=form.firstname.data,
                              lastname=form.lastname.data, email=form.email.data)
        db.session.add(new_student)
        try:
            db.session.commit()
            flash(f'New Student added: {form.username.data} received', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            if Student.query.filter_by(username=form.username.data).first():
                form.username.errors.append('This username is already taken. Please choose another')
            if Student.query.filter_by(email=form.email.data).first():
                form.email.errors.append('This email address is already registered. Please choose another')
    return render_template('add_student.html', title='Add Student', form=form)


@app.route('/borrow', methods=['GET', 'POST'])
def borrow():
    form = BorrowForm()
    if form.validate_on_submit():
        new_loan = Loan(device_id=form.device_id.data,
                        student_id=form.student_id.data,
                        borrowdatetime=datetime.now())

        db.session.add(new_loan)
        try:
            db.session.commit()
            flash(f'New Loan added', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
    return render_template('borrow.html', title='Borrow', form=form)

@app.route('/returnLoan', methods=['GET', 'POST'])
def returnLoan():
    form = ReturnForm()
    if form.validate_on_submit(): # add return date to existing entry on Loans table
        loan_id = form.loanId.data
        loan = Loan.query.filter_by(loan_id=loan_id).first()
        loan.returndatetime = datetime.now()
        try:
            db.session.commit()
            flash(f'Device {loan.device_id} returned on {loan.returndatetime}. Loan ID: {loan.loan_id}', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
    return render_template('return.html', title='Return Device', form=form)

