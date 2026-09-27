(function () {
  'use strict';

  document.addEventListener('click', async function (event) {
    const button = event.target.closest('[data-copy-entry-reference]');
    if (!button || button.disabled) return;
    const reference = button.dataset.copyEntryReference;
    if (!/^#[1-9][0-9]{0,9}$/.test(reference)) return;
    event.preventDefault();
    button.disabled = true;
    try {
      await navigator.clipboard.writeText(reference);
      showToast(reference + ' referansı kopyalandı.', 'success');
    } catch (error) {
      showToast('Kopyalanamadı. Referans: ' + reference, 'error');
    } finally {
      button.disabled = false;
    }
  });
}());
