import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from lxml import html

from core.models import Answer, Kenarda, Question


class AnswerActionLayoutTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='action-layout-owner')
        cls.other = User.objects.create_user(username='action-layout-other')
        cls.question = Question.objects.create(question_text='Action layout', user=cls.user)
        cls.answer = Answer.objects.create(
            question=cls.question, user=cls.user, answer_text='Original answer',
        )
        cls.other_answer = Answer.objects.create(
            question=cls.question, user=cls.other, answer_text='Another answer',
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_actions_are_between_textarea_and_preview_in_all_editors(self):
        cases = [
            ('edit_answer', [self.answer.pk], 'kenarda-dursun-btn'),
            ('question_detail', [self.question.slug], 'sabaha-birak-btn'),
            ('single_answer', [self.question.slug, self.answer.pk], 'sabaha-birak-btn'),
            ('add_starting_question', [], 'kenarda-dursun-btn'),
            ('add_subquestion', [self.question.slug], 'kenarda-dursun-btn'),
            ('add_question_from_search', [], 'kenarda-dursun-btn'),
            ('add_answer', [self.question.slug], None),
            ('answer_suggest_edit', [self.other_answer.pk], None),
        ]
        for name, args, draft_id in cases:
            with self.subTest(editor=name):
                response = self.client.get(reverse(name, args=args), {'q': 'New title'})
                self.assertEqual(response.status_code, 200)
                page = html.fromstring(response.content)
                textarea, = page.xpath('//textarea[@name="answer_text"]')
                preview, = page.xpath('//*[@id="answer-live-preview-root"]')
                form = textarea.xpath('ancestor::form')[0]
                self.assertIn(preview, form.iter())
                self.assertTrue(form.xpath('.//input[@name="csrfmiddlewaretoken"]'))
                submit, = form.xpath('.//button[@type="submit"]')
                elements = list(form.iter())
                self.assertLess(elements.index(textarea), elements.index(submit))
                self.assertLess(elements.index(submit), elements.index(preview))
                if draft_id:
                    draft, = page.xpath(f'//*[@id="{draft_id}"]')
                    self.assertEqual(draft.get('type'), 'button')
                    self.assertLess(elements.index(textarea), elements.index(draft))
                    self.assertLess(elements.index(draft), elements.index(preview))

    def test_saving_long_edit_draft_does_not_publish_or_clear_content(self):
        content = 'Long draft content.\n' * 3000
        response = self.client.post(
            reverse('kenarda_save'),
            data=json.dumps({
                'answer_id': self.answer.pk, 'question_id': self.question.pk,
                'content': content, 'draft_source': 'answer_edit',
            }),
            content_type='application/json',
        )
        self.assertEqual(response.json()['status'], 'ok')
        draft = Kenarda.objects.get(user=self.user, answer=self.answer, is_sent=False)
        self.assertEqual(draft.content, content)
        self.answer.refresh_from_db()
        self.assertEqual(self.answer.answer_text, 'Original answer')
        response = self.client.get(reverse('edit_answer', args=[self.answer.pk]), {'draft_id': draft.pk})
        page = html.fromstring(response.content)
        # Browsers discard the first newline in textarea markup; lxml retains it.
        rendered = page.xpath('//textarea[@name="answer_text"]')[0].text
        self.assertTrue(rendered.removeprefix('\n') == content)

    def test_update_still_publishes_the_submitted_text(self):
        response = self.client.post(
            reverse('edit_answer', args=[self.answer.pk]), {'answer_text': 'Updated answer'},
        )
        self.assertEqual(response.status_code, 302)
        self.answer.refresh_from_db()
        self.assertEqual(self.answer.answer_text, 'Updated answer')
