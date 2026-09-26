from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from lxml import html

from .left_frame import day_questions, left_frame_context
from .models import Answer, Kenarda, Question


class DayNavigationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='day-reader')
        cls.author = User.objects.create_user(username='day-author')
        cls.other = User.objects.create_user(username='other-author')
        cls.user.userprofile.following.add(cls.author.userprofile)
        cls.day = date(2026, 8, 12)
        cls.first = Question.objects.create(user=cls.other, question_text='First daily topic')
        cls.second = Question.objects.create(user=cls.author, question_text='Second daily topic')
        cls.outside = Question.objects.create(user=cls.other, question_text='Outside selected day', left_frame_pinned=True)
        cls.empty = Question.objects.create(user=cls.user, question_text='No entries')
        cls.add_entry(cls.outside, '2026-08-11T23:59:59', cls.author)
        cls.earliest = cls.add_entry(cls.first, '2026-08-12T00:00:00', cls.other)
        cls.add_entry(cls.second, '2026-08-12T09:00:00', cls.author)
        cls.add_entry(cls.first, '2026-08-12T23:59:59', cls.other)
        cls.add_entry(cls.outside, '2026-08-13T00:00:00', cls.other)
        # An old followed author's entry must not count as activity on this day.
        cls.add_entry(cls.first, '2026-08-10T09:00:00', cls.author)
        Kenarda.objects.create(user=cls.user, question=cls.empty, content='Private draft')

    @classmethod
    def add_entry(cls, question, timestamp, user):
        entry = Answer.objects.create(question=question, user=user, answer_text='Daily entry')
        instant = datetime.fromisoformat(timestamp).replace(tzinfo=ZoneInfo('Europe/Istanbul'))
        Answer.objects.filter(pk=entry.pk).update(created_at=instant)
        return entry

    def context(self, params, user=None):
        request = RequestFactory().get('/', params)
        request.user = user or AnonymousUser()
        return left_frame_context(request, 'page')

    def test_day_uses_local_midnights_unique_topics_and_first_entry_order(self):
        with self.assertNumQueries(1):
            topics = list(day_questions(self.day))
        self.assertEqual([topic.pk for topic in topics], [self.first.pk, self.second.pk])
        self.assertEqual([topic.answers_count for topic in topics], [2, 1])
        self.assertEqual(timezone.localtime(topics[0].first_day_entry).hour, 0)

    def test_editing_old_entry_does_not_move_it_to_today(self):
        Answer.objects.filter(pk=self.earliest.pk).update(updated_at=timezone.now())
        self.assertIn(self.first, day_questions(self.day))
        self.assertNotIn(self.first, day_questions(timezone.localdate()))

    def test_following_matches_day_activity_or_topic_owner_not_old_entries(self):
        context = self.context({'day': self.day.isoformat(), 'followed': '1'}, self.user)
        self.assertEqual(list(context['all_questions']), [self.second])
        self.assertTrue(context['show_followed_only'])

    def test_anonymous_follow_filter_cannot_hide_daily_topics(self):
        context = self.context({'day': self.day.isoformat(), 'followed': '1'})
        self.assertEqual(len(context['all_questions']), 2)
        self.assertFalse(context['show_followed_only'])

    def test_invalid_future_and_out_of_range_dates_have_empty_safe_results(self):
        for value in ('nope', '2026-02-30', '20260812', '0001-01-01', '9999-12-31', '<script>'):
            with self.subTest(value=value):
                context = self.context({'day': value})
                self.assertTrue(context['left_day_error'])
                self.assertFalse(list(context['all_questions']))

    def test_empty_day_is_not_replaced_with_recent_topics(self):
        context = self.context({'day': '2020-01-01'})
        self.assertFalse(context['left_day_error'])
        self.assertEqual(context['all_questions'].paginator.count, 0)

    def test_three_content_views_preserve_the_day_in_topic_links(self):
        paths = [reverse('user_homepage'), reverse('question_detail', args=[self.first.slug]),
                 reverse('single_answer', args=[self.first.slug, self.earliest.pk])]
        for path in paths:
            with self.subTest(path=path):
                response = self.client.get(path, {'day': self.day.isoformat()})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(list(response.context['all_questions_page']), [self.first, self.second])
                page = html.fromstring(response.content)
                links = page.xpath('//*[@id="questions-list"]//a/@href')
                self.assertEqual(len(links), 2)
                self.assertTrue(all('day=2026-08-12' in link for link in links))
                self.assertContains(response, '00:00')

    def test_pagination_stable_ties_and_context_stay_bounded(self):
        for index in range(21):
            question = Question.objects.create(user=self.author, question_text=f'Daily extra {index}')
            self.add_entry(question, '2026-08-12T10:00:00', self.author)
        with self.assertNumQueries(2):
            context = self.context({'day': self.day.isoformat(), 'page': '2'})
            topics = list(context['all_questions'])
            # Rendering titles and creators should not add per-item queries.
            [(topic.question_text, topic.user.username, topic.answers_count) for topic in topics]
        self.assertEqual(len(topics), 3)
        self.assertEqual(context['all_questions'].paginator.count, 23)
        self.assertEqual([topic.pk for topic in topics], sorted(topic.pk for topic in topics))
        self.assertIn('q_page=2', context['left_nav_query'])
        response = self.client.get('/', {'day': self.day.isoformat()})
        page = html.fromstring(response.content)
        next_link = page.xpath('//*[@data-left-pagination]//a[@title="Sonraki Sayfa"]/@href')[0]
        self.assertIn('day=2026-08-12', next_link)
        self.assertIn('page=2', next_link)

    def test_toolbar_keeps_actions_visible_without_explanatory_headings(self):
        self.client.force_login(self.user)
        for query in [{}, {'day': self.day.isoformat()}]:
            page = html.fromstring(self.client.get(reverse('user_homepage'), query).content)
            toolbar = page.xpath('//*[contains(@class, "left-navigation")]')[0]
            self.assertFalse(toolbar.xpath('.//h2'))
            text = toolbar.text_content()
            for label in ['Tümü', 'Takip', 'Tarih']:
                self.assertIn(label, text)
            for label in ['Günün başlıkları', 'Son hareketler', 'Eskiden yeniye']:
                self.assertNotIn(label, text)
            self.assertTrue(toolbar.xpath('.//*[@id="left-date-form"]/@hidden'))
            self.assertEqual(toolbar.xpath('.//*[@id="left-date-toggle"]/@aria-expanded'), ['false'])
            self.assertEqual(toolbar.xpath('.//select[@id="followed-filter-btn"]/@name'), ['followed'])
            self.assertEqual(toolbar.xpath('.//select/option/@value'), ['0', '1'])
            for button, label in [('random-question-btn', 'Doldur'), ('shuffle-btn', 'Git')]:
                self.assertEqual(toolbar.xpath(f'.//*[@id="{button}"]/@title'), [label])
                self.assertTrue(toolbar.xpath(f'.//*[@id="{button}"]/@aria-label'))

    def test_day_switch_resets_only_left_pagination_and_keeps_filters(self):
        request = RequestFactory().get('/topic/', {'day': '2026-08-12', 'q_page': '2', 'a_page': '3', 'followed': '1'})
        request.user = self.user
        context = left_frame_context(request, 'q_page')
        self.assertNotIn('q_page=', context['left_prev_day_url'])
        self.assertIn('a_page=3', context['left_prev_day_url'])
        self.assertIn('followed=1', context['left_prev_day_url'])
        self.assertNotIn('day=', context['left_current_url'])
        self.assertNotIn('day', dict(context['left_form_query']))

    def test_today_has_no_future_navigation_and_default_still_has_pins(self):
        context = self.context({'day': timezone.localdate().isoformat()})
        self.assertEqual(context['left_next_day_url'], '')
        context = self.context({})
        self.assertFalse(context['left_day_active'])
        self.assertEqual(list(context['all_questions'])[0], self.outside)
