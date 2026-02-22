from __future__ import annotations

import hashlib
import ipaddress
from datetime import timedelta

from django.conf import settings
from django.db import DatabaseError
from django.http import Http404
from django.shortcuts import render
from django.utils import timezone

from .models import DailyVisitor, UserProfile


class CustomErrorPagesMiddleware:
    """
    Forces custom 404 pages on hosted environments even if DEBUG=True.

    This avoids Django's technical 404 pages leaking into production if DEBUG
    is accidentally enabled on the server.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if self._should_use_custom_errors(request) and getattr(response, "status_code", None) == 404:
            return render(request, "404.html", status=404)
        return response

    def process_exception(self, request, exception):
        if self._should_use_custom_errors(request) and isinstance(exception, Http404):
            return render(request, "404.html", status=404)
        return None

    @staticmethod
    def _should_use_custom_errors(request):
        try:
            host = (request.get_host() or "").split(":", 1)[0].lower()
        except Exception:
            host = ""
        return host not in {"127.0.0.1", "localhost"}


class LastSeenMiddleware:
    """
    Tracks authenticated users' "last active" time.

    Notes:
    - This is not "last_login". It updates while the user is browsing the site.
    - Updates are throttled to avoid a DB write on every request.
    """

    SESSION_KEY = "_last_seen_update_ts"
    VISITOR_COOKIE_KEY = "_daily_visitor_seen"
    THROTTLE_DELTA = timedelta(minutes=1)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self._update_last_seen(request)
        self._track_daily_unique_visitor(request, response)
        return response

    def _update_last_seen(self, request):
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return

        now = timezone.now()

        try:
            last_update_iso = request.session.get(self.SESSION_KEY)
        except Exception:
            last_update_iso = None

        if last_update_iso:
            try:
                last_update = timezone.datetime.fromisoformat(last_update_iso)
                if timezone.is_naive(last_update):
                    last_update = timezone.make_aware(last_update, timezone.get_current_timezone())
            except Exception:
                last_update = None
        else:
            last_update = None

        if last_update and (now - last_update) < self.THROTTLE_DELTA:
            return

        try:
            updated = UserProfile.objects.filter(user_id=user.id).update(last_seen=now)
            if updated == 0:
                UserProfile.objects.get_or_create(user_id=user.id, defaults={"last_seen": now})
        except DatabaseError:
            return

        try:
            request.session[self.SESSION_KEY] = now.isoformat()
        except Exception:
            pass

    def _track_daily_unique_visitor(self, request, response):
        if not self._should_track_unique_visitor(request):
            return

        today = timezone.localdate()
        today_marker = today.isoformat()

        if request.COOKIES.get(self.VISITOR_COOKIE_KEY) == today_marker:
            return

        visitor_hash = self._build_daily_visitor_hash(request, today)
        if visitor_hash:
            try:
                DailyVisitor.objects.get_or_create(date=today, visitor_hash=visitor_hash)
            except DatabaseError:
                return

        try:
            response.set_cookie(
                self.VISITOR_COOKIE_KEY,
                today_marker,
                max_age=60 * 60 * 24 * 2,
                secure=getattr(settings, "SESSION_COOKIE_SECURE", False),
                httponly=True,
                samesite="Lax",
            )
        except Exception:
            return

    @staticmethod
    def _should_track_unique_visitor(request):
        """
        Count only real page navigations.

        This prevents noisy probes (e.g. /.well-known/...), static/media loads,
        and non-document fetches from inflating daily unique visitor stats.
        """
        if request.method != "GET":
            return False

        path = (request.path or "").lower()
        if path.startswith("/static/") or path.startswith("/media/"):
            return False
        if path == "/favicon.ico" or path.startswith("/.well-known/"):
            return False

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return False

        sec_fetch_dest = (request.META.get("HTTP_SEC_FETCH_DEST") or "").lower()
        if sec_fetch_dest and sec_fetch_dest != "document":
            return False

        accept = (request.META.get("HTTP_ACCEPT") or "").lower()
        if accept and "text/html" not in accept and "application/xhtml+xml" not in accept:
            return False

        return True

    @staticmethod
    def _build_daily_visitor_hash(request, day):
        ip_value = LastSeenMiddleware._get_client_ip(request)
        if not ip_value:
            return None

        anonymized_ip = LastSeenMiddleware._anonymize_ip(ip_value)
        user_agent = (request.META.get("HTTP_USER_AGENT") or "")[:200]
        payload = f"{settings.SECRET_KEY}|{day.isoformat()}|{anonymized_ip}|{user_agent}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    @staticmethod
    def _get_client_ip(request):
        forwarded = (request.META.get("HTTP_X_FORWARDED_FOR") or "").strip()
        if forwarded:
            raw_ip = forwarded.split(",")[0].strip()
        else:
            raw_ip = (
                (request.META.get("HTTP_X_REAL_IP") or "").strip()
                or (request.META.get("REMOTE_ADDR") or "").strip()
            )

        if not raw_ip:
            return None

        try:
            ipaddress.ip_address(raw_ip)
        except ValueError:
            return None
        return raw_ip

    @staticmethod
    def _anonymize_ip(raw_ip):
        ip_obj = ipaddress.ip_address(raw_ip)
        if isinstance(ip_obj, ipaddress.IPv4Address):
            octets = raw_ip.split(".")
            octets[-1] = "0"
            return ".".join(octets)

        network = ipaddress.IPv6Network(f"{raw_ip}/64", strict=False)
        return f"{network.network_address.compressed}/64"
