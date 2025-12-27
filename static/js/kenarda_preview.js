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
      new bootstrap.Tooltip(el, {
        trigger: 'hover',
        delay: { show: 500, hide: 100 },
      });
    });

    root.querySelectorAll('[data-bs-toggle="popover"]').forEach((el) => {
      const inst = bootstrap.Popover.getInstance(el);
      if (inst) inst.dispose();
      new bootstrap.Popover(el);
    });
  }

  async function updateKenardaPreview(payload, options = {}) {
    const rootId = options.rootId || 'kenarda-preview-root';
    const root = document.getElementById(rootId);
    if (!root) return;

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

