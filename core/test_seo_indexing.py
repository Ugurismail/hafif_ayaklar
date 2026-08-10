import json
import os
import subprocess
import sys

from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from .models import Question


class SitemapVisibilityTests(TestCase):
    def test_sitemap_contains_public_pages_but_not_login_only_profiles(self):
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
        self.assertNotContains(response, "/profile/")


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
