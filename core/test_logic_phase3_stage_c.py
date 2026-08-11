from html import unescape

from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from .logic_course_data import VISIBLE_LOGIC_LESSONS
from .logic_phase3_stage_a import STAGE_A_CANDIDATE_MAP
from .logic_phase3_stage_b import STAGE_B_CANDIDATE_MAP
from .logic_phase3_stage_c import (
    STAGE_C_CANDIDATE_LESSONS,
    STAGE_C_CANDIDATE_MAP,
    STAGE_C_SOURCE_REFERENCES,
)
from .logic_tfl_semantics import (
    TFLParseError,
    analyze_joint_satisfiability,
    analyze_semantic_consequence,
    analyze_semantic_equivalence,
    classify_semantic_status,
    complete_truth_table,
    compound_subformulas,
    evaluate_tfl,
    evaluation_trace,
    find_target_valuations,
    generate_valuations,
    ordered_atoms,
    parse_tfl,
)
from .models import LogicLessonProgress


class LogicPhase3StageCIntegrityTests(SimpleTestCase):
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
    }

    def test_stage_c_candidate_ids_orders_and_slugs_are_unique(self):
        self.assertEqual(
            [lesson["curriculum_id"] for lesson in STAGE_C_CANDIDATE_LESSONS],
            ["C14", "C15", "C16", "C17", "C18", "C19"],
        )
        self.assertEqual(
            [lesson["order"] for lesson in STAGE_C_CANDIDATE_LESSONS],
            [14, 15, 16, 17, 18, 19],
        )
        self.assertEqual(
            len({lesson["slug"] for lesson in STAGE_C_CANDIDATE_LESSONS}),
            len(STAGE_C_CANDIDATE_LESSONS),
        )
        self.assertEqual(
            len(STAGE_C_CANDIDATE_MAP),
            len(STAGE_C_CANDIDATE_LESSONS),
        )

    def test_every_stage_c_candidate_has_common_fields_and_known_sources(self):
        for lesson in STAGE_C_CANDIDATE_LESSONS:
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
                        STAGE_C_SOURCE_REFERENCES
                    )
                )

    def test_stage_c_prerequisites_exist_and_always_point_backwards(self):
        all_candidates = {
            **STAGE_A_CANDIDATE_MAP,
            **STAGE_B_CANDIDATE_MAP,
            **STAGE_C_CANDIDATE_MAP,
        }

        for lesson in STAGE_C_CANDIDATE_LESSONS:
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

    def test_no_stage_c_candidate_is_visible_to_learners(self):
        visible_slugs = {lesson["slug"] for lesson in VISIBLE_LOGIC_LESSONS}
        candidate_slugs = {
            lesson["slug"] for lesson in STAGE_C_CANDIDATE_LESSONS
        }

        self.assertTrue(candidate_slugs.isdisjoint(visible_slugs))


