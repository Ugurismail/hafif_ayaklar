from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest.mock import patch
from uuid import uuid4

from django.contrib.auth.models import AnonymousUser, User
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.db import close_old_connections, connections
from django.http import HttpResponse
from django.test import Client, RequestFactory, TestCase, TransactionTestCase, skipUnlessDBFeature

from core.forms import InvitationForm, SignupForm
from core.models import Invitation, UserProfile
from core.views.auth_views import send_invitation, signup
from core.views.user_views import user_profile


class InvitationSecurityTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(username='invite-owner', password='pass')
        cls.other = User.objects.create_user(username='invite-other', password='pass')

    def setUp(self):
        self.client.force_login(self.owner)
        self.urls = ['/send-invitation/', '/profile/invite-owner/?tab=davetler']
        self.set_quota(3)

    def set_quota(self, value):
        UserProfile.objects.filter(user=self.owner).update(invitation_quota=value)

    def test_both_creation_routes_debit_exactly_the_granted_quota(self):
        for url in self.urls:
            with self.subTest(url=url):
                self.set_quota(3)
                count = Invitation.objects.count()
                response = self.client.post(url, {'quota_granted': 2})
                self.assertIn(response.status_code, (200, 302))
                self.assertEqual(Invitation.objects.count(), count + 1)
                invitation = Invitation.objects.latest('pk')
                self.assertEqual((invitation.sender_id, invitation.quota_granted), (self.owner.pk, 2))
                self.assertEqual(UserProfile.objects.get(user=self.owner).invitation_quota, 1)

    def test_stale_quota_cannot_create_an_extra_code(self):
        original = InvitationForm.is_valid

        def drain_after_validation(form):
            valid = original(form)
            self.set_quota(0)
            return valid

        for url in self.urls:
            with self.subTest(url=url):
                self.set_quota(1)
                count = Invitation.objects.count()
                with patch.object(InvitationForm, 'is_valid', drain_after_validation):
                    response = self.client.post(url, {'quota_granted': 1})
                self.assertIn(response.status_code, (200, 302))
                self.assertEqual(Invitation.objects.count(), count)
                self.assertEqual(UserProfile.objects.get(user=self.owner).invitation_quota, 0)

    def test_invitation_creation_does_not_overwrite_concurrent_profile_changes(self):
        original = InvitationForm.is_valid

        def change_after_validation(form):
            valid = original(form)
            UserProfile.objects.filter(user=self.owner).update(font_size=31)
            return valid

        for url in self.urls:
            with self.subTest(url=url):
                self.set_quota(2)
                UserProfile.objects.filter(user=self.owner).update(font_size=18)
                with patch.object(InvitationForm, 'is_valid', change_after_validation):
                    self.client.post(url, {'quota_granted': 1})
                self.assertEqual(UserProfile.objects.get(user=self.owner).font_size, 31)

    def test_remaining_quota_is_not_subtracted_twice(self):
        self.set_quota(2)
        Invitation.objects.bulk_create([
            Invitation(sender=self.owner, quota_granted=1) for _ in range(3)
        ])
        response = self.client.get(self.urls[1])
        self.assertEqual(response.context['remaining_invitations'], 2)

    def test_other_profile_writes_cannot_restore_spent_quota(self):
        original = UserProfile.save

        def spend_before_save(profile, *args, **kwargs):
            if profile.user_id == self.owner.pk:
                self.set_quota(0)
            return original(profile, *args, **kwargs)

        for url, data in [('/settings/', {'font_size': 23}),
                          ('/settings/', {'reset': '1'}),
                          ('/profile/update_photo/', {'remove_photo': 'true'}),
                          ('/profile/update_photo/', {})]:
            with self.subTest(url=url, data=data):
                self.set_quota(3)
                with patch.object(UserProfile, 'save', spend_before_save):
                    response = self.client.post(url, data)
                self.assertEqual(response.status_code, 302)
                profile = UserProfile.objects.get(user=self.owner)
                self.assertEqual(profile.invitation_quota, 0)
                if 'font_size' in data:
                    self.assertEqual(profile.font_size, 23)
                if 'reset' in data:
                    self.assertEqual(profile.font_size, 18)

        self.set_quota(3)
        with patch.object(UserProfile, 'save', spend_before_save):
            response = self.client.get('/profile/invite-owner/?tab=kelimeler&exclude_word=example')
        self.assertEqual(response.status_code, 200)
        profile = UserProfile.objects.get(user=self.owner)
        self.assertEqual(profile.invitation_quota, 0)
        self.assertEqual(profile.excluded_words, 'example')

    def test_invalid_and_insufficient_grants_create_nothing(self):
        for url in self.urls:
            for value in ('0', '-1', '1.5', 'true', '', '2147483648', '999999999999999999999', '4'):
                with self.subTest(url=url, value=value):
                    response = self.client.post(url, {'quota_granted': value})
                    self.assertIn(response.status_code, (200, 302))
                    self.assertFalse(Invitation.objects.exists())
                    self.assertEqual(UserProfile.objects.get(user=self.owner).invitation_quota, 3)

    def test_failed_code_insert_rolls_back_quota(self):
        for url in self.urls:
            with self.subTest(url=url):
                with patch.object(Invitation, 'save', side_effect=RuntimeError('test insert failure')):
                    with self.assertRaises(RuntimeError):
                        self.client.post(url, {'quota_granted': 2})
                self.assertEqual(UserProfile.objects.get(user=self.owner).invitation_quota, 3)
                self.assertFalse(Invitation.objects.exists())

    def test_foreign_profile_guests_get_and_csrf_do_not_create_codes(self):
        self.assertEqual(self.client.post('/profile/invite-other/?tab=davetler',
                                         {'quota_granted': 1}).status_code, 403)
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.owner)
        for url in self.urls:
            self.assertEqual(csrf_client.post(url, {'quota_granted': 1}).status_code, 403)
            self.assertEqual(self.client.get(url).status_code, 200)
            self.assertIn(Client().post(url, {'quota_granted': 1}).status_code, (302, 403))
        self.assertFalse(Invitation.objects.exists())

    def test_signup_consumes_code_once_and_transfers_grant(self):
        invitation = Invitation.objects.create(sender=self.owner, quota_granted=2)
        response = self.client.post('/signup/', {
            'username': 'new-member', 'password': 'test-password', 'invitation_code': str(invitation.code),
        })
        self.assertEqual(response.status_code, 302)
        member = User.objects.get(username='new-member')
        invitation.refresh_from_db()
        self.assertTrue(invitation.is_used)
        self.assertEqual(invitation.used_by_id, member.pk)
        self.assertEqual(member.userprofile.invitation_quota, 2)
        response = self.client.post('/signup/', {
            'username': 'second-member', 'password': 'test-password', 'invitation_code': str(invitation.code),
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='second-member').exists())

    def test_invalid_or_missing_signup_code_creates_no_user(self):
        for code in ('not-a-uuid', str(uuid4()), ''):
            response = self.client.post('/signup/', {
                'username': 'not-created', 'password': 'test-password', 'invitation_code': code,
            })
            self.assertEqual(response.status_code, 200)
            self.assertFalse(User.objects.filter(username='not-created').exists())

    def test_failed_signup_rolls_back_user_and_code(self):
        invitation = Invitation.objects.create(sender=self.owner, quota_granted=2)
        original = SignupForm.save

        def fail_after_user(form):
            original(form)
            raise RuntimeError('test signup failure')

        with patch.object(SignupForm, 'save', fail_after_user), self.assertRaises(RuntimeError):
            self.client.post('/signup/', {
                'username': 'rolled-back', 'password': 'test-password', 'invitation_code': str(invitation.code),
            })
        invitation.refresh_from_db()
        self.assertFalse(invitation.is_used)
        self.assertIsNone(invitation.used_by_id)
        self.assertFalse(User.objects.filter(username='rolled-back').exists())


