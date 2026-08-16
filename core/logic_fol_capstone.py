"""Cross-check the three independent channels of the Stage F capstone.

The module deliberately does not add another logical decision procedure.
Translation is checked by the Stage E structural assessor, finite models by
the Stage F semantic engine, and derivations by the FOL Fitch auditor.  This
orchestrator only verifies that those channels concern the same argument and
reports disagreements without hiding them.
"""

from collections.abc import Mapping

from .logic_fol import (
    assess_fol_symbolization,
    formulas_alpha_equivalent,
    parse_fol,
    signature_from_data,
)
from .logic_fol_fitch import F40_RULES, audit_fol_fitch_proof
from .logic_fol_semantics import (
    COUNTERMODEL_FOUND,
    evaluation_trace,
    interpretation_from_data,
    search_countermodel,
)


CAPSTONE_BLOCKED = "blocked"
CAPSTONE_COUNTERMODEL_FOUND = "countermodel_found"
CAPSTONE_PROOF_VERIFIED = "proof_verified"
CAPSTONE_NEEDS_REVISION = "needs_revision"
CAPSTONE_UNDETERMINED = "undetermined"


class FOLCapstoneError(ValueError):
    """Stable validation error for authored capstone data."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def _require_mapping(value, code, message):
    if not isinstance(value, Mapping):
        raise FOLCapstoneError(code, message)
    return value


def _parse_sentence(source, signature, label):
    formula = parse_fol(source, signature)
    if not formula.is_sentence:
        raise FOLCapstoneError(
            "capstone.open_formula",
            f"{label} serbest değişken içeremez.",
        )
    return formula


def _proof_matches_argument(proof, premises, conclusion, signature):
    if not isinstance(proof, Mapping):
        return False
    proof_premises = proof.get("premises")
    if not isinstance(proof_premises, list) or len(proof_premises) != len(premises):
        return False
    try:
        expected = [_parse_sentence(item, signature, "Argüman öncülü") for item in premises]
        supplied = [_parse_sentence(item, signature, "Kanıt öncülü") for item in proof_premises]
        expected_target = _parse_sentence(conclusion, signature, "Argüman sonucu")
        supplied_target = _parse_sentence(proof.get("target"), signature, "Kanıt hedefi")
    except (TypeError, ValueError):
        return False

    unmatched = list(supplied)
    for formula in expected:
        match_index = next(
            (
                index
                for index, candidate in enumerate(unmatched)
                if formulas_alpha_equivalent(formula, candidate)
            ),
            None,
        )
        if match_index is None:
            return False
        unmatched.pop(match_index)
    return not unmatched and formulas_alpha_equivalent(expected_target, supplied_target)


def reconcile_capstone_results(
    *,
    translations_accepted: bool,
    countermodel_status: str,
    proof_provided: bool,
    proof_verified: bool,
):
    """Classify independent results without turning sample failure into proof."""

    blocking_conflict = proof_verified and countermodel_status == COUNTERMODEL_FOUND
    if blocking_conflict:
        status = CAPSTONE_BLOCKED
    elif countermodel_status == COUNTERMODEL_FOUND:
        status = CAPSTONE_COUNTERMODEL_FOUND
    elif not translations_accepted:
        status = CAPSTONE_NEEDS_REVISION
    elif proof_verified:
        status = CAPSTONE_PROOF_VERIFIED
    elif proof_provided:
        status = CAPSTONE_NEEDS_REVISION
    else:
        status = CAPSTONE_UNDETERMINED

    return {
        "status": status,
        "blocking_conflict": blocking_conflict,
        "conflict_code": (
            "capstone.proof_countermodel_conflict" if blocking_conflict else None
        ),
        "sample_establishes_validity": False,
    }


def audit_fol_capstone(case, *, allowed_rules=F40_RULES):
    """Audit one serialisable translation/model/proof capstone case."""

    case = _require_mapping(
        case,
        "capstone.data_invalid",
        "Aşama projesi verisi bir sözlük olmalıdır.",
    )
    signature_data = _require_mapping(
        case.get("signature"),
        "capstone.signature_missing",
        "Aşama projesi geçerli bir FOL imzası taşımalıdır.",
    )
    signature = signature_from_data(signature_data)

    argument = _require_mapping(
        case.get("argument"),
        "capstone.argument_missing",
        "Aşama projesi bir argüman taşımalıdır.",
    )
    premises = argument.get("premises")
    conclusion = argument.get("conclusion")
    if not isinstance(premises, list) or not premises:
        raise FOLCapstoneError(
            "capstone.premises_invalid",
            "Argüman en az bir öncül içermelidir.",
        )
    parsed_premises = [
        _parse_sentence(source, signature, f"{index + 1}. öncül")
        for index, source in enumerate(premises)
    ]
    parsed_conclusion = _parse_sentence(conclusion, signature, "Sonuç")

    tasks = case.get("translation_tasks")
    if not isinstance(tasks, list) or not tasks:
        raise FOLCapstoneError(
            "capstone.translation_tasks_invalid",
            "Her argüman formülü için çeviri görevi verilmelidir.",
        )

    translation_items = []
    covered_slots = set()
    for index, task in enumerate(tasks):
        task = _require_mapping(
            task,
            "capstone.translation_task_invalid",
            f"{index + 1}. çeviri görevi bir sözlük olmalıdır.",
        )
        role = task.get("role")
        position = task.get("position") if role == "premise" else None
        if role == "premise" and isinstance(position, int) and not isinstance(position, bool):
            if position < 0 or position >= len(parsed_premises):
                raise FOLCapstoneError(
                    "capstone.translation_position_invalid",
                    "Çeviri görevinin öncül sırası argüman dışında kaldı.",
                )
            slot = ("premise", position)
            argument_formula = parsed_premises[position]
        elif role == "conclusion" and position is None:
            slot = ("conclusion", None)
            argument_formula = parsed_conclusion
        else:
            raise FOLCapstoneError(
                "capstone.translation_role_invalid",
                "Çeviri görevi geçerli bir öncül sırası veya sonuç rolü taşımalıdır.",
            )
        if slot in covered_slots:
            raise FOLCapstoneError(
                "capstone.translation_slot_duplicate",
                "Aynı argüman formülü için birden fazla çeviri görevi verilemez.",
            )
        covered_slots.add(slot)

        accepted_sources = task.get("accepted_sources")
        if not isinstance(accepted_sources, list) or not accepted_sources:
            raise FOLCapstoneError(
                "capstone.translation_key_missing",
                "Çeviri görevi en az bir kabul edilen yapı taşımalıdır.",
            )
        accepted_formulas = [
            _parse_sentence(source, signature, "Çeviri anahtarı")
            for source in accepted_sources
        ]
        if not any(
            formulas_alpha_equivalent(argument_formula, accepted)
            for accepted in accepted_formulas
        ):
            raise FOLCapstoneError(
                "capstone.translation_argument_mismatch",
                "Çeviri anahtarı denetlenen argüman formülüyle eşleşmiyor.",
            )

        result = assess_fol_symbolization(
            task.get("candidate", ""),
            accepted_sources,
            signature,
        )
        translation_items.append(
            {
                "id": task.get("id") or f"translation-{index + 1}",
                "label": task.get("label", ""),
                "role": role,
                "position": position,
                **result,
            }
        )

    expected_slots = {
        *(("premise", index) for index in range(len(parsed_premises))),
        ("conclusion", None),
    }
    if covered_slots != expected_slots:
        raise FOLCapstoneError(
            "capstone.translation_coverage_incomplete",
            "Her öncül ve sonuç tam bir çeviri göreviyle kapsanmalıdır.",
        )

    models_data = case.get("models", [])
    if not isinstance(models_data, list):
        raise FOLCapstoneError(
            "capstone.models_invalid",
            "Model bankası bir liste olmalıdır.",
        )
    models = [interpretation_from_data(data, signature) for data in models_data]
    model_rows = []
    for model in models:
        premise_traces = [evaluation_trace(formula, model) for formula in parsed_premises]
        conclusion_trace = evaluation_trace(parsed_conclusion, model)
        model_rows.append(
            {
                "label": model.label,
                "premise_values": [trace["value"] for trace in premise_traces],
                "conclusion_value": conclusion_trace["value"],
                "premise_traces": premise_traces,
                "conclusion_trace": conclusion_trace,
            }
        )
    countermodel = search_countermodel(
        parsed_premises,
        parsed_conclusion,
        models,
        signature,
    )

    proof = case.get("proof")
    proof_provided = proof is not None
    proof_matches = proof_provided and _proof_matches_argument(
        proof,
        premises,
        conclusion,
        signature,
    )
    if proof_provided and not proof_matches:
        proof_issues = [
            {
                "code": "capstone.proof_argument_mismatch",
                "message": "Kanıt, çeviri ve model kanalındaki argümanla eşleşmiyor.",
                "line_id": None,
                "severity": "error",
            }
        ]
    elif proof_provided:
        proof_issues = audit_fol_fitch_proof(
            proof,
            signature,
            allowed_rules=allowed_rules,
        )
    else:
        proof_issues = []
    proof_verified = proof_provided and proof_matches and not proof_issues

    translations_accepted = all(item["accepted"] for item in translation_items)
    integrity = reconcile_capstone_results(
        translations_accepted=translations_accepted,
        countermodel_status=countermodel["status"],
        proof_provided=proof_provided,
        proof_verified=proof_verified,
    )

    return {
        "case_id": case.get("id", ""),
        "translation": {
            "accepted": translations_accepted,
            "items": translation_items,
        },
        "semantics": {
            "models": model_rows,
            "countermodel_search": countermodel,
            "sample_establishes_validity": False,
        },
        "proof": {
            "provided": proof_provided,
            "matches_argument": proof_matches,
            "verified": proof_verified,
            "issues": proof_issues,
        },
        "integrity": integrity,
    }
