from django.test import RequestFactory, SimpleTestCase

from core.middleware import LastSeenMiddleware
from core.templatetags.custom_tags import safe_markdownify
from core.views.attendance_views import _normalize_marks, _normalize_sheets


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


class MarkdownRenderingTests(SimpleTestCase):
    def test_multi_digit_leading_ordinal_renders_as_text(self):
        rendered = str(safe_markdownify("16. yüzyılda gerçekleşen olay"))

        self.assertIn("16. yüzyılda gerçekleşen olay", rendered)
        self.assertNotIn("<ol>", rendered)
        self.assertNotIn("<li>", rendered)

    def test_single_digit_ordered_lists_still_render_as_lists(self):
        rendered = str(safe_markdownify("1. Bir\n2. İki"))

        self.assertIn("<ol>", rendered)
        self.assertIn("<li>Bir</li>", rendered)
        self.assertIn("<li>İki</li>", rendered)


class AttendanceSheetTests(SimpleTestCase):
    def test_normalize_sheets_keeps_blank_rows_and_order(self):
        raw_sheets = [{
            "page": 1,
            "sections": [{
                "code": "120",
                "people": [
                    {"id": "blank-row", "name": "", "is_blank": True},
                    {"id": "person-a", "name": "A KISI", "is_blank": False},
                    {"id": "person-b", "name": "B KISI", "is_blank": False},
                ],
            }],
        }]

        sheets = _normalize_sheets(raw_sheets)
        people = sheets[0]["sections"][0]["people"]

        self.assertEqual([person["id"] for person in people[:3]], ["blank-row", "person-a", "person-b"])
        self.assertTrue(people[0]["is_blank"])
        self.assertEqual(people[0]["name"], "")

    def test_normalize_marks_ignores_blank_rows(self):
        sheets = _normalize_sheets([{
            "page": 1,
            "sections": [{
                "code": "120",
                "people": [
                    {"id": "blank-row", "name": "", "is_blank": True},
                    {"id": "person-a", "name": "A KISI", "is_blank": False},
                ],
            }],
        }])

        marks = _normalize_marks({
            "blank-row": {"morning-in": "İ"},
            "person-a": {"morning-in": "G", "morning-out": "H", "noon-out": "R"},
        }, sheets)

        self.assertNotIn("blank-row", marks)
        self.assertEqual(marks["person-a"], {"morning-in": "G", "morning-out": "H", "noon-out": "R"})
