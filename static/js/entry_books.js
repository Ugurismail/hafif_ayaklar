(function () {
    'use strict';

    function initEntryBookQuickAdd() {
        const modalElement = document.getElementById('entryBookQuickAddModal');
        if (!modalElement || typeof bootstrap === 'undefined') return;

        const modal = bootstrap.Modal.getOrCreateInstance(modalElement);
        const context = document.getElementById('entryBookQuickAddContext');
        const search = document.getElementById('entryBookQuickSearch');
        const status = document.getElementById('entryBookQuickStatus');
        const list = document.getElementById('entryBookQuickList');
        const empty = document.getElementById('entryBookQuickEmpty');
        const createDetails = document.getElementById('entryBookQuickCreate');
        const createForm = document.getElementById('entryBookQuickCreateForm');
        const nameInput = document.getElementById('entryBookQuickName');
        const createButton = createForm.querySelector('button[type="submit"]');

        let activeAnswerId = null;
        let activeTrigger = null;
        let books = [];
        let requestController = null;
        let busy = false;

        function normalize(value) {
            return String(value || '')
                .normalize('NFKC')
                .toLocaleLowerCase('tr-TR')
                .trim();
        }

        function csrfToken() {
            const meta = document.querySelector('meta[name="csrf-token"]');
            if (meta && meta.content) return meta.content;
            if (typeof getCookie === 'function') return getCookie('csrftoken');
            return '';
        }

        async function parseResponse(response) {
            const data = await response.json().catch(function () {
                return {};
            });
            if (!response.ok) {
                throw new Error(data.error || 'Kitap işlemi tamamlanamadı.');
            }
            return data;
        }

        function setStatus(message, tone) {
            status.textContent = message || '';
            if (tone) {
                status.dataset.tone = tone;
            } else {
                delete status.dataset.tone;
            }
        }

        function setBusy(value) {
            busy = value;
            modalElement.dataset.busy = value ? 'true' : 'false';
            search.disabled = value;
            nameInput.disabled = value;
            createButton.disabled = value;
        }

        function entryAddUrl(bookId) {
            return modalElement.dataset.addUrlTemplate.replace(
                '/0/',
                '/' + bookId + '/'
            );
        }

        function updateBook(updatedBook) {
            books = books.map(function (book) {
                if (String(book.id) !== String(updatedBook.id)) return book;
                return Object.assign({}, book, updatedBook);
            });
        }

        function createBookRow(book) {
            const row = document.createElement('button');
            const alreadyAdded = Boolean(book.contains_entry);
            row.type = 'button';
            row.className = 'entry-book-quick-row';
            row.dataset.bookId = book.id;
            row.dataset.added = alreadyAdded ? 'true' : 'false';
            row.disabled = alreadyAdded || busy;

            const icon = document.createElement('span');
            icon.className = 'entry-book-quick-row-icon';
            icon.innerHTML = '<i class="bi bi-journal-bookmark" aria-hidden="true"></i>';

            const copy = document.createElement('span');
            copy.className = 'entry-book-quick-row-copy';

            const title = document.createElement('strong');
            title.textContent = book.title;

            const count = document.createElement('small');
            count.textContent = book.item_count + ' entry';

            const action = document.createElement('span');
            action.className = 'entry-book-quick-row-action';
            action.innerHTML = alreadyAdded
                ? '<i class="bi bi-check-lg" aria-hidden="true"></i><span>Eklendi</span>'
                : '<i class="bi bi-plus-lg" aria-hidden="true"></i><span>Ekle</span>';

            copy.append(title, count);
            row.append(icon, copy, action);
            return row;
        }

        function renderBooks() {
            const query = normalize(search.value);
            const visibleBooks = books.filter(function (book) {
                return !query || normalize(book.title).includes(query);
            });

            list.replaceChildren();
            visibleBooks.forEach(function (book) {
                list.appendChild(createBookRow(book));
            });

            empty.hidden = visibleBooks.length > 0;
            const emptyTitle = empty.querySelector('strong');
            const emptyText = empty.querySelector('span');
            if (books.length && query) {
                emptyTitle.textContent = 'Eşleşen kitap bulunamadı';
                emptyText.textContent = 'Başka bir arama deneyebilirsin.';
            } else {
                emptyTitle.textContent = 'Henüz bir kitap yok';
                emptyText.textContent = 'Aşağıdan ilk kitabını oluşturabilirsin.';
            }
        }

        function showLoading() {
            list.replaceChildren();
            empty.hidden = true;
            const loading = document.createElement('div');
            loading.className = 'entry-book-quick-loading';
            loading.innerHTML = [
                '<span></span>',
                '<span></span>',
                '<span></span>'
            ].join('');
            list.appendChild(loading);
        }

        async function loadBooks() {
            if (!activeAnswerId) return;
            if (requestController) requestController.abort();
            const controller = new AbortController();
            requestController = controller;
            setBusy(true);
            setStatus('Kitapların yükleniyor...');
            showLoading();

            const url = new URL(modalElement.dataset.listUrl, window.location.origin);
            url.searchParams.set('entry_id', activeAnswerId);

            try {
                const response = await fetch(url, {
                    headers: {'Accept': 'application/json'},
                    credentials: 'same-origin',
                    signal: controller.signal
                });
                const data = await parseResponse(response);
                books = Array.isArray(data.books) ? data.books : [];
                setStatus(
                    books.length
                        ? 'Eklemek istediğin kitabı seç.'
                        : 'İlk kitabını aşağıdan oluştur.',
                    ''
                );
            } catch (error) {
                if (error.name === 'AbortError') return;
                books = [];
                setStatus(error.message, 'error');
            } finally {
                if (requestController === controller) {
                    setBusy(false);
                    renderBooks();
                }
            }
        }

        async function addToBook(bookId) {
            if (busy || !activeAnswerId) return;
            const book = books.find(function (item) {
                return String(item.id) === String(bookId);
            });
            if (!book || book.contains_entry) return;

            setBusy(true);
            setStatus('Entry kitaba ekleniyor...');
            renderBooks();

            try {
                const response = await fetch(entryAddUrl(bookId), {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken()
                    },
                    body: JSON.stringify({entry_id: activeAnswerId})
                });
                const data = await parseResponse(response);
                updateBook(Object.assign({}, data.book, {contains_entry: true}));
                setStatus(data.message, 'success');
                if (typeof showToast === 'function') {
                    showToast(data.message, 'success');
                }
                if (activeTrigger) {
                    activeTrigger.dataset.added = 'true';
                }
            } catch (error) {
                setStatus(error.message, 'error');
            } finally {
                setBusy(false);
                renderBooks();
            }
        }

        async function createBook(event) {
            event.preventDefault();
            if (busy || !activeAnswerId) return;

            const title = nameInput.value.trim();
            if (!title) {
                setStatus('Önce kitap adını yaz.', 'error');
                nameInput.focus();
                return;
            }

            setBusy(true);
            setStatus('Kitap oluşturuluyor...');

            try {
                const response = await fetch(modalElement.dataset.listUrl, {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken()
                    },
                    body: JSON.stringify({
                        title: title,
                        entry_ids: [Number(activeAnswerId)]
                    })
                });
                const data = await parseResponse(response);
                const createdBook = Object.assign(
                    {},
                    data.book,
                    {contains_entry: true}
                );
                books.unshift(createdBook);
                nameInput.value = '';
                createDetails.open = false;
                setStatus(
                    'Kitap oluşturuldu ve entry kitaba eklendi.',
                    'success'
                );
                if (typeof showToast === 'function') {
                    showToast(
                        'Kitap oluşturuldu ve entry kitaba eklendi.',
                        'success'
                    );
                }
                if (activeTrigger) {
                    activeTrigger.dataset.added = 'true';
                }
            } catch (error) {
                setStatus(error.message, 'error');
            } finally {
                setBusy(false);
                renderBooks();
            }
        }

        function openForTrigger(trigger) {
            activeAnswerId = trigger.dataset.answerId;
            activeTrigger = trigger;
            books = [];
            search.value = '';
            nameInput.value = '';
            createDetails.open = false;
            const title = trigger.dataset.entryTitle || 'Bu entry';
            context.textContent = '“' + title + '”';
            modal.show();
            loadBooks();
        }

        document.addEventListener('click', function (event) {
            const trigger = event.target.closest('[data-entry-book-add]');
            if (!trigger) return;
            event.preventDefault();
            openForTrigger(trigger);
        });

        list.addEventListener('click', function (event) {
            const row = event.target.closest('[data-book-id]');
            if (!row) return;
            addToBook(row.dataset.bookId);
        });

        search.addEventListener('input', renderBooks);
        createForm.addEventListener('submit', createBook);
        modalElement.addEventListener('hidden.bs.modal', function () {
            if (requestController) requestController.abort();
            activeAnswerId = null;
            activeTrigger = null;
            books = [];
            setStatus('');
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initEntryBookQuickAdd);
    } else {
        initEntryBookQuickAdd();
    }
})();