class TFLSemanticCoreTests(SimpleTestCase):
    def test_parser_accepts_strict_formulas_and_optional_outer_parentheses(self):
        formula = parse_tfl("¬(A ∧ B) → (C ↔ A₁)")

        self.assertEqual(formula.main_connective, "→")
        self.assertEqual(formula.atoms, {"A", "A₁", "B", "C"})
        self.assertEqual(
            formula.render(),
            "(¬(A ∧ B) → (C ↔ A₁))",
        )
        self.assertEqual(
            parse_tfl("((A ∨ B) → C)").render(),
            "((A ∨ B) → C)",
        )

    def test_parser_rejects_ambiguous_incomplete_and_unsupported_formulas(self):
        invalid_formulas = [
            "",
            "A ∧ B ∨ C",
            "(A ∧ B",
            "A ∧",
            "∧ A B",
            "A & B",
            "a ∨ B",
            "A_",
        ]

        for formula in invalid_formulas:
            with self.subTest(formula=formula):
                with self.assertRaises(TFLParseError):
                    parse_tfl(formula)

    def test_each_characteristic_truth_function_is_computed_correctly(self):
        cases = [
            ("¬A", {"A": "T"}, False),
            ("¬A", {"A": "F"}, True),
            ("A ∧ B", {"A": "T", "B": "T"}, True),
            ("A ∧ B", {"A": "T", "B": "F"}, False),
            ("A ∨ B", {"A": "T", "B": "T"}, True),
            ("A ∨ B", {"A": "F", "B": "F"}, False),
            ("A → B", {"A": "T", "B": "F"}, False),
            ("A → B", {"A": "F", "B": "F"}, True),
            ("A ↔ B", {"A": "T", "B": "T"}, True),
            ("A ↔ B", {"A": "F", "B": "F"}, True),
            ("A ↔ B", {"A": "T", "B": "F"}, False),
        ]

        for formula, valuation, expected in cases:
            with self.subTest(formula=formula, valuation=valuation):
                self.assertIs(evaluate_tfl(formula, valuation), expected)

    def test_evaluation_requires_a_valid_value_for_every_used_atom(self):
        with self.assertRaisesRegex(ValueError, "B atomu eksik"):
            evaluate_tfl("A ∧ B", {"A": "T"})

        with self.assertRaisesRegex(ValueError, "bool, 'T' veya 'F'"):
            evaluate_tfl("A", {"A": "D"})

    def test_trace_is_post_order_and_ends_with_the_whole_formula(self):
        trace = evaluation_trace(
            "¬(A ∧ B) → B",
            {"A": "T", "B": "F"},
        )

        self.assertEqual(
            [step["formula"] for step in trace],
            [
                "A",
                "B",
                "(A ∧ B)",
                "¬(A ∧ B)",
                "B",
                "(¬(A ∧ B) → B)",
            ],
        )
        self.assertEqual(
            [step["value"] for step in trace],
            ["T", "F", "F", "T", "F", "F"],
        )

    def test_atoms_are_distinct_and_naturally_ordered(self):
        self.assertEqual(
            ordered_atoms("(B ∧ A₂) → (A ∨ A₁)"),
            ["A", "A₁", "A₂", "B"],
        )
        self.assertEqual(
            ordered_atoms("(A ↔ A) ∨ ¬A"),
            ["A"],
        )

    def test_valuations_follow_the_standard_complete_pattern(self):
        valuations = generate_valuations(["C", "A", "B", "A"])

        self.assertEqual(len(valuations), 8)
        self.assertEqual(
            valuations,
            [
                {"A": "T", "B": "T", "C": "T"},
                {"A": "T", "B": "T", "C": "F"},
                {"A": "T", "B": "F", "C": "T"},
                {"A": "T", "B": "F", "C": "F"},
                {"A": "F", "B": "T", "C": "T"},
                {"A": "F", "B": "T", "C": "F"},
                {"A": "F", "B": "F", "C": "T"},
                {"A": "F", "B": "F", "C": "F"},
            ],
        )
        self.assertEqual(
            len({tuple(row.items()) for row in valuations}),
            len(valuations),
        )

    def test_complete_table_generation_has_a_bounded_atom_count(self):
        with self.assertRaisesRegex(ValueError, "En az bir"):
            generate_valuations([])

        with self.assertRaisesRegex(ValueError, "güvenlik sınırını"):
            generate_valuations(list("ABCDEFGHI"))

    def test_compound_columns_follow_dependency_order_without_duplicates(self):
        formulas = compound_subformulas("(A ∧ B) → ¬C")

        self.assertEqual(
            [formula.render() for formula in formulas],
            ["(A ∧ B)", "¬C", "((A ∧ B) → ¬C)"],
        )
        repeated = compound_subformulas("(A ∧ B) ↔ (A ∧ B)")
        self.assertEqual(
            [formula.render() for formula in repeated],
            ["(A ∧ B)", "((A ∧ B) ↔ (A ∧ B))"],
        )

    def test_complete_table_marks_the_main_column_without_classifying_it(self):
        table = complete_truth_table("(A ∧ B) → ¬C")

        self.assertEqual(table["atoms"], ["A", "B", "C"])
        self.assertEqual(table["row_count"], 8)
        self.assertEqual(
            [column["formula"] for column in table["columns"]],
            [
                "A",
                "B",
                "C",
                "(A ∧ B)",
                "¬C",
                "((A ∧ B) → ¬C)",
            ],
        )
        self.assertEqual(
            [column["formula"] for column in table["columns"] if column["is_main"]],
            ["((A ∧ B) → ¬C)"],
        )
        self.assertEqual(
            [row["values"][table["main_column"]] for row in table["rows"]],
            ["F", "T", "T", "T", "T", "T", "T", "T"],
        )
        self.assertNotIn("status", table)

    def test_repeated_sentence_letters_do_not_increase_the_row_count(self):
        table = complete_truth_table("(A ↔ A) ∨ ¬A")

        self.assertEqual(table["atoms"], ["A"])
        self.assertEqual(table["row_count"], 2)
        self.assertEqual(
            [row["values"][table["main_column"]] for row in table["rows"]],
            ["T", "T"],
        )

    def test_semantic_status_uses_every_main_column_value(self):
        cases = [
            ("A ∨ ¬A", "tautology", 2, 0),
            ("A ∧ ¬A", "contradiction", 0, 2),
            ("A → B", "contingency", 3, 1),
        ]

        for formula, expected_status, true_count, false_count in cases:
            with self.subTest(formula=formula):
                result = classify_semantic_status(formula)
                self.assertEqual(result["status"], expected_status)
                self.assertEqual(result["true_count"], true_count)
                self.assertEqual(result["false_count"], false_count)
                self.assertEqual(
                    result["true_count"] + result["false_count"],
                    result["row_count"],
                )

    def test_contingency_exposes_both_witness_types(self):
        result = classify_semantic_status("A → B")

        self.assertIn({"A": "T", "B": "T"}, result["true_valuations"])
        self.assertEqual(
            result["false_valuations"],
            [{"A": "T", "B": "F"}],
        )

    def test_equivalence_uses_the_union_of_both_atom_sets(self):
        equivalent = analyze_semantic_equivalence("A → B", "¬A ∨ B")
        separated = analyze_semantic_equivalence("A", "A ∨ B")

        self.assertTrue(equivalent["equivalent"])
        self.assertEqual(equivalent["atoms"], ["A", "B"])
        self.assertEqual(equivalent["separating_valuations"], [])
        self.assertFalse(separated["equivalent"])
        self.assertEqual(separated["atoms"], ["A", "B"])
        self.assertEqual(
            separated["separating_valuations"],
            [{"A": "F", "B": "T"}],
        )

    def test_joint_satisfiability_requires_one_shared_true_valuation(self):
        satisfiable = analyze_joint_satisfiability(["A ∨ B", "¬A"])
        unsatisfiable = analyze_joint_satisfiability(["A", "¬A"])

        self.assertTrue(satisfiable["jointly_satisfiable"])
        self.assertEqual(
            satisfiable["satisfying_valuations"],
            [{"A": "F", "B": "T"}],
        )
        self.assertFalse(unsatisfiable["jointly_satisfiable"])
        self.assertEqual(unsatisfiable["satisfying_valuations"], [])

    def test_joint_satisfiability_rejects_an_empty_formula_collection(self):
        with self.assertRaisesRegex(ValueError, "En az bir TFL cümlesi"):
            analyze_joint_satisfiability([])

    def test_semantic_consequence_returns_only_real_countervaluations(self):
        valid = analyze_semantic_consequence(["A → B", "A"], "B")
        invalid = analyze_semantic_consequence(["A → B", "B"], "A")

        self.assertTrue(valid["entails"])
        self.assertEqual(valid["countervaluations"], [])
        self.assertFalse(invalid["entails"])
        self.assertEqual(
            invalid["countervaluations"],
            [{"A": "F", "B": "T"}],
        )

    def test_semantic_consequence_handles_empty_and_incompatible_premises(self):
        premise_free = analyze_semantic_consequence([], "A ∨ ¬A")
        incompatible = analyze_semantic_consequence(["A", "¬A"], "B")

        self.assertTrue(premise_free["entails"])
        self.assertEqual(len(premise_free["premise_true_valuations"]), 2)
        self.assertTrue(incompatible["entails"])
        self.assertEqual(incompatible["premise_true_valuations"], [])
        self.assertEqual(incompatible["countervaluations"], [])

    def test_target_valuations_construct_exact_partial_table_witnesses(self):
        conditional = find_target_valuations([("A → B", "F")])
        shared = find_target_valuations(
            [("A ∨ B", "T"), ("¬A", "T")]
        )

        self.assertEqual(conditional["atoms"], ["A", "B"])
        self.assertEqual(conditional["row_count"], 4)
        self.assertEqual(
            conditional["matching_valuations"],
            [{"A": "T", "B": "F"}],
        )
        self.assertEqual(
            shared["matching_valuations"],
            [{"A": "F", "B": "T"}],
        )

    def test_target_valuations_can_report_an_unrealizable_target(self):
        result = find_target_valuations(
            [("A → B", "T"), ("A", "T"), ("B", "F")]
        )

        self.assertEqual(result["matching_valuations"], [])

    def test_target_valuations_require_at_least_one_condition(self):
        with self.assertRaisesRegex(
            ValueError,
            "En az bir hedef doğruluk koşulu",
        ):
            find_target_valuations([])


