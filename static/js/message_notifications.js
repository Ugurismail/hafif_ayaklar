// static/js/message_notifications.js

document.addEventListener('DOMContentLoaded', function() {
    let requestInFlight = false;

    function checkNewMessages() {
        if (document.hidden || requestInFlight) {
            return;
        }
        requestInFlight = true;
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
        .catch(error => console.error('Mesaj sayısı güncellenemedi:', error))
        .finally(() => {
            requestInFlight = false;
        });
    }

    // İlk değer sunucudan geliyor; sayfa açılışında ikinci bir istek atma.
    setTimeout(checkNewMessages, 15000);

    // Her 60 saniyede bir yeni mesajları kontrol et (performans için)
    setInterval(checkNewMessages, 60000);
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) {
            checkNewMessages();
        }
    });
});
