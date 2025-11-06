// static/js/message_notifications.js

document.addEventListener('DOMContentLoaded', function() {
    function checkNewMessages() {
        fetch('/check_new_messages/', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
        })
        .then(response => response.json())
        .then(data => {
            const messageBadge = document.getElementById('message-badge');
            if (messageBadge) {
                if (data.unread_count > 0) {
                    messageBadge.textContent = data.unread_count;
                    messageBadge.style.display = 'inline-block';
                } else {
                    messageBadge.style.display = 'none';
                }
            }
        })
        .catch(error => console.error('Mesaj sayısı güncellenemedi:', error));
    }

    // İlk yüklemede kontrol et
    checkNewMessages();

    // Her 60 saniyede bir yeni mesajları kontrol et (performans için)
    setInterval(checkNewMessages, 60000);
});
