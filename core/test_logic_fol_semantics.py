from django.test import SimpleTestCase

from .logic_fol import FOLSignature
from .logic_fol_semantics import (
    COUNTERMODEL_FOUND,
    NO_COUNTERMODEL_IN_SAMPLE,
    FOLInterpretation,
    FOLSemanticError,
    analyze_binary_relation,
    evaluate_fol,
    evaluation_trace,
    interpretation_from_data,
    interpretation_to_data,
    search_countermodel,
)


class FOLInterpretationValidationTests(SimpleTestCase):
    def setUp(self):
        self.signature = FOLSignature(
            names={"a", "b"},
            variables={"x", "y", "z"},
            predicates={"F": 1, "G": 1, "R": 2},
        )
        self.data = {
            "label": "M1",
            "domain": ["ada", "bora", "cem"],
            "names": {"a": "ada", "b": "bora"},
            "predicates": {
                "F": ["ada", "cem"],
                "G": ["bora", "cem"],
                "R": [["ada", "bora"], ["bora", "cem"]],
            },
        }

    def test_serialisable_model_round_trip_is_deterministic(self):
        model = interpretation_from_data(self.data, self.signature)

        self.assertEqual(interpretation_to_data(model), self.data)
        self.assertEqual(model.predicates["F"], {("ada",), ("cem",)})

    def test_domain_must_be_non_empty_and_unique(self):
        for domain, issue_code in (
            ([], "model.domain_empty"),
            (["ada", "ada"], "model.domain_duplicate"),
        ):
            data = {**self.data, "domain": domain}
            with self.subTest(domain=domain), self.assertRaises(FOLSemanticError) as caught:
                interpretation_from_data(data, self.signature)
            self.assertEqual(caught.exception.code, issue_code)

    def test_every_name_and_predicate_must_match_the_signature(self):
        invalid_cases = (
            (
                {**self.data, "names": {"a": "ada"}},
                "model.name_key_mismatch",
            ),
            (
                {**self.data, "predicates": {"F": [], "G": []}},
                "model.predicate_key_mismatch",
            ),
        )
        for data, issue_code in invalid_cases:
            with self.subTest(issue_code=issue_code), self.assertRaises(FOLSemanticError) as caught:
                interpretation_from_data(data, self.signature)
            self.assertEqual(caught.exception.code, issue_code)

    def test_referents_and_extensions_cannot_leave_the_domain(self):
        invalid_cases = (
            (
                {**self.data, "names": {"a": "ada", "b": "deniz"}},
                "model.name_outside_domain",
            ),
            (
                {
                    **self.data,
                    "predicates": {**self.data["predicates"], "F": ["deniz"]},
                },
                "model.extension_outside_domain",
            ),
            (
                {
                    **self.data,
                    "predicates": {**self.data["predicates"], "R": [["ada"]]},
                },
                "model.extension_arity",
            ),
        )
        for data, issue_code in invalid_cases:
            with self.subTest(issue_code=issue_code), self.assertRaises(FOLSemanticError) as caught:
                interpretation_from_data(data, self.signature)
            self.assertEqual(caught.exception.code, issue_code)


class FOLEvaluationTests(SimpleTestCase):
    def setUp(self):
        self.signature = FOLSignature(
            names={"a", "b", "c"},
            variables={"x", "y", "z"},
            predicates={"F": 1, "G": 1, "R": 2},
        )
        self.model = FOLInterpretation(
            signature=self.signature,
            domain=("ada", "bora", "cem"),
            names={"a": "ada", "b": "bora", "c": "ada"},
            predicates={
                "F": {("ada",), ("cem",)},
                "G": {("ada",), ("bora",), ("cem",)},
                "R": {("ada", "bora"), ("bora", "cem"), ("cem", "cem")},
            },
            label="M",
        )

    def test_atomic_connective_and_identity_truth(self):
        expected = {
            "F(a)": True,
            "F(b)": False,
            "(F(a) ∧ G(a))": True,
            "(F(b) → G(b))": True,
            "a=c": True,
            "a≠b": True,
        }
        for formula, value in expected.items():
            with self.subTest(formula=formula):
                self.assertEqual(evaluate_fol(formula, self.model), value)

    def test_open_formula_requires_and_uses_assignment(self):
        with self.assertRaises(FOLSemanticError) as caught:
            evaluate_fol("F(x)", self.model)
        self.assertEqual(caught.exception.code, "assignment.free_variable_missing")

        self.assertTrue(evaluate_fol("F(x)", self.model, {"x": "cem"}))
        self.assertFalse(evaluate_fol("F(x)", self.model, {"x": "bora"}))

    def test_quantifiers_range_over_every_domain_member(self):
        expected = {
            "∀xG(x)": True,
            "∀xF(x)": False,
            "∃xF(x)": True,
            "∃x¬G(x)": False,
            "∀x∃yR(x,y)": True,
            "∃y∀xR(x,y)": False,
        }
        for formula, value in expected.items():
            with self.subTest(formula=formula):
                self.assertEqual(evaluate_fol(formula, self.model), value)

    def test_inner_quantifier_shadowing_restores_outer_assignment(self):
        formula = "∃x(F(x) ∧ (∃xG(x) ∧ F(x)))"

        self.assertTrue(evaluate_fol(formula, self.model))

    def test_trace_exposes_existential_witness_and_universal_counterexample(self):
        existential = evaluation_trace("∃xF(x)", self.model)
        universal = evaluation_trace("∀xF(x)", self.model)

        self.assertTrue(existential["value"])
        self.assertEqual(existential["steps"][-1]["detail"]["witness"], "ada")
        self.assertFalse(universal["value"])
        self.assertEqual(
            universal["steps"][-1]["detail"]["counterexample"],
            "bora",
        )


