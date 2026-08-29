"""Lightweight status data used by the global navigation."""

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET

from ..habit_reminders import materialize_due_habit_reminders
from ..models import Message, Notification, UserProfile
from .online_chat_views import online_chat_unread_count_for_user

NAVBAR_STATUS_CACHE_SECONDS = 10
HABIT_REMINDER_CHECK_SECONDS = 45


@login_required
@require_GET
def navbar_status(request):
    cache_key = f'navbar-status:{request.user.id}'
    cached_status = cache.get(cache_key)
    if cached_status is not None:
        return JsonResponse(cached_status)

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    now = timezone.now()
    reminder_check_key = f'habit-reminder-check:{request.user.id}'
    if cache.add(reminder_check_key, True, HABIT_REMINDER_CHECK_SECONDS):
        materialize_due_habit_reminders(request.user, now)

    status = {
        'notification_count': Notification.objects.filter(
            recipient=request.user,
            is_read=False,
        ).count(),
        'message_count': Message.objects.filter(
            recipient=request.user,
            is_read=False,
        ).count(),
        'online_chat_count': online_chat_unread_count_for_user(
            profile,
            request.user,
            now,
        ),
    }
    cache.set(cache_key, status, NAVBAR_STATUS_CACHE_SECONDS)
    return JsonResponse(status)
