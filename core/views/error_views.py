"""Error and debug-only preview views."""

from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import Http404
from django.shortcuts import render


def custom_400_view(request, exception):
    response = render(request, 'core/400.html')
    response.status_code = 400
    return response


def custom_404_view(request, exception):
    response = render(request, '404.html')
    response.status_code = 404
    return response


def custom_403_view(request, exception):
    response = render(request, '403.html')
    response.status_code = 403
    return response


def custom_500_view(request):
    response = render(request, '500.html')
    response.status_code = 500
    return response


def custom_502_view(request):
    response = render(request, 'core/502.html')
    response.status_code = 502
    return response


def _ensure_localhost_request(request):
    host = (request.get_host() or '').split(':', 1)[0]
    if host not in ('127.0.0.1', 'localhost'):
        raise Http404


def debug_show_400(request):
    _ensure_localhost_request(request)
    return custom_400_view(request, exception=None)


def debug_show_403(request):
    _ensure_localhost_request(request)
    return custom_403_view(request, exception=None)


def debug_show_404(request):
    _ensure_localhost_request(request)
    return custom_404_view(request, exception=None)


def debug_show_500(request):
    _ensure_localhost_request(request)
    return custom_500_view(request)


def debug_show_502(request):
    _ensure_localhost_request(request)
    return custom_502_view(request)


def debug_raise_400(request):
    _ensure_localhost_request(request)
    raise SuspiciousOperation('Debug 400')


def debug_raise_403(request):
    _ensure_localhost_request(request)
    raise PermissionDenied('Debug 403')


def debug_raise_404(request):
    _ensure_localhost_request(request)
    raise Http404('Debug 404')


def debug_raise_500(request):
    _ensure_localhost_request(request)
    raise RuntimeError('Debug 500')
