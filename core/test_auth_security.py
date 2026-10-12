from django.contrib.auth import SESSION_KEY
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.sessions.models import Session
from django.test import Client, TestCase
from django.urls import reverse
from lxml import html


class AuthenticationSecurityTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = 'Local-test-password-4821'
        cls.user = User.objects.create_user(username='auth-security', password=cls.password)

    def login(self, **extra):
        data = {'username': self.user.username, 'password': self.password}
        data.update(extra.pop('data', {}))
        return self.client.post(reverse('login'), data, **extra)

    def test_logout_get_and_head_do_not_change_session(self):
        self.client.force_login(self.user)
        for method in ('get', 'head'):
            with self.subTest(method=method):
                response = getattr(self.client, method)(reverse('logout'))
                self.assertEqual(response.status_code, 405)
                self.assertEqual(self.client.session[SESSION_KEY], str(self.user.pk))

    def test_logout_requires_csrf_and_valid_post_works(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        response = client.post(reverse('logout'))
        self.assertEqual(response.status_code, 403)
        self.assertIn(SESSION_KEY, client.session)
        page = html.fromstring(client.get(reverse('user_homepage')).content)
        forms = page.xpath('//form[@action="/logout/"]')
        self.assertEqual(len(forms), 2)
        for form in forms:
            self.assertEqual(form.get('method').lower(), 'post')
            self.assertTrue(form.xpath('.//button[@type="submit"]'))
        token = forms[0].xpath('.//input[@name="csrfmiddlewaretoken"]/@value')[0]
        response = client.post(reverse('logout'), {'csrfmiddlewaretoken': token})
        self.assertRedirects(response, reverse('user_homepage'), fetch_redirect_response=False)
        self.assertNotIn(SESSION_KEY, client.session)
        self.assertFalse(page.xpath('//a[@href="/logout/"]'))

    def test_same_host_next_is_preserved_on_get_failure_and_success(self):
        target = '/kenarda/?page=2&sort=new#draft'
        response = self.client.get(reverse('login'), {'next': target})
        page = html.fromstring(response.content)
        self.assertEqual(page.xpath('//form[@id="login-form"]//input[@name="next"]/@value'), [target])
        response = self.login(data={'next': target, 'password': 'wrong', 'remember_me': 'on'})
        self.assertEqual(response.status_code, 200)
        page = html.fromstring(response.content)
        self.assertEqual(page.xpath('//input[@name="next"]/@value'), [target])
        self.assertTrue(page.xpath('//input[@name="remember_me"]/@checked'))
        self.assertNotIn(SESSION_KEY, self.client.session)
        response = self.login(data={'next': target})
        self.assertEqual(response['Location'], target)

    def test_unsafe_next_falls_back_to_home(self):
        targets = (
            'https://evil.example/', '//evil.example/', '///evil.example/',
            '/\\evil.example/', 'javascript:alert(1)', 'https:///evil.example/',
            'https://testserver@evil.example/', '\x01https://evil.example/',
        )
        for target in targets:
            with self.subTest(target=target):
                self.client.logout()
                response = self.login(data={'next': target})
                self.assertEqual(response['Location'], reverse('user_homepage'))

    def test_https_login_cannot_downgrade_redirect(self):
        response = self.login(data={'next': 'http://testserver/kenarda/'}, secure=True)
        self.assertEqual(response['Location'], reverse('user_homepage'))
        response = self.login(data={'next': 'https://testserver/kenarda/'}, secure=True)
        self.assertEqual(response['Location'], 'https://testserver/kenarda/')

    def test_post_target_takes_precedence_over_query_target(self):
        response = self.client.post(
            reverse('login') + '?next=/kenarda/',
            {'username': self.user.username, 'password': self.password, 'next': '//evil.example/'},
        )
        self.assertEqual(response['Location'], reverse('user_homepage'))

    def test_remember_me_only_changes_session_expiry(self):
        self.login()
        self.assertTrue(self.client.session.get_expire_at_browser_close())
        self.client.logout()
        self.login(data={'remember_me': 'on'})
        self.assertFalse(self.client.session.get_expire_at_browser_close())
        self.assertEqual(self.client.session.get_expiry_age(), 1209600)
        self.assertNotIn(self.password, str(dict(self.client.session)))

    def test_login_page_uses_password_manager_hints_not_local_storage(self):
        response = self.client.get(reverse('login'))
        page = html.fromstring(response.content)
        self.assertEqual(page.xpath('//input[@name="username"]/@autocomplete'), ['username'])
        self.assertEqual(page.xpath('//input[@name="password"]/@autocomplete'), ['current-password'])
        self.assertNotContains(response, "localStorage.setItem('savedPassword'")
        self.assertNotContains(response, "localStorage.getItem('savedPassword'")
        self.assertNotContains(response, 'passwordInput.value')

    def test_legacy_credential_cleanup_runs_on_public_and_authenticated_pages(self):
        for authenticated in (False, True):
            with self.subTest(authenticated=authenticated):
                if authenticated:
                    self.client.force_login(self.user)
                response = self.client.get(reverse('user_homepage'))
                self.assertContains(response, "removeItem('savedPassword')")
                self.assertContains(response, "removeItem('savedUsername')")
                page = html.fromstring(response.content)
                first_script = page.xpath('//script')[0]
                self.assertIn("removeItem('savedPassword')", first_script.text)

    def test_login_responses_are_not_cacheable(self):
        for response in (self.client.get(reverse('login')), self.login(data={'password': 'wrong'}), self.login()):
            self.assertIn('no-store', response.get('Cache-Control', ''))

    def test_login_post_still_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(reverse('login'), {'username': self.user.username, 'password': self.password})
        self.assertEqual(response.status_code, 403)
        self.assertNotIn(SESSION_KEY, client.session)

    def test_login_rotates_anonymous_session_without_losing_preferences(self):
        session = self.client.session
        session['auth_test_preference'] = 'keep'
        session.save()
        old_key = session.session_key
        self.login()
        self.assertNotEqual(self.client.session.session_key, old_key)
        self.assertFalse(Session.objects.filter(session_key=old_key).exists())
        self.assertEqual(self.client.session['auth_test_preference'], 'keep')

    def test_logout_invalidates_old_session_cookie(self):
        self.login()
        old_key = self.client.session.session_key
        response = self.client.post(reverse('logout'))
        self.assertIn('no-store', response['Cache-Control'])
        self.assertFalse(Session.objects.filter(session_key=old_key).exists())
        replay = Client()
        replay.cookies[settings.SESSION_COOKIE_NAME] = old_key
        response = replay.get(reverse('navbar_status'))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(SESSION_KEY, replay.session)

    def test_inactive_account_cannot_log_in(self):
        User.objects.filter(pk=self.user.pk).update(is_active=False)
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_login_rejects_other_methods(self):
        for method in ('put', 'patch', 'delete'):
            with self.subTest(method=method):
                response = getattr(self.client, method)(reverse('login'))
                self.assertEqual(response.status_code, 405)
                self.assertNotIn(SESSION_KEY, self.client.session)
