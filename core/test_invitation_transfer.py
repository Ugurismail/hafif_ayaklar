from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest.mock import patch
from uuid import uuid4

from django.contrib.auth.models import User
from django.db import close_old_connections, connections
from django.test import Client, TestCase, TransactionTestCase, skipUnlessDBFeature
from django.urls import reverse

from core.invitations import MAX_INVITATION_GRANT, issue_invitation, transfer_invitation_quota
from core.models import Invitation, InvitationTransfer, Notification, UserProfile


class InvitationTransferTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='transfer-sender')
        self.recipient = User.objects.create_user(username='transfer-recipient')
        UserProfile.objects.filter(user=self.sender).update(invitation_quota=5)
        self.client.force_login(self.sender)
        self.url = reverse('invitation_transfer')

    def payload(self, **changes):
        form = self.client.get(self.url).context['form']
        return {'username': self.recipient.username, 'amount': 2, 'token': form.initial['token'], **changes}

    def balances(self):
        return tuple(UserProfile.objects.get(user=u).invitation_quota for u in [self.sender, self.recipient])

    def test_transfer_debits_credits_records_and_notifies_once_on_replay(self):
        data = self.payload()
        for _ in range(2):
            self.assertRedirects(self.client.post(self.url, data), self.url)
        self.assertEqual(self.balances(), (3, 2))
        self.assertEqual(InvitationTransfer.objects.count(), 1)
        notice = Notification.objects.get(recipient=self.recipient)
        self.assertIn('2 davet hakkı', notice.message)
        self.assertFalse(notice.is_read)

    def test_cannot_change_a_completed_transfer(self):
        data = self.payload()
        self.client.post(self.url, data)
        response = self.client.post(self.url, {**data, 'amount': 1})
        self.assertContains(response, 'farklı bilgilerle')
        self.assertEqual(self.balances(), (3, 2))

    def test_invalid_amount_self_unknown_and_inactive_recipient(self):
        for amount in ['0', '-1', '1.5', '6', str(MAX_INVITATION_GRANT + 1), '']:
            self.assertEqual(self.client.post(self.url, self.payload(amount=amount)).status_code, 200)
        for username in [self.sender.username, 'missing-user']:
            self.assertEqual(self.client.post(self.url, self.payload(username=username)).status_code, 200)
        self.recipient.is_active = False
        self.recipient.save(update_fields=['is_active'])
        self.client.post(self.url, self.payload())
        self.assertEqual(self.balances(), (5, 0))
        self.assertFalse(InvitationTransfer.objects.exists())

    def test_overflow_rolls_back_and_backend_rejects_non_integer(self):
        UserProfile.objects.filter(user=self.recipient).update(invitation_quota=MAX_INVITATION_GRANT)
        self.client.post(self.url, self.payload())
        for amount in [True, 1.5, 0, -1]:
            with self.assertRaises(ValueError):
                transfer_invitation_quota(self.sender, self.recipient, amount, uuid4())
        self.assertEqual(self.balances(), (5, MAX_INVITATION_GRANT))

    def test_notification_failure_rolls_back_both_balances_and_history(self):
        with patch.object(Notification.objects, 'create', side_effect=RuntimeError('test')):
            with self.assertRaises(RuntimeError):
                self.client.post(self.url, self.payload())
        self.assertEqual(self.balances(), (5, 0))
        self.assertFalse(InvitationTransfer.objects.exists())

    def test_token_tampering_expiry_and_another_user_are_rejected(self):
        data = self.payload()
        self.client.post(self.url, {**data, 'token': data['token'] + 'broken'})
        with patch('django.core.signing.time.time', return_value=9999999999):
            self.client.post(self.url, data)
        self.client.force_login(self.recipient)
        self.client.post(self.url, {**data, 'username': self.sender.username})
        self.assertEqual(self.balances(), (5, 0))
        self.assertFalse(InvitationTransfer.objects.exists())

    def test_guest_csrf_get_and_foreign_history(self):
        self.assertEqual(Client().get(self.url).status_code, 302)
        csrf = Client(enforce_csrf_checks=True)
        csrf.force_login(self.sender)
        self.assertEqual(csrf.post(self.url, self.payload()).status_code, 403)
        self.assertEqual(self.client.put(self.url).status_code, 405)
        response = self.client.get(self.url, {'amount': 5, 'username': self.recipient.username})
        self.assertIn('no-store', response['Cache-Control'])
        self.assertEqual(self.balances(), (5, 0))
        self.client.post(self.url, self.payload())
        third = User.objects.create_user(username='third-member')
        self.client.force_login(third)
        self.assertEqual(len(self.client.get(self.url).context['transfers']), 0)


class InvitationTransferConcurrencyTests(TransactionTestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender')
        self.recipient = User.objects.create_user(username='recipient')
        UserProfile.objects.filter(user=self.sender).update(invitation_quota=5)

    def parallel(self, actions):
        barrier = Barrier(len(actions))
        def run(action):
            close_old_connections()
            try:
                barrier.wait(timeout=10)
                try:
                    return action()
                except ValueError:
                    return None
            finally:
                connections.close_all()
        with ThreadPoolExecutor(max_workers=len(actions)) as pool:
            return list(pool.map(run, actions))

    @skipUnlessDBFeature('has_select_for_update')
    def test_last_rights_cannot_be_transferred_twice(self):
        self.parallel([lambda: transfer_invitation_quota(self.sender, self.recipient, 4, uuid4())] * 2)
        self.assertEqual(InvitationTransfer.objects.count(), 1)
        self.assertEqual(UserProfile.objects.get(user=self.sender).invitation_quota, 1)
        self.assertEqual(UserProfile.objects.get(user=self.recipient).invitation_quota, 4)

    @skipUnlessDBFeature('has_select_for_update')
    def test_same_token_parallel_replay(self):
        token = uuid4()
        self.parallel([lambda: transfer_invitation_quota(self.sender, self.recipient, 2, token)] * 2)
        self.assertEqual(InvitationTransfer.objects.count(), 1)
        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(UserProfile.objects.get(user=self.sender).invitation_quota, 3)

    @skipUnlessDBFeature('has_select_for_update')
    def test_transfer_competes_with_invitation_creation(self):
        self.parallel([lambda: transfer_invitation_quota(self.sender, self.recipient, 4, uuid4()),
                       lambda: issue_invitation(self.sender, 4)])
        self.assertEqual(InvitationTransfer.objects.count() + Invitation.objects.count(), 1)
        self.assertEqual(UserProfile.objects.get(user=self.sender).invitation_quota, 1)

    @skipUnlessDBFeature('has_select_for_update')
    def test_opposite_transfers_do_not_deadlock(self):
        UserProfile.objects.filter(user=self.recipient).update(invitation_quota=5)
        self.parallel([lambda: transfer_invitation_quota(self.sender, self.recipient, 2, uuid4()),
                       lambda: transfer_invitation_quota(self.recipient, self.sender, 3, uuid4())])
        self.assertEqual(InvitationTransfer.objects.count(), 2)
        self.assertEqual(UserProfile.objects.get(user=self.sender).invitation_quota, 6)
        self.assertEqual(UserProfile.objects.get(user=self.recipient).invitation_quota, 4)
