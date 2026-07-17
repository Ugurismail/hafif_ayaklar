document.addEventListener('DOMContentLoaded', function () {
    const panelEl = document.getElementById('onlineChatPanel');
    const usersEl = document.getElementById('onlineChatUsers');
    const messagesEl = document.getElementById('onlineChatMessages');
    const formEl = document.getElementById('onlineChatForm');
    const inputEl = document.getElementById('onlineChatInput');
    const metaEl = document.getElementById('onlineChatMeta');
    const countEl = document.getElementById('onlineChatCount');

    if (!panelEl || !usersEl || !messagesEl || !formEl || !inputEl || !metaEl || !countEl) {
        return;
    }

    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
    const panelStateKey = 'onlineChatPanelOpen';
    const draftStateKey = 'onlineChatDraft';
    const unreadCountKey = 'onlineChatUnreadCount';
    const lastMessageIdKey = 'onlineChatLastMessageId';
    const panel = bootstrap.Offcanvas.getOrCreateInstance(panelEl);

    const state = {
        lastMessageId: Number(localStorage.getItem(lastMessageIdKey) || 0) || null,
        unreadCount: Number(localStorage.getItem(unreadCountKey) || 0) || 0,
        pollTimer: null,
        panelOpen: false,
        loading: false,
    };

    function escapeHtml(value) {
        return String(value)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    function updateDraftState() {
        const value = inputEl.value.trim();
        if (value) {
            localStorage.setItem(draftStateKey, value);
        } else {
            localStorage.removeItem(draftStateKey);
        }
    }

    function renderUsers(users) {
        if (!users || users.length === 0) {
            usersEl.innerHTML = '<div class="online-chat-empty">Şu an aktif kullanıcı görünmüyor.</div>';
            metaEl.textContent = 'Şu an çevrimiçi kullanıcı görünmüyor.';
            return;
        }

        const otherUsers = users.filter(function (user) {
            return !user.is_self;
        });

        if (otherUsers.length === 0) {
            metaEl.textContent = 'Şu an yalnızsın.';
        } else if (otherUsers.length === 1) {
            metaEl.textContent = '1 başka kullanıcı çevrimiçi.';
        } else {
            metaEl.textContent = otherUsers.length + ' başka kullanıcı çevrimiçi.';
        }

        usersEl.innerHTML = users.map(function (user) {
            const selfSuffix = user.is_self ? ' · sen' : '';
            return `
                <a class="online-chat-user" href="${escapeHtml(user.profile_url)}">
                    <img class="online-chat-user-avatar" src="${escapeHtml(user.avatar_url)}" alt="${escapeHtml(user.username)}">
                    <div class="online-chat-user-meta">
                        <div class="online-chat-user-name">${escapeHtml(user.username)}${selfSuffix}</div>
                        <div class="online-chat-user-time">Son aktif ${escapeHtml(user.last_seen)}</div>
                    </div>
                </a>
            `;
        }).join('');
    }

    function renderMessage(message) {
        const ownClass = message.is_own ? ' online-chat-message-own' : '';
        return `
            <div class="online-chat-message${ownClass}" data-message-id="${message.id}">
                <img class="online-chat-user-avatar" src="${escapeHtml(message.avatar_url)}" alt="${escapeHtml(message.username)}">
                <div class="online-chat-message-bubble">
                    <div class="online-chat-message-head">
                        <span class="online-chat-message-user">${escapeHtml(message.username)}</span>
                        <span class="online-chat-message-time">${escapeHtml(message.created_at)}</span>
                    </div>
                    <div class="online-chat-message-body">${escapeHtml(message.body)}</div>
                </div>
            </div>
        `;
    }

    function setUnreadCount(count) {
        state.unreadCount = Math.max(0, count);
        if (state.unreadCount <= 0) {
            countEl.textContent = '0';
            countEl.style.display = 'none';
            countEl.setAttribute('aria-label', 'Yeni sohbet mesajı yok');
            localStorage.removeItem(unreadCountKey);
            return;
        }
        countEl.textContent = state.unreadCount > 9 ? '9+' : String(state.unreadCount);
        countEl.style.display = 'inline-flex';
        countEl.setAttribute('aria-label', `${state.unreadCount} yeni sohbet mesajı`);
        localStorage.setItem(unreadCountKey, String(state.unreadCount));
    }

    window.hafifAyaklarSetOnlineChatUnreadCount = function (count) {
        if (!state.panelOpen) {
            setUnreadCount(Number(count || 0));
        }
    };

    function rememberLastMessageId(messageId) {
        const numericId = Number(messageId);
        if (!numericId) {
            return;
        }
        state.lastMessageId = numericId;
        localStorage.setItem(lastMessageIdKey, String(numericId));
    }

    function buildMessagesUrl(options) {
        const params = new URLSearchParams();
        if (options.append && state.lastMessageId) {
            params.set('after', state.lastMessageId);
        }
        if (options.markRead) {
            params.set('mark_read', '1');
        }
        const query = params.toString();
        return '/online-chat/messages/' + (query ? `?${query}` : '');
    }

    function setMessages(messages, append) {
        if (!messages || messages.length === 0) {
            if (!append && !messagesEl.children.length) {
                messagesEl.innerHTML = '<div class="online-chat-empty">Henüz mesaj yok. İlk mesajı sen yaz.</div>';
            }
            return;
        }

        if (!append) {
            messagesEl.innerHTML = messages.map(renderMessage).join('');
        } else {
            const frag = document.createElement('div');
            frag.innerHTML = messages.map(renderMessage).join('');
            while (frag.firstChild) {
                messagesEl.appendChild(frag.firstChild);
            }
        }

        const last = messages[messages.length - 1];
        if (last && last.id) {
            rememberLastMessageId(last.id);
        }
        messagesEl.scrollTop = messagesEl.scrollHeight;
    }

    async function fetchChat(append = false, quiet = false) {
        if (state.loading) return;
        state.loading = true;
        try {
            const url = buildMessagesUrl({ append: append, markRead: state.panelOpen });
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            if (!response.ok) {
                throw new Error('Online sohbet yüklenemedi.');
            }
            const data = await response.json();
            renderUsers(data.online_users || []);
            setMessages(data.messages || [], append);
            setUnreadCount(Number(data.unread_count || 0));
        } catch (error) {
            if (!quiet && typeof showToast === 'function') {
                showToast(error.message || 'Online sohbet yüklenemedi.', 'error');
            }
        } finally {
            state.loading = false;
        }
    }

    async function submitMessage(event) {
        event.preventDefault();
        const body = inputEl.value.trim();
        if (!body) {
            if (typeof showToast === 'function') {
                showToast('Mesaj boş olamaz.', 'warning');
            }
            return;
        }

        try {
            const formData = new FormData();
            formData.append('body', body);
            const response = await fetch('/online-chat/messages/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || 'Mesaj gönderilemedi.');
            }
            messagesEl.querySelectorAll('.online-chat-empty').forEach(function (node) {
                node.remove();
            });
            setMessages([data.message], true);
            setUnreadCount(Number(data.unread_count || 0));
            inputEl.value = '';
            localStorage.removeItem(draftStateKey);
        } catch (error) {
            if (typeof showToast === 'function') {
                showToast(error.message || 'Mesaj gönderilemedi.', 'error');
            }
        }
    }

    panelEl.addEventListener('shown.bs.offcanvas', function () {
        state.panelOpen = true;
        document.body.classList.add('online-chat-open');
        localStorage.setItem(panelStateKey, '1');
        setUnreadCount(0);
        fetchChat(false);
        if (state.pollTimer) {
            window.clearInterval(state.pollTimer);
        }
        state.pollTimer = window.setInterval(function () {
            fetchChat(true, true);
        }, 5000);
    });

    panelEl.addEventListener('hidden.bs.offcanvas', function () {
        state.panelOpen = false;
        document.body.classList.remove('online-chat-open');
        localStorage.removeItem(panelStateKey);
        if (state.pollTimer) {
            window.clearInterval(state.pollTimer);
            state.pollTimer = null;
        }
    });

    formEl.addEventListener('submit', submitMessage);
    inputEl.addEventListener('input', updateDraftState);
    inputEl.addEventListener('keydown', function (event) {
        if (event.key !== 'Enter' || event.shiftKey || event.isComposing) {
            return;
        }
        event.preventDefault();
        formEl.requestSubmit();
    });

    const savedDraft = localStorage.getItem(draftStateKey);
    if (savedDraft) {
        inputEl.value = savedDraft;
    }
    setUnreadCount(state.unreadCount);

    if (localStorage.getItem(panelStateKey) === '1') {
        panel.show();
    }
});