class LogicPhase3StageCC14CandidateTests(SimpleTestCase):
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
        "semantic_checks",
    }

    def setUp(self):
        self.lesson = STAGE_C_CANDIDATE_LESSONS[0]

    def test_c14_remains_the_first_candidate_as_stage_c_grows(self):
        self.assertEqual(len(STAGE_C_CANDIDATE_LESSONS), 6)
        self.assertEqual(len(STAGE_C_CANDIDATE_MAP), 6)
        self.assertEqual(self.lesson["curriculum_id"], "C14")
        self.assertEqual(self.lesson["order"], 14)
        self.assertEqual(self.lesson["release_status"], "candidate")
        self.assertEqual(self.lesson["estimated_minutes"], 40)
        self.assertEqual(self.lesson["duration"], "40 dk")
        self.assertTrue(self.required_fields.issubset(self.lesson))

    def test_c14_is_not_activated_in_the_learner_facing_course(self):
        visible_slugs = {lesson["slug"] for lesson in VISIBLE_LOGIC_LESSONS}

        self.assertNotIn(self.lesson["slug"], visible_slugs)

    def test_c14_prerequisites_bridge_completed_stage_a_and_stage_b(self):
        expected = [
            "ders-kullanim-anma-ve-dil-duzeyleri",
            "ders-kosul-yalnizca-cift-yonluluk",
            "ders-tfl-cumlesi-ana-baglac-ve-kapsam",
            "ders-kademeli-sembollestirme-atolyesi",
        ]

        self.assertEqual(self.lesson["prerequisites"], expected)
        self.assertIn(expected[0], STAGE_A_CANDIDATE_MAP)
        self.assertTrue(set(expected[1:]).issubset(STAGE_B_CANDIDATE_MAP))
        self.assertTrue(
            all(
                STAGE_B_CANDIDATE_MAP[slug]["order"] < self.lesson["order"]
                for slug in expected[1:]
            )
        )

    def test_c14_has_a_complete_instructional_sequence(self):
        self.assertGreaterEqual(len(self.lesson["goals"]), 4)
        self.assertGreaterEqual(len(self.lesson["sections"]), 5)
        self.assertGreaterEqual(len(self.lesson["worked_examples"]), 8)
        self.assertGreaterEqual(len(self.lesson["mistakes"]), 7)
        self.assertGreaterEqual(len(self.lesson["practice"]), 10)
        self.assertEqual(len(self.lesson["production_tasks"]), 1)
        self.assertGreaterEqual(len(self.lesson["mastery_evidence"]), 5)
        self.assertGreaterEqual(len(self.lesson["review_prompts"]), 3)

        guided = self.lesson["guided_practice"]
        self.assertEqual(
            set(guided),
            {"prompt", "starter", "checks", "solution"},
        )
        self.assertGreaterEqual(len(guided["checks"]), 4)
        self.assertIn("F→F=T", guided["solution"])

        production = self.lesson["production_tasks"][0]
        self.assertGreaterEqual(len(production["checkpoints"]), 5)
        self.assertEqual(len(production["stimulus"]["items"]), 4)
        self.assertIn("karşıolgusal", str(production).lower())

    def test_c14_practice_answers_are_valid_unique_and_explained(self):
        for item in self.lesson["practice"]:
            with self.subTest(prompt=item["prompt"]):
                self.assertIn(item["answer"], item["choices"])
                self.assertEqual(len(item["choices"]), len(set(item["choices"])))
                self.assertTrue(item["explanation"].strip())
                self.assertIn(
                    item["difficulty_label"],
                    {"Temel", "Orta", "İleri", "Zor", "Çok Zor"},
                )

    def test_c14_stays_inside_the_single_valuation_boundary(self):
        searchable = str(self.lesson)
        blocked_symbols = {"⊢", "⊨", "∀", "∃"}

        self.assertTrue(blocked_symbols.isdisjoint(searchable))
        self.assertNotIn("2^", searchable)
        self.assertNotIn("karşı değerleme", searchable.lower())
        self.assertNotIn("doğal türetim", searchable.lower())
        self.assertNotIn("çıkarım kuralı", searchable.lower())
        self.assertIn("tek bir değerleme", searchable.lower())
        self.assertIn("sonraki ders", searchable.lower())

    def test_c14_teaches_all_characteristic_conditions_and_language_limits(self):
        searchable = str(self.lesson).lower()

        for target in [
            "olumsuzlama",
            "birleşim",
            "kapsayıcı",
            "maddi koşul",
            "çift yönlü",
            "doğruluk işlev",
            "içten dışa",
            "üst dil",
            "nedensel",
            "karşıolgusal",
        ]:
            with self.subTest(target=target):
                self.assertIn(target, searchable)

        self.assertIn("yalnız t/f", searchable)
        self.assertIn("iki taraf aynı", searchable)
        self.assertIn("iki ayrılan birlikte doğru", searchable)

    def test_every_semantic_fixture_is_independently_verified(self):
        check_ids = set()
        for check in self.lesson["semantic_checks"]:
            with self.subTest(check=check["id"]):
                self.assertNotIn(check["id"], check_ids)
                check_ids.add(check["id"])
                parsed = parse_tfl(check["formula"])
                self.assertEqual(parsed.atoms, set(check["valuation"]))
                actual = "T" if evaluate_tfl(
                    parsed,
                    check["valuation"],
                ) else "F"
                self.assertEqual(actual, check["expected"])

        self.assertGreaterEqual(len(check_ids), 10)
        self.assertTrue(
            {
                "negation",
                "conjunction",
                "inclusive-disjunction",
                "material-conditional-false",
                "material-conditional-false-antecedent",
                "biconditional-both-false",
                "guided-complex",
                "production-one",
                "production-two",
                "production-three",
            }.issubset(check_ids)
        )

    def test_c14_sources_are_explicit_and_known(self):
        self.assertEqual(
            self.lesson["source_ids"],
            [
                "forallx-use-mention",
                "forallx-characteristic-tables",
                "forallx-truth-functionality",
                "forallx-valuations",
                "mit-logic-sequence",
                "mit-logic-study-guide",
            ],
        )
        self.assertTrue(
            set(self.lesson["source_ids"]).issubset(
                STAGE_C_SOURCE_REFERENCES
            )
        )


class LogicPhase3StageCC15CandidateTests(SimpleTestCase):
    def setUp(self):
        self.lesson = STAGE_C_CANDIDATE_MAP[
            "ders-tam-dogruluk-tablosu-kurma"
        ]

    def test_c15_identity_order_and_duration_are_stable(self):
        self.assertEqual(self.lesson["curriculum_id"], "C15")
        self.assertEqual(self.lesson["order"], 15)
        self.assertEqual(self.lesson["release_status"], "candidate")
        self.assertEqual(self.lesson["estimated_minutes"], 45)
        self.assertEqual(self.lesson["duration"], "45 dk")
        self.assertIn("table_checks", self.lesson)

    def test_c15_is_not_activated_in_the_learner_facing_course(self):
        visible_slugs = {lesson["slug"] for lesson in VISIBLE_LOGIC_LESSONS}

        self.assertNotIn(self.lesson["slug"], visible_slugs)

    def test_c15_prerequisites_are_c14_and_the_stage_b_syntax_lesson(self):
        expected = [
            "ders-degerlemeler-ve-dogruluk-islevleri",
            "ders-tfl-cumlesi-ana-baglac-ve-kapsam",
        ]

        self.assertEqual(self.lesson["prerequisites"], expected)
        self.assertIn(expected[0], STAGE_C_CANDIDATE_MAP)
        self.assertIn(expected[1], STAGE_B_CANDIDATE_MAP)
        self.assertLess(
            STAGE_C_CANDIDATE_MAP[expected[0]]["order"],
            self.lesson["order"],
        )

    def test_c15_has_a_complete_instructional_sequence(self):
        self.assertGreaterEqual(len(self.lesson["goals"]), 5)
        self.assertGreaterEqual(len(self.lesson["sections"]), 5)
        self.assertGreaterEqual(len(self.lesson["worked_examples"]), 8)
        self.assertGreaterEqual(len(self.lesson["mistakes"]), 8)
        self.assertGreaterEqual(len(self.lesson["practice"]), 12)
        self.assertEqual(len(self.lesson["production_tasks"]), 1)
        self.assertGreaterEqual(len(self.lesson["mastery_evidence"]), 6)
        self.assertGreaterEqual(len(self.lesson["review_prompts"]), 4)

        guided = self.lesson["guided_practice"]
        self.assertEqual(
            set(guided),
            {"prompt", "starter", "checks", "solution"},
        )
        self.assertGreaterEqual(len(guided["checks"]), 6)
        self.assertIn("T,T,T,T", guided["solution"])

        production = self.lesson["production_tasks"][0]
        self.assertGreaterEqual(len(production["checkpoints"]), 7)
        self.assertEqual(len(production["stimulus"]["items"]), 4)
        self.assertIn("F, F, F, F, T, F, T, T", str(production))

    def test_c15_practice_answers_are_valid_unique_and_explained(self):
        for item in self.lesson["practice"]:
            with self.subTest(prompt=item["prompt"]):
                self.assertIn(item["answer"], item["choices"])
                self.assertEqual(len(item["choices"]), len(set(item["choices"])))
                self.assertTrue(item["explanation"].strip())
                self.assertIn(
                    item["difficulty_label"],
                    {"Temel", "Orta", "İleri", "Zor", "Çok Zor"},
                )

    def test_c15_stays_with_complete_table_construction_not_later_methods(self):
        searchable = str(self.lesson)
        blocked_symbols = {"⊢", "⊨", "∀", "∃"}
        production = str(self.lesson["production_tasks"][0]).lower()

        self.assertTrue(blocked_symbols.isdisjoint(searchable))
        self.assertNotIn("karşı değerleme", searchable.lower())
        self.assertNotIn("doğal türetim", searchable.lower())
        self.assertNotIn("kısmi tablo", production)
        self.assertNotIn("geçerli", production)
        self.assertNotIn("totoloji", production)
        self.assertNotIn("çelişki", production)
        self.assertNotIn("olumsal", production)
        self.assertNotIn("tfl.status_classify", self.lesson["competencies"])
        self.assertIn("sonraki ders", searchable.lower())

    def test_c15_teaches_row_column_and_accessibility_controls(self):
        searchable = str(self.lesson).lower()

        for target in [
            "2^n",
            "farklı atom",
            "blok örüntüsü",
            "benzersiz",
            "alt cümle sütunu",
            "ana sütun",
            "oluşum ağacı",
            "renk dışında",
            "yeniden hesapla",
        ]:
            with self.subTest(target=target):
                self.assertIn(target, searchable)

    def test_every_table_fixture_is_independently_recomputed(self):
        check_ids = set()
        for check in self.lesson["table_checks"]:
            with self.subTest(check=check["id"]):
                self.assertNotIn(check["id"], check_ids)
                check_ids.add(check["id"])
                table = complete_truth_table(check["formula"])
                compound_columns = [
                    column["formula"]
                    for column in table["columns"]
                    if column["kind"] == "subformula"
                ]
                main_values = [
                    row["values"][table["main_column"]]
                    for row in table["rows"]
                ]

                self.assertEqual(table["atoms"], check["expected_atoms"])
                self.assertEqual(
                    table["row_count"],
                    check["expected_row_count"],
                )
                self.assertEqual(
                    compound_columns,
                    check["expected_compound_columns"],
                )
                self.assertEqual(
                    main_values,
                    check["expected_main_values"],
                )
                self.assertEqual(
                    table["row_count"],
                    2 ** len(table["atoms"]),
                )
                self.assertEqual(
                    len({tuple(row["valuation"].items()) for row in table["rows"]}),
                    table["row_count"],
                )
                self.assertNotIn("status", table)

        self.assertEqual(
            check_ids,
            {
                "complete-three-atom-example",
                "repeated-atom-example",
                "guided-de-morgan-table",
                "independent-production-table",
            },
        )

    def test_c15_sources_are_explicit_and_known(self):
        self.assertEqual(
            self.lesson["source_ids"],
            [
                "forallx-characteristic-tables",
                "forallx-truth-functionality",
                "forallx-valuations",
                "mit-logic-sequence",
                "mit-logic-study-guide",
            ],
        )
        self.assertTrue(
            set(self.lesson["source_ids"]).issubset(
                STAGE_C_SOURCE_REFERENCES
            )
        )


