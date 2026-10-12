from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from io import StringIO
from threading import Barrier
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import SESSION_KEY
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.management import call_command
from django.db import DatabaseError, OperationalError, close_old_connections, connections
from django.test import Client, RequestFactory, SimpleTestCase, TestCase, TransactionTestCase, override_settings, skipUnlessDBFeature
from django.urls import reverse
from django.utils import timezone

from .login_rate_limit import (
    bucket_key, check_login_proxy_rollout, check_login_rate_limit,
    client_network, consume_bucket,
)
from .models import LoginRateLimitBucket


@override_settings(LOGIN_CLIENT_IP_SOURCE='remote_addr', LOGIN_TRUST_CLOUDFLARE=False)
class ClientAddressTests(SimpleTestCase):
    def network(self, **meta):
        return client_network(RequestFactory().post('/login/', **meta))

    def test_direct_peer_ignores_all_spoofed_headers(self):
        self.assertEqual(self.network(
            REMOTE_ADDR='203.0.113.5', HTTP_X_REAL_IP='198.51.100.1',
            HTTP_X_FORWARDED_FOR='198.51.100.2', HTTP_CF_CONNECTING_IP='198.51.100.3',
        ), '203.0.113.5')

    @override_settings(LOGIN_CLIENT_IP_SOURCE='pythonanywhere')
    def test_pythonanywhere_uses_guaranteed_peer_not_forwarded_list(self):
        self.assertEqual(self.network(
            REMOTE_ADDR='10.0.0.1', HTTP_X_REAL_IP='203.0.113.5',
            HTTP_X_FORWARDED_FOR='198.51.100.1, 192.0.2.1',
        ), '203.0.113.5')
        with self.assertRaises(ValueError):
            self.network(REMOTE_ADDR='10.0.0.1')

    @override_settings(LOGIN_CLIENT_IP_SOURCE='pythonanywhere', LOGIN_TRUST_CLOUDFLARE=True)
    def test_cloudflare_header_requires_verified_edge_network(self):
        self.assertEqual(self.network(HTTP_X_REAL_IP='172.64.1.1', HTTP_CF_CONNECTING_IP='203.0.113.5'), '203.0.113.5')
        self.assertEqual(self.network(HTTP_X_REAL_IP='203.0.113.9', HTTP_CF_CONNECTING_IP='203.0.113.5'), '203.0.113.9')
        with self.assertRaises(ValueError):
            self.network(HTTP_X_REAL_IP='172.64.1.1')

    def test_unconfigured_cloudflare_does_not_group_all_users(self):
        with self.assertRaises(ValueError):
            self.network(REMOTE_ADDR='172.64.1.1')

    def test_invalid_addresses_and_scoped_ipv6_are_rejected(self):
        for address in ('', 'bad', '1.2.3.4, 5.6.7.8', 'fe80::1%eth0', '1.2.3.4:1234', None):
            with self.subTest(address=address), self.assertRaises(ValueError):
                self.network(REMOTE_ADDR=address)

    def test_ipv6_subnet_and_mapped_ipv4_have_stable_keys(self):
        self.assertEqual(self.network(REMOTE_ADDR='2001:db8:1::1'), self.network(REMOTE_ADDR='2001:db8:1::ffff'))
        self.assertEqual(self.network(REMOTE_ADDR='::ffff:203.0.113.1'), '203.0.113.1')
        self.assertNotEqual(self.network(REMOTE_ADDR='2001:db8:2::1'), self.network(REMOTE_ADDR='2001:db8:1::1'))

    @override_settings(IS_HOSTED=True, LOGIN_RATE_LIMIT_PROXY_VERIFIED=False)
    def test_deploy_check_requires_proxy_verification(self):
        self.assertEqual(check_login_proxy_rollout(None)[0].id, 'core.W010')
        with override_settings(LOGIN_RATE_LIMIT_PROXY_VERIFIED=True):
            self.assertEqual(check_login_proxy_rollout(None), [])

    def test_invalid_configuration_and_csrf_order_fail_checks(self):
        self.assertEqual(check_login_rate_limit(None), [])
        with override_settings(LOGIN_CLIENT_IP_SOURCE='forwarded-first', LOGIN_RATE_LIMIT_PER_IP=0):
            self.assertEqual({x.id for x in check_login_rate_limit(None)}, {'core.E010', 'core.E011'})
        with override_settings(MIDDLEWARE=list(reversed(settings.MIDDLEWARE))):
            self.assertIn('core.E012', {x.id for x in check_login_rate_limit(None)})


