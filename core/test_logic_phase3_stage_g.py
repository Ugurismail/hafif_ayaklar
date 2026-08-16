from html import unescape

from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from .logic_course_data import VISIBLE_LOGIC_LESSONS
from .logic_phase3_stage_a import STAGE_A_CANDIDATE_MAP
from .logic_phase3_stage_b import STAGE_B_CANDIDATE_MAP
from .logic_phase3_stage_c import STAGE_C_CANDIDATE_MAP
from .logic_phase3_stage_d import STAGE_D_CANDIDATE_MAP
from .logic_phase3_stage_e import STAGE_E_CANDIDATE_MAP
from .logic_phase3_stage_f import STAGE_F_CANDIDATE_MAP
from .logic_phase3_stage_g import (
    STAGE_G_CANDIDATE_LESSONS,
    STAGE_G_CANDIDATE_MAP,
    STAGE_G_SOURCE_REFERENCES,
)
from .models import LogicLessonProgress


class LogicPhase3StageGCandidateTests(SimpleTestCase):
    def test_stage_g_candidates_are_contiguous_and_isolated(self):
        self.assertEqual(
            [lesson["curriculum_id"] for lesson in STAGE_G_CANDIDATE_LESSONS],
            ["G42", "G43", "G44", "G45", "G46", "G47", "G48", "G49", "G50"],
        )
        self.assertEqual(
            [lesson["order"] for lesson in STAGE_G_CANDIDATE_LESSONS],
            list(range(42, 51)),
        )
        visible_slugs = {lesson["slug"] for lesson in VISIBLE_LOGIC_LESSONS}
        self.assertTrue(set(STAGE_G_CANDIDATE_MAP).isdisjoint(visible_slugs))

    def test_every_candidate_has_complete_common_and_reading_contract(self):
        required = {
            "curriculum_id",
            "release_status",
            "order",
            "slug",
            "title",
            "summary",
            "focus",
            "estimated_minutes",
            "prerequisites",
            "competencies",
            "goals",
            "key_terms",
            "sections",
            "worked_examples",
            "mistakes",
            "practice",
            "guided_practice",
            "production_tasks",
            "mastery_evidence",
            "review_prompts",
            "source_ids",
            "reading_fixtures",
            "comparison_fixtures",
            "primary_text_locators",
        }
        all_candidates = {
            **STAGE_A_CANDIDATE_MAP,
            **STAGE_B_CANDIDATE_MAP,
            **STAGE_C_CANDIDATE_MAP,
            **STAGE_D_CANDIDATE_MAP,
            **STAGE_E_CANDIDATE_MAP,
            **STAGE_F_CANDIDATE_MAP,
            **STAGE_G_CANDIDATE_MAP,
        }

        for lesson in STAGE_G_CANDIDATE_LESSONS:
            with self.subTest(lesson=lesson["curriculum_id"]):
                self.assertTrue(required.issubset(lesson))
                self.assertEqual(lesson["release_status"], "candidate")
                self.assertGreaterEqual(len(lesson["sections"]), 6)
                self.assertGreaterEqual(len(lesson["worked_examples"]), 12)
                self.assertGreaterEqual(len(lesson["practice"]), 12)
                self.assertGreaterEqual(len(lesson["production_tasks"]), 2)
                self.assertGreaterEqual(len(lesson["mastery_evidence"]), 4)
                self.assertGreaterEqual(len(lesson["reading_fixtures"]), 3)
                self.assertTrue(lesson["primary_text_locators"])
                self.assertEqual(
                    len(lesson["competencies"]),
                    len(set(lesson["competencies"])),
                )
                for prerequisite in lesson["prerequisites"]:
                    self.assertIn(prerequisite, all_candidates)
                    self.assertLess(
                        all_candidates[prerequisite]["order"],
                        lesson["order"],
                    )
                for source_id in lesson["source_ids"]:
                    self.assertIn(source_id, STAGE_G_SOURCE_REFERENCES)

    def test_g42_bridges_f41_and_stage_g_forms_a_chain(self):
        self.assertEqual(
            STAGE_G_CANDIDATE_LESSONS[0]["prerequisites"],
            ["ders-41-ceviri-model-kanit-asama-projesi"],
        )
        for previous, current in zip(
            STAGE_G_CANDIDATE_LESSONS,
            STAGE_G_CANDIDATE_LESSONS[1:],
        ):
            self.assertEqual(current["prerequisites"], [previous["slug"]])

    def test_practice_answers_and_production_stimuli_are_auditable(self):
        for lesson in STAGE_G_CANDIDATE_LESSONS:
            for item in lesson["practice"]:
                with self.subTest(
                    lesson=lesson["curriculum_id"],
                    prompt=item["prompt"],
                ):
                    self.assertIn(item["answer"], "ABCD")
                    self.assertEqual(len(item["choices"]), 4)
                    self.assertTrue(item["explanation"])
            for task in lesson["production_tasks"]:
                self.assertTrue(task["stimulus"]["label"])
                self.assertTrue(task["stimulus"]["items"])
                self.assertTrue(task["checkpoints"])

    def test_reading_fixtures_have_traceable_sources_and_interpretive_limits(self):
        seen_fixture_ids = set()
        for lesson in STAGE_G_CANDIDATE_LESSONS:
            for fixture in lesson["reading_fixtures"]:
                with self.subTest(fixture=fixture["id"]):
                    self.assertNotIn(fixture["id"], seen_fixture_ids)
                    seen_fixture_ids.add(fixture["id"])
                    self.assertIn(fixture["source_id"], lesson["source_ids"])
                    self.assertIn(
                        fixture["source_id"],
                        STAGE_G_SOURCE_REFERENCES,
                    )
                    self.assertTrue(fixture["locator"].strip())
                    self.assertTrue(fixture["focus"].strip())
                    self.assertGreaterEqual(
                        len(fixture["required_distinctions"]),
                        3,
                    )
                    self.assertGreaterEqual(
                        len(fixture["prohibited_shortcuts"]),
                        2,
                    )
                    self.assertTrue(fixture["task"].strip())
                    self.assertTrue(fixture["boundary"].strip())

    def test_comparisons_preserve_shared_problem_and_real_differences(self):
        for lesson in STAGE_G_CANDIDATE_LESSONS:
            self.assertTrue(lesson["comparison_fixtures"])
            for fixture in lesson["comparison_fixtures"]:
                self.assertNotEqual(fixture["left"], fixture["right"])
                self.assertTrue(fixture["shared_problem"])
                self.assertGreaterEqual(len(fixture["differences"]), 3)
                self.assertTrue(fixture["task"])

    def test_frege_lessons_block_category_and_psychological_shortcuts(self):
        g42, g43 = STAGE_G_CANDIDATE_LESSONS[:2]
        g42_text = self._lesson_text(g42)
        g43_text = self._lesson_text(g43)

        self.assertIn("kategori", g42_text.lower())
        self.assertIn("küme", g42_text.lower())
        self.assertIn("modern fol", g42_text.lower())
        self.assertIn("zihinsel imge", g43_text.lower())
        self.assertIn("bilişsel değer", g43_text.lower())
        self.assertIn("dolaylı bağlam", g43_text.lower())

    def test_russell_lessons_keep_scope_and_historical_differences_visible(self):
        g44, g45 = STAGE_G_CANDIDATE_LESSONS[2:4]
        g44_text = self._lesson_text(g44)
        g45_text = self._lesson_text(g45)

        for term in ("varlık", "biriciklik", "yüklemleme", "dar kapsam", "geniş kapsam"):
            self.assertIn(term, g44_text.lower())
        self.assertIn("fiziksel parça", g45_text.lower())
        self.assertIn("ortak problem", g45_text.lower())
        self.assertIn("tek kuram", g45_text.lower())

    def test_tractatus_lessons_preserve_argument_architecture_and_limits(self):
        g46, g47 = STAGE_G_CANDIDATE_LESSONS[4:6]
        g46_text = self._lesson_text(g46).lower()
        g47_text = self._lesson_text(g47).lower()

        for term in ("dünya", "olgu", "nesne", "resim", "mantıksal biçim"):
            self.assertIn(term, g46_text)
        for term in ("söyleme", "gösterme", "totoloji", "merdiven", "susma"):
            self.assertIn(term, g47_text)
        self.assertIn("kelime", g47_text)
        self.assertIn("önemsiz", g47_text)

    def test_late_method_lesson_blocks_slogan_and_relativist_shortcuts(self):
        g48_text = self._lesson_text(STAGE_G_CANDIDATE_MAP[
            "ders-48-gecis-dil-oyunlari-kullanim-gramer"
        ]).lower()

        for term in ("dil oyunu", "kullanım", "aile benzerliği", "gramer"):
            self.assertIn(term, g48_text)
        self.assertIn("çoğunluk", g48_text)
        self.assertIn("sıklık", g48_text)
        self.assertIn("tekelleş", g48_text)

    def test_rule_following_and_private_language_keep_normative_boundaries(self):
        g49_text = self._lesson_text(STAGE_G_CANDIDATE_MAP[
            "ders-49-kural-izleme-ozel-dil"
        ]).lower()

        for term in ("yorum gerilemesi", "doğru görünme", "doğru olma", "böcek"):
            self.assertIn(term, g49_text)
        for shortcut in ("çoğunlukçuluk", "davranışçılık", "tek başına"):
            self.assertIn(shortcut, g49_text)

    def test_final_workshop_requires_auditable_independent_close_reading(self):
        g50 = STAGE_G_CANDIDATE_MAP[
            "ders-50-kesinlik-uzerine-bitirme-atolyesi"
        ]
        g50_text = self._lesson_text(g50).lower()

        for term in ("dünya resmi", "menteşe", "rakip okuma", "sınır notu"):
            self.assertIn(term, g50_text)
        self.assertIn("biçimsel mantık", g50_text)
        self.assertGreaterEqual(len(g50["comparison_fixtures"]), 2)
        self.assertTrue(
            any(
                "çözülmemiş" in task["prompt"].lower()
                for task in g50["production_tasks"]
            )
        )

    def test_primary_text_sources_cover_early_late_and_certainty_readings(self):
        used_sources = {
            fixture["source_id"]
            for lesson in STAGE_G_CANDIDATE_LESSONS
            for fixture in lesson["reading_fixtures"]
        }
        self.assertTrue(
            {
                "wittgenstein-tractatus",
                "wittgenstein-blue-book",
                "wittgenstein-investigations",
                "wittgenstein-on-certainty",
            }.issubset(used_sources)
        )

    def test_live_course_count_and_data_remain_unchanged(self):
        self.assertEqual(len(VISIBLE_LOGIC_LESSONS), 45)
        self.assertFalse(
            {lesson["slug"] for lesson in STAGE_G_CANDIDATE_LESSONS}
            & {lesson["slug"] for lesson in VISIBLE_LOGIC_LESSONS}
        )

    @staticmethod
    def _lesson_text(lesson):
        parts = []

        def collect(value):
            if isinstance(value, str):
                parts.append(value)
            elif isinstance(value, dict):
                for nested in value.values():
                    collect(nested)
            elif isinstance(value, (list, tuple)):
                for nested in value:
                    collect(nested)

        collect(lesson)
        return " ".join(parts)


