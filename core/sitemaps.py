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
    priority = 0.7

    def items(self):
        return UserProfile.objects.filter(user__is_active=True).select_related('user')

    def lastmod(self, obj):
        latest_question = obj.user.questions.order_by('-updated_at').values_list('updated_at', flat=True).first()
        latest_answer = obj.user.answers.order_by('-updated_at').values_list('updated_at', flat=True).first()
        timestamps = [ts for ts in (obj.last_seen, latest_question, latest_answer) if ts is not None]
        return max(timestamps) if timestamps else None

    def location(self, obj):
        return reverse('user_profile', kwargs={'username': obj.user.username})


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['user_homepage', 'about', 'site_statistics']

    def location(self, item):
        return reverse(item)
