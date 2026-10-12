"""Shared login attempt budgets; proxy trust is explicit, never inferred from XFF."""

from datetime import timedelta
from ipaddress import ip_address, ip_network
import json
import logging
import math
import unicodedata

from django.conf import settings
from django.core.checks import Error, Warning, register, Tags
from django.db import DatabaseError, transaction
from django.shortcuts import render
from django.utils import timezone
from django.utils.cache import add_never_cache_headers
from django.utils.crypto import salted_hmac
from django.utils.deprecation import MiddlewareMixin

from .models import LoginRateLimitBucket

logger = logging.getLogger(__name__)

# Official https://www.cloudflare.com/ips-{v4,v6}/, checked 2026-10-07.
# No network lookup takes place during a login request.
CLOUDFLARE_NETWORKS = tuple(map(ip_network, (
    '173.245.48.0/20', '103.21.244.0/22', '103.22.200.0/22', '103.31.4.0/22',
    '141.101.64.0/18', '108.162.192.0/18', '190.93.240.0/20', '188.114.96.0/20',
    '197.234.240.0/22', '198.41.128.0/17', '162.158.0.0/15', '104.16.0.0/13',
    '104.24.0.0/14', '172.64.0.0/13', '131.0.72.0/22', '2400:cb00::/32',
    '2606:4700::/32', '2803:f800::/32', '2405:b500::/32', '2405:8100::/32',
    '2a06:98c0::/29', '2c0f:f248::/32',
)))


def _address(value):
    if not isinstance(value, str) or len(value) > 45 or '%' in value:
        raise ValueError('Invalid client address')
    address = ip_address(value.strip())
    return getattr(address, 'ipv4_mapped', None) or address


def client_network(request):
    source = settings.LOGIN_CLIENT_IP_SOURCE
    if source == 'remote_addr':
        address = _address(request.META.get('REMOTE_ADDR'))
    elif source == 'pythonanywhere':
        # PythonAnywhere overwrites X-Real-IP with its load balancer's peer.
        address = _address(request.META.get('HTTP_X_REAL_IP'))
    else:
        raise ValueError('Unsupported client address source')

    if any(address in network for network in CLOUDFLARE_NETWORKS):
        if not settings.LOGIN_TRUST_CLOUDFLARE:
            # Do not accidentally apply a shared budget to an entire CDN edge.
            raise ValueError('Cloudflare proxy trust is not configured')
        address = _address(request.META.get('HTTP_CF_CONNECTING_IP'))
    # Forwarded/CF headers from an untrusted direct peer are deliberately ignored.
    if address.version == 6:
        return str(ip_network(f'{address}/64', strict=False))
    return str(address)


def bucket_key(scope, *parts):
    payload = json.dumps(parts, ensure_ascii=True, separators=(',', ':'))
    return salted_hmac(f'login-rate-limit:{scope}', payload, algorithm='sha256').hexdigest()


def consume_bucket(key, limit, now):
    """Reserve before password hashing; denied requests never extend the window."""
    for _ in range(3):
        # Finish competing inserts before acquiring the update lock (MySQL).
        LoginRateLimitBucket.objects.get_or_create(
            key=key, defaults={'expires_at': now + timedelta(seconds=settings.LOGIN_RATE_LIMIT_WINDOW_SECONDS)},
        )
        try:
            with transaction.atomic():
                bucket = LoginRateLimitBucket.objects.select_for_update().get(pk=key)
                if bucket.expires_at <= now:
                    bucket.attempts = 0
                    bucket.expires_at = now + timedelta(seconds=settings.LOGIN_RATE_LIMIT_WINDOW_SECONDS)
                if bucket.attempts >= limit:
                    return max(1, math.ceil((bucket.expires_at - now).total_seconds()))
                bucket.attempts += 1
                bucket.save(update_fields=['attempts', 'expires_at'])
            return 0
        except LoginRateLimitBucket.DoesNotExist:
            # Cleanup may remove an expired bucket before we acquire its lock.
            continue
    raise DatabaseError('Login counter could not be reserved')


def reserve_login_attempt(request):
    network = client_network(request)
    now = timezone.now()
    # Charge the network first to bound rows created by randomized usernames.
    retry = consume_bucket(bucket_key('ip', network), settings.LOGIN_RATE_LIMIT_PER_IP, now)
    if retry:
        return retry
    username = unicodedata.normalize('NFKC', request.POST.get('username', '').strip()).casefold()
    return consume_bucket(
        bucket_key('account-ip', network, username), settings.LOGIN_RATE_LIMIT_PER_ACCOUNT_IP, now,
    )


class LoginRateLimitMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method != 'POST' or request.resolver_match.view_name not in ('login', 'admin:login'):
            return None
        request.sensitive_post_parameters = ('password',)
        try:
            retry = reserve_login_attempt(request)
        except (DatabaseError, ValueError):
            # A failed counter must never silently turn into unlimited guesses.
            logger.error('Login rate limit unavailable; authentication was not attempted')
            return self._response(request, 503, 60)
        if retry:
            return self._response(request, 429, retry)
        return None

    @staticmethod
    def _response(request, status, retry):
        response = render(request, 'core/login_limited.html', {
            'temporarily_unavailable': status == 503,
            'retry_minutes': max(1, math.ceil(retry / 60)),
            'login_path': request.path,
        }, status=status)
        response['Retry-After'] = str(retry)
        add_never_cache_headers(response)
        return response


@register(Tags.security)
def check_login_rate_limit(app_configs, **kwargs):
    errors = []
    if settings.LOGIN_CLIENT_IP_SOURCE not in ('remote_addr', 'pythonanywhere'):
        errors.append(Error('Invalid LOGIN_CLIENT_IP_SOURCE.', id='core.E010'))
    for name in ('LOGIN_RATE_LIMIT_WINDOW_SECONDS', 'LOGIN_RATE_LIMIT_PER_IP', 'LOGIN_RATE_LIMIT_PER_ACCOUNT_IP'):
        value = getattr(settings, name)
        if type(value) is not int or value < 1:
            errors.append(Error(f'{name} must be a positive integer.', id='core.E011'))
    middleware = settings.MIDDLEWARE
    csrf = 'django.middleware.csrf.CsrfViewMiddleware'
    limiter = 'core.login_rate_limit.LoginRateLimitMiddleware'
    if limiter not in middleware or csrf not in middleware or middleware.index(limiter) < middleware.index(csrf):
        errors.append(Error('Login limiter must run after CSRF middleware.', id='core.E012'))
    return errors


@register(Tags.security, deploy=True)
def check_login_proxy_rollout(app_configs, **kwargs):
    if settings.IS_HOSTED and not settings.LOGIN_RATE_LIMIT_PROXY_VERIFIED:
        return [Warning(
            'Verify client IP handling through PythonAnywhere/Cloudflare before rollout.',
            hint='See docs/login_rate_limit.md; only then set LOGIN_RATE_LIMIT_PROXY_VERIFIED=True.',
            id='core.W010',
        )]
    return []