class LogicPhase3StageCC16CandidateTests(SimpleTestCase):
    def setUp(self):
        self.lesson = STAGE_C_CANDIDATE_MAP[
            "ders-totoloji-celiski-ve-olumsallik"
        ]

    def test_c16_identity_order_and_duration_are_stable(self):
        self.assertEqual(self.lesson["curriculum_id"], "C16")
        self.assertEqual(self.lesson["order"], 16)
        self.assertEqual(self.lesson["release_status"], "candidate")
        self.assertEqual(self.lesson["estimated_minutes"], 35)
        self.assertEqual(self.lesson["duration"], "35 dk")
        self.assertIn("status_checks", self.lesson)

    def test_c16_is_not_activated_in_the_learner_facing_course(self):
        visible_slugs = {lesson["slug"] for lesson in VISIBLE_LOGIC_LESSONS}

        self.assertNotIn(self.lesson["slug"], visible_slugs)

    def test_c16_prerequisites_bridge_stage_a_and_c15(self):
        expected = [
            "ders-3-gecerlilik-ve-dogruluk",
            "ders-kullanim-anma-ve-dil-duzeyleri",
            "ders-tam-dogruluk-tablosu-kurma",
        ]

        self.assertEqual(self.lesson["prerequisites"], expected)
        self.assertTrue(set(expected[:2]).issubset(STAGE_A_CANDIDATE_MAP))
        self.assertIn(expected[2], STAGE_C_CANDIDATE_MAP)
        self.assertLess(
            STAGE_C_CANDIDATE_MAP[expected[2]]["order"],
            self.lesson["order"],
        )

    def test_c16_has_a_complete_instructional_sequence(self):
        self.assertGreaterEqual(len(self.lesson["goals"]), 5)
        self.assertGreaterEqual(len(self.lesson["sections"]), 5)
        self.assertGreaterEqual(len(self.lesson["worked_examples"]), 8)
        self.assertGreaterEqual(len(self.lesson["mistakes"]), 9)
        self.assertGreaterEqual(len(self.lesson["practice"]), 12)
        self.assertEqual(len(self.lesson["production_tasks"]), 1)
        self.assertGreaterEqual(len(self.lesson["mastery_evidence"]), 6)
        self.assertGreaterEqual(len(self.lesson["review_prompts"]), 4)

        guided = self.lesson["guided_practice"]
        self.assertEqual(
            set(guided),
            {"prompt", "starter", "checks", "solution"},
        )
        self.assertGreaterEqual(len(guided["checks"]), 6)
        self.assertIn("çoğunluk", guided["solution"].lower())
        self.assertIn("olumsaldır", guided["solution"].lower())

        production = self.lesson["production_tasks"][0]
        self.assertGreaterEqual(len(production["checkpoints"]), 7)
        self.assertEqual(len(production["stimulus"]["items"]), 4)
        self.assertIn("bir doğru ve bir yanlış", str(production).lower())
        self.assertIn("atom", str(production).lower())

    def test_c16_practice_answers_are_valid_unique_and_explained(self):
        for item in self.lesson["practice"]:
            with self.subTest(prompt=item["prompt"]):
                self.assertIn(item["answer"], item["choices"])
                self.assertEqual(len(item["choices"]), len(set(item["choices"])))
                self.assertTrue(item["explanation"].strip())
                self.assertIn(
                    item["difficulty_label"],
                    {"Temel", "Orta", "İleri", "Zor", "Çok Zor"},
                )

    def test_c16_stays_with_single_formula_status_not_later_relations(self):
        searchable = str(self.lesson)
        production = str(self.lesson["production_tasks"][0]).lower()
        blocked_symbols = {"⊢", "⊨", "∀", "∃", "≡"}

        self.assertTrue(blocked_symbols.isdisjoint(searchable))
        self.assertNotIn("karşı değerleme", searchable.lower())
        self.assertNotIn("doğal türetim", searchable.lower())
        self.assertNotIn("çıkarım kuralı", searchable.lower())
        self.assertNotIn("eşdeğer", production)
        self.assertNotIn("birlikte doyur", production)
        self.assertNotIn("kısmi tablo", production)
        self.assertNotIn("tfl.equivalence_test", self.lesson["competencies"])
        self.assertNotIn("tfl.validity_test", self.lesson["competencies"])

    def test_c16_teaches_quantified_status_and_representation_limits(self):
        searchable = str(self.lesson).lower()

        for target in [
            "her değerlemede",
            "en az bir değerlemede",
            "totoloji",
            "çelişki",
            "olumsal",
            "ana sütun",
            "doğru tanığı",
            "yanlış tanığı",
            "üst dil",
            "2+2=4",
            "sembolleştirme",
            "çoğunluk",
        ]:
            with self.subTest(target=target):
                self.assertIn(target, searchable)

        self.assertIn("tek bir değerleme", searchable)
        self.assertIn("bütün değerlemeler", searchable)
        self.assertIn("tfl bakımından", searchable)

    def test_every_status_fixture_is_independently_recomputed(self):
        check_ids = set()
        statuses = set()

        for check in self.lesson["status_checks"]:
            with self.subTest(check=check["id"]):
                self.assertNotIn(check["id"], check_ids)
                check_ids.add(check["id"])
                table = complete_truth_table(check["formula"])
                main_values = [
                    row["values"][table["main_column"]]
                    for row in table["rows"]
                ]
                true_count = main_values.count("T")
                false_count = main_values.count("F")

                if false_count == 0:
                    independently_derived = "tautology"
                elif true_count == 0:
                    independently_derived = "contradiction"
                else:
                    independently_derived = "contingency"

                statuses.add(independently_derived)
                self.assertEqual(
                    main_values,
                    check["expected_main_values"],
                )
                self.assertEqual(
                    independently_derived,
                    check["expected_status"],
                )
                self.assertEqual(true_count, check["expected_true_count"])
                self.assertEqual(false_count, check["expected_false_count"])
                self.assertEqual(true_count + false_count, table["row_count"])

                classified = classify_semantic_status(check["formula"])
                self.assertEqual(classified["status"], independently_derived)
                self.assertEqual(classified["true_count"], true_count)
                self.assertEqual(classified["false_count"], false_count)
                if independently_derived == "contingency":
                    self.assertTrue(classified["true_valuations"])
                    self.assertTrue(classified["false_valuations"])

        self.assertGreaterEqual(len(check_ids), 10)
        self.assertEqual(
            statuses,
            {"tautology", "contradiction", "contingency"},
        )
        self.assertTrue(
            {
                "excluded-middle",
                "direct-contradiction",
                "material-conditional-contingent",
                "atomic-contingency",
                "sparse-contingency",
                "conditional-cover",
                "incompatible-conditional-conjunction",
            }.issubset(check_ids)
        )

    def test_c16_sources_are_explicit_and_known(self):
        self.assertEqual(
            self.lesson["source_ids"],
            [
                "forallx-use-mention",
                "forallx-truth-functionality",
                "forallx-valuations",
                "forallx-logical-concepts",
                "mit-logic-sequence",
                "mit-logic-study-guide",
            ],
        )
        self.assertTrue(
            set(self.lesson["source_ids"]).issubset(
                STAGE_C_SOURCE_REFERENCES
            )
        )


