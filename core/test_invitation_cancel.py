from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest.mock import patch
from uuid import uuid4

from django.contrib.auth.models import User
from django.db import close_old_connections, connections
from django.test import Client, TestCase, TransactionTestCase, skipUnlessDBFeature
from django.urls import reverse
from lxml import html

from core.invitations import MAX_INVITATION_GRANT, cancel_invitation, issue_invitation, transfer_invitation_quota
from core.models import Invitation, UserProfile


class InvitationCancelTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='cancel-owner')
        self.other = User.objects.create_user(username='Alıcı & kullanıcı')
        UserProfile.objects.filter(user=self.owner).update(invitation_quota=5)
        self.invitation = issue_invitation(self.owner, 3)
        self.url = reverse('invitation_cancel', args=[self.invitation.code])
        self.profile_url = reverse('user_profile', args=[self.owner.username]) + '?tab=davetler'
        self.client.force_login(self.owner)

    def balance(self):
        return UserProfile.objects.get(user=self.owner).invitation_quota

    def test_confirmation_is_read_only_and_refund_happens_once(self):
        self.assertContains(self.client.get(self.url), '3 davet hakkı')
        self.assertEqual(self.balance(), 2)
        for _ in range(2):
            self.assertRedirects(self.client.post(self.url), self.profile_url)
            self.assertEqual(self.balance(), 5)
        self.invitation.refresh_from_db()
        self.assertIsNotNone(self.invitation.cancelled_at)
        self.assertFalse(self.invitation.is_used)
        self.assertEqual(Invitation.objects.count(), 1)

    def test_cancelled_code_cannot_register_an_account(self):
        self.client.post(self.url)
        response = self.client.post(reverse('signup'), {
            'username': 'must-not-exist', 'password': 'test-only-password',
            'invitation_code': str(self.invitation.code),
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='must-not-exist').exists())
        self.assertEqual(self.balance(), 5)

    def test_used_or_inconsistent_invitation_is_never_refunded(self):
        for used in [True, False]:
            Invitation.objects.filter(pk=self.invitation.pk).update(is_used=used, used_by=self.other)
            self.assertEqual(self.client.post(self.url).status_code, 400)
            self.assertEqual(self.balance(), 2)
            self.invitation.refresh_from_db()
            self.assertIsNone(self.invitation.cancelled_at)

    def test_used_code_after_account_deleted_cannot_be_cancelled(self):
        Invitation.objects.filter(pk=self.invitation.pk).update(is_used=True, used_by=None)
        self.assertEqual(self.client.post(self.url).status_code, 400)
        self.assertEqual(self.balance(), 2)

    def test_ownership_login_and_csrf_are_required(self):
        self.client.force_login(self.other)
        for method in ['get', 'post']:
            self.assertEqual(getattr(self.client, method)(self.url).status_code, 404)
        self.assertEqual(Client().post(self.url).status_code, 302)
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.owner)
        self.assertEqual(csrf_client.post(self.url).status_code, 403)
        self.assertEqual(self.balance(), 2)
        self.client.force_login(self.owner)
        self.assertEqual(self.client.put(self.url).status_code, 405)

    def test_refund_rolls_back_if_cancellation_write_fails(self):
        with patch.object(Invitation, 'save', side_effect=RuntimeError('test failure')):
            with self.assertRaises(RuntimeError):
                cancel_invitation(self.owner, self.invitation.code)
        self.assertEqual(self.balance(), 2)
        self.invitation.refresh_from_db()
        self.assertIsNone(self.invitation.cancelled_at)

    def test_refund_cannot_overflow_balance(self):
        UserProfile.objects.filter(user=self.owner).update(invitation_quota=MAX_INVITATION_GRANT)
        self.assertEqual(self.client.post(self.url).status_code, 400)
        self.assertEqual(self.balance(), MAX_INVITATION_GRANT)
        self.invitation.refresh_from_db()
        self.assertIsNone(self.invitation.cancelled_at)

    def test_legacy_zero_grant_can_be_cancelled_without_creating_quota(self):
        legacy = Invitation.objects.create(sender=self.owner, quota_granted=0)
        cancel_invitation(self.owner, legacy.code)
        self.assertEqual(self.balance(), 2)

    def test_inline_actions_are_only_shown_for_eligible_invitations(self):
        Invitation.objects.create(sender=self.owner, is_used=True, used_by=self.other)
        response = self.client.get(self.profile_url)
        self.assertNotContains(response, 'Davet hakkı aktar')
        page = html.fromstring(response.content)
        plus = page.xpath('//a[@title="Ek davet"]')
        self.assertEqual(len(plus), 1)
        self.assertEqual(len(plus[0].xpath('.//i[contains(@class,"bi-plus-lg")]')), 1)
        self.assertIn(self.other.username, plus[0].getparent().text_content())
        transfer_page = self.client.get(plus[0].get('href'))
        form = transfer_page.context['form']
        self.assertEqual(form.initial['username'], self.other.username)
        self.assertEqual(html.fromstring(transfer_page.content).xpath('//input[@name="username"]/@value'),
                         [self.other.username])
        self.assertEqual(len(page.xpath('//a[@title="Daveti iptal et"]')), 1)
        cancel_invitation(self.owner, self.invitation.code)
        response = self.client.get(self.profile_url)
        self.assertContains(response, 'İptal edildi')
        self.assertNotContains(response, 'title="Daveti iptal et"')
        self.other.is_active = False
        self.other.save(update_fields=['is_active'])
        self.assertNotContains(self.client.get(self.profile_url), 'title="Ek davet"')


