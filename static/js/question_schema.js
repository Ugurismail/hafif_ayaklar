(function () {
    'use strict';

    function readJsonScript(id, fallback) {
        var element = document.getElementById(id);
        if (!element) {
            return fallback;
        }
        try {
            return JSON.parse(element.textContent);
        } catch (error) {
            return fallback;
        }
    }

    function element(tagName, className, text) {
        var node = document.createElement(tagName);
        if (className) {
            node.className = className;
        }
        if (typeof text === 'string') {
            node.textContent = text;
        }
        return node;
    }

    function icon(className) {
        var node = document.createElement('i');
        node.className = 'bi ' + className;
        node.setAttribute('aria-hidden', 'true');
        return node;
    }

    function buildEndpointUrl(template, questionId, userId) {
        var base = template.replace('/0/', '/' + questionId + '/');
        var url = new URL(base, window.location.origin);
        if (userId) {
            url.searchParams.set('user_id', String(userId));
        }
        return url.pathname + url.search;
    }

    function formatCount(value, singular, plural) {
        var count = Number(value || 0);
        return count + ' ' + (count === 1 ? singular : plural);
    }

    function initBootstrapHints(container) {
        if (!container || typeof bootstrap === 'undefined') {
            return;
        }

        container.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (item) {
            if (!bootstrap.Tooltip.getInstance(item)) {
                new bootstrap.Tooltip(item);
            }
        });

        container.querySelectorAll('[data-bs-toggle="popover"]').forEach(function (item) {
            if (!bootstrap.Popover.getInstance(item)) {
                new bootstrap.Popover(item);
            }
        });
    }

    function initSchema() {
        var workspace = document.getElementById('schemaWorkspace');
        var layout = workspace ? workspace.querySelector('.schema-layout') : null;
        var tree = document.getElementById('schemaTree');
        var viewport = document.getElementById('schemaTreeViewport');
        var rootList = document.getElementById('schemaRootList');
        var rootCount = document.getElementById('schemaRootCount');
        var summary = document.getElementById('schemaSummary');
        var breadcrumb = document.getElementById('schemaBreadcrumb');
        var emptyState = document.getElementById('schemaEmptyState');
        var showAllRoots = document.getElementById('schemaShowAllRoots');
        var userSelect = document.getElementById('schemaUserSelect');
        var rootsToggle = document.getElementById('schemaRootsToggle');
        var collapseAll = document.getElementById('schemaCollapseAll');
        var search = workspace ? workspace.querySelector('.schema-search') : null;
        var searchInput = document.getElementById('schemaSearchInput');
        var searchClear = document.getElementById('schemaSearchClear');
        var searchResults = document.getElementById('schemaSearchResults');
        var inspector = document.getElementById('schemaInspector');
        var inspectorTitle = document.getElementById('schemaInspectorTitle');
        var inspectorMetrics = document.getElementById('schemaInspectorMetrics');
        var inspectorBody = document.getElementById('schemaInspectorBody');
        var inspectorFooter = document.getElementById('schemaInspectorFooter');
        var questionLink = document.getElementById('schemaQuestionLink');
        var inspectorClose = document.getElementById('schemaInspectorClose');

        if (!workspace || !layout || !tree || !rootList) {
            return;
        }

        var roots = readJsonScript('question-schema-root-data', []);
        var state = {
            roots: Array.isArray(roots) ? roots : [],
            activeRootId: null,
            selectedId: null,
            nodeRegistry: new Map(),
            contentCache: new Map(),
            userId: tree.dataset.selectedUserId || '',
            childrenUrlTemplate: tree.dataset.childrenUrlTemplate || '',
            contentUrlTemplate: tree.dataset.contentUrlTemplate || '',
            searchUrl: tree.dataset.searchUrl || '',
            searchRequest: 0,
            searchTimer: null,
            searchItems: [],
            activeSearchIndex: -1
        };

        document.body.classList.add('schema-workspace-active');

        function updateWorkspaceHeight() {
            var navbar = document.getElementById('mainNavbar');
            var navbarHeight = navbar ? Math.round(navbar.getBoundingClientRect().height) : 70;
            workspace.style.setProperty('--schema-navbar-height', navbarHeight + 'px');
        }

        function metric(label, value) {
            var wrapper = element('div', 'schema-inspector-metric');
            wrapper.appendChild(element('span', '', label));
            wrapper.appendChild(element('strong', '', String(value || 0)));
            return wrapper;
        }

        function closeInspector() {
            layout.classList.remove('inspector-open');
            inspector.setAttribute('aria-hidden', 'true');
            state.selectedId = null;
            tree.querySelectorAll('.schema-node.is-selected').forEach(function (node) {
                node.classList.remove('is-selected');
            });
        }

        function openInspector() {
            layout.classList.add('inspector-open');
            inspector.setAttribute('aria-hidden', 'false');
        }

        function renderBreadcrumb(record) {
            breadcrumb.innerHTML = '';
            var path = [];
            var current = record;
            var guard = 0;

            while (current && guard < 100) {
                path.unshift(current.data.text);
                current = current.parentId ? state.nodeRegistry.get(String(current.parentId)) : null;
                guard += 1;
            }

            if (!path.length) {
                path.push('Tüm başlangıçlar');
            }

            path.forEach(function (label, index) {
                if (index > 0) {
                    breadcrumb.appendChild(icon('bi-chevron-right'));
                }
                breadcrumb.appendChild(element('span', '', label));
            });
        }

        function setDefaultBreadcrumb() {
            breadcrumb.innerHTML = '';
            var activeRoot = state.roots.find(function (root) {
                return String(root.id) === String(state.activeRootId);
            });
            breadcrumb.appendChild(element('span', '', activeRoot ? activeRoot.text : 'Tüm başlangıçlar'));
        }

        function inspectorMessage(className, iconClass, text) {
            inspectorBody.innerHTML = '';
            var message = element('div', className);
            if (iconClass) {
                message.appendChild(icon(iconClass));
            }
            message.appendChild(element('span', '', text));
            inspectorBody.appendChild(message);
        }

        function renderEntry(entry) {
            var article = element('article', 'schema-entry');
            var header = element('header', 'schema-entry-header');
            header.appendChild(element('span', 'schema-entry-order', (entry.roman || '?') + '.'));
            header.appendChild(element('span', '', entry.user + ' · ' + entry.created_at));
            article.appendChild(header);

            var content = element('div', 'schema-entry-text answer-text');
            if (entry.rendered_html) {
                content.innerHTML = entry.rendered_html;
            } else {
                content.textContent = entry.preview || '';
            }
            article.appendChild(content);

            var footer = element('footer', 'schema-entry-footer');
            var link = element('a', '', 'Entry’ye git');
            link.href = entry.answer_url;
            link.appendChild(icon('bi-arrow-up-right'));
            footer.appendChild(link);
            article.appendChild(footer);
            return article;
        }

        function renderInspectorPayload(payload) {
            inspectorBody.innerHTML = '';
            var answers = payload && Array.isArray(payload.answers) ? payload.answers : [];

            if (!answers.length) {
                inspectorMessage('schema-inspector-empty', 'bi-journal', 'Bu başlıkta entry yok.');
                return;
            }

            var list = element('div', 'schema-entry-list');
            answers.forEach(function (entry) {
                list.appendChild(renderEntry(entry));
            });
            inspectorBody.appendChild(list);
            initBootstrapHints(inspectorBody);

            if (payload.has_more && payload.question && payload.question.detail_url) {
                var more = element('a', 'schema-inspector-more');
                more.href = payload.question.detail_url;
                more.appendChild(element(
                    'span',
                    '',
                    String(payload.total_answers - payload.shown_answers) + ' entry daha var'
                ));
                more.appendChild(icon('bi-arrow-up-right'));
                inspectorBody.appendChild(more);
            }
        }

        function loadInspectorContent(record) {
            var nodeId = String(record.data.id);
            if (state.contentCache.has(nodeId)) {
                renderInspectorPayload(state.contentCache.get(nodeId));
                return;
            }

            inspectorMessage('schema-inspector-loading', '', 'Entry’ler yükleniyor…');
            fetch(buildEndpointUrl(state.contentUrlTemplate, record.data.id, state.userId), {
                credentials: 'same-origin',
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
                .then(function (response) {
                    if (!response.ok) {
                        throw new Error('content request failed');
                    }
                    return response.json();
                })
                .then(function (payload) {
                    state.contentCache.set(nodeId, payload);
                    if (String(state.selectedId) === nodeId) {
                        renderInspectorPayload(payload);
                    }
                })
                .catch(function () {
                    if (String(state.selectedId) === nodeId) {
                        inspectorMessage('schema-inspector-error', 'bi-exclamation-circle', 'Entry’ler yüklenemedi.');
                    }
                });
        }

        function selectNode(record, options) {
            tree.querySelectorAll('.schema-node.is-selected').forEach(function (node) {
                node.classList.remove('is-selected');
            });

            record.wrapper.classList.add('is-selected');
            state.selectedId = String(record.data.id);
            inspectorTitle.textContent = record.data.text;
            inspectorMetrics.innerHTML = '';
            inspectorMetrics.appendChild(metric('Alt başlık', record.data.child_count));
            inspectorMetrics.appendChild(metric('Entry', record.data.answer_count));
            questionLink.href = record.data.detail_url;
            inspectorFooter.hidden = false;
            renderBreadcrumb(record);
            openInspector();
            loadInspectorContent(record);

            if (!options || options.scroll !== false) {
                record.row.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'nearest' });
            }
        }

        function setExpanded(record, expanded) {
            record.children.classList.toggle('is-open', expanded);
            record.toggle.setAttribute('aria-expanded', expanded ? 'true' : 'false');
        }

        function loadingRow(record, text, isError) {
            var row = element('div', isError ? 'schema-node-error' : 'schema-node-loading');
            row.appendChild(icon(isError ? 'bi-exclamation-circle' : 'bi-hourglass-split'));
            row.appendChild(element('span', '', text));
            record.children.innerHTML = '';
            record.children.appendChild(row);
        }

        function loadChildren(record) {
            if (record.childrenLoaded) {
                setExpanded(record, true);
                return Promise.resolve(record);
            }
            if (record.childrenPromise) {
                return record.childrenPromise;
            }

            loadingRow(record, 'Alt başlıklar yükleniyor…', false);
            setExpanded(record, true);

            record.childrenPromise = fetch(
                buildEndpointUrl(state.childrenUrlTemplate, record.data.id, state.userId),
                {
                    credentials: 'same-origin',
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                }
            )
                .then(function (response) {
                    if (!response.ok) {
                        throw new Error('children request failed');
                    }
                    return response.json();
                })
                .then(function (payload) {
                    var children = payload && Array.isArray(payload.children) ? payload.children : [];
                    record.children.innerHTML = '';
                    children.forEach(function (child) {
                        record.children.appendChild(createNode(child, record.depth + 1, record.data.id));
                    });
                    record.childrenLoaded = true;
                    record.childrenPromise = null;
                    setExpanded(record, true);
                    return record;
                })
                .catch(function () {
                    record.childrenPromise = null;
                    loadingRow(record, 'Alt başlıklar yüklenemedi.', true);
                    setExpanded(record, true);
                    throw new Error('children request failed');
                });

            return record.childrenPromise;
        }

        function toggleChildren(record) {
            if (!record.data.child_count) {
                return;
            }
            if (!record.childrenLoaded) {
                loadChildren(record).catch(function () {});
                return;
            }
            setExpanded(record, !record.children.classList.contains('is-open'));
        }

        function nodeMetric(iconClass, label, value) {
            var item = element('span', 'schema-node-metric');
            item.appendChild(icon(iconClass));
            item.appendChild(element('span', '', label));
            item.appendChild(element('strong', '', String(value || 0)));
            return item;
        }

        function createNode(data, depth, parentId) {
            var wrapper = element('section', 'schema-node');
            wrapper.dataset.questionId = String(data.id);
            wrapper.dataset.depth = String(depth);
            wrapper.style.setProperty('--schema-depth', String(depth));

            var row = element('div', 'schema-node-row');
            var toggle = element('button', 'schema-node-toggle');
            toggle.type = 'button';
            toggle.disabled = !data.child_count;
            toggle.setAttribute('aria-expanded', 'false');
            toggle.setAttribute('aria-label', data.child_count ? 'Alt başlıkları aç veya kapat' : 'Alt başlık yok');
            toggle.appendChild(icon('bi-chevron-right'));
            row.appendChild(toggle);

            var select = element('button', 'schema-node-select');
            select.type = 'button';
            select.appendChild(element('span', 'schema-node-title', data.text));
            var context = element('span', 'schema-node-context');
            context.appendChild(element('span', 'schema-node-level', depth === 0 ? 'Başlangıç' : 'Seviye ' + depth));
            if (data.slug) {
                context.appendChild(element('span', 'schema-node-slug', data.slug.replace(/-/g, ' ')));
            }
            select.appendChild(context);
            row.appendChild(select);

            var metrics = element('div', 'schema-node-metrics');
            metrics.appendChild(nodeMetric('bi-diagram-2', 'Alt', data.child_count));
            metrics.appendChild(nodeMetric('bi-journal-text', 'Entry', data.answer_count));
            row.appendChild(metrics);

            var openLink = element('a', 'schema-node-open');
            openLink.href = data.detail_url;
            openLink.title = 'Başlığa git';
            openLink.setAttribute('aria-label', data.text + ' başlığına git');
            openLink.appendChild(icon('bi-arrow-up-right'));
            row.appendChild(openLink);
            wrapper.appendChild(row);

            var children = element('div', 'schema-node-children');
            children.style.setProperty('--schema-depth', String(depth));
            wrapper.appendChild(children);

            var record = {
                data: data,
                depth: depth,
                parentId: parentId ? String(parentId) : null,
                wrapper: wrapper,
                row: row,
                toggle: toggle,
                children: children,
                childrenLoaded: false,
                childrenPromise: null
            };
            state.nodeRegistry.set(String(data.id), record);

            toggle.addEventListener('click', function () {
                toggleChildren(record);
            });
            select.addEventListener('click', function () {
                selectNode(record);
            });

            return wrapper;
        }

        function visibleRoots() {
            if (state.activeRootId === null) {
                return state.roots;
            }
            return state.roots.filter(function (root) {
                return String(root.id) === String(state.activeRootId);
            });
        }

        function updateRootButtons() {
            rootList.querySelectorAll('.schema-root-button').forEach(function (button) {
                var buttonValue = button.dataset.rootId || '';
                var activeValue = state.activeRootId === null ? '' : String(state.activeRootId);
                button.classList.toggle('is-active', buttonValue === activeValue);
                button.setAttribute('aria-current', buttonValue === activeValue ? 'true' : 'false');
            });
            showAllRoots.hidden = state.activeRootId === null;
        }

        function renderTree() {
            closeInspector();
            state.nodeRegistry.clear();
            tree.innerHTML = '';
            var currentRoots = visibleRoots();

            currentRoots.forEach(function (root) {
                tree.appendChild(createNode(root, 0, null));
            });

            emptyState.hidden = currentRoots.length > 0;
            setDefaultBreadcrumb();
            updateRootButtons();
            if (viewport) {
                viewport.scrollTop = 0;
                viewport.scrollLeft = 0;
            }
        }

        function rootButton(root, isAll) {
            var button = element('button', 'schema-root-button');
            button.type = 'button';
            button.dataset.rootId = isAll ? '' : String(root.id);

            var iconBox = element('span', 'schema-root-button-icon');
            iconBox.appendChild(icon(isAll ? 'bi-grid' : 'bi-diagram-2'));
            button.appendChild(iconBox);

            var label = element('span', 'schema-root-button-label');
            label.appendChild(element('strong', '', isAll ? 'Tüm başlangıçlar' : root.text));
            label.appendChild(element(
                'small',
                '',
                isAll ? formatCount(state.roots.length, 'başlık', 'başlık') : formatCount(root.child_count, 'alt başlık', 'alt başlık')
            ));
            button.appendChild(label);
            button.appendChild(element('span', 'schema-root-button-count', isAll ? String(state.roots.length) : String(root.answer_count || 0)));

            button.addEventListener('click', function () {
                state.activeRootId = isAll ? null : String(root.id);
                renderTree();
            });
            return button;
        }

        function renderRootList() {
            rootList.innerHTML = '';
            if (state.roots.length > 1) {
                rootList.appendChild(rootButton({}, true));
            }
            state.roots.forEach(function (root) {
                rootList.appendChild(rootButton(root, false));
            });
            rootCount.textContent = String(state.roots.length);
            summary.textContent = formatCount(state.roots.length, 'başlangıç başlığı', 'başlangıç başlığı');
        }

        function collapseAllNodes() {
            state.nodeRegistry.forEach(function (record) {
                setExpanded(record, false);
            });
            setDefaultBreadcrumb();
        }

        function closeSearchResults() {
            searchResults.innerHTML = '';
            searchResults.classList.remove('is-open');
            searchInput.setAttribute('aria-expanded', 'false');
            state.searchItems = [];
            state.activeSearchIndex = -1;
        }

        function setActiveSearchResult(index) {
            var buttons = searchResults.querySelectorAll('.schema-search-result');
            buttons.forEach(function (button, buttonIndex) {
                button.classList.toggle('is-active', buttonIndex === index);
            });
        }

        function focusPath(pathIds) {
            if (!Array.isArray(pathIds) || !pathIds.length) {
                return Promise.resolve(false);
            }

            var ids = pathIds.map(function (id) { return String(id); });
            state.activeRootId = ids[0];
            renderTree();

            var chain = Promise.resolve();
            ids.slice(0, -1).forEach(function (id) {
                chain = chain.then(function () {
                    var record = state.nodeRegistry.get(id);
                    return record ? loadChildren(record) : Promise.reject(new Error('path missing'));
                });
            });

            return chain.then(function () {
                var target = state.nodeRegistry.get(ids[ids.length - 1]);
                if (!target) {
                    return false;
                }
                target.wrapper.classList.add('is-search-target');
                window.setTimeout(function () {
                    target.wrapper.classList.remove('is-search-target');
                }, 1000);
                selectNode(target);
                return true;
            });
        }

        function chooseSearchResult(result) {
            searchInput.value = result.text || '';
            search.classList.add('has-query');
            closeSearchResults();
            focusPath(result.path_ids || [result.id]).catch(function () {});
        }

        function renderSearchResults(results) {
            searchResults.innerHTML = '';
            state.searchItems = results;
            state.activeSearchIndex = -1;

            if (!results.length) {
                searchResults.appendChild(element('div', 'schema-search-empty', 'Başlık bulunamadı.'));
            } else {
                results.forEach(function (result) {
                    var button = element('button', 'schema-search-result');
                    button.type = 'button';
                    button.setAttribute('role', 'option');
                    button.appendChild(element('span', 'schema-search-result-icon'));
                    button.children[0].appendChild(icon(result.kind === 'root' ? 'bi-diagram-2' : 'bi-bezier2'));

                    var copy = element('span');
                    copy.appendChild(element('strong', '', result.text || 'Başlık'));
                    copy.appendChild(element('small', '', result.path_label || ''));
                    button.appendChild(copy);
                    button.addEventListener('click', function () {
                        chooseSearchResult(result);
                    });
                    searchResults.appendChild(button);
                });
            }

            searchResults.classList.add('is-open');
            searchInput.setAttribute('aria-expanded', 'true');
        }

        function requestSearch() {
            var query = (searchInput.value || '').trim();
            var requestId = ++state.searchRequest;
            search.classList.toggle('has-query', Boolean(query));
            window.clearTimeout(state.searchTimer);

            if (query.length < 2) {
                closeSearchResults();
                return;
            }

            state.searchTimer = window.setTimeout(function () {
                var url = new URL(state.searchUrl, window.location.origin);
                url.searchParams.set('q', query);
                url.searchParams.set('limit', '10');
                if (state.userId) {
                    url.searchParams.set('user_id', state.userId);
                }

                fetch(url.pathname + url.search, {
                    credentials: 'same-origin',
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                })
                    .then(function (response) {
                        if (!response.ok) {
                            throw new Error('search request failed');
                        }
                        return response.json();
                    })
                    .then(function (payload) {
                        if (requestId !== state.searchRequest) {
                            return;
                        }
                        renderSearchResults(payload && Array.isArray(payload.results) ? payload.results : []);
                    })
                    .catch(function () {
                        if (requestId === state.searchRequest) {
                            renderSearchResults([]);
                        }
                    });
            }, 180);
        }

        function clearSearch() {
            state.searchRequest += 1;
            searchInput.value = '';
            search.classList.remove('has-query');
            closeSearchResults();
            searchInput.focus();
        }

        if (userSelect) {
            userSelect.addEventListener('change', function () {
                var params = new URLSearchParams(window.location.search);
                if (userSelect.value) {
                    params.set('user_id', userSelect.value);
                } else {
                    params.delete('user_id');
                }
                window.location.search = params.toString();
            });
        }

        rootsToggle.addEventListener('click', function () {
            var collapsed = layout.classList.toggle('roots-collapsed');
            rootsToggle.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
        });
        collapseAll.addEventListener('click', collapseAllNodes);
        showAllRoots.addEventListener('click', function () {
            state.activeRootId = null;
            renderTree();
        });
        inspectorClose.addEventListener('click', closeInspector);
        searchInput.addEventListener('input', requestSearch);
        searchInput.addEventListener('focus', requestSearch);
        searchClear.addEventListener('click', clearSearch);

        searchInput.addEventListener('keydown', function (event) {
            if (!searchResults.classList.contains('is-open')) {
                return;
            }
            if (event.key === 'Escape') {
                event.preventDefault();
                closeSearchResults();
                return;
            }
            if (!state.searchItems.length) {
                return;
            }
            if (event.key === 'ArrowDown') {
                event.preventDefault();
                state.activeSearchIndex = (state.activeSearchIndex + 1) % state.searchItems.length;
                setActiveSearchResult(state.activeSearchIndex);
            } else if (event.key === 'ArrowUp') {
                event.preventDefault();
                state.activeSearchIndex = (state.activeSearchIndex - 1 + state.searchItems.length) % state.searchItems.length;
                setActiveSearchResult(state.activeSearchIndex);
            } else if (event.key === 'Enter') {
                event.preventDefault();
                chooseSearchResult(state.searchItems[state.activeSearchIndex >= 0 ? state.activeSearchIndex : 0]);
            }
        });

        document.addEventListener('click', function (event) {
            if (!event.target.closest('.schema-search')) {
                closeSearchResults();
            }
        });

        window.addEventListener('resize', updateWorkspaceHeight);
        window.addEventListener('orientationchange', updateWorkspaceHeight);
        updateWorkspaceHeight();
        renderRootList();
        renderTree();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSchema);
    } else {
        initSchema();
    }
})();
