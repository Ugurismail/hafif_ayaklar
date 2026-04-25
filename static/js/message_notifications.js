// static/js/message_notifications.js

document.addEventListener('DOMContentLoaded', function() {
    const messageBadge = document.getElementById('message-badge');
    if (!messageBadge) {
        return;
    }

    function canPoll() {
        return !document.hidden && navigator.onLine !== false;
    }

    function checkNewMessages() {
        if (!canPoll()) {
            return;
        }
        fetch('/check_new_messages/', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
        })
        .then(response => {
            const contentType = response.headers.get('content-type') || '';
            if (!response.ok || !contentType.includes('application/json')) {
                return null;
            }
            return response.json();
        })
        .then(data => {
            if (!data) {
                return;
            }
            if (data.unread_count > 0) {
                messageBadge.textContent = data.unread_count;
                messageBadge.style.display = 'inline-block';
            } else {
                messageBadge.style.display = 'none';
            }
        })
        .catch(() => {
            // Network interruptions should not spam the console on mobile/local reloads.
        });
    }

    // İlk yüklemede kontrol et
    checkNewMessages();

    // Her 60 saniyede bir yeni mesajları kontrol et (performans için)
    setInterval(checkNewMessages, 60000);

    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) {
            checkNewMessages();
        }
    });
});
