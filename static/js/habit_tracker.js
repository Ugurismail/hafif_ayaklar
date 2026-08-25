(function () {
    'use strict';

    const app = document.getElementById('habitTrackerApp');
    const initialDataNode = document.getElementById('habitTrackerInitialData');
    if (!app || !initialDataNode) return;

    const refs = {
        list: document.getElementById('habitList'),
        listCount: document.getElementById('habitListCount'),
        archiveCount: document.getElementById('habitArchiveCount'),
        summaryRing: document.getElementById('habitSummaryRing'),
        summaryRate: document.getElementById('habitSummaryRate'),
        completedCount: document.getElementById('habitCompletedCount'),
        scheduledCount: document.getElementById('habitScheduledCount'),
        streakCount: document.getElementById('habitStreakCount'),
        weekRate: document.getElementById('habitWeekRate'),
        activeCount: document.getElementById('habitActiveCount'),
        weekdayChart: document.getElementById('habitWeekdayChart'),
        trendChart: document.getElementById('habitTrendChart'),
        heatmap: document.getElementById('habitHeatmap'),
        status: document.getElementById('habitStatus'),
        dateLabel: document.getElementById('habitDateLabel'),
        dateContext: document.getElementById('habitDateContext'),
        dateInput: document.getElementById('habitDateInput'),
        previousDate: document.getElementById('habitPreviousDate'),
        nextDate: document.getElementById('habitNextDate'),
        dateDisplay: document.getElementById('habitDateDisplay'),
        createOpen: document.getElementById('habitCreateOpen'),
        archiveOpen: document.getElementById('habitArchiveOpen'),
        editorModal: document.getElementById('habitEditorModal'),
        dayModal: document.getElementById('habitDayModal'),
        archiveModal: document.getElementById('habitArchiveModal'),
        editorForm: document.getElementById('habitEditorForm'),
        editorId: document.getElementById('habitEditorId'),
        editorKicker: document.getElementById('habitEditorKicker'),
        editorTitle: document.getElementById('habitEditorTitle'),
        editorSubmit: document.getElementById('habitEditorSubmit'),
        nameInput: document.getElementById('habitNameInput'),
        descriptionInput: document.getElementById('habitDescriptionInput'),
        targetInput: document.getElementById('habitTargetInput'),
        unitInput: document.getElementById('habitUnitInput'),
        startDateInput: document.getElementById('habitStartDateInput'),
        iconChoices: document.getElementById('habitIconChoices'),
        colorChoices: document.getElementById('habitColorChoices'),
        frequencyControl: document.getElementById('habitFrequencyControl'),
        weekdayChoices: document.getElementById('habitWeekdayChoices'),
        archiveButton: document.getElementById('habitArchiveButton'),
        deleteButton: document.getElementById('habitDeleteButton'),
        archiveList: document.getElementById('habitArchiveList'),
        dayForm: document.getElementById('habitDayForm'),
        dayId: document.getElementById('habitDayId'),
        dayDate: document.getElementById('habitDayDate'),
        dayTitle: document.getElementById('habitDayTitle'),
        dayTargetInput: document.getElementById('habitDayTargetInput'),
        dayValueInput: document.getElementById('habitDayValueInput'),
        dayNoteInput: document.getElementById('habitDayNoteInput'),
        dayTargetUnit: document.getElementById('habitDayTargetUnit'),
        dayValueUnit: document.getElementById('habitDayValueUnit'),
        dayDefaultHint: document.getElementById('habitDayDefaultHint'),
        dayUseDefault: document.getElementById('habitDayUseDefault'),
    };

    const urls = {
        list: app.dataset.listUrl,
        create: app.dataset.createUrl,
        update: app.dataset.updateUrlTemplate,
        log: app.dataset.logUrlTemplate,
        archive: app.dataset.archiveUrlTemplate,
        delete: app.dataset.deleteUrlTemplate,
    };
    const svgNamespace = 'http://www.w3.org/2000/svg';
    const weekdayLong = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar'];
    let state = JSON.parse(initialDataNode.textContent || '{}');
    let selectedIcon = 'check2-circle';
    let selectedColor = '#2F6B4F';
    let selectedFrequency = 'daily';
    let selectedDays = new Set();
    let editorModal = null;
    let dayModal = null;
    let archiveModal = null;

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

    function parseLocalDate(isoDate) {
        return new Date(`${isoDate}T12:00:00`);
    }

    function formatLocalDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    function addDays(isoDate, amount) {
        const date = parseLocalDate(isoDate);
        date.setDate(date.getDate() + amount);
        return formatLocalDate(date);
    }

    function endpoint(template, habitId) {
        return template.replace('/0/', `/${habitId}/`);
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
        if (!response.ok) {
            throw new Error((payload && payload.error) || 'İşlem tamamlanamadı.');
        }
        return payload;
    }

    async function mutate(url, payload, fallbackMessage) {
        setBusy(true);
        try {
            const result = await jsonRequest(url, {
                method: 'POST',
                body: JSON.stringify({
                    ...payload,
                    date: state.selectedDate,
                    range: state.range,
                }),
            });
            if (result.data) {
                state = result.data;
                render();
            }
            setStatus(result.message || fallbackMessage || 'Kaydedildi.', 'success');
            return true;
        } catch (error) {
            setStatus(error.message, 'error');
            return false;
        } finally {
            setBusy(false);
        }
    }

    function renderSummary() {
        const summary = state.summary || {};
        const rate = Number(summary.rate || 0);
        refs.summaryRing.style.setProperty('--habit-rate', rate);
        refs.summaryRate.textContent = `%${rate}`;
        refs.completedCount.textContent = summary.completed || 0;
        refs.scheduledCount.textContent = ` / ${summary.scheduled || 0}`;
        refs.streakCount.textContent = summary.streak || 0;
        refs.weekRate.textContent = `%${summary.weekRate || 0}`;
        refs.activeCount.textContent = summary.active || 0;
    }

    function renderDate() {
        refs.dateLabel.textContent = state.dateLabel || state.selectedDate;
        refs.dateInput.value = state.selectedDate;
        refs.dateInput.max = state.today;
        refs.nextDate.disabled = state.selectedDate >= state.today;

        if (state.selectedDate === state.today) {
            refs.dateContext.textContent = 'Bugün';
        } else if (addDays(state.today, -1) === state.selectedDate) {
            refs.dateContext.textContent = 'Dün';
        } else {
            refs.dateContext.textContent = weekdayLong[parseLocalDate(state.selectedDate).getDay() === 0 ? 6 : parseLocalDate(state.selectedDate).getDay() - 1];
        }
    }

    function miniChart(habit) {
        const chart = element('div', 'habit-mini-chart');
        chart.setAttribute('aria-label', `${habit.name} son yedi gün`);
        habit.mini.forEach((day) => {
            const item = element('span', `habit-mini-day${day.scheduled ? '' : ' is-off'}`);
            item.title = day.scheduled
                ? `${day.label}: ${day.value} / ${day.target} ${habit.unit} (%${day.rate})`
                : `${day.label}: planlı değil`;
            const bar = document.createElement('i');
            bar.style.height = `${Math.max(3, Math.round(day.rate * 0.31))}px`;
            item.append(bar, element('span', '', day.label.slice(0, 1)));
            chart.append(item);
        });
        return chart;
    }

    function actionButton(action, iconName, label, disabled) {
        const button = element('button', 'habit-action-button');
        button.type = 'button';
        button.dataset.action = action;
        button.title = label;
        button.setAttribute('aria-label', label);
        button.disabled = Boolean(disabled);
        button.append(icon(iconName));
        return button;
    }

    function renderHabitRow(habit) {
        const row = element('article', 'habit-row');
        row.dataset.habitId = habit.id;
        row.style.setProperty('--row-color', habit.color);
        row.classList.toggle('is-complete', habit.completed);
        row.classList.toggle('is-unscheduled', !habit.scheduled);

        const rowIcon = element('span', 'habit-row-icon');
        rowIcon.append(icon(habit.icon));

        const copy = element('div', 'habit-row-copy');
        const titleWrap = element('div', 'habit-row-title');
        titleWrap.append(element('h3', '', habit.name));
        if (habit.completed) {
            const completeMark = icon('check-circle-fill');
            completeMark.classList.add('habit-complete-mark');
            completeMark.title = 'Tamamlandı';
            titleWrap.append(completeMark);
        }
        copy.append(titleWrap);
        copy.append(element('p', '', habit.description || (habit.scheduled ? habit.scheduleLabel : 'Bugün planlı değil')));

        const meta = element('div', 'habit-row-meta');
        meta.append(element('strong', '', habit.scheduleLabel));
        meta.append(element('span', '', `${habit.targetOverridden ? 'Bugün' : 'Hedef'}: ${habit.target} ${habit.unit}`));

        const progress = element('div', 'habit-row-progress');
        progress.dataset.action = 'day';
        progress.tabIndex = habit.scheduled ? 0 : -1;
        progress.setAttribute('role', 'button');
        progress.setAttribute('aria-label', `${habit.name} için günlük hedef ve ilerlemeyi düzenle`);
        progress.title = 'Günlük hedefi, yapılan miktarı ve notu düzenle';
        const progressCopy = element('div', 'habit-progress-copy');
        progressCopy.append(
            element('strong', '', habit.scheduled ? `%${habit.rate}` : 'Plan dışı'),
            element('span', '', habit.scheduled ? `${habit.value} / ${habit.target} ${habit.unit}` : habit.scheduleLabel),
        );
        const track = element('div', 'habit-progress-track');
        track.setAttribute('role', 'progressbar');
        track.setAttribute('aria-valuemin', '0');
        track.setAttribute('aria-valuemax', '100');
        track.setAttribute('aria-valuenow', String(habit.rate));
        const fill = document.createElement('i');
        fill.style.setProperty('--progress', `${habit.rate}%`);
        track.append(fill);
        progress.append(progressCopy, track);

        const actions = element('div', 'habit-row-actions');
        actions.append(
            actionButton('decrement', 'dash-lg', 'Bir azalt', !habit.scheduled || habit.value <= 0),
            actionButton('toggle', habit.completed ? 'arrow-counterclockwise' : 'check2', habit.completed ? 'Günü sıfırla' : 'Hedefi tamamla', !habit.scheduled),
            actionButton('increment', 'plus-lg', 'Bir artır', !habit.scheduled),
            actionButton('day', 'calendar2-week', 'Günlük kaydı düzenle', !habit.scheduled),
        );
        const editButton = element('button', 'habit-edit-button');
        editButton.type = 'button';
        editButton.dataset.action = 'edit';
        editButton.title = 'Düzenle';
        editButton.setAttribute('aria-label', `${habit.name} alışkanlığını düzenle`);
        editButton.append(icon('pencil'));
        actions.append(editButton);

        row.append(rowIcon, copy, meta, miniChart(habit), progress, actions);
        return row;
    }

    function renderHabits() {
        refs.list.replaceChildren();
        const habits = state.habits || [];
        refs.listCount.textContent = `${habits.length} alışkanlık`;
        if (!habits.length) {
            const empty = element('button', 'habit-empty-state');
            empty.type = 'button';
            empty.dataset.emptyCreate = 'true';
            const inner = element('span');
            inner.append(icon('calendar2-plus'));
            inner.append(element('strong', '', 'İlk alışkanlığını oluştur'));
            inner.append(element('span', '', 'Bugünün ritmi burada görünecek.'));
            empty.append(inner);
            refs.list.append(empty);
            return;
        }
        habits.forEach((habit) => refs.list.append(renderHabitRow(habit)));
    }

    function renderWeekdays() {
        refs.weekdayChart.replaceChildren();
        (state.weekdays || []).forEach((weekday) => {
            const row = element('div', 'habit-weekday-row');
            const track = element('span', 'habit-weekday-track');
            const fill = document.createElement('i');
            fill.style.setProperty('--weekday-rate', `${weekday.rate}%`);
            track.append(fill);
            row.append(
                element('span', '', weekday.label),
                track,
                element('strong', '', `%${weekday.rate}`),
            );
            refs.weekdayChart.append(row);
        });
    }

    function renderTrend() {
        refs.trendChart.replaceChildren();
        const trend = state.trend || [];
        const width = 760;
        const height = 245;
        const margin = { top: 14, right: 16, bottom: 32, left: 34 };
        const plotWidth = width - margin.left - margin.right;
        const plotHeight = height - margin.top - margin.bottom;
        const svg = svgElement('svg', {
            viewBox: `0 0 ${width} ${height}`,
            role: 'img',
            'aria-label': `${state.range} günlük tamamlama eğilimi`,
            preserveAspectRatio: 'none',
        });

        [0, 50, 100].forEach((value) => {
            const y = margin.top + plotHeight - ((value / 100) * plotHeight);
            svg.append(svgElement('line', {
                x1: margin.left,
                y1: y,
                x2: width - margin.right,
                y2: y,
                class: 'habit-chart-grid-line',
            }));
            const label = svgElement('text', {
                x: margin.left - 8,
                y: y + 3,
                class: 'habit-chart-label',
                'text-anchor': 'end',
            });
            label.textContent = `%${value}`;
            svg.append(label);
        });

        const step = plotWidth / Math.max(1, trend.length);
        const barWidth = Math.max(2, Math.min(15, step * 0.58));
        const points = [];
        const labelEvery = trend.length <= 7 ? 1 : trend.length <= 30 ? 5 : 15;

        trend.forEach((item, index) => {
            const x = margin.left + (index * step) + (step / 2);
            const barHeight = (item.rate / 100) * plotHeight;
            const y = margin.top + plotHeight - barHeight;
            const bar = svgElement('rect', {
                x: x - (barWidth / 2),
                y,
                width: barWidth,
                height: Math.max(1, barHeight),
                rx: Math.min(3, barWidth / 2),
                class: `habit-chart-bar${item.rate >= 100 ? ' is-complete' : ''}`,
            });
            const title = svgElement('title');
            title.textContent = `${item.date}: %${item.rate} · ${item.completed}/${item.scheduled}`;
            bar.append(title);
            svg.append(bar);
            points.push(`${x},${y}`);

            if (index === 0 || index === trend.length - 1 || index % labelEvery === 0) {
                const label = svgElement('text', {
                    x,
                    y: height - 8,
                    class: 'habit-chart-label',
                    'text-anchor': 'middle',
                });
                label.textContent = item.label;
                svg.append(label);
            }
        });

        if (points.length > 1) {
            svg.append(svgElement('polyline', {
                points: points.join(' '),
                class: 'habit-chart-line',
            }));
            if (trend.length <= 30) {
                points.forEach((point) => {
                    const [x, y] = point.split(',');
                    svg.append(svgElement('circle', {
                        cx: x,
                        cy: y,
                        r: 3,
                        class: 'habit-chart-point',
                    }));
                });
            }
        }
        refs.trendChart.append(svg);
    }

    function heatmapLevel(rate, scheduled, future) {
        if (future || !scheduled || rate <= 0) return 0;
        if (rate < 34) return 1;
        if (rate < 67) return 2;
        if (rate < 100) return 3;
        return 4;
    }

    function renderHeatmap() {
        refs.heatmap.replaceChildren();
        (state.heatmap || []).forEach((item) => {
            const cell = element('span', 'habit-heatmap-cell');
            cell.dataset.level = heatmapLevel(item.rate, item.scheduled, item.future);
            cell.title = item.future
                ? `${item.date}: gelecek gün`
                : `${item.date}: ${item.scheduled ? `%${item.rate}` : 'plan yok'}`;
            refs.heatmap.append(cell);
        });
    }

    function renderArchive() {
        const archived = state.archivedHabits || [];
        refs.archiveCount.textContent = archived.length;
        refs.archiveCount.hidden = archived.length === 0;
        refs.archiveList.replaceChildren();
        if (!archived.length) {
            const empty = element('div', 'habit-archive-empty');
            empty.append(icon('archive'));
            empty.append(element('p', '', 'Arşiv boş.'));
            refs.archiveList.append(empty);
            return;
        }

        archived.forEach((habit) => {
            const row = element('div', 'habit-archive-row');
            row.dataset.habitId = habit.id;
            row.style.setProperty('--archive-color', habit.color);
            const rowIcon = icon(habit.icon);
            const restore = element('button', 'habit-archive-action', 'Geri yükle');
            restore.type = 'button';
            restore.dataset.archiveAction = 'restore';
            const remove = element('button', 'habit-archive-action is-danger', 'Sil');
            remove.type = 'button';
            remove.dataset.archiveAction = 'delete';
            row.append(rowIcon, element('strong', '', habit.name), restore, remove);
            refs.archiveList.append(row);
        });
    }

    function renderRange() {
        document.querySelectorAll('[data-range]').forEach((button) => {
            const isActive = Number(button.dataset.range) === Number(state.range);
            button.classList.toggle('is-active', isActive);
            button.setAttribute('aria-pressed', isActive ? 'true' : 'false');
        });
    }

    function render() {
        renderDate();
        renderSummary();
        renderHabits();
        renderWeekdays();
        renderTrend();
        renderHeatmap();
        renderArchive();
        renderRange();

        const url = new URL(window.location.href);
        if (state.selectedDate === state.today) url.searchParams.delete('date');
        else url.searchParams.set('date', state.selectedDate);
        if (Number(state.range) === 30) url.searchParams.delete('range');
        else url.searchParams.set('range', state.range);
        window.history.replaceState({}, '', url);
    }

    async function loadDashboard(date, range) {
        setBusy(true);
        try {
            const url = new URL(urls.list, window.location.origin);
            url.searchParams.set('date', date || state.selectedDate);
            url.searchParams.set('range', range || state.range);
            const result = await jsonRequest(url.toString());
            state = result.data;
            render();
            refs.status.textContent = '';
        } catch (error) {
            setStatus(error.message, 'error');
        } finally {
            setBusy(false);
        }
    }

    function setEditorChoice(container, attribute, value) {
        container.querySelectorAll(`button[data-${attribute}]`).forEach((button) => {
            const isActive = button.dataset[attribute] === String(value);
            button.classList.toggle('is-active', isActive);
            button.setAttribute('aria-pressed', isActive ? 'true' : 'false');
        });
    }

    function setFrequency(frequency) {
        selectedFrequency = frequency === 'custom' ? 'custom' : 'daily';
        setEditorChoice(refs.frequencyControl, 'frequency', selectedFrequency);
        refs.weekdayChoices.hidden = selectedFrequency !== 'custom';
    }

    function syncWeekdayChoices() {
        refs.weekdayChoices.querySelectorAll('[data-day]').forEach((button) => {
            const isActive = selectedDays.has(Number(button.dataset.day));
            button.classList.toggle('is-active', isActive);
            button.setAttribute('aria-pressed', isActive ? 'true' : 'false');
        });
    }

    function showEditor() {
        if (!editorModal) editorModal = new bootstrap.Modal(refs.editorModal);
        editorModal.show();
        window.setTimeout(() => refs.nameInput.focus(), 180);
    }

    function openCreateEditor() {
        refs.editorForm.reset();
        refs.editorId.value = '';
        refs.editorKicker.textContent = 'Yeni kayıt';
        refs.editorTitle.textContent = 'Alışkanlık ekle';
        refs.editorSubmit.lastChild.textContent = ' Kaydet';
        refs.startDateInput.value = state.today;
        refs.startDateInput.max = state.today;
        refs.targetInput.value = '1';
        refs.unitInput.value = 'kez';
        selectedIcon = 'check2-circle';
        selectedColor = '#2F6B4F';
        selectedDays = new Set();
        setEditorChoice(refs.iconChoices, 'icon', selectedIcon);
        setEditorChoice(refs.colorChoices, 'color', selectedColor);
        setFrequency('daily');
        syncWeekdayChoices();
        refs.archiveButton.hidden = true;
        refs.deleteButton.hidden = true;
        showEditor();
    }

    function openEditEditor(habit) {
        refs.editorForm.reset();
        refs.editorId.value = habit.id;
        refs.editorKicker.textContent = 'Düzenleme';
        refs.editorTitle.textContent = habit.name;
        refs.nameInput.value = habit.name;
        refs.descriptionInput.value = habit.description || '';
        refs.targetInput.value = habit.defaultTarget;
        refs.unitInput.value = habit.unit;
        refs.startDateInput.value = habit.startDate;
        refs.startDateInput.max = state.today;
        selectedIcon = habit.icon;
        selectedColor = habit.color;
        selectedDays = new Set(habit.scheduleDays || []);
        setEditorChoice(refs.iconChoices, 'icon', selectedIcon);
        setEditorChoice(refs.colorChoices, 'color', selectedColor);
        setFrequency(habit.frequency);
        syncWeekdayChoices();
        refs.archiveButton.hidden = false;
        refs.deleteButton.hidden = false;
        showEditor();
    }

    function editorPayload() {
        return {
            name: refs.nameInput.value,
            description: refs.descriptionInput.value,
            icon: selectedIcon,
            color: selectedColor,
            target: refs.targetInput.value,
            unit: refs.unitInput.value,
            startDate: refs.startDateInput.value,
            frequency: selectedFrequency,
            scheduleDays: Array.from(selectedDays).sort((a, b) => a - b),
        };
    }

    function openDayEditor(habit) {
        refs.dayForm.reset();
        refs.dayId.value = habit.id;
        refs.dayDate.textContent = state.dateLabel || state.selectedDate;
        refs.dayTitle.textContent = habit.name;
        refs.dayTargetInput.value = habit.target;
        refs.dayValueInput.value = habit.value;
        refs.dayNoteInput.value = habit.note || '';
        refs.dayTargetUnit.textContent = habit.unit;
        refs.dayValueUnit.textContent = habit.unit;
        refs.dayDefaultHint.textContent = `Varsayılan hedef: ${habit.defaultTarget} ${habit.unit}`;
        refs.dayUseDefault.dataset.target = habit.defaultTarget;
        if (!dayModal) dayModal = new bootstrap.Modal(refs.dayModal);
        dayModal.show();
        window.setTimeout(() => refs.dayValueInput.focus(), 180);
    }

    refs.list.addEventListener('click', async (event) => {
        if (event.target.closest('[data-empty-create]')) {
            openCreateEditor();
            return;
        }
        const button = event.target.closest('[data-action]');
        const row = event.target.closest('[data-habit-id]');
        if (!button || !row) return;
        const habitId = Number(row.dataset.habitId);
        const habit = (state.habits || []).find((item) => item.id === habitId);
        if (!habit) return;
        const action = button.dataset.action;
        if (action === 'edit') {
            openEditEditor(habit);
            return;
        }
        if (action === 'day') {
            if (habit.scheduled) openDayEditor(habit);
            return;
        }
        await mutate(endpoint(urls.log, habitId), { action }, 'İlerleme kaydedildi.');
    });

    refs.list.addEventListener('keydown', (event) => {
        const progress = event.target.closest('.habit-row-progress[data-action="day"]');
        if (!progress || !['Enter', ' '].includes(event.key)) return;
        event.preventDefault();
        progress.click();
    });

    refs.createOpen.addEventListener('click', openCreateEditor);
    refs.archiveOpen.addEventListener('click', () => {
        renderArchive();
        if (!archiveModal) archiveModal = new bootstrap.Modal(refs.archiveModal);
        archiveModal.show();
    });

    refs.previousDate.addEventListener('click', () => loadDashboard(addDays(state.selectedDate, -1), state.range));
    refs.nextDate.addEventListener('click', () => {
        if (state.selectedDate < state.today) loadDashboard(addDays(state.selectedDate, 1), state.range);
    });
    refs.dateDisplay.addEventListener('click', () => loadDashboard(state.today, state.range));
    refs.dateInput.addEventListener('change', () => {
        if (refs.dateInput.value) loadDashboard(refs.dateInput.value, state.range);
    });

    document.querySelectorAll('[data-range]').forEach((button) => {
        button.addEventListener('click', () => loadDashboard(state.selectedDate, Number(button.dataset.range)));
    });

    refs.iconChoices.addEventListener('click', (event) => {
        const button = event.target.closest('[data-icon]');
        if (!button) return;
        selectedIcon = button.dataset.icon;
        setEditorChoice(refs.iconChoices, 'icon', selectedIcon);
    });

    refs.colorChoices.addEventListener('click', (event) => {
        const button = event.target.closest('[data-color]');
        if (!button) return;
        selectedColor = button.dataset.color;
        setEditorChoice(refs.colorChoices, 'color', selectedColor);
    });

    refs.frequencyControl.addEventListener('click', (event) => {
        const button = event.target.closest('[data-frequency]');
        if (button) setFrequency(button.dataset.frequency);
    });

    refs.weekdayChoices.addEventListener('click', (event) => {
        const button = event.target.closest('[data-day]');
        if (!button) return;
        const day = Number(button.dataset.day);
        if (selectedDays.has(day)) selectedDays.delete(day);
        else selectedDays.add(day);
        syncWeekdayChoices();
    });

    refs.editorForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const habitId = Number(refs.editorId.value || 0);
        const url = habitId ? endpoint(urls.update, habitId) : urls.create;
        const saved = await mutate(url, editorPayload(), habitId ? 'Alışkanlık güncellendi.' : 'Alışkanlık eklendi.');
        if (saved && editorModal) editorModal.hide();
    });

    refs.dayUseDefault.addEventListener('click', () => {
        refs.dayTargetInput.value = refs.dayUseDefault.dataset.target || '1';
        refs.dayTargetInput.focus();
    });

    refs.dayForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const habitId = Number(refs.dayId.value || 0);
        if (!habitId) return;
        const saved = await mutate(endpoint(urls.log, habitId), {
            action: 'set_day',
            target: refs.dayTargetInput.value,
            value: refs.dayValueInput.value,
            note: refs.dayNoteInput.value,
        }, 'Günlük kayıt güncellendi.');
        if (saved && dayModal) dayModal.hide();
    });

    refs.archiveButton.addEventListener('click', async () => {
        const habitId = Number(refs.editorId.value || 0);
        if (!habitId) return;
        const saved = await mutate(endpoint(urls.archive, habitId), {}, 'Alışkanlık arşivlendi.');
        if (saved && editorModal) editorModal.hide();
    });

    refs.deleteButton.addEventListener('click', async () => {
        const habitId = Number(refs.editorId.value || 0);
        const habit = (state.habits || []).find((item) => item.id === habitId);
        if (!habit || !window.confirm(`“${habit.name}” ve tüm kayıtları kalıcı olarak silinsin mi?`)) return;
        const saved = await mutate(endpoint(urls.delete, habitId), {}, 'Alışkanlık silindi.');
        if (saved && editorModal) editorModal.hide();
    });

    refs.archiveList.addEventListener('click', async (event) => {
        const button = event.target.closest('[data-archive-action]');
        const row = event.target.closest('[data-habit-id]');
        if (!button || !row) return;
        const habitId = Number(row.dataset.habitId);
        const habit = (state.archivedHabits || []).find((item) => item.id === habitId);
        if (!habit) return;

        if (button.dataset.archiveAction === 'delete') {
            if (!window.confirm(`“${habit.name}” ve tüm kayıtları kalıcı olarak silinsin mi?`)) return;
            await mutate(endpoint(urls.delete, habitId), {}, 'Alışkanlık silindi.');
        } else {
            await mutate(endpoint(urls.archive, habitId), {}, 'Alışkanlık geri yüklendi.');
        }
        renderArchive();
    });

    render();
}());
