from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

from core.models import Answer, AnswerFollow, Message, Notification, Question, QuestionFollow, QuestionRelationship, SavedItem, Vote


class NotificationDeliveryTests(TestCase):
    def setUp(self):
        cache.clear()
        self.addCleanup(cache.clear)
        self.author = User.objects.create_user(username='writer')
        self.reader = User.objects.create_user(username='Reader')
        self.question = Question.objects.create(user=self.author, question_text='Delivery test')
        self.client.force_login(self.reader)

    def notices(self, kind):
        return Notification.objects.filter(recipient=self.reader, notification_type=kind)

    def answer(self, text='A new entry'):
        return Answer.objects.create(question=self.question, user=self.author, answer_text=text)

    def test_opening_conversation_reads_only_messages_not_other_notifications(self):
        notice = Notification.objects.create(recipient=self.reader, sender=self.author, notification_type='mention', message='test')
        message = Message.objects.create(sender=self.author, recipient=self.reader, body='Hello')
        self.assertEqual(self.client.get(reverse('navbar_status')).json()['message_count'], 1)
        response = self.client.get(reverse('message_detail', args=[self.author.username]))
        self.assertEqual(response.status_code, 200)
        message.refresh_from_db()
        notice.refresh_from_db()
        self.assertTrue(message.is_read)
        self.assertFalse(notice.is_read)
        status = self.client.get(reverse('navbar_status')).json()
        self.assertEqual((status['message_count'], status['notification_count']), (0, 1))

    def test_new_message_is_not_hidden_by_cached_zero(self):
        self.client.get(reverse('navbar_status'))
        Message.objects.create(sender=self.author, recipient=self.reader, body='Hello')
        self.assertEqual(self.client.get(reverse('navbar_status')).json()['message_count'], 1)

    def test_mentions_case_variants_once_and_new_mentions_on_any_save_path(self):
        entry = self.answer('@reader @Reader')
        self.assertEqual(self.notices('mention').count(), 1)
        entry.answer_text += ' edited'
        entry.save(update_fields=['answer_text'])
        self.assertEqual(self.notices('mention').count(), 1)
        another = self.answer()
        another.answer_text = '@reader added later'
        another.save(update_fields=['answer_text'])
        self.assertEqual(self.notices('mention').count(), 2)

    def test_add_answer_http_route_does_not_duplicate_mention(self):
        self.client.force_login(self.author)
        response = self.client.post(reverse('add_answer', args=[self.question.slug]), {'answer_text': '@reader hi'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.notices('mention').count(), 1)

    def test_self_mentions_and_inactive_accounts_are_silent(self):
        self.answer('@writer')
        self.reader.is_active = False
        self.reader.save(update_fields=['is_active'])
        self.answer('@Reader')
        self.assertFalse(Notification.objects.filter(notification_type='mention').exists())

    def test_followed_question_new_answer_and_followed_author(self):
        QuestionFollow.objects.create(question=self.question, user=self.reader)
        self.reader.userprofile.following.add(self.author.userprofile)
        entry = self.answer()
        for kind in ['new_answer', 'followed_user_entry']:
            self.assertEqual(self.notices(kind).get().related_answer_id, entry.pk)

    def test_followed_entry_notifies_only_content_changes(self):
        entry = self.answer()
        AnswerFollow.objects.create(answer=entry, user=self.reader)
        entry.upvotes = 1
        entry.save(update_fields=['upvotes'])
        entry.save()
        self.assertFalse(self.notices('answer_update').exists())
        entry.answer_text = 'Changed content'
        entry.save(update_fields=['answer_text'])
        self.assertEqual(self.notices('answer_update').count(), 1)

    def test_followed_question_notifies_only_title_changes(self):
        QuestionFollow.objects.create(question=self.question, user=self.reader)
        self.question.left_frame_pinned = True
        self.question.save(update_fields=['left_frame_pinned'])
        self.question.save()
        self.assertFalse(self.notices('question_update').exists())
        self.question.question_text = 'Changed title'
        self.question.save(update_fields=['question_text'])
        self.assertEqual(self.notices('question_update').count(), 1)

    def test_new_subquestion_uses_relationship_author_and_does_not_repeat_on_update(self):
        QuestionFollow.objects.create(question=self.question, user=self.reader)
        child = Question.objects.create(user=self.reader, question_text='Existing child')
        relation = QuestionRelationship.objects.create(parent=self.question, child=child, user=self.author)
        notice = self.notices('new_subquestion').get()
        self.assertEqual(notice.sender_id, self.author.pk)
        self.assertEqual(notice.related_question_id, child.pk)
        relation.save()
        self.assertEqual(self.notices('new_subquestion').count(), 1)

    def test_following_user_and_question_notifies_owner_once(self):
        for name, args, kind in [('follow_user', [self.author.username], 'new_follower'),
                                  ('follow_question', [self.question.pk], 'question_follow')]:
            url = reverse(name, args=args)
            self.client.post(url)
            self.client.post(url)
            self.assertEqual(self.client.get(url).status_code, 405)
            self.assertEqual(Notification.objects.filter(recipient=self.author, notification_type=kind).count(), 1)

    def test_message_sidebar_has_shared_navigation_styles_and_pagination(self):
        for index in range(25):
            q = Question.objects.create(user=self.author, question_text=f'Sidebar {index}')
            Answer.objects.create(question=q, user=self.author, answer_text='Entry')
        for url in [reverse('message_list'), reverse('message_detail', args=[self.author.username])]:
            response = self.client.get(url)
            self.assertContains(response, 'css/left_navigation.css')
            self.assertContains(response, 'css/messages.css')
            self.assertEqual(response.context['left_page_param'], 'page')
            self.assertLessEqual(len(response.context['all_questions_page']), 20)

    def test_vote_and_save_notify_author_but_undo_does_not(self):
        entry = self.answer()
        payload = {'content_type': 'answer', 'object_id': entry.pk}
        for name, data, kind in [('vote', {**payload, 'value': 1}, 'answer_vote'),
                                  ('save_item', payload, 'answer_save')]:
            response = self.client.post(reverse(name), data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(Notification.objects.filter(recipient=self.author, notification_type=kind).count(), 1)
            self.client.post(reverse(name), data)
            self.assertEqual(Notification.objects.filter(recipient=self.author, notification_type=kind).count(), 1)

    def test_vote_and_save_do_not_silently_lose_notifications(self):
        entry = self.answer()
        payload = {'content_type': 'answer', 'object_id': entry.pk}
        for name, data, method in [('vote', {**payload, 'value': 1}, 'create_answer_vote_notification'),
                                    ('save_item', payload, 'create_answer_save_notification')]:
            with patch.object(Notification, method, side_effect=RuntimeError('test notification failure')):
                with self.assertRaises(RuntimeError):
                    self.client.post(reverse(name), data)
            self.assertFalse(Vote.objects.exists())
            self.assertFalse(SavedItem.objects.exists())
            entry.refresh_from_db()
            self.assertEqual(entry.upvotes, 0)