class LogicPhase3StageGPreviewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.staff_user = user_model.objects.create_user(
            username="logic-stage-g-reviewer",
            password="review-pass",
            is_staff=True,
        )
        cls.regular_user = user_model.objects.create_user(
            username="logic-stage-g-student",
            password="student-pass",
        )

    def test_preview_requires_staff_access(self):
        url = reverse("logic_stage_g_preview")
        anonymous_response = self.client.get(url)
        self.assertEqual(anonymous_response.status_code, 302)
        self.assertIn(reverse("admin:login"), anonymous_response.url)

        self.client.force_login(self.regular_user)
        regular_response = self.client.get(url)
        self.assertEqual(regular_response.status_code, 302)
        self.assertIn(reverse("admin:login"), regular_response.url)

    def test_staff_preview_renders_lessons_readings_and_comparisons(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("logic_stage_g_preview"))
        rendered_text = unescape(response.content.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/logic_stage_a_preview.html")
        self.assertIn(
            "Faz 3G: Frege, Russell ve Wittgenstein okuma köprüsü",
            rendered_text,
        )
        self.assertIn("noindex, nofollow", rendered_text)
        for lesson in STAGE_G_CANDIDATE_LESSONS:
            self.assertIn(lesson["curriculum_id"], rendered_text)
            self.assertIn(lesson["title"], rendered_text)
            for fixture in lesson["reading_fixtures"]:
                self.assertIn(
                    f'data-reading-fixture="{fixture["id"]}"',
                    rendered_text,
                )
                self.assertIn(fixture["locator"], rendered_text)
                self.assertIn(
                    STAGE_G_SOURCE_REFERENCES[fixture["source_id"]]["url"],
                    rendered_text,
                )
            for fixture in lesson["comparison_fixtures"]:
                self.assertIn(
                    f'data-comparison-fixture="{fixture["id"]}"',
                    rendered_text,
                )

    def test_preview_is_read_only_and_candidates_stay_off_learner_routes(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("logic_stage_g_preview"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LogicLessonProgress.objects.count(), 0)
        self.assertNotContains(response, "data-logic-lesson-page")
        self.assertNotContains(response, "data-progress-url")
        self.assertNotContains(response, reverse("logic_lesson_progress"))
        self.assertNotContains(response, "logic_lesson.js")

        self.client.force_login(self.regular_user)
        for lesson in STAGE_G_CANDIDATE_LESSONS:
            response = self.client.get(
                reverse(
                    "logic_lesson_detail",
                    kwargs={"lesson_slug": lesson["slug"]},
                )
            )
            self.assertEqual(response.status_code, 404)
