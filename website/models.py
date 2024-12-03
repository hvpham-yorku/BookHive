from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user2.id'))

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # a reference ID
    name = db.Column(db.String(150), nullable=False)  # a title
    author = db.Column(db.String(150), nullable=False)  # an author
    genre = db.Column(db.String(50), nullable=True)  # genre (optional)
    copies = db.Column(db.Integer, nullable=False)  # number of total copies
    remaining_copies = db.Column(db.Integer, nullable=False)  # number of remaining copies
    content_link = db.Column(db.String(500), nullable=True)  # link to access the book (optional)
    borrowed_books = db.relationship('BorrowedBook', backref='book')# relationship to track borrow records for this book


 

class User2(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    date_of_birth = db.Column((db.Date))
    address = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    borrowed_books = db.relationship('BorrowedBook', backref='user', lazy=True)
    messages = db.relationship('UserMessage', backref='user', lazy=True)
    is_active = db.Column(db.Boolean, default=True)  # To check if the account is active



class BorrowedBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user2.id'))  
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))  
    borrow_date = db.Column(db.DateTime, default=func.now())   
    due_date = db.Column(db.DateTime)                         
    returned = db.Column(db.Boolean, default=False)

class UserMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user2.id'))
    content = db.Column(db.String(500), nullable=False)
    is_read = db.Column(db.Boolean, default=False)  # To track if the message is read
    timestamp = db.Column(db.DateTime, default=func.now())
