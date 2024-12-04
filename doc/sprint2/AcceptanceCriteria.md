# Sprint 2 User Stories Breakdown

This document provides a breakdown of the user stories assigned for Sprint 2, including **acceptance criteria**, **implementation steps**, and **testing plan**.

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
- Search results display all books matching the title input.
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
3. **Database:**
   - Query the `Books` table to match titles.

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
## **8. Receive returned book confirmations (User Story #8)**

### **User Story:**
_As a user, I want to receive returned book confirmations so I know I successfully returned a book._

### **Acceptance Criteria:**
- Users receive a confirmation notification in their "Messages" tab upon returning a book.
- Users receive a confirmation email with return details.
- The notification includes the book title, return date, and a thank-you message.

### **Implementation Steps:**
1. **Backend:**
   - Update the return book API (`POST /return`) to generate a confirmation message.
   - Send an email confirmation with the return details (book title and return date).
   - Create a record in the `UserMessages` table for the notification.
2. **Frontend:**
   - Display the confirmation message in the "Messages" tab after the return process.
   - Provide visual feedback (e.g., a success message) after returning the book.
3. **Database:**
   - Add a new entry in the `UserMessages` table for each confirmation.

### **Testing Plan:**
- Verify the API correctly generates confirmation notifications and emails.
- Test that returned books are listed correctly in the borrowing history as returned.
- Check that the confirmation appears in the user's "Messages" tab and email inbox.

---

## **9. Admin sign-up (User Story #9)**

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
## **10. Admin login (User Story #10)**

### **User Story:**
_As an admin, I want to log in to the admin dashboard so that I can manage the library._

### **Acceptance Criteria:**
- Admin can successfully log in using valid credentials.
- Admin is redirected to the admin dashboard upon successful login.
- Invalid credentials display an appropriate error message.
- Admin dashboard includes management features (e.g., book management, user monitoring).

### **Implementation Steps:**
1. **Backend:**
   - Create a login API endpoint for admins (`POST /admin/login`).
   - Validate admin credentials using the `Admins` table.
   - Generate a session token upon successful login.
2. **Frontend:**
   - Build a login form specifically for admins.
   - Redirect to the admin dashboard after successful login.
   - Display error messages for invalid credentials.
3. **Database:**
   - Query the `Admins` table for valid credentials.

### **Testing Plan:**
- Test for valid and invalid login attempts.
- Verify redirection to the admin dashboard upon success.
- Ensure error handling works for invalid credentials.

---

## **11. Add new books to the catalog (User Story #11)**

### **User Story:**
_As an admin, I want to add new books to the catalog so that the library inventory is updated._

### **Acceptance Criteria:**
- Admin can add a new book with required details (title, author, genre, total copies).
- The new book is saved in the database and visible in the catalog and search results.
- Admin receives a confirmation message upon successful addition.

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`POST /admin/add-book`).
   - Validate input fields (e.g., non-empty title and author).
   - Save the new book to the `Books` table in the database.
2. **Frontend:**
   - Build a form for adding new books, including fields for title, author, genre, and total copies.
   - Display a confirmation message upon success or an error message for invalid inputs.
3. **Database:**
   - Insert the new book into the `Books` table with relevant details.

### **Testing Plan:**
- Test API functionality for valid and invalid inputs.
- Verify the new book appears in the catalog and search results.
- Confirm the admin receives a success message after adding a book.

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
- Test API for successful updates.
- Verify that updated details are displayed correctly in the catalog.

---

## **13. Remove books from the catalog (User Story #13)**

### **User Story:**
_As an admin, I want to remove books from the catalog so that outdated or unavailable books are not listed._

### **Acceptance Criteria:**
- Admin can remove a book by specifying its ID.
- Removed books are deleted from the database.
- The removed book no longer appears in the catalog or search results.
- Admin receives a confirmation message upon successful removal.

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`DELETE /admin/remove-book/:id`).
   - Validate the book ID to ensure it exists before attempting to remove it.
   - Delete the book from the `Books` table in the database.
2. **Frontend:**
   - Add a "Remove" button for each book in the catalog (accessible only to admins).
   - Confirm the removal action with a modal or alert box before proceeding.
   - Display a success or error message based on the response from the API.
