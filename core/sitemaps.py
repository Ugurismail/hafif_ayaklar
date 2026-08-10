from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Question


class QuestionSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Question.objects.all().order_by('-created_at')

    def lastmod(self, obj):
        return obj.updated_at or obj.created_at

    def location(self, obj):
        return f'/{obj.slug}/'


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['user_homepage', 'about', 'site_statistics']

    def location(self, item):
        return reverse(item)
