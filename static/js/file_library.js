document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('file-search-form');
    const input = document.getElementById('file-search-input');
    const searchSection = document.getElementById('file-search-section');
    const searchResults = document.getElementById('file-search-results');
    const searchTitle = document.getElementById('file-search-title');
    const searchCount = document.getElementById('file-search-count');
    const searchEmpty = document.getElementById('file-search-empty');
    const latestResults = document.getElementById('file-latest-results');
    const latestTitle = document.getElementById('file-latest-title');
    const latestCount = document.getElementById('file-latest-count');
    const latestEmpty = document.getElementById('file-latest-empty');

    if (!form || !input || !searchResults || !latestResults) return;

    const searchUrl = form.dataset.searchUrl;
    let timer = null;

    function toggleSearchSection(show) {
        if (!searchSection) return;
        searchSection.style.display = show ? 'block' : 'none';
    }

    function buildItem(item) {
        const wrapper = document.createElement('div');
        wrapper.className = 'list-group-item d-flex flex-column flex-md-row align-items-md-center justify-content-between gap-2';

        const info = document.createElement('div');
        info.className = 'flex-grow-1';

        const itemTitle = document.createElement('div');
        itemTitle.className = 'fw-semibold';
        itemTitle.textContent = item.title;
        info.appendChild(itemTitle);

        const meta = document.createElement('div');
        meta.className = 'text-muted small';
        meta.textContent = `${item.filename} • ${item.size} • ${item.uploaded_by} • ${item.uploaded_at}`;
        info.appendChild(meta);

        if (item.description) {
            const desc = document.createElement('div');
            desc.className = 'text-muted small mt-1';
            desc.textContent = item.description;
            info.appendChild(desc);
        }

        const actions = document.createElement('div');
        actions.className = 'd-flex gap-2 flex-wrap';

        const downloadBtn = document.createElement('a');
        downloadBtn.className = 'btn btn-sm btn-theme-primary';
        downloadBtn.href = item.file_url;
        downloadBtn.setAttribute('download', '');
        downloadBtn.innerHTML = '<i class="bi bi-download"></i> Indir';

        const openBtn = document.createElement('a');
        openBtn.className = 'btn btn-sm btn-outline-theme-secondary';
        openBtn.href = item.file_url;
        openBtn.target = '_blank';
        openBtn.rel = 'noopener noreferrer';
        openBtn.innerHTML = '<i class="bi bi-box-arrow-up-right"></i> Ac';

        actions.appendChild(downloadBtn);
        actions.appendChild(openBtn);

        wrapper.appendChild(info);
        wrapper.appendChild(actions);
        return wrapper;
    }

    function renderResults(data, listEl, titleEl, countEl, emptyEl) {
        listEl.innerHTML = '';
        if (titleEl && data.label) {
            titleEl.textContent = data.label;
        }
        if (countEl) {
            if (typeof data.count === 'number') {
                countEl.textContent = `${data.shown} / ${data.count} sonuc`;
            } else {
                countEl.textContent = '';
            }
        }

        if (!data.results || data.results.length === 0) {
            if (emptyEl) emptyEl.style.display = 'block';
            return;
        }
        if (emptyEl) emptyEl.style.display = 'none';

        data.results.forEach(item => {
            listEl.appendChild(buildItem(item));
        });
    }

    function fetchResults(query, listEl, titleEl, countEl, emptyEl, limit) {
        if (!searchUrl) return;
        listEl.innerHTML = '';
        if (emptyEl) emptyEl.style.display = 'none';
        const url = new URL(searchUrl, window.location.origin);
        if (query) {
            url.searchParams.set('q', query);
        }
        if (limit) {
            url.searchParams.set('limit', String(limit));
        }
        fetch(url.toString(), { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(r => r.json())
            .then(data => renderResults(data, listEl, titleEl, countEl, emptyEl))
            .catch(() => {
                listEl.innerHTML = '';
                if (emptyEl) emptyEl.style.display = 'block';
            });
    }

    form.addEventListener('submit', function (event) {
        event.preventDefault();
    });

    input.addEventListener('input', function () {
        const query = input.value.trim();
        clearTimeout(timer);
        timer = setTimeout(function () {
            if (!query) {
                toggleSearchSection(false);
                searchResults.innerHTML = '';
                if (searchEmpty) searchEmpty.style.display = 'none';
                return;
            }
            toggleSearchSection(true);
            fetchResults(query, searchResults, searchTitle, searchCount, searchEmpty);
        }, 250);
    });

    const initialQuery = input.value.trim();
    if (initialQuery) {
        toggleSearchSection(true);
        fetchResults(initialQuery, searchResults, searchTitle, searchCount, searchEmpty);
    } else {
        toggleSearchSection(false);
    }
    fetchResults('', latestResults, latestTitle, latestCount, latestEmpty, 10);
});
