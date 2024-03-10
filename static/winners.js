// winner.js

$(document).ready(function() {
    $('.add-winner').on('click', function() {
        // Get data from input fields
        var playerId = $('#playerId').val();
        var giftId = $('#giftId').val();
        var amount = $('#amount').val();
        var state = $('#state').val();

        // Create an object to hold the data
        var winnerData = {
            playerId: playerId,
            giftId: giftId,
            amount: amount,
            state: state
        };

        // Perform AJAX request to add winner
        $.ajax({
            url: '/add_winner',  // Update this URL to match your server route
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(winnerData),
            success: function(response) {
                // Handle success response from the server
                alert('Winner added successfully!');
            },
            error: function(error) {
                // Handle error response from the server
                alert('Error adding winner.');
                console.error(error);
            }
        });
    });
});
