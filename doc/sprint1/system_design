# Library Management System: System Design Document

## 1. High-Level Architecture
The system follows a modular design, consisting of the following components:
- **Database Layer**: SQLite database (`database.db`) for user and admin information and book information.
- **Controllers**: Python modules (`auth.py`, `models.py`, `views.py`) to handle backend logic.
- **Frontend**: HTML and CSS templates and JavaScript files for user interaction.


## 2. CRC Cards

### 2.1 User Authentication (`auth.py`)
**Class Name**: auth  
**Parent Class**: None  
**Subclasses**: None  

**Responsibilities**:
- Authenticate users via login.
- Manage user registration.

**Collaborators**:
- `models.py` (for user data storage/retrieval).
- `views.py` (to route requests).

### 2.2 Book Management (`models.py`)
**Class Name**: models  
**Parent Class**: None  
**Subclasses**: None  

**Responsibilities**:
- Manage book inventory.
- Handle book borrowing/returning.

## 3. System Interaction with the Environment
- **Programming Language**: Python 3
- **Framework**: Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Operating System**: Cross-platform


## 4. Error and Exception Handling
- **Invalid Input**: Provide clear error messages on user-facing forms.
- **Database Errors**: Log errors and clear error message.
