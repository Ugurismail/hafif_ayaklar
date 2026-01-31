# core/context_processors.py

from django.conf import settings
from .models import Message, Notification, RadioProgram
from .radio_utils import expire_live_programs

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

def radio_live_indicator(request):
    if not request.user.is_authenticated:
        return {}
    expire_live_programs()
    is_live = RadioProgram.objects.filter(is_live=True, is_finished=False).exists()
    return {'radio_is_live': is_live}
