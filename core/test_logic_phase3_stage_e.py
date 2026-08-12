from django.test import SimpleTestCase

from .logic_course_data import VISIBLE_LOGIC_LESSONS
from .logic_fol import (
    FOLParseError,
    FOLSignature,
    audit_fol_expression,
    classify_fol_expression,
    parse_fol,
    signature_from_data,
)
from .logic_phase3_stage_a import STAGE_A_CANDIDATE_MAP
from .logic_phase3_stage_b import STAGE_B_CANDIDATE_MAP
from .logic_phase3_stage_c import STAGE_C_CANDIDATE_MAP
from .logic_phase3_stage_d import STAGE_D_CANDIDATE_MAP
from .logic_phase3_stage_e import (
    E27_SIGNATURE,
    STAGE_E_CANDIDATE_LESSONS,
    STAGE_E_CANDIDATE_MAP,
    STAGE_E_SOURCE_REFERENCES,
)


class FOLSyntaxCoreTests(SimpleTestCase):
    def setUp(self):
        self.signature = FOLSignature(
            names={"a", "b"},
            variables={"x", "y", "z"},
            predicates={"F": 1, "G": 1, "R": 2},
        )

    def test_signature_rejects_category_overlap_and_bad_arity(self):
        with self.assertRaises(ValueError):
            FOLSignature(names={"x"}, variables={"x"}, predicates={"F": 1})
        with self.assertRaises(ValueError):
            FOLSignature(names={"a"}, predicates={"F": 0})
        with self.assertRaises(ValueError):
            FOLSignature(names={"x"}, predicates={"F": 1})

    def test_classifier_distinguishes_vocabulary_terms_and_formulas(self):
        expected = {
            "a": "name",
            "x": "variable",
            "F": "predicate",
            "F(a)": "sentence",
            "F(x)": "open_formula",
            "(F(a) ∧ G(b))": "sentence",
            "(F(x) ∧ G(a))": "open_formula",
        }
        for source, category in expected.items():
            with self.subTest(source=source):
                result = classify_fol_expression(source, self.signature)
                self.assertEqual(result["category"], category)

    def test_parser_builds_predicate_identity_binary_and_quantifier_nodes(self):
        predicate = parse_fol("R(a,b)", self.signature)
        identity = parse_fol("a=b", self.signature)
        binary = parse_fol("(F(a) → G(b))", self.signature)
        quantified = parse_fol("∀x(F(x) → G(x))", self.signature)

        self.assertEqual(predicate.kind, "predicate")
        self.assertEqual([term.symbol for term in predicate.terms], ["a", "b"])
        self.assertEqual(identity.kind, "identity")
        self.assertEqual(binary.kind, "binary")
        self.assertEqual(binary.operator, "→")
        self.assertEqual(quantified.kind, "quantifier")
        self.assertEqual(quantified.operator, "∀")
        self.assertTrue(quantified.is_sentence)
        self.assertEqual(quantified.render(), "∀x(F(x) → G(x))")

    def test_predicate_arity_is_checked_against_the_signature(self):
        for source in ("F()", "F(a,b)", "R(a)", "R(a,b,x)"):
            with self.subTest(source=source):
                result = audit_fol_expression(source, self.signature)
                self.assertFalse(result["accepted"])
                self.assertEqual(
                    result["issue_code"],
                    "predicate.arity_mismatch",
                )

    def test_unknown_predicate_and_term_have_separate_error_codes(self):
        self.assertEqual(
            audit_fol_expression("H(a)", self.signature)["issue_code"],
            "predicate.unknown",
        )
        self.assertEqual(
            audit_fol_expression("F(q)", self.signature)["issue_code"],
            "term.unknown",
        )

    def test_bare_term_is_not_silently_accepted_as_a_formula(self):
        result = audit_fol_expression("a ∧ F(a)", self.signature)

        self.assertFalse(result["accepted"])
        self.assertEqual(
            result["issue_code"],
            "formula.term_without_identity",
        )

    def test_each_variable_occurrence_records_its_nearest_binder(self):
        formula = parse_fol(
            "(∀x(F(x) ∨ G(y)) → ∃yR(y,x))",
            self.signature,
        )
        occurrences = formula.variable_occurrences

        self.assertEqual(len(occurrences), 4)
        self.assertTrue(occurrences[0]["bound"])
        self.assertEqual(occurrences[0]["binder_operator"], "∀")
        self.assertFalse(occurrences[1]["bound"])
        self.assertTrue(occurrences[2]["bound"])
        self.assertEqual(occurrences[2]["binder_operator"], "∃")
        self.assertFalse(occurrences[3]["bound"])
        self.assertEqual(formula.free_variables, frozenset({"x", "y"}))

    def test_nearest_quantifier_wins_and_shadowing_is_a_warning(self):
        formula = parse_fol("∀x∃xR(x,x)", self.signature)
        occurrences = formula.variable_occurrences
        warning_codes = {warning["code"] for warning in formula.warnings}

        self.assertTrue(all(item["bound"] for item in occurrences))
        self.assertEqual(
            {item["binder_operator"] for item in occurrences},
            {"∃"},
        )
        self.assertIn("quantifier.shadowing", warning_codes)
        self.assertIn("quantifier.vacuous", warning_codes)

    def test_vacuous_quantification_is_accepted_with_a_warning(self):
        result = classify_fol_expression("∃xF(a)", self.signature)

        self.assertEqual(result["category"], "sentence")
        self.assertEqual(
            [warning["code"] for warning in result["warnings"]],
            ["quantifier.vacuous"],
        )

    def test_binary_scope_requires_parentheses_when_more_than_one_is_present(self):
        with self.assertRaises(FOLParseError) as context:
            parse_fol("F(a) ∧ G(a) ∨ F(b)", self.signature)

        self.assertEqual(
            context.exception.code,
            "connective.multiple_unparenthesized",
        )

    def test_signature_can_be_built_from_serialisable_lesson_data(self):
        signature = signature_from_data(E27_SIGNATURE)

        self.assertEqual(signature.names, frozenset({"a", "b"}))
        self.assertEqual(signature.variables, frozenset({"x", "y", "z"}))
        self.assertEqual(signature.predicates, {"F": 1, "G": 1})


