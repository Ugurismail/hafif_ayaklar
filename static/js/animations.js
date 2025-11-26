/**
 * Animation enhancements and micro-interactions
 * Modern UX improvements
 */

document.addEventListener('DOMContentLoaded', function() {

    // ========== NAVBAR SCROLL EFFECT ==========
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        let lastScroll = 0;

        window.addEventListener('scroll', function() {
            const currentScroll = window.pageYOffset;

            if (currentScroll > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }

            lastScroll = currentScroll;
        });
    }

    // ========== SMOOTH REVEAL ON SCROLL ==========
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal');
                // Stop observing after reveal
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe cards and answers
    document.querySelectorAll('.card, .answer').forEach(el => {
        observer.observe(el);
    });

    // ========== RIPPLE EFFECT FOR BUTTONS ==========
    function createRipple(event) {
        const button = event.currentTarget;

        const circle = document.createElement('span');
        const diameter = Math.max(button.clientWidth, button.clientHeight);
        const radius = diameter / 2;

        circle.style.width = circle.style.height = `${diameter}px`;
        circle.style.left = `${event.clientX - button.offsetLeft - radius}px`;
        circle.style.top = `${event.clientY - button.offsetTop - radius}px`;
        circle.classList.add('ripple');

        const ripple = button.getElementsByClassName('ripple')[0];

        if (ripple) {
            ripple.remove();
        }

        button.appendChild(circle);
    }

    // Apply ripple to buttons
    const buttons = document.querySelectorAll('.btn-primary, .btn-secondary');
    buttons.forEach(button => {
        button.addEventListener('click', createRipple);
    });

    // ========== TOAST NOTIFICATIONS AUTO-DISMISS ==========
    // Toasts are now manually triggered, not auto-shown
    // Initialize toasts but don't auto-show them
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        // Just initialize, don't show automatically
        new bootstrap.Toast(toast, {
            autohide: true,
            delay: 5000
        });
    });

    // ========== LOADING INDICATOR FOR AJAX ==========
    let loadingIndicator = null;

    window.showLoading = function() {
        if (!loadingIndicator) {
            loadingIndicator = document.createElement('div');
            loadingIndicator.className = 'loading-overlay';
            loadingIndicator.innerHTML = '<div class="loading-spinner"></div>';
            document.body.appendChild(loadingIndicator);
        }
        loadingIndicator.style.display = 'flex';
    };

    window.hideLoading = function() {
        if (loadingIndicator) {
            loadingIndicator.style.display = 'none';
        }
    };

    // ========== ENHANCE FORM INTERACTIONS ==========
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Gönderiliyor...';

                // Re-enable after 3 seconds as fallback
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = submitBtn.dataset.originalText || 'Gönder';
                }, 3000);
            }
        });
    });

    // Store original button text
    document.querySelectorAll('button[type="submit"]').forEach(btn => {
        btn.dataset.originalText = btn.innerHTML;
    });

    // ========== TOOLTIP INITIALIZATION ==========
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            trigger: 'hover',
            delay: { show: 500, hide: 100 }
        });
    });

    // ========== POPOVER INITIALIZATION ==========
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // ========== COPY TO CLIPBOARD FEEDBACK ==========
    document.querySelectorAll('[data-clipboard]').forEach(btn => {
        btn.addEventListener('click', function() {
            const text = this.dataset.clipboard;
            navigator.clipboard.writeText(text).then(() => {
                // Show success feedback
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="bi bi-check"></i> Kopyalandı!';
                this.classList.add('btn-success');

                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.classList.remove('btn-success');
                }, 2000);
            });
        });
    });

    // ========== ANIMATE NUMBERS ==========
    function animateNumber(element, start, end, duration) {
        const range = end - start;
        const increment = range / (duration / 16); // 60fps
        let current = start;

        const timer = setInterval(() => {
            current += increment;
            if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
                current = end;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current);
        }, 16);
    }

    // Animate vote counts on page load
    document.querySelectorAll('.icon-number').forEach(el => {
        const finalValue = parseInt(el.textContent) || 0;
        if (finalValue > 0) {
            animateNumber(el, 0, finalValue, 1000);
        }
    });

    // ========== KEYBOARD SHORTCUTS ==========
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K to focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('#search-input');
            if (searchInput) {
                searchInput.focus();
            }
        }

        // Escape to close modals
        if (e.key === 'Escape') {
            const openModals = document.querySelectorAll('.modal.show');
            openModals.forEach(modal => {
                bootstrap.Modal.getInstance(modal)?.hide();
            });
        }
    });

    // ========== LAZY LOAD IMAGES ==========
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        imageObserver.unobserve(img);
                    }
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // ========== AUTO-RESIZE TEXTAREAS ==========
    document.querySelectorAll('textarea.auto-resize').forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    });

    // ========== PREVENT DOUBLE SUBMIT ==========
    let formSubmitted = false;
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (formSubmitted) {
                e.preventDefault();
                return false;
            }
            formSubmitted = true;

            // Reset after 3 seconds
            setTimeout(() => {
                formSubmitted = false;
            }, 3000);
        });
    });

    // ========== ADD CSS FOR LOADING OVERLAY ==========
    if (!document.querySelector('#loading-styles')) {
        const style = document.createElement('style');
        style.id = 'loading-styles';
        style.textContent = `
            .loading-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.5);
                display: none;
                align-items: center;
                justify-content: center;
                z-index: 9999;
            }

            .ripple {
                position: absolute;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.6);
                transform: scale(0);
                animation: ripple-animation 0.6s ease-out;
                pointer-events: none;
            }

            @keyframes ripple-animation {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }

            .reveal {
                opacity: 1;
                transform: translateY(0);
            }
        `;
        document.head.appendChild(style);
    }

    // ========== CLICKABLE ANSWER CARDS ==========
    // Make answer cards clickable (go to single answer page)
    // But don't trigger when clicking on interactive elements
    document.querySelectorAll('.answer.random-item-card').forEach(card => {
        card.style.cursor = 'pointer';

        card.addEventListener('click', function(e) {
            // Don't navigate if clicking on interactive elements
            const clickedElement = e.target;
            const isInteractive = clickedElement.closest('a, button, input, textarea, select, .vote-btn, .save-btn, .dropdown, .read-more, .bi-pencil-square, .bi-trash, i');

            if (isInteractive) {
                return; // Let the interactive element handle the click
            }

            // Get the single answer URL from the copy-link button
            const copyLinkBtn = this.querySelector('.copy-link-btn');

            if (copyLinkBtn) {
                const singleAnswerUrl = copyLinkBtn.dataset.url;

                if (singleAnswerUrl) {
                    window.location.href = singleAnswerUrl;
                }
            }
        });
    });
});

// ========== EXPORT UTILITIES ==========
window.AnimationUtils = {
    showLoading: function() {
        window.showLoading();
    },
    hideLoading: function() {
        window.hideLoading();
    }
};
