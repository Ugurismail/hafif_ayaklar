(function () {
    'use strict';
    if (window.ReferenceHistory) return;
    let retry = null;
    function context(textarea) {
        const form = textarea.form;
        if (!form) throw new Error('Yazı formu bulunamadı.');
        let field = form.querySelector('[name="reference_context"]');
        if (!field) {
            field = document.createElement('input');
            field.type = 'hidden'; field.name = 'reference_context';
            field.value = document.getElementById('kaynakRefModal').dataset.referenceContext || crypto.randomUUID();
            form.appendChild(field);
        }
        return field.value;
    }
    window.ReferenceHistory = {
        async record(textarea, reference, page) {
            const modal = document.getElementById('kaynakRefModal');
            const contextId = context(textarea);
            const key = JSON.stringify([contextId, reference, page]);
            if (!retry || retry.key !== key) retry = {key, id: crypto.randomUUID()};
            const title = textarea.form.querySelector('[name="question_text"]')?.value || modal.dataset.referenceTitle || '';
            const buttons = Array.from(textarea.form.querySelectorAll('button')).map(button => [button, button.disabled]);
            const wasReadOnly = textarea.readOnly;
            const preventSubmit = event => { event.preventDefault(); event.stopImmediatePropagation(); };
            textarea.form.addEventListener('submit', preventSubmit, true);
            buttons.forEach(([button]) => { button.disabled = true; });
            textarea.readOnly = true;
            const controller = new AbortController();
            const timeout = setTimeout(() => controller.abort(), 15000);
            try {
                const response = await fetch(modal.dataset.historyUrl, {
                    method: 'POST', credentials: 'same-origin', signal: controller.signal,
                    headers: {'Content-Type': 'application/json', 'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content},
                    body: JSON.stringify({event_id: retry.id, context_id: contextId, reference_id: Number(reference),
                        page, title: title.slice(0, 200), draft_id: new URL(location.href).searchParams.get('draft_id')}),
                });
                if (!response.headers.get('content-type')?.includes('application/json')) throw new Error('Oturumunu kontrol edip tekrar dene.');
                const data = await response.json();
                if (!response.ok) throw new Error(data.error || 'Kaynak geçmişi kaydedilemedi.');
                retry = null;
                return data;
            } catch (error) {
                if (error.name === 'AbortError' || error instanceof TypeError) throw new Error('Bağlantı kurulamadı. Kaynak metne eklenmedi; tekrar dene.');
                throw error;
            } finally {
                clearTimeout(timeout);
                buttons.forEach(([button, disabled]) => { button.disabled = disabled; });
                textarea.readOnly = wasReadOnly;
                textarea.form.removeEventListener('submit', preventSubmit, true);
            }
        },
    };
    document.addEventListener('DOMContentLoaded', function () {
        const textarea = document.getElementById('id_answer_text');
        if (textarea?.form && document.getElementById('kaynakRefModal')?.dataset.referenceContext) context(textarea);
    });
}());
