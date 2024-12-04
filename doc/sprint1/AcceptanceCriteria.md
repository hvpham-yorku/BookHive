# Sprint 1 User Stories Breakdown

This document provides a breakdown of the user stories assigned for Sprint 1, including **acceptance criteria**, **implementation steps**, and **testing plan**.

---

## **1. Register for an account (User Story #1)**

### **User Story:**
_As a user, I want to register for an account so that I can borrow books._

### **Acceptance Criteria:**
- User can successfully create an account with valid details.
- System sends a confirmation message upon successful registration.

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`POST /register`).
   - Validate input (e.g., email format, password strength).
   - Check for duplicate accounts.
   - Store the new account in the database.
2. **Frontend:**
   - Create a registration form with fields (name, email, password, etc.).
   - Display success or error messages based on the API response.
3. **Database:**
   - Design a `Users` table with fields for name, email, password (hashed), etc.

### **Testing Plan:**
- Unit tests for backend API to validate inputs and handle edge cases.
- UI testing for form validation and success/error messages.

---

## **2. Log in to account (User Story #2)**

### **User Story:**
_As a user, I want to log in to my account so that I can access my dashboard._

### **Acceptance Criteria:**
- User can log in with valid credentials.
- Invalid credentials display an error message.
- Successful login redirects the user to their dashboard.

### **Implementation Steps:**
1. **Backend:**
   - Create a login API endpoint (`POST /login`).
   - Validate user credentials (email and password).
   - Generate a session token upon success.
2. **Frontend:**
   - Build a login form with fields for email and password.
   - Redirect user to the dashboard after successful login.
3. **Database:**
   - Query the `Users` table for valid credentials.

### **Testing Plan:**
- Test for valid and invalid login attempts.
- Check for redirection to the dashboard upon success.

---

## **3. Search for books by title (User Story #3)**

### **User Story:**
_As a user, I want to search for books by title so that I can find specific books easily._

### **Acceptance Criteria:**
- Search results must display all books matching the title input.
- Partial title matches should also be included in the results.
- The system must handle cases where no books match the search query (e.g., display "No results found").

### **Implementation Steps:**
1. **Backend:**
   - Set up an API endpoint for searching books (`GET /search?title=<title>`).
   - Query the database to find books whose titles match the input.
2. **Frontend:**
   - Create a search input field and button in the UI.
   - Display the results dynamically below the search field.
   - Show "No results found" when the API returns an empty list.

### **Testing Plan:**
- Write unit tests for the backend API to ensure correct results for:
  - Exact matches.
  - Partial matches.
  - No matches.
- Conduct manual tests on the frontend for usability and edge cases.

---

## **4. View book details (User Story #4)**

### **User Story:**
_As a user, I want to view book details so that I can check availability before borrowing._

### **Acceptance Criteria:**
- The book details page displays title, author, genre, availability status, and description.
- Users can access the details page by selecting a book from the search results.

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`GET /books/:id`) to fetch book details.
2. **Frontend:**
   - Create a book details page.
   - Link books in the search results to their details page.
3. **Database:**
   - Store book details in the `Books` table.

### **Testing Plan:**
- Verify correct details are fetched and displayed for each book.
- Test UI navigation from search results to the book details page.

---

## **5. Borrow a book (User Story #5)**

### **User Story:**
_As a user, I want to borrow a book so that I can read it._

### **Acceptance Criteria:**
- Borrowing updates the book's availability.
- A borrowing record is created with a due date.

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`POST /borrow`).
   - Update the book’s availability status.
   - Add an entry in the `BorrowingRecords` table.
2. **Frontend:**
   - Add a "Borrow" button on the book details page.
   - Show a confirmation message after borrowing.
3. **Database:**
   - Update the `Books` table and add a record in `BorrowingRecords`.

### **Testing Plan:**
- Ensure the book's status changes after borrowing.
- Verify borrowing records are stored correctly.

---

## **6. Return a book (User Story #6)**

### **User Story:**
_As a user, I want to return a book after borrowing and reading it._

### **Acceptance Criteria:**
- Returning a book updates its availability status.
- The borrowing record is marked as "returned."

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`POST /return`).
   - Update the book’s availability in the `Books` table.
   - Mark the corresponding borrowing record as "returned."
2. **Frontend:**
   - Add a "Return" button in the user's borrowing history.
3. **Database:**
   - Update the `BorrowingRecords` table.

### **Testing Plan:**
- Test the API for correct updates to availability and borrowing records.
- Verify UI reflects returned books.

---

## **7. View borrowing history (User Story #7)**

### **User Story:**
_As a user, I want to view my borrowing history so that I can keep track of books I have borrowed._

### **Acceptance Criteria:**
- The history displays details of each borrowed book (title, borrow date, return date, status).
- Users can view both active and past borrowing records.

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`GET /borrowing-history`).
   - Fetch borrowing records for the logged-in user.
2. **Frontend:**
   - Build a borrowing history page to display records.
3. **Database:**
   - Query the `BorrowingRecords` table.

### **Testing Plan:**
- Verify correct borrowing history is displayed for each user.
- Ensure UI handles scenarios with no borrowing records.

