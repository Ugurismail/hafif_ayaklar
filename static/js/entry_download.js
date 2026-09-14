(function () {
  'use strict';

  const mimeTypes = {
    pdf: 'application/pdf',
    docx: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    xlsx: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    json: 'application/json',
  };

  window.requestEntryDownload = async function ({url, format, body, signal}) {
    const response = await fetch(url, {
      method: 'POST', body, signal, credentials: 'same-origin', cache: 'no-store',
    });
    if (response.redirected || response.status === 401 || response.status === 403) {
      throw new Error('Oturumunuzu ve indirme yetkinizi kontrol edip tekrar deneyin.');
    }
    const type = (response.headers.get('Content-Type') || '').split(';')[0].trim();
    if (!response.ok) {
      if (response.status === 503 && type === 'text/plain') {
        const message = (await response.text()).trim();
        if (message && message.length <= 500) throw new Error(message);
      }
      throw new Error('Dosya hazırlanamadı. Seçimleriniz korundu; lütfen tekrar deneyin.');
    }
    const disposition = response.headers.get('Content-Disposition') || '';
    if (type !== mimeTypes[format] || !/^attachment\s*(;|$)/i.test(disposition)) {
      throw new Error('Sunucu bir indirme dosyası döndürmedi. Lütfen oturumunuzu kontrol edin.');
    }
    let filename = `entryler.${format}`;
    const extended = disposition.match(/filename\*=UTF-8''([^;]+)/i);
    const quoted = disposition.match(/filename="([^"]+)"/i);
    try {
      filename = extended ? decodeURIComponent(extended[1]) : (quoted ? quoted[1] : filename);
    } catch (_) { /* Keep the fallback if the header is malformed. */ }
    filename = filename.replace(/[\\/\u0000-\u001f]/g, '_');
    const blob = await response.blob();
    if (!blob.size) throw new Error('İndirme dosyası boş geldi. Lütfen tekrar deneyin.');
    return {blob, filename};
  };
})();
