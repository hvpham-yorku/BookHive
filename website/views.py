from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Book, BorrowedBook
from . import db
import json
from flask_mail import Message
from datetime import datetime, timedelta
from . import mail
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from threading import Thread
from sqlalchemy import extract,func
from datetime import datetime
from .models import User2
views = Blueprint('views', __name__)

def get_best_books():
    current_month = datetime.now().month
    current_year = datetime.now().year

    best_books = db.session.query(
        Book.id,
        Book.name,
        Book.author,
        func.avg(BorrowedBook.rating).label('avg_rating')
    ).join(BorrowedBook, Book.id == BorrowedBook.book_id)\
    .filter(
        BorrowedBook.rating.isnot(None),
        BorrowedBook.returned == True,
        extract('month', BorrowedBook.borrowed_date) == current_month,
        extract('year', BorrowedBook.borrowed_date) == current_year
    ).group_by(Book.id)\
    .order_by(func.avg(BorrowedBook.rating).desc())\
    .limit(5).all()

    return best_books

@views.route('/')
@login_required
def home():
    best_books = get_best_books()
    return render_template(
        'home.html',
        name=current_user.first_name,
        is_admin=current_user.is_admin,
        best_books=best_books
    )


from sqlalchemy import func

from sqlalchemy import func

@views.route('/book-list', methods=['GET', 'POST'])
@login_required
def book_list():
    selected_author = request.args.get('author')
    selected_genre = request.args.get('genre')

    # Base query to fetch books
    base_query = db.session.query(
        Book.id,
        Book.name,
        Book.author,
        Book.genre,
        Book.remaining_copies,
        func.coalesce(func.avg(BorrowedBook.rating), 0).label('average_rating')
    ).outerjoin(BorrowedBook, Book.id == BorrowedBook.book_id)

    if selected_author:
        base_query = base_query.filter(Book.author == selected_author)
    elif selected_genre:
        base_query = base_query.filter(Book.genre == selected_genre)

    # Group by book and fetch all results
    books = base_query.group_by(Book.id).all()

    # Fetch distinct genres and authors for filtering
    genres = db.session.query(Book.genre).distinct().all()
    authors = db.session.query(Book.author).distinct().all()

    # Fetch borrowed books to disable borrowing for current user
    borrowed_book_ids = [borrow.book_id for borrow in BorrowedBook.query.filter_by(user_id=current_user.id, returned=False).all()]

    return render_template(
        'book_list.html',
        books=books,
        borrowed_book_ids=borrowed_book_ids,
        genres=genres,
        authors=authors
    )




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
    due_date = datetime.now() + timedelta(days = 14)  # 14-day loan period
    new_borrow = BorrowedBook(
        user_id=current_user.id,
        book_id=book.id,
        borrowed_date=datetime.now(),
        due_date=due_date
    )
    book.remaining_copies -= 1
    db.session.add(new_borrow)
    db.session.commit()

    # Send Loan Receipt Email
    send_loan_receipt(current_user.email, book.name, book.author, new_borrow.borrowed_date, new_borrow.due_date)

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

@views.route('/my-books', methods=['GET', 'POST'])
@login_required
def my_books():
    # Fetch books
    borrowed_books = BorrowedBook.query.filter_by(user_id=current_user.id).all()

    in_progress_books = []
    overdue_books = []

    for borrow in borrowed_books:
        if borrow.returned:
            continue
        if borrow.due_date < datetime.now():
            overdue_days = (datetime.now() - borrow.due_date).days
            fine = round(overdue_days * 0.10, 2)
            overdue_books.append({'name': borrow.book.name, 'author': borrow.book.author, 'due_date': borrow.due_date, 'fine': fine, 'id': borrow.id})
        else:
            in_progress_books.append({'name': borrow.book.name, 'author': borrow.book.author, 'due_date': borrow.due_date, 'id': borrow.id, 'content_link': borrow.book.content_link})

    # Check if the popup needs to be shown
    show_rating_popup = request.args.get('show_rating_popup', default=False, type=bool)
    borrow_id = request.args.get('borrow_id', type=int)

    return render_template('my_books.html', in_progress_books=in_progress_books, overdue_books=overdue_books, show_rating_popup=show_rating_popup, borrow_id=borrow_id)


