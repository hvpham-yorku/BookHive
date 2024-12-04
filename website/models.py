"""
The `models.py` file defines the database schema for the library system using SQLAlchemy ORM. It includes the following tables:

1. `Note`:
   - Stores notes associated with users, including text data and timestamps.

2. `Book`:
   - Represents the library's catalog of books, including details such as title, author, genre, and availability.
   - Tracks borrowing records through a relationship with the `BorrowedBook` table.

3. `User2`:
   - Represents users in the system, including both regular users and administrators.
   - Includes personal details, account status, and relationships with borrowed books and user messages.

4. `BorrowedBook`:
   - Tracks borrowing transactions, linking users and books.
   - Records borrowing dates, due dates, return status, and optional user ratings.

5. `UserMessage`:
   - Stores messages sent to users, such as notifications or administrative updates.
   - Tracks whether messages have been read and includes timestamps for creation.

Each table is implemented as a Python class inheriting from `db.Model`, and relationships between tables are defined using SQLAlchemy's `relationship` and `ForeignKey`.
"""
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user2.id'))

"""
The `Book` table represents the library's collection of books and their details.

Columns:
1. `id` (Integer, Primary Key): 
   - A unique identifier for each book.
2. `name` (String, 150, Non-Nullable): 
   - The title of the book.
3. `author` (String, 150, Non-Nullable): 
   - The name of the book's author.
4. `genre` (String, 50, Nullable): 
   - The genre of the book (optional).
5. `copies` (Integer, Non-Nullable): 
   - The total number of copies of the book available in the library.
6. `remaining_copies` (Integer, Non-Nullable): 
   - The number of copies currently available for borrowing.
7. `content_link` (String, 500, Nullable): 
   - An optional link to access the book's content (e.g., digital version or external reference).

Relationships:
- `borrowed_books`: 
   - Establishes a one-to-many relationship with the `BorrowedBook` table, tracking all borrowing records associated with this book.

This table is essential for maintaining the library's catalog, tracking the availability of books, and linking borrow records through the `BorrowedBook` relationship.
"""
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # a reference ID
    name = db.Column(db.String(150), nullable=False)  # a title
    author = db.Column(db.String(150), nullable=False)  # an author
    genre = db.Column(db.String(50), nullable=True)  # genre (optional)
    copies = db.Column(db.Integer, nullable=False)  # number of total copies
    remaining_copies = db.Column(db.Integer, nullable=False)  # number of remaining copies
    content_link = db.Column(db.String(500), nullable=True)  # link to access the book (optional)
    borrowed_books = db.relationship('BorrowedBook', backref='book')# relationship to track borrow records for this book

"""
The `User2` table represents the users of the library system, including both regular users and administrators.

Columns:
1. `id` (Integer, Primary Key): 
   - A unique identifier for each user.
2. `email` (String, 150, Unique): 
   - The user's email address, used for login and communication.
3. `password` (String, 150): 
   - The hashed password for the user's account.
4. `first_name` (String, 150): 
   - The user's first name.
5. `last_name` (String, 150): 
   - The user's last name.
6. `date_of_birth` (Date): 
   - The user's date of birth.
7. `address` (String, 100): 
   - The user's residential address.
8. `is_admin` (Boolean, Default False): 
   - Indicates whether the user has administrative privileges.
9. `is_active` (Boolean, Default True): 
   - Indicates whether the user's account is active or deactivated.

Relationships:
- `borrowed_books`: 
   - Establishes a one-to-many relationship with the `BorrowedBook` table, tracking all books borrowed by the user.
- `messages`: 
   - Establishes a one-to-many relationship with the `UserMessage` table, storing all messages sent to the user.

This table serves as the central repository for user information, supporting user authentication, account management, and role-based access within the system.
"""
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
<<<<<<< HEAD
    is_active = db.Column(db.Boolean, default=True)  
=======
    is_active = db.Column(db.Boolean, default=True)  # To check if the account is active

>>>>>>> 03edd5c3082998ed70a6ba6db7ebb680f8f8b3f4

"""
The `BorrowedBook` table tracks borrowing transactions in the library system, linking users with the books they have borrowed.

Columns:
1. `id` (Integer, Primary Key): 
   - A unique identifier for each borrowing transaction.
2. `book_id` (Integer, Foreign Key `book.id`, Non-Nullable): 
   - References the `Book` table to identify the borrowed book.
3. `user_id` (Integer, Foreign Key `user2.id`, Non-Nullable): 
   - References the `User2` table to identify the user who borrowed the book.
4. `borrowed_date` (DateTime, Default `datetime.now`): 
   - The date and time when the book was borrowed.
5. `due_date` (DateTime, Non-Nullable): 
   - The date and time by which the book must be returned.
6. `returned` (Boolean, Default False): 
   - Indicates whether the book has been returned.
7. `rating` (Integer, Nullable): 
   - An optional field allowing users to rate the book after returning it.
8. `return_date` (DateTime, Nullable): 
   - The date and time when the book was returned, if applicable.

Relationships:
- Links to the `Book` table via `book_id` to identify the book being borrowed.
- Links to the `User2` table via `user_id` to track the borrowing user.

This table is crucial for managing borrowing activity, enforcing due dates, tracking returns, and collecting feedback through user ratings.
"""
class BorrowedBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
<<<<<<< HEAD
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user2.id'), nullable=False)
    borrowed_date = db.Column(db.DateTime, default=datetime.now)
    due_date = db.Column(db.DateTime, nullable=False)
    returned = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Integer, nullable=True)  
    return_date = db.Column(db.DateTime, nullable=True)

"""
The `UserMessage` table stores messages sent to users within the library system.

Columns:
1. `id` (Integer, Primary Key): 
   - A unique identifier for each message.
2. `user_id` (Integer, Foreign Key `user2.id`): 
   - References the `User2` table to associate the message with a specific user.
3. `content` (String, 500, Non-Nullable): 
   - The message content to be displayed to the user.
4. `is_read` (Boolean, Default False): 
   - Indicates whether the message has been read by the user.
5. `timestamp` (DateTime, Default `func.now()`): 
   - The date and time when the message was created.

Relationships:
- Links to the `User2` table via `user_id` to identify the recipient of the message.

This table facilitates user notifications by storing system-generated or admin-generated messages and tracking whether they have been read.
"""    
=======
    user_id = db.Column(db.Integer, db.ForeignKey('user2.id'))  
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))  
    borrow_date = db.Column(db.DateTime, default=func.now())   
    due_date = db.Column(db.DateTime)                         
    returned = db.Column(db.Boolean, default=False)

>>>>>>> 03edd5c3082998ed70a6ba6db7ebb680f8f8b3f4
class UserMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user2.id'))
    content = db.Column(db.String(500), nullable=False)
<<<<<<< HEAD
    is_read = db.Column(db.Boolean, default=False)  
    timestamp = db.Column(db.DateTime, default=func.now())



=======
    is_read = db.Column(db.Boolean, default=False)  # To track if the message is read
    timestamp = db.Column(db.DateTime, default=func.now())
>>>>>>> 03edd5c3082998ed70a6ba6db7ebb680f8f8b3f4