class LogicPhase3StageECandidateTests(SimpleTestCase):
    required_fields = {
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
        "fol_signature",
        "syntax_scope",
        "syntax_fixtures",
    }

    def test_stage_e_starts_with_only_the_e27_candidate(self):
        self.assertEqual(
            [lesson["curriculum_id"] for lesson in STAGE_E_CANDIDATE_LESSONS],
            ["E27"],
        )
        self.assertEqual(len(STAGE_E_CANDIDATE_MAP), 1)
        lesson = STAGE_E_CANDIDATE_LESSONS[0]
        self.assertTrue(self.required_fields.issubset(lesson))
        self.assertEqual(lesson["release_status"], "candidate")
        self.assertEqual(lesson["order"], 27)
        self.assertEqual(lesson["estimated_minutes"], 35)
        self.assertEqual(lesson["duration"], "35 dk")

    def test_e27_prerequisites_bridge_completed_b_and_d_candidates(self):
        lesson = STAGE_E_CANDIDATE_LESSONS[0]
        all_previous = {
            **STAGE_A_CANDIDATE_MAP,
            **STAGE_B_CANDIDATE_MAP,
            **STAGE_C_CANDIDATE_MAP,
            **STAGE_D_CANDIDATE_MAP,
        }

        self.assertEqual(
            lesson["prerequisites"],
            [
                "ders-17-sembollestirmeye-giris",
                "ders-kanit-ve-semantik-gecerlilik-koprusu",
            ],
        )
        for prerequisite in lesson["prerequisites"]:
            self.assertIn(prerequisite, all_previous)
            self.assertLess(all_previous[prerequisite]["order"], lesson["order"])

    def test_e27_is_isolated_from_the_learner_course(self):
        visible_slugs = {lesson["slug"] for lesson in VISIBLE_LOGIC_LESSONS}
        candidate = STAGE_E_CANDIDATE_LESSONS[0]

        self.assertNotIn(candidate["slug"], visible_slugs)
        self.assertEqual(len(VISIBLE_LOGIC_LESSONS), 45)

    def test_e27_has_sufficient_teaching_and_assessment_depth(self):
        lesson = STAGE_E_CANDIDATE_LESSONS[0]

        self.assertGreaterEqual(len(lesson["sections"]), 5)
        self.assertGreaterEqual(len(lesson["worked_examples"]), 8)
        self.assertGreaterEqual(len(lesson["practice"]), 12)
        self.assertGreaterEqual(len(lesson["production_tasks"]), 1)
        self.assertGreaterEqual(len(lesson["mastery_evidence"]), 5)
        self.assertGreaterEqual(len(lesson["syntax_fixtures"]), 10)
        self.assertEqual(
            lesson["syntax_scope"]["introduced"],
            [
                "domain",
                "name",
                "variable",
                "unary_predicate",
                "atomic_formula",
                "open_formula",
                "sentence",
            ],
        )
        self.assertIn("∀", lesson["syntax_scope"]["locked_until_later"])
        self.assertIn("∃", lesson["syntax_scope"]["locked_until_later"])
        self.assertIn("=", lesson["syntax_scope"]["locked_until_later"])

    def test_e27_sources_are_known_and_relevant(self):
        lesson = STAGE_E_CANDIDATE_LESSONS[0]

        self.assertEqual(
            lesson["source_ids"],
            [
                "forallx-fol-building-blocks",
                "forallx-fol-sentences",
                "mit-logic-sequence",
            ],
        )
        self.assertTrue(
            set(lesson["source_ids"]).issubset(STAGE_E_SOURCE_REFERENCES)
        )

    def test_every_e27_syntax_fixture_matches_the_independent_parser(self):
        lesson = STAGE_E_CANDIDATE_LESSONS[0]
        signature = signature_from_data(lesson["fol_signature"])

        for fixture in lesson["syntax_fixtures"]:
            with self.subTest(fixture=fixture["id"]):
                result = audit_fol_expression(fixture["source"], signature)
                self.assertEqual(result["accepted"], fixture["accepted"])
                if fixture["accepted"]:
                    self.assertEqual(
                        result["category"],
                        fixture["expected_category"],
                    )
                    self.assertIsNone(result["issue_code"])
                else:
                    self.assertEqual(
                        result["issue_code"],
                        fixture["expected_issue_code"],
                    )

    def test_e27_competencies_are_stable_and_unique(self):
        competencies = STAGE_E_CANDIDATE_LESSONS[0]["competencies"]

        self.assertEqual(len(competencies), len(set(competencies)))
        self.assertTrue(
            all(
                competency.startswith("fol.")
                and competency.count(".") == 1
                and competency.replace(".", "").replace("_", "").isalnum()
                for competency in competencies
            )
        )
