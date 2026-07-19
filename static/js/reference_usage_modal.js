(function () {
    'use strict';

    function createElement(tagName, className, text) {
        const element = document.createElement(tagName);
        if (className) element.className = className;
        if (text !== undefined && text !== null) element.textContent = text;
        return element;
    }

    function createIcon(iconName) {
        const icon = createElement('i', 'bi ' + iconName);
        icon.setAttribute('aria-hidden', 'true');
        return icon;
    }

    function formatDate(value) {
        const date = new Date(value);
        if (Number.isNaN(date.getTime())) return '';
        return new Intl.DateTimeFormat('tr-TR', {
            day: '2-digit',
            month: 'short',
            year: 'numeric',
        }).format(date);
    }

    document.addEventListener('DOMContentLoaded', function () {
        const modalElement = document.getElementById('referenceUsageModal');
        if (!modalElement || modalElement.dataset.initialized === '1') return;
        modalElement.dataset.initialized = '1';

        const loading = modalElement.querySelector('[data-reference-usage-loading]');
        const error = modalElement.querySelector('[data-reference-usage-error]');
        const content = modalElement.querySelector('[data-reference-usage-content]');
        const empty = modalElement.querySelector('[data-reference-usage-empty]');
        const list = modalElement.querySelector('[data-reference-usage-list]');
        const source = modalElement.querySelector('[data-reference-usage-source]');
        const details = modalElement.querySelector('[data-reference-usage-details]');
        const entryCount = modalElement.querySelector('[data-reference-entry-count]');
        const citationCount = modalElement.querySelector('[data-reference-citation-count]');
        const more = modalElement.querySelector('[data-reference-usage-more]');
        const loadMoreButton = modalElement.querySelector('[data-reference-usage-load-more]');
        const retryButton = modalElement.querySelector('[data-reference-usage-retry]');

        let baseUrl = '';
        let nextPage = null;
        let requestController = null;

        function setState(state) {
            loading.hidden = state !== 'loading';
            error.hidden = state !== 'error';
            content.hidden = state !== 'content';
        }

        function resetModal() {
            if (requestController) requestController.abort();
            requestController = null;
            nextPage = null;
            list.replaceChildren();
            source.textContent = '';
            details.textContent = '';
            entryCount.textContent = '0';
            citationCount.textContent = '0';
            empty.hidden = true;
            more.hidden = true;
            setState('loading');
        }

        function addMetaItem(container, iconName, text) {
            if (!text) return;
            const item = createElement('span');
            item.append(createIcon(iconName), document.createTextNode(text));
            container.appendChild(item);
        }

        function renderEntry(entry) {
            const link = createElement('a', 'reference-usage-item');
            link.href = entry.url;

            const main = createElement('div', 'reference-usage-item-main');
            const title = createElement('h4', 'reference-usage-item-title', entry.title);
            const meta = createElement('div', 'reference-usage-item-meta');
            addMetaItem(meta, 'bi-person', entry.author);
            addMetaItem(meta, 'bi-calendar3', formatDate(entry.updated_at));

            const excerpt = createElement('div', 'reference-usage-excerpt');
            if (entry.context_before) {
                excerpt.appendChild(createElement('span', 'reference-usage-context', entry.context_before));
            }
            excerpt.appendChild(createElement(
                'span',
                'reference-usage-citation-sentence',
                entry.citation_sentence || 'Kaynağın geçtiği cümle belirlenemedi.'
            ));
            if (entry.context_after) {
                excerpt.appendChild(createElement('span', 'reference-usage-context', entry.context_after));
            }
            main.append(title, meta, excerpt);

            const citationMeta = createElement('div', 'reference-usage-citation-meta');
            const usageLabel = entry.usage_count === 1 ? '1 kullanım' : entry.usage_count + ' kullanım';
            addMetaItem(citationMeta, 'bi-journal-check', usageLabel);
            if (entry.pages && entry.pages.length) {
                addMetaItem(citationMeta, 'bi-file-earmark-text', 's. ' + entry.pages.join(', '));
            }
            citationMeta.appendChild(createIcon('bi-arrow-right'));

            link.append(main, citationMeta);
            list.appendChild(link);
        }

        async function loadPage(page, append) {
            if (!baseUrl) return;
            if (requestController) requestController.abort();
            requestController = new AbortController();
            const controller = requestController;

            const url = new URL(baseUrl, window.location.origin);
            url.searchParams.set('page', String(page));
            if (!append) setState('loading');
            loadMoreButton.disabled = true;

            try {
                const response = await fetch(url.toString(), {
                    headers: {'X-Requested-With': 'XMLHttpRequest'},
                    signal: controller.signal,
                });
                if (!response.ok) throw new Error('HTTP ' + response.status);
                const data = await response.json();
                if (controller !== requestController) return;

                if (!append) {
                    list.replaceChildren();
                    source.textContent = data.reference.display;
                    details.textContent = data.reference.details || '';
                    entryCount.textContent = String(data.counts.entries);
                    citationCount.textContent = String(data.counts.usages);
                }

                data.entries.forEach(renderEntry);
                empty.hidden = data.counts.entries !== 0;
                nextPage = data.pagination.next_page;
                more.hidden = !data.pagination.has_next;
                setState('content');
            } catch (requestError) {
                if (requestError.name !== 'AbortError') setState('error');
            } finally {
                if (controller === requestController) loadMoreButton.disabled = false;
            }
        }

        document.addEventListener('click', function (event) {
            const trigger = event.target.closest('[data-reference-usage-url]');
            if (!trigger) return;
            event.preventDefault();
            baseUrl = trigger.dataset.referenceUsageUrl;
            resetModal();
            bootstrap.Modal.getOrCreateInstance(modalElement).show();
            loadPage(1, false);
        });

        loadMoreButton.addEventListener('click', function () {
            if (nextPage) loadPage(nextPage, true);
        });

        retryButton.addEventListener('click', function () {
            loadPage(1, false);
        });

        modalElement.addEventListener('hidden.bs.modal', resetModal);
    });
})();