---

## **8. Notifications for due dates (User Story #8)**

### **User Story:**
_As a user, I want to receive notifications for due dates so that I can return books on time._

### **Acceptance Criteria:**
- Notifications are sent 3 days before the due date.
- Notifications are sent via email or displayed in the user's dashboard.

### **Implementation Steps:**
1. **Backend:**
   - Set up a cron job to check for due dates daily.
   - Send notifications for books due in 3 days.
2. **Frontend:**
   - Display notifications in the dashboard.
3. **Database:**
   - Query the `BorrowingRecords` table for due dates.

### **Testing Plan:**
- Verify notifications are sent for books nearing their due date.
- Test UI displays notifications correctly.

---

## **9. Admin Sign-up (User Story #9)**

### **User Story:**
_As an admin, I want to sign up for an admin account as a new administrator and get access to the admin dashboard._

### **Acceptance Criteria:**
- Admin can create a new account using a valid passcode.
- Admin receives confirmation upon successful sign-up.
- Invalid passcodes prevent account creation.

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`POST /admin/register`).
   - Validate admin passcode before creating an account.
2. **Frontend:**
   - Add a registration form for admins.
   - Display appropriate success or error messages.
3. **Database:**
   - Store admin accounts in an `Admins` table.

### **Testing Plan:**
- Test passcode validation and account creation workflows.
- Verify error handling for invalid passcodes.

---

## **10. Admin Login (User Story #10)**

### **User Story:**
_As an admin, I want to log in to the admin dashboard so that I can manage the library._

### **Acceptance Criteria:**
- Admin can log in with valid credentials.
- Successful login redirects to the admin dashboard.
- Invalid credentials display an error message.

### **Implementation Steps:**
1. **Backend:**
   - Create a login API endpoint (`POST /admin/login`).
   - Validate admin credentials and generate a session token.
2. **Frontend:**
   - Build a login form for admins.
   - Redirect successful logins to the admin dashboard.
3. **Database:**
   - Query the `Admins` table to validate credentials.

### **Testing Plan:**
- Test for valid and invalid login attempts.
- Check redirection to the admin dashboard upon successful login.

---

## **11. Add new books (User Story #11)**

### **User Story:**
_As an admin, I want to add new books to the catalog so that the library inventory is updated._

### **Acceptance Criteria:**
- Admin can successfully add a new book with required details.
- Newly added books are visible in the catalog and search results.

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`POST /books/add`).
   - Validate book details before adding them to the database.
2. **Frontend:**
   - Build a form for adding new books.
   - Display success or error messages based on the response.
3. **Database:**
   - Insert new book entries into the `Books` table.

### **Testing Plan:**
- Validate API response for correctly and incorrectly formatted book details.
- Verify new books appear in the catalog and search results.

---

## **12. Update book details (User Story #12)**

### **User Story:**
_As an admin, I want to update book details so that the catalog reflects accurate information._

### **Acceptance Criteria:**
- Admin can update any field of a book's details.
- Updated details are saved and displayed correctly in the catalog.

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`PUT /books/:id`).
   - Validate updates and save changes to the database.
2. **Frontend:**
   - Create an interface for updating book details.
3. **Database:**
   - Update the relevant entry in the `Books` table.

### **Testing Plan:**
- Test API for successful updates.
- Verify that updated details are displayed correctly in the catalog.

---

## **13. Remove books from the catalog (User Story #13)**

### **User Story:**
_As an admin, I want to remove books from the catalog so that outdated or unavailable books are not listed._

### **Acceptance Criteria:**
- Admin can remove a book by specifying its ID.
- Removed books no longer appear in search results.

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`DELETE /books/:id`).
2. **Frontend:**
   - Add a "Remove" button for each book in the catalog.
   - Confirm removal before proceeding.
3. **Database:**
   - Delete the relevant entry from the `Books` table.

### **Testing Plan:**
- Test removal functionality and confirm books no longer appear in the catalog.
- Handle error cases (e.g., trying to remove non-existent books).

---

## **14. Monitor user activity (User Story #14)**

### **User Story:**
_As an admin, I want to monitor user activity so that I can manage borrowing effectively._

### **Acceptance Criteria:**
- Admin can view a list of users and their borrowing activity.
- Admin can identify overdue books.

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`GET /admin/user-activity`).
   - Fetch user borrowing history and overdue books.
2. **Frontend:**
   - Display user activity in a dashboard format.
3. **Database:**
   - Query the `Users` and `BorrowingRecords` tables.

### **Testing Plan:**
- Verify that borrowing activity and overdue books are displayed accurately.
- Ensure error handling for empty or corrupted data.

---

## **15. Generate reports (User Story #15)**

### **User Story:**
_As an admin, I want to generate reports on borrowing statistics so that I can analyze library usage._

### **Acceptance Criteria:**
- Admin can generate reports showing most borrowed books, user engagement, and trends.
- Reports are exportable as CSV or PDF.

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`GET /admin/reports`).
   - Generate borrowing statistics and format as CSV or PDF.
2. **Frontend:**
   - Provide a "Generate Report" button.