class FOLCountermodelSearchTests(SimpleTestCase):
    def setUp(self):
        self.signature = FOLSignature(
            names={"a"},
            variables={"x", "y"},
            predicates={"F": 1, "G": 1},
        )

    def model(self, label, f_extension, g_extension):
        return FOLInterpretation(
            signature=self.signature,
            domain=("u", "v"),
            names={"a": "u"},
            predicates={"F": f_extension, "G": g_extension},
            label=label,
        )

    def test_one_countermodel_establishes_non_entailment(self):
        models = [
            self.model("supports", {("u",)}, {("u",)}),
            self.model("counter", {("u",)}, set()),
        ]

        result = search_countermodel(
            ["∃xF(x)"],
            "∃xG(x)",
            models,
            self.signature,
        )

        self.assertEqual(result["status"], COUNTERMODEL_FOUND)
        self.assertFalse(result["entails"])
        self.assertEqual(result["countermodel"]["label"], "counter")
        self.assertEqual(result["checked_model_count"], 2)

    def test_no_sample_countermodel_does_not_claim_validity(self):
        result = search_countermodel(
            ["∀xF(x)"],
            "F(a)",
            [self.model("sample", {("u",), ("v",)}, set())],
            self.signature,
        )

        self.assertEqual(result["status"], NO_COUNTERMODEL_IN_SAMPLE)
        self.assertIsNone(result["entails"])
        self.assertIn("geçerliliğini kanıtlamaz", result["warning"])

    def test_consequence_search_rejects_open_formulas(self):
        with self.assertRaises(FOLSemanticError) as caught:
            search_countermodel(
                ["F(x)"],
                "F(a)",
                [],
                self.signature,
            )
        self.assertEqual(caught.exception.code, "consequence.open_formula")


class FOLRelationPropertyTests(SimpleTestCase):
    def setUp(self):
        self.signature = FOLSignature(
            variables={"x", "y", "z"},
            predicates={"R": 2, "F": 1},
        )

    def model(self, relation):
        return FOLInterpretation(
            signature=self.signature,
            domain=(1, 2, 3),
            names={},
            predicates={"R": relation, "F": set()},
        )

    def test_equivalence_relation_properties_hold(self):
        relation = {(left, right) for left in (1, 2, 3) for right in (1, 2, 3)}
        properties = analyze_binary_relation(self.model(relation), "R")["properties"]

        self.assertTrue(properties["reflexive"]["holds"])
        self.assertTrue(properties["symmetric"]["holds"])
        self.assertTrue(properties["transitive"]["holds"])
        self.assertTrue(properties["serial"]["holds"])
        self.assertFalse(properties["irreflexive"]["holds"])
        self.assertFalse(properties["antisymmetric"]["holds"])

    def test_property_failures_include_decisive_counterexamples(self):
        properties = analyze_binary_relation(
            self.model({(1, 2), (2, 1), (2, 3)}),
            "R",
        )["properties"]

        self.assertEqual(properties["reflexive"]["counterexample"], 1)
        self.assertIn(properties["symmetric"]["counterexample"], {(2, 3)})
        self.assertEqual(properties["antisymmetric"]["counterexample"], (1, 2))
        self.assertEqual(properties["transitive"]["counterexample"], (1, 2, 3))
        self.assertEqual(properties["serial"]["counterexample"], 3)

    def test_relation_analysis_requires_binary_predicate(self):
        with self.assertRaises(FOLSemanticError) as caught:
            analyze_binary_relation(self.model(set()), "F")
        self.assertEqual(caught.exception.code, "relation.arity")
