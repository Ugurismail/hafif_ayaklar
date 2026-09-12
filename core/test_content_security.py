from urllib.parse import parse_qs, urlsplit
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db import close_old_connections, connections
from django.test import Client, RequestFactory, TestCase, TransactionTestCase, skipUnlessDBFeature
from django.urls import reverse

from .models import Answer, ContentReport, SavedCollection, SavedCollectionItem, SavedItem, Vote, Question
from .views.vote_save_views import get_saved_items, vote


class ContentSecurityTests(TestCase):
    def setUp(self):
        cache.clear()
        self.addCleanup(cache.clear)
        self.owner = User.objects.create_user(username='owner')
        self.reader = User.objects.create_user(username='reader')
        self.question = Question.objects.create(user=self.owner, question_text='Security target')
        self.answer = Answer.objects.create(user=self.owner, question=self.question, answer_text='Public entry')
        self.client.force_login(self.reader)
        self.target = {'content_type': 'answer', 'object_id': self.answer.pk}
        self.ct = ContentType.objects.get_for_model(Answer)

    def test_external_report_redirects_are_blocked(self):
        for target in ('https://outside.invalid/', '//outside.invalid/', 'http://testserver/', '/\\outside.invalid/', 'javascript:alert(1)'):
            response = self.client.get(reverse('report_content'), {'content_type': 'bad', 'next': target}, secure=True)
            self.assertRedirects(response, '/', fetch_redirect_response=False)

    def test_report_preserves_local_query_and_fragment(self):
        target = '/search/?q=hello&tab=answers#entry'
        response = self.client.post(reverse('report_content'), {**self.target, 'reason': 'spam', 'next': target})
        self.assertRedirects(response, target, fetch_redirect_response=False)
        self.assertTrue(ContentReport.objects.filter(reporter=self.reader).exists())
        response = self.client.post(reverse('report_content'), {**self.target, 'reason': 'invalid', 'next': target})
        self.assertEqual(parse_qs(urlsplit(response['Location']).query)['next'], [target])

    def test_successful_report_cannot_redirect_off_site(self):
        response = self.client.post(reverse('report_content'), {
            **self.target, 'reason': 'spam', 'next': 'https://outside.invalid/',
        }, secure=True)
        self.assertRedirects(response, '/', fetch_redirect_response=False)
        self.assertTrue(ContentReport.objects.filter(reporter=self.reader).exists())

    def test_unsupported_targets_cannot_be_voted_saved_or_inspected(self):
        for content_type in ('user', 'kenarda', 'radioprogram', 'cikistesti', 'notification'):
            data = {'content_type': content_type, 'object_id': self.owner.pk, 'value': 1}
            for route in ('vote', 'save_item'):
                self.assertEqual(self.client.post(reverse(route), data).status_code, 400)
            self.assertEqual(self.client.get(reverse('saved_item_collection_options'), data).status_code, 400)
        self.assertFalse(Vote.objects.exists())
        self.assertFalse(SavedItem.objects.exists())

    def test_invalid_ids_and_missing_targets_never_create_records(self):
        for value in ('oops', '0', '-1', '9' * 100):
            for route in ('vote', 'save_item'):
                response = self.client.post(reverse(route), {**self.target, 'object_id': value, 'value': 1})
                self.assertEqual(response.status_code, 400)
        for route in ('vote', 'save_item'):
            self.assertEqual(self.client.post(reverse(route), {**self.target, 'object_id': 2147483647, 'value': 1}).status_code, 404)
        self.assertFalse(SavedItem.objects.exists())
        self.assertFalse(Vote.objects.exists())

    def test_vote_toggle_and_timestamp_preservation(self):
        original_time = self.answer.updated_at
        for value, totals in [(1, (1, 0, 1)), (-1, (0, 1, -1)), (-1, (0, 0, 0))]:
            response = self.client.post(reverse('vote'), {**self.target, 'value': value})
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual((data['upvotes'], data['downvotes'], data['user_vote_value']), totals)
            self.answer.refresh_from_db()
            self.assertEqual(self.answer.updated_at, original_time)
            self.assertEqual((self.answer.upvotes, self.answer.downvotes), totals[:2])

    def test_vote_failure_rolls_back_vote_record(self):
        with patch('django.db.models.query.QuerySet.aggregate', side_effect=RuntimeError('local rollback probe')):
            with self.assertRaises(RuntimeError):
                self.client.post(reverse('vote'), {**self.target, 'value': 1})
        self.assertFalse(Vote.objects.exists())

    def test_saved_lists_are_owner_only(self):
        SavedItem.objects.create(user=self.owner, content_type=self.ct, object_id=self.answer.pk)
        response = self.client.get(reverse('get_saved_items'), {'username': self.owner.username})
        self.assertEqual(response.status_code, 403)
        self.client.force_login(self.owner)
        self.assertEqual(len(self.client.get(reverse('get_saved_items')).json()['saved_items']), 1)

    def test_invalid_collection_input_has_no_partial_save(self):
        other = SavedCollection.objects.create(user=self.owner, name='Private')
        for extra in ({'new_collection_name': 'x' * 81}, {'collection_ids': [other.pk]}, {'collection_ids': ['oops']}, {'action': 'invalid'}):
            response = self.client.post(reverse('save_item'), {**self.target, 'action': 'save', **extra})
            self.assertEqual(response.status_code, 400)
            self.assertFalse(SavedItem.objects.exists())

    def test_unsave_is_idempotent_and_legacy_toggle_still_works(self):
        for _ in range(2):
            response = self.client.post(reverse('save_item'), {**self.target, 'action': 'unsave'})
            self.assertEqual(response.json()['status'], 'unsaved')
            self.assertFalse(SavedItem.objects.exists())
        self.assertEqual(self.client.post(reverse('save_item'), self.target).json()['status'], 'saved')
        self.assertEqual(self.client.post(reverse('save_item'), self.target).json()['status'], 'unsaved')

    def test_normal_collection_save_and_update(self):
        first = self.client.post(reverse('save_item'), {**self.target, 'action': 'save', 'new_collection_name': 'Reading'})
        self.assertEqual(first.status_code, 200)
        item_id = first.json()['saved_item_id']
        second = self.client.post(reverse('save_item'), {**self.target, 'action': 'save', 'new_collection_name': 'Reading'})
        self.assertEqual(second.json()['saved_item_id'], item_id)
        self.assertEqual(SavedItem.objects.count(), 1)
        self.assertEqual(SavedCollectionItem.objects.count(), 1)
        options = self.client.get(reverse('saved_item_collection_options'), self.target).json()
        self.assertTrue(options['is_saved'])
        self.assertTrue(options['collections'][0]['selected'])

    def test_invalid_update_preserves_current_collections(self):
        item = SavedItem.objects.create(user=self.reader, content_type=self.ct, object_id=self.answer.pk)
        collection = SavedCollection.objects.create(user=self.reader, name='Reading')
        SavedCollectionItem.objects.create(collection=collection, saved_item=item)
        response = self.client.post(reverse('update_saved_item_collections', args=[item.pk]), {'collection_ids': ['oops']})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(item.collection_links.count(), 1)

    def test_login_post_and_csrf_requirements(self):
        for route in ('vote', 'save_item'):
            self.assertEqual(self.client.get(reverse(route)).status_code, 405)
        anonymous = Client()
        for route in ('vote', 'save_item'):
            self.assertEqual(anonymous.post(reverse(route), {**self.target, 'value': 1}).status_code, 403)
        csrf = Client(enforce_csrf_checks=True)
        csrf.force_login(self.reader)
        for route in ('vote', 'save_item', 'report_content'):
            self.assertEqual(csrf.post(reverse(route), {**self.target, 'value': 1, 'reason': 'spam'}).status_code, 403)

    def test_question_vote_save_search_and_unsave(self):
        target = {'content_type': 'question', 'object_id': self.question.pk}
        original_time = self.question.updated_at
        response = self.client.post(reverse('vote'), {**target, 'value': 1})
        self.assertEqual(response.json()['upvotes'], 1)
        self.question.refresh_from_db()
        self.assertEqual(self.question.updated_at, original_time)
        self.assertEqual(self.client.post(reverse('save_item'), target).json()['status'], 'saved')
        response = self.client.get(reverse('get_saved_items'), {'q': 'security', 'username': self.reader.username})
        self.assertEqual(response.json()['saved_items'][0]['id'], self.question.pk)
        self.assertIn('private', response['Cache-Control'])
        self.assertIn('no-store', response['Cache-Control'])
        self.assertEqual(self.client.post(reverse('save_item'), {**target, 'action': 'unsave'}).json()['save_count'], 0)

    def test_multiple_voters_have_independent_votes(self):
        self.client.post(reverse('vote'), {**self.target, 'value': 1})
        self.client.force_login(self.owner)
        response = self.client.post(reverse('vote'), {**self.target, 'value': -1})
        self.assertEqual(response.json(), {'upvotes': 1, 'downvotes': 1, 'user_vote_value': -1})
        self.client.force_login(self.reader)
        response = self.client.post(reverse('vote'), {**self.target, 'value': 1})
        self.assertEqual(response.json(), {'upvotes': 0, 'downvotes': 1, 'user_vote_value': 0})
        self.assertEqual(Vote.objects.get().user_id, self.owner.pk)

    def test_invalid_vote_values_do_not_change_existing_vote(self):
        self.client.post(reverse('vote'), {**self.target, 'value': 1})
        for value in ('', 'oops', '0', '2', '-2', '9' * 100):
            self.assertEqual(self.client.post(reverse('vote'), {**self.target, 'value': value}).status_code, 400)
        self.assertEqual(Vote.objects.get().value, 1)
        self.answer.refresh_from_db()
        self.assertEqual(self.answer.upvotes, 1)

    def test_new_save_failure_rolls_back_item_and_collection(self):
        with patch.object(SavedCollectionItem.objects, 'get_or_create', side_effect=RuntimeError('local rollback probe')):
            with self.assertRaises(RuntimeError):
                self.client.post(reverse('save_item'), {**self.target, 'action': 'save', 'new_collection_name': 'Reading'})
        self.assertFalse(SavedItem.objects.exists())
        self.assertFalse(SavedCollection.objects.exists())

    def test_collection_update_failure_preserves_previous_selection(self):
        item = SavedItem.objects.create(user=self.reader, content_type=self.ct, object_id=self.answer.pk)
        first = SavedCollection.objects.create(user=self.reader, name='First')
        second = SavedCollection.objects.create(user=self.reader, name='Second')
        SavedCollectionItem.objects.create(collection=first, saved_item=item)
        for route, data in (
            (reverse('update_saved_item_collections', args=[item.pk]), {'collection_ids': [second.pk]}),
            (reverse('save_item'), {**self.target, 'action': 'save', 'collection_ids': [second.pk]}),
        ):
            with patch.object(SavedCollectionItem.objects, 'get_or_create', side_effect=RuntimeError('local rollback probe')):
                with self.assertRaises(RuntimeError):
                    self.client.post(route, data)
            self.assertEqual(list(item.collection_links.values_list('collection_id', flat=True)), [first.pk])

    def test_other_users_collections_and_saved_items_cannot_be_modified(self):
        own_item = SavedItem.objects.create(user=self.reader, content_type=self.ct, object_id=self.answer.pk)
        other_item = SavedItem.objects.create(user=self.owner, content_type=self.ct, object_id=self.answer.pk)
        other_collection = SavedCollection.objects.create(user=self.owner, name='Private')
        SavedCollectionItem.objects.create(collection=other_collection, saved_item=other_item)
        response = self.client.post(reverse('update_saved_item_collections', args=[own_item.pk]), {'collection_ids': [other_collection.pk]})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.client.post(reverse('update_saved_item_collections', args=[other_item.pk])).status_code, 404)
        options = self.client.get(reverse('saved_item_collection_options'), self.target).json()
        self.assertEqual(options['collections'], [])
        self.client.post(reverse('save_item'), {**self.target, 'action': 'unsave'})
        self.assertTrue(SavedItem.objects.filter(pk=other_item.pk).exists())
        self.assertEqual(other_item.collection_links.count(), 1)

    def test_empty_selection_intentionally_clears_collection_links_not_saved_item(self):
        item = SavedItem.objects.create(user=self.reader, content_type=self.ct, object_id=self.answer.pk)
        collection = SavedCollection.objects.create(user=self.reader, name='Reading')
        SavedCollectionItem.objects.create(collection=collection, saved_item=item)
        response = self.client.post(reverse('update_saved_item_collections', args=[item.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(item.collection_links.exists())
        self.assertTrue(SavedItem.objects.filter(pk=item.pk).exists())

    def test_stale_and_unsupported_legacy_saves_are_ignored(self):
        SavedItem.objects.create(user=self.reader, content_type=self.ct, object_id=2147483647)
        SavedItem.objects.create(user=self.reader, content_type=ContentType.objects.get_for_model(User), object_id=self.owner.pk)
        SavedItem.objects.create(user=self.reader, content_type=self.ct, object_id=self.answer.pk)
        items = self.client.get(reverse('get_saved_items')).json()['saved_items']
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['type'], 'answer')
        self.assertEqual(SavedItem.objects.count(), 3)

    def test_saved_list_uses_bulk_content_queries(self):
        question_ct = ContentType.objects.get_for_model(Question)
        SavedItem.objects.create(user=self.reader, content_type=question_ct, object_id=self.question.pk)
        for i in range(8):
            answer = Answer.objects.create(user=self.owner, question=self.question, answer_text=f'Entry {i}')
            SavedItem.objects.create(user=self.reader, content_type=self.ct, object_id=answer.pk)
        request = RequestFactory().get(reverse('get_saved_items'))
        request.user = self.reader
        # ContentType lookups are warm; content loading stays at three queries.
        with self.assertNumQueries(3):
            response = get_saved_items(request)
        self.assertEqual(response.status_code, 200)

    def test_valid_csrf_requests_still_work(self):
        csrf = Client(enforce_csrf_checks=True)
        csrf.force_login(self.reader)
        response = csrf.get(reverse('report_content'), self.target)
        self.assertEqual(response.status_code, 200)
        token = csrf.cookies['csrftoken'].value
        for route in ('vote', 'save_item'):
            response = csrf.post(reverse(route), {**self.target, 'value': 1}, HTTP_X_CSRFTOKEN=token)
            self.assertEqual(response.status_code, 200)


class ConcurrentVoteTests(TransactionTestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner')
        self.question = Question.objects.create(user=self.owner, question_text='Concurrent target')
        self.answer = Answer.objects.create(user=self.owner, question=self.question, answer_text='Entry')

    def run_parallel_votes(self, user_ids):
        barrier = Barrier(len(user_ids))

        def cast(user_id):
            close_old_connections()
            try:
                request = RequestFactory().post('/vote/', {
                    'content_type': 'answer', 'object_id': self.answer.pk, 'value': 1,
                })
                request.user = User.objects.get(pk=user_id)
                barrier.wait(timeout=10)
                return vote(request).status_code
            finally:
                connections.close_all()

        with patch('core.views.vote_save_views.Notification.create_answer_vote_notification'):
            with ThreadPoolExecutor(max_workers=len(user_ids)) as executor:
                self.assertEqual(list(executor.map(cast, user_ids)), [200] * len(user_ids))

    @skipUnlessDBFeature('has_select_for_update')
    def test_parallel_voters_keep_totals_consistent(self):
        user_ids = [User.objects.create_user(username=f'reader-{i}').pk for i in range(4)]
        self.run_parallel_votes(user_ids)
        self.answer.refresh_from_db()
        self.assertEqual(self.answer.upvotes, 4)
        self.assertEqual(Vote.objects.filter(value=1).count(), 4)
        self.run_parallel_votes(user_ids)
        self.answer.refresh_from_db()
        self.assertEqual(self.answer.upvotes, 0)
        self.assertFalse(Vote.objects.exists())

    @skipUnlessDBFeature('has_select_for_update')
    def test_same_user_parallel_toggles_cancel_each_other(self):
        self.run_parallel_votes([self.owner.pk, self.owner.pk])
        self.answer.refresh_from_db()
        self.assertEqual(self.answer.upvotes, 0)
        self.assertFalse(Vote.objects.exists())
