from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Book, BorrowedBook
from . import db
import json
from flask_mail import Message
from datetime import datetime, timedelta
from . import mail

views = Blueprint('views', __name__)
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template(
        'home.html',
        name=current_user.first_name,
        is_admin=current_user.is_admin
    )

@views.route('/book-list', methods=['GET'])
@login_required
def book_list():
    books = Book.query.all()  # Fetch all books in the database

    # Get all books borrowed by the current user that are not yet returned
    borrowed_books = BorrowedBook.query.filter_by(user_id=current_user.id, returned=False).all()
    
    # Create a set of book IDs that the user has borrowed
    borrowed_book_ids = {borrowed.book_id for borrowed in borrowed_books}

    return render_template('book_list.html', books=books, borrowed_book_ids=borrowed_book_ids)






@views.route('/borrow-book/<int:book_id>', methods=['POST'])
@login_required
def borrow_book(book_id):
    # Check if the book exists and has available copies
    book = Book.query.get(book_id)
    if not book or book.remaining_copies <= 0:
        flash('This book is not available.', category='error')
        return redirect(url_for('views.book_list'))

    # Check if the user has already borrowed the book
    borrowed_books = BorrowedBook.query.filter_by(user_id=current_user.id, book_id=book_id, returned=False).first()
    if borrowed_books:
        flash('You have already borrowed this book.', category='error')
        return redirect(url_for('views.book_list'))

    # Check if the user has already borrowed 5 books
    borrowed_count = BorrowedBook.query.filter_by(user_id=current_user.id, returned=False).count()
    if borrowed_count >= 5:
        flash('You have already borrowed the maximum number of books (5).', category='error')
        return redirect(url_for('views.book_list'))

    # Borrow the book
    due_date = datetime.now() + timedelta(days=14)  # 14-day loan period
    new_borrow = BorrowedBook(
        user_id=current_user.id,
        book_id=book.id,
        borrow_date=datetime.now(),
        due_date=due_date
    )
    book.remaining_copies -= 1
    db.session.add(new_borrow)
    db.session.commit()

    # Send Loan Receipt Email
    send_loan_receipt(current_user.email, book.name, book.author, new_borrow.borrow_date, new_borrow.due_date)

    flash(f'You have successfully borrowed "{book.name}". A loan receipt has been emailed to you.', category='success')
    return redirect(url_for('views.book_list'))

def send_loan_receipt(email, book_name, author, borrow_date, due_date):
    msg = Message(
        subject="Loan Receipt: Book Borrowed Successfully",
        recipients=[email],
        body=f"""
        Thank you for borrowing a book from our library!
        
        Details of your loan:
        - Book Title: {book_name}
        - Author: {author}
        - Date Borrowed: {borrow_date.strftime('%Y-%m-%d')}
        - Due Date: {due_date.strftime('%Y-%m-%d')}

        Please make sure to return the book by the due date.

        Happy Reading :))
        Library Management System
        """
    )
    mail.send(msg)





@views.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
    # Only allow admins to access this route
    if not current_user.is_admin:
        flash("You do not have permission to access this page.", category='error')
        return redirect(url_for('views.home'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        author = request.form.get('author')
        copies = request.form.get('copies')

        if not name or not author or not copies:
            flash('Please fill in all fields.', category='error')
        else:
            new_book = Book(
                name=name,
                author=author,
                copies=int(copies),
                remaining_copies=int(copies),
                user_id=current_user.id  # Optionally associate with admin who added it
            )
            db.session.add(new_book)
            db.session.commit()
            flash('Book added successfully!', category='success')
            return redirect(url_for('views.book_list'))  # Redirect to the Book List Page

    return render_template('add_book.html')