3. **Database:**
   - Ensure the book is removed from the `Books` table and any associated borrowing records are updated or removed as needed.

### **Testing Plan:**
- Test the API with valid and invalid book IDs to confirm proper handling of both cases.
- Verify that removed books are no longer displayed in the catalog or search results.
- Check that the admin receives a confirmation message upon successful removal.
- Ensure the UI correctly handles errors (e.g., attempting to remove a non-existent book).

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
- Reports provide insights into most borrowed books, user engagement, and trends.
- Reports are exportable as CSV or PDF.

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`GET /admin/reports`).
   - Generate borrowing statistics and format them as CSV or PDF.
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
- Users can select a genre from a dropdown or list of options.
- Search results display only books that match the selected genre.
- If no books match the selected genre, the system displays a "No results found" message.

### **Implementation Steps:**
1. **Backend:**
   - Update the search API (`GET /search?genre=<genre>`) to include genre filters.
   - Query the `Books` table to fetch books matching the selected genre.
   - Return a list of books or an empty result if no matches are found.
2. **Frontend:**
   - Add a genre filter dropdown or checkbox group to the search interface.
   - Dynamically update the search results based on the selected genre.
   - Display a "No results found" message if the filter returns no matches.
3. **Database:**
   - Ensure the `Books` table includes a `genre` field that can be queried.

### **Testing Plan:**
- Verify the API returns correct results for valid genre inputs.
- Test UI functionality for filtering search results by genre.
- Check edge cases:
  - No books matching the genre.
  - Invalid or empty genre selection.
- Ensure the "No results found" message is displayed appropriately.
  
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
- Users can log out by clicking a "Logout" button in the navigation bar.
- Upon logout, the user's session is invalidated.
- The user is redirected to the home page after logging out.
- A confirmation message is displayed indicating the user has been logged out successfully.

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`POST /logout`).
   - Invalidate the user's session by clearing the session token or cookies.
   - Redirect the user to the home page.
2. **Frontend:**
   - Add a "Logout" button in the navigation bar, visible only to logged-in users.
   - On button click, call the logout API and handle the response.
   - Display a confirmation message upon successful logout.
3. **Database:**
   - If using token-based authentication, remove or invalidate the token from the database or cache.

### **Testing Plan:**
- Test the API to ensure session invalidation and redirection work correctly.
- Verify the "Logout" button is functional and redirects to the home page.
- Confirm users cannot access authenticated pages after logging out.
- Check the confirmation message is displayed after a successful logout.

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
- Recommendations are generated based on previous borrowing patterns.
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
- Users can access a "Contact Us" button or link on the website.
- Clicking the "Contact Us" button redirects users to their default email client.
- The email address of the administration is pre-filled in the email client.

### **Implementation Steps:**
1. **Frontend:**
   - Add a "Contact Us" button or link to the navigation bar or footer.
   - Use a `mailto:` link with the administration's email address (e.g., `mailto:admin@library.com`).
2. **Backend:**
   - No backend implementation is required for this feature.
3. **Database:**
   - No database updates are required.

### **Testing Plan:**
- Verify the "Contact Us" button opens the user's default email client.
- Ensure the email client pre-fills the administration's email address.
- Test across different devices and browsers to confirm compatibility.

---

## **23. Reset password (User Story #23)**

### **User Story:**
_As a user, I want to be able to reset my password so that I can regain access to my account._

### **Acceptance Criteria:**
- Users can access a "Forgot Password" link on the login page.
- Clicking the link redirects users to a password reset page.
- Users receive a reset link via email after providing their registered email address.
- Users can log in with the updated password after resetting.

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`POST /password/reset`) to send a reset link to the user's email.
   - Validate the email address and generate a reset token.
   - Create another API endpoint (`POST /password/update`) to update the password.
2. **Frontend:**
   - Add a "Forgot Password" link on the login page.
   - Build a password reset page where users can enter their new password.
   - Display success or error messages during the process.
3. **Database:**
   - Add a `reset_token` and `token_expiry` field to the `Users` table for token-based password resets.

### **Testing Plan:**
- Verify the reset link is sent to the correct email address.
- Ensure the reset token expires after the specified time (e.g., 24 hours).
- Test the password reset process for valid and invalid tokens.
- Confirm users can log in with the new password after resetting.

