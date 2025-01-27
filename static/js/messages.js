console.log('messages.js file loaded');

function closeMessage() {
    console.log('closeMessage function called');
    document.querySelector('.messages').style.display = 'none';
}

function fetchNotifications() {
    console.log('fetchNotifications function called at', new Date().toLocaleTimeString());
    fetch('/get_notifications/')
        .then(response => {
            console.log('Response received:', response);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Data received:', data);
            if (data.status === 'success') {
                console.log('Notifications fetched successfully at', new Date().toLocaleTimeString());
                if (data.notifications.length > 0) {
                    const messagesDiv = document.querySelector('.messages');
                    data.notifications.forEach(notification => {
                        const notificationItem = document.createElement('div');
                        notificationItem.className = `alert ${notification.tags}`;
                        notificationItem.innerHTML = `
                            ${notification.message}
                            <span class="close-btn" onclick="closeMessage()">×</span>
                        `;
                        messagesDiv.appendChild(notificationItem);
                    });
                }
            }
        })
        .catch(error => console.error('Error fetching notifications:', error));
}

// Poll for new notifications every 10 seconds
// setInterval(fetchNotifications, 10000);

// Fetch notifications on page load
fetchNotifications();