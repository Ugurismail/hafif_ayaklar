import json
import os
import subprocess
import sys

from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from .models import Question


class SitemapVisibilityTests(TestCase):
    def test_sitemap_contains_public_pages_and_profiles(self):
        user = User.objects.create_user(username="sitemap-user", password="test-pass")
        question = Question.objects.create(
            question_text="Sitemap test basligi",
            user=user,
        )

        response = self.client.get(
            "/sitemap.xml",
            secure=True,
            HTTP_HOST="hafifayaklar.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"https://hafifayaklar.com/{question.slug}/")
        self.assertContains(response, f"https://hafifayaklar.com{reverse('about')}")
        self.assertContains(response, reverse("user_profile", args=[user.username]))


class HttpsRedirectTests(SimpleTestCase):
    @override_settings(
        SECURE_SSL_REDIRECT=True,
        SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO", "https"),
    )
    def test_forwarded_http_request_redirects_to_https(self):
        response = self.client.get(
            "/robots.txt",
            HTTP_HOST="hafifayaklar.com",
            HTTP_X_FORWARDED_PROTO="http",
        )

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "https://hafifayaklar.com/robots.txt")

    @override_settings(
        SECURE_SSL_REDIRECT=True,
        SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO", "https"),
    )
    def test_forwarded_https_request_does_not_redirect(self):
        response = self.client.get(
            "/robots.txt",
            HTTP_HOST="hafifayaklar.com",
            HTTP_X_FORWARDED_PROTO="https",
        )

        self.assertEqual(response.status_code, 200)


class HostedSecuritySettingsTests(SimpleTestCase):
    def test_hosted_security_is_enabled_even_when_debug_is_true(self):
        environment = os.environ.copy()
        environment.update({
            "HOME": "/home/test-user",
            "DJANGO_DEBUG": "True",
            "DEBUG": "True",
        })
        code = """
import json
from hafifayaklar import settings
print(json.dumps({
    'csrf_cookie_secure': settings.CSRF_COOKIE_SECURE,
    'session_cookie_secure': settings.SESSION_COOKIE_SECURE,
    'ssl_redirect': settings.SECURE_SSL_REDIRECT,
    'hsts_seconds': settings.SECURE_HSTS_SECONDS,
    'proxy_header': settings.SECURE_PROXY_SSL_HEADER,
}))
"""

        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=str(os.path.dirname(os.path.dirname(__file__))),
            env=environment,
            check=True,
            capture_output=True,
            text=True,
        )
        hosted_settings = json.loads(result.stdout)

        self.assertTrue(hosted_settings["csrf_cookie_secure"])
        self.assertTrue(hosted_settings["session_cookie_secure"])
        self.assertTrue(hosted_settings["ssl_redirect"])
        self.assertEqual(hosted_settings["hsts_seconds"], 31536000)
        self.assertEqual(
            hosted_settings["proxy_header"],
            ["HTTP_X_FORWARDED_PROTO", "https"],
        )


