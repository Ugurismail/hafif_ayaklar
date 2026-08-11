from django.test import SimpleTestCase

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
    complete_truth_table,
    compound_subformulas,
    evaluate_tfl,
    evaluation_trace,
    generate_valuations,
    ordered_atoms,
    parse_tfl,
)


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
            ["C14", "C15"],
        )
        self.assertEqual(
            [lesson["order"] for lesson in STAGE_C_CANDIDATE_LESSONS],
            [14, 15],
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
        self.assertEqual(len(STAGE_C_CANDIDATE_LESSONS), 2)
        self.assertEqual(len(STAGE_C_CANDIDATE_MAP), 2)
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
