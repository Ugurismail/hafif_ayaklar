from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .answer_git import (
    create_answer_suggestion,
    ensure_initial_revision,
)
from .models import Answer, AnswerSuggestion, Notification, Question


class CorrectionWorkflowTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='entry-owner',
            password='pass',
        )
        self.proposer = User.objects.create_user(
            username='helpful-editor',
            password='pass',
        )
        self.outsider = User.objects.create_user(
            username='unrelated-user',
            password='pass',
        )
        self.question = Question.objects.create(
            question_text='Düzeltme akışı testi',
            user=self.owner,
        )
        self.answer = Answer.objects.create(
            question=self.question,
            user=self.owner,
            answer_text='Bu metinde küçük bir hata var.',
        )
        ensure_initial_revision(self.answer)

    def create_suggestion(self, *, summary='Yazım hatasını düzelttim.'):
        return create_answer_suggestion(
            self.answer,
            proposed_by=self.proposer,
            proposed_text='Bu metindeki küçük hatayı düzelttim.',
            change_summary=summary,
        )

    def test_new_notification_links_to_the_exact_suggestion(self):
        suggestion = self.create_suggestion()

        notification = Notification.objects.get(
            notification_type='answer_suggestion',
            recipient=self.owner,
        )

        self.assertEqual(notification.related_suggestion, suggestion)
        self.assertEqual(
            notification.get_target_url(),
            reverse('answer_suggestion_detail', args=[suggestion.id]),
        )

    def test_legacy_suggestion_notification_falls_back_to_inbox(self):
        notification = Notification.objects.create(
            recipient=self.owner,
            sender=self.proposer,
            notification_type='answer_suggestion',
            message='Eski bildirim',
            related_answer=self.answer,
            related_question=self.question,
        )

        self.assertEqual(
            notification.get_target_url(),
            f"{reverse('correction_inbox')}?view=incoming",
        )

    def test_incoming_and_outgoing_inboxes_show_the_same_suggestion(self):
        suggestion = self.create_suggestion()

        self.client.force_login(self.owner)
        incoming_response = self.client.get(reverse('correction_inbox'))
        self.assertEqual(incoming_response.status_code, 200)
        self.assertContains(incoming_response, self.question.question_text)
        self.assertContains(incoming_response, self.proposer.username)
        self.assertContains(
            incoming_response,
            reverse('answer_suggestion_detail', args=[suggestion.id]),
        )

        self.client.force_login(self.proposer)
        outgoing_response = self.client.get(
            reverse('correction_inbox'),
            {'view': 'outgoing'},
        )
        self.assertEqual(outgoing_response.status_code, 200)
        self.assertContains(outgoing_response, self.question.question_text)
        self.assertContains(outgoing_response, self.owner.username)

    def test_suggestion_detail_is_private_to_participants(self):
        suggestion = self.create_suggestion()
        url = reverse('answer_suggestion_detail', args=[suggestion.id])

        anonymous_response = self.client.get(url)
        self.assertEqual(anonymous_response.status_code, 302)

        self.client.force_login(self.outsider)
        outsider_response = self.client.get(url)
        self.assertEqual(outsider_response.status_code, 403)

        self.client.force_login(self.proposer)
        proposer_response = self.client.get(url)
        self.assertEqual(proposer_response.status_code, 200)

        self.client.force_login(self.owner)
        owner_response = self.client.get(url)
        self.assertEqual(owner_response.status_code, 200)

    def test_history_only_exposes_suggestions_visible_to_current_user(self):
        suggestion = self.create_suggestion()
        history_url = reverse('answer_git_history', args=[self.answer.id])

        anonymous_response = self.client.get(history_url)
        self.assertNotContains(anonymous_response, f'Öneri #{suggestion.id}')
        self.assertNotContains(anonymous_response, self.proposer.username)

        self.client.force_login(self.outsider)
        outsider_response = self.client.get(history_url)
        self.assertNotContains(outsider_response, f'Öneri #{suggestion.id}')
        self.assertNotContains(outsider_response, self.proposer.username)

        self.client.force_login(self.proposer)
        proposer_response = self.client.get(history_url)
        self.assertContains(proposer_response, f'Öneri #{suggestion.id}')

        self.client.force_login(self.owner)
        owner_response = self.client.get(history_url)
        self.assertContains(owner_response, f'Öneri #{suggestion.id}')

    def test_opening_detail_marks_only_its_notification_as_read(self):
        first = self.create_suggestion(summary='Birinci öneri')
        second = create_answer_suggestion(
            self.answer,
            proposed_by=self.proposer,
            proposed_text='İkinci ve farklı bir öneri.',
            change_summary='İkinci öneri',
        )
        first_notification = Notification.objects.get(
            related_suggestion=first,
            recipient=self.owner,
        )
        second_notification = Notification.objects.get(
            related_suggestion=second,
            recipient=self.owner,
        )

        self.client.force_login(self.owner)
        self.client.get(
            reverse('answer_suggestion_detail', args=[first.id]),
        )

        first_notification.refresh_from_db()
        second_notification.refresh_from_db()
        self.assertTrue(first_notification.is_read)
        self.assertFalse(second_notification.is_read)

    def test_accepting_suggestion_updates_entry_and_notifies_proposer(self):
        suggestion = self.create_suggestion()
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse('answer_suggestion_accept', args=[suggestion.id]),
            {'review_note': 'Düzeltme yerinde.'},
        )

        self.assertRedirects(
            response,
            reverse('answer_suggestion_detail', args=[suggestion.id]),
        )
        suggestion.refresh_from_db()
        self.answer.refresh_from_db()
        self.assertEqual(suggestion.status, 'accepted')
        self.assertEqual(
            self.answer.answer_text,
            'Bu metindeki küçük hatayı düzelttim.',
        )
        result_notification = Notification.objects.get(
            notification_type='suggestion_result',
            recipient=self.proposer,
        )
        self.assertEqual(result_notification.related_suggestion, suggestion)
        self.assertIn('kabul etti', result_notification.message)

    def test_rejecting_suggestion_keeps_entry_and_notifies_proposer(self):
        suggestion = self.create_suggestion()
        original_text = self.answer.answer_text
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse('answer_suggestion_reject', args=[suggestion.id]),
            {'review_note': 'Bu değişiklik gerekli değil.'},
        )

        self.assertRedirects(
            response,
            reverse('answer_suggestion_detail', args=[suggestion.id]),
        )
        suggestion.refresh_from_db()
        self.answer.refresh_from_db()
        self.assertEqual(suggestion.status, 'rejected')
        self.assertEqual(self.answer.answer_text, original_text)
        result_notification = Notification.objects.get(
            notification_type='suggestion_result',
            recipient=self.proposer,
        )
        self.assertEqual(result_notification.related_suggestion, suggestion)
        self.assertIn('reddetti', result_notification.message)

    def test_suggestion_form_requires_a_plain_summary(self):
        self.client.force_login(self.proposer)

        response = self.client.post(
            reverse('answer_suggest_edit', args=[self.answer.id]),
            {
                'change_summary': '',
                'answer_text': 'Değiştirilmiş içerik.',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bu alan zorunludur.')
        self.assertFalse(AnswerSuggestion.objects.exists())
