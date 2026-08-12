"""Cross-check candidate Fitch proofs against the independent TFL semantics.

This module is deliberately separate from both engines.  A failed proof audit
does not establish semantic invalidity, while a verified proof paired with a
countervaluation would expose a conflict that must block curriculum release.
"""

from collections.abc import Iterable

from .logic_fitch import D26_RULES, audit_fitch_proof
from .logic_tfl_semantics import analyze_semantic_consequence


BRIDGE_CORROBORATED = "corroborated"
BRIDGE_PROOF_NOT_ESTABLISHED = "proof_not_established"
BRIDGE_COUNTERVALUATION = "countervaluation"
BRIDGE_SOUNDNESS_CONFLICT = "soundness_conflict"


def cross_validate_proof_semantics(
    proof,
    *,
    allowed_rules: Iterable[str] = D26_RULES,
):
    """Return independent proof-audit and semantic-consequence results.

    ``proof_not_established`` is intentionally not called a counterexample:
    an incomplete or malformed proof attempt can concern a semantically valid
    argument.  Conversely, a real countervaluation is decisive evidence that
    the argument is not semantically valid.
    """

    if not isinstance(proof, dict):
        raise TypeError("Kanıt verisi bir sözlük olmalıdır.")

    proof_issues = audit_fitch_proof(
        proof,
        allowed_rules=allowed_rules,
        require_complete=True,
    )
    semantic_result = analyze_semantic_consequence(
        proof.get("premises", []),
        proof.get("target"),
    )
    proof_verified = not proof_issues
    semantic_entails = semantic_result["entails"]

    if proof_verified and semantic_entails:
        bridge_status = BRIDGE_CORROBORATED
    elif proof_verified:
        bridge_status = BRIDGE_SOUNDNESS_CONFLICT
    elif semantic_entails:
        bridge_status = BRIDGE_PROOF_NOT_ESTABLISHED
    else:
        bridge_status = BRIDGE_COUNTERVALUATION

    return {
        "proof_id": proof.get("id"),
        "proof_verified": proof_verified,
        "proof_issue_codes": [issue["code"] for issue in proof_issues],
        "semantic_entails": semantic_entails,
        "countervaluations": semantic_result["countervaluations"],
        "row_count": semantic_result["row_count"],
        "bridge_status": bridge_status,
    }
