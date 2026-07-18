import re

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.test import TestCase

from .answer_git import attach_answer_revision_metadata
from .content_link_preload import preload_content_links
from .models import (
    Answer,
    AnswerRevision,
    AnswerRevisionApproval,
    AnswerSuggestion,
    Definition,
    Question,
    Reference,
    SavedItem,
)
from .services import VoteSaveService
from .templatetags.custom_tags import mention_link, ref_link, reference_link, tanim_link


class ContentLinkPreloadTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="hedefkullanici", password="pass")
        self.question = Question.objects.create(question_text="Hedef baslik", user=self.user)
        self.definition = Definition.objects.create(
            user=self.user,
            question=self.question,
            definition_text="Toplu yuklenen tanim.",
        )
        self.reference = Reference.objects.create(
            author_surname="Yazar",
            author_name="Ad",
            year=2026,
            metin_ismi="Metin",
            rest="Yayinevi",
            created_by=self.user,
        )

    def test_embedded_links_use_bulk_loaded_objects_without_extra_queries(self):
        snippets = [
            f"(tanim:Kavram:{self.definition.id})",
            f"(kaynak:{self.reference.id}, sayfa:12)",
            "(ref:Hedef baslik)",
            "@hedefkullanici",
        ]

        with preload_content_links(snippets):
            with self.assertNumQueries(0):
                definition_html = str(tanim_link(snippets[0]))
                reference_html = str(reference_link(snippets[1]))
                question_html = str(ref_link(snippets[2]))
                mention_html = str(mention_link(snippets[3]))

        self.assertIn("Toplu yuklenen tanim.", definition_html)
        self.assertIn("Yazar, Ad", reference_html)
        self.assertIn(self.question.slug, question_html)
        self.assertIn("hedefkullanici", mention_html)


class RevisionMetadataQueryTests(TestCase):
    def test_revision_counts_suggestions_and_approvals_are_loaded_in_two_queries(self):
        owner = User.objects.create_user(username="owner", password="pass")
        question = Question.objects.create(question_text="Surum testi", user=owner)
        answer = Answer.objects.create(question=question, user=owner, answer_text="Ilk metin")
        first_revision = answer.revisions.get(revision_no=1)
        first_revision.is_current = False
        first_revision.save(update_fields=["is_current"])
        current_revision = AnswerRevision.objects.create(
            answer=answer,
            parent_revision=first_revision,
            base_revision=first_revision,
            created_by=owner,
            content="Guncel metin",
            revision_no=2,
            source="author_edit",
            is_current=True,
        )
        AnswerSuggestion.objects.create(
            answer=answer,
            base_revision=current_revision,
            proposed_by=owner,
            proposed_text="Onerilen metin",
            status="open",
        )
        AnswerRevisionApproval.objects.create(
            revision=current_revision,
            user=owner,
            status="approved",
        )

        with self.assertNumQueries(2):
            attach_answer_revision_metadata([answer], current_user=owner)

        self.assertEqual(answer.revision_count, 2)
        self.assertEqual(answer.open_suggestion_count, 1)
        self.assertEqual(answer.contributor_usernames, ["owner"])
        self.assertTrue(answer.current_user_revision_approval)


class SaveInfoQueryTests(TestCase):
    def test_save_count_and_current_user_state_are_loaded_in_one_query(self):
        owner = User.objects.create_user(username="save-owner", password="pass")
        other = User.objects.create_user(username="save-other", password="pass")
        question = Question.objects.create(question_text="Kaydetme testi", user=owner)
        answer = Answer.objects.create(question=question, user=owner, answer_text="Metin")
        content_type = ContentType.objects.get_for_model(Answer)
        SavedItem.objects.create(
            user=owner,
            content_type=content_type,
            object_id=answer.id,
        )
        SavedItem.objects.create(
            user=other,
            content_type=content_type,
            object_id=answer.id,
        )

        with self.assertNumQueries(1):
            saved_ids, save_counts = VoteSaveService.get_save_info([answer], owner, Answer)

        self.assertEqual(saved_ids, {answer.id})
        self.assertEqual(save_counts, {answer.id: 2})


class HomepagePerformanceIntegrationTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username="homepage-owner", password="pass")
        self.question = Question.objects.create(question_text="Ana sayfa testi", user=self.user)
        self.answer = Answer.objects.create(
            question=self.question,
            user=self.user,
            answer_text="**Onemli** ana sayfa metni",
        )

    def tearDown(self):
        cache.clear()

    def test_homepage_exposes_timing_and_reuses_rendered_cards(self):
        first_response = self.client.get("/", HTTP_HOST="localhost")
        second_response = self.client.get("/", HTTP_HOST="localhost")

        self.assertEqual(first_response.status_code, 200)
        self.assertContains(second_response, "<strong>Onemli</strong>", html=True)
        timing = second_response.headers.get("Server-Timing", "")
        self.assertIn("db;dur=", timing)
        match = re.search(r'desc="(\d+) queries"', timing)
        self.assertIsNotNone(match)
        self.assertLessEqual(int(match.group(1)), 8)