class LogicPhase3StageCC17CandidateTests(SimpleTestCase):
    def setUp(self):
        self.lesson = STAGE_C_CANDIDATE_MAP[
            "ders-mantiksal-esdegerlik-ve-tutarlilik"
        ]

    def test_c17_identity_order_and_duration_are_stable(self):
        self.assertEqual(self.lesson["curriculum_id"], "C17")
        self.assertEqual(self.lesson["order"], 17)
        self.assertEqual(self.lesson["release_status"], "candidate")
        self.assertEqual(self.lesson["estimated_minutes"], 45)
        self.assertEqual(self.lesson["duration"], "45 dk")
        self.assertIn("equivalence_checks", self.lesson)
        self.assertIn("satisfiability_checks", self.lesson)

    def test_c17_is_not_activated_in_the_learner_facing_course(self):
        visible_slugs = {lesson["slug"] for lesson in VISIBLE_LOGIC_LESSONS}

        self.assertNotIn(self.lesson["slug"], visible_slugs)

    def test_c17_prerequisites_are_c16_and_stage_b_scope(self):
        expected = [
            "ders-totoloji-celiski-ve-olumsallik",
            "ders-tfl-cumlesi-ana-baglac-ve-kapsam",
        ]

        self.assertEqual(self.lesson["prerequisites"], expected)
        self.assertIn(expected[0], STAGE_C_CANDIDATE_MAP)
        self.assertIn(expected[1], STAGE_B_CANDIDATE_MAP)
        self.assertLess(
            STAGE_C_CANDIDATE_MAP[expected[0]]["order"],
            self.lesson["order"],
        )

    def test_c17_has_a_complete_instructional_sequence(self):
        self.assertGreaterEqual(len(self.lesson["goals"]), 5)
        self.assertGreaterEqual(len(self.lesson["sections"]), 5)
        self.assertGreaterEqual(len(self.lesson["worked_examples"]), 9)
        self.assertGreaterEqual(len(self.lesson["mistakes"]), 10)
        self.assertGreaterEqual(len(self.lesson["practice"]), 12)
        self.assertEqual(len(self.lesson["production_tasks"]), 1)
        self.assertGreaterEqual(len(self.lesson["mastery_evidence"]), 6)
        self.assertGreaterEqual(len(self.lesson["review_prompts"]), 4)

        guided = self.lesson["guided_practice"]
        self.assertEqual(
            set(guided),
            {"prompt", "starter", "checks", "solution"},
        )
        self.assertGreaterEqual(len(guided["checks"]), 6)
        self.assertIn("ayırıcı", guided["solution"].lower())
        self.assertIn("birlikte doyurulamaz", guided["solution"].lower())

        production = self.lesson["production_tasks"][0]
        self.assertGreaterEqual(len(production["checkpoints"]), 7)
        self.assertEqual(len(production["stimulus"]["items"]), 4)
        self.assertIn("ortak değerleme", str(production).lower())
        self.assertIn("ayırıcı", str(production).lower())

    def test_c17_practice_answers_are_valid_unique_and_explained(self):
        for item in self.lesson["practice"]:
            with self.subTest(prompt=item["prompt"]):
                self.assertIn(item["answer"], item["choices"])
                self.assertEqual(len(item["choices"]), len(set(item["choices"])))
                self.assertTrue(item["explanation"].strip())
                self.assertIn(
                    item["difficulty_label"],
                    {"Temel", "Orta", "İleri", "Zor", "Çok Zor"},
                )

    def test_c17_stays_with_formula_relations_not_argument_validity(self):
        searchable = str(self.lesson)
        production = str(self.lesson["production_tasks"][0]).lower()
        blocked_symbols = {"⊢", "⊨", "⊭", "∀", "∃", "≡"}

        self.assertTrue(blocked_symbols.isdisjoint(searchable))
        self.assertNotIn("karşı değerleme", production)
        self.assertNotIn("geçerli argüman", production)
        self.assertNotIn("semantik sonuç", production)
        self.assertNotIn("doğal türetim", production)
        self.assertNotIn("çıkarım kuralı", production)
        self.assertNotIn("tfl.validity_test", self.lesson["competencies"])
        self.assertNotIn("tfl.entailment_test", self.lesson["competencies"])

    def test_c17_teaches_relation_set_and_witness_type_boundaries(self):
        searchable = str(self.lesson).lower()

        for target in [
            "mantıksal eşdeğerlik",
            "ortak değerleme uzayı",
            "ayırıcı değerleme",
            "birlikte doyurulabilir",
            "birlikte doyurulamaz",
            "ortak doğru tanığı",
            "aynı satır",
            "bütün satır",
            "tek cümle",
            "cümle kümesi",
            "üst dil",
        ]:
            with self.subTest(target=target):
                self.assertIn(target, searchable)

        self.assertIn("a↔b", searchable)
        self.assertIn("her biri olumsal", searchable)
        self.assertIn("varlık iddiası", searchable)
        self.assertIn("yokluk iddiası", searchable)

    def test_every_equivalence_fixture_is_independently_recomputed(self):
        check_ids = set()
        saw_equivalent = False
        saw_non_equivalent = False

        for check in self.lesson["equivalence_checks"]:
            with self.subTest(check=check["id"]):
                self.assertNotIn(check["id"], check_ids)
                check_ids.add(check["id"])
                left = parse_tfl(check["left"])
                right = parse_tfl(check["right"])
                atoms = sorted(left.atoms | right.atoms)
                valuations = generate_valuations(atoms)
                separating = [
                    dict(valuation)
                    for valuation in valuations
                    if evaluate_tfl(left, valuation)
                    != evaluate_tfl(right, valuation)
                ]
                independently_equivalent = not separating

                saw_equivalent |= independently_equivalent
                saw_non_equivalent |= not independently_equivalent
                self.assertEqual(
                    independently_equivalent,
                    check["expected_equivalent"],
                )
                self.assertEqual(
                    separating,
                    check["expected_separating_valuations"],
                )

                analyzed = analyze_semantic_equivalence(
                    check["left"],
                    check["right"],
                )
                self.assertEqual(analyzed["atoms"], atoms)
                self.assertEqual(
                    analyzed["row_count"],
                    2 ** len(atoms),
                )
                self.assertEqual(
                    analyzed["equivalent"],
                    independently_equivalent,
                )
                self.assertEqual(
                    analyzed["separating_valuations"],
                    separating,
                )

        self.assertEqual(len(check_ids), 8)
        self.assertTrue(saw_equivalent)
        self.assertTrue(saw_non_equivalent)
        self.assertIn("union-atom-space-separator", check_ids)

    def test_every_satisfiability_fixture_is_independently_recomputed(self):
        check_ids = set()
        saw_satisfiable = False
        saw_unsatisfiable = False

        for check in self.lesson["satisfiability_checks"]:
            with self.subTest(check=check["id"]):
                self.assertNotIn(check["id"], check_ids)
                check_ids.add(check["id"])
                formulas = [parse_tfl(item) for item in check["formulas"]]
                atoms = sorted(
                    set().union(*(formula.atoms for formula in formulas))
                )
                valuations = generate_valuations(atoms)
                satisfying = [
                    dict(valuation)
                    for valuation in valuations
                    if all(
                        evaluate_tfl(formula, valuation)
                        for formula in formulas
                    )
                ]
                independently_satisfiable = bool(satisfying)

                saw_satisfiable |= independently_satisfiable
                saw_unsatisfiable |= not independently_satisfiable
                self.assertEqual(
                    independently_satisfiable,
                    check["expected_jointly_satisfiable"],
                )
                self.assertEqual(
                    satisfying,
                    check["expected_satisfying_valuations"],
                )

                analyzed = analyze_joint_satisfiability(check["formulas"])
                self.assertEqual(analyzed["atoms"], atoms)
                self.assertEqual(
                    analyzed["row_count"],
                    2 ** len(atoms),
                )
                self.assertEqual(
                    analyzed["jointly_satisfiable"],
                    independently_satisfiable,
                )
                self.assertEqual(
                    analyzed["satisfying_valuations"],
                    satisfying,
                )

        self.assertEqual(len(check_ids), 8)
        self.assertTrue(saw_satisfiable)
        self.assertTrue(saw_unsatisfiable)
        self.assertTrue(
            {
                "direct-incompatibility",
                "shared-consequent-set",
                "modus-ponens-incompatibility",
                "exhausted-disjunction",
            }.issubset(check_ids)
        )

    def test_c17_sources_are_explicit_and_known(self):
        self.assertEqual(
            self.lesson["source_ids"],
            [
                "forallx-use-mention",
                "forallx-valuations",
                "forallx-logical-concepts",
                "mit-logic-sequence",
                "mit-logic-study-guide",
            ],
        )
        self.assertTrue(
            set(self.lesson["source_ids"]).issubset(
                STAGE_C_SOURCE_REFERENCES
            )
        )


