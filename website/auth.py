"""
The `auth` Blueprint handles authentication and user management features for the library system. 

Key Features:
1. **Login and Logout**:
   - Provides routes for user login and logout.
   - Ensures secure authentication and session management.

2. **User Registration**:
   - Allows new users to sign up and optionally supports admin registration using a passcode.

3. **Password Management**:
   - Includes features for password reset:
     - Generates secure tokens for resetting passwords.
     - Sends password reset emails and updates user passwords upon submission.

4. **Routes**:
   - `/login`: Handles user authentication.
   - `/logout`: Logs the user out of the system.
   - `/sign-up`: Facilitates account registration.
   - `/forgot-password`: Allows users to request a password reset.
   - `/reset-password/<token>`: Processes password reset requests using secure tokens.

5. **Dependencies**:
   - Utilizes Flask-Login for session management.
   - Uses Flask-Mail for email functionalities, including password reset notifications.
   - Uses itsdangerous for generating and validating secure tokens.

This class organizes all authentication-related functionality into a dedicated Blueprint, improving modularity and maintainability of the application.
"""


from flask import Blueprint, render_template, request, flash, redirect, url_for
<<<<<<< HEAD
from .models import User2, UserMessage
=======
from .models import User2
>>>>>>> 03edd5c3082998ed70a6ba6db7ebb680f8f8b3f4
from flask_mail import Message, Mail
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, mail  
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime


auth = Blueprint('auth', __name__)
s = URLSafeTimedSerializer('nono')  
mail = Mail()

mail = Mail()

"""
The `login` route handles user login functionality, allowing registered users to authenticate and access the system.

Method: Supports both GET and POST requests.

Functionality:
1. Handle POST Requests:
   - Retrieves the `email` and `password` fields submitted via the login form.
   - Searches the database for a user with the specified email.
     - If the email is not found, an error message is displayed, and the user remains on the login page.
   - Validates the user's account status:
     - If the user's account is deactivated (`is_active = False`), displays an error message prompting the user to contact an admin.
   - Verifies the password:
     - Uses `check_password_hash` to compare the hashed password in the database with the submitted password.
     - If the password is incorrect, an error message is displayed.
   - Logs in the user:
     - If the email and password are correct, logs the user in using `login_user`.
     - Redirects the user to the home page with a success message.

2. Handle GET Requests:
   - Renders the login form (`login.html`) when the user navigates to the login page.

Parameters:
- None (form data is submitted via POST, and user details are accessed dynamically).

Template Variables Passed:
- `user`: The currently logged-in user object (if any), passed to the template for personalization.

Returns:
- On POST:
  - Redirects to the home page if login is successful.
  - Displays an error message and remains on the login page if login fails.
- On GET:
  - Renders the `login.html` template with the login form.

This route ensures secure and user-friendly authentication, including handling inactive accounts and providing detailed feedback on login attempts.
"""
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User2.query.filter_by(email=email).first()
        if user:
            # To check if the user is active
            if not user.is_active:
                flash("Your account is deactivated. Please contact admin.", category="error")
                return redirect(url_for('auth.login'))
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


"""
The `logout` route logs out the currently authenticated user and redirects them to the login page.

Method: Supports GET requests.
Login Required: Ensures only authenticated users can access this functionality via the login_required decorator.

Functionality:
1. Logs Out the User:
   - Calls the `logout_user` function from Flask-Login to end the user's session.
   - Clears the user's authentication state and session data.

2. Redirects to Login Page:
   - After logging out, redirects the user to the login page for future re-authentication.

Parameters:
- None (the user's session is determined dynamically via Flask-Login).

Returns:
- Redirects the user to the `auth.login` route, rendering the login page.

This route provides a simple and secure way for users to log out of their accounts and ensures session data is cleared appropriately.
"""
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

