from copy import deepcopy

from django.test import SimpleTestCase

from .logic_course_data import VISIBLE_LOGIC_LESSONS
from .logic_fitch import (
    D20_RULES,
    D21_RULES,
    D22_RULES,
    D23_RULES,
    D24_RULES,
    D25_RULES,
    audit_fitch_proof,
)
from .logic_phase3_stage_a import STAGE_A_CANDIDATE_MAP
from .logic_phase3_stage_b import STAGE_B_CANDIDATE_MAP
from .logic_phase3_stage_c import STAGE_C_CANDIDATE_MAP
from .logic_phase3_stage_d import (
    STAGE_D_CANDIDATE_LESSONS,
    STAGE_D_CANDIDATE_MAP,
    STAGE_D_SOURCE_REFERENCES,
)


def _proof_line(
    line_id,
    formula,
    rule,
    *,
    citations=None,
    depth=0,
    opens=None,
    closes=None,
):
    return {
        "id": line_id,
        "formula": formula,
        "rule": rule,
        "citations": citations or [],
        "depth": depth,
        "opens": opens,
        "closes": closes or [],
    }


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

    def test_stage_d_contains_only_the_reviewed_candidates_in_order(self):
        self.assertEqual(
            [lesson["curriculum_id"] for lesson in STAGE_D_CANDIDATE_LESSONS],
            ["D20", "D21", "D22", "D23", "D24", "D25"],
        )
        self.assertEqual(
            [lesson["order"] for lesson in STAGE_D_CANDIDATE_LESSONS],
            [20, 21, 22, 23, 24, 25],
        )
        self.assertEqual(len(STAGE_D_CANDIDATE_MAP), 6)

    def test_stage_d_candidates_have_complete_fields_and_known_sources(self):
        for lesson in STAGE_D_CANDIDATE_LESSONS:
            with self.subTest(lesson=lesson["curriculum_id"]):
                self.assertTrue(self.common_required_fields.issubset(lesson))
                self.assertEqual(lesson["release_status"], "candidate")
                self.assertEqual(
                    lesson["duration"],
                    f'{lesson["estimated_minutes"]} dk',
                )
                self.assertTrue(lesson["source_ids"])
                self.assertTrue(
                    set(lesson["source_ids"]).issubset(
                        STAGE_D_SOURCE_REFERENCES
                    )
                )

    def test_stage_d_prerequisites_exist_and_point_backwards(self):
        all_candidates = {
            **STAGE_A_CANDIDATE_MAP,
            **STAGE_B_CANDIDATE_MAP,
            **STAGE_C_CANDIDATE_MAP,
            **STAGE_D_CANDIDATE_MAP,
        }
        for lesson in STAGE_D_CANDIDATE_LESSONS:
            for prerequisite in lesson["prerequisites"]:
                with self.subTest(
                    lesson=lesson["curriculum_id"],
                    prerequisite=prerequisite,
                ):
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

    def test_d21_has_rule_scope_depth_and_all_fixture_kinds(self):
        lesson = STAGE_D_CANDIDATE_LESSONS[1]

        self.assertGreaterEqual(len(lesson["sections"]), 5)
        self.assertGreaterEqual(len(lesson["worked_examples"]), 7)
        self.assertGreaterEqual(len(lesson["practice"]), 12)
        self.assertEqual(
            set(lesson["rule_scope"]["introduced"]),
            {"∧I", "∧E", "→I", "→E"},
        )
        self.assertEqual(
            set(lesson["rule_scope"]["review_only"]),
            D20_RULES,
        )
        self.assertEqual(
            {fixture["kind"] for fixture in lesson["proof_fixtures"]},
            {"complete", "incomplete", "error"},
        )

    def test_d22_has_rule_scope_depth_and_all_fixture_kinds(self):
        lesson = STAGE_D_CANDIDATE_LESSONS[2]

        self.assertGreaterEqual(len(lesson["sections"]), 6)
        self.assertGreaterEqual(len(lesson["worked_examples"]), 8)
        self.assertGreaterEqual(len(lesson["practice"]), 12)
        self.assertEqual(
            set(lesson["rule_scope"]["introduced"]),
            {"¬I", "¬E", "X", "IP"},
        )
        self.assertEqual(
            set(lesson["rule_scope"]["review_only"]),
            D21_RULES,
        )
        self.assertEqual(
            {fixture["kind"] for fixture in lesson["proof_fixtures"]},
            {"complete", "incomplete", "error"},
        )

    def test_d23_has_rule_scope_depth_and_all_fixture_kinds(self):
        lesson = STAGE_D_CANDIDATE_LESSONS[3]

        self.assertGreaterEqual(len(lesson["sections"]), 6)
        self.assertGreaterEqual(len(lesson["worked_examples"]), 8)
        self.assertGreaterEqual(len(lesson["practice"]), 12)
        self.assertEqual(
            set(lesson["rule_scope"]["introduced"]),
            {"∨I", "∨E", "↔I", "↔E"},
        )
        self.assertEqual(
            set(lesson["rule_scope"]["review_only"]),
            D22_RULES,
        )
        self.assertEqual(
            {fixture["kind"] for fixture in lesson["proof_fixtures"]},
            {"complete", "incomplete", "error"},
        )

    def test_d24_adds_strategy_depth_without_unlocking_a_new_rule(self):
        lesson = STAGE_D_CANDIDATE_LESSONS[4]

        self.assertGreaterEqual(len(lesson["sections"]), 6)
        self.assertGreaterEqual(len(lesson["worked_examples"]), 8)
        self.assertGreaterEqual(len(lesson["practice"]), 12)
        self.assertEqual(lesson["rule_scope"]["introduced"], [])
        self.assertEqual(
            set(lesson["rule_scope"]["review_only"]),
            D24_RULES,
        )
        self.assertEqual(D24_RULES, D23_RULES)
        self.assertEqual(
            {fixture["kind"] for fixture in lesson["proof_fixtures"]},
            {"complete", "incomplete", "error"},
        )

    def test_d24_strategy_cases_are_structured_and_linked_to_fixtures(self):
        lesson = STAGE_D_CANDIDATE_LESSONS[4]
        required_fields = {
            "id",
            "problem",
            "backward_goal",
            "candidate_last_rules",
            "forward_resources",
            "bridge",
            "scope_plan",
            "first_action",
            "rationale",
        }
        strategy_ids = {case["id"] for case in lesson["strategy_cases"]}

        self.assertGreaterEqual(len(strategy_ids), 5)
        self.assertEqual(len(strategy_ids), len(lesson["strategy_cases"]))
        for case in lesson["strategy_cases"]:
            with self.subTest(case=case["id"]):
                self.assertTrue(required_fields.issubset(case))
                self.assertTrue(case["candidate_last_rules"])
                self.assertTrue(case["forward_resources"])
                self.assertTrue(case["bridge"])
                self.assertTrue(case["rationale"])

        for fixture in lesson["proof_fixtures"]:
            with self.subTest(fixture=fixture["id"]):
                self.assertIn(fixture["strategy_case_id"], strategy_ids)

    def test_d25_has_derived_rule_depth_and_auditable_expansions(self):
        lesson = STAGE_D_CANDIDATE_LESSONS[5]

        self.assertGreaterEqual(len(lesson["sections"]), 6)
        self.assertGreaterEqual(len(lesson["worked_examples"]), 8)
        self.assertGreaterEqual(len(lesson["practice"]), 12)
        self.assertEqual(
            set(lesson["rule_scope"]["introduced"]),
            {"DS", "MT", "DNE", "LEM", "DeM"},
        )
        self.assertEqual(
            set(lesson["rule_scope"]["review_only"]),
            D24_RULES,
        )
        self.assertEqual(
            D25_RULES,
            D24_RULES | {"DS", "MT", "DNE", "LEM", "DeM"},
        )
        self.assertEqual(
            {fixture["kind"] for fixture in lesson["proof_fixtures"]},
            {"complete", "incomplete", "error"},
        )

        expansions = {
            expansion["rule"]: expansion
            for expansion in lesson["derived_rule_expansions"]
        }
        self.assertEqual(set(expansions), {"DS", "MT", "DNE"})
        for expansion in expansions.values():
            with self.subTest(rule=expansion["rule"]):
                self.assertTrue(expansion["basic_rules"])
                self.assertEqual(
                    set(expansion["preserves"]),
                    {"premises", "target", "open assumptions"},
                )

        self.assertFalse(expansions["DS"]["classical_dependency"])
        self.assertFalse(expansions["MT"]["classical_dependency"])
        self.assertTrue(expansions["DNE"]["classical_dependency"])


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


