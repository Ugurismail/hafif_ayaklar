from django.contrib.auth.models import User
from django.db.models import OuterRef, Q, Subquery
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .logic_course_data import get_logic_course
from .models import Answer, Question


class EntrySitemap(Sitemap):
    changefreq = 'weekly'
    limit = 1000

    def items(self):
        return Answer.objects.filter(user__is_active=True).select_related('question').only(
            'pk', 'question_id', 'question__slug', 'created_at', 'updated_at',
        ).order_by('pk')

    def lastmod(self, obj):
        return obj.updated_at or obj.created_at

    def location(self, obj):
        return reverse('single_answer', args=[obj.question.slug, obj.pk])

    def get_latest_lastmod(self):
        # The index needs one timestamp, not every entry and its related question.
        return self.items().order_by('-updated_at').values_list('updated_at', flat=True).first()


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


class AuthorSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        # Independent subqueries avoid multiplying every entry by every topic.
        return (
            User.objects.filter(is_active=True).annotate(
                latest_entry=Subquery(Answer.objects.filter(user_id=OuterRef('pk'))
                                     .order_by('-updated_at').values('updated_at')[:1]),
                latest_question=Subquery(Question.objects.filter(user_id=OuterRef('pk'))
                                        .order_by('-updated_at').values('updated_at')[:1]),
            ).filter(Q(latest_entry__isnull=False) | Q(latest_question__isnull=False))
            .only('pk', 'username').order_by('pk')
        )

    def lastmod(self, obj):
        return max(value for value in (obj.latest_entry, obj.latest_question) if value is not None)

    def location(self, obj):
        return reverse('public_author', args=[obj.pk])


class ProfileSitemap(AuthorSitemap):
    def location(self, obj):
        return reverse('user_profile', args=[obj.username])