3. **Database:**
   - Query the `BorrowingRecords` table to calculate statistics.

### **Testing Plan:**
- Test report generation for accuracy and proper formatting.
- Verify export functionality.

---

## **16. Filter search results by genre (User Story #16)**

### **User Story:**
_As a user, I want to filter search results by genre so that I can find books in specific categories._

### **Acceptance Criteria:**
- Filter options return results matching the selected genre.
- Multiple genres can be selected at once.

### **Implementation Steps:**
1. **Backend:**
   - Extend the search API to include genre filters (`GET /search?genre=<genre>`).
2. **Frontend:**
   - Add a genre filter dropdown or checkboxes to the search interface.
3. **Database:**
   - Ensure `Books` table includes a genre field.

### **Testing Plan:**
- Verify correct results are returned for selected genres.
- Test for scenarios with no matching books.

---
---

## **17. Update profile information (User Story #17)**

### **User Story:**
_As a user, I want to update my profile information so that my account details are current._

### **Acceptance Criteria:**
- Changes to the user profile are saved successfully.
- Updated details are reflected in the user's account.

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`PUT /user/profile`).
   - Validate and update user details in the database.
2. **Frontend:**
   - Provide an interface for updating profile details.
   - Display success or error messages based on the response.
3. **Database:**
   - Update the relevant user entry in the `Users` table.

### **Testing Plan:**
- Test profile updates with valid and invalid inputs.
- Verify updated details appear correctly on the profile page.

---

## **18. List of most popular books (User Story #18)**

### **User Story:**
_As a user, I want to see the list of the most popular books of the month._

### **Acceptance Criteria:**
- A list of the most popular books is displayed based on borrowing frequency.
- Users can scroll through the list.

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`GET /books/popular`).
   - Fetch the top borrowed books for the current month.
2. **Frontend:**
   - Display the list of popular books in a scrollable format.
3. **Database:**
   - Query the `BorrowingRecords` table to calculate popularity.

### **Testing Plan:**
- Verify correct books are marked as popular.
- Ensure the UI handles scenarios with no popular books.

---

## **19. Log out of account (User Story #19)**

### **User Story:**
_As a user, I want to log out of my account so that I can ensure my account security._

### **Acceptance Criteria:**
- User is logged out and their session is invalidated.
- User is redirected to the home page after logging out.

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`POST /logout`).
   - Invalidate the user's session token.
2. **Frontend:**
   - Add a "Logout" button in the navigation bar.
   - Redirect the user to the home page upon logout.

### **Testing Plan:**
- Verify session tokens are invalidated after logout.
- Check redirection to the home page.

---

## **20. Manage user accounts (User Story #20)**

### **User Story:**
_As an admin, I want to manage user accounts so that I can deactivate or reactivate accounts as needed._

### **Acceptance Criteria:**
- Admin can deactivate or reactivate user accounts.
- Changes are reflected in the user account status.

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`PUT /admin/users/:id/status`).
   - Update the user's status in the database.
2. **Frontend:**
   - Provide options to deactivate/reactivate accounts in the admin panel.
3. **Database:**
   - Update the `Users` table to include an `isActive` field.

### **Testing Plan:**
- Verify correct status changes for accounts.
- Ensure deactivated users cannot log in.

---

## **21. Recommended books (User Story #21)**

### **User Story:**
_As a user, I want to see recommended books based on my borrowing history so that I can discover new reads._

### **Acceptance Criteria:**
- Recommendations are generated based on borrowing patterns.
- Recommendations are displayed prominently on the dashboard.

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`GET /user/recommendations`).
   - Use machine learning or rule-based algorithms to generate recommendations.
2. **Frontend:**
   - Add a section on the dashboard for recommended books.
3. **Database:**
   - Query the `BorrowingRecords` table to analyze borrowing patterns.

### **Testing Plan:**
- Validate the accuracy of recommendations.
- Test the display of recommended books on the dashboard.

---

## **22. Contact administration (User Story #22)**

### **User Story:**
_As a user, I want to be able to contact the administration._

### **Acceptance Criteria:**
- Users are redirected to an email client to contact the administration.
- Contact information is prominently displayed.

### **Implementation Steps:**
1. **Frontend:**
   - Add a "Contact Us" link or button.
   - Link to the library’s contact email.
2. **Backend:**
   - No backend changes required.
3. **Testing Plan:**
- Verify the "Contact Us" link opens the user’s default email client.
- Check that the correct email address is pre-filled.

---

## **23. Reset password (User Story #23)**

### **User Story:**
_As a user, I want to be able to reset my password so that I can regain access to my account._

### **Acceptance Criteria:**
- Users are redirected to a password reset page.
- New passwords must meet complexity requirements.
- Users can log in with the updated password.

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`POST /password/reset`).
   - Send a reset link to the user’s registered email.
   - Validate and update the password upon reset.
2. **Frontend:**
   - Add a "Forgot Password" link on the login page.
   - Create a reset password page.
3. **Database:**
   - Update the `Users` table with the new hashed password.

### **Testing Plan:**
- Verify the reset link is sent to the correct email.
- Test password complexity validation.
- Ensure users can log in with the new password.

---
