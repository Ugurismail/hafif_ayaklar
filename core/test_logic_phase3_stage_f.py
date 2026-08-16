from django.test import SimpleTestCase

from .logic_course_data import VISIBLE_LOGIC_LESSONS
from .logic_fol import signature_from_data
from .logic_fol_semantics import (
    analyze_binary_relation,
    evaluate_fol,
    evaluation_trace,
    interpretation_from_data,
    search_countermodel,
)
from .logic_phase3_stage_a import STAGE_A_CANDIDATE_MAP
from .logic_phase3_stage_b import STAGE_B_CANDIDATE_MAP
from .logic_phase3_stage_c import STAGE_C_CANDIDATE_MAP
from .logic_phase3_stage_d import STAGE_D_CANDIDATE_MAP
from .logic_phase3_stage_e import STAGE_E_CANDIDATE_MAP
from .logic_phase3_stage_f import (
    STAGE_F_CANDIDATE_LESSONS,
    STAGE_F_CANDIDATE_MAP,
    STAGE_F_SOURCE_REFERENCES,
)


class LogicPhase3StageFCandidateTests(SimpleTestCase):
    def test_stage_f_current_candidates_are_contiguous_and_isolated(self):
        self.assertEqual(
            [lesson["curriculum_id"] for lesson in STAGE_F_CANDIDATE_LESSONS],
            ["F35", "F36", "F37"],
        )
        self.assertEqual(
            [lesson["order"] for lesson in STAGE_F_CANDIDATE_LESSONS],
            [35, 36, 37],
        )
        visible_slugs = {lesson["slug"] for lesson in VISIBLE_LOGIC_LESSONS}
        self.assertTrue(set(STAGE_F_CANDIDATE_MAP).isdisjoint(visible_slugs))

    def test_every_candidate_has_complete_common_contract(self):
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
            "fol_signature",
        }
        all_candidates = {
            **STAGE_A_CANDIDATE_MAP,
            **STAGE_B_CANDIDATE_MAP,
            **STAGE_C_CANDIDATE_MAP,
            **STAGE_D_CANDIDATE_MAP,
            **STAGE_E_CANDIDATE_MAP,
            **STAGE_F_CANDIDATE_MAP,
        }

        for lesson in STAGE_F_CANDIDATE_LESSONS:
            with self.subTest(lesson=lesson["curriculum_id"]):
                self.assertTrue(required.issubset(lesson))
                self.assertEqual(lesson["release_status"], "candidate")
                self.assertGreaterEqual(len(lesson["sections"]), 6)
                self.assertGreaterEqual(len(lesson["worked_examples"]), 12)
                self.assertGreaterEqual(len(lesson["practice"]), 12)
                self.assertGreaterEqual(len(lesson["production_tasks"]), 2)
                self.assertGreaterEqual(len(lesson["mastery_evidence"]), 4)
                self.assertEqual(len(lesson["competencies"]), len(set(lesson["competencies"])))
                for prerequisite in lesson["prerequisites"]:
                    self.assertIn(prerequisite, all_candidates)
                    self.assertLess(all_candidates[prerequisite]["order"], lesson["order"])
                for source_id in lesson["source_ids"]:
                    self.assertIn(source_id, STAGE_F_SOURCE_REFERENCES)

    def test_f35_bridges_e34_and_f36_f37_form_a_chain(self):
        self.assertEqual(
            STAGE_F_CANDIDATE_LESSONS[0]["prerequisites"],
            ["ders-fol-belirsizlik-sembollestirme-atolyesi"],
        )
        self.assertEqual(
            STAGE_F_CANDIDATE_LESSONS[1]["prerequisites"],
            [STAGE_F_CANDIDATE_LESSONS[0]["slug"]],
        )
        self.assertEqual(
            STAGE_F_CANDIDATE_LESSONS[2]["prerequisites"],
            [STAGE_F_CANDIDATE_LESSONS[1]["slug"]],
        )

    def test_practice_answers_and_production_stimuli_are_auditable(self):
        for lesson in STAGE_F_CANDIDATE_LESSONS:
            for item in lesson["practice"]:
                with self.subTest(lesson=lesson["curriculum_id"], prompt=item["prompt"]):
                    self.assertIn(item["answer"], "ABCD")
                    self.assertEqual(len(item["choices"]), 4)
                    self.assertTrue(item["explanation"])
            for task in lesson["production_tasks"]:
                self.assertTrue(task["stimulus"]["label"])
                self.assertTrue(task["stimulus"]["items"])
                self.assertTrue(task["checkpoints"])

    def test_live_course_count_and_data_remain_unchanged(self):
        self.assertEqual(len(VISIBLE_LOGIC_LESSONS), 45)
        self.assertFalse(
            {lesson["slug"] for lesson in STAGE_F_CANDIDATE_LESSONS}
            & {lesson["slug"] for lesson in VISIBLE_LOGIC_LESSONS}
        )