class LogicPhase3StageCC18CandidateTests(SimpleTestCase):
    def setUp(self):
        self.lesson = STAGE_C_CANDIDATE_MAP[
            "ders-gecerlilik-ve-karsi-degerleme"
        ]

    def test_c18_identity_order_and_duration_are_stable(self):
        self.assertEqual(self.lesson["curriculum_id"], "C18")
        self.assertEqual(self.lesson["order"], 18)
        self.assertEqual(self.lesson["release_status"], "candidate")
        self.assertEqual(self.lesson["estimated_minutes"], 45)
        self.assertEqual(self.lesson["duration"], "45 dk")
        self.assertIn("consequence_checks", self.lesson)

    def test_c18_is_not_activated_in_the_learner_facing_course(self):
        visible_slugs = {lesson["slug"] for lesson in VISIBLE_LOGIC_LESSONS}

        self.assertNotIn(self.lesson["slug"], visible_slugs)

    def test_c18_prerequisites_bridge_stage_a_and_c17(self):
        expected = [
            "ders-3-gecerlilik-ve-dogruluk",
            "ders-9-karsi-ornek-sema-ve-curutme-teknikleri",
            "ders-kullanim-anma-ve-dil-duzeyleri",
            "ders-mantiksal-esdegerlik-ve-tutarlilik",
        ]

        self.assertEqual(self.lesson["prerequisites"], expected)
        self.assertTrue(set(expected[:3]).issubset(STAGE_A_CANDIDATE_MAP))
        self.assertIn(expected[3], STAGE_C_CANDIDATE_MAP)
        self.assertLess(
            STAGE_C_CANDIDATE_MAP[expected[3]]["order"],
            self.lesson["order"],
        )

    def test_c18_has_a_complete_instructional_sequence(self):
        self.assertGreaterEqual(len(self.lesson["goals"]), 5)
        self.assertGreaterEqual(len(self.lesson["sections"]), 5)
        self.assertGreaterEqual(len(self.lesson["worked_examples"]), 9)
        self.assertGreaterEqual(len(self.lesson["mistakes"]), 10)
        self.assertGreaterEqual(len(self.lesson["practice"]), 12)
        self.assertEqual(len(self.lesson["production_tasks"]), 1)
        self.assertGreaterEqual(len(self.lesson["mastery_evidence"]), 6)
        self.assertGreaterEqual(len(self.lesson["review_prompts"]), 4)

        guided = self.lesson["guided_practice"]
        self.assertEqual(
            set(guided),
            {"prompt", "starter", "checks", "solution"},
        )
        self.assertGreaterEqual(len(guided["checks"]), 6)
        self.assertIn("karşı değerleme", guided["solution"].lower())
        self.assertIn("üst dil", guided["solution"].lower())

        production = self.lesson["production_tasks"][0]
        self.assertGreaterEqual(len(production["checkpoints"]), 7)
        self.assertEqual(len(production["stimulus"]["items"]), 4)
        self.assertIn("kötü satır", str(production).lower())
        self.assertIn("karşı değerleme", str(production).lower())

    def test_c18_practice_answers_are_valid_unique_and_explained(self):
        for item in self.lesson["practice"]:
            with self.subTest(prompt=item["prompt"]):
                self.assertIn(item["answer"], item["choices"])
                self.assertEqual(len(item["choices"]), len(set(item["choices"])))
                self.assertTrue(item["explanation"].strip())
                self.assertIn(
                    item["difficulty_label"],
                    {"Temel", "Orta", "İleri", "Zor", "Çok Zor"},
                )

    def test_c18_uses_semantic_turnstiles_without_entering_proof_systems(self):
        searchable = str(self.lesson)
        production = str(self.lesson["production_tasks"][0]).lower()
        blocked_symbols = {"⊢", "∀", "∃", "≡"}

        self.assertTrue(blocked_symbols.isdisjoint(searchable))
        self.assertIn("⊨", searchable)
        self.assertIn("⊭", searchable)
        self.assertNotIn("kısmi tablo", production)
        self.assertNotIn("doğal türetim", production)
        self.assertNotIn("çıkarım kuralı", production)
        self.assertNotIn("yeniden yazma", production)
        self.assertNotIn("tfl.partial_table_construct", self.lesson["competencies"])

    def test_c18_teaches_bad_rows_and_language_levels(self):
        searchable = str(self.lesson).lower()

        for target in [
            "bütün öncüller t",
            "sonuç f",
            "kötü satır",
            "karşı değerleme",
            "öncül-doğru",
            "semantik sonuç",
            "geçerli",
            "sağlamlık",
            "nesne dili",
            "üst dil",
            "a⊭b",
            "a⊨¬b",
        ]:
            with self.subTest(target=target):
                self.assertIn(target, searchable)

        self.assertIn("birlikte doyurulamaz öncül", searchable)
        self.assertIn("tek iyi satır", searchable)
        self.assertIn("hiçbir kötü satır", searchable)

    def test_every_consequence_fixture_is_independently_recomputed(self):
        check_ids = set()
        saw_valid = False
        saw_invalid = False

        for check in self.lesson["consequence_checks"]:
            with self.subTest(check=check["id"]):
                self.assertNotIn(check["id"], check_ids)
                check_ids.add(check["id"])
                premises = [parse_tfl(item) for item in check["premises"]]
                conclusion = parse_tfl(check["conclusion"])
                atoms = sorted(
                    set().union(
                        conclusion.atoms,
                        *(premise.atoms for premise in premises),
                    )
                )
                valuations = generate_valuations(atoms)
                premise_true = [
                    dict(valuation)
                    for valuation in valuations
                    if all(
                        evaluate_tfl(premise, valuation)
                        for premise in premises
                    )
                ]
                countervaluations = [
                    valuation
                    for valuation in premise_true
                    if not evaluate_tfl(conclusion, valuation)
                ]
                independently_entails = not countervaluations

                saw_valid |= independently_entails
                saw_invalid |= not independently_entails
                self.assertEqual(
                    independently_entails,
                    check["expected_entails"],
                )
                self.assertEqual(
                    len(premise_true),
                    check["expected_premise_true_count"],
                )
                self.assertEqual(
                    countervaluations,
                    check["expected_countervaluations"],
                )

                analyzed = analyze_semantic_consequence(
                    check["premises"],
                    check["conclusion"],
                )
                self.assertEqual(analyzed["atoms"], atoms)
                self.assertEqual(
                    analyzed["row_count"],
                    2 ** len(atoms),
                )
                self.assertEqual(analyzed["entails"], independently_entails)
                self.assertEqual(
                    analyzed["premise_true_valuations"],
                    premise_true,
                )
                self.assertEqual(
                    analyzed["countervaluations"],
                    countervaluations,
                )

        self.assertEqual(len(check_ids), 12)
        self.assertTrue(saw_valid)
        self.assertTrue(saw_invalid)
        self.assertTrue(
            {
                "modus-ponens",
                "affirming-the-consequent",
                "hypothetical-syllogism",
                "denying-the-antecedent",
                "incompatible-premises",
                "premise-free-tautology",
            }.issubset(check_ids)
        )

    def test_c18_sources_are_explicit_and_known(self):
        self.assertEqual(
            self.lesson["source_ids"],
            [
                "forallx-use-mention",
                "forallx-valuations",
                "forallx-logical-concepts",
                "mit-logic-sequence",
                "mit-logic-study-guide",
            ],
        )
        self.assertTrue(
            set(self.lesson["source_ids"]).issubset(
                STAGE_C_SOURCE_REFERENCES
            )
        )


