(function () {
    'use strict';

    function initPollForm(form) {
        var fields = Array.from(form.querySelectorAll('[data-option-field]'));
        var addButton = form.querySelector('[data-add-option]');
        var countLabel = form.querySelector('[data-option-count]');
        if (!fields.length || !addButton) {
            return;
        }

        var lastVisibleIndex = 1;
        fields.forEach(function (field, index) {
            if (!field.classList.contains('is-hidden')) {
                lastVisibleIndex = index;
            }
        });
        fields.forEach(function (field, index) {
            if (index <= lastVisibleIndex) {
                field.classList.remove('is-hidden');
            }
        });

        function refreshOptions() {
            var visibleFields = fields.filter(function (field) {
                return !field.classList.contains('is-hidden');
            });
            visibleFields.forEach(function (field, index) {
                var number = field.querySelector('[data-option-number]');
                if (number) {
                    number.textContent = String(index + 1);
                }
            });
            if (countLabel) {
                countLabel.textContent = visibleFields.length + ' / ' + fields.length;
            }
            addButton.disabled = visibleFields.length === fields.length;
        }

        fields.slice(0, 2).forEach(function (field) {
            var input = field.querySelector('input');
            if (input) {
                input.required = true;
            }
        });

        addButton.addEventListener('click', function () {
            var nextField = fields.find(function (field) {
                return field.classList.contains('is-hidden');
            });
            if (!nextField) {
                return;
            }
            nextField.classList.remove('is-hidden');
            var input = nextField.querySelector('input');
            if (input) {
                input.focus();
            }
            refreshOptions();
        });

        form.querySelectorAll('[data-remove-option]').forEach(function (button) {
            button.addEventListener('click', function () {
                var field = button.closest('[data-option-field]');
                var input = field ? field.querySelector('input') : null;
                if (input) {
                    input.value = '';
                }
                if (field) {
                    field.classList.add('is-hidden');
                }
                refreshOptions();
            });
        });

        refreshOptions();
    }

    function initVoteForm(form) {
        form.addEventListener('submit', function (event) {
            var selected = form.querySelector('input[name="option"]:checked:not(:disabled)');
            var error = form.querySelector('.poll-vote-error');
            if (!selected) {
                event.preventDefault();
                if (error) {
                    error.hidden = false;
                }
                return;
            }

            if (error) {
                error.hidden = true;
            }
            var template = form.dataset.voteUrlTemplate || '';
            form.action = template.replace('/0/', '/' + selected.value + '/');
        });

        form.querySelectorAll('input[name="option"]').forEach(function (input) {
            input.addEventListener('change', function () {
                var error = form.querySelector('.poll-vote-error');
                if (error) {
                    error.hidden = true;
                }
            });
        });
    }

    function initDeleteForm(form) {
        form.addEventListener('submit', async function (event) {
            event.preventDefault();
            var confirmed;
            if (typeof window.showConfirm === 'function') {
                confirmed = await window.showConfirm(
                    'Bu anket kalıcı olarak silinsin mi?',
                    'Anketi sil',
                    'Sil',
                    'btn-outline-danger'
                );
            } else {
                confirmed = window.confirm('Bu anket kalıcı olarak silinsin mi?');
            }
            if (confirmed) {
                form.submit();
            }
        });
    }

    function openRequestedModal(page) {
        if (typeof bootstrap === 'undefined') {
            return;
        }
        var modalId = null;
        if (page.dataset.openEdit === 'true') {
            modalId = 'editPollModal';
        } else if (page.dataset.openCreate === 'true') {
            modalId = 'createPollModal';
        }
        if (!modalId) {
            return;
        }
        var modalElement = document.getElementById(modalId);
        if (modalElement) {
            bootstrap.Modal.getOrCreateInstance(modalElement).show();
        }
    }

    function init() {
        var page = document.getElementById('pollsPage');
        if (!page) {
            return;
        }

        document.querySelectorAll('[data-poll-form]').forEach(initPollForm);
        document.querySelectorAll('.poll-vote-form').forEach(initVoteForm);
        document.querySelectorAll('.poll-delete-form').forEach(initDeleteForm);

        document.addEventListener('click', function (event) {
            document.querySelectorAll('.poll-card-menu[open]').forEach(function (menu) {
                if (!menu.contains(event.target)) {
                    menu.removeAttribute('open');
                }
            });
        });

        openRequestedModal(page);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
