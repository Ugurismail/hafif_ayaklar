import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.models import Answer, Question


class EntryDownloadSelectorTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="download-user",
            password="pass",
        )
        self.first_question = Question.objects.create(
            question_text="Birinci başlık",
            user=self.user,
        )
        self.second_question = Question.objects.create(
            question_text="İkinci başlık",
            user=self.user,
        )
        self.first_answer = Answer.objects.create(
            question=self.first_question,
            user=self.user,
            answer_text="Aramada bulunacak özel ifade ve ilk entry.",
        )
        self.second_answer = Answer.objects.create(
            question=self.second_question,
            user=self.user,
            answer_text="Başka bir entry metni.",
        )
        self.client.force_login(self.user)

    def test_answer_search_does_not_change_unfiltered_results(self):
        url = reverse("get_user_answers")

        filtered = self.client.get(
            url,
            {"username": self.user.username, "q": "özel ifade"},
        )
        unfiltered = self.client.get(
            url,
            {"username": self.user.username, "q": ""},
        )

        self.assertEqual(filtered.status_code, 200)
        self.assertEqual(
            [answer["id"] for answer in filtered.json()["answers"]],
            [self.first_answer.id],
        )
        self.assertEqual(unfiltered.status_code, 200)
        self.assertEqual(unfiltered.json()["total"], 2)
        self.assertCountEqual(
            [answer["id"] for answer in unfiltered.json()["answers"]],
            [self.first_answer.id, self.second_answer.id],
        )

    def test_answer_list_uses_safe_pagination_defaults_and_limit(self):
        url = reverse("get_user_answers")

        invalid = self.client.get(
            url,
            {
                "username": self.user.username,
                "page": "not-a-page",
                "page_size": "not-a-size",
            },
        )
        oversized = self.client.get(
            url,
            {"username": self.user.username, "page_size": "1000"},
        )

        self.assertEqual(invalid.status_code, 200)
        self.assertEqual(invalid.json()["page"], 1)
        self.assertEqual(invalid.json()["page_size"], 50)
        self.assertEqual(oversized.status_code, 200)
        self.assertEqual(oversized.json()["page_size"], 100)

    def test_profile_renders_persistent_selection_workspace(self):
        response = self.client.get(
            reverse("user_profile", args=[self.user.username]),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="selectedEntriesList"')
        self.assertContains(response, "Arama değişse de seçimlerin korunur.")
        self.assertContains(response, "selectedEntryOrder.filter")

    def test_custom_export_accepts_entries_selected_from_separate_searches(self):
        response = self.client.post(
            reverse("download_entries_json", args=[self.user.username]),
            {
                "entry_ids": f"{self.second_answer.id},{self.first_answer.id}",
                "order": "custom",
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = json.loads(response.content.decode("utf-8"))
        self.assertEqual(
            [entry["answer_id"] for entry in payload["entries"]],
            [self.second_answer.id, self.first_answer.id],
        )