class D21RuleAuditTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.lesson = STAGE_D_CANDIDATE_LESSONS[1]
        cls.fixtures = {
            fixture["id"]: fixture
            for fixture in cls.lesson["proof_fixtures"]
        }

    def test_complete_d21_fixtures_pass_the_expanded_rule_set(self):
        complete_fixtures = [
            fixture
            for fixture in self.lesson["proof_fixtures"]
            if fixture["kind"] == "complete"
        ]

        for fixture in complete_fixtures:
            with self.subTest(fixture=fixture["id"]):
                self.assertEqual(
                    audit_fitch_proof(
                        fixture["proof"],
                        allowed_rules=D21_RULES,
                    ),
                    [],
                )

    def test_d21_incomplete_fixture_is_valid_before_conditional_closure(self):
        fixture = self.fixtures["d21-incomplete-conditional"]

        self.assertEqual(
            audit_fitch_proof(
                fixture["proof"],
                allowed_rules=D21_RULES,
                require_complete=False,
            ),
            [],
        )
        self.assertEqual(
            {
                issue["code"]
                for issue in audit_fitch_proof(
                    fixture["proof"],
                    allowed_rules=D21_RULES,
                )
            },
            {
                "proof.scope_unclosed",
                "proof.target_in_subproof",
                "proof.target_not_reached",
            },
        )

    def test_d21_error_fixture_detects_swapped_conditional_sides(self):
        fixture = self.fixtures["d21-swapped-conditional-range"]

        self.assertEqual(
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    fixture["proof"],
                    allowed_rules=D21_RULES,
                )
            ],
            fixture["expected_issue_codes"],
        )

    def test_conjunction_introduction_preserves_component_order(self):
        proof = deepcopy(
            self.fixtures["d21-complete-rule-chain"]["proof"]
        )
        proof["lines"][-1]["citations"] = [
            {"kind": "line", "id": "l3"},
            {"kind": "line", "id": "l6"},
        ]

        self.assertIn(
            "rule.conjunction_introduction_mismatch",
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    proof,
                    allowed_rules=D21_RULES,
                )
            ],
        )

    def test_conjunction_elimination_only_returns_a_direct_component(self):
        proof = {
            "id": "nested-conjunction",
            "premises": ["A ∧ (B ∧ C)"],
            "target": "C",
            "lines": [
                {
                    "id": "l1",
                    "formula": "A ∧ (B ∧ C)",
                    "rule": "PR",
                    "citations": [],
                    "depth": 0,
                    "opens": None,
                    "closes": [],
                },
                {
                    "id": "l2",
                    "formula": "C",
                    "rule": "∧E",
                    "citations": [{"kind": "line", "id": "l1"}],
                    "depth": 0,
                    "opens": None,
                    "closes": [],
                },
            ],
        }

        self.assertEqual(
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    proof,
                    allowed_rules=D21_RULES,
                )
            ],
            ["rule.conjunction_elimination_mismatch"],
        )

    def test_conditional_elimination_accepts_either_citation_order(self):
        fixture = self.fixtures["d21-complete-rule-chain"]
        line_six = fixture["proof"]["lines"][5]

        self.assertEqual(line_six["rule"], "→E")
        self.assertEqual(
            line_six["citations"],
            [
                {"kind": "line", "id": "l4"},
                {"kind": "line", "id": "l5"},
            ],
        )
        self.assertEqual(
            audit_fitch_proof(
                fixture["proof"],
                allowed_rules=D21_RULES,
            ),
            [],
        )

    def test_conditional_elimination_rejects_affirming_the_consequent(self):
        proof = {
            "id": "affirming-consequent",
            "premises": ["A → B", "B"],
            "target": "A",
            "lines": [
                {
                    "id": "l1",
                    "formula": "A → B",
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
                    "formula": "A",
                    "rule": "→E",
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

        self.assertEqual(
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    proof,
                    allowed_rules=D21_RULES,
                )
            ],
            ["rule.conditional_elimination_mismatch"],
        )

    def test_conditional_introduction_requires_a_closed_subproof(self):
        proof = {
            "id": "open-subproof-citation",
            "premises": ["A"],
            "target": "B → A",
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
                    "rule": "AS",
                    "citations": [],
                    "depth": 1,
                    "opens": "s1",
                    "closes": [],
                },
                {
                    "id": "l3",
                    "formula": "A",
                    "rule": "R",
                    "citations": [{"kind": "line", "id": "l1"}],
                    "depth": 1,
                    "opens": None,
                    "closes": [],
                },
                {
                    "id": "l4",
                    "formula": "B → A",
                    "rule": "→I",
                    "citations": [
                        {"kind": "subproof", "start": "l2", "end": "l3"}
                    ],
                    "depth": 1,
                    "opens": None,
                    "closes": [],
                },
            ],
        }

        self.assertIn(
            "citation.subproof_open",
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    proof,
                    allowed_rules=D21_RULES,
                    require_complete=False,
                )
            ],
        )

    def test_subproof_reference_must_end_on_its_last_direct_line(self):
        proof = deepcopy(
            self.fixtures["d21-complete-conditional-introduction"]["proof"]
        )
        proof["lines"].insert(
            3,
            {
                "id": "l3a",
                "formula": "B",
                "rule": "R",
                "citations": [{"kind": "line", "id": "l2"}],
                "depth": 1,
                "opens": None,
                "closes": [],
            },
        )

        self.assertIn(
            "citation.subproof_end_not_last",
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    proof,
                    allowed_rules=D21_RULES,
                )
            ],
        )


