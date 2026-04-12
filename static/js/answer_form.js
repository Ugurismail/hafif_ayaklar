// answer_form.js

document.addEventListener('DOMContentLoaded', function() {
  function isUsableCsrfToken(token) {
    if (!token) return false;
    var normalized = String(token).trim();
    if (!normalized) return false;
    return normalized !== 'NOTPROVIDED' &&
           normalized !== 'undefined' &&
           normalized !== 'null' &&
           normalized !== 'csrf_token' &&
           normalized !== 'csrftoken';
  }

  function getCsrfToken() {
    var metaToken = document.querySelector('meta[name="csrf-token"]');
    var metaValue = metaToken && metaToken.content ? metaToken.content : '';
    if (isUsableCsrfToken(metaValue)) {
      return metaValue.trim();
    }

    var csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    var inputValue = csrfInput && csrfInput.value ? csrfInput.value : '';
    if (isUsableCsrfToken(inputValue)) {
      return inputValue.trim();
    }

    var cookieMatch = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
    var cookieValue = cookieMatch ? decodeURIComponent(cookieMatch[1]) : '';
    return isUsableCsrfToken(cookieValue) ? cookieValue.trim() : '';
  }

  function notify(message, level) {
    if (typeof showToast === 'function') {
      showToast(message, level || 'info');
      return;
    }
    alert(message);
  }

  function dispatchAnswerTextChanged(textarea) {
    if (!textarea) return;
    textarea.dispatchEvent(new Event('input', { bubbles: true }));
  }

  window.hafifAyaklarAnswerTextChanged = dispatchAnswerTextChanged;

  function reinitPreviewOverlays(root) {
    if (!root || typeof bootstrap === 'undefined') return;

    root.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function(el) {
      var inst = bootstrap.Tooltip.getInstance(el);
      if (inst) inst.dispose();
      var wantsHtml = (el.getAttribute('data-bs-html') || '').toLowerCase() === 'true';
      new bootstrap.Tooltip(el, {
        container: 'body',
        trigger: 'hover focus',
        html: wantsHtml,
        delay: { show: 500, hide: 100 }
      });
    });

    root.querySelectorAll('[data-bs-toggle="popover"]').forEach(function(el) {
      var inst = bootstrap.Popover.getInstance(el);
      if (inst) inst.dispose();
      new bootstrap.Popover(el, {
        container: 'body',
        html: true,
        trigger: el.getAttribute('data-bs-trigger') || 'hover focus',
      });
    });
  }

  function preventPreviewNavigation(root) {
    if (!root || root.dataset.previewNavBound === '1') return;
    root.dataset.previewNavBound = '1';
    root.addEventListener('click', function(e) {
      var anchor = e.target && e.target.closest ? e.target.closest('a') : null;
      if (!anchor) return;
      e.preventDefault();
      e.stopPropagation();
    });
  }

  function initAnswerLivePreview() {
    var root = document.getElementById('answer-live-preview-root');
    var textarea = document.getElementById('id_answer_text') || document.querySelector('textarea[name="answer_text"]');
    if (!root || !textarea) return;

    var previewEndpoint = '/answer/preview/';
    var lastRenderedContent = null;
    var debounceTimer = null;

    preventPreviewNavigation(root);

    function clearPreview() {
      root.innerHTML = '';
      root.style.display = 'none';
      lastRenderedContent = '';
    }

    function renderPreviewNow() {
      var content = textarea.value || '';
      if (!content.trim()) {
        clearPreview();
        return;
      }
      if (content === lastRenderedContent) {
        return;
      }

      fetch(previewEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({
          content: content,
          question_text: root.dataset.previewQuestionText || '',
          question_slug: root.dataset.previewQuestionSlug || '',
        }),
      })
        .then(function(response) { return response.json().then(function(data) { return { ok: response.ok, data: data }; }); })
        .then(function(result) {
          if (!result.ok || !result.data || result.data.status !== 'ok') {
            return;
          }
          lastRenderedContent = content;
          root.innerHTML = result.data.html || '';
          root.style.display = root.innerHTML ? 'block' : 'none';
          reinitPreviewOverlays(root);
          if (typeof window.hafifAyaklarRenderMath === 'function') {
            window.hafifAyaklarRenderMath(root);
          }
        })
        .catch(function() {
          // silent
        });
    }

    function schedulePreview() {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(renderPreviewNow, 320);
    }

    textarea.addEventListener('input', schedulePreview);
    textarea.addEventListener('change', schedulePreview);

    if ((textarea.value || '').trim()) {
      schedulePreview();
    }
  }

  initAnswerLivePreview();

  //==================================================================
  // A) METİN BİÇİMLENDİRME BUTONLARI (BOLD, ITALIC)
  //==================================================================
  var formatButtons = document.querySelectorAll('.format-btn');
  formatButtons.forEach(function(button) {
      button.addEventListener('click', function() {
          var format = this.getAttribute('data-format');
          var textarea = document.getElementById('id_answer_text');
          applyFormat(textarea, format);
      });
  });

  function applyFormat(textarea, format) {
      if (!textarea) return;
      var start = textarea.selectionStart;
      var end   = textarea.selectionEnd;
      var selectedText = textarea.value.substring(start, end);
      var before = textarea.value.substring(0, start);
      var after  = textarea.value.substring(end);

      var formattedText = selectedText;
      if (format === 'bold') {
          formattedText = '**' + selectedText + '**';
      } else if (format === 'italic') {
          formattedText = '*' + selectedText + '*';
      }

      textarea.value = before + formattedText + after;
      // Seçili alanı yeniden belirle
      textarea.selectionStart = start;
      textarea.selectionEnd   = start + formattedText.length;
      textarea.focus({ preventScroll: true });
      dispatchAnswerTextChanged(textarea);
  }

  //==================================================================
  // SPOILER (YILDIZ) BUTONU
  //==================================================================
  var spoilerBtns = document.querySelectorAll('.spoiler-btn');
  spoilerBtns.forEach(function(btn) {
      btn.addEventListener('click', function() {
          var textarea = document.getElementById('id_answer_text') ||
                        document.querySelector('textarea[name="answer_text"]');
          if (!textarea) return;

          var start = textarea.selectionStart;
          var end = textarea.selectionEnd;
          var selectedText = textarea.value.substring(start, end);

          if (!selectedText) {
              if (typeof showToast === 'function') {
                  showToast('Gizlemek için bir metin seçin!', 'warning');
              } else {
                  alert('Gizlemek için bir metin seçin!');
              }
              return;
          }

          var before = textarea.value.substring(0, start);
          var after = textarea.value.substring(end);
          var spoilerText = '-g- ' + selectedText + ' -g-';

          textarea.value = before + spoilerText + after;
          textarea.selectionStart = start;
          textarea.selectionEnd = start + spoilerText.length;
          textarea.focus({ preventScroll: true });
          dispatchAnswerTextChanged(textarea);
      });
  });


  //==================================================================
  // B) HARİCİ LİNK EKLEME (MODAL)
  //==================================================================
  var linkModalElem = document.getElementById('linkModal');
  if (linkModalElem) {
    var linkModal    = new bootstrap.Modal(linkModalElem);
    var insertLinkBtn= document.querySelector('.insert-link-btn');
    var linkForm     = document.getElementById('link-form');

    if (insertLinkBtn && linkForm) {
      insertLinkBtn.addEventListener('click', function() {
        linkModal.show();
        linkForm.reset();
      });

      linkForm.addEventListener('submit', function(event) {
        event.preventDefault();
        var url  = document.getElementById('link-url').value.trim();
        var text = document.getElementById('link-text').value.trim();
        if (url && text) {
            var textarea = document.getElementById('id_answer_text');
            if (!textarea) return;
            var start = textarea.selectionStart;
            var end   = textarea.selectionEnd;
            var before= textarea.value.substring(0, start);
            var after = textarea.value.substring(end);
            var linkMarkdown = '[' + text + '](' + url + ')';
            textarea.value = before + linkMarkdown + after;
            textarea.selectionStart = start;
            textarea.selectionEnd   = start + linkMarkdown.length;
            textarea.focus({ preventScroll: true });
            dispatchAnswerTextChanged(textarea);
            linkModal.hide();
        }
      });
    }
  }


  //==================================================================
  // B.1) GÖRSEL EKLEME (MODAL)
  //==================================================================
  var imageModalElem = document.getElementById('imageModal');
  if (imageModalElem) {
    var imageModal = new bootstrap.Modal(imageModalElem);
    var imageForm = document.getElementById('image-form');
    var imageFileInput = document.getElementById('image-file');
    var imageAltInput = document.getElementById('image-alt');
    var imageSubmitBtn = document.getElementById('image-submit-btn');
    var insertImageButtons = document.querySelectorAll('.insert-image-btn');
    var imageModalRestoreTarget = null;

    imageModalElem.addEventListener('hide.bs.modal', function() {
      var activeEl = document.activeElement;
      if (activeEl && imageModalElem.contains(activeEl) && typeof activeEl.blur === 'function') {
        activeEl.blur();
      }
    });

    imageModalElem.addEventListener('hidden.bs.modal', function() {
      var target = imageModalRestoreTarget ||
        document.getElementById('id_answer_text') ||
        document.querySelector('textarea[name="answer_text"]');

      if (target && typeof target.focus === 'function') {
        setTimeout(function() {
          try {
            target.focus({ preventScroll: true });
          } catch (err) {
            target.focus();
          }
        }, 0);
      }

      imageModalRestoreTarget = null;
    });

    insertImageButtons.forEach(function(button) {
      button.addEventListener('click', function(e) {
        e.preventDefault();
        imageModalRestoreTarget = button;
        if (imageForm) imageForm.reset();
        if (imageSubmitBtn) {
          imageSubmitBtn.disabled = false;
          imageSubmitBtn.textContent = 'Yukle ve Ekle';
        }
        imageModal.show();
        if (imageFileInput) {
          setTimeout(function() {
            imageFileInput.focus();
          }, 120);
        }
      });
    });

    if (imageForm) {
      imageForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        var textarea = document.getElementById('id_answer_text') ||
                      document.querySelector('textarea[name="answer_text"]');
        if (!textarea) {
          notify('Yanit alani bulunamadi.', 'error');
          return;
        }

        var selectedFile = imageFileInput && imageFileInput.files ? imageFileInput.files[0] : null;
        var altValue = imageAltInput ? imageAltInput.value.trim() : '';
        var uploadUrl = imageForm.getAttribute('data-upload-url') || '/upload-editor-image/';

        if (!selectedFile) {
          notify('Lutfen yuklenecek gorseli secin.', 'warning');
          return;
        }

        var formData = new FormData();
        formData.append('image', selectedFile);
        var csrfTokenValue = getCsrfToken();
        if (csrfTokenValue) {
          formData.append('csrfmiddlewaretoken', csrfTokenValue);
        }

        if (imageSubmitBtn) {
          imageSubmitBtn.disabled = true;
          imageSubmitBtn.textContent = 'Yukleniyor...';
        }

        var response;
        try {
          response = await fetch(uploadUrl, {
            method: 'POST',
            headers: {
              'X-CSRFToken': csrfTokenValue,
              'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
          });
        } catch (err) {
          if (imageSubmitBtn) {
            imageSubmitBtn.disabled = false;
            imageSubmitBtn.textContent = 'Yukle ve Ekle';
          }
          notify('Gorsel yuklenemedi. Baglantiyi kontrol edip tekrar deneyin.', 'error');
          return;
        }

        var result = {};
        try {
          result = await response.json();
        } catch (err) {
          result = {};
        }

        if (!response.ok || !result.file_url) {
          if (imageSubmitBtn) {
            imageSubmitBtn.disabled = false;
            imageSubmitBtn.textContent = 'Yukle ve Ekle';
          }
          notify(result.error || 'Gorsel yukleme basarisiz.', 'error');
          return;
        }

        var normalizedUrl = new URL(result.file_url, window.location.origin).href;
        var safeAlt = altValue.replace(/\]/g, '\\]');
        var imageMarkdown = '![' + safeAlt + '](' + normalizedUrl + ')';
        var imageBlock = imageMarkdown;

        var start = textarea.selectionStart;
        var end = textarea.selectionEnd;
        var before = textarea.value.substring(0, start);
        var after = textarea.value.substring(end);
        var hasTextBefore = before.trim().length > 0;
        var hasTextAfter = after.trim().length > 0;

        if (hasTextBefore || hasTextAfter) {
          imageBlock = (hasTextBefore ? '\n\n' : '') + imageMarkdown + (hasTextAfter ? '\n\n' : '');
        }

        textarea.value = before + imageBlock + after;
        textarea.selectionStart = start + imageBlock.length;
        textarea.selectionEnd = start + imageBlock.length;
        textarea.focus({ preventScroll: true });
        dispatchAnswerTextChanged(textarea);
        imageModalRestoreTarget = textarea;

        if (imageSubmitBtn) {
          imageSubmitBtn.disabled = false;
          imageSubmitBtn.textContent = 'Yukle ve Ekle';
        }
        imageModal.hide();
        notify('Gorsel eklendi.', 'success');
      });
    }
  }


  //==================================================================
