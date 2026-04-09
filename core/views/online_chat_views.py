"""
Online chat views
- online_chat_messages
"""

from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.templatetags.static import static
from django.utils import timezone

from ..models import OnlineChatMessage, UserProfile

ONLINE_WINDOW = timedelta(minutes=5)
CHAT_RATE_LIMIT_WINDOW = timedelta(minutes=1)
CHAT_RATE_LIMIT_COUNT = 12
RECENT_MESSAGES_LIMIT = 60
MAX_CHAT_MESSAGE_LENGTH = 500


@login_required
def online_chat_messages(request):
    now = timezone.now()

    def serialize_message(message):
        profile = getattr(message.user, 'userprofile', None)
        avatar_url = profile.photo.url if profile and profile.photo else static('imgs/default_profile.jpg')
        return {
            'id': message.id,
            'body': message.body,
            'username': message.user.username,
            'avatar_url': avatar_url,
            'created_at': timezone.localtime(message.created_at).strftime('%H:%M'),
            'is_own': message.user_id == request.user.id,
        }

    def serialize_online_user(profile):
        return {
            'username': profile.user.username,
            'avatar_url': profile.photo.url if profile.photo else static('imgs/default_profile.jpg'),
            'profile_url': f'/profile/{profile.user.username}/',
            'last_seen': timezone.localtime(profile.last_seen).strftime('%H:%M') if profile.last_seen else '',
            'is_self': profile.user_id == request.user.id,
        }

    if request.method == 'POST':
        body = request.POST.get('body', '').strip()
        if not body:
            return JsonResponse({'error': 'Mesaj boş olamaz.'}, status=400)
        if len(body) > MAX_CHAT_MESSAGE_LENGTH:
            return JsonResponse({'error': f'Mesaj çok uzun (max {MAX_CHAT_MESSAGE_LENGTH} karakter).'}, status=400)

        recent_messages_count = OnlineChatMessage.objects.filter(
            user=request.user,
            created_at__gte=now - CHAT_RATE_LIMIT_WINDOW,
        ).count()
        if recent_messages_count >= CHAT_RATE_LIMIT_COUNT:
            return JsonResponse({'error': 'Çok hızlı yazıyorsun. Lütfen biraz bekle.'}, status=429)

        message = OnlineChatMessage.objects.create(
            user=request.user,
            body=body,
        )
        return JsonResponse({'message': serialize_message(message)}, status=201)

    after = request.GET.get('after')
    if after and after.isdigit():
        messages = (
            OnlineChatMessage.objects.filter(id__gt=int(after))
            .select_related('user', 'user__userprofile')
            .order_by('created_at')
        )
    else:
        messages = list(
            OnlineChatMessage.objects.select_related('user', 'user__userprofile')
            .order_by('-id')[:RECENT_MESSAGES_LIMIT]
        )
        messages.reverse()

    online_profiles = (
        UserProfile.objects.filter(last_seen__gte=now - ONLINE_WINDOW)
        .select_related('user')
        .order_by('-last_seen', 'user__username')
    )

    return JsonResponse({
        'messages': [serialize_message(message) for message in messages],
        'online_users': [serialize_online_user(profile) for profile in online_profiles],
        'online_count': online_profiles.count(),
    })