---

## **24. View borrowed books (User Story #24)**

### **User Story:**
_As a user, I want to view my borrowed books so that I can track what I have borrowed._

### **Acceptance Criteria:**
- Users can access a "My Borrowed Books" section from their dashboard or navigation menu.
- The section displays a list of books the user has borrowed, including:
  - Title, author, borrow date, and due date.
  - Status (e.g., returned or overdue).
- Users can see books they have returned in their history.

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`GET /user/borrowed-books`) to fetch the user's borrowed books.
   - Query the `BorrowedBooks` table for active and past borrow records.
2. **Frontend:**
   - Add a "My Borrowed Books" section in the dashboard or a dedicated page.
   - Display a list of borrowed books with their details and status.
3. **Database:**
   - Query the `BorrowedBooks` table and join it with the `Books` table for detailed information.

### **Testing Plan:**
- Verify the API returns accurate borrowing records for the logged-in user.
- Ensure the frontend displays both active and past borrowed books correctly.
- Test scenarios for users with no borrowing records and ensure appropriate messaging.

---

## **25. Rate borrowed books (User Story #25)**

### **User Story:**
_As a user, I want to be able to rate my borrowed books so that other readers can benefit from it._

### **Acceptance Criteria:**
- Users can rate books they have borrowed using a 5-star system.
- Users can optionally add a written review along with their rating.
- Ratings and reviews are visible to other users on the book details page.

### **Implementation Steps:**
1. **Backend:**
   - Create an API endpoint (`POST /books/:id/rate`) to submit a rating and review.
   - Validate that the user has borrowed the book before allowing them to rate it.
   - Save ratings and reviews in a new `Ratings` table.
2. **Frontend:**
   - Add a rating system (e.g., 5-star widget) and a review input field on the "My Borrowed Books" page.
   - Display existing ratings and reviews on the book details page.
3. **Database:**
   - Create a `Ratings` table with fields for user ID, book ID, rating, and review text.

### **Testing Plan:**
- Verify that only users who have borrowed a book can submit ratings or reviews.
- Test the API for valid and invalid inputs (e.g., missing rating or review).
- Ensure ratings and reviews are displayed correctly on the book details page.
- Validate average ratings are calculated and updated accurately.

---


## **26. Book ratings (User Story #26)**

### **User Story:**
_As a user, I want to see book ratings before I borrow a book, so I can know what other readers think of it._

### **Acceptance Criteria:**
- Book details page displays the average rating and individual reviews.

### **Implementation Steps:**
1. **Backend:**
   - Extend the book details API (`GET /books/:id`) to include ratings.
2. **Frontend:**
   - Display the average rating on the book details page.
3. **Database:**
   - Query the `Ratings` table for average and individual ratings.

### **Testing Plan:**
- Verify correct display of ratings and reviews.
- Test edge cases, such as books with no ratings.

---

## **27. Email verification codes upon login (User Story #27)**

### **User Story:**
_As a user, I want to receive verification codes to my email each time I log in to enhance account security._

### **Acceptance Criteria:**
- Users receive a verification code to their registered email after entering valid login credentials.
- Users must enter the verification code to complete the login process.
- Verification codes expire after a specified time (e.g., 5 minutes).
- Invalid or expired codes prevent login.
- Users are notified if the verification code is incorrect or expired.

### **Implementation Steps:**
1. **Backend:**
   - Extend the login API to send a one-time verification code to the user's registered email.
   - Create an API endpoint (`POST /verify-code`) to validate the verification code.
   - Implement logic for code expiration and retry limits.
2. **Frontend:**
   - Modify the login flow to include a step for entering the verification code after submitting credentials.
   - Display success or error messages based on the verification response.
3. **Database:**
   - Add fields for `verification_code` and `code_expiry` in the `Users` table to store the one-time code and expiration time.

### **Testing Plan:**
- Verify that a verification code is sent to the correct email address upon login.
- Test the validation of verification codes, including handling of:
  - Correct codes within the expiration period.
  - Incorrect codes.
  - Expired codes.
- Check for appropriate error messages and user feedback during the process.
- Test edge cases, such as users entering the wrong code multiple times or attempting login after the code expires.
