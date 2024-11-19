function deleteBook(event, bookId) {
    event.preventDefault(); // Prevent default form submission
    const button = event.target.closest('.button');

    if (!button.classList.contains('delete')) {
        button.classList.add('delete');

        // Perform deletion after animation
        setTimeout(() => {
            fetch(`/delete-book/${bookId}`, {
                method: 'POST',
            })
                .then(response => {
                    if (response.ok) {
                        location.reload(); // Reload page to update book list
                    } else {
                        alert('Failed to delete the book.');
                    }
                })
                .catch(err => console.error(err));
        }, 1500);
    }
}
