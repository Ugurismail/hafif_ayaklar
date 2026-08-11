from copy import deepcopy

from django.test import SimpleTestCase

from .logic_course_data import VISIBLE_LOGIC_LESSONS
from .logic_fitch import D20_RULES, audit_fitch_proof
from .logic_phase3_stage_a import STAGE_A_CANDIDATE_MAP
from .logic_phase3_stage_b import STAGE_B_CANDIDATE_MAP
from .logic_phase3_stage_c import STAGE_C_CANDIDATE_MAP
from .logic_phase3_stage_d import (
    STAGE_D_CANDIDATE_LESSONS,
    STAGE_D_CANDIDATE_MAP,
    STAGE_D_SOURCE_REFERENCES,
)


class LogicPhase3StageDIntegrityTests(SimpleTestCase):
    common_required_fields = {
        "curriculum_id",
        "release_status",
        "order",
        "slug",
        "title",
        "summary",
        "focus",
        "duration",
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
        "next_step",
        "source_ids",
        "reading_note",
        "rigor_note",
        "symbol_set",
        "proof_tools",
        "legacy_sources",
        "rule_scope",
        "proof_fixtures",
    }

    def test_stage_d_starts_with_only_the_reviewed_d20_candidate(self):
        self.assertEqual(
            [lesson["curriculum_id"] for lesson in STAGE_D_CANDIDATE_LESSONS],
            ["D20"],
        )
        self.assertEqual(
            [lesson["order"] for lesson in STAGE_D_CANDIDATE_LESSONS],
            [20],
        )
        self.assertEqual(len(STAGE_D_CANDIDATE_MAP), 1)

    def test_d20_has_complete_candidate_fields_and_known_sources(self):
        lesson = STAGE_D_CANDIDATE_LESSONS[0]

        self.assertTrue(self.common_required_fields.issubset(lesson))
        self.assertEqual(lesson["release_status"], "candidate")
        self.assertEqual(
            lesson["duration"],
            f'{lesson["estimated_minutes"]} dk',
        )
        self.assertTrue(lesson["source_ids"])
        self.assertTrue(
            set(lesson["source_ids"]).issubset(STAGE_D_SOURCE_REFERENCES)
        )

    def test_d20_prerequisites_exist_and_point_backwards(self):
        all_candidates = {
            **STAGE_A_CANDIDATE_MAP,
            **STAGE_B_CANDIDATE_MAP,
            **STAGE_C_CANDIDATE_MAP,
            **STAGE_D_CANDIDATE_MAP,
        }
        lesson = STAGE_D_CANDIDATE_LESSONS[0]

        for prerequisite in lesson["prerequisites"]:
            with self.subTest(prerequisite=prerequisite):
                self.assertIn(prerequisite, all_candidates)
                self.assertLess(
                    all_candidates[prerequisite]["order"],
                    lesson["order"],
                )

    def test_d20_remains_isolated_from_the_learner_course(self):
        visible_slugs = {lesson["slug"] for lesson in VISIBLE_LOGIC_LESSONS}
        candidate_slugs = {
            lesson["slug"] for lesson in STAGE_D_CANDIDATE_LESSONS
        }

        self.assertTrue(candidate_slugs.isdisjoint(visible_slugs))

    def test_d20_has_sufficient_teaching_and_assessment_depth(self):
        lesson = STAGE_D_CANDIDATE_LESSONS[0]

        self.assertGreaterEqual(len(lesson["sections"]), 5)
        self.assertGreaterEqual(len(lesson["worked_examples"]), 6)
        self.assertGreaterEqual(len(lesson["practice"]), 10)
        self.assertGreaterEqual(len(lesson["production_tasks"]), 1)
        self.assertGreaterEqual(len(lesson["mastery_evidence"]), 5)
        self.assertEqual(
            set(lesson["rule_scope"]["introduced"]),
            D20_RULES,
        )
        self.assertTrue(
            D20_RULES.isdisjoint(
                lesson["rule_scope"]["locked_until_later"]
            )
        )

    def test_d20_includes_complete_incomplete_and_error_fixtures(self):
        lesson = STAGE_D_CANDIDATE_LESSONS[0]

        self.assertEqual(
            {fixture["kind"] for fixture in lesson["proof_fixtures"]},
            {"complete", "incomplete", "error"},
        )
        for fixture in lesson["proof_fixtures"]:
            with self.subTest(fixture=fixture["id"]):
                self.assertEqual(fixture["id"], fixture["proof"]["id"])
                self.assertTrue(fixture["proof"]["lines"])
                self.assertIn("expected_issue_codes", fixture)


class FitchProofAuditTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.lesson = STAGE_D_CANDIDATE_LESSONS[0]
        cls.fixtures = {
            fixture["kind"]: fixture
            for fixture in cls.lesson["proof_fixtures"]
        }

    def test_complete_fixture_passes_every_d20_check(self):
        fixture = self.fixtures["complete"]

        self.assertEqual(
            audit_fitch_proof(fixture["proof"]),
            [],
        )

    def test_incomplete_fixture_is_valid_as_an_open_working_draft(self):
        fixture = self.fixtures["incomplete"]

        self.assertEqual(
            audit_fitch_proof(
                fixture["proof"],
                require_complete=False,
            ),
            [],
        )
        completion_codes = {
            issue["code"]
            for issue in audit_fitch_proof(fixture["proof"])
        }
        self.assertEqual(
            completion_codes,
            {
                "proof.scope_unclosed",
                "proof.target_in_subproof",
                "proof.target_not_reached",
            },
        )

    def test_error_fixture_identifies_the_closed_scope_reference(self):
        fixture = self.fixtures["error"]
        issues = audit_fitch_proof(fixture["proof"])

        self.assertEqual(
            [issue["code"] for issue in issues],
            fixture["expected_issue_codes"],
        )
        self.assertEqual(issues[0]["line_id"], "l4")

    def test_reiteration_requires_exact_formula_identity(self):
        proof = {
            "id": "reiteration-mismatch",
            "premises": ["A"],
            "target": "¬¬A",
            "lines": [
                {
                    "id": "l1",
                    "formula": "A",
                    "rule": "PR",
                    "citations": [],
                    "depth": 0,
                    "opens": None,
                    "closes": [],
                },
                {
                    "id": "l2",
                    "formula": "¬¬A",
                    "rule": "R",
                    "citations": [{"kind": "line", "id": "l1"}],
                    "depth": 0,
                    "opens": None,
                    "closes": [],
                },
            ],
        }

        codes = [issue["code"] for issue in audit_fitch_proof(proof)]
        self.assertEqual(codes, ["rule.r_formula_mismatch"])

    def test_forward_and_unknown_citations_are_distinguished(self):
        proof = {
            "id": "forward-reference",
            "premises": ["A"],
            "target": "A",
            "lines": [
                {
                    "id": "l1",
                    "formula": "A",
                    "rule": "R",
                    "citations": [{"kind": "line", "id": "l2"}],
                    "depth": 0,
                    "opens": None,
                    "closes": [],
                },
                {
                    "id": "l2",
                    "formula": "A",
                    "rule": "PR",
                    "citations": [],
                    "depth": 0,
                    "opens": None,
                    "closes": [],
                },
                {
                    "id": "l3",
                    "formula": "A",
                    "rule": "R",
                    "citations": [{"kind": "line", "id": "missing"}],
                    "depth": 0,
                    "opens": None,
                    "closes": [],
                },
            ],
        }

        codes = [
            issue["code"]
            for issue in audit_fitch_proof(proof)
            if issue["code"].startswith("citation.")
        ]
        self.assertEqual(codes, ["citation.forward", "citation.unknown"])

    def test_scope_depth_is_derived_from_open_scope_stack(self):
        proof = deepcopy(self.fixtures["complete"]["proof"])
        proof["lines"][2]["depth"] = 0

        issues = audit_fitch_proof(proof)

        self.assertIn(
            ("line.depth_mismatch", "l3"),
            {(issue["code"], issue["line_id"]) for issue in issues},
        )

    def test_rules_locked_until_later_are_rejected_in_d20(self):
        proof = {
            "id": "early-rule",
            "premises": ["A", "B"],
            "target": "A ∧ B",
            "lines": [
                {
                    "id": "l1",
                    "formula": "A",
                    "rule": "PR",
                    "citations": [],
                    "depth": 0,
                    "opens": None,
                    "closes": [],
                },
                {
                    "id": "l2",
                    "formula": "B",
                    "rule": "PR",
                    "citations": [],
                    "depth": 0,
                    "opens": None,
                    "closes": [],
                },
                {
                    "id": "l3",
                    "formula": "A ∧ B",
                    "rule": "∧I",
                    "citations": [
                        {"kind": "line", "id": "l1"},
                        {"kind": "line", "id": "l2"},
                    ],
                    "depth": 0,
                    "opens": None,
                    "closes": [],
                },
            ],
        }

        self.assertIn(
            "rule.not_available",
            [issue["code"] for issue in audit_fitch_proof(proof)],
        )

    def test_premise_lines_must_come_from_the_problem(self):
        proof = {
            "id": "invented-premise",
            "premises": ["A"],
            "target": "B",
            "lines": [
                {
                    "id": "l1",
                    "formula": "B",
                    "rule": "PR",
                    "citations": [],
                    "depth": 0,
                    "opens": None,
                    "closes": [],
                }
            ],
        }

        self.assertEqual(
            [issue["code"] for issue in audit_fitch_proof(proof)],
            ["rule.pr_not_premise"],
        )

    def test_premise_rule_cannot_be_used_inside_a_subproof(self):
        proof = {
            "id": "nested-premise",
            "premises": ["A"],
            "target": "A",
            "lines": [
                {
                    "id": "l1",
                    "formula": "B",
                    "rule": "AS",
                    "citations": [],
                    "depth": 1,
                    "opens": "s1",
                    "closes": [],
                },
                {
                    "id": "l2",
                    "formula": "A",
                    "rule": "PR",
                    "citations": [],
                    "depth": 1,
                    "opens": None,
                    "closes": [],
                },
            ],
        }

        self.assertIn(
            "rule.pr_not_root",
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    proof,
                    require_complete=False,
                )
            ],
        )

    def test_stable_line_ids_survive_inserting_an_unrelated_line(self):
        proof = deepcopy(self.fixtures["complete"]["proof"])
        proof["lines"].insert(
            1,
            {
                "id": "l1a",
                "formula": "A",
                "rule": "R",
                "citations": [{"kind": "line", "id": "l1"}],
                "depth": 0,
                "opens": None,
                "closes": [],
            },
        )

        self.assertEqual(audit_fitch_proof(proof), [])

    def test_invalid_formula_is_reported_without_crashing_the_audit(self):
        proof = deepcopy(self.fixtures["complete"]["proof"])
        proof["lines"][0]["formula"] = "A ∧"

        issues = audit_fitch_proof(proof)

        self.assertIn(
            ("formula.invalid", "l1"),
            {(issue["code"], issue["line_id"]) for issue in issues},
        )
