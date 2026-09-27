import json

from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from core.answer_git import accept_answer_suggestion, create_answer_revision, create_answer_suggestion
from core.entry_references import notify_entry_references, published_entry_reference_ids
from core.models import Answer, EntryReferenceNotice, Kenarda, Notification, Question
from core.templatetags.custom_tags import safe_markdownify


class EntryReferenceNotificationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username='reference-sender')
        cls.recipient = User.objects.create_user(username='reference-recipient')
        cls.other = User.objects.create_user(username='reference-other')
        cls.question = Question.objects.create(user=cls.author, question_text='Referans bildirimi')
        cls.target = Answer.objects.create(user=cls.recipient, question=cls.question, answer_text='Hedef')
        cls.second = Answer.objects.create(user=cls.recipient, question=cls.question, answer_text='Diğer hedef')
        cls.third = Answer.objects.create(user=cls.other, question=cls.question, answer_text='Başka yazar')
        cls.ref = f'#{cls.target.pk}'

    def notices(self):
        return Notification.objects.filter(notification_type='entry_reference')

    def publish(self, text=None):
        return Answer.objects.create(user=self.author, question=self.question,
                                     answer_text=self.ref if text is None else text)

    def test_publishing_notifies_target_author_and_opens_source_entry(self):
        self.client.force_login(self.author)
        response = self.client.post(reverse('add_answer', args=[self.question.slug]), {'answer_text': self.ref})
        self.assertEqual(response.status_code, 302)
        notification = self.notices().get()
        self.assertEqual(notification.recipient_id, self.recipient.pk)
        self.assertEqual(notification.sender_id, self.author.pk)
        self.assertNotEqual(notification.related_answer_id, self.target.pk)
        self.assertIn(self.ref, notification.message)
        self.assertFalse(notification.is_read)
        target_url = reverse('entry_permalink', args=[notification.related_answer_id])
        self.assertEqual(notification.get_target_url(), target_url)
        response = self.client.get(target_url)
        self.assertEqual(response['Location'], reverse('single_answer', args=[self.question.slug, notification.related_answer_id]))

    def test_multiple_references_group_by_owner(self):
        self.publish(f'{self.ref} {self.ref} #{self.second.pk} #{self.third.pk}')
        self.assertEqual(self.notices().count(), 2)
        self.assertEqual(EntryReferenceNotice.objects.count(), 3)
        message = self.notices().get(recipient=self.recipient).message
        self.assertIn(self.ref, message)
        self.assertIn(f'#{self.second.pk}', message)

    def test_edit_sends_only_new_references(self):
        source = self.publish()
        create_answer_revision(source, content=f'{self.ref} #{self.third.pk}', created_by=self.author)
        self.assertEqual(self.notices().filter(recipient=self.recipient).count(), 1)
        self.assertEqual(self.notices().filter(recipient=self.other).count(), 1)

    def test_new_target_for_same_owner_is_a_new_notification(self):
        source = self.publish()
        create_answer_revision(source, content=f'{self.ref} #{self.second.pk}', created_by=self.author)
        self.assertEqual(self.notices().filter(recipient=self.recipient).count(), 2)

    def test_unchanged_and_unrelated_edits_do_not_repeat_read_notification(self):
        source = self.publish()
        self.notices().update(is_read=True)
        source.save()
        source.answer_text += ' Ek açıklama.'
        source.save(update_fields=['answer_text', 'updated_at'])
        self.assertEqual(self.notices().count(), 1)
        self.assertTrue(self.notices().get().is_read)

    def test_removing_and_readding_does_not_repeat_even_if_notification_deleted(self):
        source = self.publish()
        self.notices().delete()
        source.answer_text = 'Referans kaldırıldı'
        source.save()
        source.answer_text = self.ref
        source.save()
        self.assertEqual(EntryReferenceNotice.objects.count(), 1)
        self.assertFalse(self.notices().exists())

    def test_references_in_code_math_urls_and_escaped_text_stay_silent(self):
        for text in [f'`{self.ref}`', f'```\n{self.ref}\n```', f'    {self.ref}',
                     f'${self.ref}$', f'$${self.ref}$$', f'\\{self.ref}',
                     f'[{self.ref}](https://example.com)', f'https://example.com/{self.ref}',
                     f'<a href="https://example.com">{self.ref}</a>',
                     f'<img src="/x.png" alt="{self.ref}">', '#felsefe #2026yılı']:
            with self.subTest(text=text):
                self.publish(text)
                self.assertFalse(self.notices().exists())

    def test_formatted_and_outline_references_notify(self):
        for text in [f'**{self.ref}**', f'== {self.ref}', f'1.1. {self.ref}']:
            source = self.publish(text)
            self.assertTrue(self.notices().filter(related_answer=source).exists())

    def test_self_missing_inactive_and_deleted_targets_stay_silent(self):
        own = self.publish('Kendi entrym')
        User.objects.filter(pk=self.other.pk).update(is_active=False)
        deleted_id = self.second.pk
        self.second.delete()
        self.publish(f'#{own.pk} #{self.third.pk} #{deleted_id} #2147483647 #2147483648')
        self.assertFalse(self.notices().exists())

    def test_preview_reading_and_draft_save_do_not_notify(self):
        self.client.force_login(self.author)
        preview = self.client.post(reverse('answer_live_preview'), json.dumps({'content': self.ref}),
                                   content_type='application/json')
        self.assertEqual(preview.status_code, 200)
        draft = self.client.post(reverse('kenarda_save'), json.dumps({
            'question_id': self.question.pk, 'content': self.ref, 'draft_source': 'answer',
        }), content_type='application/json')
        self.assertEqual(draft.status_code, 200)
        self.assertTrue(Kenarda.objects.filter(user=self.author, content=self.ref).exists())
        safe_markdownify(self.ref)
        self.client.get(reverse('entry_permalink', args=[self.target.pk]))
        self.assertFalse(self.notices().exists())
        self.assertFalse(EntryReferenceNotice.objects.exists())

    def test_unpublished_suggestion_is_silent_then_acceptance_notifies(self):
        source = self.publish('İlk sürüm')
        suggestion = create_answer_suggestion(source, proposed_by=self.other, proposed_text=self.ref)
        self.assertFalse(self.notices().exists())
        accept_answer_suggestion(suggestion, reviewed_by=self.author)
        self.assertEqual(self.notices().get().recipient_id, self.recipient.pk)

    def test_unsaved_text_and_raw_fixture_signals_do_not_notify(self):
        from core.signals import collect_new_entry_references, send_new_entry_reference_notifications

        source = self.publish('İlk sürüm')
        source.answer_text = self.ref
        source.save(update_fields=['upvotes'])
        collect_new_entry_references(Answer, source, raw=True)
        send_new_entry_reference_notifications(Answer, source, raw=True)
        self.assertFalse(self.notices().exists())
        source.refresh_from_db()
        self.assertEqual(source.answer_text, 'İlk sürüm')

    def test_old_references_are_not_backfilled_on_unrelated_edit(self):
        source = self.publish('Eski entry')
        Answer.objects.filter(pk=source.pk).update(answer_text=self.ref)
        source.refresh_from_db()
        source.answer_text += ' Yazım düzeltmesi.'
        source.save()
        self.assertFalse(self.notices().exists())

    def test_database_constraint_and_retry_prevent_duplicate_delivery(self):
        source = self.publish()
        notify_entry_references(source, {self.target.pk}, using='default')
        self.assertEqual(self.notices().count(), 1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            EntryReferenceNotice.objects.create(source=source, target=self.target)

    def test_rollback_leaves_no_notification_or_delivery_history(self):
        with self.assertRaises(RuntimeError):
            with transaction.atomic():
                self.publish()
                raise RuntimeError('Rollback')
        self.assertFalse(self.notices().exists())
        self.assertFalse(EntryReferenceNotice.objects.exists())

    def test_recipient_badge_filter_and_isolation(self):
        source = self.publish()
        self.client.force_login(self.recipient)
        self.assertEqual(self.client.get(reverse('get_unread_notification_count')).json()['count'], 1)
        response = self.client.get(reverse('notification_list'), {'type': 'entry_reference'})
        self.assertContains(response, 'Entry Referansları')
        self.assertContains(response, self.notices().get().message)
        self.assertContains(response, reverse('entry_permalink', args=[source.pk]))
        self.client.force_login(self.other)
        response = self.client.get(reverse('notification_list'), {'type': 'entry_reference'})
        self.assertNotContains(response, self.notices().get().message)

    def test_reference_collection_is_read_only_and_does_not_leak_to_rendering(self):
        with self.assertNumQueries(0):
            self.assertEqual(published_entry_reference_ids(self.ref), {self.target.pk})
        self.assertIn('class="entry-reference"', safe_markdownify(self.ref))

    def test_source_deletion_cleans_its_notification_and_history(self):
        source = self.publish()
        source.delete()
        self.assertFalse(self.notices().exists())
        self.assertFalse(EntryReferenceNotice.objects.exists())
