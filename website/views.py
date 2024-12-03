from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Book, BorrowedBook, User2
from . import db
import json
from flask_mail import Message
from .models import UserMessage  
from datetime import datetime, timedelta
from . import mail
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from threading import Thread



views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template(
        'home.html',
        name=current_user.first_name,
        is_admin=current_user.is_admin
    )




@views.route('/book-list', methods=['GET', 'POST'])
@login_required
def book_list():
    selected_author = request.args.get('author')
    selected_genre = request.args.get('genre')
    
    if selected_author:
        books = Book.query.filter_by(author=selected_author).all()
    elif selected_genre:
        books = Book.query.filter_by(genre=selected_genre).all()
    else:
        books = Book.query.all()

    genres = db.session.query(Book.genre).distinct().all()
    authors = db.session.query(Book.author).distinct().all()

    # Get the IDs of books the user has already borrowed
    borrowed_book_ids = [borrow.book_id for borrow in current_user.borrowed_books]
    return render_template('book_list.html', books=books, borrowed_book_ids=borrowed_book_ids, 
                           genres=genres, authors=authors, selected_genre=selected_genre, 
                           selected_author=selected_author)


@views.route('/delete-book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    if not current_user.is_admin:
        flash('Only admins can delete books.', category='error')
        return redirect(url_for('views.book_list'))

    book = Book.query.get(book_id)
    if not book:
        flash('Book not found.', category='error')
        return redirect(url_for('views.book_list'))

    db.session.delete(book)
    db.session.commit()
    flash(f'Book "{book.name}" has been deleted successfully.', category='success')
    return redirect(url_for('views.book_list'))




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

    # Create a notification message for the Messages Tab
    message_content = f'You have successfully borrowed "{book.name}" by {book.author}. It is due on {due_date.strftime("%b %d, %Y")}.'
    new_message = UserMessage(
    user_id=current_user.id,
    content=message_content,
)
    db.session.add(new_message)

    # Commit changes to the database
    db.session.commit()

    # Send Loan Receipt Email
    send_loan_receipt(current_user.email, book.name, book.author, new_borrow.borrow_date, new_borrow.due_date)

    # Flash success message
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

        Happy Reading :)
        Library Management System
        """
    )
    mail.send(msg)





@views.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
    if not current_user.is_admin:
        flash("You do not have permission to access this page.", category='error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        name = request.form.get('name')
        author = request.form.get('author')
        genre = request.form.get('genre')
        copies = request.form.get('copies')
        content_link = request.form.get('content_link')

        if not name or not author or not copies:
            flash('Please fill in all required fields.', category='error')
        else:
            new_book = Book(
                name=name,
                author=author,
                genre=genre,
                copies=int(copies),
                remaining_copies=int(copies),
                content_link=content_link
            )
            db.session.add(new_book)
            db.session.commit()
            flash(f'Book "{name}" added successfully!', category='success')
            return redirect(url_for('views.book_list'))

    return render_template('add_book.html')


@views.route('/edit-book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    if not current_user.is_admin:
        flash("You do not have permission to access this page.", category='error')
        return redirect(url_for('views.home'))

    # Fetch the book by ID
    book = Book.query.get(book_id)
    if not book:
        flash("Book not found.", category='error')
        return redirect(url_for('views.book_list'))

    if request.method == 'POST':
        # Get updated data from the form
        book.name = request.form.get('name')
        book.author = request.form.get('author')
        book.genre = request.form.get('genre')
        book.copies = int(request.form.get('copies'))
        book.remaining_copies = int(request.form.get('remaining_copies'))  # Admin can adjust available copies
        book.content_link = request.form.get('content_link')

        # Update the book in the database
        db.session.commit()
        flash(f'Book "{book.name}" updated successfully!', category='success')
        return redirect(url_for('views.book_list'))

    # Render the edit page with the book's current details
    return render_template('edit_book.html', book=book)

@views.route('/search-books', methods=['GET'])
@login_required
def search_books():
    query = request.args.get('query', '').strip()  # Extract the query from the URL
    books = []

    if query:  # Only perform the search if there's a query
        books = Book.query.filter(
            (Book.name.ilike(f'%{query}%')) |
            (Book.author.ilike(f'%{query}%')) |
            (Book.genre.ilike(f'%{query}%'))
        ).all()
    else:
        flash('Please enter a search term.', category='error')

    # Pass the books and query back to the template
    return render_template('search_books.html', results=books, query=query)

@views.route('/message/<int:message_id>')
@login_required
def view_message(message_id):
    message = UserMessage.query.filter_by(id=message_id, user_id=current_user.id).first()
    if not message:
        flash('Message not found', category='error')
        return redirect(url_for('views.home'))

    # Mark the message as read
    if not message.is_read:
        message.is_read = True
        db.session.commit()


    return render_template('view_message.html', message=message)

@views.context_processor
def inject_messages():
    if current_user.is_authenticated:
        user_messages = UserMessage.query.filter_by(user_id=current_user.id).order_by(UserMessage.timestamp.desc()).all()
        unread_count = UserMessage.query.filter_by(user_id=current_user.id, is_read=False).count()

        return {'user_messages': user_messages, 'unread_count': unread_count}
    return {}


@views.route('/contact-us', methods=['GET', 'POST'])
@login_required
def contact_us():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        query = request.form.get('query')

        # Email the query to the library management system
        msg = Message(
            subject=f"New Query from {name}",
            recipients=["librarymanagementsystem59@gmail.com"],  
            body=f"""
            You have received a new query:

            Name: {name}
            Email: {email}
            Query: {query}
            """
        )
        mail.send(msg)
        flash('Your query has been submitted successfully. We will get back to you soon!', category='success')
        return redirect(url_for('views.home'))

    return render_template('contact_us.html')

@views.route('/profile_information', methods=['GET', 'POST'])
@login_required
def profile_information():
    # Fetch the currently logged-in user
    user = User2.query.get(current_user.id)

    if request.method == 'POST':
        # Update only when the "Update Information" button is clicked
        user.first_name = request.form.get('firstName', user.first_name)
        user.last_name = request.form.get('lastName', user.last_name)
        dob = user.date_of_birth = request.form.get('dateOfBirth')

        # Handle date conversion
        if dob:
            try:
                    user.date_of_birth = datetime.strptime(dob, '%Y-%m-%d').date()
            except ValueError:
                    flash('Invalid date format for Date of Birth.', category='error')
                    return redirect(url_for('views.profile_information'))
        user.address = request.form.get('address', user.address)

        # Commit changes to the database
        db.session.commit()
        flash('Profile updated successfully!', category='success')
        db.session.refresh(user)  # Reload user to ensure updated data is shown

    
        # Redirect to the same page to refresh 
        return redirect(url_for('views.profile_information'))
    
    # For GET requests, render the page with the current user's inforamtion
    return render_template('profile_information.html', user=user)



# For the admin to manage the users 
@views.route('/manage_users', methods=['GET', 'POST'])
@login_required
def manage_users():
    if not current_user.is_admin:
        flash('Access denied. Admins only.', category='error')
        return redirect(url_for('views.home'))

    users = User2.query.filter(User2.id != current_user.id).all()  # Exclude the current admin
    print(users)
    return render_template('manage_users.html', users=users)


@views.route('/toggle_user/<int:user_id>', methods=['POST'])
@login_required
def toggle_user(user_id):
    if not current_user.is_admin:
        flash("Access denied. Admins only.", category="error")
        return redirect(url_for('views.home'))

    user = User2.query.get(user_id)
    if not user:
        flash("User not found.", category="error")
        return redirect(url_for('views.manage_users'))

    # Toggle activation status
    user.is_active = not user.is_active
    db.session.commit()
    status = "activated" if user.is_active else "deactivated"
    flash(f"User {user.first_name} has been {status}.", category="success")

    return redirect(url_for('views.manage_users'))

