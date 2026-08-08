from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Answer, Question, QuestionRelationship, StartingQuestion


class QuestionSchemaTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="schema-owner", password="pass")
        self.other = User.objects.create_user(username="schema-other", password="pass")

        self.root = Question.objects.create(question_text="Ana baslik", user=self.owner)
        self.child = Question.objects.create(question_text="Ilk alt baslik", user=self.owner)
        self.grandchild = Question.objects.create(question_text="Derin hedef baslik", user=self.owner)
        self.other_root = Question.objects.create(question_text="Baska sema", user=self.other)

        StartingQuestion.objects.create(user=self.owner, question=self.root)
        StartingQuestion.objects.create(user=self.other, question=self.other_root)
        QuestionRelationship.objects.create(
            user=self.owner,
            parent=self.root,
            child=self.child,
        )
        QuestionRelationship.objects.create(
            user=self.owner,
            parent=self.child,
            child=self.grandchild,
        )

        self.owner_answer = Answer.objects.create(
            question=self.child,
            user=self.owner,
            answer_text="**Sema entry metni**",
        )
        Answer.objects.create(
            question=self.child,
            user=self.other,
            answer_text="Baska kullanicinin entrysi",
        )

    def test_page_only_bootstraps_selected_users_roots(self):
        response = self.client.get(
            reverse("question_schema"),
            {"user_id": self.owner.id},
        )

        self.assertEqual(response.status_code, 200)
        roots = response.context["root_nodes"]
        self.assertEqual([row["id"] for row in roots], [self.root.id])
        self.assertEqual(roots[0]["child_count"], 1)
        self.assertNotContains(response, self.other_root.question_text)

    def test_children_endpoint_returns_only_the_selected_users_branch(self):
        response = self.client.get(
            reverse("question_schema_children", args=[self.root.id]),
            {"user_id": self.owner.id},
        )

        self.assertEqual(response.status_code, 200)
        children = response.json()["children"]
        self.assertEqual([row["id"] for row in children], [self.child.id])
        self.assertEqual(children[0]["child_count"], 1)
        self.assertEqual(children[0]["answer_count"], 1)

    def test_content_endpoint_filters_entries_by_selected_user(self):
        response = self.client.get(
            reverse("question_schema_content", args=[self.child.id]),
            {"user_id": self.owner.id},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["total_answers"], 1)
        self.assertEqual([row["id"] for row in payload["answers"]], [self.owner_answer.id])
        self.assertIn("<strong>Sema entry metni</strong>", payload["answers"][0]["rendered_html"])

    def test_search_returns_the_full_path_to_a_nested_title(self):
        response = self.client.get(
            reverse("question_schema_search"),
            {"user_id": self.owner.id, "q": "Derin hedef"},
        )

        self.assertEqual(response.status_code, 200)
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], self.grandchild.id)
        self.assertEqual(
            results[0]["path_ids"],
            [self.root.id, self.child.id, self.grandchild.id],
        )
        self.assertEqual(results[0]["depth"], 2)
