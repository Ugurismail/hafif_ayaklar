from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Answer, Question


class ExpandedAnswerContentTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(
            username='expanded-answer-owner',
            password='pass',
        )
        self.question = Question.objects.create(
            question_text='Uzun yanit testi',
            user=self.user,
        )
        self.answer = Answer.objects.create(
            question=self.question,
            user=self.user,
            answer_text='Tam yanit metni',
        )
        self.url = reverse('expanded_answer_content', args=[self.answer.id])

    def tearDown(self):
        cache.clear()

    @patch(
        'core.views.answer_page_views.render_answer_content_html',
        return_value='<p>Tam yanit</p>',
    )
    def test_rendered_content_is_cached_for_repeated_expansions(self, render_mock):
        first_response = self.client.get(self.url)
        second_response = self.client.get(self.url)

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(first_response.json()['html'], '<p>Tam yanit</p>')
        self.assertEqual(second_response.json()['html'], '<p>Tam yanit</p>')
        self.assertEqual(render_mock.call_count, 1)

    @patch(
        'core.views.answer_page_views.render_answer_content_html',
        side_effect=['<p>Ilk</p>', '<p>Guncel</p>'],
    )
    def test_answer_update_invalidates_cached_content(self, render_mock):
        first_response = self.client.get(self.url)

        Answer.objects.filter(id=self.answer.id).update(
            answer_text='Guncel yanit metni',
            updated_at=timezone.now() + timedelta(seconds=1),
        )
        second_response = self.client.get(self.url)

        self.assertEqual(first_response.json()['html'], '<p>Ilk</p>')
        self.assertEqual(second_response.json()['html'], '<p>Guncel</p>')
        self.assertEqual(render_mock.call_count, 2)

    def test_homepage_read_more_has_timeout_and_retry_state(self):
        response = self.client.get(reverse('user_homepage'))
        content = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn('const readMoreTimeoutMs = 10000;', content)
        self.assertIn("controller.abort();", content)
        self.assertIn("Yükleme gecikti · tekrar dene", content)
        self.assertNotIn("window.location.href = link.href;", content)
