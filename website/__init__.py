# Import necessary modules and libraries
from flask import Flask  # Core Flask framework
from flask_sqlalchemy import SQLAlchemy  # ORM for database interactions
from flask_login import LoginManager  # User session management
from flask_mail import Mail  # Email functionality
from os import path, getenv  # Path handling and environment variables

# Initialize the database and email extensions
db = SQLAlchemy()
DB_NAME = "database.db"  # Name of the SQLite database file
mail = Mail()  # Flask-Mail initialization

# Function to create and configure the Flask app
def create_app():
    app = Flask(__name__)  # Create a Flask application instance
    
    # App configuration settings
    app.config['SECRET_KEY'] = 'nono'  # Secret key for secure sessions
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # Database URI for SQLite

    # Flask-Mail configuration for sending emails
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # SMTP server for Gmail
    app.config['MAIL_PORT'] = 587  # Port for TLS encryption
    app.config['MAIL_USE_TLS'] = True  # Enable TLS encryption
    app.config['MAIL_USERNAME'] = 'librarymanagementsystem59@gmail.com'  # Email username
    app.config['MAIL_PASSWORD'] = 'jjrv hbht kqtc lryj'  # App-specific email password
    app.config['MAIL_DEFAULT_SENDER'] = 'librarymanagementsystem59@gmail.com'  # Default sender for emails

    # Initialize extensions with the Flask app
    db.init_app(app)  # Initialize SQLAlchemy
    mail.init_app(app)  # Initialize Flask-Mail

    # Import and register blueprints for modular app structure
    from .views import views  # Import views blueprint
    from .auth import auth  # Import auth blueprint

    app.register_blueprint(views, url_prefix='/')  # Register the views blueprint
    app.register_blueprint(auth, url_prefix='/')  # Register the auth blueprint

    # Create database tables if they do not exist
    from .models import User2, Note  # Import database models
    with app.app_context():
        db.create_all()  # Create tables within the application context

    # Setup for Flask-Login
    login_manager = LoginManager()  # Initialize LoginManager
    login_manager.login_view = 'auth.login'  # Redirect to 'auth.login' for unauthorized users
    login_manager.init_app(app)  # Bind LoginManager to the app

    # User loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(id):
        # Query the database to retrieve the user by ID
        return User2.query.get(int(id))

    return app  # Return the configured Flask app instance
