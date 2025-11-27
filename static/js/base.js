/* base.js */

/**
 * Show a toast notification
 * @param {string} message - The message to display
 * @param {string} type - Type of toast: 'success', 'error', 'warning', 'info'
 * @param {number} duration - Duration in ms before auto-hide (default: 4000)
 */
function showToast(message, type = 'info', duration = 4000) {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    // Create unique ID for this toast
    const toastId = 'toast-' + Date.now();

    // Determine icon and color based on type
    let icon, bgClass, textClass;
    switch(type) {
        case 'success':
            icon = 'bi-check-circle-fill';
            bgClass = 'bg-success';
            textClass = 'text-white';
            break;
        case 'error':
            icon = 'bi-x-circle-fill';
            bgClass = 'bg-danger';
            textClass = 'text-white';
            break;
        case 'warning':
            icon = 'bi-exclamation-triangle-fill';
            bgClass = 'bg-warning';
            textClass = 'text-dark';
            break;
        case 'info':
        default:
            icon = 'bi-info-circle-fill';
            bgClass = 'bg-info';
            textClass = 'text-white';
    }

    // Create toast element
    const toastHtml = `
        <div id="${toastId}" class="toast align-items-center ${bgClass} ${textClass} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi ${icon} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;

    // Append to container
    container.insertAdjacentHTML('beforeend', toastHtml);

    // Get the toast element and show it
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: duration
    });

    // Remove from DOM after hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });

    toast.show();
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
}

/**
 * Arama sonuçlarını global bir değişkende tutacağız,
 * böylece Enter'a basıldığında bakabiliriz.
 */
let lastSearchResults = [];
let currentSearchQuery = '';
let currentSearchOffset = 0;
let hasMoreResults = false;
let isLoadingMore = false;
let searchTimeout = null; // Debounce için

document.addEventListener('DOMContentLoaded', function() {
    var searchInput = document.getElementById('search-input');
    var searchResults = document.getElementById('search-results');

    // Eğer search elementleri yoksa (signup sayfası gibi), bu kodu çalıştırma
    if (!searchInput || !searchResults) {
        return;
    }

    var query = '';
    var currentFocus = -1;  // Ok tuşlarıyla hangi item seçili

    function loadSearchResults(isLoadMore = false) {
        const q = currentSearchQuery;
        const offset = isLoadMore ? currentSearchOffset : 0;

        if (!isLoadMore) {
            currentSearchOffset = 0;
            lastSearchResults = [];
        }

        isLoadingMore = true;

        fetch('/search_suggestions/?q=' + encodeURIComponent(q) + '&offset=' + offset + '&limit=20', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            isLoadingMore = false;

            // Gelen sonuçları ekle
            data.suggestions.forEach(function(item) {
                lastSearchResults.push(item);

                var div = document.createElement('div');
                div.classList.add('list-group-item');

                div.textContent = item.label;
                div.dataset.type = item.type;
                div.dataset.url = item.url; // Store full URL for all types
                if (item.type === 'question') {
                    // URL'den slug'ı çıkar (örn: /slug/ -> slug)
                    const slug = item.url.split('/').filter(s => s).pop();
                    div.dataset.slug = slug;
                } else if (item.type === 'user') {
                    // URL'den username'i çıkar (örn: /profile/username/ -> username)
                    const username = item.url.split('/').filter(s => s).pop();
                    div.dataset.username = username;
                } else if (item.type === 'hashtag') {
                    // For hashtag, just use the full URL
                    // No need to extract, we'll use dataset.url
                }
                searchResults.appendChild(div);
            });

            // "Daha Fazla Göster" butonunu güncelle veya ekle
            hasMoreResults = data.has_more;
            let loadMoreBtn = document.getElementById('load-more-search-btn');

            if (hasMoreResults) {
                currentSearchOffset = data.next_offset;

                if (!loadMoreBtn) {
                    loadMoreBtn = document.createElement('button');
                    loadMoreBtn.id = 'load-more-search-btn';
                    loadMoreBtn.className = 'btn btn-sm btn-outline-primary w-100 mt-2';
                    loadMoreBtn.textContent = '20 Sonuç Daha Göster';
                    loadMoreBtn.onclick = function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        loadSearchResults(true);
                    };
                    searchResults.appendChild(loadMoreBtn);
                } else {
                    loadMoreBtn.style.display = 'block';
                }
            } else {
                if (loadMoreBtn) {
                    loadMoreBtn.style.display = 'none';
                }
            }

            // Eğer hiç sonuç yoksa "Yeni başlık oluştur" seçeneği göster
            if (!isLoadMore && lastSearchResults.length === 0) {
                // Önce var olan no-results mesajını kontrol et, varsa ekleme
                const existingNoResults = searchResults.querySelector('[data-type="no-results"]');
                if (!existingNoResults) {
                    var div = document.createElement('div');
                    div.classList.add('list-group-item');
                    div.dataset.type = 'no-results';

                    var span = document.createElement('span');
                    span.textContent = 'Sonuç bulunamadı. ';

                    var a = document.createElement('a');
                    a.href = '#';
                    a.id = 'create-new-question';
                    a.textContent = 'Yeni başlık oluştur';

                    div.appendChild(span);
                    div.appendChild(a);
                    searchResults.appendChild(div);
                }
            }

            searchResults.style.display = 'block';
            currentFocus = -1;
        })
        .catch(error => {
            console.error('Arama hatası:', error);
            isLoadingMore = false;
        });
    }

    searchInput.addEventListener('input', function() {
        query = this.value.trim();
        currentSearchQuery = query;

        // Önceki timeout'u iptal et (debounce)
        if (searchTimeout) {
            clearTimeout(searchTimeout);
        }

        if (query.length > 0) {
            // Önceki sonuçları temizle
            searchResults.innerHTML = '';
            lastSearchResults = [];
            currentSearchOffset = 0;

            // 300ms bekle, sonra arama yap (debounce)
            searchTimeout = setTimeout(function() {
                loadSearchResults(false);
            }, 300);
        } else {
            searchResults.style.display = 'none';
            lastSearchResults = [];
            currentSearchOffset = 0;
        }
    });

    // Fare tıklamasıyla seçim
    searchResults.addEventListener('click', function(event) {
        var target = event.target;

        // Eğer tıklanan element list-group-item değilse, parent'ını kontrol et
        if (!target.classList.contains('list-group-item')) {
            target = target.closest('.list-group-item');
        }

        if (!target) return;  // Hiçbir list-group-item bulunmadıysa çık

        if (target.id === 'create-new-question' || target.querySelector('#create-new-question')) {
            event.preventDefault();
            var q = searchInput.value.trim();
            window.location.href = '/add_question_from_search/?q=' + encodeURIComponent(q);
        }
        else if (target.classList.contains('list-group-item')) {
            var type = target.dataset.type;
            if (type === 'question') {
                var slug = target.dataset.slug;
                if (slug) {
                    window.location.href = '/' + slug + '/';  // SEO-friendly slug URL
                }
            } else if (type === 'user') {
                var username = target.dataset.username;
                if (username) {
                    window.location.href = '/profile/' + username + '/';
                }
            } else if (type === 'hashtag') {
                // Use full URL directly from backend
                var url = target.dataset.url;
                if (url) {
                    window.location.href = url;
                }
            }
        }
    });

    // Sayfanın başka yerine tıklayınca listeyi gizle
    document.addEventListener('click', function(event) {
        if (!event.target.closest('#search-input') && !event.target.closest('#search-results')) {
            searchResults.style.display = 'none';
        }
    });

    /**
     * ========== Ok Tuşları ve Enter Desteği ==========
     */
    searchInput.addEventListener('keydown', function(e) {
        // Mevcut list-group-item'lar
        var items = searchResults.querySelectorAll('.list-group-item');

        if (e.keyCode === 40) {
            // Arrow Down
            e.preventDefault();
            currentFocus++;
            if (currentFocus >= items.length) currentFocus = 0;
            highlightItem(items);
        }
        else if (e.keyCode === 38) {
            // Arrow Up
            e.preventDefault();
            currentFocus--;
            if (currentFocus < 0) currentFocus = items.length - 1;
            highlightItem(items);
        }
        else if (e.keyCode === 13) {
            // ====== ENTER'a basıldı ======
            e.preventDefault();

            // 1) Ok tuşlarıyla bir sonuç seçiliyse => tıkla
            if (currentFocus > -1) {
                items[currentFocus].click();
                return;
            }

            // 2) Hiçbir sonuç "aktif" değil =>
            //    bkz view'ını kullan - bu view tam eşleşme varsa başlığa,
            //    yoksa yeni başlık oluşturma sayfasına otomatik yönlendirir
            if (searchInput.value.trim()) {
                window.location.href = '/bkz/' + encodeURIComponent(searchInput.value.trim()) + '/';
            }
        }
    });

    function highlightItem(items) {
        // Tümünde 'active'ı temizle
        for (var i = 0; i < items.length; i++) {
            items[i].classList.remove('active');
        }
        if (currentFocus >= 0 && currentFocus < items.length) {
            items[currentFocus].classList.add('active');
        }
    }

    /**
     * ========== Bildirim Badge Güncellemesi ==========
     * Checks for unread notifications and updates the badge
     */
    function updateNotificationBadge() {
        fetch('/notifications/unread-count/')
            .then(response => response.json())
            .then(data => {
                const badge = document.getElementById('notification-badge');
                if (badge) {
                    if (data.count > 0) {
                        badge.textContent = data.count;
                        badge.style.display = 'inline-block';
                    } else {
                        badge.style.display = 'none';
                    }
                }
            })
            .catch(error => console.error('Bildirim badge güncellenemedi:', error));
    }

    // İlk yüklemede kontrol et
    updateNotificationBadge();

    // Her 60 saniyede bir kontrol et (performans için)
    setInterval(updateNotificationBadge, 60000);
});