class LogicPhase3StageCC19CandidateTests(SimpleTestCase):
    def setUp(self):
        self.lesson = STAGE_C_CANDIDATE_MAP[
            "ders-kismi-tablolar-ve-tfl-sinirlari"
        ]

    def test_c19_identity_order_duration_and_method_data_are_stable(self):
        self.assertEqual(self.lesson["curriculum_id"], "C19")
        self.assertEqual(self.lesson["order"], 19)
        self.assertEqual(self.lesson["release_status"], "candidate")
        self.assertEqual(self.lesson["estimated_minutes"], 50)
        self.assertEqual(self.lesson["duration"], "50 dk")
        self.assertIn("method_checks", self.lesson)
        self.assertIn("partial_target_checks", self.lesson)
        self.assertIn("witness_checks", self.lesson)
        self.assertIn("expressiveness_cases", self.lesson)

    def test_c19_is_not_activated_in_the_learner_facing_course(self):
        visible_slugs = {lesson["slug"] for lesson in VISIBLE_LOGIC_LESSONS}

        self.assertNotIn(self.lesson["slug"], visible_slugs)

    def test_c19_prerequisites_bridge_stage_b_and_c18(self):
        expected = [
            "ders-belirsizlik-bulaniklik-savunulabilir-okumalar",
            "ders-kademeli-sembollestirme-atolyesi",
            "ders-gecerlilik-ve-karsi-degerleme",
        ]

        self.assertEqual(self.lesson["prerequisites"], expected)
        self.assertTrue(set(expected[:2]).issubset(STAGE_B_CANDIDATE_MAP))
        self.assertIn(expected[2], STAGE_C_CANDIDATE_MAP)
        self.assertLess(
            STAGE_C_CANDIDATE_MAP[expected[2]]["order"],
            self.lesson["order"],
        )

    def test_c19_has_a_complete_instructional_sequence(self):
        self.assertGreaterEqual(len(self.lesson["goals"]), 6)
        self.assertGreaterEqual(len(self.lesson["sections"]), 6)
        self.assertGreaterEqual(len(self.lesson["worked_examples"]), 10)
        self.assertGreaterEqual(len(self.lesson["mistakes"]), 10)
        self.assertGreaterEqual(len(self.lesson["practice"]), 12)
        self.assertEqual(len(self.lesson["production_tasks"]), 1)
        self.assertGreaterEqual(len(self.lesson["mastery_evidence"]), 6)
        self.assertGreaterEqual(len(self.lesson["review_prompts"]), 4)

        guided = self.lesson["guided_practice"]
        self.assertEqual(
            set(guided),
            {"prompt", "starter", "checks", "solution"},
        )
        self.assertGreaterEqual(len(guided["checks"]), 7)
        self.assertIn("geri çöz", guided["solution"].lower())
        self.assertIn("ileri hesap", guided["solution"].lower())

        production = self.lesson["production_tasks"][0]
        self.assertGreaterEqual(len(production["checkpoints"]), 7)
        self.assertEqual(len(production["stimulus"]["items"]), 4)
        self.assertIn("sınır raporu", str(production).lower())
        self.assertIn("kanıt yükü", str(production).lower())

    def test_c19_practice_answers_are_valid_unique_and_explained(self):
        for item in self.lesson["practice"]:
            with self.subTest(prompt=item["prompt"]):
                self.assertIn(item["answer"], item["choices"])
                self.assertEqual(len(item["choices"]), len(set(item["choices"])))
                self.assertTrue(item["explanation"].strip())
                self.assertIn(
                    item["difficulty_label"],
                    {"Temel", "Orta", "İleri", "Zor", "Çok Zor"},
                )

    def test_c19_closes_table_semantics_without_entering_proof_or_quantifiers(self):
        searchable = str(self.lesson)
        production = str(self.lesson["production_tasks"][0]).lower()
        blocked_symbols = {"⊢", "∀", "∃", "≡"}

        self.assertTrue(blocked_symbols.isdisjoint(searchable))
        self.assertIn("⊨", searchable)
        self.assertIn("⊭", searchable)
        self.assertNotIn("doğal türetim", production)
        self.assertNotIn("çıkarım kuralı", production)
        self.assertNotIn("türetim kuralı", production)
        self.assertNotIn("niceleyici", production)
        self.assertTrue(
            {
                "tfl.table_method_select",
                "tfl.partial_table_construct",
                "tfl.proof_burden_explain",
                "tfl.expressiveness_limit_diagnose",
            }.issubset(self.lesson["competencies"])
        )

    def test_c19_teaches_method_scope_and_representation_boundaries(self):
        searchable = str(self.lesson).lower()

        for target in [
            "tam doğruluk tablosu",
            "kısaltılmış tam tablo",
            "kısmi doğruluk tablosu",
            "kanıt yükü",
            "evrensel iddia",
            "varlık iddiası",
            "geri çöz",
            "ileri doğrulama",
            "sembolleştirme kaybı",
            "ifade gücü sınırı",
            "bulanıklık",
            "zorunluluk",
            "karşıolgusal",
            "nedensellik",
            "zaman sırası",
            "pragmatik",
        ]:
            with self.subTest(target=target):
                self.assertIn(target, searchable)

        self.assertIn("bütün değerleme satırlarını koru", searchable)
        self.assertIn("tek karşı tanık", searchable)
        self.assertIn("tablo hesap hatası", searchable)

    def test_method_matrix_covers_both_answers_with_the_correct_burden(self):
        expected = {
            "tautology": {
                "yes": ("exhaustive", {"complete", "shortened_complete"}),
                "no": ("witness", {"partial"}),
            },
            "contradiction": {
                "yes": ("exhaustive", {"complete", "shortened_complete"}),
                "no": ("witness", {"partial"}),
            },
            "equivalence": {
                "yes": ("exhaustive", {"complete", "shortened_complete"}),
                "no": ("witness", {"partial"}),
            },
            "joint_satisfiability": {
                "yes": ("witness", {"partial"}),
                "no": ("exhaustive", {"complete", "shortened_complete"}),
            },
            "validity": {
                "yes": ("exhaustive", {"complete", "shortened_complete"}),
                "no": ("witness", {"partial"}),
            },
        }
        observed = {}
        ids = set()

        for check in self.lesson["method_checks"]:
            with self.subTest(check=check["id"]):
                self.assertNotIn(check["id"], ids)
                ids.add(check["id"])
                key = (check["question"], check["answer"])
                self.assertNotIn(key, observed)
                observed[key] = (
                    check["expected_burden"],
                    set(check["acceptable_methods"]),
                )

        self.assertEqual(len(ids), 10)
        self.assertEqual(
            observed,
            {
                (question, answer): result
                for question, answers in expected.items()
                for answer, result in answers.items()
            },
        )

    def test_every_partial_target_fixture_is_independently_recomputed(self):
        check_ids = set()

        for check in self.lesson["partial_target_checks"]:
            with self.subTest(check=check["id"]):
                self.assertNotIn(check["id"], check_ids)
                check_ids.add(check["id"])
                parsed_requirements = [
                    (parse_tfl(formula), target == "T")
                    for formula, target in check["requirements"]
                ]
                atoms = sorted(
                    set().union(
                        *(formula.atoms for formula, _ in parsed_requirements)
                    )
                )
                independently_matching = [
                    dict(valuation)
                    for valuation in generate_valuations(atoms)
                    if all(
                        evaluate_tfl(formula, valuation) == target
                        for formula, target in parsed_requirements
                    )
                ]

                self.assertEqual(
                    independently_matching,
                    check["expected_matching_valuations"],
                )
                analyzed = find_target_valuations(check["requirements"])
                self.assertEqual(analyzed["atoms"], atoms)
                self.assertEqual(analyzed["row_count"], 2 ** len(atoms))
                self.assertEqual(
                    analyzed["matching_valuations"],
                    independently_matching,
                )

        self.assertEqual(len(check_ids), 5)
        self.assertIn("unrealizable-target", check_ids)

    def test_every_economic_witness_is_independently_verified(self):
        check_ids = set()
        kinds = set()

        for check in self.lesson["witness_checks"]:
            with self.subTest(check=check["id"]):
                self.assertNotIn(check["id"], check_ids)
                check_ids.add(check["id"])
                kinds.add(check["kind"])
                witness = check["expected_witness"]

                if check["kind"] == "non_equivalence":
                    self.assertNotEqual(
                        evaluate_tfl(check["left"], witness),
                        evaluate_tfl(check["right"], witness),
                    )
                    result = analyze_semantic_equivalence(
                        check["left"],
                        check["right"],
                    )
                    self.assertIn(witness, result["separating_valuations"])
                elif check["kind"] == "joint_satisfiability":
                    self.assertTrue(
                        all(
                            evaluate_tfl(formula, witness)
                            for formula in check["formulas"]
                        )
                    )
                    result = analyze_joint_satisfiability(check["formulas"])
                    self.assertIn(witness, result["satisfying_valuations"])
                elif check["kind"] == "countervaluation":
                    self.assertTrue(
                        all(
                            evaluate_tfl(premise, witness)
                            for premise in check["premises"]
                        )
                    )
                    self.assertFalse(
                        evaluate_tfl(check["conclusion"], witness)
                    )
                    result = analyze_semantic_consequence(
                        check["premises"],
                        check["conclusion"],
                    )
                    self.assertIn(witness, result["countervaluations"])
                else:
                    self.fail(f'Bilinmeyen tanık türü: {check["kind"]}')

        self.assertEqual(
            kinds,
            {"non_equivalence", "joint_satisfiability", "countervaluation"},
        )

    def test_expressiveness_cases_cover_the_required_loss_categories(self):
        categories = set()
        ids = set()

        for case in self.lesson["expressiveness_cases"]:
            with self.subTest(case=case["id"]):
                self.assertNotIn(case["id"], ids)
                ids.add(case["id"])
                categories.add(case["category"])
                self.assertTrue(case["example"].strip())
                self.assertTrue(case["loss"].strip())
                self.assertTrue(case["needed_information"].strip())

        self.assertEqual(
            categories,
            {
                "internal_structure",
                "vagueness",
                "modality",
                "counterfactual",
                "causation",
                "time",
                "pragmatics",
            },
        )

    def test_c19_sources_are_explicit_and_known(self):
        self.assertEqual(
            self.lesson["source_ids"],
            [
                "forallx-truth-functionality",
                "forallx-logical-concepts",
                "forallx-expressiveness",
                "forallx-table-shortcuts",
                "forallx-partial-tables",
                "mit-logic-sequence",
                "mit-logic-study-guide",
            ],
        )
        self.assertTrue(
            set(self.lesson["source_ids"]).issubset(
                STAGE_C_SOURCE_REFERENCES
            )
        )


