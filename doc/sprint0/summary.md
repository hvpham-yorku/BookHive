# Project Overview
The Library Management System is a full-stack web application aiming to digitize the management of library operations. Some possible actions are borrowing books, returns, and catalog management. The application is designed to serve both users and administrators.

## Objectives

- **Purpose**: To create an online platform enabling users to view the library catalog, check book availability, and manage borrowing/returning processes.
  
- **Key Technologies**:
  - Frontend: HTML, CSS, JavaScript
  - Backend: Python
  - Database: SQL
  - API: Flask API
   (Changed after sprint 1 design decisions. The changes have been approved by professor. For more information please read the lable of readme.md file)
## Key Users
1. **Main Users**:
   - Students
   - General readers who need to borrow books, check availability, and view their borrowing history.

2. **Administrators (admin)**:
   - Librarians
   - Authorized staff responsible for managing the library’s inventory, user accounts, and monitoring activity.

## Key Use Cases
- **User Actions**:
  - Registering and logging into the system
  - Searching for books by title, author, or genre
  - Borrowing available books and viewing borrowing history
  - Returning borrowed books and receiving notifications about due dates

- **Admin Actions**:
  - Managing the book catalog by adding, updating, or removing books
  - Monitoring user activity and sending reminders for overdue books
  - Accessing reports on book borrowing trends and user engagement

## Key Usage Scenarios
1. **User Journey**:
   - A user logs into the library system, searches for a specific book, checks its availability, and borrows it if available. The system updates the database to reflect the change in availability. The user can later return the book, and the system will update the record accordingly. Alerts are sent to remind the user of due dates.

2. **Admin Journey**:
   - An administrator logs into the system to add new books to the catalog and updates details for existing books based on new stock or changes in information. The admin can also check borrowing statistics, and send reminders for overdue books.

## Principles
- **Clear Communication / Notifications**: Users will be communicated with and receive notifications that remind them of the returning due dates.
  
- **User-Centric**: Having a simplified user interface to ensure users have a smooth experience.
  
- **Efficiency / Productivity**: Prioritizing features that ensure efficiency and user productivity, such as quick search, automated notifications, etc.
  
- **Accessibility / Inclusivity**: Ensuring users have access to an inclusive platform regardless of their specific needs.