class PublicAuthorSeoTests(TestCase):
    def setUp(self):
        from .models import Answer
        self.author = User.objects.create_user(
            username='Uğur İsmail', email='private@example.com', password='test-pass',
        )
        self.author.userprofile.bio = 'PRIVATE BIO'
        self.author.userprofile.save()
        self.question = Question.objects.create(question_text='Yazarın başlığı', user=self.author)
        self.answer = Answer.objects.create(
            question=self.question, user=self.author, answer_text='Herkese açık yazı',
        )
        self.url = reverse('public_author', args=[self.author.pk])

    def test_public_author_is_crawlable_and_does_not_expose_private_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1>Uğur İsmail</h1>')
        self.assertContains(response, 'Herkese açık yazı')
        self.assertNotContains(response, 'private@example.com')
        self.assertNotContains(response, 'PRIVATE BIO')
        import re
        data = json.loads(re.search(
            r'<script type="application/ld\+json">(.*?)</script>', response.content.decode(), re.S,
        ).group(1))
        self.assertEqual(data['mainEntity']['name'], self.author.username)
        self.assertTrue(data['mainEntity']['url'].endswith(self.url))
        self.assertEqual(self.client.get(reverse('user_profile', args=[self.author.username])).status_code, 200)

    def test_author_sitemap_and_stable_url_after_rename(self):
        response = self.client.get('/sitemap.xml')
        self.assertContains(response, self.url)
        self.author.username = 'Uğur İsmail Cemil'
        self.author.save()
        self.assertContains(self.client.get(self.url), '<h1>Uğur İsmail Cemil</h1>')

    def test_inactive_author_is_not_published(self):
        self.author.is_active = False
        self.author.save()
        self.assertEqual(self.client.get(self.url).status_code, 404)
        self.assertNotContains(self.client.get('/sitemap.xml'), self.url)

    def test_entry_title_and_structured_author(self):
        import re
        response = self.client.get(reverse('single_answer', args=[self.question.slug, self.answer.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<title>Uğur İsmail — Yazarın başlığı | Hafif Ayaklar</title>')
        data = json.loads(re.search(
            r'<script type="application/ld\+json">(.*?)</script>', response.content.decode(), re.S,
        ).group(1))
        self.assertEqual(data['author']['name'], self.author.username)
        self.assertTrue(data['author']['url'].endswith(self.url))

    def test_question_schema_uses_real_author_and_public_url(self):
        import re
        response = self.client.get(reverse('question_detail', args=[self.question.slug]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(re.search(
            r'<script type="application/ld\+json">(.*?)</script>', response.content.decode(), re.S,
        ).group(1))
        self.assertEqual(data['mainEntity']['author']['name'], self.author.username)
        self.assertEqual(data['mainEntity']['acceptedAnswer']['author']['name'], self.author.username)
        self.assertTrue(data['mainEntity']['author']['url'].endswith(self.url))

    def test_pagination_preserves_discoverability_and_escapes_names(self):
        from .models import Answer
        for i in range(20):
            Answer.objects.create(user=self.author, question=self.question, answer_text=f'Entry {i}')
        self.assertContains(self.client.get(self.url), 'rel="next"')
        response = self.client.get(self.url, {'page': 2})
        self.assertContains(response, f'{self.url}?page=2')
        self.assertContains(response, 'Herkese açık yazı')
        self.author.username = '</script><script>alert(1)</script>'
        self.author.save()
        response = self.client.get(self.url)
        self.assertNotContains(response, '<script>alert(1)</script>')


    def test_public_profile_and_private_tabs(self):
        from .models import Invitation
        invitation = Invitation.objects.create(sender=self.author)
        url = reverse('user_profile', args=[self.author.username])
        response = self.client.get(url)
        self.assertContains(response, '<h1 class="h4 card-title mb-3">Uğur İsmail</h1>')
        self.assertContains(response, 'Herkese açık yazı')
        self.assertNotContains(response, self.author.email)
        self.assertNotContains(response, str(invitation.code))
        for tab in ['kaydedilenler', 'davetler', 'davet_aagac']:
            self.assertEqual(self.client.get(url, {'tab': tab}).status_code, 403)
        self.assertEqual(self.client.post(url, {'tab': 'davetler'}).status_code, 403)
        for tab in ['revizyonlar', 'tanimlar', 'kaynaklarim', 'kelimeler', 'istatistikler']:
            self.assertEqual(self.client.get(url, {'tab': tab}).status_code, 200)
        self.client.force_login(self.author)
        self.assertContains(self.client.get(url, {'tab': 'davetler'}), str(invitation.code))
        self.assertEqual(self.client.get(url, {'tab': 'kaydedilenler'}).status_code, 200)

    def test_drafts_remain_owner_only_after_profiles_become_public(self):
        from .models import Kenarda
        draft = Kenarda.objects.create(
            user=self.author, question=self.question,
            content='PRIVATE-DRAFT-ONLY-OWNER-9371',
        )
        outsider = User.objects.create_user(username='other-reader', password='test-pass')
        public_urls = [
            self.url,
            reverse('user_profile', args=[self.author.username]),
            reverse('question_detail', args=[self.question.slug]),
            reverse('single_answer', args=[self.question.slug, self.answer.pk]),
        ]
        for logged_in in [False, True]:
            if logged_in:
                self.client.force_login(outsider)
            for url in public_urls:
                response = self.client.get(url, {'draft_id': draft.pk})
                self.assertEqual(response.status_code, 200)
                self.assertNotContains(response, draft.content)
            response = self.client.get(reverse('kenarda_list'))
            if logged_in:
                self.assertNotContains(response, draft.content)
            else:
                self.assertEqual(response.status_code, 302)
            for action in ['kenarda_sil', 'kenarda_gonder']:
                response = self.client.post(reverse(action, args=[draft.pk]))
                if logged_in:
                    if action == 'kenarda_gonder':
                        self.assertEqual(response.status_code, 404)
                    else:
                        self.assertEqual(response.json()['status'], 'fail')
                else:
                    self.assertEqual(response.status_code, 302)
                self.assertTrue(Kenarda.objects.filter(pk=draft.pk).exists())
        self.client.force_login(self.author)
        self.assertContains(self.client.get(reverse('kenarda_list')), draft.content)
