(function () {
    'use strict';

    document.querySelectorAll('[data-password-controls] input[type="password"]').forEach(input => {
        const field = document.createElement('span');
        field.className = 'password-field';
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'password-toggle';
        button.setAttribute('aria-controls', input.id);
        const icon = document.createElement('i');
        icon.setAttribute('aria-hidden', 'true');
        button.appendChild(icon);
        input.parentNode.insertBefore(field, input);
        field.appendChild(input);
        field.appendChild(button);

        function setVisible(visible) {
            input.type = visible ? 'text' : 'password';
            icon.className = visible ? 'bi bi-eye-slash' : 'bi bi-eye';
            const label = visible ? 'Şifreyi gizle' : 'Şifreyi göster';
            button.setAttribute('aria-label', label);
            button.setAttribute('aria-pressed', String(visible));
            button.title = label;
        }

        setVisible(false);
        button.addEventListener('click', () => setVisible(input.type === 'password'));
        // Never restore a revealed password when returning through browser history.
        window.addEventListener('pageshow', () => setVisible(false));
        window.addEventListener('pagehide', () => setVisible(false));
        input.form.addEventListener('submit', () => setVisible(false));
    });
}());