// C) (bkz:...) REFERANS EKLEME (MODAL)
//==================================================================
var referenceModalElem = document.getElementById('referenceModal');
  if (!referenceModalElem) return;

  var referenceModal = new bootstrap.Modal(referenceModalElem);
  var insertReferenceBtn = document.querySelector('.insert-reference-btn');
  var referenceSearchInput = document.getElementById('reference-search-input');
  var referenceSearchResults = document.getElementById('reference-search-results');
  var noResultsDiv = document.getElementById('no-results');
  var addCurrentQueryBtn = document.getElementById('add-current-query');

  function getAnswerTextarea() {
    return document.getElementById('id_answer_text') ||
          document.querySelector('textarea[name="answer_text"]');
  }

  // Modalı açan buton
  if (insertReferenceBtn) {
    var bkzInlineHandled = false;

    function tryInlineBkzInsert(e) {
      if (bkzInlineHandled) return;

      var textarea = getAnswerTextarea();
      if (!textarea) return;

      // Seçim, butona basınca bazı tarayıcılarda click anında kaybolabiliyor.
      // Bu yüzden pointerdown/mousedown anında yakalayıp doğrudan ekliyoruz.
      var selectedText = textarea.value.substring(textarea.selectionStart, textarea.selectionEnd).trim();
      if (!selectedText) return;

      bkzInlineHandled = true;
      if (e) {
        e.preventDefault();
        e.stopPropagation();
      }
      insertBkzReference(selectedText);
    }

    insertReferenceBtn.addEventListener('pointerdown', tryInlineBkzInsert, true);
    insertReferenceBtn.addEventListener('mousedown', tryInlineBkzInsert, true);

    insertReferenceBtn.addEventListener('click', function (e) {
      // Eğer kullanıcı metin seçtiyse modal açmadan direkt (bkz: ...) ekle
      if (bkzInlineHandled) {
        bkzInlineHandled = false;
        if (e) e.preventDefault();
        return;
      }

      var textarea = getAnswerTextarea();
      if (textarea) {
        var selectedText = textarea.value.substring(textarea.selectionStart, textarea.selectionEnd).trim();
        if (selectedText) {
          if (e) e.preventDefault();
          insertBkzReference(selectedText);
          return;
        }
      }

      referenceModal.show();
      if (referenceSearchInput) referenceSearchInput.value = '';
      if (referenceSearchResults) referenceSearchResults.innerHTML = '';
      if (noResultsDiv) noResultsDiv.style.display = 'none';
    });
  }

  // Keyboard navigation state
  var currentFocusBkz = -1;

  // Arama işlemi
  if (referenceSearchInput && referenceSearchResults && noResultsDiv) {
    referenceSearchInput.addEventListener('input', function () {
      var query = this.value.trim();
      currentFocusBkz = -1; // Reset focus on new input
      if (query.length > 0) {
        fetch('/reference-search/?q=' + encodeURIComponent(query), {
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.json())
        .then(data => {
          referenceSearchResults.innerHTML = '';
          if (data.results && data.results.length > 0) {
            data.results.forEach(function (item) {
              var div = document.createElement('div');
              div.classList.add('list-group-item');
              div.textContent = item.text;
              div.dataset.questionId = item.id;
              referenceSearchResults.appendChild(div);
            });
          }
          // *** Her zaman göster ***
          noResultsDiv.style.display = 'block';
        });
      } else {
        referenceSearchResults.innerHTML = '';
        noResultsDiv.style.display = 'none';
      }
    });
  
    // Sonuçlardan birine tıklama
    referenceSearchResults.addEventListener('click', function (event) {
      var target = event.target;
      if (target && target.matches('.list-group-item')) {
        insertBkzReference(target.textContent);
        referenceModal.hide();
      }
    });

    // Keyboard navigation for (bkz:) results
    referenceSearchInput.addEventListener('keydown', function(e) {
      var items = referenceSearchResults.querySelectorAll('.list-group-item');

      if (e.keyCode === 40) {
        // Arrow Down
        e.preventDefault();
        currentFocusBkz++;
        if (currentFocusBkz >= items.length) currentFocusBkz = 0;
        highlightBkzItem(items);
      }
      else if (e.keyCode === 38) {
        // Arrow Up
        e.preventDefault();
        currentFocusBkz--;
        if (currentFocusBkz < 0) currentFocusBkz = items.length - 1;
        highlightBkzItem(items);
      }
      else if (e.keyCode === 13) {
        // Enter key
        e.preventDefault();
        if (currentFocusBkz > -1 && currentFocusBkz < items.length) {
          // Select the highlighted item
          items[currentFocusBkz].click();
        } else {
          // No item selected, use "ekle" button behavior
          var query = referenceSearchInput.value.trim();
          if (query.length > 0) {
            insertBkzReference(query);
            referenceModal.hide();
          }
        }
      }
    });

    function highlightBkzItem(items) {
      // Remove active class from all items
      for (var i = 0; i < items.length; i++) {
        items[i].classList.remove('active');
      }
      // Add active class to current item
      if (currentFocusBkz >= 0 && currentFocusBkz < items.length) {
        items[currentFocusBkz].classList.add('active');
      }
    }

    // "ekle" butonuna tıklama
    if (addCurrentQueryBtn) {
      addCurrentQueryBtn.addEventListener('click', function () {
        var query = referenceSearchInput.value.trim();
        if (query.length > 0) {
          insertBkzReference(query);
          referenceModal.hide();
        }
      });
    }
  }
  
  

  function insertBkzReference(text) {
    var textarea = getAnswerTextarea();
    if (!textarea) return;
    var start = textarea.selectionStart;
    var end = textarea.selectionEnd;
    var before = textarea.value.substring(0, start);
    var after = textarea.value.substring(end);
    var referenceText = '(bkz: ' + text + ')';
    textarea.value = before + referenceText + after;
    textarea.selectionStart = start;
    textarea.selectionEnd = start + referenceText.length;
    textarea.focus({ preventScroll: true });
    dispatchAnswerTextChanged(textarea);
  }



  //==================================================================
  // D) (ref:...) BUTONU
  //==================================================================
  var insertRefLinkBtn = document.querySelector('.insert-ref-link-btn');
  if (insertRefLinkBtn) {
    insertRefLinkBtn.addEventListener('click', function() {
      var textarea = document.getElementById('id_answer_text');
      if (!textarea) return;

      var selectedText = getSelectedText(textarea);
      if (selectedText) {
          var refMarkup = `(r:${selectedText})`;
          insertTextAtCursor(textarea, refMarkup);
      } else {
          showToast('Lütfen renkli bağlantı yapmak istediğiniz metni seçiniz.', 'warning');
      }
    });
  }

  function getSelectedText(textarea) {
    if (!textarea) return '';
    var start = textarea.selectionStart;
    var end   = textarea.selectionEnd;
    return textarea.value.substring(start, end);
  }

  function insertTextAtCursor(textarea, text) {
    var start = textarea.selectionStart;
    var end   = textarea.selectionEnd;
    var before= textarea.value.substring(0, start);
    var after = textarea.value.substring(end);
    textarea.value = before + text + after;
    textarea.selectionStart = textarea.selectionEnd = start + text.length;
    textarea.focus({ preventScroll: true });
    dispatchAnswerTextChanged(textarea);
  }


  //==================================================================
  // E) TANIM MODALI (3 SEKME)
  //==================================================================
  var definitionModalElem = document.getElementById('definitionModal');
  if (!definitionModalElem) {
    // "Tanım" modalı yoksa çık
    return;
  }
  var defModal = new bootstrap.Modal(definitionModalElem);

  // Modalı açan buton
  var showDefinitionModalBtn = document.getElementById('showDefinitionModalBtn');
  if (showDefinitionModalBtn) {
    showDefinitionModalBtn.addEventListener('click', function(e) {
      e.preventDefault();
      defModal.show();
    });
  }

  // (E.1) TANIM YAP Sekmesi
  var createDefinitionForm = document.getElementById('createDefinitionForm');
  if (createDefinitionForm) {
    createDefinitionForm.addEventListener('submit', function(e) {
      e.preventDefault();
      var definitionText = document.getElementById('definitionText').value.trim();
      var definitionModalElem = document.getElementById('definitionModal');

      if (!definitionModalElem) {
        showToast("Tanım modal bulunamadı.", 'error');
        return;
      }

      if (!definitionText) {
        showToast("Lütfen bir tanım girin.", 'warning');
        return;
      }

      var questionSlug = definitionModalElem.dataset.questionSlug;
      var answerTextarea = document.getElementById('id_answer_text') || document.querySelector('textarea[name="answer_text"]');

      if (!answerTextarea) {
        showToast("Yanıt alanı bulunamadı!", 'error');
        return;
      }

      // Eğer questionSlug yoksa (yeni soru oluşturma), tanım metnini doğrudan ekle
      if (!questionSlug) {
        // Yeni soru oluşturma sayfasında - tanım metnini imlecin bulunduğu yere ekle
        // Eğer metin seçiliyse, seçimin sonuna ekle (seçili metni koruyoruz)
        var insertPos = Math.max(answerTextarea.selectionStart, answerTextarea.selectionEnd);
        var before = answerTextarea.value.substring(0, insertPos);
        var after = answerTextarea.value.substring(insertPos);

        answerTextarea.value = before + definitionText + after;
        answerTextarea.selectionStart = answerTextarea.selectionEnd = insertPos + definitionText.length;
        answerTextarea.focus({ preventScroll: true });
        dispatchAnswerTextChanged(answerTextarea);

        // Hidden input'a da ekle - backend'de Definition kaydı oluşturmak için
        var hiddenDefInput = document.getElementById('hiddenDefinitionText');
        if (hiddenDefInput) {
          hiddenDefInput.value = definitionText;
        }

        // Modal'ı kapat
        let modalInstance = bootstrap.Modal.getInstance(definitionModalElem);
        if (modalInstance) {
          modalInstance.hide();
        }

        document.getElementById('definitionText').value = "";
        showToast("Tanım metni eklendi! Yanıtı gönderdikten sonra tanım oluşturulacak.", 'success');
        return;
      }

      // Mevcut soru için tanım oluşturma API'sine gönder
      fetch(`/create-definition/${questionSlug}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          definition_text: definitionText
        })
      })
      .then(res => res.json())
      .then(data => {
         if (data.status === 'success') {
           // İmlecin bulunduğu konuma tanım metnini ekle (format değil)
           // Eğer metin seçiliyse, seçimin sonuna ekle (seçili metni koruyoruz)
           var insertPos = Math.max(answerTextarea.selectionStart, answerTextarea.selectionEnd);
           var before = answerTextarea.value.substring(0, insertPos);
           var after = answerTextarea.value.substring(insertPos);

           answerTextarea.value = before + definitionText + after;
           answerTextarea.selectionStart = answerTextarea.selectionEnd = insertPos + definitionText.length;
           answerTextarea.focus({ preventScroll: true });
           dispatchAnswerTextChanged(answerTextarea);

           // Modal'ı kapat
           let modalInstance = bootstrap.Modal.getInstance(definitionModalElem);
           if (modalInstance) {
             modalInstance.hide();
           }

           document.getElementById('definitionText').value = "";
           showToast("Tanım eklendi!", 'success');
         } else {
           showToast("Hata oluştu: " + JSON.stringify(data.errors || data.error || data), 'error');
         }
      })
      .catch(err => {
        console.error(err);
        showToast("Sunucu veya ağ hatası oluştu.", 'error');
      });
    });
  }


  // (E.2) TANIMLARIM Sekmesi (Kullanıcı Tanımları)
  // Arama + liste + radio buton + sayfalama
  var userDefTab           = document.getElementById('tanim-bul-tab');
  var userDefSearchInput   = document.getElementById('userDefSearchInput');
  var userDefinitionsList  = document.getElementById('userDefinitionsList');
  var userDefPagination    = document.getElementById('userDefPagination');
  var insertUserDefinitionBtn = document.getElementById('insertUserDefinitionBtn');

  if (userDefTab) {
    // Sekme açıldığında => 1. sayfa, boş arama
    userDefTab.addEventListener('show.bs.tab', function(e) {
      loadUserDefinitions(1, "");
      if (userDefSearchInput) {
        userDefSearchInput.value = "";
      }
    });
  }

  if (userDefSearchInput) {
    userDefSearchInput.addEventListener('keyup', function() {
      var q = this.value.trim();
      loadUserDefinitions(1, q);
    });
  }

  function loadUserDefinitions(page, q) {
    let url = `/get-user-definitions/?page=${page}`;
    if (q) url += `&q=${encodeURIComponent(q)}`;

    fetch(url)
      .then(res => res.json())
      .then(data => {
        // data: { definitions: [...], current_page, total_pages, ... }
        if (userDefinitionsList) {
          userDefinitionsList.innerHTML = '';
          if (!data.definitions || data.definitions.length === 0) {
            const emptyItem = document.createElement('li');
            emptyItem.className = 'list-group-item text-muted';
            emptyItem.textContent = 'Hiç tanım bulunamadı.';
            userDefinitionsList.appendChild(emptyItem);
          } else {
            data.definitions.forEach(function(d) {
              let shortDef = d.definition_text;
              if (shortDef.length > 50) {
                shortDef = shortDef.substring(0,50) + '...';
              }
              let li = document.createElement('li');
              li.classList.add('list-group-item');

              const wrapper = document.createElement('div');
              wrapper.className = 'form-check';

              const input = document.createElement('input');
              input.className = 'form-check-input';
              input.type = 'radio';
              input.name = 'userDef';
              input.value = JSON.stringify(d);
              input.id = `userDef_${d.id}`;

              const label = document.createElement('label');
              label.className = 'form-check-label';
              label.setAttribute('for', input.id);

              const strong = document.createElement('strong');
              strong.textContent = d.question_text;

              const em = document.createElement('em');
              em.textContent = ` (${shortDef})`;

              const small = document.createElement('small');
              small.className = 'text-muted';
              small.textContent = ` [Ben:${d.usage_count_self}, Tüm:${d.usage_count_all}]`;

              label.appendChild(strong);
              label.appendChild(em);
              label.appendChild(small);

              wrapper.appendChild(input);
              wrapper.appendChild(label);
              li.appendChild(wrapper);
              userDefinitionsList.appendChild(li);
            });
          }
        }

        // Sayfalama
        if (userDefPagination) {
          userDefPagination.innerHTML = '';
          if (data.total_pages > 1) {
            // Prev
            if (data.current_page > 1) {
              let prevBtn = document.createElement('button');
              prevBtn.classList.add('btn','btn-sm','btn-outline-theme-secondary','me-2');
              prevBtn.textContent = 'Önceki';
              prevBtn.addEventListener('click', function() {
                loadUserDefinitions(data.current_page - 1, userDefSearchInput.value.trim());
              });
              userDefPagination.appendChild(prevBtn);
            }
            // sayfa info
            let pageInfo = document.createElement('span');
            pageInfo.textContent = `Sayfa ${data.current_page} / ${data.total_pages}`;
            pageInfo.classList.add('me-2');
            userDefPagination.appendChild(pageInfo);

            // Next
            if (data.current_page < data.total_pages) {
              let nextBtn = document.createElement('button');
              nextBtn.classList.add('btn','btn-sm','btn-outline-theme-secondary');
              nextBtn.textContent = 'Sonraki';
              nextBtn.addEventListener('click', function() {
                loadUserDefinitions(data.current_page + 1, userDefSearchInput.value.trim());
              });
              userDefPagination.appendChild(nextBtn);
            }
          }
        }
      })
      .catch(err => {
        console.error(err);
        showToast("Tanımlar (kullanıcı) yüklenirken hata oluştu.", 'error');
      });
  }

  if (insertUserDefinitionBtn) {
    insertUserDefinitionBtn.addEventListener('click', function() {
      let checked = document.querySelector('input[name="userDef"]:checked');
      if (!checked) {
        showToast("Lütfen bir tanım seçiniz.", 'warning');
        return;
      }
      let item = JSON.parse(checked.value);
      let questionWord = item.question_text;
      let definitionId = item.id;

      let answerTextarea = document.querySelector('textarea[name="answer_text"]');
      if (!answerTextarea) {
        showToast("Yanıt textarea bulunamadı!", 'error');
        return;
      }

      let insertStr = ` (t:${questionWord}:${definitionId})`;

      // İmlecin bulunduğu konuma ekle
      let start = answerTextarea.selectionStart;
      let end = answerTextarea.selectionEnd;
      let before = answerTextarea.value.substring(0, start);
      let after = answerTextarea.value.substring(end);
      answerTextarea.value = before + insertStr + after;
      answerTextarea.selectionStart = answerTextarea.selectionEnd = start + insertStr.length;
      answerTextarea.focus({ preventScroll: true });
      dispatchAnswerTextChanged(answerTextarea);

      // Modal kapat
      let defModalInstance = bootstrap.Modal.getInstance(definitionModalElem);
      if (defModalInstance) {
        defModalInstance.hide();
      }
    });
  }


  // (E.3) GENEL TANIMLAR Sekmesi
  var allDefTab               = document.getElementById('genel-tanim-tab');
  var allDefSearchInput       = document.getElementById('allDefSearchInput');
  var allDefinitionsList      = document.getElementById('allDefinitionsList');
  var allDefPagination        = document.getElementById('allDefPagination');
  var insertGlobalDefinitionBtn = document.getElementById('insertGlobalDefinitionBtn');

  if (allDefTab) {
    allDefTab.addEventListener('show.bs.tab', function(e) {
      loadGlobalDefinitions(1, "");
      if(allDefSearchInput) {
        allDefSearchInput.value = "";
      }
    });
  }

  if (allDefSearchInput) {
    allDefSearchInput.addEventListener('keyup', function() {
      var query = this.value.trim();
      loadGlobalDefinitions(1, query);
    });
  }

  function loadGlobalDefinitions(page, query) {
    let url = '/get-all-definitions/?page=' + page;
    if (query) {
      url += '&q=' + encodeURIComponent(query);
    }

    fetch(url)
      .then(res => res.json())
      .then(data => {
        // data.definitions => [ {id, question_text, definition_text, username, usage_count_all}, ... ]
        if (allDefinitionsList) {
          allDefinitionsList.innerHTML = '';
          if (!data.definitions || data.definitions.length === 0) {
            const emptyItem = document.createElement('li');
            emptyItem.className = 'list-group-item text-muted';
            emptyItem.textContent = 'Hiç tanım bulunamadı.';
            allDefinitionsList.appendChild(emptyItem);
          } else {
            data.definitions.forEach(function(d) {
              let shortDef = d.definition_text;
              if (shortDef.length > 50) {
                shortDef = shortDef.substring(0,50) + '...';
              }
              let li = document.createElement('li');
              li.classList.add('list-group-item');

              const wrapper = document.createElement('div');
              wrapper.className = 'form-check';

              const input = document.createElement('input');
              input.className = 'form-check-input';
              input.type = 'radio';
              input.name = 'globalDef';
              input.value = JSON.stringify(d);
              input.id = `globalDef_${d.id}`;

              const label = document.createElement('label');
              label.className = 'form-check-label';
              label.setAttribute('for', input.id);

              const strong = document.createElement('strong');
              strong.textContent = d.question_text;

              const em = document.createElement('em');
              em.textContent = ` (${shortDef})`;

              const by = document.createElement('small');
              by.className = 'text-muted';
              by.textContent = ` by ${d.username}`;

              const usage = document.createElement('small');
              usage.className = 'ms-2';
              usage.textContent = ` [${d.usage_count_all} kez kullanılmış]`;

              label.appendChild(strong);
              label.appendChild(em);
              label.appendChild(by);
              label.appendChild(usage);

              wrapper.appendChild(input);
              wrapper.appendChild(label);
              li.appendChild(wrapper);
              allDefinitionsList.appendChild(li);
            });
          }
        }

        // Sayfalama
        if (allDefPagination) {
          allDefPagination.innerHTML = '';
          if (data.total_pages > 1) {
            // Prev
            if (data.current_page > 1) {
              let prevBtn = document.createElement('button');
              prevBtn.textContent = 'Önceki';
              prevBtn.classList.add('btn','btn-sm','btn-outline-theme-secondary','me-2');
              prevBtn.addEventListener('click', function(){
                loadGlobalDefinitions(data.current_page - 1, allDefSearchInput.value.trim());
              });
              allDefPagination.appendChild(prevBtn);
            }
            // Page Info
            let pageInfo = document.createElement('span');
            pageInfo.textContent = `Sayfa ${data.current_page} / ${data.total_pages}`;
            pageInfo.classList.add('me-2');
            allDefPagination.appendChild(pageInfo);

            // Next
            if (data.current_page < data.total_pages) {
              let nextBtn = document.createElement('button');
              nextBtn.textContent = 'Sonraki';
              nextBtn.classList.add('btn','btn-sm','btn-outline-theme-secondary');
              nextBtn.addEventListener('click', function(){
                loadGlobalDefinitions(data.current_page + 1, allDefSearchInput.value.trim());
              });
              allDefPagination.appendChild(nextBtn);
            }
          }
        }
      })
      .catch(err => {
        console.error(err);
        showToast("Genel tanımlar alınırken hata oluştu.", 'error');
      });
  }

  if (insertGlobalDefinitionBtn) {
    insertGlobalDefinitionBtn.addEventListener('click', function(e) {
      var checkedRadio = document.querySelector('input[name="globalDef"]:checked');
      if(!checkedRadio) {
        showToast("Lütfen bir tanım seçin.", 'warning');
        return;
      }
      var item = JSON.parse(checkedRadio.value);
      // item => {id, question_text, definition_text, usage_count_all, username...}
      var answerTextarea = document.querySelector('textarea[name="answer_text"]');
      if(!answerTextarea) {
        showToast("Yanıt textarea bulunamadı!", 'error');
        return;
      }
      var insertStr = ` (t:${item.question_text}:${item.id})`;

      // İmlecin bulunduğu konuma ekle
      var start = answerTextarea.selectionStart;
      var end = answerTextarea.selectionEnd;
      var before = answerTextarea.value.substring(0, start);
      var after = answerTextarea.value.substring(end);
      answerTextarea.value = before + insertStr + after;
      answerTextarea.selectionStart = answerTextarea.selectionEnd = start + insertStr.length;
      answerTextarea.focus({ preventScroll: true });
      dispatchAnswerTextChanged(answerTextarea);

      let defModalInstance = bootstrap.Modal.getInstance(definitionModalElem);
      if (defModalInstance) {
        defModalInstance.hide();
      }
    });
  }

  function initInlineAutocomplete() {
    var textarea = document.getElementById('id_answer_text') ||
      document.querySelector('textarea[name="answer_text"]');
    if (!textarea) return;

    var dropdown = document.createElement('div');
    dropdown.className = 'answer-inline-autocomplete';
    document.body.appendChild(dropdown);

    var state = {
      items: [],
      activeIndex: -1,
      start: 0,
      end: 0,
      prefix: '',
      query: '',
      requestToken: 0
    };
    var debounceTimer = null;

    function hideDropdown() {
      dropdown.classList.remove('show');
      dropdown.innerHTML = '';
      state.items = [];
      state.activeIndex = -1;
    }

    function positionDropdown() {
      var rect = textarea.getBoundingClientRect();
      var top = window.scrollY + rect.bottom + 8;
      if (top + dropdown.offsetHeight > window.scrollY + window.innerHeight - 16) {
        top = window.scrollY + rect.top - dropdown.offsetHeight - 8;
      }
      dropdown.style.top = top + 'px';
      dropdown.style.left = (window.scrollX + rect.left) + 'px';
      dropdown.style.width = Math.min(rect.width, 360) + 'px';
    }

    function getCaretContext() {
      var cursor = textarea.selectionStart || 0;
      var beforeCursor = textarea.value.slice(0, cursor);
      var match = beforeCursor.match(/(?:^|[\s(\[])([#@][0-9A-Za-zÇĞİÖŞÜçğıöşü_.-]{1,40})$/u);
      if (!match) return null;
      var token = match[1];
      return {
        prefix: token.charAt(0),
        query: token.slice(1),
        start: cursor - token.length,
        end: cursor
      };
    }

    function renderDropdown() {
      if (!state.items.length) {
        hideDropdown();
        return;
      }
      dropdown.innerHTML = '';
      state.items.forEach(function (item, index) {
        var button = document.createElement('button');
        button.type = 'button';
        button.className = 'answer-inline-autocomplete-item' + (index === state.activeIndex ? ' active' : '');
        button.innerHTML =
          '<span class="answer-inline-autocomplete-main">' +
            '<span class="answer-inline-autocomplete-label">' + item.label + '</span>' +
          '</span>' +
          '<span class="answer-inline-autocomplete-meta">' + item.meta + '</span>';
        button.addEventListener('mousedown', function (event) {
          event.preventDefault();
          applySelection(item);
        });
        dropdown.appendChild(button);
      });
      dropdown.classList.add('show');
      positionDropdown();
    }

    function applySelection(item) {
      var before = textarea.value.slice(0, state.start);
      var after = textarea.value.slice(state.end);
      var replacement = state.prefix + item.value + ' ';
      textarea.value = before + replacement + after;
      var caret = before.length + replacement.length;
      textarea.selectionStart = caret;
      textarea.selectionEnd = caret;
      textarea.focus({ preventScroll: true });
      dispatchAnswerTextChanged(textarea);
      hideDropdown();
    }

    function normalizeHashtagResults(data) {
      if (!data || !Array.isArray(data.hashtags)) return [];
      return data.hashtags.map(function (hashtag) {
        return {
          value: hashtag.name,
          label: '#' + hashtag.name,
          meta: (hashtag.usage_count || 0) + ' kullanım'
        };
      });
    }

    function normalizeUserResults(data) {
      if (!data || !Array.isArray(data.results)) return [];
      return data.results.map(function (user) {
        return {
          value: user.username,
          label: '@' + user.username,
          meta: 'kullanıcı'
        };
      });
    }

    function fetchSuggestions(context) {
      state.requestToken += 1;
      var currentToken = state.requestToken;
      var url = context.prefix === '#'
        ? '/hashtags/search/?q=' + encodeURIComponent(context.query)
        : '/user-search/?q=' + encodeURIComponent(context.query);

      fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
        .then(function (response) { return response.json(); })
        .then(function (data) {
          if (currentToken !== state.requestToken) return;
          state.items = context.prefix === '#'
            ? normalizeHashtagResults(data)
            : normalizeUserResults(data);
          state.activeIndex = state.items.length ? 0 : -1;
          renderDropdown();
        })
        .catch(function () {
          hideDropdown();
        });
    }

    function scheduleLookup() {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(function () {
        var context = getCaretContext();
        if (!context || !context.query.trim()) {
          hideDropdown();
          return;
        }
        state.start = context.start;
        state.end = context.end;
        state.prefix = context.prefix;
        state.query = context.query;
        fetchSuggestions(context);
      }, 140);
    }

    textarea.addEventListener('input', scheduleLookup);
    textarea.addEventListener('click', scheduleLookup);
    textarea.addEventListener('keyup', function (event) {
      if (['ArrowUp', 'ArrowDown', 'Enter', 'Escape', 'Tab'].indexOf(event.key) !== -1) return;
      scheduleLookup();
    });

    textarea.addEventListener('keydown', function (event) {
      if (!dropdown.classList.contains('show')) return;
      if (event.key === 'Escape') {
        hideDropdown();
        return;
      }
      if (event.key === 'ArrowDown') {
        event.preventDefault();
        state.activeIndex = (state.activeIndex + 1) % state.items.length;
        renderDropdown();
        return;
      }
      if (event.key === 'ArrowUp') {
        event.preventDefault();
        state.activeIndex = (state.activeIndex - 1 + state.items.length) % state.items.length;
        renderDropdown();
        return;
      }
      if (event.key === 'Enter' || event.key === 'Tab') {
        if (state.activeIndex < 0 || !state.items[state.activeIndex]) return;
        event.preventDefault();
        applySelection(state.items[state.activeIndex]);
      }
    });

    window.addEventListener('resize', function () {
      if (dropdown.classList.contains('show')) positionDropdown();
    });
    document.addEventListener('click', function (event) {
      if (event.target === textarea || dropdown.contains(event.target)) return;
      hideDropdown();
    });
  }

  initInlineAutocomplete();

});
