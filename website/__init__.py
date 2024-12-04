"""
The `__init__.py` file initializes and configures the Flask application, setting up extensions, routes, and database connections.

Key Components:
1. Application Initialization:
   - The `create_app` function initializes the Flask application and configures settings such as the secret key and database URI.
 
2. Configurations:
   - `SECRET_KEY`: Used for securely signing session data.
   - `SQLALCHEMY_DATABASE_URI`: Specifies the SQLite database file (`database.db`).
   - Flask-Mail configurations:
     - `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`: Configures the SMTP server for sending emails.
     - `MAIL_USERNAME`, `MAIL_PASSWORD`: Provides the email credentials for the library's account.
     - `MAIL_DEFAULT_SENDER`: Specifies the sender address for all outgoing emails.

3. Extensions:
   - `SQLAlchemy`: Configured to manage database operations.
   - `Flask-Mail`: Initialized to handle email functionality.

4. Blueprints:
   - Registers `views` and `auth` blueprints, which organize the application's routes.

5. Database Initialization:
   - Ensures the database tables are created if they do not exist when the app starts.
   - Includes models like `User2` and `Note` for database structure.

6. Login Manager:
   - Sets up Flask-Login for user session management.
   - Specifies `auth.login` as the default login view.
   - Configures the `load_user` function to retrieve user details by ID.

Returns:
- The Flask application instance configured with the specified settings and extensions.

This file serves as the entry point for the Flask application, combining configurations, database setup, route organization, and extension initialization.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail  # Import Flask-Mail
from os import path, getenv
from flask_migrate import Migrate

db = SQLAlchemy()
DB_NAME = "database.db"
mail = Mail()  # Initialize Flask-Mail


def create_app():
    app = Flask(__name__)
    migrate = Migrate()

    
    # App configurations
    app.config['SECRET_KEY'] = 'nono'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    #Flask Mail Configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'librarymanagementsystem59@gmail.com'
    app.config['MAIL_PASSWORD'] = 'jjrv hbht kqtc lryj'  #DONT CHANGE THIS (app password for our account)
    app.config['MAIL_DEFAULT_SENDER'] = 'librarymanagementsystem59@gmail.com'


    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)  # Initialize Flask-Mail with the app
    migrate.init_app(app, db)
    # Import and register blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Create the database tables if they don't exist
    from .models import User2, Note
    with app.app_context():
        db.create_all()

    # Login Manager setup
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User2.query.get(int(id))

    return app
