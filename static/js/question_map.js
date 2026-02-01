// static/js/question_map.js

document.addEventListener('DOMContentLoaded', function () {
    var chartElement = document.getElementById('chart');
    if (!chartElement) {
        console.error('Chart element not found');
        return;
    }
    var width = chartElement.clientWidth;
    var height = chartElement.clientHeight || 800;
    var svg, g, zoom, simulation, link, node, label, userLabelGroup, arrows;
    var nodesData = [], linksData = [], selectedUsers = [];
    const BASE_NODE_SIZE = 20;
    const LINK_SIZE_STEP = 1;
    const LABEL_BASE_SIZE = 12;
    var focusQuestionId = window.focusQuestionId || null;

    setupButtons();
    setupUserSearch();
    setupQuestionSearch();
    setupHashtagSearch();

    fetchData('/map-data/', function (data) {
        nodesData = data.nodes;
        linksData = data.links;
        applyLinkBasedSizing();
        createGraph();
        updateStatistics();
    });

    function fetchData(url, callback) {
        fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(r => r.json()).then(callback);
    }

    function setupButtons() {
        let btnMe = document.getElementById('btn-me');
        let btnAll = document.getElementById('btn-all');
        let btnFilter = document.getElementById('btn-filter-users');
        if (btnMe) btnMe.onclick = function () {
            selectedUsers = [];
            let container = document.getElementById('selected-users-container');
            if (container) container.innerHTML = '';
            fetchData('/map-data/?filter=me', updateGraphFromData);
        };
        if (btnAll) btnAll.onclick = function () {
            selectedUsers = [];
            let container = document.getElementById('selected-users-container');
            if (container) container.innerHTML = '';
            fetchData('/map-data/', updateGraphFromData);
        };
        if (btnFilter) btnFilter.onclick = function () {
            if (selectedUsers.length > 0) {
                let params = selectedUsers.map(id => 'user_id=' + id).join('&');
                fetchData('/map-data/?' + params, updateGraphFromData);
            }
        };
    }

    function setupUserSearch() {
        let searchInput = document.getElementById('user-search-input');
        let resultsDiv = document.getElementById('user-search-results');
        let currentFocus = -1;

        if (!searchInput || !resultsDiv) return;

        searchInput.addEventListener('input', function () {
            let q = this.value.trim();
            currentFocus = -1;
            if (!q) return resultsDiv.style.display = 'none';
            fetch('/user-search/?q=' + encodeURIComponent(q), { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(r => r.json())
                .then(data => {
                    resultsDiv.innerHTML = '';
                    if (data.results.length) {
                        data.results.forEach(u => {
                            let div = document.createElement('div');
                            div.className = 'list-group-item';
                            div.textContent = u.username;
                            div.dataset.userId = u.id;
                            resultsDiv.appendChild(div);
                        });
                        resultsDiv.style.display = 'block';
                    } else {
                        resultsDiv.style.display = 'none';
                    }
                });
        });

        // Keyboard navigation
        searchInput.addEventListener('keydown', function(e) {
            let items = resultsDiv.querySelectorAll('.list-group-item');

            if (e.keyCode === 40) {
                // Arrow Down
                e.preventDefault();
                currentFocus++;
                if (currentFocus >= items.length) currentFocus = 0;
                highlightUserItem(items, currentFocus);
            }
            else if (e.keyCode === 38) {
                // Arrow Up
                e.preventDefault();
                currentFocus--;
                if (currentFocus < 0) currentFocus = items.length - 1;
                highlightUserItem(items, currentFocus);
            }
            else if (e.keyCode === 13) {
                // Enter
                e.preventDefault();
                if (currentFocus > -1 && currentFocus < items.length) {
                    items[currentFocus].click();
                }
            }
        });

        function highlightUserItem(items, index) {
            // Remove active class from all items
            for (let i = 0; i < items.length; i++) {
                items[i].classList.remove('active');
            }
            // Add active class to current item
            if (index >= 0 && index < items.length) {
                items[index].classList.add('active');
            }
        }

        resultsDiv.addEventListener('click', function (event) {
            let t = event.target;
            if (t.classList.contains('list-group-item')) {
                let userId = t.dataset.userId;
                let username = t.textContent;
                if (!selectedUsers.includes(userId)) {
                    selectedUsers.push(userId);
                    addUserToSelectedList(userId, username);
                }
                searchInput.value = '';
                resultsDiv.style.display = 'none';
                currentFocus = -1;
            }
        });
        document.addEventListener('click', function (event) {
            if (!event.target.closest('#user-search-input') && !event.target.closest('#user-search-results')) {
                resultsDiv.style.display = 'none';
            }
        });
        function addUserToSelectedList(userId, username) {
            let container = document.getElementById('selected-users-container');
            let filterBtn = document.getElementById('btn-filter-users');

            let tag = document.createElement('span');
            tag.className = 'selected-user-tag';
            tag.dataset.userId = userId;
            tag.textContent = username;

            let removeBtn = document.createElement('button');
            removeBtn.className = 'remove-btn';
            removeBtn.innerHTML = '&times;';
            removeBtn.onclick = function () {
                selectedUsers = selectedUsers.filter(id => id !== userId);
                container.removeChild(tag);
                if (selectedUsers.length === 0) {
                    filterBtn.style.display = 'none';
                }
            };

            tag.appendChild(removeBtn);
            container.appendChild(tag);
            filterBtn.style.display = 'block';
        }
    }

    function setupQuestionSearch() {
        let searchInput = document.getElementById('question-search-input');
        let resultsDiv = document.getElementById('question-search-results');
        let currentFocus = -1;

        if (!searchInput || !resultsDiv) return;

        searchInput.addEventListener('input', function () {
            let q = this.value.trim().toLowerCase();
            resultsDiv.innerHTML = '';
            currentFocus = -1;

            if (!q) return;

            // Filter nodes by question text
            let matches = nodesData.filter(n => n.label.toLowerCase().includes(q)).slice(0, 10);

            if (matches.length) {
                matches.forEach(n => {
                    let div = document.createElement('div');
                    div.className = 'list-group-item list-group-item-action';
                    div.textContent = n.label;
                    div.style.cursor = 'pointer';
                    div.onclick = function () {
                        highlightAndZoomToNode(n);
                        searchInput.value = '';
                        resultsDiv.innerHTML = '';
                    };
                    resultsDiv.appendChild(div);
                });
            } else {
                let div = document.createElement('div');
                div.className = 'list-group-item text-muted';
                div.textContent = 'Sonuç bulunamadı';
                resultsDiv.appendChild(div);
            }
        });

        // Keyboard navigation
        searchInput.addEventListener('keydown', function(e) {
            let items = resultsDiv.querySelectorAll('.list-group-item-action');

            if (e.keyCode === 40) {
                // Arrow Down
                e.preventDefault();
                currentFocus++;
                if (currentFocus >= items.length) currentFocus = 0;
                highlightQuestionItem(items, currentFocus);
            }
            else if (e.keyCode === 38) {
                // Arrow Up
                e.preventDefault();
                currentFocus--;
                if (currentFocus < 0) currentFocus = items.length - 1;
                highlightQuestionItem(items, currentFocus);
            }
            else if (e.keyCode === 13) {
                // Enter
                e.preventDefault();
                if (currentFocus > -1 && currentFocus < items.length) {
                    items[currentFocus].click();
                }
            }
        });

        function highlightQuestionItem(items, index) {
            // Remove active class from all items
            for (let i = 0; i < items.length; i++) {
                items[i].classList.remove('active');
            }
            // Add active class to current item
            if (index >= 0 && index < items.length) {
                items[index].classList.add('active');
            }
        }
    }

    function setupHashtagSearch() {
        let searchInput = document.getElementById('hashtag-search-input');
        let resultsDiv = document.getElementById('hashtag-search-results');
        let currentFocus = -1;
        let currentHashtags = [];

        if (!searchInput || !resultsDiv) return;

        searchInput.addEventListener('input', function () {
            let q = this.value.trim().replace('#', '').toLowerCase();
            resultsDiv.innerHTML = '';
            currentFocus = -1;
            currentHashtags = [];

            if (!q) return;

            // Fetch hashtags from API
            fetch('/hashtags/search/?q=' + encodeURIComponent(q))
                .then(r => r.json())
                .then(data => {
                    if (data.hashtags && data.hashtags.length) {
                        currentHashtags = data.hashtags;
                        data.hashtags.forEach(h => {
                            let div = document.createElement('div');
                            div.className = 'list-group-item list-group-item-action d-flex justify-content-between';
                            div.style.cursor = 'pointer';

                            let nameSpan = document.createElement('span');
                            nameSpan.textContent = '#' + h.name;

                            let countBadge = document.createElement('span');
                            countBadge.className = 'badge bg-primary';
                            countBadge.textContent = h.usage_count;

                            div.appendChild(nameSpan);
                            div.appendChild(countBadge);

                            div.onclick = function () {
                                filterByHashtag(h.name);
                                searchInput.value = '';
                                resultsDiv.innerHTML = '';
                            };

                            resultsDiv.appendChild(div);
                        });
                    } else {
                        let div = document.createElement('div');
                        div.className = 'list-group-item text-muted';
                        div.textContent = 'Etiket bulunamadı';
                        resultsDiv.appendChild(div);
                    }
                });
        });

        // Keyboard navigation
        searchInput.addEventListener('keydown', function(e) {
            let items = resultsDiv.querySelectorAll('.list-group-item-action');

            if (e.keyCode === 40) {
                // Arrow Down
                e.preventDefault();
                currentFocus++;
                if (currentFocus >= items.length) currentFocus = 0;
                highlightHashtagItem(items, currentFocus);
            }
            else if (e.keyCode === 38) {
                // Arrow Up
                e.preventDefault();
                currentFocus--;
                if (currentFocus < 0) currentFocus = items.length - 1;
                highlightHashtagItem(items, currentFocus);
            }
            else if (e.keyCode === 13) {
                // Enter
                e.preventDefault();
                if (currentFocus > -1 && currentFocus < items.length && currentHashtags[currentFocus]) {
                    filterByHashtag(currentHashtags[currentFocus].name);
                    searchInput.value = '';
                    resultsDiv.innerHTML = '';
                }
            }
        });

        function highlightHashtagItem(items, index) {
            // Remove active class from all items
            for (let i = 0; i < items.length; i++) {
                items[i].classList.remove('active');
            }
            // Add active class to current item
            if (index >= 0 && index < items.length) {
                items[index].classList.add('active');
            }
        }
    }

    function highlightAndZoomToNode(targetNode) {
        if (!node || !svg) {
            console.error('Graph not initialized yet');
            return;
        }

        // Remove previous highlights
        node.classed('highlighted-node', false);

        // Highlight target node
        node.each(function (d) {
            if (d.id === targetNode.id) {
                d3.select(this).classed('highlighted-node', true);
            }
        });

        // Stop simulation immediately to speed up navigation
        if (simulation) {
            simulation.stop();
        }

        // Force immediate position update if node doesn't have position
        if (typeof targetNode.x !== 'number' || typeof targetNode.y !== 'number') {
            targetNode.x = width / 2;
            targetNode.y = height / 2;
        }

        // Zoom to node immediately
        zoomToNode(targetNode);

        // Remove highlight after 3 seconds
        setTimeout(() => {
            if (node) {
                node.classed('highlighted-node', false);
            }
        }, 3000);
    }

    function filterByHashtag(hashtagName) {
        // Filter the map by hashtag
        fetchData('/map-data/?hashtag=' + encodeURIComponent(hashtagName), updateGraphFromData);
    }

    function updateGraphFromData(data) {
        nodesData = data.nodes;
        linksData = data.links;
        applyLinkBasedSizing();
        updateGraph();
        updateStatistics();
    }

    function applyLinkBasedSizing() {
        const linkCounts = {};
        linksData.forEach(link => {
            const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
            const targetId = typeof link.target === 'object' ? link.target.id : link.target;
            if (sourceId) linkCounts[sourceId] = (linkCounts[sourceId] || 0) + 1;
            if (targetId) linkCounts[targetId] = (linkCounts[targetId] || 0) + 1;
        });
        nodesData.forEach(node => {
            const linkUserIds = Array.isArray(node.link_user_ids) ? node.link_user_ids : [];
            const linkUsers = Array.isArray(node.link_users) ? node.link_users : [];
            const linkerCount = linkUserIds.length || linkUsers.length || (linkCounts[node.id] || 0);
            node.size = BASE_NODE_SIZE + Math.max(0, linkerCount - 1) * LINK_SIZE_STEP;
        });
    }

    function updateStatistics() {
        // Count total nodes and links
        const totalNodes = nodesData.length;
        const totalLinks = linksData.length;

        // Count unique users
        const uniqueUsers = new Set();
        nodesData.forEach(node => {
            if (node.user_ids && Array.isArray(node.user_ids)) {
                node.user_ids.forEach(uid => uniqueUsers.add(uid));
            }
        });
        const totalUsers = uniqueUsers.size;

        // Update DOM
        document.getElementById('stat-total-nodes').textContent = totalNodes;
        document.getElementById('stat-total-links').textContent = totalLinks;
        document.getElementById('stat-total-users').textContent = totalUsers;
    }

    function createGraph() {
        // Update size dynamically based on current chart container size
        const chartEl = document.getElementById('chart');
        width = chartEl.clientWidth;
        height = chartEl.clientHeight || height;

        // Get current theme colors from CSS variables
        const rootStyles = getComputedStyle(document.documentElement);
        let backgroundColor = rootStyles.getPropertyValue('--content-background-color').trim() || '#fafafa';
        const bgColor = rootStyles.getPropertyValue('--background-color').trim();

        // Smart fallback: Eğer content-background beyazsa ama background-color koyuysa, background-color'ı kullan
        // Bu, eski profil ayarlarıyla uyumluluk için
        if (isLightColor(backgroundColor) && !isLightColor(bgColor)) {
            backgroundColor = bgColor;
        }

        function isLightColor(color) {
            // Hex rengi RGB'ye çevir ve parlaklığı hesapla
            if (!color || color === '') return true;
            const hex = color.replace('#', '');
            const r = parseInt(hex.substr(0, 2), 16);
            const g = parseInt(hex.substr(2, 2), 16);
            const b = parseInt(hex.substr(4, 2), 16);
            // Relative luminance formula
            const brightness = (r * 299 + g * 587 + b * 114) / 1000;
            return brightness > 155; // 155+ açık renk sayılır
        }

        d3.select("#chart").selectAll("*").remove();
        svg = d3.select("#chart").append("svg")
            .attr("width", width).attr("height", height)
            .style("background", backgroundColor);

        g = svg.append("g");
        userLabelGroup = g.append("g").attr("class", "user-labels");

        // Zoom
        zoom = d3.zoom()
            .scaleExtent([0.05, 5])
            .on("zoom", function (event) {
                g.attr("transform", event.transform);
                updateNodeVisibility(event.transform.k);
            });
        svg.call(zoom);

        // Çizgiler
        link = g.append("g").attr("class", "links")
            .selectAll("line").data(linksData).enter().append("line")
            .attr("stroke-width", 2).attr("stroke", "#999");

        // Ortada oklar için paths
        arrows = g.append("g").attr("class", "mid-arrows")
            .selectAll("path")
            .data(linksData)
            .enter().append("path")
            .attr("fill", "#999")
            .attr("stroke", "none");

        // Düğümler
        node = g.append("g").attr("class", "nodes")
            .selectAll("circle").data(nodesData).enter().append("circle")
            .attr("r", d => d.size).attr("fill", d => d.color)
            .style("cursor", "pointer")
            .on("click", function (event, d) {
                event.stopPropagation();
                showNodeUserLabels(event, d);
            })
            .call(d3.drag()
                .on("start", dragstarted).on("drag", dragged).on("end", dragended)
            );

        // Başlık etiketleri - fallback ile
        let textColor = rootStyles.getPropertyValue('--text-color').trim() || '#222';
        // Eğer background koyu ama text açıksa, text color'ı kullan
        if (!isLightColor(backgroundColor) && isLightColor(textColor)) {
            // Koyu arka plan, açık metin - doğru kombinasyon, değiştirme
        } else if (!isLightColor(backgroundColor) && !isLightColor(textColor)) {
            // Koyu arka plan, koyu metin - yanlış! Açık renge çevir
            textColor = '#e5e5e5';
        }

        label = g.append("g").attr("class", "labels")
            .selectAll("text").data(nodesData).enter().append("text")
            .attr("dy", -10)
            .attr("text-anchor", "middle")
            .text(d => d.label)
            .style("font-size", d => (LABEL_BASE_SIZE + Math.max(0, d.size - BASE_NODE_SIZE) * 0.5) + "px")
            .style("fill", textColor);

        // Force simulation
        simulation = d3.forceSimulation(nodesData)
            .force("link", d3.forceLink(linksData)
                .id(d => d.id)
                .distance(150)
            )
            .force("charge", d3.forceManyBody().strength(-200))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collide", d3.forceCollide().radius(d => d.size * 1.3));

        // Update SVG dimensions
        svg.attr("width", width).attr("height", height);

        // Sadece bir kez odaklama yapmak için
        let zoomed = false;
        simulation.on("tick", function() {
            ticked();
            if (!zoomed && focusQuestionId && simulation.alpha() < 0.03) {
                let node = nodesData.find(n => String(n.question_id) === String(focusQuestionId));
                if (node && typeof node.x === "number" && typeof node.y === "number") {
                    zoomToNode(node);
                    zoomed = true;
                }
            }
        });

        updateNodeVisibility(1);

        svg.on("click", function () {
            if (userLabelGroup) userLabelGroup.selectAll("*").remove();
        });
    }

    // Kart şeklinde kutu üstünde göster!
    function showNodeUserLabels(event, d) {
        userLabelGroup.selectAll("*").remove();

        // Get theme colors with smart fallback
        const rootStyles = getComputedStyle(document.documentElement);
        let cardBgColor = rootStyles.getPropertyValue('--content-background-color').trim() || '#fff';
        let cardTextColor = rootStyles.getPropertyValue('--text-color').trim() || '#24264b';
        const borderColor = rootStyles.getPropertyValue('--header-background-color').trim() || '#4682ea';
        const bgColor = rootStyles.getPropertyValue('--background-color').trim();

        // Helper function
        function isLightColor(color) {
            if (!color || color === '') return true;
            const hex = color.replace('#', '');
            const r = parseInt(hex.substr(0, 2), 16);
            const g = parseInt(hex.substr(2, 2), 16);
            const b = parseInt(hex.substr(4, 2), 16);
            const brightness = (r * 299 + g * 587 + b * 114) / 1000;
            return brightness > 155;
        }

        // Fallback: Eğer content-background beyazsa ama background-color koyuysa
        if (isLightColor(cardBgColor) && !isLightColor(bgColor)) {
            cardBgColor = bgColor;
        }

        // Text color fallback: Koyu arka plan + koyu metin = yanlış!
        if (!isLightColor(cardBgColor) && !isLightColor(cardTextColor)) {
            cardTextColor = '#e5e5e5';
        }

        // Kutu ayarları
        const allUsers = Array.isArray(d.users) ? d.users : [];
        const linkUsers = Array.isArray(d.link_users) ? d.link_users : [];
        const displayTitle = linkUsers.length ? 'Bağlayanlar' : 'Girdiler';
        let displayUsers = linkUsers.length ? linkUsers : allUsers;
        const displayCount = displayUsers.length;

        const maxUsersShown = 12;
        const maxPerRow = 3;
        const userBoxWidth = 120, userBoxHeight = 34, userBoxPadding = 12;
        const rowGap = 12;
        const minCardWidth = 280;
        const headerHeight = 52;
        const btnH = 38;

        if (displayUsers.length === 0) {
            displayUsers = [{ username: 'Girdi yok', isPlaceholder: true }];
        }

        let shownUsers = displayUsers.slice(0, maxUsersShown);
        let hiddenCount = displayUsers.length - shownUsers.length;

        // Satırlara böl
        let userRows = [];
        for (let i = 0; i < shownUsers.length; i += maxPerRow) {
            userRows.push(shownUsers.slice(i, i + maxPerRow));
        }
        if (hiddenCount > 0) {
            if (userRows.length === 0 || userRows[userRows.length-1].length === maxPerRow) {
                userRows.push([]);
            }
            userRows[userRows.length-1].push({username: `…ve ${hiddenCount} kişi daha`, isMore: true});
        }

        let rowCount = userRows.length;
        let maxRowLen = userRows.reduce((max, row) => Math.max(max, row.length), 1);
        let rowW = Math.max(
            minCardWidth,
            Math.min(maxPerRow, maxRowLen) * (userBoxWidth + userBoxPadding) - userBoxPadding
        );
        let cardWidth = rowW;
        let cardHeight = headerHeight + rowCount * (userBoxHeight + rowGap) + btnH + 24;

        // Kartı node'un üstünde ortala
        let nodeX = d.x, nodeY = d.y - d.size - 22;
        let cardLeft = nodeX - cardWidth / 2;
        let cardTop = nodeY - cardHeight;

        // Kart grubu
        let card = userLabelGroup.append("g")
            .attr("class", "user-card")
            .attr("transform", `translate(${cardLeft},${cardTop})`);

        // Gölge
        card.append("rect")
            .attr("x", 7).attr("y", 7)
            .attr("rx", 18).attr("ry", 18)
            .attr("width", cardWidth).attr("height", cardHeight)
            .attr("fill", "#1c2c5820")
            .attr("opacity", 0.12);

        // Kutu
        card.append("rect")
            .attr("x", 0).attr("y", 0)
            .attr("rx", 16).attr("ry", 16)
            .attr("width", cardWidth).attr("height", cardHeight)
            .attr("fill", cardBgColor)
            .attr("stroke", borderColor)
            .attr("stroke-width", 1.3);

        // Baslik
        const headerText = `${displayTitle} (${displayCount})`;
        card.append("text")
            .attr("x", cardWidth/2)
            .attr("y", 30)
            .attr("text-anchor", "middle")
            .attr("font-size", "16px")
            .attr("font-weight", "700")
            .attr("fill", cardTextColor)
            .text(headerText);

        card.append("line")
            .attr("x1", 18)
            .attr("x2", cardWidth - 18)
            .attr("y1", 40)
            .attr("y2", 40)
            .attr("stroke", borderColor)
            .attr("stroke-opacity", 0.35);

        function formatUsername(name, maxLen) {
            if (name.length <= maxLen) return name;
            return name.slice(0, maxLen - 3) + '...';
        }

        // Kullanıcı etiketleri
        userRows.forEach((row, rowIdx) => {
            row.forEach((user, colIdx) => {
                let totalUsersInRow = row.length;
                let totalRowWidth = totalUsersInRow * (userBoxWidth + userBoxPadding) - userBoxPadding;
                let startX = (cardWidth - totalRowWidth) / 2;

                let x = startX + colIdx * (userBoxWidth + userBoxPadding);
                let y = headerHeight + rowIdx * (userBoxHeight + rowGap);

                let isClickable = !user.isMore && !user.isPlaceholder && user.answer_id;
                let g = card.append("g")
                    .style("cursor", isClickable || user.isMore ? "pointer" : "default")
                    .on("click", function (event) {
                        if (!isClickable && !user.isMore) return;
                        event.stopPropagation();
                        if (user.isMore) {
                            window.location.href = `/${d.slug}/`;
                        } else if (user.answer_id) {
                            window.location.href = `/${d.slug}/answer/${user.answer_id}/`;
                        } else {
                            showToast('Bu kullanıcının bu başlıkta entrysi yok.', 'warning');
                        }
                    });

                // Kutu
                g.append("rect")
                    .attr("x", x)
                    .attr("y", y)
                    .attr("rx", 10).attr("ry", 10)
                    .attr("width", userBoxWidth)
                    .attr("height", userBoxHeight)
                    .attr("fill", user.isMore || user.isPlaceholder ? "#f1f1f1" : "#e7edfa")
                    .attr("stroke", "#4682ea")
                    .attr("stroke-width", 1.1);

                const displayName = user.isMore
                    ? user.username
                    : user.isPlaceholder
                        ? user.username
                        : ("@" + formatUsername(user.username, 14));

                g.append("text")
                    .attr("x", x + userBoxWidth/2)
                    .attr("y", y + 22)
                    .attr("text-anchor", "middle")
                    .attr("fill", user.isMore || user.isPlaceholder ? "#7a7a7a" : "#3554ad")
                    .attr("font-size", "15px")
                    .attr("font-weight", user.isMore || user.isPlaceholder ? "500" : "700")
                    .text(displayName);
            });
        });

        // Başlığa git butonu
        let btnX = cardWidth/2 - 60, btnY = cardHeight - btnH - 12;
        let group = card.append("g")
            .attr("class", "to-title-label")
            .style("cursor", "pointer")
            .on("click", function (event) {
                event.stopPropagation();
                window.location.href = `/${d.slug}/`;
            });
        group.append("rect")
            .attr("x", btnX).attr("y", btnY)
            .attr("width", 120).attr("height", btnH)
            .attr("rx", 12).attr("fill", "#f9fbff")
            .attr("stroke", "#4682ea").attr("stroke-width", 1.4)
            .attr("opacity", 0.99)
            .attr("filter", null);
        group.append("text")
            .attr("x", btnX + 60).attr("y", btnY + 24)
            .attr("text-anchor", "middle").attr("fill", "#2554A3")
            .attr("font-size", "15px").attr("font-weight", "600").text("Başlığa git");
    }

    function ticked() {
        // Kenar çizgileri
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        // Ortada ok çizimi
        arrows.attr("d", function (d) {
            let x1 = d.source.x, y1 = d.source.y;
            let x2 = d.target.x, y2 = d.target.y;
            let mx = (x1 + x2) / 2;
            let my = (y1 + y2) / 2;
            let dx = x2 - x1, dy = y2 - y1;
            let angle = Math.atan2(dy, dx);
            let arrowLength = 24, arrowWidth = 10;
            let tipX = mx + Math.cos(angle) * (arrowLength / 2);
            let tipY = my + Math.sin(angle) * (arrowLength / 2);
            let baseX = mx - Math.cos(angle) * (arrowLength / 2);
            let baseY = my - Math.sin(angle) * (arrowLength / 2);
            let leftX = baseX + Math.cos(angle + Math.PI/2) * (arrowWidth/2);
            let leftY = baseY + Math.sin(angle + Math.PI/2) * (arrowWidth/2);
            let rightX = baseX + Math.cos(angle - Math.PI/2) * (arrowWidth/2);
            let rightY = baseY + Math.sin(angle - Math.PI/2) * (arrowWidth/2);
            return `M${leftX},${leftY} L${tipX},${tipY} L${rightX},${rightY} Z`;
        });

        // Düğümler ve etiketler
        node.attr("cx", d => d.x).attr("cy", d => d.y);
        label.attr("x", d => d.x).attr("y", d => d.y - d.size - 5);
    }

    function updateNodeVisibility(zoomLevel) {
        node.each(function (d) {
            let minOpacity = 0.8, maxOpacity = 0.95;
            let maxSize = d3.max(nodesData, d => d.size) || BASE_NODE_SIZE;
            let sizeFactor = (d.size - BASE_NODE_SIZE) / (maxSize - BASE_NODE_SIZE || 1);
            let opacity = minOpacity + (maxOpacity - minOpacity) * sizeFactor;
            if (zoomLevel < 0.5) opacity = opacity * zoomLevel * 2;
            d3.select(this).style("opacity", opacity);
        });
        label.style("opacity", d => 1);
        label.style("font-size", d => (LABEL_BASE_SIZE + Math.max(0, d.size - BASE_NODE_SIZE) * 0.5) * zoomLevel + "px");
    }

    function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x; d.fy = d.y;
    }
    function dragged(event, d) {
        d.fx = event.x; d.fy = event.y;
    }
    function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null; d.fy = null;
    }
    function zoomToNode(node) {
        let scale = 1.5;
        let x = -node.x * scale + width / 2;
        let y = -node.y * scale + height / 2;
        svg.transition()
            .duration(750)
            .call(zoom.transform, d3.zoomIdentity.translate(x, y).scale(scale));
    }
    function updateGraph() {
        createGraph();
        updateStatistics();
    }

    // Export functionality
    document.getElementById('export-svg-btn')?.addEventListener('click', function() {
        exportSVG();
    });

    document.getElementById('export-png-btn')?.addEventListener('click', function() {
        exportPNG();
    });

    // Handle window resize events (including sidebar toggle)
    let resizeTimeout;
    window.addEventListener('resize', function() {
        // Clear previous timeout
        clearTimeout(resizeTimeout);

        // Wait for CSS transition to complete (300ms) before updating
        resizeTimeout = setTimeout(function() {
            const chartEl = document.getElementById('chart');
            const newWidth = chartEl.clientWidth;
            const newHeight = chartEl.clientHeight || height;
            const widthChanged = Math.abs(newWidth - width) > 10;
            const heightChanged = Math.abs(newHeight - height) > 10;

            if (widthChanged || heightChanged) {
                width = newWidth;
                height = newHeight;

                // Update SVG dimensions
                if (svg) {
                    svg.attr("width", width).attr("height", height);
                }

                // Update force center and restart simulation
                if (simulation) {
                    simulation.force("center", d3.forceCenter(width / 2, height / 2));
                    simulation.alpha(0.3).restart();
                }
            }
        }, 350); // Wait slightly longer than CSS transition (300ms)
    });

    function exportSVG() {
        const svgElement = d3.select("#chart svg").node();
        if (!svgElement) {
            showToast('Harita henüz yüklenmedi!', 'warning');
            return;
        }

        // Clone SVG to avoid affecting the original
        const clonedSvg = svgElement.cloneNode(true);

        // Set proper SVG attributes
        clonedSvg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
        clonedSvg.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink');

        // Serialize SVG
        const serializer = new XMLSerializer();
        const svgString = serializer.serializeToString(clonedSvg);

        // Create download link
        const blob = new Blob([svgString], { type: 'image/svg+xml' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'soru_haritasi.svg';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }

    function exportPNG() {
        const svgElement = d3.select("#chart svg").node();
        if (!svgElement) {
            showToast('Harita henüz yüklenmedi!', 'warning');
            return;
        }

        // Ask user for resolution scale
        const scaleInput = prompt(
            'Çözünürlük seçin (daha yüksek değerler daha net ama daha büyük dosya):\n\n' +
            '1 = Normal (varsayılan)\n' +
            '2 = Yüksek (önerilen)\n' +
            '3 = Çok Yüksek\n' +
            '4 = Ultra Yüksek (çok fazla node için)',
            '2'
        );

        if (!scaleInput) {
            return; // User cancelled
        }

        const scale = parseFloat(scaleInput);
        if (isNaN(scale) || scale < 1 || scale > 4) {
            showToast('Geçersiz değer! 1-4 arası bir sayı girin.', 'error');
            return;
        }

        // Get SVG dimensions
        const bbox = svgElement.getBBox();
        const baseWidth = Math.max(bbox.width + Math.abs(bbox.x), 800) + 100; // Add padding
        const baseHeight = Math.max(bbox.height + Math.abs(bbox.y), 600) + 100; // Add padding

        // Apply resolution multiplier
        const canvasWidth = baseWidth * scale;
        const canvasHeight = baseHeight * scale;

        // Clone and serialize SVG
        const clonedSvg = svgElement.cloneNode(true);
        clonedSvg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
        clonedSvg.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink');
        clonedSvg.setAttribute('width', baseWidth);
        clonedSvg.setAttribute('height', baseHeight);

        const serializer = new XMLSerializer();
        const svgString = serializer.serializeToString(clonedSvg);

        // Create canvas with high resolution
        const canvas = document.createElement('canvas');
        canvas.width = canvasWidth;
        canvas.height = canvasHeight;
        const ctx = canvas.getContext('2d');

        // Create image from SVG
        const img = new Image();
        const svgBlob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
        const url = URL.createObjectURL(svgBlob);

        img.onload = function() {
            // Draw background with theme color (with fallback)
            const rootStyles = getComputedStyle(document.documentElement);
            let backgroundColor = rootStyles.getPropertyValue('--content-background-color').trim() || '#fafafa';
            const bgColor = rootStyles.getPropertyValue('--background-color').trim();

            // Helper function
            function isLightColor(color) {
                if (!color || color === '') return true;
                const hex = color.replace('#', '');
                const r = parseInt(hex.substr(0, 2), 16);
                const g = parseInt(hex.substr(2, 2), 16);
                const b = parseInt(hex.substr(4, 2), 16);
                const brightness = (r * 299 + g * 587 + b * 114) / 1000;
                return brightness > 155;
            }

            // Fallback: Eğer content-background beyazsa ama background-color koyuysa
            if (isLightColor(backgroundColor) && !isLightColor(bgColor)) {
                backgroundColor = bgColor;
            }

            ctx.fillStyle = backgroundColor;
            ctx.fillRect(0, 0, canvasWidth, canvasHeight);

            // Scale context for high resolution rendering
            ctx.scale(scale, scale);

            // Draw SVG
            ctx.drawImage(img, 0, 0, baseWidth, baseHeight);

            // Convert to PNG and download
            canvas.toBlob(function(blob) {
                const pngUrl = URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = pngUrl;
                link.download = `soru_haritasi_${scale}x.png`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(pngUrl);
                URL.revokeObjectURL(url);
            });
        };

        img.onerror = function() {
            showToast('PNG oluşturulurken hata oluştu. Lütfen tekrar deneyin.', 'error');
            URL.revokeObjectURL(url);
        };

        img.src = url;
    }
});
