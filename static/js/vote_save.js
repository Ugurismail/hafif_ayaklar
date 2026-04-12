// static/js/vote_save.js

document.addEventListener('DOMContentLoaded', function() {
    // CSRF token'ını meta tag'den al
    const csrftoken = document.querySelector('meta[name="csrf-token"]')?.content || getCookie('csrftoken');
    const saveModalEl = document.getElementById('globalSaveCollectionModal');
    const saveModal = saveModalEl ? new bootstrap.Modal(saveModalEl) : null;
    const saveForm = document.getElementById('globalSaveCollectionForm');
    const saveChoices = document.getElementById('globalSaveCollectionChoices');
    const saveNameInput = document.getElementById('globalSaveCollectionName');
    const saveMeta = document.getElementById('globalSaveCollectionModalMeta');
    const saveEmpty = document.getElementById('globalSaveCollectionEmpty');
    const saveContentTypeInput = document.getElementById('globalSaveCollectionContentType');
    const saveObjectIdInput = document.getElementById('globalSaveCollectionObjectId');
    const saveSavedStateInput = document.getElementById('globalSaveCollectionSavedState');
    const saveRemoveBtn = document.getElementById('globalSaveCollectionRemoveBtn');
    let activeSaveButton = null;

    // **Oylama İşlevselliği** (Upvote / Downvote)
    // Capture fazında (window seviyesinde) dinle: bazı sayfalarda üst seviye handler'lar click'i yutabiliyor.
    window.addEventListener('click', function(event) {
        const voteButton = event.target.closest?.('.vote-btn');
        if (voteButton) {
            event.preventDefault();
            event.stopPropagation();
            const contentType = voteButton.getAttribute('data-content-type');
            const objectId = voteButton.getAttribute('data-object-id');
            const value = parseInt(voteButton.getAttribute('data-value'));

            if (!csrftoken) {
                showToast('CSRF token bulunamadı. Sayfayı yenileyip tekrar deneyin.', 'error');
                return;
            }

            // FormData
            const formData = new FormData();
            formData.append('content_type', contentType);
            formData.append('object_id', objectId);
            formData.append('value', value);

            fetch('/vote/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    // 403 hatası için JSON parse et
                    if (response.status === 403) {
                        return response.json().then(data => {
                            throw new Error(data.error || 'Yetkisiz işlem');
                        });
                    }
                    return response.text().then(text => { throw new Error(text); });
                }
                return response.json();
            })
            .then(data => {
                if (data.upvotes !== undefined && data.downvotes !== undefined) {
                    if (contentType === 'question') {
                        // Soru up/down sayıları
                        const upvotesEl = document.getElementById('question-upvotes');
                        const downvotesEl = document.getElementById('question-downvotes');
                        if (upvotesEl) upvotesEl.innerText = data.upvotes;
                        if (downvotesEl) downvotesEl.innerText = data.downvotes;

                        const upvoteButton = document.querySelector(`.vote-btn[data-content-type="question"][data-object-id="${objectId}"][data-value="1"]`);
                        const downvoteButton = document.querySelector(`.vote-btn[data-content-type="question"][data-object-id="${objectId}"][data-value="-1"]`);
                        updateVoteButtonStyles(upvoteButton, downvoteButton, data.user_vote_value);

                    } else if (contentType === 'answer') {
                        // Yanıt up/down sayıları
                        const upvotesEl = document.getElementById(`answer-upvotes-${objectId}`);
                        const downvotesEl = document.getElementById(`answer-downvotes-${objectId}`);
                        if (upvotesEl) upvotesEl.innerText = data.upvotes;
                        if (downvotesEl) downvotesEl.innerText = data.downvotes;

                        const upvoteButton = document.querySelector(`.vote-btn[data-content-type="answer"][data-object-id="${objectId}"][data-value="1"]`);
                        const downvoteButton = document.querySelector(`.vote-btn[data-content-type="answer"][data-object-id="${objectId}"][data-value="-1"]`);
                        updateVoteButtonStyles(upvoteButton, downvoteButton, data.user_vote_value);
                    }
                } else if (data.message) {
                    showToast(data.message, 'info');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast(error.message || 'Bir hata oluştu. Lütfen tekrar deneyin.', 'error');
            });
        }
    }, true);

    function updateSaveButtons(contentType, objectId, isSaved, saveCount) {
        document.querySelectorAll(`.save-btn[data-content-type="${contentType}"][data-object-id="${objectId}"]`).forEach(function(saveButton) {
            const icon = saveButton.querySelector('i');
            if (icon) {
                icon.classList.toggle('bi-bookmark-fill', isSaved);
                icon.classList.toggle('bi-bookmark', !isSaved);
            }
            const saveCountSpan = saveButton.parentElement?.querySelector('.save-count') || saveButton.nextElementSibling;
            if (saveCountSpan && saveCount !== undefined) {
                saveCountSpan.innerText = saveCount;
            }
        });
    }

    function populateCollectionChoices(collections) {
        if (!saveChoices) return;
        saveChoices.innerHTML = '';
        if (!collections.length) {
            if (saveEmpty) saveEmpty.style.display = 'block';
            return;
        }
        if (saveEmpty) saveEmpty.style.display = 'none';
        collections.forEach(function(collection) {
            const label = document.createElement('label');
            label.className = 'd-flex align-items-center gap-2 border rounded px-2 py-2';
            const input = document.createElement('input');
            input.className = 'form-check-input mt-0';
            input.type = 'checkbox';
            input.value = collection.id;
            input.checked = !!collection.selected;
            const span = document.createElement('span');
            span.textContent = collection.name;
            label.appendChild(input);
            label.appendChild(span);
            saveChoices.appendChild(label);
        });
    }

    async function requestSaveAction(saveButton, action) {
        const contentType = saveButton.getAttribute('data-content-type');
        const objectId = saveButton.getAttribute('data-object-id');
        const formData = new FormData();
        formData.append('content_type', contentType);
        formData.append('object_id', objectId);
        if (action) {
            formData.append('action', action);
        }
        const response = await fetch('/save-item/', {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            body: formData
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Bir hata oluştu.');
        }
        return data;
    }

    async function openSaveCollectionsModal(saveButton) {
        const contentType = saveButton.getAttribute('data-content-type');
        const objectId = saveButton.getAttribute('data-object-id');

        const response = await fetch(`/collections/options/?content_type=${encodeURIComponent(contentType)}&object_id=${encodeURIComponent(objectId)}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Koleksiyon bilgileri yüklenemedi.');
        }

        activeSaveButton = saveButton;
        if (saveContentTypeInput) saveContentTypeInput.value = contentType;
        if (saveObjectIdInput) saveObjectIdInput.value = objectId;
        if (saveSavedStateInput) saveSavedStateInput.value = data.is_saved ? '1' : '0';
        if (saveNameInput) saveNameInput.value = '';
        if (saveMeta) {
            saveMeta.textContent = data.is_saved
                ? 'Kaydedilmiş içerik. İstersen koleksiyonlarını güncelle ya da kaydı kaldır.'
                : 'İçeriği doğrudan bir koleksiyona ekleyebilir ya da koleksiyonsuz kaydedebilirsin.';
        }
        if (saveRemoveBtn) {
            saveRemoveBtn.style.display = data.is_saved ? 'inline-flex' : 'none';
        }
        populateCollectionChoices(data.collections || []);
        saveModal?.show();
    }

    // **Kaydet / Koleksiyona Ekle İşlevi**
    window.addEventListener('click', async function(event) {
        const saveButton = event.target.closest?.('.save-btn');
        if (!saveButton) return;

        event.preventDefault();
        event.stopPropagation();

        if (!csrftoken) {
            showToast('CSRF token bulunamadı. Sayfayı yenileyip tekrar deneyin.', 'error');
            return;
        }

        if (!saveModal) {
            try {
                const data = await requestSaveAction(saveButton, '');
                updateSaveButtons(
                    saveButton.getAttribute('data-content-type'),
                    saveButton.getAttribute('data-object-id'),
                    data.status === 'saved',
                    data.save_count
                );
            } catch (error) {
                console.error('Error:', error);
                showToast(error.message || 'Bir hata oluştu. Lütfen tekrar deneyin.', 'error');
            }
            return;
        }

        try {
            await openSaveCollectionsModal(saveButton);
        } catch (error) {
            console.error('Error:', error);
            showToast(error.message || 'Koleksiyonlar açılamadı.', 'error');
        }
    }, true);

    saveForm?.addEventListener('submit', async function(event) {
        event.preventDefault();

        if (!activeSaveButton) return;

        const formData = new FormData();
        formData.append('content_type', saveContentTypeInput?.value || '');
        formData.append('object_id', saveObjectIdInput?.value || '');
        formData.append('action', 'save');
        saveChoices?.querySelectorAll('input[type="checkbox"]:checked').forEach(function(input) {
            formData.append('collection_ids', input.value);
        });
        if (saveNameInput?.value.trim()) {
            formData.append('new_collection_name', saveNameInput.value.trim());
        }

        try {
            const response = await fetch('/save-item/', {
                method: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
                body: formData
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || 'Kaydetme işlemi başarısız.');
            }

            updateSaveButtons(saveContentTypeInput.value, saveObjectIdInput.value, true, data.save_count);
            if (window.location.href.includes('/profile/') || window.location.href.includes('/collections/')) {
                window.location.reload();
                return;
            }
            showToast(
                data.collections?.length
                    ? 'İçerik kaydedildi ve koleksiyona eklendi.'
                    : 'İçerik kaydedildi.',
                'success'
            );
            saveModal?.hide();
        } catch (error) {
            console.error('Error:', error);
            showToast(error.message || 'Bir hata oluştu. Lütfen tekrar deneyin.', 'error');
        }
    });

    saveRemoveBtn?.addEventListener('click', async function() {
        if (!activeSaveButton) return;
        try {
            const data = await requestSaveAction(activeSaveButton, 'unsave');
            updateSaveButtons(saveContentTypeInput.value, saveObjectIdInput.value, false, data.save_count);
            if (window.location.href.includes('/profile/') || window.location.href.includes('/collections/')) {
                window.location.reload();
                return;
            }
            showToast('Kayıt kaldırıldı.', 'success');
            saveModal?.hide();
        } catch (error) {
            console.error('Error:', error);
            showToast(error.message || 'Bir hata oluştu. Lütfen tekrar deneyin.', 'error');
        }
    });

    // Oy butonlarının görünümünü güncelle
    function updateVoteButtonStyles(upvoteButton, downvoteButton, userVoteValue) {
        if (upvoteButton) upvoteButton.classList.remove('voted-up');
        if (downvoteButton) downvoteButton.classList.remove('voted-down');

        if (userVoteValue === 1 || userVoteValue === "1") {
            if (upvoteButton) upvoteButton.classList.add('voted-up');
        } else if (userVoteValue === -1 || userVoteValue === "-1") {
            if (downvoteButton) downvoteButton.classList.add('voted-down');
        }
    }
});
