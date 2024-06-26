window.addEventListener('load', function() {
    document.getElementById('loading').style.display = 'none';
    document.body.classList.add('loaded');
});

document.addEventListener('DOMContentLoaded', function() {
    const updateButton = document.querySelector('.button-update');
    if (updateButton) {
        updateButton.addEventListener('click', function(event) {
            event.preventDefault();
            const host = document.querySelector('input[name="host"]').value;
            if (!host) {
                showNotification("No host selected", "error");
                return;
            }
            
            document.getElementById('loading').style.display = 'block';

            fetch('/update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({ host: host }),
            })
            .then(response => {
                document.getElementById('loading').style.display = 'none';
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.error || 'Network response was not ok');
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    showNotification(data.error, "error");
                } else {
                    showNotification("Update successful", "success");
                    setTimeout(() => {
                        location.reload();
                    }, 1000); // Reload the page to get updated data
                }
            })
            .catch(error => {
                showNotification("Error fetching data: " + error.message, "error");
            });
        });
    }
});

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerText = message;
    document.body.appendChild(notification);
    setTimeout(() => {
        notification.style.display = 'none';
        notification.remove();
    }, 3000);
}

function showPopup(message) {
    showNotification(message, "error");
}