class ConcurrentInvitationTests(TransactionTestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='parallel-inviter')

    def run_parallel(self, actions, form_class):
        barrier = Barrier(len(actions))
        original = form_class.is_valid

        def synchronized_validation(form):
            valid = original(form)
            barrier.wait(timeout=15)
            return valid

        def call(action):
            close_old_connections()
            try:
                return action()
            finally:
                connections.close_all()

        with patch.object(form_class, 'is_valid', synchronized_validation):
            with ThreadPoolExecutor(max_workers=len(actions)) as executor:
                return list(executor.map(call, actions))

    def request(self, url, data, authenticated=True):
        request = RequestFactory().post(url, data)
        request.user = User.objects.get(pk=self.owner.pk) if authenticated else AnonymousUser()
        SessionMiddleware(lambda r: HttpResponse()).process_request(request)
        MessageMiddleware(lambda r: HttpResponse()).process_request(request)
        return request

    def issue(self, profile=False, grant=1):
        request = self.request('/profile/parallel-inviter/?tab=davetler' if profile
                               else '/send-invitation/', {'quota_granted': grant})
        response = user_profile(request, 'parallel-inviter') if profile else send_invitation(request)
        return response.status_code

    @skipUnlessDBFeature('has_select_for_update')
    def test_both_routes_compete_for_last_quota(self):
        UserProfile.objects.filter(user=self.owner).update(invitation_quota=1)
        statuses = self.run_parallel([lambda: self.issue(), lambda: self.issue(True)], InvitationForm)
        self.assertEqual(statuses, [200, 302])
        self.assertEqual(Invitation.objects.count(), 1)
        self.assertEqual(UserProfile.objects.get(user=self.owner).invitation_quota, 0)

    @skipUnlessDBFeature('has_select_for_update')
    def test_parallel_grants_preserve_quota_balance(self):
        UserProfile.objects.filter(user=self.owner).update(invitation_quota=5)
        self.run_parallel([lambda: self.issue(grant=2), lambda: self.issue(True, 2),
                           lambda: self.issue(grant=2)], InvitationForm)
        self.assertEqual(Invitation.objects.count(), 2)
        self.assertEqual(UserProfile.objects.get(user=self.owner).invitation_quota, 1)

    @skipUnlessDBFeature('has_select_for_update')
    def test_same_code_cannot_register_two_accounts(self):
        invitation = Invitation.objects.create(sender=self.owner, quota_granted=3)

        def register(username):
            request = self.request('/signup/', {
                'username': username, 'password': 'test-password', 'invitation_code': str(invitation.code),
            }, authenticated=False)
            return signup(request).status_code

        statuses = self.run_parallel([lambda: register('parallel-a'), lambda: register('parallel-b')], SignupForm)
        self.assertEqual(sorted(statuses), [200, 302])
        members = User.objects.filter(username__in=['parallel-a', 'parallel-b'])
        self.assertEqual(members.count(), 1)
        invitation.refresh_from_db()
        self.assertEqual(invitation.used_by_id, members.get().pk)
        self.assertTrue(invitation.is_used)
        self.assertEqual(members.get().userprofile.invitation_quota, 3)
