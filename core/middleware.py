from __future__ import annotations

from datetime import timedelta

from django.db import DatabaseError
from django.http import Http404
from django.shortcuts import render
from django.utils import timezone

from .models import UserProfile


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
    THROTTLE_DELTA = timedelta(minutes=1)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return response

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
            return response

        try:
            updated = UserProfile.objects.filter(user_id=user.id).update(last_seen=now)
            if updated == 0:
                UserProfile.objects.get_or_create(user_id=user.id, defaults={"last_seen": now})
        except DatabaseError:
            return response

        try:
            request.session[self.SESSION_KEY] = now.isoformat()
        except Exception:
            pass

        return response
