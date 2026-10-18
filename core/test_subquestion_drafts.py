import json
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from lxml import html

from core.models import Answer, Kenarda, Question, QuestionRelationship


class SubquestionDraftTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='child-author')
        self.other = User.objects.create_user(username='other-author')
        self.parent = Question.objects.create(user=self.user, question_text='Parent fixture')
        self.other_parent = Question.objects.create(user=self.user, question_text='Other parent')
        self.client.force_login(self.user)
        self.url = reverse('add_subquestion', args=[self.parent.slug])
        self.save_url = reverse('kenarda_save')

    def save(self, **overrides):
        data = dict(title='Child fixture', content='Child entry',
                    question_id=self.parent.pk, draft_source='subquestion')
        data.update(overrides)
        return self.client.post(self.save_url, json.dumps(data), content_type='application/json')

    def draft(self, **overrides):
        response = self.save(**overrides)
        self.assertEqual(response.status_code, 200, response.content)
        return Kenarda.objects.get(pk=response.json()['draft_id'])

    def publish(self, draft, **overrides):
        data = dict(draft_id=draft.pk, question_text=draft.title, answer_text=draft.content)
        data.update(overrides)
        return self.client.post(self.url, data)

    def test_siblings_including_same_title_are_distinct_and_rename_updates_only_id(self):
        first = self.draft()
        second = self.draft()
        third = self.draft(title='Another child')
        self.assertEqual(len({first.pk, second.pk, third.pk}), 3)
        response = self.save(draft_id=first.pk, title='Renamed child', content='New content')
        self.assertEqual(response.json()['draft_id'], first.pk)
        first.refresh_from_db()
        second.refresh_from_db()
        self.assertEqual((first.title, first.content), ('Renamed child', 'New content'))
        self.assertEqual(second.content, 'Child entry')
        self.assertEqual(Kenarda.objects.count(), 3)

    def test_list_and_reopen_use_child_title_and_explicit_identity(self):
        draft = self.draft()
        response = self.client.get(reverse('kenarda_list'))
        document = html.fromstring(response.content)
        links = document.xpath('//a[@href=$url]', url=f'{self.url}?draft_id={draft.pk}')
        self.assertTrue(any(draft.title in link.text_content() for link in links))
        response = self.client.get(self.url, {'draft_id': draft.pk})
        self.assertEqual(response.context['form'].initial['question_text'], draft.title)
        self.assertEqual(response.context['form'].initial['answer_text'], draft.content)
        document = html.fromstring(response.content)
        self.assertEqual(document.get_element_by_id('subquestionDraftId').get('value'), str(draft.pk))

    def test_legacy_draft_can_be_updated_without_replacement(self):
        draft = Kenarda.objects.create(user=self.user, question=self.parent, title='Legacy child',
                                      content='Legacy entry', draft_source='subquestion')
        self.assertEqual(self.save(draft_id=str(draft.pk)).status_code, 200)
        self.assertEqual(Kenarda.objects.count(), 1)

    def test_wrong_owner_parent_source_sent_or_answer_cannot_be_loaded_updated_or_published(self):
        answer = Answer.objects.create(user=self.user, question=self.parent, answer_text='Existing')
        for overrides in ({'user': self.other}, {'question': self.other_parent},
                          {'draft_source': 'answer_edit'}, {'is_sent': True}, {'answer': answer}):
            with self.subTest(overrides=overrides):
                data = dict(user=self.user, question=self.parent, title='Private child',
                            content='Private text', draft_source='subquestion')
                data.update(overrides)
                draft = Kenarda.objects.create(**data)
                self.assertEqual(self.save(draft_id=draft.pk).status_code, 404)
                self.assertEqual(self.client.get(self.url, {'draft_id': draft.pk}).status_code, 404)
                self.assertEqual(self.publish(draft).status_code, 404)
                draft.refresh_from_db()
                self.assertEqual(draft.content, 'Private text')

    def test_invalid_payloads_do_not_create_drafts(self):
        for overrides in ({'question_id': True}, {'question_id': -1}, {'draft_id': []},
                          {'draft_id': '9' * 100}, {'draft_id': '12x'}, {'draft_id': 0},
                          {'title': 0}, {'content': []}, {'title': 'x' * 201},
                          {'title': '', 'content': ' '}, {'answer_id': 1}):
            with self.subTest(overrides=overrides):
                self.assertEqual(self.save(**overrides).status_code, 400)
        for raw in ('[]', '{', 'null', b'\xff'):
            self.assertEqual(self.client.post(self.save_url, raw, content_type='application/json').status_code, 400)
        self.assertEqual(self.save(question_id=999999).status_code, 404)
        self.assertEqual(self.save(draft_id=999999).status_code, 404)
        self.assertFalse(Kenarda.objects.exists())

    def test_authentication_and_csrf_required(self):
        anonymous = Client()
        self.assertEqual(anonymous.post(self.save_url, '{}', content_type='application/json').status_code, 302)
        protected = Client(enforce_csrf_checks=True)
        protected.force_login(self.user)
        self.assertEqual(protected.post(self.save_url, '{}', content_type='application/json').status_code, 403)

    def test_direct_send_cannot_turn_child_draft_into_parent_answer(self):
        draft = self.draft()
        response = self.client.post(reverse('kenarda_gonder', args=[draft.pk]))
        self.assertEqual(response.status_code, 400)
        self.assertTrue(Kenarda.objects.filter(pk=draft.pk).exists())
        self.assertFalse(Answer.objects.exists())

    def test_publish_creates_child_and_removes_only_selected_draft(self):
        draft = self.draft()
        sibling = self.draft(title='Sibling')
        ordinary = Kenarda.objects.create(user=self.user, question=self.parent, content='Ordinary')
        response = self.publish(draft)
        child = Question.objects.get(question_text=draft.title)
        self.assertRedirects(response, reverse('question_detail', args=[child.slug]))
        self.assertTrue(QuestionRelationship.objects.filter(parent=self.parent, child=child, user=self.user).exists())
        self.assertEqual(Answer.objects.get().question_id, child.pk)
        self.assertFalse(Kenarda.objects.filter(pk=draft.pk).exists())
        self.assertEqual(set(Kenarda.objects.values_list('pk', flat=True)), {sibling.pk, ordinary.pk})
        self.assertEqual(self.publish(draft).status_code, 404)
        self.assertEqual(Answer.objects.count(), 1)

    def test_invalid_form_and_failed_publish_preserve_draft(self):
        draft = self.draft()
        response = self.publish(draft, answer_text='')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertTrue(Kenarda.objects.filter(pk=draft.pk).exists())
        with patch('core.views.question_page_views.Answer.objects.create', side_effect=RuntimeError('test rollback')):
            with self.assertRaises(RuntimeError):
                self.publish(draft)
        self.assertTrue(Kenarda.objects.filter(pk=draft.pk).exists())
        self.assertFalse(Question.objects.filter(question_text=draft.title).exists())
        self.assertFalse(QuestionRelationship.objects.exists())

    def test_parent_answer_publication_preserves_child_drafts_on_both_paths(self):
        draft = self.draft()
        for route in ('question_detail', 'add_answer'):
            with self.subTest(route=route):
                ordinary = Kenarda.objects.create(user=self.user, question=self.parent, content='Ordinary')
                response = self.client.post(reverse(route, args=[self.parent.slug]), {'answer_text': 'Parent entry'})
                self.assertEqual(response.status_code, 302)
                self.assertTrue(Kenarda.objects.filter(pk=draft.pk).exists())
                self.assertFalse(Kenarda.objects.filter(pk=ordinary.pk).exists())

    def test_parent_editors_do_not_load_child_content(self):
        draft = self.draft()
        answer = Answer.objects.create(user=self.user, question=self.parent, answer_text='Existing')
        urls = (reverse('question_detail', args=[self.parent.slug]),
                reverse('single_answer', args=[self.parent.slug, answer.pk]))
        for url in urls:
            response = self.client.get(url, {'draft_id': draft.pk})
            self.assertEqual(response.status_code, 200)
            self.assertFalse(response.context['draft_content'])
