from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Question, UserProfile


class QuestionSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Question.objects.all().order_by('-created_at')

    def lastmod(self, obj):
        return obj.updated_at or obj.created_at

    def location(self, obj):
        return f'/{obj.slug}/'


class UserProfileSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return UserProfile.objects.filter(user__is_active=True).select_related('user')

    def lastmod(self, obj):
        # Users don't have an updated_at field, so we use a default
        return None

    def location(self, obj):
        return reverse('user_profile', kwargs={'username': obj.user.username})


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['user_homepage', 'about', 'site_statistics']

    def location(self, item):
        return reverse(item)
