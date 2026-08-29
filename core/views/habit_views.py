"""Private habit tracking dashboard and JSON actions."""

import json
import re
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db import transaction
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_time
from django.views.decorators.http import require_GET, require_POST

from ..models import Habit, HabitEntry


HABIT_COLOR_PALETTE = [
    ('#2F6B4F', 'Orman'),
    ('#2F7F78', 'Çamurcun'),
    ('#3D6F8E', 'Okyanus'),
    ('#476A9C', 'Gece mavisi'),
    ('#4E5968', 'Grafit'),
    ('#65743A', 'Zeytin'),
    ('#5B7F3B', 'Yaprak'),
    ('#765A86', 'Erik'),
    ('#6A5FA8', 'İndigo'),
    ('#8B5E83', 'Mürdüm'),
    ('#A16A3A', 'Bakır'),
    ('#B08D57', 'Altın'),
    ('#C07A32', 'Kehribar'),
    ('#B85C4A', 'Kiremit'),
    ('#C45D75', 'Gül'),
    ('#8A6F5A', 'Toprak'),
]
HABIT_ICONS = {choice[0] for choice in Habit.ICON_CHOICES}
HABIT_RANGES = {7, 30, 90}
MAX_ACTIVE_HABITS = 40
MAX_ENTRY_VALUE = 9999
WEEKDAY_NAMES = ('Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz')
MONTH_NAMES = (
    '', 'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
    'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık',
)


