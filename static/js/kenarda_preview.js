// static/js/kenarda_preview.js
// Server-side draft preview helper (Kenarda)

(function () {
  function getCsrfToken() {
    return (
      document.querySelector('meta[name="csrf-token"]')?.content ||
      document.querySelector('input[name="csrfmiddlewaretoken"]')?.value ||
      ''
    );
  }

  function reinitBootstrapOverlays(root) {
    if (!root || typeof bootstrap === 'undefined') return;

    // Dispose existing instances within root to avoid duplicates
    root.querySelectorAll('[data-bs-toggle="tooltip"]').forEach((el) => {
      const inst = bootstrap.Tooltip.getInstance(el);
      if (inst) inst.dispose();
      const wantsHtml = (el.getAttribute('data-bs-html') || '').toLowerCase() === 'true';
      new bootstrap.Tooltip(el, {
        container: 'body',
        trigger: 'hover focus',
        html: wantsHtml,
        delay: { show: 500, hide: 100 },
      });
    });

    root.querySelectorAll('[data-bs-toggle="popover"]').forEach((el) => {
      const inst = bootstrap.Popover.getInstance(el);
      if (inst) inst.dispose();
      new bootstrap.Popover(el, {
        container: 'body',
        html: true,
        trigger: el.getAttribute('data-bs-trigger') || 'hover focus',
      });
    });
  }

  function preventPreviewNavigation(root) {
    if (!root) return;
    if (root.dataset.kenardaPreviewNavBound === '1') return;
    root.dataset.kenardaPreviewNavBound = '1';

    root.addEventListener('click', function (e) {
      const anchor = e.target && e.target.closest ? e.target.closest('a') : null;
      if (!anchor) return;
      e.preventDefault();
      e.stopPropagation();
    });
  }

  async function updateKenardaPreview(payload, options = {}) {
    const rootId = options.rootId || 'kenarda-preview-root';
    const root = document.getElementById(rootId);
    if (!root) return;

    preventPreviewNavigation(root);

    try {
      const res = await fetch('/kenarda/preview/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify(payload || {}),
      });

      const data = await res.json().catch(() => null);
      if (!res.ok || !data || data.status !== 'ok') {
        return;
      }

      root.innerHTML = data.html || '';
      root.style.display = root.innerHTML ? 'block' : 'none';
      reinitBootstrapOverlays(root);
    } catch (e) {
      // silent
    }
  }

  window.kenardaUpdatePreview = updateKenardaPreview;
})();
