document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('file-search-form');
    const input = document.getElementById('file-search-input');
    const searchSection = document.getElementById('file-search-section');
    const searchResults = document.getElementById('file-search-results');
    const searchTitle = document.getElementById('file-search-title');
    const searchCount = document.getElementById('file-search-count');
    const searchEmpty = document.getElementById('file-search-empty');

    const listCard = document.getElementById('file-library-list');
    const listUrl = listCard ? listCard.dataset.listUrl : null;
    const deleteUrlTemplate = listCard ? listCard.dataset.deleteUrlTemplate : null;

    const allResults = document.getElementById('file-all-results');
    const allCount = document.getElementById('file-all-count');
    const allEmpty = document.getElementById('file-all-empty');
    const allLoad = document.getElementById('file-all-load');

    const mineResults = document.getElementById('file-mine-results');
    const mineCount = document.getElementById('file-mine-count');
    const mineEmpty = document.getElementById('file-mine-empty');
    const mineLoad = document.getElementById('file-mine-load');

    if (!form || !input || !searchResults) return;

    const searchUrl = form.dataset.searchUrl;
    let timer = null;

    const listConfigs = {
        all: {
            listEl: allResults,
            countEl: allCount,
            emptyEl: allEmpty,
            loadBtn: allLoad,
            offset: 0,
            limit: 20,
            mine: false,
            total: 0,
            loading: false,
            loadedOnce: false
        },
        mine: {
            listEl: mineResults,
            countEl: mineCount,
            emptyEl: mineEmpty,
            loadBtn: mineLoad,
            offset: 0,
            limit: 20,
            mine: true,
            total: 0,
            loading: false,
            loadedOnce: false
        }
    };

    function getCsrfToken() {
        if (typeof getCookie === 'function') {
            return getCookie('csrftoken');
        }
        return null;
    }

    function showFeedback(message, type) {
        if (typeof showToast === 'function') {
            showToast(message, type);
        } else {
            alert(message);
        }
    }

    function toggleSearchSection(show) {
        if (!searchSection) return;
        searchSection.style.display = show ? 'block' : 'none';
    }

    function buildItem(item, options = {}) {
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

        if (options.allowDelete && item.can_delete) {
            const deleteBtn = document.createElement('button');
            deleteBtn.type = 'button';
            deleteBtn.className = 'btn btn-sm btn-outline-danger';
            deleteBtn.innerHTML = '<i class="bi bi-trash"></i> Sil';
            deleteBtn.addEventListener('click', function () {
                if (typeof options.onDelete === 'function') {
                    options.onDelete(item, wrapper);
                }
            });
            actions.appendChild(deleteBtn);
        }

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

    function setListLoading(config, loading) {
        config.loading = loading;
        if (!config.loadBtn) return;
        config.loadBtn.disabled = loading;
        config.loadBtn.textContent = loading ? 'Yukleniyor...' : 'Daha fazla goster';
    }

    function updateListCount(config) {
        if (!config.countEl) return;
        if (config.total > 0) {
            const shown = Math.min(config.offset, config.total);
            config.countEl.textContent = `${shown} / ${config.total} sonuc`;
        } else {
            config.countEl.textContent = '';
        }
    }

    function fetchList(key, reset = false) {
        const config = listConfigs[key];
        if (!config || !listUrl || config.loading) return;

        if (reset) {
            config.offset = 0;
            config.total = 0;
            if (config.listEl) config.listEl.innerHTML = '';
        }

        setListLoading(config, true);

        const url = new URL(listUrl, window.location.origin);
        url.searchParams.set('limit', String(config.limit));
        url.searchParams.set('offset', String(config.offset));
        url.searchParams.set('mine', config.mine ? '1' : '0');

        fetch(url.toString(), { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(r => r.json())
            .then(data => {
                const results = data.results || [];
                if (reset && config.listEl) {
                    config.listEl.innerHTML = '';
                }
                results.forEach(item => {
                    if (config.listEl) {
                        config.listEl.appendChild(buildItem(item, {
                            allowDelete: true,
                            onDelete: handleDelete
                        }));
                    }
                });
                config.offset += results.length;
                config.total = typeof data.count === 'number' ? data.count : 0;
                updateListCount(config);
                config.loadedOnce = true;

                if (config.emptyEl) {
                    config.emptyEl.style.display = config.total === 0 ? 'block' : 'none';
                }
                if (config.loadBtn) {
                    config.loadBtn.style.display = data.has_more ? 'inline-block' : 'none';
                }
            })
            .catch(() => {
                if (reset && config.listEl) config.listEl.innerHTML = '';
                if (config.emptyEl) config.emptyEl.style.display = 'block';
                if (config.loadBtn) config.loadBtn.style.display = 'none';
            })
            .finally(() => setListLoading(config, false));
    }

    function refreshLists() {
        fetchList('all', true);
        if (listConfigs.mine.loadedOnce) {
            fetchList('mine', true);
        }
    }

    function handleDelete(item) {
        if (!deleteUrlTemplate || !item || !item.id) return;
        if (!confirm('Bu dosyayi silmek istiyor musun?')) return;

        const csrfToken = getCsrfToken();
        const url = deleteUrlTemplate.replace('/0/', `/${item.id}/`);

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken || '',
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Silme basarisiz');
                }
                return response.json();
            })
            .then(() => {
                showFeedback('Dosya silindi.', 'success');
                refreshLists();
            })
            .catch(() => {
                showFeedback('Dosya silinemedi.', 'error');
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
    if (allLoad) {
        allLoad.addEventListener('click', function () {
            fetchList('all');
        });
    }
    if (mineLoad) {
        mineLoad.addEventListener('click', function () {
            fetchList('mine');
        });
    }

    const mineTab = document.getElementById('file-tab-mine');
    if (mineTab) {
        mineTab.addEventListener('shown.bs.tab', function () {
            if (!listConfigs.mine.loadedOnce) {
                fetchList('mine', true);
            }
        });
    }

    fetchList('all', true);
});
