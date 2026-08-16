from django.test import SimpleTestCase

from .logic_fol_capstone import (
    CAPSTONE_BLOCKED,
    CAPSTONE_COUNTERMODEL_FOUND,
    CAPSTONE_NEEDS_REVISION,
    CAPSTONE_PROOF_VERIFIED,
    CAPSTONE_UNDETERMINED,
    FOLCapstoneError,
    audit_fol_capstone,
    reconcile_capstone_results,
)


SIGNATURE = {
    "names": {"a": "Ada", "b": "Bora", "c": "taze nesne", "d": "Deniz"},
    "variables": ["x", "y", "z"],
    "predicates": {
        "F": {"arity": 1, "reading": "x araştırmacı"},
        "K": {"arity": 1, "reading": "x koordinatör"},
        "R": {"arity": 2, "reading": "x, y'ye danıştı"},
    },
}


ARGUMENT = {
    "premises": [
        "∀x(F(x) → ∃y(K(y) ∧ R(x,y)))",
        "F(a)",
        "a=b",
    ],
    "conclusion": "∃y(K(y) ∧ R(b,y))",
}


def _line(line_id, formula, rule, citations=()):
    return {
        "id": line_id,
        "formula": formula,
        "rule": rule,
        "citations": [{"kind": "line", "id": item} for item in citations],
        "depth": 0,
        "opens": None,
        "closes": [],
    }


VALID_PROOF = {
    "premises": ARGUMENT["premises"],
    "target": ARGUMENT["conclusion"],
    "lines": [
        _line("l1", ARGUMENT["premises"][0], "PR"),
        _line("l2", "F(a)", "PR"),
        _line("l3", "a=b", "PR"),
        _line("l4", "F(a) → ∃y(K(y) ∧ R(a,y))", "∀E", ["l1"]),
        _line("l5", "∃y(K(y) ∧ R(a,y))", "→E", ["l4", "l2"]),
        _line("l6", "∃y(K(y) ∧ R(b,y))", "=E", ["l3", "l5"]),
    ],
}


MODELS = [
    {
        "label": "İki araştırmacı, ortak koordinatör",
        "domain": ["ada", "deniz", "koor"],
        "names": {"a": "ada", "b": "ada", "c": "deniz", "d": "deniz"},
        "predicates": {
            "F": ["ada", "deniz"],
            "K": ["koor"],
            "R": [["ada", "koor"], ["deniz", "koor"]],
        },
    },
    {
        "label": "Tek araştırmacı",
        "domain": ["ada", "koor"],
        "names": {"a": "ada", "b": "ada", "c": "koor", "d": "koor"},
        "predicates": {
            "F": ["ada"],
            "K": ["koor"],
            "R": [["ada", "koor"]],
        },
    },
]


def _translation_tasks(candidate_overrides=None):
    candidate_overrides = candidate_overrides or {}
    tasks = []
    for index, formula in enumerate(ARGUMENT["premises"]):
        task_id = f"p{index + 1}"
        tasks.append(
            {
                "id": task_id,
                "label": f"{index + 1}. öncül",
                "role": "premise",
                "position": index,
                "candidate": candidate_overrides.get(task_id, formula),
                "accepted_sources": [formula],
            }
        )
    tasks.append(
        {
            "id": "c",
            "label": "Sonuç",
            "role": "conclusion",
            "candidate": candidate_overrides.get("c", ARGUMENT["conclusion"]),
            "accepted_sources": [ARGUMENT["conclusion"]],
        }
    )
    return tasks


def _case(**overrides):
    data = {
        "id": "stage-f-capstone",
        "signature": SIGNATURE,
        "argument": ARGUMENT,
        "translation_tasks": _translation_tasks(),
        "models": MODELS,
        "proof": VALID_PROOF,
    }
    data.update(overrides)
    return data


