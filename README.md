# BookHive: Library Management System

BookHive is a modern library management system designed to streamline the management of books, authors, and users while providing an intuitive interface for both administrators and readers. The platform serves as a gateway to a world of knowledge and imagination, featuring seamless book management, interactive dashboards, and an elegant design.

## Features

### User Features
 Browse Available Books: Explore the library's collection by genre, author, or title.
 Account Management: Users can register, log in, and recover passwords.
 Book Details: View detailed information about each book, including available copies and genre.
 Contact Us: Easily reach out to the library for queries or support.
### Admin Features
 Add New Books: Upload new books to the collection.
 Edit Existing Books: Modify book details such as title, author, genre, or availability.
Track Copies: Manage the total and remaining copies of each book.
Dashboard Overview: Monitor and manage the library efficiently.

## Technology Stack
### Frontend:
HTML5, CSS3, JavaScript (with animations for interactive elements)
Responsive design using modern web standards
### Backend:
Python (Flask Framework)
Jinja2 for templating
### Database:
MySQL for storing book and user data
### Hosting:
Flask development server
### Static Assets:
Images, videos, and CSS hosted in the /static folder

## Key Pages
Home Page: An interactive landing page featuring an animated book and project overview.
Login/Signup: User authentication pages with secure form handling.
Dashboard:
Admin Dashboard: Manage the library's collection.
User Dashboard: Explore and view available books.
Forgot Password: Password recovery form with email integration.
Contact Us: Submit inquiries or feedback.


## Setup and Installation
Follow these steps to set up the project locally:

1. Clone the Repository:
git clone https://github.com/hvpham-yorku/BookHive.git
cd BookHive

2. Install Dependencies
Make sure you have Python installed. Then, install the required packages:
pip install -r requirements.txt

3. Configure the Database and Tables:
  1. Start the Flask Shell
   flask shell
  2. Inside the shell, initialize the database:
     from website import db
      db.create_all()
     


4. Run the Application
Start the Flask development server:
flask run
Visit the app at http://127.0.0.1:5000.

## Future Improvements
Enhanced Search: Implement a robust search functionality for books and authors.
User Activity Tracking: Allow users to borrow and return books, with history tracking.
Recommendations: Add personalized book recommendations based on user preferences.
In-site Messaging features for Admin and regular Users.
Enabling users to rate books and displaying Book of Month on the Home Page.
Mobile App: Extend the functionality to mobile platforms.

## Contributing
Contributions are welcome! Follow these steps to contribute:
1. Fork the repository.
2. Create a new branch
 git checkout -b feature-branch
3. Commit changes and push to your branch.
4. Open a pull request with a description of your changes.

## Contact
For questions or feedback, please reach out via the Contact Us page on BookHive or send an email to librarymanagementsystem59@gmail.com.