class LogicPhase3StageCPreviewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.staff_user = user_model.objects.create_user(
            username="logic-stage-c-reviewer",
            password="review-pass",
            is_staff=True,
        )
        cls.regular_user = user_model.objects.create_user(
            username="logic-stage-c-student",
            password="student-pass",
        )

    def test_preview_requires_staff_access(self):
        url = reverse("logic_stage_c_preview")

        anonymous_response = self.client.get(url)
        self.assertEqual(anonymous_response.status_code, 302)
        self.assertIn(reverse("admin:login"), anonymous_response.url)

        self.client.force_login(self.regular_user)
        regular_response = self.client.get(url)
        self.assertEqual(regular_response.status_code, 302)
        self.assertIn(reverse("admin:login"), regular_response.url)

    def test_staff_preview_contains_every_stage_c_candidate(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("logic_stage_c_preview"))
        rendered_text = unescape(response.content.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/logic_stage_a_preview.html")
        self.assertIn(
            "Faz 3C: TFL semantiği ve yöntem seçimi",
            rendered_text,
        )
        for lesson in STAGE_C_CANDIDATE_LESSONS:
            with self.subTest(lesson=lesson["curriculum_id"]):
                self.assertIn(lesson["curriculum_id"], rendered_text)
                self.assertIn(lesson["title"], rendered_text)

    def test_staff_preview_contains_each_production_stimulus(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("logic_stage_c_preview"))
        rendered_text = unescape(response.content.decode())

        for lesson in STAGE_C_CANDIDATE_LESSONS:
            for task in lesson["production_tasks"]:
                stimulus = task["stimulus"]
                with self.subTest(lesson=lesson["curriculum_id"]):
                    self.assertIn(stimulus["label"], rendered_text)
                    for item in stimulus["items"]:
                        self.assertIn(item, rendered_text)

    def test_preview_lists_cross_stage_prerequisites_without_live_links(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("logic_stage_c_preview"))
        rendered_text = unescape(response.content.decode())

        self.assertIn(
            "B12 · Belirsizlik, Bulanıklık ve Savunulabilir Okumalar",
            rendered_text,
        )
        self.assertIn("B13 · Kademeli Sembolleştirme Atölyesi", rendered_text)
        self.assertIn("C18 · Geçerlilik ve Karşı Değerleme", rendered_text)
        self.assertNotIn('href="#aday-b12"', rendered_text)
        self.assertNotIn('href="#aday-b13"', rendered_text)
        self.assertIn('href="#aday-c18"', rendered_text)

    def test_preview_is_read_only_and_has_no_learner_progress_hooks(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("logic_stage_c_preview"))

        self.assertEqual(LogicLessonProgress.objects.count(), 0)
        self.assertNotContains(response, "data-logic-lesson-page")
        self.assertNotContains(response, "data-progress-url")
        self.assertNotContains(response, reverse("logic_lesson_progress"))
        self.assertNotContains(response, "logic_lesson.js")
