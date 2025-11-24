from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import QuestionSitemap, UserProfileSitemap, StaticViewSitemap
from django.views.generic import TemplateView
import os

sitemaps = {
    'questions': QuestionSitemap,
    'users': UserProfileSitemap,
    'static': StaticViewSitemap,
}

# Configurable admin URL path for security
ADMIN_URL_PATH = os.environ.get('ADMIN_URL_PATH', 'admin')

urlpatterns = [
    path(f'{ADMIN_URL_PATH}/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots_txt'),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'
handler403 = 'django.views.defaults.permission_denied'
