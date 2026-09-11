"""Tombstones for removed tools; do not route these paths to entry slugs."""

from django.http import HttpResponseGone


def retired_feature(request):
    response = HttpResponseGone('Bu ozellik kaldirildi.', content_type='text/plain; charset=utf-8')
    response['X-Robots-Tag'] = 'noindex'
    return response
