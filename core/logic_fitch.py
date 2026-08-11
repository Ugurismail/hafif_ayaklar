"""Structured Fitch proof auditing for release-candidate logic lessons.

The learner-facing course does not import this module yet.  It provides a
small, deterministic core for checking candidate proof fixtures before an
interactive proof editor is introduced.
"""

from collections.abc import Iterable

from .logic_tfl_semantics import TFLParseError, parse_tfl


D20_RULES = frozenset({"PR", "AS", "R"})
REQUIRED_LINE_FIELDS = frozenset(
    {"id", "formula", "rule", "citations", "depth", "opens", "closes"}
)


def _issue(code, message, *, line_id=None, severity="error"):
    return {
        "code": code,
        "message": message,
        "line_id": line_id,
        "severity": severity,
    }


def _scope_is_accessible(source_path, current_path):
    """Return whether a line in ``source_path`` is visible in ``current_path``."""

    return current_path[: len(source_path)] == source_path


def _parse_formula(source, *, label, line_id=None):
    try:
        return parse_tfl(source), None
    except (TFLParseError, TypeError) as exc:
        return None, _issue(
            "formula.invalid",
            f"{label} geçerli bir TFL cümlesi değil: {exc}",
            line_id=line_id,
        )


def audit_fitch_proof(
    proof,
    *,
    allowed_rules: Iterable[str] = D20_RULES,
    require_complete=True,
):
    """Audit one structured Fitch proof and return ordered issue dictionaries.

    D20 deliberately enables only premise, assumption, and reiteration.  The
    line/scope representation is already suitable for later introduction and
    elimination rules, whose validators will be added lesson by lesson.
    """

    issues = []
    if not isinstance(proof, dict):
        return [_issue("proof.invalid", "Kanıt verisi bir sözlük olmalıdır.")]

    premises = proof.get("premises", [])
    if not isinstance(premises, list):
        issues.append(
            _issue("proof.premises_invalid", "Öncüller bir liste olmalıdır.")
        )
        premises = []

    parsed_premises = []
    for index, premise in enumerate(premises, start=1):
        parsed, problem = _parse_formula(
            premise,
            label=f"{index}. öncül",
        )
        if problem:
            issues.append(problem)
        else:
            parsed_premises.append(parsed)

    parsed_target, target_problem = _parse_formula(
        proof.get("target"),
        label="Hedef",
    )
    if target_problem:
        issues.append(target_problem)

    lines = proof.get("lines", [])
    if not isinstance(lines, list):
        issues.append(
            _issue("proof.lines_invalid", "Kanıt satırları bir liste olmalıdır.")
        )
        lines = []

    allowed_rules = frozenset(allowed_rules)
    all_line_positions = {}
    for position, line in enumerate(lines):
        if not isinstance(line, dict):
            continue
        line_id = line.get("id")
        if isinstance(line_id, str) and line_id not in all_line_positions:
            all_line_positions[line_id] = position

    active_scopes = []
    opened_scopes = set()
    seen_lines = {}
    last_line = None

    for position, line in enumerate(lines):
        if not isinstance(line, dict):
            issues.append(
                _issue(
                    "line.invalid",
                    f"{position + 1}. satır bir sözlük olmalıdır.",
                )
            )
            continue

        missing = REQUIRED_LINE_FIELDS - set(line)
        line_id = line.get("id")
        issue_line_id = line_id if isinstance(line_id, str) else None
        if missing:
            issues.append(
                _issue(
                    "line.fields_missing",
                    "Eksik satır alanları: " + ", ".join(sorted(missing)),
                    line_id=issue_line_id,
                )
            )
            continue

        if not isinstance(line_id, str) or not line_id.strip():
            issues.append(
                _issue(
                    "line.id_invalid",
                    "Satır kimliği boş olmayan bir metin olmalıdır.",
                )
            )
            line_id = f"__invalid_{position}"
            issue_line_id = None
        elif line_id in seen_lines:
            issues.append(
                _issue(
                    "line.id_duplicate",
                    f"{line_id} satır kimliği birden fazla kullanılmış.",
                    line_id=line_id,
                )
            )

        closes = line.get("closes")
        if not isinstance(closes, list) or not all(
            isinstance(scope_id, str) and scope_id for scope_id in closes
        ):
            issues.append(
                _issue(
                    "scope.closes_invalid",
                    "closes alanı kapsam kimliklerinden oluşan bir liste olmalıdır.",
                    line_id=issue_line_id,
                )
            )
            closes = []

        for scope_id in closes:
            if not active_scopes or active_scopes[-1] != scope_id:
                issues.append(
                    _issue(
                        "scope.close_order",
                        f"{scope_id} açık kapsam yığınının tepesinde değil.",
                        line_id=issue_line_id,
                    )
                )
                continue
            active_scopes.pop()

        opens = line.get("opens")
        if opens is not None:
            if not isinstance(opens, str) or not opens:
                issues.append(
                    _issue(
                        "scope.opens_invalid",
                        "opens alanı boş olmayan bir kapsam kimliği olmalıdır.",
                        line_id=issue_line_id,
                    )
                )
                opens = None
            elif opens in opened_scopes:
                issues.append(
                    _issue(
                        "scope.id_duplicate",
                        f"{opens} kapsam kimliği daha önce kullanılmış.",
                        line_id=issue_line_id,
                    )
                )
                opens = None
            else:
                opened_scopes.add(opens)
                active_scopes.append(opens)

        scope_path = tuple(active_scopes)
        depth = line.get("depth")
        if not isinstance(depth, int) or isinstance(depth, bool) or depth < 0:
            issues.append(
                _issue(
                    "line.depth_invalid",
                    "Kapsam derinliği sıfır veya daha büyük bir tam sayı olmalıdır.",
                    line_id=issue_line_id,
                )
            )
        elif depth != len(scope_path):
            issues.append(
                _issue(
                    "line.depth_mismatch",
                    f"Satır derinliği {depth}, açık kapsam sayısı {len(scope_path)}.",
                    line_id=issue_line_id,
                )
            )

        parsed_formula, formula_problem = _parse_formula(
            line.get("formula"),
            label="Satır formülü",
            line_id=issue_line_id,
        )
        if formula_problem:
            issues.append(formula_problem)

        rule = line.get("rule")
        if not isinstance(rule, str) or not rule:
            issues.append(
                _issue(
                    "rule.invalid",
                    "Kural etiketi boş olmayan bir metin olmalıdır.",
                    line_id=issue_line_id,
                )
            )
            rule = ""
        elif rule not in allowed_rules:
            issues.append(
                _issue(
                    "rule.not_available",
                    f"{rule} kuralı bu derste henüz kullanılamaz.",
                    line_id=issue_line_id,
                )
            )

        citations = line.get("citations")
        if not isinstance(citations, list):
            issues.append(
                _issue(
                    "citation.list_invalid",
                    "Atıflar bir liste olmalıdır.",
                    line_id=issue_line_id,
                )
            )
            citations = []

        resolved_line_citations = []
        for citation in citations:
            if not isinstance(citation, dict) or citation.get("kind") != "line":
                issues.append(
                    _issue(
                        "citation.kind_invalid",
                        "Satır atıfları {kind: 'line', id: '...'} biçiminde olmalıdır.",
                        line_id=issue_line_id,
                    )
                )
                continue

            cited_id = citation.get("id")
            if not isinstance(cited_id, str) or not cited_id:
                issues.append(
                    _issue(
                        "citation.id_invalid",
                        "Atıf geçerli bir satır kimliği taşımalıdır.",
                        line_id=issue_line_id,
                    )
                )
                continue

            cited_line = seen_lines.get(cited_id)
            if cited_line is None:
                code = (
                    "citation.forward"
                    if all_line_positions.get(cited_id, -1) >= position
                    else "citation.unknown"
                )
                issues.append(
                    _issue(
                        code,
                        f"{cited_id} satırı henüz erişilebilir bir kaynak değil.",
                        line_id=issue_line_id,
                    )
                )
                continue

            if not _scope_is_accessible(cited_line["scope_path"], scope_path):
                issues.append(
                    _issue(
                        "citation.inaccessible",
                        f"{cited_id} kapanmış veya kardeş bir alt kanıtta.",
                        line_id=issue_line_id,
                    )
                )
                continue
            resolved_line_citations.append(cited_line)

        if opens is not None and rule != "AS":
            issues.append(
                _issue(
                    "scope.open_requires_assumption",
                    "Yeni kapsam yalnız AS satırıyla açılabilir.",
                    line_id=issue_line_id,
                )
            )

        if rule == "PR":
            if citations:
                issues.append(
                    _issue(
                        "rule.pr_has_citations",
                        "PR satırı başka satıra atıf yapmaz.",
                        line_id=issue_line_id,
                    )
                )
            if opens is not None:
                issues.append(
                    _issue(
                        "rule.pr_opens_scope",
                        "PR satırı alt kanıt açmaz.",
                        line_id=issue_line_id,
                    )
                )
            if scope_path:
                issues.append(
                    _issue(
                        "rule.pr_not_root",
                        "PR yalnız kanıtın kök kapsamında kullanılabilir.",
                        line_id=issue_line_id,
                    )
                )
            if (
                parsed_formula is not None
                and parsed_formula not in parsed_premises
            ):
                issues.append(
                    _issue(
                        "rule.pr_not_premise",
                        "PR satırı problemde verilen öncüllerden biri olmalıdır.",
                        line_id=issue_line_id,
                    )
                )
        elif rule == "AS":
            if citations:
                issues.append(
                    _issue(
                        "rule.as_has_citations",
                        "AS satırı başka satıra atıf yapmaz.",
                        line_id=issue_line_id,
                    )
                )
            if opens is None:
                issues.append(
                    _issue(
                        "rule.as_missing_scope",
                        "AS satırı yeni ve benzersiz bir kapsam açmalıdır.",
                        line_id=issue_line_id,
                    )
                )
        elif rule == "R":
            if len(citations) != 1:
                issues.append(
                    _issue(
                        "rule.r_citation_count",
                        "R tam olarak bir erişilebilir satıra atıf yapmalıdır.",
                        line_id=issue_line_id,
                    )
                )
            elif len(resolved_line_citations) == 1 and (
                parsed_formula is not None
                and resolved_line_citations[0]["formula"] is not None
                and parsed_formula != resolved_line_citations[0]["formula"]
            ):
                issues.append(
                    _issue(
                        "rule.r_formula_mismatch",
                        "R kaynak satırdaki formülü değiştirmeden tekrarlar.",
                        line_id=issue_line_id,
                    )
                )

        record = {
            "id": line_id,
            "formula": parsed_formula,
            "scope_path": scope_path,
            "depth": depth,
            "position": position,
        }
        if line_id not in seen_lines:
            seen_lines[line_id] = record
        last_line = record

    if require_complete:
        if active_scopes:
            issues.append(
                _issue(
                    "proof.scope_unclosed",
                    "Tamamlanmış kanıtta açık alt kanıt kalamaz.",
                    severity="incomplete",
                )
            )
        if last_line is None:
            issues.append(
                _issue(
                    "proof.empty",
                    "Tamamlanmış kanıt en az bir satır içermelidir.",
                    severity="incomplete",
                )
            )
        else:
            if last_line["scope_path"]:
                issues.append(
                    _issue(
                        "proof.target_in_subproof",
                        "Hedef satır kök kapsamda erişilebilir olmalıdır.",
                        line_id=last_line["id"],
                        severity="incomplete",
                    )
                )
            if (
                parsed_target is not None
                and last_line["formula"] is not None
                and parsed_target != last_line["formula"]
            ):
                issues.append(
                    _issue(
                        "proof.target_not_reached",
                        "Son kök satır hedef formülle eşleşmiyor.",
                        line_id=last_line["id"],
                        severity="incomplete",
                    )
                )

    return issues
