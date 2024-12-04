"""
The `views` Blueprint handles core application functionality for the library system. 

Key Features:
1. **Home and Navigation**:
   - Includes routes for displaying the homepage, book lists, and user recommendations.
   - Dynamically fetches and displays data based on user activity and database records.

2. **Library Management**:
   - Provides routes for managing books (`add_book`, `edit_book`, `delete_book`) with admin-only access.
   - Allows users to borrow, return, and rate books.

3. **User Interaction**:
   - Includes features like viewing messages, updating profile information, and contacting the library system.
   - Supports notifications and contextual messages for personalized user experiences.

4. **Admin Controls**:
   - Offers admin-exclusive routes for tracking user activity, managing accounts, and accessing reports.
   - Enables toggling user activation status and viewing detailed user activity reports.

5. **Reports and Analytics**:
   - Generates statistical data such as borrowing trends, most borrowed books, and active user counts.
   - Provides endpoints for backend analytics and frontend visualizations.

6. **Notifications and Messaging**:
   - Implements a message system for user notifications, including unread message counts.
   - Ensures all messages are contextually available across templates using a context processor.

7. **Error Handling and User Feedback**:
   - Provides appropriate error messages and redirects for unauthorized or invalid actions.
   - Utilizes Flask's flash messages for immediate user feedback.

Dependencies:
- Flask extensions:
  - `flask_login` for user authentication and session management.
  - `flask_sqlalchemy` for database interactions.
  - `flask_mail` for email notifications.
- SQLAlchemy for database querying and relationships.
- Utility libraries like `datetime` for date operations.

This Blueprint serves as the backbone of the application, integrating user-facing features, admin tools, and analytics to provide a seamless library management experience.
"""
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Book, BorrowedBook
from . import db
import json
from flask_mail import Message
from .models import UserMessage  
from datetime import datetime, timedelta
from . import mail
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from threading import Thread
from sqlalchemy import extract,func
from sqlalchemy.sql.expression import func
from datetime import datetime
from .models import User2
views = Blueprint('views', __name__)
from .models import UserMessage  


"""The get_best_books function retrieves the top-rated books for the current month to display them on the homepage as the "Best of the Month." It queries the database for books that meet the following criteria:

Returned Books Only: Ensures only books that have been returned are considered.
Books Rated by Users: Includes only books that have a non-None rating.
Borrowed in the Current Month and Year: Filters books borrowed during the current month and year using the borrowed_date.
Top 5 by Average Rating: Groups books by their IDs, calculates the average rating, and orders them in descending order of their average rating, limiting the results to the top 5.


Parameters:
None. The function dynamically calculates the current month and year using the datetime.now() method.


Returns:
A list of tuples containing the following:
Book.id: The ID of the book.
Book.name: The name of the book.
Book.author: The author of the book.
avg_rating: The average rating of the book.


This function is intended to be used for dynamically displaying a curated list of the best books of the month on the homepage."""
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

"""
The `home` route is responsible for rendering the homepage of the application. 

- It retrieves the "Best of the Month" books using the `get_best_books` function.
- The route ensures that only logged-in users can access the homepage, as indicated by the `@login_required` decorator.
- It passes user-specific and dynamic content to the `home.html` template for rendering.

Parameters:
- None (handled internally via Flask's route mechanism).

Template Variables Passed:
- `name`: The first name of the currently logged-in user, used for personalized greetings.
- `is_admin`: A boolean indicating whether the current user has administrative privileges.
- `best_books`: A list of the top-rated books for the current month, retrieved by `get_best_books`.

Returns:
- The rendered `home.html` template populated with dynamic content.

This route serves as the primary landing page for authenticated users, showcasing the top books of the month and user-specific information.
"""

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

"""
The `book_list` route renders a list of all available books in the library, with filters for genre and author.

- Method: Supports `GET` and `POST`.
- Login Required: The route ensures only authenticated users can access it via the `@login_required` decorator.

Functionality:
1. Filtering by Author or Genre:
   - Fetches filter options from query parameters (`author` or `genre`) passed via `request.args`.
   - Filters the book list dynamically based on the selected author or genre.
2. Book List with Ratings:
   - Joins the `Book` and `BorrowedBook` tables to calculate the average rating for each book using `func.coalesce`.
   - Includes key book details like title, author, genre, remaining copies, and average rating.
3. Group and Aggregate:
   - Groups the query results by book ID to ensure distinct entries.
4. Distinct Authors and Genres:
   - Fetches all unique authors and genres to provide filtering options on the frontend.
5. Borrowed Books:
   - Identifies books already borrowed by the current user (`borrowed_book_ids`) to disable their borrow buttons on the frontend.

Template Variables Passed:
- `books`: A list of books with their details, including ID, name, author, genre, remaining copies, and average rating.
- `borrowed_book_ids`: A list of book IDs that the current user has already borrowed and not returned.
- `genres`: A list of distinct genres available in the library for filtering.
- `authors`: A list of distinct authors available in the library for filtering.

Returns:
- Renders the `book_list.html` template with dynamic content for displaying books and filters.

This route serves as a central location for users to browse available books, view their ratings, and apply filters to refine their search.
"""

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


