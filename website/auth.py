# Import necessary modules
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User2
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, mail  
from flask_login import login_user, login_required, logout_user, current_user

# Define the auth blueprint
auth = Blueprint('auth', __name__)

# Serializer for secure token generation
s = URLSafeTimedSerializer('nono')  

# Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Authenticate the user
        user = User2.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

# Logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Forgot password route
@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User2.query.filter_by(email=email).first()
        
        if user:
            # Send reset email with a tokenized link
            token = s.dumps(email, salt='password-reset-salt')
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            msg = Message(
                subject="Password Reset Request",
                recipients=[email],
                body=f"Please click the link to reset your password: {reset_url}"
            )
            mail.send(msg)
            flash('A password reset email has been sent.', category='success')
        else:
            flash('No account found with that email address.', category='error')

    return render_template('forgot_password.html')  

# Sign-up route
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        passcode = request.form.get('passcode') 

        # Validate user input and check for existing account
        user = User2.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Check if the user is an admin
            admin_passcode = "secure_passcode"
            is_admin = passcode == admin_passcode

            # Create a new user
            new_user = User2(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='pbkdf2:sha256'), is_admin=is_admin)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

# Reset password route
@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        # Verify token and get email
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The reset link is invalid or has expired.', category='error')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Validate passwords and update user password
        if password1 != password2:
            flash("Passwords don't match!", category='error')
        elif len(password1) < 6:
            flash("Password must be at least 6 characters long.", category='error')
        else:
            user = User2.query.filter_by(email=email).first()
            if user:
                user.password = generate_password_hash(password1, method='pbkdf2:sha256')
                db.session.commit()
                flash('Your password has been updated!', category='success')
                return redirect(url_for('auth.login'))

    return render_template('reset_password.html')
