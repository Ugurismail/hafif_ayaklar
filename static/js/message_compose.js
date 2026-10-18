(function () {
    'use strict';

    const form = document.querySelector('.message-compose');
    if (!form) return;
    const input = form.querySelector('textarea[name="body"]');
    const button = form.querySelector('button[type="submit"]');
    if (!input || !button) return;
    let sending = false;

    input.addEventListener('keydown', function (event) {
        if (event.key !== 'Enter' || event.shiftKey || event.ctrlKey || event.altKey
                || event.metaKey || event.isComposing || event.keyCode === 229
                || event.defaultPrevented) return;
        event.preventDefault();
        if (!event.repeat && !sending) form.requestSubmit(button);
    });

    input.addEventListener('input', function () {
        input.setCustomValidity('');
    });

    form.addEventListener('submit', function (event) {
        if (event.defaultPrevented) return;
        if (sending || !input.value.trim()) {
            event.preventDefault();
            if (!sending) {
                input.setCustomValidity('Lütfen bir mesaj yazın.');
                input.reportValidity();
            }
            return;
        }
        sending = true;
        button.disabled = true;
        form.setAttribute('aria-busy', 'true');
    });

    // Restore controls when the browser brings this page back from its cache.
    window.addEventListener('pageshow', function () {
        sending = false;
        button.disabled = false;
        form.removeAttribute('aria-busy');
    });
}());
