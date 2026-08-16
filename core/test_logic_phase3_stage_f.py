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
from .logic_fol_fitch import F38_RULES, F39_RULES, F40_RULES, audit_fol_fitch_proof
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
            ["F35", "F36", "F37", "F38", "F39", "F40"],
        )
        self.assertEqual(
            [lesson["order"] for lesson in STAGE_F_CANDIDATE_LESSONS],
            [35, 36, 37, 38, 39, 40],
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

    def test_f35_bridges_e34_and_stage_f_forms_a_chain(self):
        self.assertEqual(
            STAGE_F_CANDIDATE_LESSONS[0]["prerequisites"],
            ["ders-fol-belirsizlik-sembollestirme-atolyesi"],
        )
        for previous, current in zip(
            STAGE_F_CANDIDATE_LESSONS,
            STAGE_F_CANDIDATE_LESSONS[1:],
        ):
            self.assertEqual(current["prerequisites"], [previous["slug"]])

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


class LogicPhase3F38ToF40ProofFixtureTests(SimpleTestCase):
    RULES = {
        "F38": F38_RULES,
        "F39": F39_RULES,
        "F40": F40_RULES,
    }

    def test_every_proof_fixture_is_recomputed_by_the_fol_auditor(self):
        for lesson in STAGE_F_CANDIDATE_LESSONS[3:6]:
            signature = signature_from_data(lesson["fol_signature"])
            for fixture in lesson["proof_fixtures"]:
                issues = audit_fol_fitch_proof(
                    fixture["proof"],
                    signature,
                    allowed_rules=self.RULES[lesson["curriculum_id"]],
                )
                actual_codes = {issue["code"] for issue in issues}
                with self.subTest(
                    lesson=lesson["curriculum_id"],
                    fixture=fixture["id"],
                ):
                    if fixture["kind"] == "valid":
                        self.assertEqual(issues, [])
                    else:
                        self.assertTrue(fixture["expected_codes"])
                        self.assertTrue(
                            set(fixture["expected_codes"]).issubset(actual_codes)
                        )

    def test_rule_availability_grows_without_removing_prior_rules(self):
        self.assertLess(F38_RULES, F39_RULES)
        self.assertLess(F39_RULES, F40_RULES)
        self.assertEqual(F39_RULES - F38_RULES, {"∀I", "∃E"})
        self.assertEqual(F40_RULES - F39_RULES, {"=I", "=E"})

    def test_eigenname_and_identity_limits_are_explicit_in_content(self):
        f39_text = " ".join(
            [
                STAGE_F_CANDIDATE_LESSONS[4]["summary"],
                STAGE_F_CANDIDATE_LESSONS[4]["rigor_note"],
                *STAGE_F_CANDIDATE_LESSONS[4]["mistakes"],
            ]
        )
        f40_text = " ".join(
            [
                STAGE_F_CANDIDATE_LESSONS[5]["summary"],
                STAGE_F_CANDIDATE_LESSONS[5]["rigor_note"],
                *STAGE_F_CANDIDATE_LESSONS[5]["mistakes"],
            ]
        )
        self.assertIn("bağımlılık", f39_text)
        self.assertIn("sonuç", f39_text)
        self.assertIn("seçili", f40_text)
        self.assertIn("bağlı değişken", f40_text.lower())
