from datetime import timedelta
import json

from django.contrib.auth.models import User
from django.test import RequestFactory, SimpleTestCase, TestCase
from django.utils import timezone

from core.content_limits import EDITOR_CONTENT_MAX_LENGTH
from core.middleware import LastSeenMiddleware
from core.models import Kenarda, OnlineChatMessage, Question, UserProfile
from core.templatetags.custom_tags import bkz_link, safe_markdownify
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

    def test_dotted_outline_renders_up_to_four_levels(self):
        rendered = str(safe_markdownify(
            "1. Bir\n"
            "1.1. İki\n"
            "1.1.1. Üç\n"
            "1.1.1.1. Dört"
        ))

        self.assertIn('class="answer-outline-list"', rendered)
        self.assertIn('class="answer-outline-item answer-outline-level-1"', rendered)
        self.assertIn('class="answer-outline-item answer-outline-level-2"', rendered)
        self.assertIn('class="answer-outline-item answer-outline-level-3"', rendered)
        self.assertIn('class="answer-outline-item answer-outline-level-4"', rendered)
        self.assertIn('<span class="answer-outline-marker">1.1.1.1.</span>', rendered)

    def test_math_text_is_not_rewritten_by_bkz_filter(self):
        rendered = str(bkz_link(safe_markdownify(r"$\text{(bkz: test)} + x$")))

        self.assertIn(r"$\text{(bkz: test)} + x$", rendered)
        self.assertNotIn("<a ", rendered)


class OnlineChatUnreadCountTests(TestCase):
    def test_unread_count_endpoint_returns_lightweight_payload(self):
        viewer = User.objects.create_user(username="viewer", password="pass")
        sender = User.objects.create_user(username="sender", password="pass")
        profile, _ = UserProfile.objects.get_or_create(user=viewer)
        profile.online_chat_last_read_at = timezone.now() - timedelta(minutes=5)
        profile.save(update_fields=["online_chat_last_read_at"])
        OnlineChatMessage.objects.create(user=sender, body="selam")

        self.client.force_login(viewer)
        response = self.client.get(
            "/online-chat/unread-count/",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["unread_count"], 1)
        self.assertNotIn("messages", payload)
        self.assertNotIn("online_users", payload)

    def test_existing_matrix_row_break_is_not_over_normalized(self):
        rendered = str(safe_markdownify(r"$$\begin{pmatrix}1 & 2\\ 3 & 4\end{pmatrix}$$"))

        self.assertIn(r"\\ 3", rendered)
        self.assertNotIn(r"\\\ 3", rendered)

    def test_single_backslash_before_matrix_row_is_normalized(self):
        rendered = str(safe_markdownify(r"$$\begin{pmatrix}1 & 2\3 & 4\end{pmatrix}$$"))

        self.assertIn(r"\\ 3", rendered)


class KenardaDraftTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="draft-user", password="pass")
        self.question = Question.objects.create(
            question_text="Uzun taslak testi",
            user=self.user,
        )
        self.client.force_login(self.user)

    def test_save_accepts_draft_longer_than_50000_characters(self):
        content = "uzun taslak " * 5000

        response = self.client.post(
            "/kenarda/save/",
            data=json.dumps({"question_id": self.question.id, "content": content}),
            content_type="application/json",
            HTTP_HOST="127.0.0.1:8000",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

        draft = Kenarda.objects.get(user=self.user, question=self.question, is_sent=False)
        self.assertEqual(draft.content, content)
        self.assertGreater(len(draft.content), 50000)

    def test_live_preview_accepts_draft_longer_than_50000_characters(self):
        content = "uzun önizleme " * 5000

        response = self.client.post(
            "/answer/preview/",
            data=json.dumps(
                {
                    "content": content,
                    "question_text": self.question.question_text,
                    "question_slug": self.question.slug,
                }
            ),
            content_type="application/json",
            HTTP_HOST="127.0.0.1:8000",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        self.assertIn("uzun önizleme", response.json()["html"])
        self.assertGreater(len(content), 50000)

    def test_save_and_live_preview_share_the_same_maximum_length(self):
        content = "x" * (EDITOR_CONTENT_MAX_LENGTH + 1)
        payloads = (
            ("/kenarda/save/", {"question_id": self.question.id, "content": content}),
            ("/answer/preview/", {"content": content}),
        )

        for path, payload in payloads:
            with self.subTest(path=path):
                response = self.client.post(
                    path,
                    data=json.dumps(payload),
                    content_type="application/json",
                    HTTP_HOST="127.0.0.1:8000",
                )

                self.assertEqual(response.status_code, 400)
                self.assertIn(str(EDITOR_CONTENT_MAX_LENGTH), response.json()["error"])

    def test_draft_list_does_not_embed_full_content_in_button_attributes(self):
        content = "uzun taslak " * 700
        Kenarda.objects.create(user=self.user, question=self.question, content=content)

        response = self.client.get("/kenarda/", HTTP_HOST="127.0.0.1:8000")

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "data-taslak-content")
        self.assertNotContains(response, content)


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
