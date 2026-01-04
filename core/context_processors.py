# core/context_processors.py

from django.conf import settings
from .models import Message, Notification

def static_asset_version(request):
    return {'STATIC_ASSET_VERSION': getattr(settings, 'STATIC_ASSET_VERSION', '1')}

def unread_message_count(request):
    if request.user.is_authenticated:
        count = Message.objects.filter(recipient=request.user, is_read=False).count()
        return {'unread_message_count': count}
    else:
        return {}

def unread_notification_count(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return {'unread_notification_count': count}
    else:
        return {}
