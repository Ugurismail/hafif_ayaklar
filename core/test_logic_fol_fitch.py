from django.test import SimpleTestCase

from .logic_fol import FOLSignature
from .logic_fol_fitch import (
    F38_RULES,
    F39_RULES,
    F40_RULES,
    audit_fol_fitch_proof,
)


SIGNATURE = FOLSignature(
    names={"a", "b", "c", "d"},
    predicates={"F": 1, "G": 1, "H": 1, "K": 1, "R": 2},
)


def line(line_id, formula, rule, citations=(), *, depth=0, opens=None, closes=()):
    return {
        "id": line_id,
        "formula": formula,
        "rule": rule,
        "citations": list(citations),
        "depth": depth,
        "opens": opens,
        "closes": list(closes),
    }


def cite(line_id):
    return {"kind": "line", "id": line_id}


def cite_subproof(start, end):
    return {"kind": "subproof", "start": start, "end": end}


def proof(premises, target, lines):
    return {"premises": premises, "target": target, "lines": lines}


def codes(result):
    return {issue["code"] for issue in result}


class FOLFitchUnrestrictedRuleTests(SimpleTestCase):
    def test_universal_elimination_accepts_capture_free_instance(self):
        candidate = proof(
            ["∀x(F(x) → ∃yR(x,y))"],
            "(F(a) → ∃yR(a,y))",
            [
                line("l1", "∀x(F(x) → ∃yR(x,y))", "PR"),
                line("l2", "(F(a) → ∃yR(a,y))", "∀E", [cite("l1")]),
            ],
        )
        self.assertEqual(audit_fol_fitch_proof(candidate, SIGNATURE, allowed_rules=F38_RULES), [])

    def test_universal_elimination_rejects_non_instance(self):
        candidate = proof(
            ["∀xR(x,x)"],
            "R(a,b)",
            [
                line("l1", "∀xR(x,x)", "PR"),
                line("l2", "R(a,b)", "∀E", [cite("l1")]),
            ],
        )
        self.assertIn(
            "rule.universal_elimination_substitution",
            codes(audit_fol_fitch_proof(candidate, SIGNATURE, allowed_rules=F38_RULES)),
        )

    def test_existential_introduction_allows_selected_occurrences(self):
        candidate = proof(
            ["R(a,a)"],
            "∃xR(x,a)",
            [
                line("l1", "R(a,a)", "PR"),
                line("l2", "∃xR(x,a)", "∃I", [cite("l1")]),
            ],
        )
        self.assertEqual(audit_fol_fitch_proof(candidate, SIGNATURE, allowed_rules=F38_RULES), [])

    def test_existential_introduction_rejects_changed_constant(self):
        candidate = proof(
            ["R(a,b)"],
            "∃xR(x,x)",
            [
                line("l1", "R(a,b)", "PR"),
                line("l2", "∃xR(x,x)", "∃I", [cite("l1")]),
            ],
        )
        self.assertIn(
            "rule.existential_introduction_substitution",
            codes(audit_fol_fitch_proof(candidate, SIGNATURE, allowed_rules=F38_RULES)),
        )

    def test_quantifier_rule_is_unavailable_before_its_stage(self):
        candidate = proof(
            ["F(a)"],
            "∃xF(x)",
            [
                line("l1", "F(a)", "PR"),
                line("l2", "∃xF(x)", "∃I", [cite("l1")]),
            ],
        )
        self.assertIn(
            "rule.not_available",
            codes(audit_fol_fitch_proof(candidate, SIGNATURE, allowed_rules={"PR"})),
        )

    def test_open_formula_is_never_a_proof_line(self):
        candidate = proof(
            [],
            "F(a)",
            [line("l1", "F(x)", "=I")],
        )
        self.assertIn(
            "formula.open",
            codes(audit_fol_fitch_proof(candidate, SIGNATURE, allowed_rules=F40_RULES)),
        )


