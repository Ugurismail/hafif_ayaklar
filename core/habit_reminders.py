"""Create due habit reminders through the existing navbar heartbeat."""

from django.db import transaction
from django.utils import timezone

from .models import Habit, HabitEntry, HabitReminderDelivery, Notification


def materialize_due_habit_reminders(user, now=None):
    """Create at most one site notification per due habit and local date."""
    if not user or not user.is_authenticated:
        return 0

    local_now = timezone.localtime(now or timezone.now())
    today = local_now.date()
    current_time = local_now.time().replace(tzinfo=None)

    due_habits = list(
        Habit.objects.filter(
            user=user,
            is_archived=False,
            reminder_enabled=True,
            reminder_time__isnull=False,
            reminder_time__lte=current_time,
            start_date__lte=today,
        ).order_by('position', 'id')
    )
    if not due_habits:
        return 0

    entries = {
        entry.habit_id: entry
        for entry in HabitEntry.objects.filter(
            habit__in=due_habits,
            date=today,
        )
    }
    created_count = 0
    for habit in due_habits:
        if not habit.is_scheduled_for(today):
            continue

        entry = entries.get(habit.id)
        target = entry.effective_target if entry else habit.target
        if entry and entry.value >= target:
            continue

        with transaction.atomic():
            _, created = HabitReminderDelivery.objects.get_or_create(
                habit=habit,
                date=today,
            )
            if not created:
                continue

            Notification.objects.create(
                recipient=user,
                notification_type='habit_reminder',
                related_habit=habit,
                message=(
                    f'{habit.name} için hatırlatma: '
                    f'bugünkü hedefin {target} {habit.unit}.'
                ),
            )
            created_count += 1

    return created_count