@override_settings(LOGIN_CLIENT_IP_SOURCE='remote_addr', LOGIN_TRUST_CLOUDFLARE=False,
                   LOGIN_RATE_LIMIT_PER_IP=6, LOGIN_RATE_LIMIT_PER_ACCOUNT_IP=3,
                   LOGIN_RATE_LIMIT_WINDOW_SECONDS=300)
class LoginRateLimitTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = 'Synthetic-auth-test-681!'
        cls.user = User.objects.create_user(username='limited-user', password=cls.password)

    def attempt(self, username='limited-user', ip='203.0.113.4', password='wrong', client=None, url=None, **extra):
        return (client or self.client).post(url or reverse('login'), {
            'username': username, 'password': password,
        }, REMOTE_ADDR=ip, **extra)

    def test_budget_shared_by_fresh_clients_and_cache_resets(self):
        for _ in range(3):
            self.assertEqual(self.attempt(client=Client()).status_code, 200)
            cache.clear()
        with patch('core.forms.LoginForm.is_valid', side_effect=AssertionError('Must not hash password')):
            response = self.attempt(client=Client(), password=self.password)
        self.assertEqual(response.status_code, 429)
        self.assertTrue(1 <= int(response['Retry-After']) <= 300)
        self.assertIn('no-store', response['Cache-Control'])
        self.assertNotIn(SESSION_KEY, self.client.session)
        self.assertNotContains(response, self.password, status_code=429)

    def test_ip_isolation_prevents_global_account_lockout(self):
        for _ in range(3):
            self.attempt()
        self.assertEqual(self.attempt(password=self.password, ip='203.0.113.99').status_code, 302)
        self.assertIn(SESSION_KEY, self.client.session)

    def test_new_usernames_are_bounded_by_ip_budget(self):
        for i in range(6):
            self.assertEqual(self.attempt(username=f'unknown-{i}').status_code, 200)
        self.assertEqual(LoginRateLimitBucket.objects.count(), 7)
        for i in range(6, 10):
            self.assertEqual(self.attempt(username=f'unknown-{i}').status_code, 429)
        self.assertEqual(LoginRateLimitBucket.objects.count(), 7)

    def test_unknown_and_known_accounts_have_same_limits(self):
        for username in ('limited-user', 'missing-user'):
            ip = '203.0.113.5' if username == 'limited-user' else '203.0.113.6'
            for _ in range(3):
                self.assertEqual(self.attempt(username=username, ip=ip).status_code, 200)
            self.assertEqual(self.attempt(username=username, ip=ip).status_code, 429)

    def test_case_and_nfkc_variations_do_not_get_new_budget(self):
        for username in ('limited-user', ' LIMITED-USER ', 'ｌｉｍｉｔｅｄ-user'):
            self.assertEqual(self.attempt(username=username).status_code, 200)
        self.assertEqual(self.attempt().status_code, 429)

    def test_blocked_requests_do_not_extend_wait_and_expiry_allows_login(self):
        start = timezone.now()
        with patch('core.login_rate_limit.timezone.now', return_value=start):
            for _ in range(3):
                self.attempt()
        with patch('core.login_rate_limit.timezone.now', return_value=start + timedelta(seconds=120)):
            self.assertEqual(self.attempt()['Retry-After'], '180')
        with patch('core.login_rate_limit.timezone.now', return_value=start + timedelta(seconds=300)):
            self.assertEqual(self.attempt(password=self.password).status_code, 302)

    def test_admin_and_public_login_share_the_same_budget(self):
        for _ in range(3):
            self.attempt(url=reverse('admin:login'))
        self.assertEqual(self.attempt().status_code, 429)
        self.assertEqual(self.attempt(url=reverse('admin:login')).status_code, 429)

    def test_successful_logins_do_not_reset_budget(self):
        for _ in range(3):
            self.assertEqual(self.attempt(password=self.password, client=Client()).status_code, 302)
        self.assertEqual(self.attempt().status_code, 429)

    def test_csrf_rejections_get_requests_and_logout_do_not_consume_budget(self):
        self.assertEqual(self.attempt(client=Client(enforce_csrf_checks=True)).status_code, 403)
        self.client.get(reverse('login'))
        self.client.get(reverse('admin:login'))
        self.client.post(reverse('logout'))
        self.assertEqual(LoginRateLimitBucket.objects.count(), 0)

    def test_db_failure_and_missing_ip_do_not_authenticate(self):
        with patch('core.login_rate_limit.consume_bucket', side_effect=OperationalError('synthetic failure')):
            self.assertEqual(self.attempt(password=self.password).status_code, 503)
        self.assertEqual(self.attempt(password=self.password, ip='').status_code, 503)
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_bucket_contains_only_digest_attempts_and_expiry(self):
        self.attempt()
        for bucket in LoginRateLimitBucket.objects.values():
            self.assertEqual(set(bucket), {'key', 'attempts', 'expires_at'})
            self.assertRegex(bucket['key'], r'^[0-9a-f]{64}$')
        self.assertNotEqual(bucket_key('ip', 'a'), bucket_key('account-ip', 'a'))
        with override_settings(SECRET_KEY='another-test-only-key'):
            changed = bucket_key('ip', 'a')
        self.assertNotEqual(changed, bucket_key('ip', 'a'))

    def test_cleanup_preserves_live_buckets_and_deletes_expired(self):
        now = timezone.now()
        consume_bucket('a' * 64, 1, now - timedelta(seconds=301))
        consume_bucket('b' * 64, 1, now)
        call_command('cleanup_login_rate_limits', stdout=StringIO())
        self.assertEqual(list(LoginRateLimitBucket.objects.values_list('pk', flat=True)), ['b' * 64])

    def test_cleanup_race_retries_without_allowing_an_uncounted_attempt(self):
        now = timezone.now()
        key = 'c' * 64
        queryset = LoginRateLimitBucket.objects.select_for_update()
        with patch.object(LoginRateLimitBucket.objects, 'select_for_update') as locked:
            locked.return_value.get.side_effect = [LoginRateLimitBucket.DoesNotExist(),
                                                   LoginRateLimitBucket(key=key, expires_at=now + timedelta(seconds=300))]
            self.assertEqual(consume_bucket(key, 1, now), 0)
        self.assertEqual(queryset.get(pk=key).attempts, 1)
        with patch.object(LoginRateLimitBucket.objects, 'select_for_update') as locked:
            locked.return_value.get.side_effect = LoginRateLimitBucket.DoesNotExist()
            with self.assertRaises(DatabaseError):
                consume_bucket(key, 1, now)
            self.assertEqual(locked.return_value.get.call_count, 3)


class LoginRateLimitConcurrencyTests(TransactionTestCase):
    @skipUnlessDBFeature('has_select_for_update')
    def test_parallel_workers_cannot_exceed_one_shared_budget(self):
        for state in ('absent', 'live', 'expired'):
            with self.subTest(state=state):
                LoginRateLimitBucket.objects.all().delete()
                now = timezone.now()
                key = 'f' * 64
                if state != 'absent':
                    LoginRateLimitBucket.objects.create(
                        key=key, attempts=3 if state == 'expired' else 0,
                        expires_at=now + timedelta(seconds=-1 if state == 'expired' else 300),
                    )
                barrier = Barrier(8)

                def worker(_):
                    close_old_connections()
                    try:
                        barrier.wait(timeout=10)
                        return consume_bucket(key, 3, now)
                    finally:
                        connections.close_all()

                with ThreadPoolExecutor(max_workers=8) as pool:
                    results = list(pool.map(worker, range(8)))
                self.assertEqual(results.count(0), 3)
                self.assertEqual(LoginRateLimitBucket.objects.get(pk=key).attempts, 3)