class LogicPhase3F35SemanticFixtureTests(SimpleTestCase):
    def setUp(self):
        self.lesson = STAGE_F_CANDIDATE_LESSONS[0]
        self.signature = signature_from_data(self.lesson["fol_signature"])
        self.models = {
            data["label"]: interpretation_from_data(data, self.signature)
            for data in self.lesson["model_fixtures"]
        }

    def test_every_declared_truth_value_and_decisive_trace_is_computed(self):
        for fixture in self.lesson["semantic_fixtures"]:
            model = self.models[fixture["model"]]
            with self.subTest(fixture=fixture["id"]):
                result = evaluation_trace(
                    fixture["formula"],
                    model,
                    fixture["assignment"],
                )
                self.assertEqual(result["value"], fixture["expected"])
                self.assertEqual(
                    evaluate_fol(fixture["formula"], model, fixture["assignment"]),
                    fixture["expected"],
                )
                self.assertIn(
                    fixture["decisive_kind"],
                    result["steps"][-1]["detail"],
                )
                if "decisive_value" in fixture:
                    self.assertEqual(
                        result["steps"][-1]["detail"][fixture["decisive_kind"]],
                        fixture["decisive_value"],
                    )

    def test_f35_explicitly_teaches_open_formula_and_named_object_limits(self):
        text = " ".join(
            [
                self.lesson["summary"],
                self.lesson["rigor_note"],
                *self.lesson["mistakes"],
                *(section["summary"] for section in self.lesson["sections"]),
            ]
        )
        self.assertIn("Açık formül", text)
        self.assertIn("adı olmayan", text)
        self.assertIn("tek yorum", text)


class LogicPhase3F36CountermodelFixtureTests(SimpleTestCase):
    def setUp(self):
        self.lesson = STAGE_F_CANDIDATE_LESSONS[1]
        self.signature = signature_from_data(self.lesson["fol_signature"])

    def test_every_countermodel_fixture_has_the_declared_limited_result(self):
        for fixture in self.lesson["countermodel_fixtures"]:
            with self.subTest(fixture=fixture["id"]):
                result = search_countermodel(
                    fixture["premises"],
                    fixture["conclusion"],
                    fixture["models"],
                    self.signature,
                )
                self.assertEqual(result["status"], fixture["expected_status"])
                if result["status"] == "countermodel_found":
                    self.assertTrue(all(result["premise_values"]))
                    self.assertFalse(result["conclusion_value"])
                    self.assertFalse(result["entails"])
                else:
                    self.assertIsNone(result["entails"])
                    self.assertIn("geçerliliğini kanıtlamaz", result["warning"])

    def test_lesson_never_equates_failed_search_with_validity(self):
        text = " ".join(
            [
                self.lesson["summary"],
                self.lesson["rigor_note"],
                *self.lesson["mistakes"],
                *(item["reason"] for item in self.lesson["worked_examples"]),
            ]
        )
        self.assertIn("geçerlilik", text)
        self.assertIn("örneklem", text)
        self.assertIn("karşı model", text)


class LogicPhase3F37RelationFixtureTests(SimpleTestCase):
    def setUp(self):
        self.lesson = STAGE_F_CANDIDATE_LESSONS[2]
        self.signature = signature_from_data(self.lesson["fol_signature"])

    def test_every_relation_profile_is_recomputed(self):
        for fixture in self.lesson["relation_fixtures"]:
            model = interpretation_from_data(fixture["model"], self.signature)
            actual = analyze_binary_relation(model, "R")["properties"]
            with self.subTest(fixture=fixture["id"]):
                self.assertEqual(
                    {name: details["holds"] for name, details in actual.items()},
                    fixture["expected"],
                )
                for name, expected in fixture["expected"].items():
                    if not expected:
                        self.assertIsNotNone(actual[name]["counterexample"])

    def test_symmetry_family_and_reflexivity_family_are_not_collapsed(self):
        terms = {item["term"] for item in self.lesson["key_terms"]}
        self.assertTrue(
            {"Yansımalı", "Yansımasız", "Simetrik", "Asimetrik", "Ters-simetrik"}.issubset(terms)
        )
        mistake_text = " ".join(self.lesson["mistakes"])
        self.assertIn("Yansımalı değil", mistake_text)
        self.assertIn("Simetrik değil", mistake_text)
