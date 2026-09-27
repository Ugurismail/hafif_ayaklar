/* Navbar counters must initialize even when the page has no search form. */
document.addEventListener('DOMContentLoaded', function () {
    if (!document.getElementById('notification-badge') && !document.getElementById('message-badge')) return;
    let inFlight = false;
    let lastStarted = 0;

    function updateBadge(id, count) {
        const badge = document.getElementById(id);
        const value = Number(count);
        if (!badge || !Number.isFinite(value) || value < 0) return;
        badge.textContent = value > 99 ? '99+' : String(value);
        badge.style.display = value > 0 ? 'inline-block' : 'none';
    }

    async function refresh() {
        if (document.hidden || inFlight || Date.now() - lastStarted < 1000) return;
        inFlight = true;
        lastStarted = Date.now();
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 10000);
        try {
            const response = await fetch('/navbar/status/', {
                cache: 'no-store',
                signal: controller.signal,
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
            });
            if (!response.ok || !(response.headers.get('content-type') || '').includes('application/json')) return;
            const data = await response.json();
            updateBadge('notification-badge', data.notification_count);
            updateBadge('message-badge', data.message_count);
            if (typeof window.hafifAyaklarSetOnlineChatUnreadCount === 'function') {
                window.hafifAyaklarSetOnlineChatUnreadCount(data.online_chat_count);
            }
        } catch (error) {
            // Keep the server-rendered count on network failures and retry later.
        } finally {
            clearTimeout(timeout);
            inFlight = false;
        }
    }

    refresh();
    setInterval(refresh, 15000);
    document.addEventListener('visibilitychange', refresh);
    window.addEventListener('focus', refresh);
    window.addEventListener('pageshow', refresh);
});
