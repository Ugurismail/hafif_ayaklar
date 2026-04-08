from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.templatetags.static import static as static_url
import os

# Configurable admin URL path for security
ADMIN_URL_PATH = os.environ.get('ADMIN_URL_PATH', 'admin')


def sitemap_view(request, *args, **kwargs):
    from django.contrib.sitemaps.views import sitemap
    from core.sitemaps import QuestionSitemap, UserProfileSitemap, StaticViewSitemap

    sitemaps = {
        'questions': QuestionSitemap,
        'users': UserProfileSitemap,
        'static': StaticViewSitemap,
    }
    return sitemap(request, sitemaps=sitemaps, *args, **kwargs)


def logic_home(request, *args, **kwargs):
    from core.views.logic_views import logic_home as view
    return view(request, *args, **kwargs)


def logic_lesson_detail(request, *args, **kwargs):
    from core.views.logic_views import logic_lesson_detail as view
    return view(request, *args, **kwargs)


def logic_level_test(request, *args, **kwargs):
    from core.views.logic_views import logic_level_test as view
    return view(request, *args, **kwargs)

urlpatterns = [
    path(f'{ADMIN_URL_PATH}/', admin.site.urls),
    path('sitemap.xml', sitemap_view, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots_txt'),
    # Google requires at least 48x48 for the Search results icon; serve a 48x48 PNG via /favicon.ico.
    path('favicon.ico', RedirectView.as_view(url=static_url('imgs/favicon-48.png'), permanent=True), name='favicon'),
    path('mantik/', logic_home, name='logic_home'),
    path('mantik/bitirme-testi/', logic_level_test, name='logic_level_test'),
    path('mantik/<slug:lesson_slug>/', logic_lesson_detail, name='logic_lesson_detail'),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers (use our themed templates)
handler400 = 'core.views.misc_views.custom_400_view'
handler403 = 'core.views.misc_views.custom_403_view'
handler404 = 'core.views.misc_views.custom_404_view'
handler500 = 'core.views.misc_views.custom_500_view'