class D22RuleAuditTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.lesson = STAGE_D_CANDIDATE_LESSONS[2]
        cls.fixtures = {
            fixture["id"]: fixture
            for fixture in cls.lesson["proof_fixtures"]
        }

    def test_complete_d22_fixtures_pass_the_expanded_rule_set(self):
        for fixture in self.lesson["proof_fixtures"]:
            if fixture["kind"] != "complete":
                continue
            with self.subTest(fixture=fixture["id"]):
                self.assertEqual(
                    audit_fitch_proof(
                        fixture["proof"],
                        allowed_rules=D22_RULES,
                    ),
                    [],
                )

    def test_d22_incomplete_fixture_is_valid_before_negation_closure(self):
        fixture = self.fixtures["d22-incomplete-negation-introduction"]

        self.assertEqual(
            audit_fitch_proof(
                fixture["proof"],
                allowed_rules=D22_RULES,
                require_complete=False,
            ),
            [],
        )
        self.assertEqual(
            {
                issue["code"]
                for issue in audit_fitch_proof(
                    fixture["proof"],
                    allowed_rules=D22_RULES,
                )
            },
            {
                "proof.scope_unclosed",
                "proof.target_in_subproof",
                "proof.target_not_reached",
            },
        )

    def test_error_fixture_rejects_different_atoms_as_a_contradiction(self):
        fixture = self.fixtures["d22-false-contradiction"]

        self.assertEqual(
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    fixture["proof"],
                    allowed_rules=D22_RULES,
                )
            ],
            fixture["expected_issue_codes"],
        )

    def test_negation_elimination_accepts_compound_formulas_in_either_order(self):
        for citations in (
            [
                {"kind": "line", "id": "l1"},
                {"kind": "line", "id": "l2"},
            ],
            [
                {"kind": "line", "id": "l2"},
                {"kind": "line", "id": "l1"},
            ],
        ):
            proof = {
                "id": "compound-contradiction",
                "premises": ["A ∧ B", "¬(A ∧ B)"],
                "target": "⊥",
                "lines": [
                    _proof_line("l1", "A ∧ B", "PR"),
                    _proof_line("l2", "¬(A ∧ B)", "PR"),
                    _proof_line(
                        "l3",
                        "⊥",
                        "¬E",
                        citations=citations,
                    ),
                ],
            }

            with self.subTest(citations=citations):
                self.assertEqual(
                    audit_fitch_proof(proof, allowed_rules=D22_RULES),
                    [],
                )

    def test_negation_elimination_can_only_conclude_bottom(self):
        proof = deepcopy(self.fixtures["d22-complete-explosion"]["proof"])
        proof["target"] = "C"
        proof["lines"][2]["formula"] = "C"
        proof["lines"] = proof["lines"][:3]

        self.assertEqual(
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    proof,
                    allowed_rules=D22_RULES,
                )
            ],
            ["rule.negation_elimination_conclusion"],
        )

    def test_negation_introduction_requires_assumption_then_bottom(self):
        proof = deepcopy(
            self.fixtures["d22-complete-negation-introduction"]["proof"]
        )
        proof["lines"][-1]["formula"] = "¬B"
        proof["target"] = "¬B"

        self.assertIn(
            "rule.negation_introduction_mismatch",
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    proof,
                    allowed_rules=D22_RULES,
                )
            ],
        )

    def test_indirect_proof_requires_the_targets_exact_negation(self):
        proof = deepcopy(
            self.fixtures["d22-complete-indirect-proof"]["proof"]
        )
        proof["lines"][-1]["formula"] = "B"
        proof["target"] = "B"

        self.assertEqual(
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    proof,
                    allowed_rules=D22_RULES,
                )
            ],
            ["rule.indirect_proof_mismatch"],
        )

    def test_explosion_requires_an_accessible_bottom_line(self):
        proof = {
            "id": "explosion-without-bottom",
            "premises": ["A"],
            "target": "C",
            "lines": [
                _proof_line("l1", "A", "PR"),
                _proof_line(
                    "l2",
                    "C",
                    "X",
                    citations=[{"kind": "line", "id": "l1"}],
                ),
            ],
        }

        self.assertEqual(
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    proof,
                    allowed_rules=D22_RULES,
                )
            ],
            ["rule.explosion_source"],
        )

    def test_explosion_cannot_reach_into_a_closed_subproof(self):
        proof = {
            "id": "closed-bottom",
            "premises": ["A", "¬A"],
            "target": "C",
            "lines": [
                _proof_line("l1", "A", "PR"),
                _proof_line("l2", "¬A", "PR"),
                _proof_line(
                    "l3",
                    "B",
                    "AS",
                    depth=1,
                    opens="s1",
                ),
                _proof_line(
                    "l4",
                    "⊥",
                    "¬E",
                    citations=[
                        {"kind": "line", "id": "l1"},
                        {"kind": "line", "id": "l2"},
                    ],
                    depth=1,
                ),
                _proof_line(
                    "l5",
                    "¬B",
                    "¬I",
                    citations=[
                        {"kind": "subproof", "start": "l3", "end": "l4"}
                    ],
                    closes=["s1"],
                ),
                _proof_line(
                    "l6",
                    "C",
                    "X",
                    citations=[{"kind": "line", "id": "l4"}],
                ),
            ],
        }

        self.assertIn(
            "citation.inaccessible",
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    proof,
                    allowed_rules=D22_RULES,
                )
            ],
        )