def _request_payload(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def _selected_date(value):
    today = timezone.localdate()
    parsed = parse_date(str(value or '')) or today
    return min(parsed, today)


def _selected_range(value):
    try:
        range_days = int(value)
    except (TypeError, ValueError):
        return 30
    return range_days if range_days in HABIT_RANGES else 30


def _archive_date(habit):
    if not habit.archived_at:
        return None
    return timezone.localtime(habit.archived_at).date()


def _habit_available_on(habit, selected_date):
    if selected_date < habit.start_date:
        return False
    archived_on = _archive_date(habit)
    return archived_on is None or selected_date < archived_on


def _schedule_label(habit):
    if habit.frequency == Habit.FREQUENCY_DAILY:
        return 'Her gün'
    days = [
        WEEKDAY_NAMES[day]
        for day in habit.schedule_days
        if isinstance(day, int) and 0 <= day <= 6
    ]
    return ' · '.join(days) if days else 'Gün seçilmedi'


def _progress(value, target):
    if not target:
        return 0
    return min(100, round((value / target) * 100))


def _dashboard_payload(user, selected_date=None, range_days=30):
    selected_date = _selected_date(selected_date)
    range_days = _selected_range(range_days)
    history_start = selected_date - timedelta(days=365)

    all_habits = list(
        Habit.objects.filter(user=user)
        .order_by('position', 'created_at')
    )
    entries = HabitEntry.objects.filter(
        habit__user=user,
        date__range=(history_start, selected_date),
    ).values_list('habit_id', 'date', 'value', 'target', 'note')
    entry_data = {
        (habit_id, entry_date): {
            'value': value,
            'target': target,
            'note': note,
        }
        for habit_id, entry_date, value, target, note in entries
    }

    def values_for(habit, day):
        entry = entry_data.get((habit.id, day)) or {}
        return {
            'value': entry.get('value', 0),
            'target': entry.get('target') or habit.target,
            'target_overridden': entry.get('target') is not None,
            'note': entry.get('note', ''),
        }

    def scheduled_habits(day):
        return [
            habit
            for habit in all_habits
            if _habit_available_on(habit, day) and habit.is_scheduled_for(day)
        ]

    def day_metric(day):
        scheduled = scheduled_habits(day)
        if not scheduled:
            return {
                'date': day.isoformat(),
                'label': str(day.day),
                'rate': 0,
                'scheduled': 0,
                'completed': 0,
            }

        fractions = []
        completed = 0
        for habit in scheduled:
            values = values_for(habit, day)
            fractions.append(min(1, values['value'] / values['target']))
            if values['value'] >= values['target']:
                completed += 1
        return {
            'date': day.isoformat(),
            'label': str(day.day),
            'rate': round((sum(fractions) / len(scheduled)) * 100),
            'scheduled': len(scheduled),
            'completed': completed,
        }

    visible_habits = [
        habit
        for habit in all_habits
        if not habit.is_archived and habit.start_date <= selected_date
    ]
    habit_payload = []
    for habit in visible_habits:
        selected_values = values_for(habit, selected_date)
        value = selected_values['value']
        target = selected_values['target']
        is_scheduled = habit.is_scheduled_for(selected_date)
        mini_days = []
        for offset in range(6, -1, -1):
            mini_date = selected_date - timedelta(days=offset)
            mini_values = values_for(habit, mini_date)
            mini_scheduled = _habit_available_on(habit, mini_date) and habit.is_scheduled_for(mini_date)
            mini_days.append({
                'date': mini_date.isoformat(),
                'label': WEEKDAY_NAMES[mini_date.weekday()],
                'scheduled': mini_scheduled,
                'value': mini_values['value'],
                'target': mini_values['target'],
                'rate': _progress(mini_values['value'], mini_values['target']) if mini_scheduled else 0,
            })

        habit_payload.append({
            'id': habit.id,
            'name': habit.name,
            'description': habit.description,
            'color': habit.color,
            'icon': habit.icon,
            'frequency': habit.frequency,
            'scheduleDays': habit.schedule_days,
            'scheduleLabel': _schedule_label(habit),
            'defaultTarget': habit.target,
            'target': target,
            'targetOverridden': selected_values['target_overridden'],
            'unit': habit.unit,
            'startDate': habit.start_date.isoformat(),
            'reminderEnabled': habit.reminder_enabled,
            'reminderTime': habit.reminder_time.strftime('%H:%M') if habit.reminder_time else '',
            'scheduled': is_scheduled,
            'value': value,
            'note': selected_values['note'],
            'rate': _progress(value, target) if is_scheduled else 0,
            'completed': is_scheduled and value >= target,
            'mini': mini_days,
        })

    selected_metric = day_metric(selected_date)
    trend_start = selected_date - timedelta(days=range_days - 1)
    trend_dates = [
        trend_start + timedelta(days=offset)
        for offset in range(range_days)
    ]
    trend = [day_metric(day) for day in trend_dates]
    habit_trends = {}
    for habit in visible_habits:
        rates = []
        for day in trend_dates:
            is_scheduled = (
                _habit_available_on(habit, day)
                and habit.is_scheduled_for(day)
            )
            if not is_scheduled:
                rates.append(None)
                continue
            values = values_for(habit, day)
            rates.append(_progress(values['value'], values['target']))
        habit_trends[str(habit.id)] = rates
    current_week_start = selected_date - timedelta(days=selected_date.weekday())
    heatmap_start = current_week_start - timedelta(weeks=11)
    heatmap = []
    for offset in range(84):
        heatmap_date = heatmap_start + timedelta(days=offset)
        if heatmap_date > selected_date:
            heatmap.append({
                'date': heatmap_date.isoformat(),
                'label': str(heatmap_date.day),
                'rate': 0,
                'scheduled': 0,
                'completed': 0,
                'future': True,
            })
        else:
            heatmap.append({**day_metric(heatmap_date), 'future': False})

    weekday_buckets = {weekday: [] for weekday in range(7)}
    for item in trend:
        item_date = parse_date(item['date'])
        if item['scheduled']:
            weekday_buckets[item_date.weekday()].append(item['rate'])
    weekdays = []
    for weekday in range(7):
        rates = weekday_buckets[weekday]
        weekdays.append({
            'label': WEEKDAY_NAMES[weekday],
            'rate': round(sum(rates) / len(rates)) if rates else 0,
        })

    week_metrics = [
        day_metric(selected_date - timedelta(days=offset))
        for offset in range(6, -1, -1)
    ]
    week_rates = [item['rate'] for item in week_metrics if item['scheduled']]
    week_rate = round(sum(week_rates) / len(week_rates)) if week_rates else 0

    streak = 0
    cursor = selected_date
    for _ in range(366):
        metric = day_metric(cursor)
        if not metric['scheduled']:
            cursor -= timedelta(days=1)
            continue
        if metric['rate'] < 100:
            break
        streak += 1
        cursor -= timedelta(days=1)

    archived_habits = [
        {
            'id': habit.id,
            'name': habit.name,
            'color': habit.color,
            'icon': habit.icon,
            'archivedAt': habit.archived_at.isoformat() if habit.archived_at else '',
        }
        for habit in all_habits
        if habit.is_archived
    ]

    return {
        'selectedDate': selected_date.isoformat(),
        'today': timezone.localdate().isoformat(),
        'dateLabel': f'{selected_date.day} {MONTH_NAMES[selected_date.month]} {selected_date.year}',
        'range': range_days,
        'habits': habit_payload,
        'archivedHabits': archived_habits,
        'summary': {
            'rate': selected_metric['rate'],
            'completed': selected_metric['completed'],
            'scheduled': selected_metric['scheduled'],
            'streak': streak,
            'weekRate': week_rate,
            'active': len(visible_habits),
        },
        'trend': trend,
        'habitTrends': habit_trends,
        'heatmap': heatmap,
        'weekdays': weekdays,
    }


def _clean_habit_payload(payload):
    name = str(payload.get('name', '')).strip()[:80]
    if not name:
        return None, 'Alışkanlık adı boş olamaz.'

    description = str(payload.get('description', '')).strip()[:240]
    color = str(payload.get('color', '')).strip().upper()
    if not re.fullmatch(r'#[0-9A-F]{6}', color):
        color = '#2F6B4F'

    icon = str(payload.get('icon', '')).strip()
    if icon not in HABIT_ICONS:
        icon = 'check2-circle'

    frequency = str(payload.get('frequency', Habit.FREQUENCY_DAILY)).strip()
    if frequency not in {Habit.FREQUENCY_DAILY, Habit.FREQUENCY_CUSTOM}:
        frequency = Habit.FREQUENCY_DAILY

    raw_days = payload.get('scheduleDays', [])
    if not isinstance(raw_days, list):
        raw_days = []
    schedule_days = sorted({
        day for day in raw_days if isinstance(day, int) and 0 <= day <= 6
    })
    if frequency == Habit.FREQUENCY_CUSTOM and not schedule_days:
        return None, 'Belirli günler için en az bir gün seçin.'
    if frequency == Habit.FREQUENCY_DAILY:
        schedule_days = []

    try:
        target = int(payload.get('target', 1))
    except (TypeError, ValueError):
        return None, 'Günlük hedef sayı olmalıdır.'
    if not 1 <= target <= 999:
        return None, 'Günlük hedef 1 ile 999 arasında olmalıdır.'

    unit = str(payload.get('unit', '')).strip()[:18] or 'kez'
    start_date = parse_date(str(payload.get('startDate', ''))) or timezone.localdate()
    if start_date > timezone.localdate():
        return None, 'Başlangıç tarihi gelecekte olamaz.'

    reminder_enabled = payload.get('reminderEnabled') is True
    reminder_time = None
    if reminder_enabled:
        reminder_time = parse_time(str(payload.get('reminderTime', '')).strip())
        if reminder_time is None:
            return None, 'Hatırlatma için geçerli bir saat seçin.'
        reminder_time = reminder_time.replace(second=0, microsecond=0)

    return {
        'name': name,
        'description': description,
        'color': color,
        'icon': icon,
        'frequency': frequency,
        'schedule_days': schedule_days,
        'target': target,
        'unit': unit,
        'start_date': start_date,
        'reminder_enabled': reminder_enabled,
        'reminder_time': reminder_time,
    }, None


def _response_with_dashboard(request, message, status=200):
    payload = _request_payload(request) or {}
    return JsonResponse({
        'ok': True,
        'message': message,
        'data': _dashboard_payload(
            request.user,
            payload.get('date'),
            payload.get('range', 30),
        ),
    }, status=status)


@login_required
def habit_tracker(request):
    selected_date = _selected_date(request.GET.get('date'))
    range_days = _selected_range(request.GET.get('range'))
    return render(request, 'core/habit_tracker.html', {
        'habit_tracker_data': _dashboard_payload(request.user, selected_date, range_days),
        'habit_colors': HABIT_COLOR_PALETTE,
        'habit_icons': Habit.ICON_CHOICES,
    })


@login_required
@require_GET
def habit_tracker_data(request):
    return JsonResponse({
        'ok': True,
        'data': _dashboard_payload(
            request.user,
            request.GET.get('date'),
            request.GET.get('range', 30),
        ),
    })


@login_required
@require_POST
def habit_create(request):
    payload = _request_payload(request)
    if payload is None:
        return JsonResponse({'error': 'Geçersiz veri.'}, status=400)
    if Habit.objects.filter(user=request.user, is_archived=False).count() >= MAX_ACTIVE_HABITS:
        return JsonResponse({'error': f'En fazla {MAX_ACTIVE_HABITS} aktif alışkanlık ekleyebilirsiniz.'}, status=400)

    cleaned, error = _clean_habit_payload(payload)
    if error:
        return JsonResponse({'error': error}, status=400)

    max_position = Habit.objects.filter(user=request.user).aggregate(Max('position'))['position__max'] or 0
    Habit.objects.create(user=request.user, position=max_position + 1, **cleaned)
    cache.delete_many([
        f'navbar-status:{request.user.id}',
        f'habit-reminder-check:{request.user.id}',
    ])
    return _response_with_dashboard(request, 'Alışkanlık eklendi.', status=201)


@login_required
@require_POST
def habit_update(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    if habit.is_archived:
        return JsonResponse({'error': 'Arşivlenmiş alışkanlığı önce geri yükleyin.'}, status=400)
    payload = _request_payload(request)
    if payload is None:
        return JsonResponse({'error': 'Geçersiz veri.'}, status=400)

    cleaned, error = _clean_habit_payload(payload)
    if error:
        return JsonResponse({'error': error}, status=400)
    for field, value in cleaned.items():
        setattr(habit, field, value)
    habit.save(update_fields=[*cleaned.keys(), 'updated_at'])
    cache.delete_many([
        f'navbar-status:{request.user.id}',
        f'habit-reminder-check:{request.user.id}',
    ])
    return _response_with_dashboard(request, 'Alışkanlık güncellendi.')


@login_required
@require_POST
def habit_log(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user, is_archived=False)
    payload = _request_payload(request)
    if payload is None:
        return JsonResponse({'error': 'Geçersiz veri.'}, status=400)

    selected_date = _selected_date(payload.get('date'))
    if not habit.is_scheduled_for(selected_date):
        return JsonResponse({'error': 'Bu alışkanlık seçilen gün için planlı değil.'}, status=400)

    action = str(payload.get('action', 'toggle')).strip()
    with transaction.atomic():
        entry = HabitEntry.objects.select_for_update().filter(
            habit=habit,
            date=selected_date,
        ).first()
        current_value = entry.value if entry else 0

        if action == 'increment':
            new_value = min(MAX_ENTRY_VALUE, current_value + 1)
        elif action == 'decrement':
            new_value = max(0, current_value - 1)
        elif action == 'toggle':
            effective_target = entry.target if entry and entry.target else habit.target
            new_value = 0 if current_value >= effective_target else effective_target
        elif action in {'set', 'set_day'}:
            try:
                new_value = int(payload.get('value', 0))
            except (TypeError, ValueError):
                return JsonResponse({'error': 'Değer sayı olmalıdır.'}, status=400)
            new_value = max(0, min(MAX_ENTRY_VALUE, new_value))
        else:
            return JsonResponse({'error': 'Geçersiz işlem.'}, status=400)

        if action == 'set_day':
            try:
                daily_target = int(payload.get('target', habit.target))
            except (TypeError, ValueError):
                return JsonResponse({'error': 'Günlük hedef sayı olmalıdır.'}, status=400)
            if not 1 <= daily_target <= MAX_ENTRY_VALUE:
                return JsonResponse({'error': f'Günlük hedef 1 ile {MAX_ENTRY_VALUE} arasında olmalıdır.'}, status=400)
            note = str(payload.get('note', '')).strip()[:240]
            stored_target = None if daily_target == habit.target else daily_target
            if new_value == 0 and stored_target is None and not note:
                if entry:
                    entry.delete()
            else:
                HabitEntry.objects.update_or_create(
                    habit=habit,
                    date=selected_date,
                    defaults={
                        'value': new_value,
                        'target': stored_target,
                        'note': note,
                    },
                )
        elif new_value == 0:
            if entry and entry.target is None and not entry.note:
                entry.delete()
            elif entry:
                entry.value = 0
                entry.save(update_fields=['value', 'updated_at'])
        else:
            HabitEntry.objects.update_or_create(
                habit=habit,
                date=selected_date,
                defaults={'value': new_value},
            )

    return _response_with_dashboard(request, 'İlerleme kaydedildi.')


@login_required
@require_POST
def habit_archive(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    if habit.is_archived:
        if Habit.objects.filter(user=request.user, is_archived=False).count() >= MAX_ACTIVE_HABITS:
            return JsonResponse({'error': 'Aktif alışkanlık sınırına ulaştınız.'}, status=400)
        habit.is_archived = False
        habit.archived_at = None
        message = 'Alışkanlık geri yüklendi.'
    else:
        habit.is_archived = True
        habit.archived_at = timezone.now()
        message = 'Alışkanlık arşivlendi.'
    habit.save(update_fields=['is_archived', 'archived_at', 'updated_at'])
    return _response_with_dashboard(request, message)


@login_required
@require_POST
def habit_delete(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.delete()
    return _response_with_dashboard(request, 'Alışkanlık kalıcı olarak silindi.')
