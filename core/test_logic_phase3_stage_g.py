from django.test import SimpleTestCase

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


class LogicPhase3StageGCandidateTests(SimpleTestCase):
    def test_current_frege_russell_candidates_are_contiguous_and_isolated(self):
        self.assertEqual(
            [lesson["curriculum_id"] for lesson in STAGE_G_CANDIDATE_LESSONS],
            ["G42", "G43", "G44", "G45"],
        )
        self.assertEqual(
            [lesson["order"] for lesson in STAGE_G_CANDIDATE_LESSONS],
            [42, 43, 44, 45],
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

    def test_live_course_count_and_data_remain_unchanged(self):
        self.assertEqual(len(VISIBLE_LOGIC_LESSONS), 45)
        self.assertFalse(
            {lesson["slug"] for lesson in STAGE_G_CANDIDATE_LESSONS}
            & {lesson["slug"] for lesson in VISIBLE_LOGIC_LESSONS}
        )

    @staticmethod
    def _lesson_text(lesson):
        parts = [
            lesson["summary"],
            lesson["rigor_note"],
            *lesson["mistakes"],
            *(section["summary"] for section in lesson["sections"]),
            *(item["reason"] for item in lesson["worked_examples"]),
            *(fixture["boundary"] for fixture in lesson["reading_fixtures"]),
        ]
        return " ".join(parts)