"""
The `delete_book` route allows an admin user to delete a book from the library system.

- Method: Accepts `POST` requests.
- Login Required: Ensures that only authenticated users can access this route via the `@login_required` decorator.
- Admin Only: Restricts access to admin users. Non-admin users are redirected with an error message.

Functionality:
1. Admin Authorization:
   - Checks if the currently logged-in user is an admin (`current_user.is_admin`).
   - Displays an error message and redirects non-admin users to the book list page.
2. Book Existence Check:
   - Fetches the book by `book_id` from the database.
   - Displays an error message and redirects if the book is not found.
3. Delete Book:
   - Deletes the book record from the database using `db.session.delete`.
   - Commits the deletion to persist the changes.
   - Displays a success message indicating the book has been deleted.
4. Redirection:
   - Redirects the user to the `book_list` page after the deletion.

Template Variables Passed:
- None (the route handles redirection).

Parameters:
- `book_id` (int): The ID of the book to be deleted.

Returns:
- Redirects the user to the `book_list` page with a flash message indicating the result of the operation.

This route ensures that only authorized users (admins) can manage and delete books from the library system, maintaining the integrity of the book catalog.
"""
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




"""
The `borrow_book` route allows authenticated users to borrow a book from the library, provided it is available and the user meets borrowing criteria.

- Method: Accepts `POST` requests.
- Login Required: Ensures only authenticated users can access this functionality via the `@login_required` decorator.

Functionality:
1. Book Availability Check:
   - Verifies if the book exists in the database and has remaining copies available.
   - Displays an error message and redirects if the book is unavailable.

2. Duplicate Borrow Check:
   - Ensures the user has not already borrowed the same book without returning it.
   - Displays an error message if a duplicate borrow attempt is detected.

3. Borrowing Limit Check:
   - Verifies that the user has not exceeded the borrowing limit (5 books).
   - Displays an error message and redirects if the limit is reached.

4. Book Borrowing:
   - Creates a new record in the `BorrowedBook` table with the current user, book, and loan details.
   - Reduces the `remaining_copies` of the book by 1.

5. Notification Creation:
   - Adds a message to the `UserMessage` table, notifying the user of their successful borrowing and the due date.

6. Database Commit:
   - Saves the changes to the database, including the updated book and borrowing records.

7. Email Notification:
   - Sends a loan receipt email to the user with details about the borrowed book and the due date using the `send_loan_receipt` function.

8. User Feedback:
   - Displays a success message and redirects the user back to the book list.

Parameters:
- `book_id` (int): The ID of the book the user wants to borrow.

Returns:
- Redirects the user to the `book_list` page with a flash message indicating the result of the borrowing operation.

Helper Function:
- `send_loan_receipt`: Sends an email with loan details, including the book title, author, borrowing date, and due date.

This route ensures proper validation of borrowing conditions and provides the user with immediate feedback and notifications, enhancing the user experience.
"""

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
     # Create a notification message for the Messages Tab
    message_content = f'You have successfully borrowed "{book.name}" by {book.author}. It is due on {due_date.strftime("%b %d, %Y")}.'
    new_message = UserMessage(
    user_id=current_user.id,
    content=message_content,
    )
    db.session.add(new_message)

    # Commit changes to the database
    db.session.commit()
    db.session.commit()

    # Send Loan Receipt Email
    send_loan_receipt(current_user.email, book.name, book.author, new_borrow.borrowed_date, new_borrow.due_date)

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






