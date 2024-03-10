document.addEventListener('DOMContentLoaded', function () {
    // Edit link
    document.querySelectorAll('.edit-link').forEach(function (editBtn) {
        editBtn.addEventListener('click', function () {
            var linkId = this.getAttribute('data-link-id');
            editLink(linkId);
        });
    });

    // Delete link
    document.querySelectorAll('.delete-link').forEach(function (deleteBtn) {
        deleteBtn.addEventListener('click', function () {
            var linkId = this.getAttribute('data-link-id');
            deleteLink(linkId);
        });
    });

    // Share link
    document.querySelectorAll('.share-link').forEach(function (shareBtn) {
        shareBtn.addEventListener('click', function () {
            var linkId = this.getAttribute('data-link-id');
            shareLink(linkId);
        });
    });
});

function editLink(linkId) {
    // Implement the logic to handle editing a link with the specified linkId
    // You may use fetch or another method to send a PUT request to your Flask API
    fetch(`/api/public_links/${linkId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            // Provide the updated data here
            Link: 'new_link_value',
            GameId: 'new_game_value',
            Poster: 'new_poster_value',
            Caption: 'new_caption_value',
        }),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // Handle success, e.g., update the UI
        })
        .catch(error => {
            console.error('Error:', error);
            // Handle error
        });
}

function deleteLink(linkId) {
    // Implement the logic to handle deleting a link with the specified linkId
    // You may use fetch or another method to send a DELETE request to your Flask API
    fetch(`/api/public_links/${linkId}`, {
        method: 'DELETE',
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // Handle success, e.g., update the UI
        })
        .catch(error => {
            console.error('Error:', error);
            // Handle error
        });
}

function shareLink(linkId) {
    // Implement the logic to handle sharing a link with the specified linkId
    // You may use fetch or another method to send a POST request to your Flask API
    fetch(`/api/public_links/share/${linkId}`, {
        method: 'POST',
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', linkId);
            // Handle success, e.g., update the UI
        })
        .catch(error => {
            console.error('Error:', error);
            // Handle error
        });
}