class D23RuleAuditTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.lesson = STAGE_D_CANDIDATE_LESSONS[3]
        cls.fixtures = {
            fixture["id"]: fixture
            for fixture in cls.lesson["proof_fixtures"]
        }

    def test_complete_d23_fixtures_pass_the_expanded_rule_set(self):
        for fixture in self.lesson["proof_fixtures"]:
            if fixture["kind"] != "complete":
                continue
            with self.subTest(fixture=fixture["id"]):
                self.assertEqual(
                    audit_fitch_proof(
                        fixture["proof"],
                        allowed_rules=D23_RULES,
                    ),
                    [],
                )

    def test_d23_incomplete_fixture_is_valid_before_second_case(self):
        fixture = self.fixtures["d23-incomplete-disjunction-elimination"]

        self.assertEqual(
            audit_fitch_proof(
                fixture["proof"],
                allowed_rules=D23_RULES,
                require_complete=False,
            ),
            [],
        )
        self.assertEqual(
            {
                issue["code"]
                for issue in audit_fitch_proof(
                    fixture["proof"],
                    allowed_rules=D23_RULES,
                )
            },
            {
                "proof.scope_unclosed",
                "proof.target_in_subproof",
            },
        )

    def test_error_fixture_rejects_different_case_results(self):
        fixture = self.fixtures["d23-different-branch-results"]

        self.assertEqual(
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    fixture["proof"],
                    allowed_rules=D23_RULES,
                )
            ],
            fixture["expected_issue_codes"],
        )

    def test_disjunction_introduction_requires_a_direct_disjunct(self):
        proof = {
            "id": "nested-disjunction-introduction",
            "premises": ["A"],
            "target": "(A ∧ B) ∨ C",
            "lines": [
                _proof_line("l1", "A", "PR"),
                _proof_line(
                    "l2",
                    "(A ∧ B) ∨ C",
                    "∨I",
                    citations=[{"kind": "line", "id": "l1"}],
                ),
            ],
        }

        self.assertEqual(
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    proof,
                    allowed_rules=D23_RULES,
                )
            ],
            ["rule.disjunction_introduction_mismatch"],
        )

    def test_disjunction_elimination_uses_the_two_direct_disjuncts(self):
        proof = {
            "id": "wrong-case-assumptions",
            "premises": ["A ∨ B", "C"],
            "target": "C",
            "lines": [
                _proof_line("l1", "A ∨ B", "PR"),
                _proof_line("l2", "C", "PR"),
                _proof_line("l3", "A", "AS", depth=1, opens="s1"),
                _proof_line(
                    "l4",
                    "C",
                    "R",
                    citations=[{"kind": "line", "id": "l2"}],
                    depth=1,
                ),
                _proof_line(
                    "l5",
                    "D",
                    "AS",
                    depth=1,
                    opens="s2",
                    closes=["s1"],
                ),
                _proof_line(
                    "l6",
                    "C",
                    "R",
                    citations=[{"kind": "line", "id": "l2"}],
                    depth=1,
                ),
                _proof_line(
                    "l7",
                    "C",
                    "∨E",
                    citations=[
                        {"kind": "line", "id": "l1"},
                        {"kind": "subproof", "start": "l3", "end": "l4"},
                        {"kind": "subproof", "start": "l5", "end": "l6"},
                    ],
                    closes=["s2"],
                ),
            ],
        }

        self.assertEqual(
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    proof,
                    allowed_rules=D23_RULES,
                )
            ],
            ["rule.disjunction_elimination_assumptions"],
        )

    def test_disjunction_elimination_rejects_reusing_one_branch_twice(self):
        proof = {
            "id": "duplicate-case-branch",
            "premises": ["A ∨ B", "C"],
            "target": "C",
            "lines": [
                _proof_line("l1", "A ∨ B", "PR"),
                _proof_line("l2", "C", "PR"),
                _proof_line("l3", "A", "AS", depth=1, opens="s1"),
                _proof_line(
                    "l4",
                    "C",
                    "R",
                    citations=[{"kind": "line", "id": "l2"}],
                    depth=1,
                ),
                _proof_line(
                    "l5",
                    "C",
                    "∨E",
                    citations=[
                        {"kind": "line", "id": "l1"},
                        {"kind": "subproof", "start": "l3", "end": "l4"},
                        {"kind": "subproof", "start": "l3", "end": "l4"},
                    ],
                    closes=["s1"],
                ),
            ],
        }

        self.assertEqual(
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    proof,
                    allowed_rules=D23_RULES,
                )
            ],
            ["rule.disjunction_elimination_duplicate_branch"],
        )

    def test_disjunction_elimination_requires_sibling_branches(self):
        proof = {
            "id": "nested-case-branches",
            "premises": ["A ∨ B", "C"],
            "target": "C",
            "lines": [
                _proof_line("l1", "A ∨ B", "PR"),
                _proof_line("l2", "C", "PR"),
                _proof_line("l3", "A", "AS", depth=1, opens="s1"),
                _proof_line(
                    "l4",
                    "C",
                    "R",
                    citations=[{"kind": "line", "id": "l2"}],
                    depth=1,
                ),
                _proof_line("l5", "B", "AS", depth=2, opens="s2"),
                _proof_line(
                    "l6",
                    "C",
                    "R",
                    citations=[{"kind": "line", "id": "l2"}],
                    depth=2,
                ),
                _proof_line(
                    "l7",
                    "C",
                    "∨E",
                    citations=[
                        {"kind": "line", "id": "l1"},
                        {"kind": "subproof", "start": "l3", "end": "l4"},
                        {"kind": "subproof", "start": "l5", "end": "l6"},
                    ],
                    closes=["s2", "s1"],
                ),
            ],
        }

        self.assertEqual(
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    proof,
                    allowed_rules=D23_RULES,
                )
            ],
            ["citation.subproof_inaccessible"],
        )

    def test_biconditional_elimination_accepts_both_directions_and_orders(self):
        cases = (
            ("A", "B", ["l1", "l2"]),
            ("B", "A", ["l2", "l1"]),
        )
        for given, target, citation_order in cases:
            proof = {
                "id": f"biconditional-{given}-to-{target}",
                "premises": ["A ↔ B", given],
                "target": target,
                "lines": [
                    _proof_line("l1", "A ↔ B", "PR"),
                    _proof_line("l2", given, "PR"),
                    _proof_line(
                        "l3",
                        target,
                        "↔E",
                        citations=[
                            {"kind": "line", "id": line_id}
                            for line_id in citation_order
                        ],
                    ),
                ],
            }

            with self.subTest(given=given, target=target):
                self.assertEqual(
                    audit_fitch_proof(
                        proof,
                        allowed_rules=D23_RULES,
                    ),
                    [],
                )

    def test_biconditional_elimination_rejects_an_unrelated_argument(self):
        proof = {
            "id": "unrelated-biconditional-argument",
            "premises": ["A ↔ B", "C"],
            "target": "A",
            "lines": [
                _proof_line("l1", "A ↔ B", "PR"),
                _proof_line("l2", "C", "PR"),
                _proof_line(
                    "l3",
                    "A",
                    "↔E",
                    citations=[
                        {"kind": "line", "id": "l1"},
                        {"kind": "line", "id": "l2"},
                    ],
                ),
            ],
        }

        self.assertEqual(
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    proof,
                    allowed_rules=D23_RULES,
                )
            ],
            ["rule.biconditional_elimination_mismatch"],
        )

    def test_biconditional_introduction_rejects_one_range_used_twice(self):
        proof = {
            "id": "duplicate-biconditional-direction",
            "premises": ["B"],
            "target": "A ↔ B",
            "lines": [
                _proof_line("l1", "B", "PR"),
                _proof_line("l2", "A", "AS", depth=1, opens="s1"),
                _proof_line(
                    "l3",
                    "B",
                    "R",
                    citations=[{"kind": "line", "id": "l1"}],
                    depth=1,
                ),
                _proof_line(
                    "l4",
                    "A ↔ B",
                    "↔I",
                    citations=[
                        {"kind": "subproof", "start": "l2", "end": "l3"},
                        {"kind": "subproof", "start": "l2", "end": "l3"},
                    ],
                    closes=["s1"],
                ),
            ],
        }

        self.assertEqual(
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    proof,
                    allowed_rules=D23_RULES,
                )
            ],
            ["rule.biconditional_introduction_duplicate_direction"],
        )

    def test_biconditional_introduction_requires_opposite_directions(self):
        proof = {
            "id": "same-biconditional-direction-twice",
            "premises": ["B"],
            "target": "A ↔ B",
            "lines": [
                _proof_line("l1", "B", "PR"),
                _proof_line("l2", "A", "AS", depth=1, opens="s1"),
                _proof_line(
                    "l3",
                    "B",
                    "R",
                    citations=[{"kind": "line", "id": "l1"}],
                    depth=1,
                ),
                _proof_line(
                    "l4",
                    "A",
                    "AS",
                    depth=1,
                    opens="s2",
                    closes=["s1"],
                ),
                _proof_line(
                    "l5",
                    "B",
                    "R",
                    citations=[{"kind": "line", "id": "l1"}],
                    depth=1,
                ),
                _proof_line(
                    "l6",
                    "A ↔ B",
                    "↔I",
                    citations=[
                        {"kind": "subproof", "start": "l2", "end": "l3"},
                        {"kind": "subproof", "start": "l4", "end": "l5"},
                    ],
                    closes=["s2"],
                ),
            ],
        }

        self.assertEqual(
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    proof,
                    allowed_rules=D23_RULES,
                )
            ],
            ["rule.biconditional_introduction_directions"],
        )