"""
The `add_book` route allows admin users to add new books to the library system.

- Method: Supports both `GET` and `POST` requests.
- Login Required: Ensures only authenticated users can access this functionality via the `@login_required` decorator.
- Admin Only: Restricts access to admin users. Non-admin users are redirected to the home page with an error message.

Functionality:
1. Admin Authorization:
   - Verifies if the currently logged-in user is an admin (`current_user.is_admin`).
   - Displays an error message and redirects non-admin users to the homepage.

2. Form Handling:
   - On `POST` requests:
     - Collects book details (`name`, `author`, `genre`, `copies`, `content_link`) from the form.
     - Validates required fields (`name`, `author`, `copies`) to ensure they are not empty.
     - Displays an error message if any required fields are missing.
     - Creates a new `Book` object with the provided details, setting `remaining_copies` to the initial number of `copies`.
     - Saves the new book to the database.
     - Displays a success message and redirects to the `book_list` page.
   - On `GET` requests:
     - Renders the `add_book.html` template to display the book addition form.

3. Database Commit:
   - Adds the new book to the database and commits the changes, ensuring persistence.

Parameters:
- None (handled via form data in `POST` requests).

Template Variables Passed:
- None (renders the `add_book.html` template directly).

Returns:
- On `GET`: Renders the `add_book.html` template with the form for adding a new book.
- On `POST`: Redirects the user to the `book_list` page after successfully adding the book.

This route provides a simple and secure way for admin users to expand the library's catalog by adding new books with relevant details.
"""

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

"""
The `edit_book` route allows admin users to update the details of an existing book in the library system.

- Method: Supports both `GET` and `POST` requests.
- Login Required: Ensures only authenticated users can access this functionality via the `@login_required` decorator.
- Admin Only: Restricts access to admin users. Non-admin users are redirected to the home page with an error message.

Functionality:
1. Admin Authorization:
   - Verifies if the currently logged-in user is an admin (`current_user.is_admin`).
   - Displays an error message and redirects non-admin users to the homepage.

2. Fetch Book Details:
   - Retrieves the book record by `book_id` from the database.
   - Displays an error message and redirects to the `book_list` page if the book is not found.

3. Form Handling:
   - On `POST` requests:
     - Updates the book's attributes (`name`, `author`, `genre`, `copies`, `remaining_copies`, `content_link`) with data from the form.
     - Saves the updated book details to the database.
     - Displays a success message and redirects to the `book_list` page.
   - On `GET` requests:
     - Renders the `edit_book.html` template with the current details of the book, allowing the admin to edit them.

4. Database Commit:
   - Saves the updated book details to the database to ensure persistence.

Parameters:
- `book_id` (int): The ID of the book to be edited.

Template Variables Passed:
- `book`: The `Book` object containing the current details of the book to be edited.

Returns:
- On `GET`: Renders the `edit_book.html` template with the current book details.
- On `POST`: Redirects the user to the `book_list` page after successfully updating the book.

This route provides an efficient way for admin users to manage and update the library's catalog by modifying existing book details.
"""

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

"""
The `search_books` route allows users to search for books in the library based on the book's name, author, or genre.

- Method: Supports `GET` requests.
- Login Required: Ensures only authenticated users can access this functionality via the `@login_required` decorator.

Functionality:
1. Extracts the search query from the request URL's query parameters (`query`). 
   - Trims any leading or trailing whitespace using `.strip()`.
   - Defaults to an empty string if no query is provided.
2. Performs a case-insensitive search on the `Book` table:
   - Matches the search term against the `name`, `author`, or `genre` fields.
   - Uses `ilike` to perform the case-insensitive search.
3. Handles Empty Search:
   - If no query is provided, it flashes an error message prompting the user to enter a search term.
4. Renders the `search_books.html` template:
   - Passes the search results (`books`) and the original query back to the template for display.

Parameters:
- None (the query is extracted from the request's query parameters).

Template Variables Passed:
- `results`: A list of books matching the search query.
- `query`: The original search term entered by the user.

Returns:
- Renders the `search_books.html` template with the search results and the query term.

This route provides a simple search functionality for users to find books based on their preferences.
"""
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
"""
The `contact_us` route allows users to submit queries or feedback to the library management system.

- Method: Supports `GET` and `POST` requests.
- Login Required: Ensures only authenticated users can access this functionality via the `@login_required` decorator.

Functionality:
1. Handles `GET` Requests:
   - Renders the `contact_us.html` template to display the contact form.

2. Handles `POST` Requests:
   - Collects user input from the contact form, including `name`, `email`, and the query message.
   - Sends an email containing the user's query to the library's management email address (`librarymanagementsystem59@gmail.com`).
   - Displays a success message to the user confirming that their query has been submitted.
   - Redirects the user to the homepage after submission.

3. Email Content:
   - The email includes the user's name, email, and query details for easy tracking and response by the library management team.

Parameters:
- None (the form data is extracted from the request during `POST`).

Template Variables Passed:
- None (renders the `contact_us.html` template directly for `GET` requests).

Returns:
- On `GET`: Renders the `contact_us.html` template with the contact form.
- On `POST`: Redirects to the homepage with a flash message indicating successful submission.

This route provides users with a way to directly contact the library management system for support, inquiries, or feedback.
"""

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

