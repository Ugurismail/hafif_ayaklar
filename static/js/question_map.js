// static/js/question_map.js

document.addEventListener('DOMContentLoaded', function () {
    var width = document.getElementById('chart').clientWidth;
    var height = 800;
    var svg, g, zoom, simulation, link, node, label, userLabelGroup, arrows;
    var nodesData = [], linksData = [], selectedUsers = [];
    var focusQuestionId = window.focusQuestionId || null;

    setupButtons();
    setupUserSearch();
    setupQuestionSearch();
    setupHashtagSearch();

    fetchData('/map-data/', function (data) {
        nodesData = data.nodes;
        linksData = data.links;
        createGraph();
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

        if (!searchInput) return;

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

        if (!searchInput) return;

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
        if (!searchInput) return;

        searchInput.addEventListener('input', function () {
            let q = this.value.trim().replace('#', '').toLowerCase();
            resultsDiv.innerHTML = '';

            if (!q) return;

            // Fetch hashtags from API
            fetch('/hashtags/search/?q=' + encodeURIComponent(q))
                .then(r => r.json())
                .then(data => {
                    if (data.hashtags && data.hashtags.length) {
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
                        div.textContent = 'Hashtag bulunamadı';
                        resultsDiv.appendChild(div);
                    }
                });
        });
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

        // Zoom to node
        if (typeof targetNode.x === 'number' && typeof targetNode.y === 'number') {
            zoomToNode(targetNode);
        } else {
            // If node doesn't have position yet, wait for simulation to settle
            let checkInterval = setInterval(() => {
                if (typeof targetNode.x === 'number' && typeof targetNode.y === 'number') {
                    clearInterval(checkInterval);
                    zoomToNode(targetNode);
                }
            }, 100);
            setTimeout(() => clearInterval(checkInterval), 2000); // timeout after 2s
        }

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
        updateGraph();
    }

    function createGraph() {
        d3.select("#chart").selectAll("*").remove();
        svg = d3.select("#chart").append("svg")
            .attr("width", width).attr("height", height)
            .style("background", "#fafafa");

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

        // Başlık etiketleri
        label = g.append("g").attr("class", "labels")
            .selectAll("text").data(nodesData).enter().append("text")
            .attr("dy", -10)
            .attr("text-anchor", "middle")
            .text(d => d.label)
            .style("font-size", d => (12 + d.users.length * 2) + "px")
            .style("fill", "#222");

        // Force simulation
        simulation = d3.forceSimulation(nodesData)
            .force("link", d3.forceLink(linksData)
                .id(d => d.id)
                .distance(150)
            )
            .force("charge", d3.forceManyBody().strength(-200))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collide", d3.forceCollide().radius(d => d.size * 1.3));

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

        // Kutu ayarları
        const users = d.users;
        const maxUsersShown = 12;
        const maxPerRow = 4;
        const userBoxWidth = 92, userBoxHeight = 32, userBoxPadding = 10;
        const rowGap = 10;
        const minCardWidth = 250;
        const headerHeight = 35;
        const btnH = 36;

        let shownUsers = users.slice(0, maxUsersShown);
        let hiddenCount = users.length - shownUsers.length;

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
        let rowW = Math.max(minCardWidth, Math.min(maxPerRow, userRows[0].length) * (userBoxWidth + userBoxPadding));
        let cardWidth = rowW;
        let cardHeight = headerHeight + rowCount * (userBoxHeight + rowGap) + btnH + 20;

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
            .attr("rx", 19).attr("ry", 19)
            .attr("width", cardWidth).attr("height", cardHeight)
            .attr("fill", "#1c2c5820")
            .attr("opacity", 0.14);

        // Kutu
        card.append("rect")
            .attr("x", 0).attr("y", 0)
            .attr("rx", 17).attr("ry", 17)
            .attr("width", cardWidth).attr("height", cardHeight)
            .attr("fill", "#fff")
            .attr("stroke", "#4682ea")
            .attr("stroke-width", 1.5);

        // Başlık
        card.append("text")
            .attr("x", cardWidth/2)
            .attr("y", 28)
            .attr("text-anchor", "middle")
            .attr("font-size", "24px")
            .attr("font-weight", "bold")
            .attr("fill", "#24264b");

        // Kullanıcı etiketleri
        userRows.forEach((row, rowIdx) => {
            row.forEach((user, colIdx) => {
                let totalUsersInRow = row.length;
                let totalRowWidth = totalUsersInRow * (userBoxWidth + userBoxPadding) - userBoxPadding;
                let startX = (cardWidth - totalRowWidth) / 2;

                let x = startX + colIdx * (userBoxWidth + userBoxPadding);
                let y = headerHeight + rowIdx * (userBoxHeight + rowGap);

                let g = card.append("g")
                    .style("cursor", "pointer")
                    .on("click", function (event) {
                        event.stopPropagation();
                        if (user.isMore) {
                            window.location.href = `/question/${d.question_id}/`;
                        } else {
                            window.location.href = `/question/${d.question_id}/answer/${user.answer_id}/`;
                        }
                    });

                // Kutu
                g.append("rect")
                    .attr("x", x)
                    .attr("y", y)
                    .attr("rx", 8).attr("ry", 8)
                    .attr("width", userBoxWidth)
                    .attr("height", userBoxHeight)
                    .attr("fill", user.isMore ? "#eee" : "#e7edfa")
                    .attr("stroke", "#4682ea")
                    .attr("stroke-width", 1.1);

                g.append("text")
                    .attr("x", x + userBoxWidth/2)
                    .attr("y", y + 21)
                    .attr("text-anchor", "middle")
                    .attr("fill", user.isMore ? "#7a7a7a" : "#3554ad")
                    .attr("font-size", "17px")
                    .attr("font-weight", user.isMore ? "500" : "bold")
                    .text(user.isMore ? user.username : ("@" + user.username));
            });
        });

        // Başlığa git butonu
        let btnX = cardWidth/2 - 55, btnY = cardHeight - btnH - 10;
        let group = card.append("g")
            .attr("class", "to-title-label")
            .style("cursor", "pointer")
            .on("click", function (event) {
                event.stopPropagation();
                window.location.href = `/question/${d.question_id}/`;
            });
        group.append("rect")
            .attr("x", btnX).attr("y", btnY)
            .attr("width", 110).attr("height", btnH)
            .attr("rx", 11).attr("fill", "#f9fbff")
            .attr("stroke", "#4682ea").attr("stroke-width", 1.4)
            .attr("opacity", 0.99)
            .attr("filter", null);
        group.append("text")
            .attr("x", btnX + 55).attr("y", btnY + 24)
            .attr("text-anchor", "middle").attr("fill", "#2554A3")
            .attr("font-size", "17px").attr("font-weight", "500").text("Başlığa git");
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
            let userCountFactor = (d.users.length - 1) / (d3.max(nodesData, d => d.users.length) - 1 || 1);
            let opacity = minOpacity + (maxOpacity - minOpacity) * userCountFactor;
            if (zoomLevel < 0.5) opacity = opacity * zoomLevel * 2;
            d3.select(this).style("opacity", opacity);
        });
        label.style("opacity", d => 1);
        label.style("font-size", d => (12 + d.users.length * 2) * zoomLevel + "px");
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
    }
});
