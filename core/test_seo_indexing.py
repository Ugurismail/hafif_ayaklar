import json
import os
import subprocess
import sys
import re
from unittest.mock import patch
from xml.etree import ElementTree

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


class EntrySitemapTests(TestCase):
    def setUp(self):
        from .models import Answer
        self.author = User.objects.create_user(username='entry-author')
        self.question = Question.objects.create(question_text='Entry sitemap', user=self.author)
        self.entries = [Answer.objects.create(
            user=self.author, question=self.question, answer_text=f'Public entry {i}',
        ) for i in range(3)]

    @patch('core.sitemaps.EntrySitemap.limit', 2)
    def test_index_discovers_every_page_without_duplicate_entries(self):
        index = self.client.get('/sitemap-entries.xml', secure=True)
        self.assertEqual(index.status_code, 200)
        namespace = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        locations = [node.text for node in ElementTree.fromstring(index.content).findall('.//s:loc', namespace)]
        self.assertEqual(len(locations), 2)
        self.assertTrue(locations[1].endswith('?p=2'))
        entry_locations = []
        for location in locations:
            response = self.client.get(location, secure=True)
            self.assertEqual(response.status_code, 200)
            entry_locations.extend(node.text for node in ElementTree.fromstring(response.content).findall('.//s:loc', namespace))
        self.assertEqual(entry_locations, [
            'https://testserver' + reverse('single_answer', args=[self.question.slug, entry.pk])
            for entry in self.entries
        ])
        self.assertContains(self.client.get('/robots.txt'), '/sitemap-entries.xml')

    def test_sitemap_excludes_inactive_authors_and_drafts(self):
        from .models import Kenarda
        Kenarda.objects.create(user=self.author, question=self.question, content='PRIVATE-DRAFT')
        response = self.client.get('/sitemap-entries-entries.xml')
        self.assertNotContains(response, 'PRIVATE-DRAFT')
        self.assertNotContains(response, '/kenarda/')
        self.author.is_active = False
        self.author.save()
        response = self.client.get('/sitemap-entries-entries.xml')
        for entry in self.entries:
            self.assertNotContains(response, reverse('single_answer', args=[self.question.slug, entry.pk]))

    def test_sitemap_metadata_has_no_per_entry_queries_or_body_fetch(self):
        from .sitemaps import EntrySitemap
        sitemap = EntrySitemap()
        with self.assertNumQueries(1):
            entries = list(sitemap.items())
            for entry in entries:
                self.assertIn('answer_text', entry.get_deferred_fields())
                sitemap.location(entry)
                sitemap.lastmod(entry)
        with self.assertNumQueries(1):
            self.assertEqual(sitemap.get_latest_lastmod(), self.entries[-1].updated_at)


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
            "DJANGO_SECRET_KEY": "test-only-security-key-0123456789-abcdefghijklmnopqrstuvwxyz",
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

    def test_public_profile_definitions_have_stable_pagination(self):
        from django.utils import timezone
        from .models import Definition

        definitions = [Definition.objects.create(
            user=self.author, question=self.question, definition_text=f'Definition {i}',
        ) for i in range(7)]
        Definition.objects.filter(pk__in=[item.pk for item in definitions]).update(
            created_at=timezone.now(),
        )
        url = reverse('user_profile', args=[self.author.username])
        first = self.client.get(url, {'tab': 'tanimlar', 'd_page': 1})
        second = self.client.get(url, {'tab': 'tanimlar', 'd_page': 2})
        expected = [item.pk for item in reversed(definitions)]
        self.assertEqual(
            [item.pk for item in first.context['definitions_page']], expected[:5],
        )
        self.assertEqual(
            [item.pk for item in second.context['definitions_page']], expected[5:],
        )

    def test_profile_does_not_show_extra_public_author_banner(self):
        url = reverse('user_profile', args=[self.author.username])
        self.assertNotContains(self.client.get(url), 'Herkese açık yazar sayfası')
        self.client.force_login(self.author)
        self.assertNotContains(self.client.get(url), 'Herkese açık yazar sayfası')
        self.assertEqual(self.client.get(self.url).status_code, 200)

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
        entry_url = 'http://testserver' + reverse('single_answer', args=[self.question.slug, self.answer.pk])
        self.assertEqual(data['url'], entry_url)
        self.assertEqual(data['mainEntityOfPage'], entry_url)
        self.assertEqual(data['@id'], entry_url + '#entry')
        self.assertTrue(data['dateModified'])

    def test_profile_pages_have_distinct_canonicals_and_one_author_identity(self):
        from .models import Answer
        from django.utils import timezone
        from lxml import html

        for i in range(12):
            Answer.objects.create(user=self.author, question=self.question, answer_text=f'Entry {i}')
        Answer.objects.filter(user=self.author).update(created_at=timezone.now())
        url = reverse('user_profile', args=[self.author.username])
        ids = []
        for number in (1, 2):
            response = self.client.get(url, {'answer_page': number, 'tab': 'girdiler', 'utm_source': 'test'})
            tree = html.fromstring(response.content)
            expected = 'http://testserver' + url + (f'?answer_page={number}' if number > 1 else '')
            self.assertEqual(tree.xpath('//link[@rel="canonical"]/@href'), [expected])
            data = json.loads(tree.xpath('//script[@type="application/ld+json"]/text()')[0])
            self.assertEqual(data['url'], expected)
            self.assertEqual(data['mainEntity']['url'], 'http://testserver' + self.url)
            self.assertEqual(data['mainEntity']['@id'], 'http://testserver' + self.url + '#person')
            ids.extend(entry.pk for entry in response.context['answers'])
        self.assertEqual(len(ids), 13)
        self.assertEqual(len(set(ids)), 13)
        self.assertEqual(ids, sorted(ids, reverse=True))
        response = self.client.get(url, {'answer_page': 'invalid'})
        self.assertEqual(html.fromstring(response.content).xpath('//link[@rel="canonical"]/@href'), ['http://testserver' + url])

    def test_author_sitemap_dates_follow_public_content_without_extra_queries(self):
        from datetime import timedelta
        from django.utils import timezone
        from .models import Answer, Kenarda
        from .sitemaps import AuthorSitemap

        draft_author = User.objects.create_user(username='draft-only-author')
        Kenarda.objects.create(user=draft_author, question=self.question, content='PRIVATE DRAFT')
        inactive_author = User.objects.create_user(username='inactive-author', is_active=False)
        Answer.objects.create(user=inactive_author, question=self.question, answer_text='Inactive')
        newer = timezone.now() + timedelta(minutes=1)
        Answer.objects.filter(pk=self.answer.pk).update(updated_at=newer)
        sitemap = AuthorSitemap()
        with self.assertNumQueries(1):
            authors = list(sitemap.items())
            self.assertEqual([author.pk for author in authors], [self.author.pk])
            self.assertEqual(sitemap.lastmod(authors[0]), newer)
            self.assertEqual(sitemap.location(authors[0]), self.url)
        newest = newer + timedelta(minutes=1)
        Question.objects.filter(pk=self.question.pk).update(updated_at=newest)
        self.assertEqual(sitemap.lastmod(sitemap.items().get(pk=self.author.pk)), newest)

    def test_public_entry_cards_link_to_stable_author_but_members_keep_profile(self):
        from django.template.loader import render_to_string
        from django.contrib.auth.models import AnonymousUser
        from lxml import html

        for user, expected in [(AnonymousUser(), self.url), (self.author, reverse('user_profile', args=[self.author.username]))]:
            content = render_to_string('core/_answers_list.html', {
                'answers': [self.answer], 'user': user, 'search_keyword': '',
                'answer_save_dict': {}, 'saved_answer_ids': [],
                'question': self.question,
            })
            self.assertIn(expected, html.fromstring(content).xpath('//a[@rel="author"]/@href'))

    def test_homepage_author_links_use_public_identity_for_guests(self):
        from django.core.cache import cache
        from lxml import html

        cache.clear()
        self.addCleanup(cache.clear)
        response = self.client.get(reverse('user_homepage'))
        self.assertIn(self.url, html.fromstring(response.content).xpath('//a[@rel="author"]/@href'))
        self.client.force_login(self.author)
        response = self.client.get(reverse('user_homepage'))
        self.assertIn(reverse('user_profile', args=[self.author.username]),
                      html.fromstring(response.content).xpath('//a[@rel="author"]/@href'))

    def test_author_schema_excerpt_is_bounded_and_escaped(self):
        from lxml import html

        self.answer.answer_text = '</script><script>alert("x")</script> ' + 'word ' * 150
        self.answer.save()
        response = self.client.get(self.url)
        self.assertNotContains(response, '<script>alert("x")</script>')
        tree = html.fromstring(response.content)
        data = json.loads(tree.xpath('//script[@type="application/ld+json"]/text()')[0])
        excerpt = data['hasPart'][0]['text']
        self.assertLessEqual(len(excerpt.split()), 61)
        self.assertIn(excerpt, tree.text_content())

    def test_author_schema_references_only_visible_entries_with_matching_identity(self):
        from .models import Answer
        for i in range(20):
            Answer.objects.create(user=self.author, question=self.question, answer_text=f'Entry {i}')
        for page, expected_count in [(1, 20), (2, 1)]:
            response = self.client.get(self.url, {'page': page})
            data = json.loads(re.search(
                r'<script type="application/ld\+json">(.*?)</script>', response.content.decode(), re.S,
            ).group(1))
            self.assertEqual(len(data['hasPart']), expected_count)
            for posting, entry in zip(data['hasPart'], response.context['entries_page']):
                self.assertEqual(posting['author']['@id'], data['mainEntity']['@id'])
                self.assertEqual(posting['author']['name'], self.author.username)
                self.assertEqual(posting['author']['url'], data['mainEntity']['url'])
                self.assertEqual(posting['text'], entry.answer_text)
                self.assertTrue(posting['dateModified'])
                self.assertEqual(posting['url'], 'http://testserver' + reverse(
                    'single_answer', args=[entry.question.slug, entry.pk],
                ))

    def test_author_schema_empty_list_and_untrusted_title_are_valid_json(self):
        from .models import Answer
        self.question.question_text = '</script><script>alert("x")</script>'
        self.question.save()
        response = self.client.get(self.url)
        self.assertNotContains(response, '<script>alert("x")</script>')
        data = json.loads(re.search(
            r'<script type="application/ld\+json">(.*?)</script>', response.content.decode(), re.S,
        ).group(1))
        self.assertEqual(data['hasPart'][0]['headline'], self.question.question_text)
        Answer.objects.filter(user=self.author).delete()
        response = self.client.get(self.url)
        data = json.loads(re.search(
            r'<script type="application/ld\+json">(.*?)</script>', response.content.decode(), re.S,
        ).group(1))
        self.assertEqual(data['hasPart'], [])

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