class D24StrategyAuditTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.lesson = STAGE_D_CANDIDATE_LESSONS[4]
        cls.fixtures = {
            fixture["id"]: fixture
            for fixture in cls.lesson["proof_fixtures"]
        }

    def test_complete_d24_fixtures_use_only_the_existing_rule_set(self):
        for fixture in self.lesson["proof_fixtures"]:
            if fixture["kind"] != "complete":
                continue
            with self.subTest(fixture=fixture["id"]):
                self.assertEqual(
                    audit_fitch_proof(
                        fixture["proof"],
                        allowed_rules=D24_RULES,
                    ),
                    [],
                )

    def test_d24_incomplete_plan_is_valid_before_scope_discharge(self):
        fixture = self.fixtures["d24-incomplete-conditional-chain"]

        self.assertEqual(
            audit_fitch_proof(
                fixture["proof"],
                allowed_rules=D24_RULES,
                require_complete=False,
            ),
            [],
        )
        self.assertEqual(
            {
                issue["code"]
                for issue in audit_fitch_proof(
                    fixture["proof"],
                    allowed_rules=D24_RULES,
                )
            },
            {
                "proof.scope_unclosed",
                "proof.target_in_subproof",
                "proof.target_not_reached",
            },
        )

    def test_d24_error_fixture_finds_the_premature_closure(self):
        fixture = self.fixtures["d24-premature-conditional-closure"]

        self.assertEqual(
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    fixture["proof"],
                    allowed_rules=D24_RULES,
                )
            ],
            fixture["expected_issue_codes"],
        )
        self.assertIn("B satırını koru", fixture["repair"])

    def test_d24_local_repair_preserves_the_bridge_and_completes_target(self):
        proof = deepcopy(
            self.fixtures["d24-premature-conditional-closure"]["proof"]
        )
        proof["lines"].insert(
            -1,
            _proof_line(
                "l4a",
                "C",
                "→E",
                citations=[
                    {"kind": "line", "id": "l2"},
                    {"kind": "line", "id": "l4"},
                ],
                depth=1,
            ),
        )
        proof["lines"][-1]["citations"] = [
            {"kind": "subproof", "start": "l3", "end": "l4a"}
        ]

        self.assertEqual(
            audit_fitch_proof(proof, allowed_rules=D24_RULES),
            [],
        )
        self.assertEqual(proof["lines"][3]["formula"], "B")

    def test_d24_keeps_derived_rules_locked(self):
        proof = {
            "id": "early-disjunctive-syllogism",
            "premises": ["A ∨ B", "¬A"],
            "target": "B",
            "lines": [
                _proof_line("l1", "A ∨ B", "PR"),
                _proof_line("l2", "¬A", "PR"),
                _proof_line(
                    "l3",
                    "B",
                    "DS",
                    citations=[
                        {"kind": "line", "id": "l1"},
                        {"kind": "line", "id": "l2"},
                    ],
                ),
            ],
        }

        self.assertIn(
            "rule.not_available",
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    proof,
                    allowed_rules=D24_RULES,
                )
            ],
        )


