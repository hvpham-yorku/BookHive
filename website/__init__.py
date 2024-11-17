# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from os import path
# from flask_login import LoginManager

# db = SQLAlchemy()
# DB_NAME = "database.db"


# def create_app():
#     app = Flask(__name__)
#     app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
#     app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
#     db.init_app(app)

#     from .views import views
#     from .auth import auth

#     app.register_blueprint(views, url_prefix='/')
#     app.register_blueprint(auth, url_prefix='/')

#     from .models import User, Note
    
#     with app.app_context():
#         print("creating the databse...")
#         db.create_all()
#         print("database creation completed.")

#     login_manager = LoginManager()
#     login_manager.login_view = 'auth.login'
#     login_manager.init_app(app)

#     @login_manager.user_loader
#     def load_user(id):
#         return User.query.get(int(id))

#     return app


# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail  # Import Flask-Mail
from os import path, getenv

db = SQLAlchemy()
DB_NAME = "database.db"
mail = Mail()  # Initialize Flask-Mail

def create_app():
    app = Flask(__name__)
    
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