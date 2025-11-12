// static/js/link_existing_question.js
document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('linkExistingQuestionModal');
    const searchInput = document.getElementById('link-question-search-input');
    const resultsDiv = document.getElementById('link-question-search-results');
    const noResultsDiv = document.getElementById('link-question-no-results');

    if (!modal || !searchInput || !resultsDiv) return;

    // Get question slug from data attribute or URL
    const questionSlug = modal.dataset.questionSlug ||
        window.location.pathname.split('/').filter(p => p).slice(-1)[0];

    // Also try to get question ID for search API (if available)
    const questionId = document.getElementById('answer_form_question_id')?.value || '';

    if (!questionSlug) {
        console.error('Question slug not found');
        return;
    }

    let searchTimeout;
    let selectedIndex = -1;

    // Keyboard navigation
    searchInput.addEventListener('keydown', function (e) {
        const items = resultsDiv.querySelectorAll('.list-group-item');

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            selectedIndex = Math.min(selectedIndex + 1, items.length - 1);
            updateSelection(items);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            selectedIndex = Math.max(selectedIndex - 1, -1);
            updateSelection(items);
        } else if (e.key === 'Enter' && selectedIndex >= 0 && items[selectedIndex]) {
            e.preventDefault();
            items[selectedIndex].click();
        }
    });

    function updateSelection(items) {
        items.forEach((item, index) => {
            if (index === selectedIndex) {
                item.classList.add('active');
                item.scrollIntoView({ block: 'nearest' });
            } else {
                item.classList.remove('active');
            }
        });
    }

    // Search when user types
    searchInput.addEventListener('input', function () {
        selectedIndex = -1;
        clearTimeout(searchTimeout);
        const query = this.value.trim();

        if (!query || query.length < 2) {
            resultsDiv.innerHTML = '';
            noResultsDiv.style.display = 'none';
            return;
        }

        searchTimeout = setTimeout(() => {
            fetch(`/search-questions-for-linking/?q=${encodeURIComponent(query)}&parent_id=${questionId}`, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
                .then(r => r.json())
                .then(data => {
                    resultsDiv.innerHTML = '';
                    if (data.results && data.results.length > 0) {
                        noResultsDiv.style.display = 'none';
                        data.results.forEach(item => {
                            const div = document.createElement('div');
                            div.className = 'list-group-item list-group-item-action';
                            div.style.cursor = 'pointer';
                            div.innerHTML = `
                                <div class="d-flex justify-content-between align-items-center">
                                    <span>${item.text}</span>
                                    <small class="text-muted">${item.answer_count} yanıt</small>
                                </div>
                            `;
                            div.dataset.questionId = item.id;
                            div.addEventListener('click', () => linkQuestion(item.id, item.text));
                            resultsDiv.appendChild(div);
                        });
                    } else {
                        noResultsDiv.style.display = 'block';
                    }
                })
                .catch(err => console.error('Arama hatası:', err));
        }, 300);
    });

    // Link selected question
    function linkQuestion(subquestionId, subquestionText) {
        // Get CSRF token
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(`/${questionSlug}/add-as-subquestion/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: `subquestion_id=${subquestionId}`
        })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    // Show success message
                    showMessage(data.message, 'success');
                    // Close modal
                    const modalInstance = bootstrap.Modal.getInstance(modal);
                    modalInstance.hide();
                    // Clear search
                    searchInput.value = '';
                    resultsDiv.innerHTML = '';
                    // Reload page to show new subquestion
                    setTimeout(() => location.reload(), 1000);
                } else {
                    showMessage(data.error || 'Bir hata oluştu', 'danger');
                }
            })
            .catch(err => {
                console.error('Bağlama hatası:', err);
                showMessage('Bağlantı eklenirken bir hata oluştu', 'danger');
            });
    }

    // Show message helper
    function showMessage(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 80px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(alertDiv);
        setTimeout(() => alertDiv.remove(), 5000);
    }

    // Clear search when modal is closed
    modal.addEventListener('hidden.bs.modal', function () {
        searchInput.value = '';
        resultsDiv.innerHTML = '';
        noResultsDiv.style.display = 'none';
    });
});
