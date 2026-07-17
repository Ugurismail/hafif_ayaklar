# core/context_processors.py

from django.conf import settings
from django.core.cache import cache
from .models import RadioProgram
from .radio_utils import expire_live_programs

RADIO_LIVE_CACHE_KEY = 'navbar_radio_is_live'
RADIO_LIVE_CACHE_SECONDS = 30

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

def radio_live_indicator(request):
    if not request.user.is_authenticated:
        return {}

    is_live = cache.get(RADIO_LIVE_CACHE_KEY)
    if is_live is None:
        expire_live_programs()
        is_live = RadioProgram.objects.filter(is_live=True, is_finished=False).exists()
        cache.set(RADIO_LIVE_CACHE_KEY, is_live, RADIO_LIVE_CACHE_SECONDS)
    return {'radio_is_live': is_live}