class ConcurrentInvitationCancelTests(TransactionTestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='cancel-race-owner')
        self.recipient = User.objects.create_user(username='cancel-race-recipient')
        UserProfile.objects.filter(user=self.owner).update(invitation_quota=5)
        self.invitation = issue_invitation(self.owner, 3)

    def parallel(self, *actions):
        barrier = Barrier(len(actions))

        def run(action):
            close_old_connections()
            try:
                barrier.wait(timeout=15)
                return action()
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=len(actions)) as pool:
            return list(pool.map(run, actions))

    @skipUnlessDBFeature('has_select_for_update')
    def test_parallel_cancellations_refund_once(self):
        def cancel():
            return cancel_invitation(self.owner, self.invitation.code)[1]
        self.assertEqual(sorted(self.parallel(cancel, cancel)), [False, True])
        self.assertEqual(UserProfile.objects.get(user=self.owner).invitation_quota, 5)

    @skipUnlessDBFeature('has_select_for_update')
    def test_registration_and_cancellation_cannot_both_win(self):
        def cancel():
            try:
                return cancel_invitation(self.owner, self.invitation.code)[1]
            except ValueError:
                return False

        def register():
            return Client().post(reverse('signup'), {
                'username': 'cancel-race-new', 'password': 'test-only-password',
                'invitation_code': str(self.invitation.code),
            }).status_code

        cancelled, status = self.parallel(cancel, register)
        self.invitation.refresh_from_db()
        self.assertNotEqual(self.invitation.is_used, self.invitation.cancelled_at is not None)
        self.assertEqual(status, 200 if cancelled else 302)
        self.assertEqual(User.objects.filter(username='cancel-race-new').exists(), not cancelled)
        self.assertEqual(UserProfile.objects.get(user=self.owner).invitation_quota, 5 if cancelled else 2)

    @skipUnlessDBFeature('has_select_for_update')
    def test_refund_and_transfer_preserve_both_balance_changes(self):
        self.parallel(
            lambda: cancel_invitation(self.owner, self.invitation.code),
            lambda: transfer_invitation_quota(self.owner, self.recipient, 2, uuid4()),
        )
        self.assertEqual(UserProfile.objects.get(user=self.owner).invitation_quota, 3)
        self.assertEqual(UserProfile.objects.get(user=self.recipient).invitation_quota, 2)
