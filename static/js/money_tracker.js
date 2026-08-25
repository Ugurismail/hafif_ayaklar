(function () {
    'use strict';

    const app = document.getElementById('habitTrackerApp');
    if (!app) return;

    const refs = {
        habitTab: document.getElementById('habitTab'),
        moneyTab: document.getElementById('moneyTab'),
        habitView: document.getElementById('habitView'),
        moneyView: document.getElementById('moneyView'),
        habitActions: document.getElementById('habitHeaderActions'),
        moneyActions: document.getElementById('moneyHeaderActions'),
        status: document.getElementById('habitStatus'),
        createOpen: document.getElementById('moneyCreateOpen'),
        previousMonth: document.getElementById('moneyPreviousMonth'),
        nextMonth: document.getElementById('moneyNextMonth'),
        monthDisplay: document.getElementById('moneyMonthDisplay'),
        monthInput: document.getElementById('moneyMonthInput'),
        monthLabel: document.getElementById('moneyMonthLabel'),
        balance: document.getElementById('moneyBalance'),
        balanceContext: document.getElementById('moneyBalanceContext'),
        income: document.getElementById('moneyIncome'),
        expense: document.getElementById('moneyExpense'),
        transactionCount: document.getElementById('moneyTransactionCount'),
        trendChart: document.getElementById('moneyTrendChart'),
        breakdown: document.getElementById('moneyCategoryBreakdown'),
        transactionList: document.getElementById('moneyTransactionList'),
        searchInput: document.getElementById('moneySearchInput'),
        kindFilter: document.getElementById('moneyKindFilter'),
        editorModal: document.getElementById('moneyEditorModal'),
        editorForm: document.getElementById('moneyEditorForm'),
        editorId: document.getElementById('moneyEditorId'),
        editorKicker: document.getElementById('moneyEditorKicker'),
        editorTitle: document.getElementById('moneyEditorTitle'),
        kindControl: document.getElementById('moneyKindControl'),
        amountInput: document.getElementById('moneyAmountInput'),
        dateInput: document.getElementById('moneyDateInput'),
        categoryInput: document.getElementById('moneyCategoryInput'),
        noteInput: document.getElementById('moneyNoteInput'),
        deleteButton: document.getElementById('moneyDeleteButton'),
        categoryToggle: document.getElementById('moneyCategoryCreateToggle'),
        categoryFields: document.getElementById('moneyCategoryCreateFields'),
        categoryName: document.getElementById('moneyCategoryNameInput'),
        categorySubmit: document.getElementById('moneyCategoryCreateSubmit'),
    };
    const urls = {
        list: app.dataset.moneyListUrl,
        create: app.dataset.moneyCreateUrl,
        update: app.dataset.moneyUpdateUrlTemplate,
        delete: app.dataset.moneyDeleteUrlTemplate,
        category: app.dataset.moneyCategoryUrl,
    };
    const svgNamespace = 'http://www.w3.org/2000/svg';
    const moneyFormatter = new Intl.NumberFormat('tr-TR', {
        style: 'currency',
        currency: 'TRY',
        minimumFractionDigits: 2,
    });
    const monthFormatter = new Intl.DateTimeFormat('tr-TR', {
        month: 'long',
        year: 'numeric',
    });
    const dayFormatter = new Intl.DateTimeFormat('tr-TR', {
        day: 'numeric',
        month: 'short',
    });
    let moneyState = null;
    let selectedKind = 'expense';
    let editorModal = null;
    let activeView = new URL(window.location.href).searchParams.get('view') === 'money' ? 'money' : 'habits';

    function element(tagName, className, text) {
        const node = document.createElement(tagName);
        if (className) node.className = className;
        if (text !== undefined && text !== null) node.textContent = text;
        return node;
    }

    function icon(name) {
        const node = document.createElement('i');
        node.className = `bi bi-${name}`;
        node.setAttribute('aria-hidden', 'true');
        return node;
    }

    function svgElement(tagName, attributes) {
        const node = document.createElementNS(svgNamespace, tagName);
        Object.entries(attributes || {}).forEach(([name, value]) => node.setAttribute(name, value));
        return node;
    }

    function csrfToken() {
        const meta = document.querySelector('meta[name="csrf-token"]');
        return meta ? meta.content : '';
    }

    function setBusy(isBusy) {
        app.classList.toggle('is-busy', isBusy);
        app.setAttribute('aria-busy', isBusy ? 'true' : 'false');
    }

    function setStatus(message, type) {
        refs.status.textContent = message || '';
        refs.status.classList.toggle('is-error', type === 'error');
        if (message && typeof window.showToast === 'function') {
            window.showToast(message, type || 'success');
        }
    }

    function endpoint(template, id) {
        return template.replace('/0/', `/${id}/`);
    }

    async function jsonRequest(url, options) {
        const response = await fetch(url, {
            credentials: 'same-origin',
            headers: {
                'Accept': 'application/json',
                ...(options && options.method === 'POST' ? {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken(),
                } : {}),
            },
            ...options,
        });
        const contentType = response.headers.get('content-type') || '';
        const payload = contentType.includes('application/json') ? await response.json() : null;
        if (!response.ok) throw new Error((payload && payload.error) || 'İşlem tamamlanamadı.');
        return payload;
    }

    function currency(value) {
        return moneyFormatter.format(Number(value || 0));
    }

    function parseDate(value) {
        return new Date(`${value}T12:00:00`);
    }

    function addMonths(month, amount) {
        const [year, monthNumber] = month.split('-').map(Number);
        const date = new Date(year, monthNumber - 1 + amount, 1, 12);
        return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
    }

    function selectedMonthDate() {
        return parseDate(`${moneyState.month}-01`);
    }

    function showView(view) {
        activeView = view === 'money' ? 'money' : 'habits';
        const moneyActive = activeView === 'money';
        refs.habitView.hidden = moneyActive;
        refs.moneyView.hidden = !moneyActive;
        refs.habitActions.hidden = moneyActive;
        refs.moneyActions.hidden = !moneyActive;
        refs.habitTab.classList.toggle('is-active', !moneyActive);
        refs.moneyTab.classList.toggle('is-active', moneyActive);
        refs.habitTab.setAttribute('aria-selected', moneyActive ? 'false' : 'true');
        refs.moneyTab.setAttribute('aria-selected', moneyActive ? 'true' : 'false');

        const url = new URL(window.location.href);
        if (moneyActive) url.searchParams.set('view', 'money');
        else url.searchParams.delete('view');
        window.history.replaceState({}, '', url);
        if (moneyActive && !moneyState) loadMoney();
    }

    function renderSummary() {
        const summary = moneyState.summary || {};
        const balance = Number(summary.balance || 0);
        refs.balance.textContent = currency(balance);
        refs.balance.classList.toggle('is-negative', balance < 0);
        refs.income.textContent = currency(summary.income);
        refs.expense.textContent = currency(summary.expense);
        refs.transactionCount.textContent = summary.transactionCount || 0;
        if (summary.expenseChange === null || summary.expenseChange === undefined) {
            refs.balanceContext.textContent = 'Bu ayın dengesi';
        } else if (summary.expenseChange === 0) {
            refs.balanceContext.textContent = 'Gider geçen ayla aynı';
        } else {
            refs.balanceContext.textContent = `Gider geçen aya göre %${Math.abs(summary.expenseChange)} ${summary.expenseChange > 0 ? 'fazla' : 'az'}`;
        }
    }

    function renderMonth() {
        refs.monthInput.value = moneyState.month;
        refs.monthInput.max = moneyState.today.slice(0, 7);
        refs.monthLabel.textContent = monthFormatter.format(selectedMonthDate());
        refs.nextMonth.disabled = moneyState.month >= moneyState.today.slice(0, 7);
    }

    function renderTrend() {
        refs.trendChart.replaceChildren();
        const daily = moneyState.daily || [];
        const hasMovement = daily.some((item) => Number(item.expense) || Number(item.income));
        if (!hasMovement) {
            const empty = element('div', 'money-empty-state money-chart-empty');
            empty.append(
                icon('bar-chart-line'),
                element('strong', '', 'Bu ay henüz hareket yok'),
                element('span', '', 'İlk kayıt eklendiğinde günlük akış burada oluşur.'),
            );
            refs.trendChart.append(empty);
            return;
        }
        const width = 760;
        const height = 250;
        const margin = { top: 16, right: 14, bottom: 30, left: 56 };
        const plotWidth = width - margin.left - margin.right;
        const plotHeight = height - margin.top - margin.bottom;
        const maxValue = Math.max(1, ...daily.flatMap((item) => [Number(item.expense), Number(item.income)]));
        const svg = svgElement('svg', {
            viewBox: `0 0 ${width} ${height}`,
            role: 'img',
            'aria-label': 'Seçilen ayın günlük gelir ve giderleri',
            preserveAspectRatio: 'none',
        });

        [0, .5, 1].forEach((ratio) => {
            const y = margin.top + plotHeight - (plotHeight * ratio);
            svg.append(svgElement('line', {
                x1: margin.left,
                y1: y,
                x2: width - margin.right,
                y2: y,
                class: 'money-chart-grid-line',
            }));
            const label = svgElement('text', {
                x: margin.left - 8,
                y: y + 4,
                class: 'money-chart-label',
                'text-anchor': 'end',
            });
            label.textContent = ratio === 0 ? '₺0' : `₺${Math.round(maxValue * ratio).toLocaleString('tr-TR')}`;
            svg.append(label);
        });

        const step = plotWidth / Math.max(1, daily.length);
        const barWidth = Math.max(3, Math.min(11, step * .32));
        daily.forEach((item, index) => {
            if (item.future) return;
            const x = margin.left + (index * step) + (step / 2);
            [['expense', -barWidth * .58], ['income', barWidth * .58]].forEach(([kind, offset]) => {
                const amount = Number(item[kind]);
                const barHeight = (amount / maxValue) * plotHeight;
                const bar = svgElement('rect', {
                    x: x + offset - (barWidth / 2),
                    y: margin.top + plotHeight - barHeight,
                    width: barWidth,
                    height: Math.max(amount ? 2 : 0, barHeight),
                    rx: Math.min(3, barWidth / 2),
                    class: `money-chart-bar is-${kind}`,
                });
                const title = svgElement('title');
                title.textContent = `${item.date} · ${kind === 'expense' ? 'Gider' : 'Gelir'}: ${currency(amount)}`;
                bar.append(title);
                svg.append(bar);
            });
            if (index === 0 || index === daily.length - 1 || index % 5 === 4) {
                const label = svgElement('text', {
                    x,
                    y: height - 8,
                    class: 'money-chart-label',
                    'text-anchor': 'middle',
                });
                label.textContent = item.label;
                svg.append(label);
            }
        });
        refs.trendChart.append(svg);
    }

    function renderBreakdown() {
        refs.breakdown.replaceChildren();
        const items = moneyState.breakdown || [];
        if (!items.length) {
            const empty = element('div', 'money-empty-state');
            empty.append(icon('pie-chart'), element('strong', '', 'Henüz gider yok'), element('span', '', 'Kategoriler ilk gider kaydından sonra burada karşılaştırılır.'));
            refs.breakdown.append(empty);
            return;
        }
        items.slice(0, 8).forEach((item) => {
            const row = element('div', 'money-category-row');
            row.style.setProperty('--category-color', item.color);
            const categoryIcon = element('span', 'money-category-icon');
            categoryIcon.append(icon(item.icon));
            const copy = element('div', 'money-category-copy');
            copy.append(element('strong', '', item.name), element('span', '', `%${item.rate}`));
            const track = element('span', 'money-category-track');
            const fill = document.createElement('i');
            fill.style.setProperty('--category-rate', `${item.rate}%`);
            track.append(fill);
            row.append(categoryIcon, copy, element('b', '', currency(item.total)), track);
            refs.breakdown.append(row);
        });
    }

    function matchesFilters(item) {
        const kind = refs.kindFilter.value;
        if (kind !== 'all' && item.kind !== kind) return false;
        const query = refs.searchInput.value.trim().toLocaleLowerCase('tr-TR');
        if (!query) return true;
        return `${item.note} ${item.category ? item.category.name : ''}`.toLocaleLowerCase('tr-TR').includes(query);
    }

    function renderTransactions() {
        refs.transactionList.replaceChildren();
        const items = (moneyState.transactions || []).filter(matchesFilters);
        if (!items.length) {
            const empty = element('button', 'money-ledger-empty');
            empty.type = 'button';
            empty.dataset.moneyCreate = 'true';
            empty.append(icon('receipt-cutoff'), element('strong', '', 'Bu görünümde kayıt yok'), element('span', '', 'İlk gelir veya gider hareketini ekle.'));
            refs.transactionList.append(empty);
            return;
        }
        items.forEach((item) => {
            const row = element('button', `money-transaction-row is-${item.kind}`);
            row.type = 'button';
            row.dataset.transactionId = item.id;
            row.setAttribute('aria-label', `${item.category ? item.category.name : 'Kategorisiz'} kaydını düzenle`);
            const categoryIcon = element('span', 'money-transaction-icon');
            categoryIcon.style.setProperty('--transaction-color', item.category ? item.category.color : '#4E5968');
            categoryIcon.append(icon(item.category ? item.category.icon : 'tag'));
            const copy = element('span', 'money-transaction-copy');
            copy.append(
                element('strong', '', item.note || (item.category ? item.category.name : 'Kategorisiz')),
                element('small', '', `${item.category ? item.category.name : 'Kategorisiz'} · ${dayFormatter.format(parseDate(item.date))}`),
            );
            const amount = element('b', '', `${item.kind === 'expense' ? '−' : '+'}${currency(item.amount)}`);
            row.append(categoryIcon, copy, amount, icon('chevron-right'));
            refs.transactionList.append(row);
        });
    }

    function renderCategories(selectedId) {
        refs.categoryInput.replaceChildren();
        (moneyState.categories || []).filter((item) => item.kind === selectedKind).forEach((item) => {
            const option = document.createElement('option');
            option.value = item.id;
            option.textContent = item.name;
            refs.categoryInput.append(option);
        });
        if (selectedId && refs.categoryInput.querySelector(`option[value="${selectedId}"]`)) {
            refs.categoryInput.value = String(selectedId);
        }
    }

    function render() {
        renderMonth();
        renderSummary();
        renderTrend();
        renderBreakdown();
        renderTransactions();
    }

    async function loadMoney(month) {
        setBusy(true);
        try {
            const url = new URL(urls.list, window.location.origin);
            if (month) url.searchParams.set('month', month);
            const result = await jsonRequest(url.toString());
            moneyState = result.data;
            render();
            refs.status.textContent = '';
        } catch (error) {
            setStatus(error.message, 'error');
        } finally {
            setBusy(false);
        }
    }

    async function mutate(url, payload, fallbackMessage) {
        setBusy(true);
        try {
            const result = await jsonRequest(url, {
                method: 'POST',
                body: JSON.stringify({ ...payload, month: moneyState.month }),
            });
            if (result.data) {
                moneyState = result.data;
                render();
            }
            setStatus(result.message || fallbackMessage, 'success');
            return result;
        } catch (error) {
            setStatus(error.message, 'error');
            return null;
        } finally {
            setBusy(false);
        }
    }

    function setKind(kind, categoryId) {
        selectedKind = kind === 'income' ? 'income' : 'expense';
        refs.kindControl.querySelectorAll('[data-money-kind]').forEach((button) => {
            const active = button.dataset.moneyKind === selectedKind;
            button.classList.toggle('is-active', active);
            button.setAttribute('aria-pressed', active ? 'true' : 'false');
        });
        renderCategories(categoryId);
    }

    function defaultTransactionDate() {
        const todayMonth = moneyState.today.slice(0, 7);
        if (moneyState.month === todayMonth) return moneyState.today;
        const [year, month] = moneyState.month.split('-').map(Number);
        return `${moneyState.month}-${String(new Date(year, month, 0).getDate()).padStart(2, '0')}`;
    }

    function openEditor(item) {
        refs.editorForm.reset();
        refs.editorId.value = item ? item.id : '';
        refs.editorKicker.textContent = item ? 'Düzenleme' : 'Yeni hareket';
        refs.editorTitle.textContent = item ? (item.note || (item.category && item.category.name) || 'Para hareketi') : 'Para hareketi ekle';
        refs.amountInput.value = item ? item.amount : '';
        refs.dateInput.value = item ? item.date : defaultTransactionDate();
        refs.dateInput.max = moneyState.today;
        refs.noteInput.value = item ? item.note : '';
        refs.deleteButton.hidden = !item;
        refs.categoryFields.hidden = true;
        refs.categoryName.value = '';
        setKind(item ? item.kind : 'expense', item && item.category ? item.category.id : null);
        if (!editorModal) editorModal = new bootstrap.Modal(refs.editorModal);
        editorModal.show();
        window.setTimeout(() => refs.amountInput.focus(), 180);
    }

    refs.habitTab.addEventListener('click', () => showView('habits'));
    refs.moneyTab.addEventListener('click', () => showView('money'));
    refs.createOpen.addEventListener('click', () => {
        if (moneyState) openEditor(null);
    });
    refs.previousMonth.addEventListener('click', () => loadMoney(addMonths(moneyState.month, -1)));
    refs.nextMonth.addEventListener('click', () => {
        if (moneyState.month < moneyState.today.slice(0, 7)) loadMoney(addMonths(moneyState.month, 1));
    });
    refs.monthDisplay.addEventListener('click', () => loadMoney(moneyState.today.slice(0, 7)));
    refs.monthInput.addEventListener('change', () => {
        if (refs.monthInput.value) loadMoney(refs.monthInput.value);
    });
    refs.searchInput.addEventListener('input', renderTransactions);
    refs.kindFilter.addEventListener('change', renderTransactions);
    refs.transactionList.addEventListener('click', (event) => {
        if (event.target.closest('[data-money-create]')) {
            openEditor(null);
            return;
        }
        const row = event.target.closest('[data-transaction-id]');
        if (!row) return;
        const item = (moneyState.transactions || []).find((candidate) => candidate.id === Number(row.dataset.transactionId));
        if (item) openEditor(item);
    });
    refs.kindControl.addEventListener('click', (event) => {
        const button = event.target.closest('[data-money-kind]');
        if (button) setKind(button.dataset.moneyKind);
    });
    refs.categoryToggle.addEventListener('click', () => {
        refs.categoryFields.hidden = !refs.categoryFields.hidden;
        if (!refs.categoryFields.hidden) refs.categoryName.focus();
    });
    refs.categorySubmit.addEventListener('click', async () => {
        const result = await mutate(urls.category, {
            kind: selectedKind,
            name: refs.categoryName.value,
        }, 'Kategori eklendi.');
        if (!result || !result.category) return;
        moneyState.categories.push(result.category);
        renderCategories(result.category.id);
        refs.categoryFields.hidden = true;
        refs.categoryName.value = '';
    });
    refs.editorForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const itemId = Number(refs.editorId.value || 0);
        const result = await mutate(itemId ? endpoint(urls.update, itemId) : urls.create, {
            kind: selectedKind,
            amount: refs.amountInput.value,
            date: refs.dateInput.value,
            categoryId: refs.categoryInput.value,
            note: refs.noteInput.value,
        }, itemId ? 'Para hareketi güncellendi.' : 'Para hareketi eklendi.');
        if (result && editorModal) editorModal.hide();
    });
    refs.deleteButton.addEventListener('click', async () => {
        const itemId = Number(refs.editorId.value || 0);
        if (!itemId || !window.confirm('Bu para hareketi kalıcı olarak silinsin mi?')) return;
        const result = await mutate(endpoint(urls.delete, itemId), {}, 'Para hareketi silindi.');
        if (result && editorModal) editorModal.hide();
    });

    showView(activeView);
}());