class FOLFitchEigennameTests(SimpleTestCase):
    def test_universal_introduction_accepts_name_absent_from_dependencies(self):
        candidate = proof(
            ["∀x(F(x) → G(x))", "∀xF(x)"],
            "∀xG(x)",
            [
                line("l1", "∀x(F(x) → G(x))", "PR"),
                line("l2", "∀xF(x)", "PR"),
                line("l3", "(F(a) → G(a))", "∀E", [cite("l1")]),
                line("l4", "F(a)", "∀E", [cite("l2")]),
                line("l5", "G(a)", "→E", [cite("l3"), cite("l4")]),
                line("l6", "∀xG(x)", "∀I", [cite("l5")]),
            ],
        )
        self.assertEqual(audit_fol_fitch_proof(candidate, SIGNATURE, allowed_rules=F39_RULES), [])

    def test_universal_introduction_rejects_name_in_premise_dependency(self):
        candidate = proof(
            ["F(a)"],
            "∀xF(x)",
            [
                line("l1", "F(a)", "PR"),
                line("l2", "∀xF(x)", "∀I", [cite("l1")]),
            ],
        )
        self.assertIn(
            "rule.universal_introduction_name_not_fresh",
            codes(audit_fol_fitch_proof(candidate, SIGNATURE, allowed_rules=F39_RULES)),
        )

    def test_universal_introduction_rejects_name_in_open_assumption_dependency(self):
        candidate = proof(
            [],
            "(F(a) → ∀xF(x))",
            [
                line("l1", "F(a)", "AS", depth=1, opens="s1"),
                line("l2", "∀xF(x)", "∀I", [cite("l1")], depth=1),
                line("l3", "(F(a) → ∀xF(x))", "→I", [cite_subproof("l1", "l2")], closes=["s1"]),
            ],
        )
        self.assertIn(
            "rule.universal_introduction_name_not_fresh",
            codes(audit_fol_fitch_proof(candidate, SIGNATURE, allowed_rules=F39_RULES)),
        )

    def test_existential_elimination_accepts_fresh_witness_subproof(self):
        candidate = proof(
            ["∃xF(x)", "∀x(F(x) → G(x))"],
            "∃xG(x)",
            [
                line("l1", "∃xF(x)", "PR"),
                line("l2", "∀x(F(x) → G(x))", "PR"),
                line("l3", "F(a)", "AS", depth=1, opens="w"),
                line("l4", "(F(a) → G(a))", "∀E", [cite("l2")], depth=1),
                line("l5", "G(a)", "→E", [cite("l4"), cite("l3")], depth=1),
                line("l6", "∃xG(x)", "∃I", [cite("l5")], depth=1),
                line("l7", "∃xG(x)", "∃E", [cite("l1"), cite_subproof("l3", "l6")], closes=["w"]),
            ],
        )
        self.assertEqual(audit_fol_fitch_proof(candidate, SIGNATURE, allowed_rules=F39_RULES), [])

    def test_existential_elimination_rejects_witness_in_conclusion(self):
        candidate = proof(
            ["∃xF(x)"],
            "F(a)",
            [
                line("l1", "∃xF(x)", "PR"),
                line("l2", "F(a)", "AS", depth=1, opens="w"),
                line("l3", "F(a)", "R", [cite("l2")], depth=1),
                line("l4", "F(a)", "∃E", [cite("l1"), cite_subproof("l2", "l3")], closes=["w"]),
            ],
        )
        self.assertIn(
            "rule.existential_elimination_name_not_fresh",
            codes(audit_fol_fitch_proof(candidate, SIGNATURE, allowed_rules=F39_RULES)),
        )

    def test_existential_elimination_rejects_witness_already_in_existential_source(self):
        candidate = proof(
            ["∃xR(x,a)"],
            "∃xR(x,x)",
            [
                line("l1", "∃xR(x,a)", "PR"),
                line("l2", "R(a,a)", "AS", depth=1, opens="w"),
                line("l3", "∃xR(x,x)", "∃I", [cite("l2")], depth=1),
                line("l4", "∃xR(x,x)", "∃E", [cite("l1"), cite_subproof("l2", "l3")], closes=["w"]),
            ],
        )
        self.assertIn(
            "rule.existential_elimination_name_not_fresh",
            codes(audit_fol_fitch_proof(candidate, SIGNATURE, allowed_rules=F39_RULES)),
        )

    def test_existential_elimination_rejects_witness_in_external_dependency(self):
        candidate = proof(
            ["∃xF(x)", "(K(a) → ∃xG(x))", "K(a)"],
            "∃xG(x)",
            [
                line("l1", "∃xF(x)", "PR"),
                line("l2", "(K(a) → ∃xG(x))", "PR"),
                line("l3", "K(a)", "PR"),
                line("l4", "∃xG(x)", "→E", [cite("l2"), cite("l3")]),
                line("l5", "F(a)", "AS", depth=1, opens="w"),
                line("l6", "∃xG(x)", "R", [cite("l4")], depth=1),
                line("l7", "∃xG(x)", "∃E", [cite("l1"), cite_subproof("l5", "l6")], closes=["w"]),
            ],
        )
        self.assertIn(
            "rule.existential_elimination_name_not_fresh",
            codes(audit_fol_fitch_proof(candidate, SIGNATURE, allowed_rules=F39_RULES)),
        )


class FOLFitchIdentityAndScopeTests(SimpleTestCase):
    def test_identity_introduction_needs_no_citation(self):
        candidate = proof([], "a=a", [line("l1", "a=a", "=I")])
        self.assertEqual(audit_fol_fitch_proof(candidate, SIGNATURE, allowed_rules=F40_RULES), [])