@views.route('/return-book/<int:borrow_id>', methods=['POST'])
@login_required
def return_book(borrow_id):
    borrowed_book = BorrowedBook.query.get(borrow_id)

    if not borrowed_book or borrowed_book.user_id != current_user.id:
        flash('Invalid request.', category='error')
        return redirect(url_for('views.my_books'))

    # Mark as returned
    borrowed_book.returned = True
    borrowed_book.book.remaining_copies += 1
    db.session.commit()

    # Send Return Confirmation Email
    send_return_confirmation(
        current_user.email,
        borrowed_book.book.name,
        borrowed_book.borrowed_date,
        borrowed_book.due_date
    )

    flash(f'You have successfully returned "{borrowed_book.book.name}". Please rate the book.', category='success')

    # Redirect to the rating page
    return redirect(url_for('views.rate_book', borrow_id=borrow_id))


def send_return_confirmation(email, book_name, borrow_date, due_date):
    msg = Message(
        subject="Return Confirmation: Book Successfully Returned",
        recipients=[email],
        body=f"""
        Thank you for returning the book!

        Details of your loan:
        - Book Title: {book_name}
        - Borrowed Date: {borrow_date.strftime('%Y-%m-%d')}
        - Due Date: {due_date.strftime('%Y-%m-%d')}

        We hope you enjoyed reading this book. Please take a moment to rate your experience.

        Happy Reading!
        Library Management System
        """
    )
    mail.send(msg)



@views.route('/rate-book/<int:borrow_id>', methods=['GET', 'POST'])
@login_required
def rate_book(borrow_id):
    borrowed_book = BorrowedBook.query.get(borrow_id)
    if not borrowed_book or borrowed_book.user_id != current_user.id:
        flash('Invalid request.', category='error')
        return redirect(url_for('views.my_books'))

    if request.method == 'POST':
        rating = request.form.get('rating')
        if rating:
            borrowed_book.rating = int(rating)
            db.session.commit()
            flash(f'Thank you for rating the book "{borrowed_book.book.name}"!', category='success')
            return redirect(url_for('views.my_books'))
        else:
            flash('Please select a rating before submitting.', category='error')

    return render_template('rate_book.html', borrowed_book=borrowed_book)


@views.route('/reports', methods=['GET'])
@login_required
def report_page():
    # Renders the reports.html page
    return render_template('reports.html', user=current_user)

@views.route('/reports/data', methods=['GET'])
@login_required
def report_data():
    # Fetch Most Borrowed Books
    most_borrowed_books = db.session.query(
        Book.name,
        db.func.count(BorrowedBook.id).label('borrow_count')
    ).join(BorrowedBook, BorrowedBook.book_id == Book.id)\
     .filter(BorrowedBook.returned == False)\
     .group_by(Book.id)\
     .order_by(db.desc('borrow_count')).limit(5).all()

    # Fetch Active Users
    active_users = db.session.query(
        db.func.count(User2.id)
    ).join(BorrowedBook, BorrowedBook.user_id == User2.id)\
     .filter(BorrowedBook.returned == False).scalar()

    # Fetch Borrowing Trends (Date Formatting Adjusted)
    borrowing_trends = db.session.query(
        BorrowedBook.borrowed_date.label('borrow_date'),
        db.func.count(BorrowedBook.id).label('borrow_count')
    ).filter(
        BorrowedBook.borrowed_date >= datetime.now() - timedelta(days=30)
    ).group_by(BorrowedBook.borrowed_date).order_by(BorrowedBook.borrowed_date).all()

    # Adjust data formatting for trends to include formatted dates
    trends = [{'date': trend.borrow_date.strftime('%Y-%m-%d'), 'count': trend.borrow_count} for trend in borrowing_trends]

    # Return JSON response
    return jsonify({
        'most_borrowed_books': [{'name': book[0], 'count': book[1]} for book in most_borrowed_books],
        'active_users': active_users,
        'borrowing_trends': trends
    })