"""
The `forgot_password` route allows users to request a password reset if they have forgotten their account password.

Method: Supports both GET and POST requests.

Functionality:
1. Handle POST Requests:
   - Retrieves the email address submitted through the password reset form.
   - Searches the `User2` table for a user with the specified email.
     - If no user is found, an error message is displayed.
   - Generates a secure token using the `URLSafeTimedSerializer` to encode the user's email.
   - Constructs a password reset URL that includes the token.
   - Sends a password reset email to the user's registered email address with the reset URL.
   - Displays a success message to inform the user that the reset email has been sent.

2. Handle GET Requests:
   - Renders the `forgot_password.html` template, displaying the password reset request form.

Parameters:
- None (email is submitted via the POST request).

Template Variables Passed:
- None (renders the template directly).

Returns:
- On GET: Renders the `forgot_password.html` template with the reset request form.
- On POST:
  - Sends a password reset email if the email exists in the system.
  - Displays an error or success message, depending on whether the email is associated with an account.

This route provides a secure and user-friendly way for users to request a password reset and receive instructions via email.
"""
@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')  # Get the email from the form
        user = User2.query.filter_by(email=email).first()  # Check if the user exists
        
        if user:
            # Generate a password reset token
            token = s.dumps(email, salt='password-reset-salt')
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            
            # Send the reset email
            msg = Message(
                subject="Password Reset Request",
                recipients=[email],
                body=f"Please click the link to reset your password: {reset_url}"
            )
            mail.send(msg)
            flash('A password reset email has been sent. Please check your inbox.', category='success')
        else:
            flash('No account found with that email address.', category='error')

    return render_template('forgot_password.html')  


"""
The `sign_up` route allows new users to register for an account in the library system. It also supports admin registration with a passcode.

Method: Supports both GET and POST requests.

Functionality:
1. Handle POST Requests:
   - Collects user information from the sign-up form:
     - Email, first name, last name, date of birth, address, and password.
     - An optional passcode to identify admin registration.
   - Validates the form input:
     - Ensures email, name, and address meet minimum length requirements.
     - Confirms that passwords match and meet security standards.
     - Checks for an existing account with the same email.
     - Verifies the date of birth format and converts it to a `date` object.
   - Determines if the new user is an admin:
     - Compares the passcode input with the predefined `admin_passcode`.
   - Creates a new user account:
     - Hashes the password for security.
     - Adds the user to the database.
   - Adds a welcome message for the new user to the `UserMessage` table.
   - Logs in the new user and redirects them to the home page.

2. Handle GET Requests:
   - Renders the `sign_up.html` template to display the sign-up form.

Parameters:
- None (form data is submitted via the POST request).

Template Variables Passed:
- `user`: The currently logged-in user object, if any, for personalization.

Returns:
- On GET: Renders the `sign_up.html` template with the registration form.
- On POST:
  - Creates a new user account and logs the user in if the form submission is valid.
  - Displays error messages and remains on the sign-up page if the submission is invalid.

This route ensures secure and seamless account creation for both regular users and admins, with appropriate feedback and validation.
"""
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        date_of_birth = request.form.get('dateOfBirth')
        address = request.form.get('address')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        passcode = request.form.get('passcode') 

        # Convert date_of_birth to a date object
        try:
            date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', category='error')
            return render_template("sign_up.html", user=current_user)
        
        user = User2.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif len(address) < 2:
            flash('Address must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:

            # Default admin passcode
            admin_passcode = "secure_passcode"
            
            # Check passcode for admin registration
            is_admin = passcode == admin_passcode

            new_user = User2(email=email, first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, address=address, password=generate_password_hash(
                password1, method='pbkdf2:sha256'), is_admin=is_admin)
            db.session.add(new_user)
            db.session.commit()
            # Add a welcome message for the new user
            welcome_message = UserMessage(
                user_id=new_user.id,
                content=f"Welcome to our library system, {first_name}! We're excited to have you on board."
            )
            db.session.add(welcome_message)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
        

    return render_template("sign_up.html", user=current_user)



@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        # Verify the token and retrieve the email
        email = s.loads(token, salt='password-reset-salt', max_age=3600)  # 1-hour expiration
    except:
        flash('The reset link is invalid or has expired.', category='error')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 != password2:
            flash("Passwords don't match!", category='error')
        elif len(password1) < 6:
            flash("Password must be at least 6 characters long.", category='error')
        else:
            user = User2.query.filter_by(email=email).first()
            if user:
                # Update the user's password
                user.password = generate_password_hash(password1, method='pbkdf2:sha256')
                db.session.commit()
                flash('Your password has been updated!', category='success')
                return redirect(url_for('auth.login'))

    return render_template('reset_password.html')