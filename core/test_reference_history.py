import csv
import io
import json
from datetime import timedelta
from uuid import uuid4

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Answer, Kenarda, Question, Reference, ReferenceUsage
from .reference_history import bind_reference_history


class ReferenceHistoryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('writer', password='TestPassword123!')
        self.other = User.objects.create_user('other')
        self.client.force_login(self.user)
        self.reference = Reference.objects.create(created_by=self.other, author_name='Ludwig',
            author_surname='Wittgenstein', year=1953, rest='Test edition', metin_ismi='Investigations')
        self.question = Question.objects.create(user=self.user, question_text='Dil üzerine')
        self.context = str(uuid4())
        self.data = {'event_id': str(uuid4()), 'context_id': self.context, 'reference_id': self.reference.pk,
                     'page': '42–45', 'title': 'Özel yazı'}
        self.citation = f'(k:{self.reference.pk} s:42–45)'

    def record(self, **changes):
        return self.client.post(reverse('record_reference_usage'), json.dumps(dict(self.data, **changes)), content_type='application/json')

    def usage(self):
        return ReferenceUsage.objects.get(user=self.user, event_id=self.data['event_id'])

    def test_insertion_is_saved_before_draft_or_publication(self):
        before = timezone.now()
        response = self.record(created_at='1990-01-01T00:00:00Z')
        self.assertEqual(response.status_code, 201)
        usage = self.usage()
        self.assertGreaterEqual(usage.created_at, before)
        self.assertEqual(usage.status, 'writing')
        self.assertFalse(Kenarda.objects.exists())
        self.assertFalse(Answer.objects.exists())
        self.assertIn('Wittgenstein', usage.citation)
        self.assertIn('no-store', response['Cache-Control'])

    def test_retries_are_idempotent_and_do_not_move_time(self):
        self.record()
        before = self.usage().created_at
        self.assertEqual(self.record().status_code, 200)
        self.assertEqual(self.usage().created_at, before)
        self.assertEqual(ReferenceUsage.objects.count(), 1)
        self.assertEqual(self.record(page='46').status_code, 409)
        self.assertEqual(self.record(event_id=str(uuid4())).status_code, 201)
        self.assertEqual(ReferenceUsage.objects.count(), 2)

    def test_auth_csrf_and_methods(self):
        for name in ['reference_history', 'record_reference_usage']:
            self.assertEqual(Client().get(reverse(name)).status_code, 302)
        protected = Client(enforce_csrf_checks=True)
        protected.force_login(self.user)
        self.assertEqual(protected.post(reverse('record_reference_usage'), '{}', content_type='application/json').status_code, 403)
        self.assertEqual(self.client.get(reverse('record_reference_usage')).status_code, 405)
        self.assertEqual(self.client.post(reverse('reference_history')).status_code, 405)

    def test_invalid_data_does_not_write(self):
        for patch in [{'context_id': 'bad'}, {'event_id': None}, {'reference_id': True},
                      {'reference_id': 2**63}, {'page': []}, {'title': {}}, {'title': 'x'*201},
                      {'page': 'x'*101}, {'page': '2) <script>'}, {'page': '2\n3'}]:
            with self.subTest(patch=patch):
                self.assertEqual(self.record(**patch).status_code, 400)
        for body in ['[]', 'null', 'oops']:
            self.assertEqual(self.client.post(reverse('record_reference_usage'), body, content_type='application/json').status_code, 400)
        self.assertEqual(self.record(reference_id=99999999).status_code, 404)
        self.assertFalse(ReferenceUsage.objects.exists())

    def test_cannot_attach_to_another_users_draft(self):
        draft = Kenarda.objects.create(user=self.other, content='secret', title='hidden')
        self.assertEqual(self.record(draft_id=draft.pk).status_code, 404)
        self.assertFalse(ReferenceUsage.objects.exists())

    def test_history_and_export_are_owner_only_and_escaped(self):
        self.record(title='<script>alert(1)</script>')
        response = self.client.get(reverse('reference_history'))
        self.assertContains(response, '&lt;script&gt;')
        self.assertNotContains(response, '<script>alert(1)</script>')
        self.assertIn('no-store', response['Cache-Control'])
        self.client.force_login(self.other)
        self.assertNotContains(self.client.get(reverse('reference_history'), {'user': self.user.pk}), 'Investigations')
        response = self.client.get(reverse('reference_history'), {'format': 'csv', 'user': self.user.pk})
        self.assertNotIn('Investigations', b''.join(response.streaming_content).decode())

    def test_save_draft_then_publish_keeps_original_timestamp(self):
        self.record()
        before = self.usage().created_at
        response = self.client.post(reverse('kenarda_save'), json.dumps({
            'question_id': self.question.pk, 'content': self.citation, 'reference_context': self.context,
        }), content_type='application/json')
        self.assertEqual(response.json()['status'], 'ok')
        usage = self.usage()
        self.assertEqual(usage.status, 'draft')
        self.assertIsNotNone(usage.draft_id)
        response = self.client.post(reverse('kenarda_gonder', args=[usage.draft_id]))
        self.assertEqual(response.json()['status'], 'ok')
        usage.refresh_from_db()
        self.assertEqual(usage.status, 'published')
        self.assertIsNotNone(usage.answer_id)
        self.assertEqual(usage.created_at, before)
        self.assertIsNone(usage.removed_at)

    def test_save_then_publish_from_same_form_without_draft_url(self):
        self.record()
        draft = Kenarda.objects.create(user=self.user, question=self.question, content=self.citation)
        bind_reference_history(self.user, {'reference_context': self.context}, draft=draft)
        response = self.client.post(reverse('add_answer', args=[self.question.slug]), {
            'answer_text': self.citation, 'reference_context': self.context,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.usage().status, 'published')
        self.assertIsNotNone(self.usage().answer_id)

    def test_reopened_child_draft_publishes_to_child_not_parent(self):
        self.record()
        draft = Kenarda.objects.create(user=self.user, question=self.question, content=self.citation,
                                      title='Yeni alt başlık', draft_source='subquestion')
        bind_reference_history(self.user, {'reference_context': self.context}, draft=draft)
        response = self.client.post(reverse('add_subquestion', args=[self.question.slug]), {
            'question_text': draft.title, 'answer_text': self.citation, 'draft_id': draft.pk,
        })
        self.assertEqual(response.status_code, 302)
        usage = self.usage()
        self.assertEqual(usage.status, 'published')
        self.assertEqual(usage.answer.question.question_text, 'Yeni alt başlık')
        self.assertNotEqual(usage.answer.question_id, self.question.pk)
        self.assertIsNone(usage.removed_at)

    def test_same_context_cannot_steal_another_users_usage(self):
        self.record()
        draft = Kenarda.objects.create(user=self.other, content=self.citation)
        bind_reference_history(self.other, {'reference_context': self.context}, draft=draft)
        self.assertIsNone(self.usage().draft_id)

    def test_removal_and_reinsertion_preserve_separate_occurrences(self):
        self.record()
        answer = Answer.objects.create(user=self.user, question=self.question, answer_text=self.citation)
        bind_reference_history(self.user, {'reference_context': self.context}, answer=answer)
        answer.answer_text = 'Kaynak kaldırıldı'
        answer.save()
        bind_reference_history(self.user, {}, answer=answer)
        removed = self.usage().removed_at
        self.assertIsNotNone(removed)
        self.record(event_id=str(uuid4()))
        answer.answer_text = self.citation
        answer.save()
        bind_reference_history(self.user, {'reference_context': self.context}, answer=answer)
        self.assertEqual(self.usage().removed_at, removed)
        self.assertEqual(ReferenceUsage.objects.filter(answer=answer, removed_at__isnull=True).count(), 1)

    def test_deleted_reference_or_draft_preserves_private_history(self):
        self.record()
        draft = Kenarda.objects.create(user=self.user, content=self.citation, title='Private')
        bind_reference_history(self.user, {'reference_context': self.context}, draft=draft)
        self.reference.delete()
        draft.delete()
        usage = self.usage()
        self.assertIsNone(usage.reference_id)
        self.assertIn('Wittgenstein', usage.citation)
        self.assertContains(self.client.get(reverse('reference_history')), 'Taslak silindi')

    def test_csv_formula_protection_unicode_and_filters(self):
        self.reference.author_surname = '=HYPERLINK("bad")'
        self.reference.save()
        self.record(title='@private', page='+123')
        response = self.client.get(reverse('reference_history'), {'format': 'csv'})
        content = b''.join(response.streaming_content).decode('utf-8-sig')
        rows = list(csv.reader(io.StringIO(content)))
        self.assertEqual(len(rows), 2)
        self.assertTrue(rows[1][1].startswith("'="))
        self.assertEqual(rows[1][2], "'+123")
        self.assertEqual(rows[1][3], "'@private")
        self.assertIn('no-store', response['Cache-Control'])
        self.assertNotContains(self.client.get(reverse('reference_history'), {'q': 'no match'}), '@private')
        tomorrow = (timezone.localdate() + timedelta(days=1)).isoformat()
        self.assertNotContains(self.client.get(reverse('reference_history'), {'from': tomorrow}), '@private')
        self.assertEqual(self.client.get(reverse('reference_history'), {'from': '2026-99-99'}).status_code, 200)

    def test_profile_history_link_is_not_public(self):
        url = reverse('user_profile', args=[self.user.username]) + '?tab=kaynaklarim'
        self.assertContains(self.client.get(url), reverse('reference_history'))
        self.client.force_login(self.other)
        self.assertNotContains(self.client.get(url), '> Kullanım geçmişim</a>')

    def test_hourly_limit_is_bounded_but_retry_still_succeeds(self):
        self.record()
        ReferenceUsage.objects.bulk_create([ReferenceUsage(user=self.user, event_id=uuid4(), context_id=uuid4(),
            reference_number=self.reference.pk, citation='Test') for _ in range(299)])
        self.assertEqual(self.record().status_code, 200)
        self.assertEqual(self.record(event_id=str(uuid4())).status_code, 429)