class D25DerivedRuleAuditTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.lesson = STAGE_D_CANDIDATE_LESSONS[5]
        cls.fixtures = {
            fixture["id"]: fixture
            for fixture in cls.lesson["proof_fixtures"]
        }

    def _audit_three_line_rule(
        self,
        premises,
        target,
        rule,
        *,
        citation_order=("l1", "l2"),
    ):
        proof = {
            "id": f"d25-{rule.lower()}-boundary",
            "premises": premises,
            "target": target,
            "lines": [
                _proof_line("l1", premises[0], "PR"),
                _proof_line("l2", premises[1], "PR"),
                _proof_line(
                    "l3",
                    target,
                    rule,
                    citations=[
                        {"kind": "line", "id": citation_id}
                        for citation_id in citation_order
                    ],
                ),
            ],
        }
        return audit_fitch_proof(proof, allowed_rules=D25_RULES)

    def test_complete_d25_fixtures_pass_the_expanded_rule_set(self):
        for fixture in self.lesson["proof_fixtures"]:
            if fixture["kind"] != "complete":
                continue
            with self.subTest(fixture=fixture["id"]):
                self.assertEqual(
                    audit_fitch_proof(
                        fixture["proof"],
                        allowed_rules=D25_RULES,
                    ),
                    [],
                )

    def test_d25_incomplete_lem_is_valid_before_final_discharge(self):
        fixture = self.fixtures["d25-incomplete-lem-second-branch"]

        self.assertEqual(
            audit_fitch_proof(
                fixture["proof"],
                allowed_rules=D25_RULES,
                require_complete=False,
            ),
            [],
        )
        self.assertEqual(
            {
                issue["code"]
                for issue in audit_fitch_proof(
                    fixture["proof"],
                    allowed_rules=D25_RULES,
                )
            },
            {"proof.scope_unclosed", "proof.target_in_subproof"},
        )

    def test_d25_error_fixture_rejects_silent_equivalence_as_de_morgan(self):
        fixture = self.fixtures["d25-error-silent-commutation-as-dem"]

        self.assertEqual(
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    fixture["proof"],
                    allowed_rules=D25_RULES,
                )
            ],
            fixture["expected_issue_codes"],
        )

    def test_ds_accepts_either_direct_disjunct_and_citation_order(self):
        cases = [
            (["A ∨ B", "¬A"], "B", ("l1", "l2")),
            (["A ∨ B", "¬B"], "A", ("l2", "l1")),
            (["(A ∧ C) ∨ B", "¬(A ∧ C)"], "B", ("l1", "l2")),
        ]

        for premises, target, citation_order in cases:
            with self.subTest(
                premises=premises,
                target=target,
                citation_order=citation_order,
            ):
                self.assertEqual(
                    self._audit_three_line_rule(
                        premises,
                        target,
                        "DS",
                        citation_order=citation_order,
                    ),
                    [],
                )

    def test_ds_requires_the_negation_of_a_direct_disjunct(self):
        issues = self._audit_three_line_rule(
            ["(A ∧ C) ∨ B", "¬A"],
            "B",
            "DS",
        )

        self.assertEqual(
            [issue["code"] for issue in issues],
            ["rule.disjunctive_syllogism_mismatch"],
        )

    def test_mt_accepts_compound_formulas_in_either_citation_order(self):
        for citation_order in (("l1", "l2"), ("l2", "l1")):
            with self.subTest(citation_order=citation_order):
                self.assertEqual(
                    self._audit_three_line_rule(
                        ["A → (B ∧ C)", "¬(B ∧ C)"],
                        "¬A",
                        "MT",
                        citation_order=citation_order,
                    ),
                    [],
                )

    def test_mt_rejects_denying_the_antecedent(self):
        issues = self._audit_three_line_rule(
            ["A → B", "¬A"],
            "¬B",
            "MT",
        )

        self.assertEqual(
            [issue["code"] for issue in issues],
            ["rule.modus_tollens_mismatch"],
        )

    def test_dne_requires_exactly_two_outer_negations(self):
        valid_proof = {
            "id": "d25-compound-dne",
            "premises": ["¬¬(A ∨ B)"],
            "target": "A ∨ B",
            "lines": [
                _proof_line("l1", "¬¬(A ∨ B)", "PR"),
                _proof_line(
                    "l2",
                    "A ∨ B",
                    "DNE",
                    citations=[{"kind": "line", "id": "l1"}],
                ),
            ],
        }
        invalid_proof = deepcopy(valid_proof)
        invalid_proof["id"] = "d25-inexact-dne"
        invalid_proof["target"] = "A"
        invalid_proof["lines"][-1]["formula"] = "A"

        self.assertEqual(
            audit_fitch_proof(valid_proof, allowed_rules=D25_RULES),
            [],
        )
        self.assertEqual(
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    invalid_proof,
                    allowed_rules=D25_RULES,
                )
            ],
            ["rule.double_negation_elimination_mismatch"],
        )

    def test_lem_requires_exact_contradictory_assumptions(self):
        proof = {
            "id": "d25-lem-noncontradictory-branches",
            "premises": ["C"],
            "target": "C",
            "lines": [
                _proof_line("l1", "C", "PR"),
                _proof_line("l2", "A", "AS", depth=1, opens="s1"),
                _proof_line(
                    "l3",
                    "C",
                    "R",
                    citations=[{"kind": "line", "id": "l1"}],
                    depth=1,
                ),
                _proof_line(
                    "l4",
                    "¬B",
                    "AS",
                    depth=1,
                    opens="s2",
                    closes=["s1"],
                ),
                _proof_line(
                    "l5",
                    "C",
                    "R",
                    citations=[{"kind": "line", "id": "l1"}],
                    depth=1,
                ),
                _proof_line(
                    "l6",
                    "C",
                    "LEM",
                    citations=[
                        {"kind": "subproof", "start": "l2", "end": "l3"},
                        {"kind": "subproof", "start": "l4", "end": "l5"},
                    ],
                    closes=["s2"],
                ),
            ],
        }

        self.assertEqual(
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    proof,
                    allowed_rules=D25_RULES,
                )
            ],
            ["rule.excluded_middle_assumptions"],
        )

    def test_lem_requires_the_same_result_in_both_branches(self):
        proof = {
            "id": "d25-lem-different-results",
            "premises": ["C", "D"],
            "target": "C",
            "lines": [
                _proof_line("l1", "C", "PR"),
                _proof_line("l2", "D", "PR"),
                _proof_line("l3", "A", "AS", depth=1, opens="s1"),
                _proof_line(
                    "l4",
                    "C",
                    "R",
                    citations=[{"kind": "line", "id": "l1"}],
                    depth=1,
                ),
                _proof_line(
                    "l5",
                    "¬A",
                    "AS",
                    depth=1,
                    opens="s2",
                    closes=["s1"],
                ),
                _proof_line(
                    "l6",
                    "D",
                    "R",
                    citations=[{"kind": "line", "id": "l2"}],
                    depth=1,
                ),
                _proof_line(
                    "l7",
                    "C",
                    "LEM",
                    citations=[
                        {"kind": "subproof", "start": "l3", "end": "l4"},
                        {"kind": "subproof", "start": "l5", "end": "l6"},
                    ],
                    closes=["s2"],
                ),
            ],
        }

        self.assertEqual(
            [
                issue["code"]
                for issue in audit_fitch_proof(
                    proof,
                    allowed_rules=D25_RULES,
                )
            ],
            ["rule.excluded_middle_conclusions"],
        )

    def test_de_morgan_accepts_exactly_the_four_licensed_directions(self):
        cases = [
            ("¬(A ∧ B)", "¬A ∨ ¬B"),
            ("¬A ∨ ¬B", "¬(A ∧ B)"),
            ("¬(A ∨ B)", "¬A ∧ ¬B"),
            ("¬A ∧ ¬B", "¬(A ∨ B)"),
        ]

        for source, target in cases:
            proof = {
                "id": "d25-dem-direction",
                "premises": [source],
                "target": target,
                "lines": [
                    _proof_line("l1", source, "PR"),
                    _proof_line(
                        "l2",
                        target,
                        "DeM",
                        citations=[{"kind": "line", "id": "l1"}],
                    ),
                ],
            }
            with self.subTest(source=source, target=target):
                self.assertEqual(
                    audit_fitch_proof(proof, allowed_rules=D25_RULES),
                    [],
                )

    def test_de_morgan_rejects_commutation_and_distribution(self):
        cases = [
            ("A ∧ B", "B ∧ A"),
            ("¬(A ∧ (B ∨ C))", "¬A ∨ (¬B ∧ ¬C)"),
        ]

        for source, target in cases:
            proof = {
                "id": "d25-unlicensed-equivalence",
                "premises": [source],
                "target": target,
                "lines": [
                    _proof_line("l1", source, "PR"),
                    _proof_line(
                        "l2",
                        target,
                        "DeM",
                        citations=[{"kind": "line", "id": "l1"}],
                    ),
                ],
            }
            with self.subTest(source=source, target=target):
                self.assertEqual(
                    [
                        issue["code"]
                        for issue in audit_fitch_proof(
                            proof,
                            allowed_rules=D25_RULES,
                        )
                    ],
                    ["rule.de_morgan_mismatch"],
                )
