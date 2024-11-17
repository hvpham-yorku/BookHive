from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user2.id'))

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    copies = db.Column(db.Integer, nullable=False)
    remaining_copies = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user2.id'))
    borrowed_books = db.relationship('BorrowedBook', backref='book')  

class User2(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    books = db.relationship('Book')  
    is_admin = db.Column(db.Boolean, default=False)
    borrowed_books = db.relationship('BorrowedBook', backref='user')

class BorrowedBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user2.id'))  
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))  
    borrow_date = db.Column(db.DateTime, default=func.now())   
    due_date = db.Column(db.DateTime)                         
    returned = db.Column(db.Boolean, default=False)  
