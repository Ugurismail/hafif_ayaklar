/**
 * Core JavaScript utilities
 * Shared helpers to reduce code duplication
 */

/**
 * Get CSRF token from cookies
 * @param {string} name - Cookie name (default: 'csrftoken')
 * @returns {string|null} Cookie value or null
 */
export function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * API Client for making AJAX requests with CSRF protection
 */
export class APIClient {
    /**
     * Get CSRF token for requests
     * @returns {string} CSRF token
     */
    static getCsrfToken() {
        return getCookie('csrftoken');
    }

    /**
     * Make a POST request
     * @param {string} url - API endpoint
     * @param {FormData|Object} data - Data to send
     * @param {boolean} isJson - Whether to send as JSON (default: false)
     * @returns {Promise<any>} Parsed JSON response
     */
    static async post(url, data, isJson = false) {
        const options = {
            method: 'POST',
            headers: {
                'X-CSRFToken': this.getCsrfToken(),
                'X-Requested-With': 'XMLHttpRequest'
            }
        };

        if (isJson) {
            options.headers['Content-Type'] = 'application/json';
            options.body = JSON.stringify(data);
        } else {
            // FormData or URLSearchParams
            options.body = data;
        }

        const response = await fetch(url, options);

        if (!response.ok) {
            const text = await response.text();
            throw new Error(text || `HTTP error! status: ${response.status}`);
        }

        return response.json();
    }

    /**
     * Make a GET request
     * @param {string} url - API endpoint
     * @param {Object} params - Query parameters
     * @returns {Promise<any>} Parsed JSON response
     */
    static async get(url, params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const fullUrl = queryString ? `${url}?${queryString}` : url;

        const response = await fetch(fullUrl, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return response.json();
    }

    /**
     * Make a DELETE request
     * @param {string} url - API endpoint
     * @returns {Promise<any>} Parsed JSON response
     */
    static async delete(url) {
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': this.getCsrfToken(),
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return response.json();
    }
}

/**
 * Pagination Helper for consistent pagination UI
 */
export class PaginationHelper {
    /**
     * Create pagination controls
     * @param {HTMLElement} container - Container element for pagination
     * @param {number} currentPage - Current page number
     * @param {number} totalPages - Total number of pages
     * @param {Function} onPageChange - Callback when page changes
     */
    static createPagination(container, currentPage, totalPages, onPageChange) {
        container.innerHTML = '';

        if (totalPages <= 1) return;

        // Previous button
        if (currentPage > 1) {
            const prevBtn = this.createButton('Önceki', () => onPageChange(currentPage - 1));
            container.appendChild(prevBtn);
        }

        // Page info
        const pageInfo = document.createElement('span');
        pageInfo.textContent = `Sayfa ${currentPage} / ${totalPages}`;
        pageInfo.classList.add('me-2');
        container.appendChild(pageInfo);

        // Next button
        if (currentPage < totalPages) {
            const nextBtn = this.createButton('Sonraki', () => onPageChange(currentPage + 1));
            container.appendChild(nextBtn);
        }
    }

    /**
     * Create a pagination button
     * @param {string} text - Button text
     * @param {Function} onClick - Click handler
     * @returns {HTMLButtonElement} Button element
     */
    static createButton(text, onClick) {
        const btn = document.createElement('button');
        btn.classList.add('btn', 'btn-sm', 'btn-outline-secondary', 'me-2');
        btn.textContent = text;
        btn.addEventListener('click', onClick);
        return btn;
    }
}

/**
 * Modal Manager for consistent modal handling
 */
export class ModalManager {
    /**
     * Initialize a Bootstrap modal
     * @param {string} modalId - Modal element ID
     * @param {string} openBtnSelector - Selector for open button
     * @param {Function} onOpen - Callback before modal opens
     * @returns {bootstrap.Modal|null} Modal instance or null
     */
    static init(modalId, openBtnSelector, onOpen = null) {
        const modalElem = document.getElementById(modalId);
        if (!modalElem) return null;

        const modal = new bootstrap.Modal(modalElem);
        const openBtn = document.querySelector(openBtnSelector);

        if (openBtn) {
            openBtn.addEventListener('click', function() {
                if (onOpen) onOpen(modal);
                modal.show();
            });
        }

        return modal;
    }

    /**
     * Get existing modal instance
     * @param {string} modalId - Modal element ID
     * @returns {bootstrap.Modal|null} Modal instance or null
     */
    static getInstance(modalId) {
        const modalElem = document.getElementById(modalId);
        if (!modalElem) return null;
        return bootstrap.Modal.getInstance(modalElem);
    }
}

/**
 * Show a toast/alert message
 * @param {string} message - Message text
 * @param {string} type - Bootstrap alert type (success, danger, warning, info)
 * @param {number} duration - Duration in ms (default: 5000)
 */
export function showMessage(message, type = 'success', duration = 5000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 80px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alertDiv);

    setTimeout(() => alertDiv.remove(), duration);
}

/**
 * Debounce function to limit function calls
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in ms
 * @returns {Function} Debounced function
 */
export function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
