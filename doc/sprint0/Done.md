# Definition of Done

After discussions about the definition, we have agreed upon these terms to consider our project complete or done.

## General Expectations
- **Code Completion**: All code is written and reviewed.
- **Review**: The code has been peer-reviewed and feedback is addressed.
- **Unit & Integration Tests**: Relevant tests are written and passed.
- **Functional Testing**: The feature works as expected and no critical bugs exist.
- **Documentation**: All relevant documentation is updated, and GitHub is updated.

## User Stories Definition of Done

### User Story 1: Register for an account
**Definition of Done**:
- The user can successfully register, and the database is updated.
- The user can log in immediately after registration if required.

### User Story 2: Log in to access the dashboard
**Definition of Done**:
- Users can log in with valid credentials.
- The user is redirected to their personalized dashboard.
- Incorrect login attempts show an error message and do not grant access.

### User Story 3: Search for books by title
**Definition of Done**:
- The search field accepts user input and returns results.
- Results show all books matching the title (case insensitive).
- Results display relevant book details like title, author, and genre.

### User Story 4: View book details
**Definition of Done**:
- Book details page displays title, author, genre, availability, and description.
- Availability status is updated correctly.
- An option to be notified when the book is available is provided if unavailable.

### User Story 5: Borrow a book
**Definition of Done**:
- Book availability status is updated when borrowed.
- A borrowing record is created with user details.

### User Story 6: Return a book
**Definition of Done**:
- The book availability status updates to "available."
- The borrowing record is updated with the return date and status.
- A "THANKS FOR RETURNING" pop-up appears.

### User Story 7: View borrowing history
**Definition of Done**:
- Users can view a list of all borrowed books with dates.

### User Story 8: Receive notifications for due dates
**Definition of Done**:
- The user receives notifications (email) before the due date.
- Notifications include book title, due date, and return instructions.
- Notifications are sent at appropriate times (e.g., 1 day before the due date).

### User Story 9: Admin login to manage the library
**Definition of Done**:
- Admin can log in with valid credentials.
- Admin is redirected to the correct dashboard with management tools.
- Invalid login attempts show appropriate error messages.

### User Story 10: Add new books to the catalog
**Definition of Done**:
- Admin can successfully add a new book (title, author, genre, etc.).
- The new book is visible in the catalog and searchable.
- All mandatory fields are validated.
- Admin receives confirmation upon successful addition.

### User Story 11: Update book details
**Definition of Done**:
- Admin can edit book details.
- Updates are saved and displayed correctly.
- Changes are visible immediately in the catalog and search results.

### User Story 12: Remove books from the catalog
**Definition of Done**:
- Admin can successfully remove a book.
- The removed book no longer appears in search results or the catalog.

### User Story 13: Monitor user activity
**Definition of Done**:
- Admin can view a list of users and their borrowing activity.

### User Story 14: Generate borrowing reports
**Definition of Done**:
- Admin can generate reports on most borrowed books and user engagement.
- Reports are accurate for a specific time period.
- Reports are exportable (e.g., CSV, PDF) or viewable in the system.

### User Story 15: Filter search results by genre
**Definition of Done**:
- Users can filter search results by genre.
- Results display books relevant to the selected genre.
- No missing or incorrect genre data.

### User Story 16: Update profile information
**Definition of Done**:
- Users can update personal details.
- Changes are saved and reflected in the account.
- The user receives confirmation of the update.

### User Story 17: See popular books of the month
**Definition of Done**:
- Users see a list of popular books, updated monthly.
- The list includes book details like title and author.
- A scrollable list is available for easy navigation.

### User Story 18: Log out for account security
**Definition of Done**:
- Users can log out successfully.
- The session is securely terminated after logout.

### User Story 19: Admin manages user accounts
**Definition of Done**:
- Admin can deactivate or reactivate user accounts.
- User account status is updated immediately in the system.

### User Story 20: See recommended books
**Definition of Done**:
- Recommendations are generated based on the user’s borrowing history.
- Recommendations are displayed on the dashboard or in a separate section.
- Users can interact with recommendations (e.g., click for more details or borrow directly).
