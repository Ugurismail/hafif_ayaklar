from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import connection
from django.test import RequestFactory, TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone

from .forms import PollForm
from .models import Poll, PollOption, PollVote
from .views.poll_views import _build_polls_context


User = get_user_model()


class PollFormTests(TestCase):
    def test_missing_end_date_returns_validation_error(self):
        form = PollForm({
            "question_text": "Eksik tarihli anket",
            "option_1": "Evet",
            "option_2": "Hayır",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("end_date", form.errors)

    def test_duplicate_options_are_rejected_case_insensitively(self):
        form = PollForm({
            "question_text": "Aynı seçenek kabul edilir mi?",
            "end_date": (timezone.now() + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M"),
            "option_1": "Katılıyorum",
            "option_2": "KATILIYORUM",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("birbirinden farklı", form.errors["option_1"][0])


class PollWorkflowTests(TestCase):
    def setUp(self):
        self.client.defaults["HTTP_HOST"] = "localhost"
        self.owner = User.objects.create_user(username="poll-owner", password="pass")
        self.voter = User.objects.create_user(username="poll-voter", password="pass")
        self.active_poll = self._make_poll(
            "Aktif anket",
            creator=self.owner,
            end_date=timezone.now() + timedelta(days=3),
            anonymous=False,
        )
        self.expired_poll = self._make_poll(
            "Arşiv anketi",
            creator=self.owner,
            end_date=timezone.now() - timedelta(days=1),
        )

    def _make_poll(self, question, creator=None, end_date=None, anonymous=True, options=None):
        poll = Poll.objects.create(
            question_text=question,
            created_by=creator or self.owner,
            end_date=end_date or timezone.now() + timedelta(days=2),
            is_anonymous=anonymous,
        )
        PollOption.objects.bulk_create([
            PollOption(poll=poll, option_text=text)
            for text in (options or ["Evet", "Hayır"])
        ])
        return poll

    def _poll_post_data(self, prefix="", **overrides):
        key = lambda name: f"{prefix}-{name}" if prefix else name
        data = {
            key("question_text"): "Yeni anket sorusu",
            key("end_date"): (timezone.now() + timedelta(days=5)).strftime("%Y-%m-%dT%H:%M"),
            key("is_anonymous"): "on",
            key("option_1"): "Birinci",
            key("option_2"): "İkinci",
            key("option_3"): "Üçüncü",
        }
        data.update(overrides)
        return data

    def test_home_separates_active_and_archived_polls(self):
        active_response = self.client.get(reverse("polls_home"), {"status": "active"})
        archive_response = self.client.get(reverse("polls_home"), {"status": "expired"})

        self.assertEqual(active_response.status_code, 200)
        self.assertContains(active_response, "Aktif anket")
        self.assertNotContains(active_response, "Arşiv anketi")
        self.assertContains(archive_response, "Arşiv anketi")
        self.assertNotContains(archive_response, "Aktif anket")
        self.assertNotContains(active_response, "Chart.js")

    def test_search_keeps_status_and_filters_questions(self):
        self._make_poll("Başka bir aktif anket")

        response = self.client.get(reverse("polls_home"), {
            "status": "active",
            "q": "Başka",
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Başka bir aktif anket")
        self.assertEqual(response.context["status"], "active")
        self.assertEqual(response.context["search_query"], "Başka")
        self.assertEqual(
            [card["poll"].question_text for card in response.context["active_polls_data"]],
            ["Başka bir aktif anket"],
        )

    def test_archive_is_paginated_for_large_collections(self):
        for index in range(21):
            self._make_poll(
                f"Eski anket {index:02d}",
                end_date=timezone.now() - timedelta(days=index + 2),
            )

        first_page = self.client.get(reverse("polls_home"), {"status": "expired"})
        second_page = self.client.get(reverse("polls_home"), {"status": "expired", "page": 2})

        self.assertEqual(first_page.context["page_obj"].paginator.num_pages, 2)
        self.assertEqual(len(first_page.context["expired_polls_data"]), 20)
        self.assertEqual(len(second_page.context["expired_polls_data"]), 2)
        self.assertContains(first_page, '<details class="poll-archive-item">', count=20, html=False)

    def test_listing_query_count_does_not_grow_per_poll(self):
        for index in range(8):
            self._make_poll(
                f"Ölçek anketi {index}",
                options=[f"Seçenek {index}-{option}" for option in range(5)],
            )
        request = RequestFactory().get("/polls/?status=active")
        request.user = self.voter

        with CaptureQueriesContext(connection) as queries:
            context = _build_polls_context(request)

        self.assertEqual(len(context["active_polls_data"]), 9)
        self.assertLessEqual(len(queries), 6)

    def test_invalid_create_reopens_form_with_errors(self):
        self.client.force_login(self.owner)
        data = self._poll_post_data()
        data["option_2"] = ""
        data["option_3"] = ""

        response = self.client.post(reverse("create_poll"), data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["open_create_poll_modal"])
        self.assertContains(response, "En az 2 seçenek")
        self.assertFalse(Poll.objects.filter(question_text="Yeni anket sorusu").exists())

    def test_create_saves_all_non_empty_options(self):
        self.client.force_login(self.owner)

        response = self.client.post(reverse("create_poll"), self._poll_post_data())

        poll = Poll.objects.get(question_text="Yeni anket sorusu")
        self.assertRedirects(response, reverse("polls_home"))
        self.assertEqual(
            list(poll.options.order_by("id").values_list("option_text", flat=True)),
            ["Birinci", "İkinci", "Üçüncü"],
        )

    def test_edit_uses_prefixed_fields_and_updates_options(self):
        self.client.force_login(self.owner)

        get_response = self.client.get(reverse("edit_poll", args=[self.active_poll.id]))
        self.assertContains(get_response, 'name="edit-question_text"')
        self.assertTrue(get_response.context["open_edit_poll_modal"])

        response = self.client.post(
            reverse("edit_poll", args=[self.active_poll.id]),
            self._poll_post_data(prefix="edit", **{"edit-question_text": "Düzenlenmiş anket"}),
        )

        self.active_poll.refresh_from_db()
        self.assertRedirects(response, reverse("polls_home"))
        self.assertEqual(self.active_poll.question_text, "Düzenlenmiş anket")
        self.assertEqual(self.active_poll.options.count(), 3)

    def test_vote_requires_post_and_allows_only_one_vote_per_poll(self):
        self.client.force_login(self.voter)
        options = list(self.active_poll.options.order_by("id"))
        first_vote_url = reverse("vote_poll", args=[self.active_poll.id, options[0].id])
        second_vote_url = reverse("vote_poll", args=[self.active_poll.id, options[1].id])

        self.assertEqual(self.client.get(first_vote_url).status_code, 405)
        self.client.post(first_vote_url)
        self.client.post(second_vote_url)

        votes = PollVote.objects.filter(user=self.voter, option__poll=self.active_poll)
        self.assertEqual(votes.count(), 1)
        self.assertEqual(votes.get().option_id, options[0].id)

    def test_expired_poll_rejects_vote(self):
        self.client.force_login(self.voter)
        option = self.expired_poll.options.order_by("id").first()

        response = self.client.post(reverse("vote_poll", args=[self.expired_poll.id, option.id]))

        self.assertRedirects(response, reverse("polls_home"))
        self.assertFalse(PollVote.objects.filter(user=self.voter, option__poll=self.expired_poll).exists())

    def test_public_detail_shows_voter_but_anonymous_detail_hides_them(self):
        public_option = self.active_poll.options.order_by("id").first()
        PollVote.objects.create(user=self.voter, option=public_option)
        anonymous_poll = self._make_poll("Anonim anket", anonymous=True)
        anonymous_option = anonymous_poll.options.order_by("id").first()
        PollVote.objects.create(user=self.voter, option=anonymous_option)
        self.client.force_login(self.owner)

        public_response = self.client.get(reverse("poll_detail", args=[self.active_poll.id]))
        anonymous_response = self.client.get(reverse("poll_detail", args=[anonymous_poll.id]))

        self.assertContains(public_response, self.voter.username)
        self.assertNotContains(anonymous_response, self.voter.username)
