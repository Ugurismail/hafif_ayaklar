from django.test import RequestFactory, SimpleTestCase

from core.middleware import LastSeenMiddleware


class VisitorTrackingTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def request(self, path="/", **headers):
        defaults = {
            "HTTP_ACCEPT": "text/html,application/xhtml+xml",
            "HTTP_USER_AGENT": "Mozilla/5.0 Safari/605.1.15",
            "HTTP_SEC_FETCH_DEST": "document",
            "REMOTE_ADDR": "203.0.113.42",
        }
        defaults.update(headers)
        return self.factory.get(path, **defaults)

    def test_tracks_normal_document_request(self):
        request = self.request("/")

        self.assertTrue(LastSeenMiddleware._should_track_unique_visitor(request))

    def test_does_not_track_bot_user_agent(self):
        request = self.request("/", HTTP_USER_AGENT="GPTBot/1.0")

        self.assertFalse(LastSeenMiddleware._should_track_unique_visitor(request))

    def test_does_not_track_statistics_page(self):
        request = self.request("/statistics/")

        self.assertFalse(LastSeenMiddleware._should_track_unique_visitor(request))

    def test_does_not_track_non_document_fetch(self):
        request = self.request(
            "/online-chat/messages/",
            HTTP_ACCEPT="application/json",
            HTTP_SEC_FETCH_DEST="empty",
        )

        self.assertFalse(LastSeenMiddleware._should_track_unique_visitor(request))

    def test_prefers_cloudflare_client_ip(self):
        request = self.request(
            "/",
            HTTP_CF_CONNECTING_IP="198.51.100.10",
            HTTP_X_FORWARDED_FOR="203.0.113.99, 198.51.100.2",
        )

        self.assertEqual(LastSeenMiddleware._get_client_ip(request), "198.51.100.10")
