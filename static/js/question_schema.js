(function () {
    function readJsonScript(id, fallback) {
        var el = document.getElementById(id);
        if (!el) {
            return fallback;
        }
        try {
            return JSON.parse(el.textContent);
        } catch (err) {
            return fallback;
        }
    }

    function setChevron(button, expanded) {
        var icon = button.querySelector('i');
        button.classList.toggle('is-open', Boolean(expanded));
        if (!icon) {
            return;
        }
        if (button.classList.contains('schema-content-btn')) {
            icon.className = expanded ? 'bi bi-eye-slash' : 'bi bi-eye';
        } else {
            icon.className = expanded ? 'bi bi-chevron-down' : 'bi bi-chevron-right';
        }
        button.setAttribute('aria-expanded', expanded ? 'true' : 'false');
    }

    function createMetricBadge(iconClass, label, value, extraClass) {
        var badge = document.createElement('span');
        badge.className = 'schema-metric';
        if (extraClass) {
            badge.classList.add(extraClass);
        }

        var icon = document.createElement('i');
        icon.className = 'schema-metric-icon ' + iconClass;
        badge.appendChild(icon);

        var labelEl = document.createElement('span');
        labelEl.className = 'schema-metric-label';
        labelEl.textContent = label;
        badge.appendChild(labelEl);

        var valueEl = document.createElement('strong');
        valueEl.className = 'schema-metric-value';
        valueEl.textContent = String(value || 0);
        badge.appendChild(valueEl);

        return badge;
    }

    function createEmptyInfo(text) {
        var empty = document.createElement('div');
        empty.className = 'schema-empty';
        empty.style.padding = '12px';
        empty.textContent = text;
        return empty;
    }

    function initBootstrapHints(container) {
        if (!container || typeof bootstrap === 'undefined') {
            return;
        }

        container.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (el) {
            if (!bootstrap.Tooltip.getInstance(el)) {
                new bootstrap.Tooltip(el);
            }
        });

        container.querySelectorAll('[data-bs-toggle="popover"]').forEach(function (el) {
            if (!bootstrap.Popover.getInstance(el)) {
                new bootstrap.Popover(el);
            }
        });
    }

    function buildEndpointUrl(template, questionId, userId) {
        var base = template.replace('/0/', '/' + questionId + '/');
        var url = new URL(base, window.location.origin);
        if (userId) {
            url.searchParams.set('user_id', String(userId));
        }
        return url.pathname + url.search;
    }

    function renderContentPanel(panel, payload) {
        panel.innerHTML = '';

        var header = document.createElement('div');
        header.className = 'schema-content-header schema-content-header-compact';

        var stats = document.createElement('span');
        stats.className = 'schema-content-count';
        stats.textContent = payload.shown_answers + '/' + payload.total_answers + ' entry';
        header.appendChild(stats);
        panel.appendChild(header);

        if (!payload.answers || payload.answers.length === 0) {
            panel.appendChild(createEmptyInfo('Bu yazarin bu baslikta entrysi yok.'));
            return;
        }

        var body = document.createElement('div');
        body.className = 'schema-content-body';

        payload.answers.forEach(function (entry, index) {
            var branch = document.createElement('div');
            branch.className = 'schema-entry-branch';
            var isLast = index === (payload.answers.length - 1);

            var stem = document.createElement('div');
            stem.className = 'schema-branch-stem' + (isLast ? ' last' : '');
            branch.appendChild(stem);

            var item = document.createElement('article');
            item.className = 'schema-entry';

            var meta = document.createElement('div');
            meta.className = 'schema-entry-meta';

            var order = document.createElement('span');
            order.className = 'schema-entry-order';
            order.textContent = (entry.roman || '?') + '.';
            meta.appendChild(order);

            var authorAndDate = document.createElement('span');
            authorAndDate.textContent = entry.user + ' | ' + entry.created_at;
            meta.appendChild(authorAndDate);
            item.appendChild(meta);

            var text = document.createElement('div');
            text.className = 'schema-entry-text answer-text';
            if (entry.rendered_html) {
                text.innerHTML = entry.rendered_html;
            } else {
                text.textContent = entry.preview;
            }
            item.appendChild(text);

            var bottom = document.createElement('div');
            bottom.className = 'schema-entry-footer';

            if (entry.is_truncated) {
                var longTag = document.createElement('span');
                longTag.className = 'schema-entry-flag';
                longTag.textContent = 'uzun icerik';
                bottom.appendChild(longTag);
            } else {
                var spacer = document.createElement('span');
                spacer.className = 'schema-entry-flag schema-entry-flag-empty';
                spacer.textContent = '';
                bottom.appendChild(spacer);
            }

            var link = document.createElement('a');
            link.className = 'schema-entry-link';
            link.href = entry.answer_url;
            link.textContent = 'Girdiye git';
            bottom.appendChild(link);

            item.appendChild(bottom);
            branch.appendChild(item);
            body.appendChild(branch);
        });

        panel.appendChild(body);
        initBootstrapHints(panel);

        if (payload.has_more && payload.question && payload.question.detail_url) {
            var footer = document.createElement('div');
            footer.className = 'schema-content-footer';

            var moreLink = document.createElement('a');
            moreLink.href = payload.question.detail_url;
            moreLink.className = 'schema-content-more';
            moreLink.textContent = 'Basliga git';
            footer.appendChild(moreLink);
            panel.appendChild(footer);
        }
    }

    function createNode(nodeData, depth, config) {
        var wrapper = document.createElement('div');
        wrapper.className = 'schema-node' + (depth === 0 ? ' root-node' : '');
        wrapper.dataset.questionId = String(nodeData.id);
        wrapper.style.setProperty('--schema-depth', String(depth || 0));
        if (config && config.nodeRegistry) {
            config.nodeRegistry.set(String(nodeData.id), wrapper);
        }

        var line = document.createElement('div');
        line.className = 'schema-node-line';
        line.dataset.depth = String(depth || 0);

        var lead = document.createElement('div');
        lead.className = 'schema-node-lead';

        var toggleChildrenBtn = document.createElement('button');
        toggleChildrenBtn.type = 'button';
        toggleChildrenBtn.className = 'schema-toggle-btn';
        toggleChildrenBtn.title = 'Alt basliklari ac/kapat';
        toggleChildrenBtn.innerHTML = '<i class="bi bi-chevron-right"></i>';
        toggleChildrenBtn.disabled = !nodeData.child_count;
        setChevron(toggleChildrenBtn, false);
        lead.appendChild(toggleChildrenBtn);
        line.appendChild(lead);

        var main = document.createElement('div');
        main.className = 'schema-node-main';

        var titleLink = document.createElement('a');
        titleLink.className = 'schema-title';
        titleLink.href = nodeData.detail_url;
        titleLink.textContent = nodeData.text;
        main.appendChild(titleLink);

        var subMeta = document.createElement('div');
        subMeta.className = 'schema-node-submeta';

        var kindEl = document.createElement('span');
        kindEl.className = 'schema-node-kind';
        kindEl.textContent = depth === 0 ? 'Kok baslik' : 'Alt baslik';
        subMeta.appendChild(kindEl);

        if (nodeData.slug) {
            var slugEl = document.createElement('span');
            slugEl.className = 'schema-node-slug';
            slugEl.textContent = nodeData.slug.replace(/-/g, ' ');
            subMeta.appendChild(slugEl);
        }
        main.appendChild(subMeta);
        line.appendChild(main);

        var actions = document.createElement('div');
        actions.className = 'schema-node-actions';
        actions.appendChild(createMetricBadge('bi bi-diagram-3', 'Alt', nodeData.child_count || 0, 'schema-metric-branches'));
        actions.appendChild(createMetricBadge('bi bi-journal-text', 'Entry', nodeData.answer_count || 0, 'schema-metric-entries'));

        var toggleContentBtn = document.createElement('button');
        toggleContentBtn.type = 'button';
        toggleContentBtn.className = 'schema-content-btn';
        toggleContentBtn.title = 'Yazarin entrylerini ac/kapat';
        toggleContentBtn.innerHTML = '<i class="bi bi-eye"></i>';
        setChevron(toggleContentBtn, false);
        actions.appendChild(toggleContentBtn);
        line.appendChild(actions);

        wrapper.appendChild(line);

        var contentPanel = document.createElement('div');
        contentPanel.className = 'schema-content-panel';
        wrapper.appendChild(contentPanel);

        var childrenContainer = document.createElement('div');
        childrenContainer.className = 'schema-children';
        wrapper.appendChild(childrenContainer);

        var childrenLoaded = false;
        var contentLoaded = false;

        function toggleChildren() {
            if (toggleChildrenBtn.disabled) {
                return;
            }

            var isOpen = childrenContainer.classList.contains('open');
            if (isOpen) {
                childrenContainer.classList.remove('open');
                setChevron(toggleChildrenBtn, false);
                return;
            }

            if (!childrenLoaded) {
                childrenContainer.innerHTML = '';
                childrenContainer.appendChild(createEmptyInfo('Yukleniyor...'));
                fetch(buildEndpointUrl(config.childrenUrlTemplate, nodeData.id, config.userId), { credentials: 'same-origin' })
                    .then(function (response) {
                        if (!response.ok) {
                            throw new Error('children request failed');
                        }
                        return response.json();
                    })
                    .then(function (payload) {
                        childrenContainer.innerHTML = '';
                        var children = payload.children || [];
                        if (!children.length) {
                            childrenContainer.appendChild(createEmptyInfo('Alt baslik bulunmuyor.'));
                        } else {
                            children.forEach(function (child) {
                                childrenContainer.appendChild(createNode(child, depth + 1, config));
                            });
                        }
                        childrenLoaded = true;
                        childrenContainer.classList.add('open');
                        setChevron(toggleChildrenBtn, true);
                    })
                    .catch(function () {
                        childrenContainer.innerHTML = '';
                        childrenContainer.appendChild(createEmptyInfo('Alt basliklar yuklenemedi.'));
                        childrenContainer.classList.add('open');
                        setChevron(toggleChildrenBtn, true);
                    });
                return;
            }

            childrenContainer.classList.add('open');
            setChevron(toggleChildrenBtn, true);
        }

        function toggleContent() {
            var isOpen = contentPanel.classList.contains('open');
            if (isOpen) {
                contentPanel.classList.remove('open');
                setChevron(toggleContentBtn, false);
                return;
            }

            if (!contentLoaded) {
                contentPanel.innerHTML = '';
                contentPanel.appendChild(createEmptyInfo('Icerik yukleniyor...'));
                contentPanel.classList.add('open');
                setChevron(toggleContentBtn, true);

                fetch(buildEndpointUrl(config.contentUrlTemplate, nodeData.id, config.userId), { credentials: 'same-origin' })
                    .then(function (response) {
                        if (!response.ok) {
                            throw new Error('content request failed');
                        }
                        return response.json();
                    })
                    .then(function (payload) {
                        renderContentPanel(contentPanel, payload);
                        contentLoaded = true;
                    })
                    .catch(function () {
                        contentPanel.innerHTML = '';
                        contentPanel.appendChild(createEmptyInfo('Icerik yuklenemedi.'));
                    });
                return;
            }

            contentPanel.classList.add('open');
            setChevron(toggleContentBtn, true);
        }

        toggleChildrenBtn.addEventListener('click', function (event) {
            event.preventDefault();
            toggleChildren();
        });

        toggleContentBtn.addEventListener('click', function (event) {
            event.preventDefault();
            toggleContent();
        });

        return wrapper;
    }

    function collapseAll(rootElement) {
        rootElement.querySelectorAll('.schema-children.open').forEach(function (el) {
            el.classList.remove('open');
        });
        rootElement.querySelectorAll('.schema-content-panel.open').forEach(function (el) {
            el.classList.remove('open');
        });
        rootElement.querySelectorAll('.schema-toggle-btn').forEach(function (btn) {
            if (!btn.disabled) {
                setChevron(btn, false);
            }
        });
        rootElement.querySelectorAll('.schema-content-btn').forEach(function (btn) {
            setChevron(btn, false);
        });
    }

    function setVisibleRootsByIds(rootElement, visibleRootIds) {
        var nodes = Array.prototype.slice.call(rootElement.children);
        var visibleCount = 0;

        nodes.forEach(function (node) {
            var nodeId = node && node.dataset ? String(node.dataset.questionId || '') : '';
            var isVisible = !visibleRootIds || visibleRootIds.has(nodeId);
            node.style.display = isVisible ? '' : 'none';
            if (isVisible) {
                visibleCount += 1;
            }
        });

        return visibleCount;
    }

    function collectRootIdsFromResults(results) {
        var ids = new Set();
        (results || []).forEach(function (result) {
            if (!result) {
                return;
            }

            if (Array.isArray(result.path_ids) && result.path_ids.length) {
                ids.add(String(result.path_ids[0]));
                return;
            }

            if (result.kind === 'root' && result.id) {
                ids.add(String(result.id));
            }
        });
        return ids;
    }

    function getRootTitleSuggestions(query, rootNodes, limit) {
        var normalized = (query || '').trim().toLowerCase();
        if (!normalized) {
            return [];
        }

        var matches = rootNodes.filter(function (node) {
            var text = node && node.text ? String(node.text) : '';
            return text.toLowerCase().indexOf(normalized) !== -1;
        });

        matches.sort(function (a, b) {
            var aText = String(a.text || '');
            var bText = String(b.text || '');
            var aNorm = aText.toLowerCase();
            var bNorm = bText.toLowerCase();
            var aStarts = aNorm.indexOf(normalized) === 0 ? 0 : 1;
            var bStarts = bNorm.indexOf(normalized) === 0 ? 0 : 1;
            if (aStarts !== bStarts) {
                return aStarts - bStarts;
            }

            var aIndex = aNorm.indexOf(normalized);
            var bIndex = bNorm.indexOf(normalized);
            if (aIndex !== bIndex) {
                return aIndex - bIndex;
            }
            return aText.localeCompare(bText, 'tr', { sensitivity: 'base' });
        });

        return matches.slice(0, limit || 8).map(function (node) {
            return {
                id: node.id,
                text: node.text,
                kind: 'root',
                depth: 0,
                path_ids: [node.id],
                path_label: node.text
            };
        });
    }

    function waitForCondition(predicate, timeoutMs, intervalMs) {
        return new Promise(function (resolve) {
            var timeout = timeoutMs || 1800;
            var interval = intervalMs || 50;
            var startedAt = Date.now();

            function tick() {
                if (predicate()) {
                    resolve(true);
                    return;
                }
                if (Date.now() - startedAt >= timeout) {
                    resolve(false);
                    return;
                }
                setTimeout(tick, interval);
            }

            tick();
        });
    }

    async function focusNodeByPath(pathIds, context) {
        if (!pathIds || !pathIds.length || !context || !context.treeRoot || !context.nodeRegistry) {
            return false;
        }

        var ids = pathIds.map(function (id) { return String(id); });

        // Ensure all root cards are visible before drilling down to a child path.
        Array.prototype.slice.call(context.treeRoot.children).forEach(function (node) {
            node.style.display = '';
        });

        if (context.emptyState) {
            context.emptyState.style.display = 'none';
            context.emptyState.textContent = 'Bu yazar icin goruntulenecek sema verisi bulunmuyor.';
        }

        if (context.zoomResetBtn) {
            context.zoomResetBtn.click();
        }

        for (var i = 0; i < ids.length - 1; i += 1) {
            var parentNode = context.nodeRegistry.get(ids[i]);
            if (!parentNode) {
                return false;
            }

            var line = parentNode.children && parentNode.children[0] ? parentNode.children[0] : null;
            var toggleBtn = line ? line.querySelector('.schema-toggle-btn') : null;
            var childrenContainer = parentNode.children && parentNode.children[2] ? parentNode.children[2] : null;

            if (toggleBtn && !toggleBtn.disabled && childrenContainer && !childrenContainer.classList.contains('open')) {
                toggleBtn.click();
            }

            var nextId = ids[i + 1];
            var ok = await waitForCondition(function () {
                return context.nodeRegistry.has(nextId);
            }, 2600, 45);

            if (!ok) {
                return false;
            }
        }

        var targetNode = context.nodeRegistry.get(ids[ids.length - 1]);
        if (!targetNode) {
            return false;
        }

        context.treeRoot.querySelectorAll('.schema-node-line.search-focus-line').forEach(function (el) {
            el.classList.remove('search-focus-line');
        });

        var targetLine = targetNode.children && targetNode.children[0] ? targetNode.children[0] : null;
        if (targetLine) {
            targetLine.classList.add('search-focus-line');
            setTimeout(function () {
                targetLine.classList.remove('search-focus-line');
            }, 2200);
        }

        try {
            targetNode.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'nearest' });
        } catch (err) {
            // Fallback not needed; smooth scrolling support depends on browser.
        }

        return true;
    }

    function initRootSearchSuggestions(searchInput, suggestionsBox, roots, options) {
        if (!searchInput || !suggestionsBox) {
            return;
        }

        var searchUrl = (options && options.searchUrl) || '';
        var selectedUserId = (options && options.userId) || '';
        var onSelect = (options && options.onSelect) || null;
        var onQueryState = (options && options.onQueryState) || null;

        var rootNodes = [];
        var seen = {};
        roots.forEach(function (node) {
            if (!node || !node.id) {
                return;
            }
            var text = (node.text ? String(node.text) : '').trim();
            if (!text) {
                return;
            }
            var key = String(node.id);
            if (seen[key]) {
                return;
            }
            seen[key] = true;
            rootNodes.push({ id: node.id, text: text });
        });

        var activeIndex = -1;
        var currentResults = [];
        var requestSeq = 0;
        var suggestionCache = {};

        function closeSuggestions() {
            suggestionsBox.innerHTML = '';
            suggestionsBox.classList.remove('open');
            activeIndex = -1;
            currentResults = [];
        }

        function getItems() {
            return Array.prototype.slice.call(
                suggestionsBox.querySelectorAll('.schema-root-suggestion-item')
            );
        }

        function setActiveItem(index) {
            var items = getItems();
            items.forEach(function (item, itemIndex) {
                item.classList.toggle('active', itemIndex === index);
            });
        }

        function applySuggestion(result) {
            if (!result) {
                return;
            }
            searchInput.value = result.text || '';
            closeSuggestions();
            searchInput.focus();
            if (typeof onSelect === 'function') {
                onSelect(result);
            } else {
                searchInput.dispatchEvent(new Event('input'));
            }
        }

        function renderSuggestionList(results) {
            if (!results || !results.length) {
                closeSuggestions();
                return;
            }

            suggestionsBox.innerHTML = '';
            currentResults = results.slice();
            currentResults.forEach(function (result, idx) {
                var button = document.createElement('button');
                button.type = 'button';
                button.className = 'schema-root-suggestion-item';
                button.dataset.index = String(idx);

                var title = document.createElement('span');
                title.className = 'schema-root-suggestion-title';
                title.textContent = result.text || '';
                button.appendChild(title);

                var meta = document.createElement('span');
                meta.className = 'schema-root-suggestion-meta';
                var typeLabel = result.kind === 'root' ? 'Kok' : 'Alt';
                meta.textContent = typeLabel + ' | ' + (result.path_label || '');
                button.appendChild(meta);

                button.addEventListener('mousedown', function (event) {
                    event.preventDefault();
                });
                button.addEventListener('click', function () {
                    applySuggestion(result);
                });
                suggestionsBox.appendChild(button);
            });

            activeIndex = -1;
            suggestionsBox.classList.add('open');
        }

        function fetchRemoteSuggestions(query) {
            var normalized = (query || '').trim();
            if (!searchUrl || !normalized) {
                return Promise.resolve([]);
            }

            var cacheKey = String(selectedUserId || '') + '::' + normalized.toLowerCase();
            if (suggestionCache[cacheKey]) {
                return Promise.resolve(suggestionCache[cacheKey]);
            }

            var url = new URL(searchUrl, window.location.origin);
            url.searchParams.set('q', normalized);
            url.searchParams.set('limit', '10');
            if (selectedUserId) {
                url.searchParams.set('user_id', String(selectedUserId));
            }

            return fetch(url.pathname + url.search, { credentials: 'same-origin' })
                .then(function (response) {
                    if (!response.ok) {
                        throw new Error('schema search request failed');
                    }
                    return response.json();
                })
                .then(function (payload) {
                    var results = payload && Array.isArray(payload.results) ? payload.results : [];
                    suggestionCache[cacheKey] = results;
                    return results;
                })
                .catch(function () {
                    return [];
                });
        }

        function renderSuggestions() {
            var query = (searchInput.value || '').trim();
            if (!query) {
                closeSuggestions();
                if (typeof onQueryState === 'function') {
                    onQueryState('', []);
                }
                return;
            }

            var localFallback = getRootTitleSuggestions(query, rootNodes, 8);
            if (typeof onQueryState === 'function' && localFallback.length) {
                onQueryState(query, localFallback);
            }
            var seq = ++requestSeq;
            fetchRemoteSuggestions(query).then(function (remoteResults) {
                if (seq !== requestSeq) {
                    return;
                }
                var merged = (remoteResults && remoteResults.length) ? remoteResults : localFallback;
                renderSuggestionList(merged);
                if (typeof onQueryState === 'function') {
                    onQueryState(query, merged);
                }
            });
        }

        searchInput.addEventListener('input', renderSuggestions);
        searchInput.addEventListener('focus', renderSuggestions);

        searchInput.addEventListener('keydown', function (event) {
            if (!suggestionsBox.classList.contains('open')) {
                return;
            }

            var items = getItems();
            if (!items.length) {
                return;
            }

            if (event.key === 'ArrowDown') {
                event.preventDefault();
                activeIndex = (activeIndex + 1) % items.length;
                setActiveItem(activeIndex);
                return;
            }

            if (event.key === 'ArrowUp') {
                event.preventDefault();
                activeIndex = (activeIndex - 1 + items.length) % items.length;
                setActiveItem(activeIndex);
                return;
            }

            if (event.key === 'Enter' && activeIndex >= 0) {
                event.preventDefault();
                applySuggestion(currentResults[activeIndex]);
                return;
            }

            if (event.key === 'Enter' && activeIndex < 0 && currentResults.length) {
                event.preventDefault();
                applySuggestion(currentResults[0]);
                return;
            }

            if (event.key === 'Escape') {
                closeSuggestions();
            }
        });

        document.addEventListener('click', function (event) {
            if (!event.target.closest || !event.target.closest('.schema-search-wrap')) {
                closeSuggestions();
            }
        });
    }

    function initPanZoom() {
        var viewport = document.getElementById('schemaDiagramViewport');
        var canvas = document.getElementById('schemaDiagramCanvas');
        var zoomInBtn = document.getElementById('schemaZoomIn');
        var zoomOutBtn = document.getElementById('schemaZoomOut');
        var zoomResetBtn = document.getElementById('schemaZoomReset');
        var zoomIndicator = document.getElementById('schemaZoomIndicator');

        if (!viewport || !canvas) {
            return;
        }

        function isInteractiveTarget(target) {
            if (!target || !target.closest) {
                return false;
            }
            return Boolean(
                target.closest(
                    '.schema-toggle-btn, .schema-content-btn, .schema-title, ' +
                    '.schema-content-panel, .schema-content-body, .schema-entry-link, ' +
                    'button, a, input, select, textarea, label'
                )
            );
        }

        var state = {
            scale: 1,
            tx: 24,
            ty: 24,
            dragging: false,
            pointerId: null,
            startX: 0,
            startY: 0,
            startTx: 0,
            startTy: 0
        };

        function apply() {
            canvas.style.transform = 'translate(' + state.tx + 'px,' + state.ty + 'px) scale(' + state.scale + ')';
            if (zoomIndicator) {
                zoomIndicator.textContent = Math.round(state.scale * 100) + '%';
            }
        }

        function setScale(nextScale, originX, originY) {
            var clamped = Number(nextScale);
            if (!isFinite(clamped) || clamped <= 0) {
                clamped = 0.01;
            }
            var worldX = (originX - state.tx) / state.scale;
            var worldY = (originY - state.ty) / state.scale;
            state.scale = clamped;
            state.tx = originX - worldX * state.scale;
            state.ty = originY - worldY * state.scale;
            apply();
        }

        viewport.addEventListener('wheel', function (event) {
            event.preventDefault();
            var rect = viewport.getBoundingClientRect();
            var originX = event.clientX - rect.left;
            var originY = event.clientY - rect.top;
            var delta = event.deltaY < 0 ? 0.1 : -0.1;
            setScale(state.scale + delta, originX, originY);
        }, { passive: false });

        viewport.addEventListener('pointerdown', function (event) {
            if (event.button !== 0) {
                return;
            }
            if (isInteractiveTarget(event.target)) {
                return;
            }
            state.dragging = true;
            state.pointerId = event.pointerId;
            state.startX = event.clientX;
            state.startY = event.clientY;
            state.startTx = state.tx;
            state.startTy = state.ty;
            viewport.classList.add('dragging');
            viewport.setPointerCapture(event.pointerId);
        });

        viewport.addEventListener('pointermove', function (event) {
            if (!state.dragging || event.pointerId !== state.pointerId) {
                return;
            }
            var dx = event.clientX - state.startX;
            var dy = event.clientY - state.startY;
            state.tx = state.startTx + dx;
            state.ty = state.startTy + dy;
            apply();
        });

        function stopDrag(event) {
            if (!state.dragging) {
                return;
            }
            if (event && state.pointerId !== null && event.pointerId === state.pointerId) {
                viewport.releasePointerCapture(state.pointerId);
            }
            state.dragging = false;
            state.pointerId = null;
            viewport.classList.remove('dragging');
        }

        viewport.addEventListener('pointerup', stopDrag);
        viewport.addEventListener('pointercancel', stopDrag);
        viewport.addEventListener('pointerleave', stopDrag);

        if (zoomInBtn) {
            zoomInBtn.addEventListener('click', function () {
                var rect = viewport.getBoundingClientRect();
                setScale(state.scale + 0.12, rect.width / 2, rect.height / 2);
            });
        }
        if (zoomOutBtn) {
            zoomOutBtn.addEventListener('click', function () {
                var rect = viewport.getBoundingClientRect();
                setScale(state.scale - 0.12, rect.width / 2, rect.height / 2);
            });
        }
        if (zoomResetBtn) {
            zoomResetBtn.addEventListener('click', function () {
                state.scale = 1;
                state.tx = 24;
                state.ty = 24;
                apply();
            });
        }

        apply();
    }

    function initSidebarToggle() {
        var layout = document.getElementById('schemaLayout');
        var toggleBtn = document.getElementById('schemaSidebarToggle');
        var toggleIcon = document.getElementById('schemaSidebarToggleIcon');

        if (!layout || !toggleBtn || !toggleIcon) {
            return;
        }

        function setCollapsed(collapsed) {
            layout.classList.toggle('sidebar-collapsed', collapsed);
            toggleIcon.className = collapsed ? 'bi bi-chevron-right' : 'bi bi-chevron-left';
            toggleBtn.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
            toggleBtn.setAttribute('aria-label', collapsed ? 'Filtre panelini ac' : 'Filtre panelini kapat');
        }

        setCollapsed(window.innerWidth <= 980);

        toggleBtn.addEventListener('click', function () {
            setCollapsed(!layout.classList.contains('sidebar-collapsed'));
        });
    }

    function initFullscreenLayout() {
        var body = document.body;
        var root = document.documentElement;
        if (!body || !root) {
            return;
        }

        body.classList.add('schema-fullscreen');

        function updateNavbarHeightVar() {
            var navbar = document.getElementById('mainNavbar');
            var navbarHeight = navbar ? Math.round(navbar.getBoundingClientRect().height) : 70;
            root.style.setProperty('--schema-navbar-height', navbarHeight + 'px');
        }

        updateNavbarHeightVar();
        window.addEventListener('resize', updateNavbarHeightVar);
        window.addEventListener('orientationchange', updateNavbarHeightVar);
    }

    document.addEventListener('DOMContentLoaded', function () {
        var treeRoot = document.getElementById('schemaTree');
        if (!treeRoot) {
            return;
        }

        var roots = readJsonScript('question-schema-root-data', []);
        var emptyState = document.getElementById('schemaEmptyState');
        var searchInput = document.getElementById('schemaRootSearch');
        var rootSuggestions = document.getElementById('schemaRootSuggestions');
        var collapseAllBtn = document.getElementById('schemaCollapseAll');
        var userSelect = document.getElementById('schemaUserSelect');
        var zoomResetBtn = document.getElementById('schemaZoomReset');
        var nodeRegistry = new Map();

        var config = {
            childrenUrlTemplate: treeRoot.dataset.childrenUrlTemplate,
            contentUrlTemplate: treeRoot.dataset.contentUrlTemplate,
            searchUrl: treeRoot.dataset.searchUrl || '',
            userId: treeRoot.dataset.selectedUserId || '',
            nodeRegistry: nodeRegistry
        };

        var searchContext = {
            treeRoot: treeRoot,
            nodeRegistry: nodeRegistry,
            emptyState: emptyState,
            searchInput: searchInput,
            zoomResetBtn: zoomResetBtn
        };

        initFullscreenLayout();
        initSidebarToggle();

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

        if (!roots.length) {
            if (emptyState) {
                emptyState.style.display = '';
            }
            initRootSearchSuggestions(searchInput, rootSuggestions, roots, {
                searchUrl: config.searchUrl,
                userId: config.userId,
                onSelect: function () {
                    // Keep fallback behavior when there is no data in the tree.
                    if (searchInput) {
                        searchInput.dispatchEvent(new Event('input'));
                    }
                }
            });
            initPanZoom();
            return;
        }

        roots.forEach(function (rootNode) {
            treeRoot.appendChild(createNode(rootNode, 0, config));
        });

        function applyRootVisibilityFromQuery(query, results) {
            var normalized = (query || '').trim();

            if (!normalized) {
                setVisibleRootsByIds(treeRoot, null);
                if (emptyState) {
                    emptyState.style.display = 'none';
                    emptyState.textContent = 'Bu yazar icin goruntulenecek sema verisi bulunmuyor.';
                }
                return;
            }

            var visibleRootIds = collectRootIdsFromResults(results);
            var visibleCount = setVisibleRootsByIds(treeRoot, visibleRootIds);
            if (emptyState) {
                var hasMatch = visibleCount > 0;
                emptyState.style.display = hasMatch ? 'none' : '';
                emptyState.textContent = hasMatch
                    ? 'Bu yazar icin goruntulenecek sema verisi bulunmuyor.'
                    : 'Arama kriterine uygun baslik bulunamadi.';
            }
        }

        initRootSearchSuggestions(searchInput, rootSuggestions, roots, {
            searchUrl: config.searchUrl,
            userId: config.userId,
            onSelect: function (result) {
                if (!result) {
                    return;
                }
                if (result.path_ids && result.path_ids.length) {
                    focusNodeByPath(result.path_ids, searchContext);
                } else if (searchInput) {
                    searchInput.dispatchEvent(new Event('input'));
                }
            },
            onQueryState: function (query, results) {
                applyRootVisibilityFromQuery(query, results);
            }
        });

        if (collapseAllBtn) {
            collapseAllBtn.addEventListener('click', function () {
                collapseAll(treeRoot);
            });
        }

        initPanZoom();
    });
})();
