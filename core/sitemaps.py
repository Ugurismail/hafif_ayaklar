from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .logic_course_data import get_logic_course
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
        return [
            'user_homepage',
            'about',
            'site_statistics',
            'logic_home',
            'logic_level_test',
        ]

    def location(self, item):
        return reverse(item)


class LogicLessonSitemap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return [lesson['slug'] for lesson in get_logic_course()['lessons']]

    def location(self, lesson_slug):
        return reverse('logic_lesson_detail', args=[lesson_slug])
