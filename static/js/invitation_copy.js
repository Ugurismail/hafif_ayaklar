(() => {
  'use strict';
  if (window.invitationCopyReady) return;
  window.invitationCopyReady = true;
  document.addEventListener('click', async (event) => {
    const button = event.target.closest('[data-copy-invitation]');
    if (!button || button.disabled) return;
    const status = button.parentElement.querySelector('[data-copy-status]');
    button.disabled = true;
    try {
      await navigator.clipboard.writeText(button.dataset.copyInvitation);
      status.textContent = 'Kopyalandı';
      button.querySelector('i').className = 'bi bi-check2';
      button.title = 'Kopyalandı';
      window.setTimeout(() => {
        button.querySelector('i').className = 'bi bi-clipboard';
        button.title = 'Davet kodunu kopyala';
      }, 1800);
    } catch (_) {
      status.textContent = 'Kopyalanamadı; kodu seçerek kopyalayın.';
      button.title = status.textContent;
    } finally {
      button.disabled = false;
    }
  });
})();
