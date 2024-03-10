document.getElementById('add-link-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const linkData = {
        Link: document.getElementById('link').value,
        GameId: document.getElementById('gameId').value,
        Poster: document.getElementById('poster').value,
        Description: document.getElementById('description').value
    };

    fetch('/api/add_link', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(linkData),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // Refresh ho?c l�m g? �� sau khi th�m th�nh c�ng
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
const apiUrl = '/public_links';

// S?a linkId b?ng c�ch l?y gi� tr? t? n�t ��?c b?m
const linkId = $(this).data('link-id');

// G?i y�u c?u PUT �? s?a
$.ajax({
    url: `${apiUrl}`,
    type: 'PUT',
    contentType: 'application/json',
    data: JSON.stringify({ LinkId: linkId, Link: 'new_link_value', GameId: 'new_game_value', Poster: 'new_poster_value', Caption: 'new_caption_value' }),
    success: function(response) {
        console.log(response);
        // X? l? th�nh c�ng
    },
    error: function(error) {
        console.log(error);
        // X? l? l?i
    }
});

// G?i y�u c?u DELETE �? x�a
$.ajax({
    url: `${apiUrl}`,
    type: 'DELETE',
    contentType: 'application/json',
    data: JSON.stringify({ LinkId: linkId }),
    success: function(response) {
        console.log(response);
        // X? l? th�nh c�ng
    },
    error: function(error) {
        console.log(error);
        // X? l? l?i
    }
});

// G?i y�u c?u POST �? chia s?
$.ajax({
    url: `${apiUrl}`,
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({ LinkId: linkId }),
    success: function(response) {
        console.log(response);
        // X? l? th�nh c�ng
    },
    error: function(error) {
        console.log(error);
        // X? l? l?i
    }
});

    // B?t �?u l?ng nghe s? ki?n click n�t Delete cho danh s�ch ng�?i chi?n th?ng
    $('.delete-winner').on('click', function() {
        var winnerId = $(this).data('winner-id');
        // G?i y�u c?u DELETE �?n endpoint manage_winner
        $.ajax({
            type: 'DELETE',
            url: '/winners/' + winnerId,
            success: function(response) {
                alert(response.message); // Hi?n th? th�ng b�o
                // Reload trang sau khi x�a �? c?p nh?t danh s�ch
                location.reload();
            },
            error: function(error) {
                alert('Failed to delete winner.'); // Hi?n th? th�ng b�o l?i n?u c�
            }
        });
    });

    // Th�m s? ki?n click cho n�t Copy trong danh s�ch ng�?i chi?n th?ng
    $('.copy-winner').on('click', function() {
        var winnerId = $(this).data('winner-id');
        // Th?c hi?n c�ng vi?c sao ch�p ? ��y (c� th? s? d?ng Clipboard API)
        // V� d?: navigator.clipboard.writeText(winnerText);
        alert('Winner copied successfully!');
    });

// �?i v?i th�m m?i Winner
document.getElementById('add-winner-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const winnerData = {
        IdPlayer: document.getElementById('idPlayer').value,
        GiftId: document.getElementById('giftId').value,
        Amount: document.getElementById('amount').value,
        State: document.getElementById('state').value
    };

    fetch('/api/add_winner', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(winnerData),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // Refresh ho?c l�m g? �� sau khi th�m th�nh c�ng
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
// Backbone Model
var Link = Backbone.Model.extend({
    defaults: {
        link: '',
        gameId: '',
        poster: '',
        description: ''
    }
});

var Winner = Backbone.Model.extend({
    defaults: {
        idWin: '',
        playerId: '',
        gameId: '',
        prizeId: '',
        quantity: '',
        status: ''
    }
});

// Backbone Collection
var LinksList = Backbone.Collection.extend({
    model: Link
});

var WinnersList = Backbone.Collection.extend({
    model: Winner
});

// Backbone Views
var LinksListView = Backbone.View.extend({
    el: '.links-list',
    initialize: function () {
        this.collection = new LinksList();
        this.render();

        // Add event listeners
        this.listenTo(this.collection, 'add', this.renderLink);
    },
    events: {
        'click .add-link': 'addLink'
    },
    render: function () {
        // Render existing links
        this.collection.each(function (link) {
            this.renderLink(link);
        }, this);
    },
    renderLink: function (link) {
        var linkTemplate = _.template($('.links-list-template').html());
        this.$el.append(linkTemplate(link.toJSON()));
    },
    addLink: function () {
        var newLink = new Link({
            link: this.$('.link-input').val(),
            gameId: this.$('.gameId-input').val(),
            poster: this.$('.poster-input').val(),
            description: this.$('.description-input').val()
        });
        this.collection.add(newLink);
        // Clear input fields
        this.$('.link-input, .gameId-input, .poster-input, .description-input').val('');
    }
});

var WinnersListView = Backbone.View.extend({
    el: '.winners-list',
    initialize: function () {
        this.collection = new WinnersList();
        this.render();

        // Add event listeners
        this.listenTo(this.collection, 'add', this.renderWinner);
    },
    events: {
        'click .add-winner': 'addWinner'
    },
    render: function () {
        // Render existing winners
        this.collection.each(function (winner) {
            this.renderWinner(winner);
        }, this);
    },
    renderWinner: function (winner) {
        var winnerTemplate = _.template($('.winners-list-template').html());
        this.$el.append(winnerTemplate(winner.toJSON()));
    },
    addWinner: function () {
        var newWinner = new Winner({
            idWin: this.$('.idWin-input').val(),
            playerId: this.$('.playerId-input').val(),
            gameId: this.$('.gameId-input').val(),
            prizeId: this.$('.prizeId-input').val(),
            quantity: this.$('.quantity-input').val(),
            status: this.$('.status-input').val()
        });
        this.collection.add(newWinner);
        // Clear input fields
        this.$('.idWin-input, .playerId-input, .gameId-input, .prizeId-input, .quantity-input, .status-input').val('');
    }
});

// Instantiate Views
var linksListView = new LinksListView();
var winnersListView = new WinnersListView();