class FOLFitchPreservedPropositionalRuleTests(SimpleTestCase):
    def assert_valid(self, candidate):
        self.assertEqual(
            audit_fol_fitch_proof(candidate, SIGNATURE, allowed_rules=F40_RULES),
            [],
        )

    def test_conjunction_and_conditional_rules(self):
        candidate = proof(
            ["F(a)", "G(a)"],
            "(F(a) → F(a))",
            [
                line("l1", "F(a)", "PR"),
                line("l2", "G(a)", "PR"),
                line("l3", "(F(a) ∧ G(a))", "∧I", [cite("l1"), cite("l2")]),
                line("l4", "F(a)", "∧E", [cite("l3")]),
                line("l5", "F(a)", "AS", depth=1, opens="s"),
                line("l6", "F(a)", "R", [cite("l5")], depth=1),
                line("l7", "(F(a) → F(a))", "→I", [cite_subproof("l5", "l6")], closes=["s"]),
            ],
        )
        self.assert_valid(candidate)

    def test_negation_explosion_and_indirect_proof_rules(self):
        candidate = proof(
            ["F(a)"],
            "F(a)",
            [
                line("l1", "F(a)", "PR"),
                line("l2", "¬F(a)", "AS", depth=1, opens="s"),
                line("l3", "⊥", "¬E", [cite("l1"), cite("l2")], depth=1),
                line("l4", "F(a)", "IP", [cite_subproof("l2", "l3")], closes=["s"]),
            ],
        )
        self.assert_valid(candidate)

        explosion = proof(
            ["F(a)", "¬F(a)"],
            "G(a)",
            [
                line("l1", "F(a)", "PR"),
                line("l2", "¬F(a)", "PR"),
                line("l3", "⊥", "¬E", [cite("l1"), cite("l2")]),
                line("l4", "G(a)", "X", [cite("l3")]),
            ],
        )
        self.assert_valid(explosion)

    def test_disjunction_introduction_and_elimination(self):
        candidate = proof(
            ["(F(a) ∨ G(a))", "(F(a) → H(a))", "(G(a) → H(a))"],
            "H(a)",
            [
                line("l1", "(F(a) ∨ G(a))", "PR"),
                line("l2", "(F(a) → H(a))", "PR"),
                line("l3", "(G(a) → H(a))", "PR"),
                line("l4", "F(a)", "AS", depth=1, opens="left"),
                line("l5", "H(a)", "→E", [cite("l2"), cite("l4")], depth=1),
                line("l6", "G(a)", "AS", depth=1, opens="right", closes=["left"]),
                line("l7", "H(a)", "→E", [cite("l3"), cite("l6")], depth=1),
                line("l8", "H(a)", "∨E", [cite("l1"), cite_subproof("l4", "l5"), cite_subproof("l6", "l7")], closes=["right"]),
            ],
        )
        self.assert_valid(candidate)

        introduction = proof(
            ["F(a)"],
            "(F(a) ∨ G(a))",
            [
                line("l1", "F(a)", "PR"),
                line("l2", "(F(a) ∨ G(a))", "∨I", [cite("l1")]),
            ],
        )
        self.assert_valid(introduction)

    def test_biconditional_introduction_and_elimination(self):
        candidate = proof(
            ["(F(a) → G(a))", "(G(a) → F(a))"],
            "(F(a) ↔ G(a))",
            [
                line("l1", "(F(a) → G(a))", "PR"),
                line("l2", "(G(a) → F(a))", "PR"),
                line("l3", "F(a)", "AS", depth=1, opens="fg"),
                line("l4", "G(a)", "→E", [cite("l1"), cite("l3")], depth=1),
                line("l5", "G(a)", "AS", depth=1, opens="gf", closes=["fg"]),
                line("l6", "F(a)", "→E", [cite("l2"), cite("l5")], depth=1),
                line("l7", "(F(a) ↔ G(a))", "↔I", [cite_subproof("l3", "l4"), cite_subproof("l5", "l6")], closes=["gf"]),
            ],
        )
        self.assert_valid(candidate)

        elimination = proof(
            ["(F(a) ↔ G(a))", "F(a)"],
            "G(a)",
            [
                line("l1", "(F(a) ↔ G(a))", "PR"),
                line("l2", "F(a)", "PR"),
                line("l3", "G(a)", "↔E", [cite("l1"), cite("l2")]),
            ],
        )
        self.assert_valid(elimination)

    def test_derived_classical_rules(self):
        fixtures = [
            proof(["(F(a) ∨ G(a))", "¬F(a)"], "G(a)", [
                line("l1", "(F(a) ∨ G(a))", "PR"), line("l2", "¬F(a)", "PR"), line("l3", "G(a)", "DS", [cite("l1"), cite("l2")]),
            ]),
            proof(["(F(a) → G(a))", "¬G(a)"], "¬F(a)", [
                line("l1", "(F(a) → G(a))", "PR"), line("l2", "¬G(a)", "PR"), line("l3", "¬F(a)", "MT", [cite("l1"), cite("l2")]),
            ]),
            proof(["¬¬F(a)"], "F(a)", [line("l1", "¬¬F(a)", "PR"), line("l2", "F(a)", "DNE", [cite("l1")])]),
            proof([], "(F(a) ∨ ¬F(a))", [line("l1", "(F(a) ∨ ¬F(a))", "LEM")]),
            proof(["¬(F(a) ∧ G(a))"], "(¬F(a) ∨ ¬G(a))", [
                line("l1", "¬(F(a) ∧ G(a))", "PR"), line("l2", "(¬F(a) ∨ ¬G(a))", "DeM", [cite("l1")]),
            ]),
        ]
        for candidate in fixtures:
            with self.subTest(target=candidate["target"]):
                self.assert_valid(candidate)

    def test_identity_elimination_can_replace_selected_occurrences(self):
        candidate = proof(
            ["a=b", "R(a,a)"],
            "R(b,a)",
            [
                line("l1", "a=b", "PR"),
                line("l2", "R(a,a)", "PR"),
                line("l3", "R(b,a)", "=E", [cite("l1"), cite("l2")]),
            ],
        )
        self.assertEqual(audit_fol_fitch_proof(candidate, SIGNATURE, allowed_rules=F40_RULES), [])

    def test_reiteration_cannot_reverse_identity_for_free(self):
        candidate = proof(
            ["a=b"],
            "b=a",
            [
                line("l1", "a=b", "PR"),
                line("l2", "b=a", "R", [cite("l1")]),
            ],
        )
        self.assertIn(
            "rule.r_formula_mismatch",
            codes(audit_fol_fitch_proof(candidate, SIGNATURE, allowed_rules=F40_RULES)),
        )

    def test_identity_elimination_can_derive_reverse_identity(self):
        candidate = proof(
            ["a=b"],
            "b=a",
            [
                line("l1", "a=b", "PR"),
                line("l2", "a=a", "=I"),
                line("l3", "b=a", "=E", [cite("l1"), cite("l2")]),
            ],
        )
        self.assertEqual(audit_fol_fitch_proof(candidate, SIGNATURE, allowed_rules=F40_RULES), [])

    def test_identity_elimination_rejects_unlicensed_change(self):
        candidate = proof(
            ["a=b", "R(a,c)"],
            "R(b,d)",
            [
                line("l1", "a=b", "PR"),
                line("l2", "R(a,c)", "PR"),
                line("l3", "R(b,d)", "=E", [cite("l1"), cite("l2")]),
            ],
        )
        self.assertIn(
            "rule.identity_elimination_substitution",
            codes(audit_fol_fitch_proof(candidate, SIGNATURE, allowed_rules=F40_RULES)),
        )

    def test_mixed_propositional_and_quantifier_proof(self):
        candidate = proof(
            ["∀x(F(x) → G(x))", "F(a)"],
            "∃xG(x)",
            [
                line("l1", "∀x(F(x) → G(x))", "PR"),
                line("l2", "F(a)", "PR"),
                line("l3", "(F(a) → G(a))", "∀E", [cite("l1")]),
                line("l4", "G(a)", "→E", [cite("l3"), cite("l2")]),
                line("l5", "∃xG(x)", "∃I", [cite("l4")]),
            ],
        )
        self.assertEqual(audit_fol_fitch_proof(candidate, SIGNATURE, allowed_rules=F40_RULES), [])

    def test_closed_subproof_line_is_inaccessible(self):
        candidate = proof(
            [],
            "F(a)",
            [
                line("l1", "F(a)", "AS", depth=1, opens="s"),
                line("l2", "F(a)", "R", [cite("l1")], depth=1),
                line("l3", "F(a)", "R", [cite("l2")], closes=["s"]),
            ],
        )
        self.assertIn(
            "citation.inaccessible",
            codes(audit_fol_fitch_proof(candidate, SIGNATURE, allowed_rules=F40_RULES)),
        )

    def test_alpha_equivalent_quantified_target_is_accepted(self):
        candidate = proof(
            ["∀xF(x)"],
            "∀yF(y)",
            [line("l1", "∀xF(x)", "PR")],
        )
        self.assertEqual(audit_fol_fitch_proof(candidate, SIGNATURE, allowed_rules=F40_RULES), [])
