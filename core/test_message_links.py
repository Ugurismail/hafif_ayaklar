from html.parser import HTMLParser

from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.utils.safestring import mark_safe

from core.models import Message
from core.templatetags.message_tags import message_links


class LinkParser(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.tags = []
        self.links = []
        self.feed(str(html))

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        if tag == 'a':
            self.links.append(dict(attrs))


class MessageLinksTests(SimpleTestCase):
    def test_web_links_open_safely_in_new_tabs(self):
        urls = ['https://example.com/read?a=1&b=2', 'http://example.org/',
                'https://hafifayaklar.com/entry/123/']
        links = LinkParser(message_links(' '.join(urls))).links
        self.assertEqual([link['href'] for link in links], urls)
        for link in links:
            self.assertEqual(link['target'], '_blank')
            self.assertEqual(set(link['rel'].split()), {'nofollow', 'noopener', 'noreferrer'})

    def test_bare_domains_and_email_remain_clickable(self):
        links = LinkParser(message_links('www.example.com reader@example.com')).links
        self.assertEqual(links[0]['target'], '_blank')
        self.assertEqual(links[1]['href'], 'mailto:reader@example.com')

    def test_user_html_and_unsafe_schemes_are_not_executable(self):
        html = message_links(mark_safe(
            '<script>alert(1)</script><img src=x onerror=alert(1)>'
            '<a href="javascript:alert(1)">click</a> javascript:alert(1)'
        ))
        self.assertEqual(LinkParser(html).tags, [])
        self.assertIn('&lt;script&gt;', html)

    def test_plain_text_is_preserved(self):
        self.assertEqual(message_links('Merhaba & iyi günler\nİkinci satır'),
                         'Merhaba &amp; iyi günler\nİkinci satır')


class MessageLinkPageTests(TestCase):
    def test_both_message_directions_use_new_tabs_but_navigation_does_not(self):
        reader = User.objects.create_user(username='link-reader')
        writer = User.objects.create_user(username='link-writer')
        for sender, recipient, path in [(reader, writer, 'sent'), (writer, reader, 'received')]:
            Message.objects.create(sender=sender, recipient=recipient,
                                   body=f'https://example.com/{path}')
        self.client.force_login(reader)
        response = self.client.get(reverse('message_detail', args=[writer.username]))
        self.assertEqual(response.status_code, 200)
        links = LinkParser(response.content.decode()).links
        for path in ['sent', 'received']:
            link = next(link for link in links if link.get('href') == f'https://example.com/{path}')
            self.assertEqual(link['target'], '_blank')
            self.assertIn('noopener', link['rel'])
        back = next(link for link in links if link.get('class') == 'message-back')
        self.assertNotIn('target', back)
