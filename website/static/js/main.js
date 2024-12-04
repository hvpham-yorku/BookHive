/**
 * deleteBook - Deletes a book record from the server and updates the UI.
 *
 * This function triggers a POST request to the server to delete a book identified by its `bookId`.
 * It prevents the default behavior of the associated event, applies a visual indicator to the delete button, 
 * and reloads the page upon successful deletion. If the server request fails, an error alert is displayed.
 *
 * Workflow:
 * 1. Prevents the default form or button behavior.
 * 2. Checks if the button already has the "delete" class to avoid duplicate operations.
 * 3. Adds a "delete" class to indicate the delete process visually.
 * 4. Uses a timeout of 1.5 seconds before initiating a fetch request to the `/delete-book/${bookId}` endpoint.
 * 5. Handles server response:
 *    - If successful, reloads the page to reflect changes.
 *    - If unsuccessful, shows an error message.
 * 6. Logs any errors encountered during the fetch operation.
 */

function deleteBook(event, bookId) {
    event.preventDefault();
    const button = event.target.closest('.button');

    if (!button.classList.contains('delete')) {
        button.classList.add('delete');

       
        setTimeout(() => {
            fetch(`/delete-book/${bookId}`, {
                method: 'POST',
            })
                .then(response => {
                    if (response.ok) {
                        location.reload(); 
                    } else {
                        alert('Failed to delete the book.');
                    }
                })
                .catch(err => console.error(err));
        }, 1500);
    }
}