class FOLCapstoneAuditTests(SimpleTestCase):
    def test_valid_case_keeps_all_channels_separate(self):
        result = audit_fol_capstone(_case())

        self.assertTrue(result["translation"]["accepted"])
        self.assertEqual(len(result["semantics"]["models"]), 2)
        self.assertEqual(
            result["semantics"]["countermodel_search"]["status"],
            "no_countermodel_in_sample",
        )
        self.assertFalse(result["semantics"]["sample_establishes_validity"])
        self.assertTrue(result["proof"]["verified"])
        self.assertEqual(result["integrity"]["status"], CAPSTONE_PROOF_VERIFIED)
        self.assertFalse(result["integrity"]["blocking_conflict"])

    def test_bad_translation_does_not_change_model_or_proof_results(self):
        result = audit_fol_capstone(
            _case(
                translation_tasks=_translation_tasks(
                    {"p1": "∃y(K(y) ∧ ∀x(F(x) → R(x,y)))"}
                )
            )
        )

        self.assertFalse(result["translation"]["accepted"])
        self.assertTrue(result["proof"]["verified"])
        self.assertEqual(result["integrity"]["status"], CAPSTONE_NEEDS_REVISION)
        self.assertFalse(result["integrity"]["blocking_conflict"])

    def test_countermodel_is_reported_without_claiming_more(self):
        invalid_argument = {
            "premises": ["∀x(F(x) → ∃y(K(y) ∧ R(x,y)))"],
            "conclusion": "∃y(K(y) ∧ ∀x(F(x) → R(x,y)))",
        }
        model = {
            "label": "Farklı koordinatörler",
            "domain": ["ada", "deniz", "k1", "k2"],
            "names": {"a": "ada", "b": "deniz", "c": "k1", "d": "k2"},
            "predicates": {
                "F": ["ada", "deniz"],
                "K": ["k1", "k2"],
                "R": [["ada", "k1"], ["deniz", "k2"]],
            },
        }
        tasks = [
            {
                "id": "p1",
                "role": "premise",
                "position": 0,
                "candidate": invalid_argument["premises"][0],
                "accepted_sources": [invalid_argument["premises"][0]],
            },
            {
                "id": "c",
                "role": "conclusion",
                "candidate": invalid_argument["conclusion"],
                "accepted_sources": [invalid_argument["conclusion"]],
            },
        ]
        result = audit_fol_capstone(
            _case(
                argument=invalid_argument,
                translation_tasks=tasks,
                models=[model],
                proof=None,
            )
        )

        search = result["semantics"]["countermodel_search"]
        self.assertEqual(search["status"], "countermodel_found")
        self.assertTrue(all(search["premise_values"]))
        self.assertFalse(search["conclusion_value"])
        self.assertEqual(result["integrity"]["status"], CAPSTONE_COUNTERMODEL_FOUND)
        self.assertFalse(result["proof"]["provided"])

    def test_proof_for_another_argument_is_rejected_before_audit(self):
        wrong_proof = {**VALID_PROOF, "target": "∃xF(x)"}
        result = audit_fol_capstone(_case(proof=wrong_proof))

        self.assertFalse(result["proof"]["matches_argument"])
        self.assertFalse(result["proof"]["verified"])
        self.assertEqual(
            result["proof"]["issues"][0]["code"],
            "capstone.proof_argument_mismatch",
        )

    def test_no_proof_and_no_sample_countermodel_remains_undetermined(self):
        result = audit_fol_capstone(_case(proof=None))

        self.assertEqual(result["integrity"]["status"], CAPSTONE_UNDETERMINED)
        self.assertFalse(result["integrity"]["sample_establishes_validity"])

    def test_translation_key_must_cover_the_same_argument(self):
        tasks = _translation_tasks()
        tasks[0] = {**tasks[0], "accepted_sources": ["F(a)"]}
        with self.assertRaises(FOLCapstoneError) as context:
            audit_fol_capstone(_case(translation_tasks=tasks))
        self.assertEqual(
            context.exception.code,
            "capstone.translation_argument_mismatch",
        )

    def test_missing_translation_slot_is_an_authoring_error(self):
        with self.assertRaises(FOLCapstoneError) as context:
            audit_fol_capstone(_case(translation_tasks=_translation_tasks()[:-1]))
        self.assertEqual(
            context.exception.code,
            "capstone.translation_coverage_incomplete",
        )


class FOLCapstoneReconciliationTests(SimpleTestCase):
    def test_verified_proof_and_countermodel_block_publication(self):
        result = reconcile_capstone_results(
            translations_accepted=True,
            countermodel_status="countermodel_found",
            proof_provided=True,
            proof_verified=True,
        )
        self.assertEqual(result["status"], CAPSTONE_BLOCKED)
        self.assertTrue(result["blocking_conflict"])
        self.assertEqual(
            result["conflict_code"],
            "capstone.proof_countermodel_conflict",
        )

    def test_failed_sample_search_never_becomes_validity(self):
        result = reconcile_capstone_results(
            translations_accepted=True,
            countermodel_status="no_countermodel_in_sample",
            proof_provided=False,
            proof_verified=False,
        )
        self.assertEqual(result["status"], CAPSTONE_UNDETERMINED)
        self.assertFalse(result["sample_establishes_validity"])