"""
The `my_books` route displays a categorized list of books borrowed by the current user, including books currently in progress, overdue books, and past (returned) books.

- Method: Supports `GET` and `POST` requests.
- Login Required: Ensures only authenticated users can access this functionality via the `@login_required` decorator.

Functionality:
1. Fetches Borrowed Books:
   - Retrieves all books borrowed by the current user from the `BorrowedBook` table.
   - Categorizes them into:
     - `in_progress_books`: Books the user is currently borrowing and are not overdue.
     - `overdue_books`: Books whose due date has passed.
     - `past_books`: Books that have been returned.

2. Categorization Logic:
   - **Returned Books (`past_books`)**:
     - Includes books marked as `returned = True` and provides details like title, author, and return date.
   - **Books in Progress (`in_progress_books`)**:
     - Includes books that are still being borrowed and have not yet reached their due date.
   - **Overdue Books (`overdue_books`)**:
     - Includes books whose `due_date` has passed.
     - Calculates a fine based on the number of overdue days (`$0.10 per day`).

3. Template Variables:
   - `in_progress_books`: A list of dictionaries containing details of books currently being borrowed.
   - `past_books`: A list of dictionaries containing details of returned books.
   - `overdue_books`: A list of dictionaries containing details of overdue books, including fines.

4. Handles Missing Data:
   - Checks if fields like `due_date` or `return_date` are `None` to prevent errors.

Parameters:
- None (the user's ID is determined via `current_user.id`).

Returns:
- Renders the `my_books.html` template with categorized book lists (`in_progress_books`, `past_books`, and `overdue_books`).

This route provides users with an organized view of their borrowed books, helping them track overdue items and manage their library activity.
"""

@views.route('/my-books', methods=['GET', 'POST'])
@login_required
def my_books():
    borrowed_books = BorrowedBook.query.filter_by(user_id=current_user.id).all()
    in_progress_books = []
    past_books = []
    overdue_books = []

    for borrow in borrowed_books:
        if borrow.returned:
            past_books.append({
                'id': borrow.id,
                'name': borrow.book.name,
                'author': borrow.book.author,
                'return_date': borrow.return_date  # Ensure this is handled
            })
        else:
            book_data = {
                'id': borrow.id,
                'name': borrow.book.name,
                'author': borrow.book.author,
                'due_date': borrow.due_date,  # Handle if due_date is None
                'content_link': borrow.book.content_link
            }

            if borrow.due_date and borrow.due_date < datetime.now():
                overdue_days = (datetime.now() - borrow.due_date).days
                fine = overdue_days * 0.10  # Fine is 10 cents per day
                overdue_books.append({
                    **book_data,
                    'fine': round(fine, 2)
                })
            else:
                in_progress_books.append(book_data)

    return render_template(
        'my_books.html',
        in_progress_books=in_progress_books,
        past_books=past_books,
        overdue_books=overdue_books
    )

"""
The `return_book` route allows users to return a borrowed book, marking it as returned and updating the library's database.

- Method: Supports `POST` requests.
- Login Required: Ensures only authenticated users can access this functionality via the `@login_required` decorator.

Functionality:
1. Fetches the Borrowed Book:
   - Retrieves the `BorrowedBook` entry using the `borrow_id` from the URL.
   - Validates that the entry exists and belongs to the current user.
   - Displays an error message and redirects to the `my_books` page if the request is invalid.

2. Marks the Book as Returned:
   - Sets the `returned` flag to `True` for the borrowed book.
   - Updates the `return_date` field with the current date and time.
   - Increments the `remaining_copies` of the book in the library.

3. Notification Creation:
   - Generates a user notification message confirming the book has been successfully returned.

4. Database Commit:
   - Saves the updated book status and the notification to the database.

5. User Feedback:
   - Displays a success message and redirects the user to the `rate_book` page, encouraging them to rate the returned book.

6. Return Confirmation Email (Optional Helper Function):
   - The `send_return_confirmation` function can be used to send an email to the user confirming the book's return. The email includes details like the book's title, borrowing date, and due date.

Parameters:
- `borrow_id` (int): The ID of the `BorrowedBook` record to be returned.
