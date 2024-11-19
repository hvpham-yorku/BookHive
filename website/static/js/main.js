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
