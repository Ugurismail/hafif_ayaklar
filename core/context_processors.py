# core/context_processors.py

from django.conf import settings
from django.utils.functional import SimpleLazyObject


def navbar_unread_counts(request):
    if not request.user.is_authenticated:
        return {}
    from .models import Message, Notification

    # Preview templates do not use the navbar; query only when a badge is rendered.
    return {
        'unread_notification_count': SimpleLazyObject(
            lambda: Notification.objects.filter(recipient=request.user, is_read=False).count()
        ),
        'unread_message_count': SimpleLazyObject(
            lambda: Message.objects.filter(recipient=request.user, is_read=False).count()
        ),
    }

def static_asset_version(request):
    return {'STATIC_ASSET_VERSION': getattr(settings, 'STATIC_ASSET_VERSION', '1')}


def google_analytics(request):
    ga_id = (getattr(settings, 'GOOGLE_ANALYTICS_ID', '') or '').strip()
    try:
        host = (request.get_host() or '').split(':', 1)[0].lower()
    except Exception:
        host = ''

    enabled = bool(ga_id) and host not in {'127.0.0.1', 'localhost'}
    return {
        'GOOGLE_ANALYTICS_ID': ga_id if enabled else '',
        'GOOGLE_ANALYTICS_ENABLED': enabled,
    }
