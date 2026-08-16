"""Structured Fitch auditing for the isolated first-order curriculum.

The live propositional proof checker deliberately remains untouched.  This
module reuses its serialisable line/scope contract, but parses every formula
with the Stage E FOL parser and tracks assumption dependencies explicitly so
the eigenname restrictions on ``∀I`` and ``∃E`` are enforceable.
"""

from collections.abc import Iterable
from dataclasses import dataclass

from .logic_fol import (
    FOLFormula,
    FOLParseError,
    FOLSignature,
    parse_fol,
    substitute_free_term,
)


PROPOSITIONAL_RULES = frozenset(
    {
        "PR",
        "AS",
        "R",
        "∧I",
        "∧E",
        "→I",
        "→E",
        "¬I",
        "¬E",
        "X",
        "IP",
        "∨I",
        "∨E",
        "↔I",
        "↔E",
        "DS",
        "MT",
        "DNE",
        "LEM",
        "DeM",
    }
)
F38_RULES = PROPOSITIONAL_RULES | frozenset({"∀E", "∃I"})
F39_RULES = F38_RULES | frozenset({"∀I", "∃E"})
F40_RULES = F39_RULES | frozenset({"=I", "=E"})
REQUIRED_LINE_FIELDS = frozenset(
    {"id", "formula", "rule", "citations", "depth", "opens", "closes"}
)


@dataclass(frozen=True)
class _Contradiction:
    def render(self):
        return "⊥"


CONTRADICTION = _Contradiction()


def _issue(code, message, *, line_id=None, severity="error"):
    return {
        "code": code,
        "message": message,
        "line_id": line_id,
        "severity": severity,
    }


def _same(left, right):
    if left is CONTRADICTION or right is CONTRADICTION:
        return left is right
    if not isinstance(left, FOLFormula) or not isinstance(right, FOLFormula):
        return False
    return _proof_structure_key(left) == _proof_structure_key(right)


def _proof_structure_key(formula):
    """Alpha-stable proof key that preserves the printed order of identity.

    The syntax curriculum treats ``a=b`` and ``b=a`` as semantically
    interchangeable.  A Fitch reiteration must nevertheless preserve the
    exact formula structure; the reverse identity requires an explicit
    identity step.
    """

    binder_counter = 0
    binders = {}

    def term_key(term):
        if term.kind == "name":
            return ("name", term.symbol)
        stack = binders.get(term.symbol, [])
        return ("bound", stack[-1]) if stack else ("free", term.symbol)

    def visit(node):
        nonlocal binder_counter
        if node.kind == "predicate":
            return ("predicate", node.predicate, tuple(term_key(term) for term in node.terms))
        if node.kind == "identity":
            return ("identity", term_key(node.terms[0]), term_key(node.terms[1]))
        if node.kind == "negation":
            return ("negation", visit(node.body))
        if node.kind == "binary":
            return ("binary", node.operator, visit(node.left), visit(node.right))
        if node.kind == "quantifier":
            binder_id = binder_counter
            binder_counter += 1
            stack = binders.setdefault(node.variable, [])
            stack.append(binder_id)
            body = visit(node.body)
            stack.pop()
            if not stack:
                binders.pop(node.variable, None)
            return ("quantifier", node.operator, body)
        raise ValueError(f"Bilinmeyen FOL düğüm türü: {node.kind!r}.")

    return visit(formula)


def _scope_is_accessible(source_path, current_path):
    return current_path[: len(source_path)] == source_path


def _parse_formula(source, signature, *, label, line_id=None):
    if source == "⊥":
        return CONTRADICTION, None
    try:
        formula = parse_fol(source, signature)
    except (FOLParseError, TypeError) as exc:
        return None, _issue(
            "formula.invalid",
            f"{label} geçerli bir FOL formülü değil: {exc}",
            line_id=line_id,
        )
    if not formula.is_sentence:
        return None, _issue(
            "formula.open",
            f"{label} açık değişken içeriyor; kanıt satırları kapalı cümle olmalıdır.",
            line_id=line_id,
        )
    return formula, None


def _formula_names(formula):
    names = set()

    def visit(node):
        if node is CONTRADICTION:
            return
        if node.kind in {"predicate", "identity"}:
            names.update(term.symbol for term in node.terms if term.kind == "name")
            return
        if node.kind == "negation":
            visit(node.body)
            return
        if node.kind == "binary":
            visit(node.left)
            visit(node.right)
            return
        if node.kind == "quantifier":
            visit(node.body)

    visit(formula)
    return frozenset(names)


def _is_negation_of(negated, formula):
    return (
        isinstance(negated, FOLFormula)
        and negated.kind == "negation"
        and _same(negated.body, formula)
    )


def _are_contradictories(first, second):
    return _is_negation_of(first, second) or _is_negation_of(second, first)


def _substitution_names(quantified, instance, signature):
    """Return names making ``instance`` a substitution of the matrix.

    An empty tuple with ``vacuous=True`` means the quantified variable does
    not occur free in its matrix and the matrix itself matches the instance.
    """

    matches = []
    for name in sorted(signature.names):
        candidate = substitute_free_term(
            quantified.body,
            quantified.variable,
            name,
            signature,
        )
        if _same(candidate, instance):
            matches.append(name)
    vacuous = _same(quantified.body, instance)
    return tuple(matches), vacuous


def _identity_substitution_matches(source, target, old_name, new_name):
    """Check that target changes one or more selected free name occurrences."""

    replacements = 0

    def term_matches(old, new):
        nonlocal replacements
        if old.kind != new.kind:
            return False
        if old.kind == "name" and old.symbol == old_name:
            if new.symbol == new_name:
                replacements += 1
                return True
            return new.symbol == old_name
        return old.symbol == new.symbol

    def visit(left, right):
        if left.kind != right.kind:
            return False
        if left.kind == "predicate":
            return (
                left.predicate == right.predicate
                and len(left.terms) == len(right.terms)
                and all(term_matches(a, b) for a, b in zip(left.terms, right.terms))
            )
        if left.kind == "identity":
            return all(term_matches(a, b) for a, b in zip(left.terms, right.terms))
        if left.kind == "negation":
            return visit(left.body, right.body)
        if left.kind == "binary":
            return (
                left.operator == right.operator
                and visit(left.left, right.left)
                and visit(left.right, right.right)
            )
        if left.kind == "quantifier":
            return (
                left.operator == right.operator
                and left.variable == right.variable
                and visit(left.body, right.body)
            )
        return False

    return visit(source, target) and replacements > 0


def _de_morgan_matches(source, target):
    if source.kind == "negation" and source.body.kind == "binary":
        compound = source.body
        if compound.operator == "∧" and target.kind == "binary" and target.operator == "∨":
            return _is_negation_of(target.left, compound.left) and _is_negation_of(
                target.right, compound.right
            )
        if compound.operator == "∨" and target.kind == "binary" and target.operator == "∧":
            return _is_negation_of(target.left, compound.left) and _is_negation_of(
                target.right, compound.right
            )
    if source.kind == "binary" and source.operator in {"∧", "∨"}:
        if source.left.kind != "negation" or source.right.kind != "negation":
            return False
        if target.kind != "negation" or target.body.kind != "binary":
            return False
        expected = "∨" if source.operator == "∧" else "∧"
        return (
            target.body.operator == expected
            and _same(source.left.body, target.body.left)
            and _same(source.right.body, target.body.right)
        )
    return False


def audit_fol_fitch_proof(
    proof,
    signature: FOLSignature,
    *,
    allowed_rules: Iterable[str] = F38_RULES,
    require_complete=True,
):
    """Audit one FOL Fitch proof and return ordered, stable issue records."""

    if not isinstance(signature, FOLSignature):
        raise TypeError("signature bir FOLSignature olmalıdır.")
    if not isinstance(proof, dict):
        return [_issue("proof.invalid", "Kanıt verisi bir sözlük olmalıdır.")]

    issues = []
    premises = proof.get("premises", [])
    if not isinstance(premises, list):
        issues.append(_issue("proof.premises_invalid", "Öncüller bir liste olmalıdır."))
        premises = []

    parsed_premises = []
    dependency_formulas = {}
    for index, premise in enumerate(premises):
        parsed, problem = _parse_formula(
            premise,
            signature,
            label=f"{index + 1}. öncül",
        )
        if problem:
            issues.append(problem)
        else:
            parsed_premises.append((index, parsed))
            dependency_formulas[("premise", index)] = parsed

    parsed_target, target_problem = _parse_formula(
        proof.get("target"),
        signature,
        label="Hedef",
    )
    if target_problem:
        issues.append(target_problem)

    lines = proof.get("lines", [])
    if not isinstance(lines, list):
        issues.append(_issue("proof.lines_invalid", "Kanıt satırları bir liste olmalıdır."))
        lines = []

    all_positions = {}
    for position, line in enumerate(lines):
        if isinstance(line, dict):
            line_id = line.get("id")
            if isinstance(line_id, str) and line_id and line_id not in all_positions:
                all_positions[line_id] = position

    allowed_rules = frozenset(allowed_rules)
    active_scopes = []
    opened_scopes = set()
    scope_records = {}
    seen_lines = {}
    last_line = None

    for position, line in enumerate(lines):
        if not isinstance(line, dict):
            issues.append(_issue("line.invalid", f"{position + 1}. satır bir sözlük olmalıdır."))
            continue

        line_id = line.get("id")
        issue_line_id = line_id if isinstance(line_id, str) and line_id else None
        missing = REQUIRED_LINE_FIELDS - set(line)
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
            issues.append(_issue("line.id_invalid", "Satır kimliği boş olamaz."))
            line_id = f"__invalid_{position}"
        elif line_id in seen_lines:
            issues.append(
                _issue("line.id_duplicate", f"{line_id} birden fazla kullanılmış.", line_id=line_id)
            )

        closes = line.get("closes")
        if not isinstance(closes, list) or not all(
            isinstance(scope_id, str) and scope_id for scope_id in closes
        ):
            issues.append(
                _issue(
                    "scope.closes_invalid",
                    "closes kapsam kimliklerinden oluşan bir liste olmalıdır.",
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
            scope_records[scope_id]["closed_at"] = position
            active_scopes.pop()

        opens = line.get("opens")
        if opens is not None:
            if not isinstance(opens, str) or not opens:
                issues.append(
                    _issue("scope.opens_invalid", "opens geçerli bir kapsam kimliği olmalıdır.", line_id=issue_line_id)
                )
                opens = None
            elif opens in opened_scopes:
                issues.append(
                    _issue("scope.id_duplicate", f"{opens} daha önce kullanılmış.", line_id=issue_line_id)
                )
                opens = None
            else:
                parent_path = tuple(active_scopes)
                opened_scopes.add(opens)
                active_scopes.append(opens)
                scope_records[opens] = {
                    "id": opens,
                    "start_id": line_id,
                    "parent_path": parent_path,
                    "scope_path": tuple(active_scopes),
                    "closed_at": None,
                    "last_direct_line_id": None,
                }

        scope_path = tuple(active_scopes)
        depth = line.get("depth")
        if not isinstance(depth, int) or isinstance(depth, bool) or depth < 0:
            issues.append(_issue("line.depth_invalid", "Derinlik negatif olmayan tam sayı olmalıdır.", line_id=issue_line_id))
        elif depth != len(scope_path):
            issues.append(
                _issue(
                    "line.depth_mismatch",
                    f"Satır derinliği {depth}; açık kapsam sayısı {len(scope_path)}.",
                    line_id=issue_line_id,
                )
            )

        parsed_formula, formula_problem = _parse_formula(
            line.get("formula"),
            signature,
            label="Satır formülü",
            line_id=issue_line_id,
        )
        if formula_problem:
            issues.append(formula_problem)

        rule = line.get("rule")
        if not isinstance(rule, str) or not rule:
            issues.append(_issue("rule.invalid", "Kural etiketi boş olamaz.", line_id=issue_line_id))
            rule = ""
        elif rule not in allowed_rules:
            issues.append(
                _issue("rule.not_available", f"{rule} bu derste kullanılamaz.", line_id=issue_line_id)
            )

        citations = line.get("citations")
        if not isinstance(citations, list):
            issues.append(_issue("citation.list_invalid", "Atıflar liste olmalıdır.", line_id=issue_line_id))
            citations = []

        line_refs = []
        subproof_refs = []
        for citation in citations:
            if not isinstance(citation, dict):
                issues.append(_issue("citation.kind_invalid", "Atıf sözlük olmalıdır.", line_id=issue_line_id))
                continue
            kind = citation.get("kind")
            if kind == "line":
                cited_id = citation.get("id")
                cited = seen_lines.get(cited_id)
                if cited is None:
                    code = "citation.forward" if all_positions.get(cited_id, -1) >= position else "citation.unknown"
                    issues.append(_issue(code, f"{cited_id} erişilebilir bir satır değil.", line_id=issue_line_id))
                    continue
                if not _scope_is_accessible(cited["scope_path"], scope_path):
                    issues.append(_issue("citation.inaccessible", f"{cited_id} kapanmış veya kardeş kapsamda.", line_id=issue_line_id))
                    continue
                line_refs.append(cited)
                continue
            if kind != "subproof":
                issues.append(_issue("citation.kind_invalid", "Atıf türü line veya subproof olmalıdır.", line_id=issue_line_id))
                continue
            start_id = citation.get("start")
            end_id = citation.get("end")
            start = seen_lines.get(start_id)
            end = seen_lines.get(end_id)
            if start is None or end is None:
                has_forward = any(
                    all_positions.get(item, -1) >= position
                    for item, found in ((start_id, start), (end_id, end))
                    if found is None
                )
                issues.append(
                    _issue(
                        "citation.subproof_forward" if has_forward else "citation.subproof_unknown",
                        "Alt kanıt aralığı erişilebilir değil.",
                        line_id=issue_line_id,
                    )
                )
                continue
            scope_id = start.get("opens")
            cited_scope = scope_records.get(scope_id)
            if start.get("rule") != "AS" or cited_scope is None:
                issues.append(_issue("citation.subproof_start_invalid", "Alt kanıt AS satırıyla başlamalıdır.", line_id=issue_line_id))
                continue
            if end["scope_path"] != cited_scope["scope_path"]:
                issues.append(_issue("citation.subproof_end_scope", "Alt kanıtın son satırı doğrudan o kapsamda olmalıdır.", line_id=issue_line_id))
                continue
            if cited_scope["last_direct_line_id"] != end_id:
                issues.append(_issue("citation.subproof_end_not_last", "Alt kanıt atfı son doğrudan satırda bitmelidir.", line_id=issue_line_id))
                continue
            if cited_scope["closed_at"] is None:
                issues.append(_issue("citation.subproof_open", "Alt kanıt atıftan önce kapatılmalıdır.", line_id=issue_line_id))
                continue
            if not _scope_is_accessible(cited_scope["parent_path"], scope_path):
                issues.append(_issue("citation.subproof_inaccessible", "Alt kanıtın ana kapsamı erişilebilir değil.", line_id=issue_line_id))
                continue
            subproof_refs.append({"start": start, "end": end, "scope": cited_scope})

        if opens is not None and rule != "AS":
            issues.append(_issue("scope.open_requires_assumption", "Yeni kapsam yalnız AS ile açılır.", line_id=issue_line_id))

        def add(code, message, severity="error"):
            issues.append(_issue(code, message, line_id=issue_line_id, severity=severity))

        def require_counts(lines_count, subproof_count, code, message):
            if len(line_refs) != lines_count or len(subproof_refs) != subproof_count or len(citations) != lines_count + subproof_count:
                add(code, message)
                return False
            return True

        if rule == "PR":
            if citations:
                add("rule.pr_has_citations", "PR satırı atıf yapmaz.")
            if scope_path:
                add("rule.pr_not_root", "PR yalnız kök kapsamda kullanılabilir.")
            if parsed_formula is not None and not any(_same(parsed_formula, premise) for _, premise in parsed_premises):
                add("rule.pr_not_premise", "PR formülü verilen öncüllerden biri değildir.")
        elif rule == "AS":
            if citations:
                add("rule.as_has_citations", "AS satırı atıf yapmaz.")
            if opens is None:
                add("rule.as_missing_scope", "AS yeni bir kapsam açmalıdır.")
        elif rule == "R" and require_counts(1, 0, "rule.r_citation_count", "R bir satıra atıf yapmalıdır."):
            if parsed_formula is not None and not _same(parsed_formula, line_refs[0]["formula"]):
                add("rule.r_formula_mismatch", "R formülü değiştiremez.")
        elif rule == "∧I" and require_counts(2, 0, "rule.conjunction_introduction_citation_count", "∧I iki satıra atıf yapmalıdır."):
            if parsed_formula is None or parsed_formula.kind != "binary" or parsed_formula.operator != "∧":
                add("rule.conjunction_introduction_shape", "∧I sonucu bir bağlaç olmalıdır.")
            elif not (
                _same(parsed_formula.left, line_refs[0]["formula"])
                and _same(parsed_formula.right, line_refs[1]["formula"])
            ):
                add("rule.conjunction_introduction_mismatch", "∧I bileşenleri atıf sırasıyla eşleşmelidir.")
        elif rule == "∧E" and require_counts(1, 0, "rule.conjunction_elimination_citation_count", "∧E bir satıra atıf yapmalıdır."):
            source = line_refs[0]["formula"]
            if source is CONTRADICTION or source.kind != "binary" or source.operator != "∧":
                add("rule.conjunction_elimination_source", "∧E kaynağı bir bağlaç olmalıdır.")
            elif parsed_formula is not None and not (_same(parsed_formula, source.left) or _same(parsed_formula, source.right)):
                add("rule.conjunction_elimination_mismatch", "∧E doğrudan bileşenlerden birini verir.")
        elif rule == "→E" and require_counts(2, 0, "rule.conditional_elimination_citation_count", "→E iki satıra atıf yapmalıdır."):
            conditionals = [ref["formula"] for ref in line_refs if ref["formula"] is not CONTRADICTION and ref["formula"].kind == "binary" and ref["formula"].operator == "→"]
            licensed = any(
                any(_same(other["formula"], conditional.left) for other in line_refs if other["formula"] is not conditional)
                and parsed_formula is not None
                and _same(parsed_formula, conditional.right)
                for conditional in conditionals
            )
            if not licensed:
                add("rule.conditional_elimination_mismatch", "→E, A→B ve A'dan B çıkarır.")
        elif rule == "→I" and require_counts(0, 1, "rule.conditional_introduction_citation_count", "→I bir kapalı alt kanıta atıf yapmalıdır."):
            subproof = subproof_refs[0]
            if parsed_formula is None or parsed_formula.kind != "binary" or parsed_formula.operator != "→" or not _same(parsed_formula.left, subproof["start"]["formula"]) or not _same(parsed_formula.right, subproof["end"]["formula"]):
                add("rule.conditional_introduction_mismatch", "→I sonucu varsayım ve alt kanıt sonucuyla eşleşmelidir.")
        elif rule == "¬E" and require_counts(2, 0, "rule.negation_elimination_citation_count", "¬E iki satıra atıf yapmalıdır."):
            if parsed_formula is not CONTRADICTION or not _are_contradictories(line_refs[0]["formula"], line_refs[1]["formula"]):
                add("rule.negation_elimination_mismatch", "¬E, A ve ¬A'dan ⊥ çıkarır.")
        elif rule == "¬I" and require_counts(0, 1, "rule.negation_introduction_citation_count", "¬I bir kapalı alt kanıta atıf yapmalıdır."):
            subproof = subproof_refs[0]
            if parsed_formula is None or parsed_formula is CONTRADICTION or parsed_formula.kind != "negation" or subproof["end"]["formula"] is not CONTRADICTION or not _same(parsed_formula.body, subproof["start"]["formula"]):
                add("rule.negation_introduction_mismatch", "¬I, A varsayımından ⊥ üreten alt kanıtla ¬A çıkarır.")
        elif rule == "X" and require_counts(1, 0, "rule.explosion_citation_count", "X bir ⊥ satırına atıf yapmalıdır."):
            if line_refs[0]["formula"] is not CONTRADICTION:
                add("rule.explosion_source", "X yalnız ⊥ kaynağından uygulanır.")
        elif rule == "IP" and require_counts(0, 1, "rule.indirect_proof_citation_count", "IP bir kapalı alt kanıta atıf yapmalıdır."):
            subproof = subproof_refs[0]
            if subproof["end"]["formula"] is not CONTRADICTION or parsed_formula is None or parsed_formula is CONTRADICTION or not _is_negation_of(subproof["start"]["formula"], parsed_formula):
                add("rule.indirect_proof_mismatch", "IP, ¬A varsayımından ⊥ üretip A çıkarır.")
        elif rule == "∨I" and require_counts(1, 0, "rule.disjunction_introduction_citation_count", "∨I bir satıra atıf yapmalıdır."):
            if parsed_formula is None or parsed_formula.kind != "binary" or parsed_formula.operator != "∨" or not (_same(line_refs[0]["formula"], parsed_formula.left) or _same(line_refs[0]["formula"], parsed_formula.right)):
                add("rule.disjunction_introduction_mismatch", "∨I kaynağı sonuç ayrışımının bir bileşeni yapar.")
        elif rule == "∨E" and require_counts(1, 2, "rule.disjunction_elimination_citation_count", "∨E bir ayrışım ve iki alt kanıta atıf yapmalıdır."):
            disjunction = line_refs[0]["formula"]
            starts = [item["start"]["formula"] for item in subproof_refs]
            ends = [item["end"]["formula"] for item in subproof_refs]
            if disjunction is CONTRADICTION or disjunction.kind != "binary" or disjunction.operator != "∨" or not ((_same(starts[0], disjunction.left) and _same(starts[1], disjunction.right)) or (_same(starts[1], disjunction.left) and _same(starts[0], disjunction.right))) or parsed_formula is None or not all(_same(end, parsed_formula) for end in ends):
                add("rule.disjunction_elimination_mismatch", "∨E iki ayrışan varsayımdan aynı sonucu üretmelidir.")
        elif rule == "↔I" and require_counts(0, 2, "rule.biconditional_introduction_citation_count", "↔I iki alt kanıta atıf yapmalıdır."):
            if parsed_formula is None or parsed_formula.kind != "binary" or parsed_formula.operator != "↔":
                add("rule.biconditional_introduction_shape", "↔I sonucu çift koşul olmalıdır.")
            else:
                pairs = [(item["start"]["formula"], item["end"]["formula"]) for item in subproof_refs]
                if not any(_same(a, parsed_formula.left) and _same(b, parsed_formula.right) for a, b in pairs) or not any(_same(a, parsed_formula.right) and _same(b, parsed_formula.left) for a, b in pairs):
                    add("rule.biconditional_introduction_mismatch", "↔I iki yönü ayrı alt kanıtlarla göstermelidir.")
        elif rule == "↔E" and require_counts(2, 0, "rule.biconditional_elimination_citation_count", "↔E iki satıra atıf yapmalıdır."):
            biconditionals = [ref["formula"] for ref in line_refs if ref["formula"] is not CONTRADICTION and ref["formula"].kind == "binary" and ref["formula"].operator == "↔"]
            licensed = any(
                parsed_formula is not None
                and any(
                    (_same(other["formula"], source.left) and _same(parsed_formula, source.right))
                    or (_same(other["formula"], source.right) and _same(parsed_formula, source.left))
                    for other in line_refs
                    if other["formula"] is not source
                )
                for source in biconditionals
            )
            if not licensed:
                add("rule.biconditional_elimination_mismatch", "↔E çift koşulun bir yönünü uygular.")
        elif rule == "DS" and require_counts(2, 0, "rule.ds_citation_count", "DS iki satıra atıf yapmalıdır."):
            licensed = False
            for source_ref in line_refs:
                source = source_ref["formula"]
                if source is CONTRADICTION or source.kind != "binary" or source.operator != "∨":
                    continue
                for other in line_refs:
                    if _is_negation_of(other["formula"], source.left) and parsed_formula is not None and _same(parsed_formula, source.right):
                        licensed = True
                    if _is_negation_of(other["formula"], source.right) and parsed_formula is not None and _same(parsed_formula, source.left):
                        licensed = True
            if not licensed:
                add("rule.ds_mismatch", "DS ayrışanlardan birinin yadsınmasından diğerini çıkarır.")
        elif rule == "MT" and require_counts(2, 0, "rule.mt_citation_count", "MT iki satıra atıf yapmalıdır."):
            licensed = False
            for source_ref in line_refs:
                source = source_ref["formula"]
                if source is CONTRADICTION or source.kind != "binary" or source.operator != "→":
                    continue
                for other in line_refs:
                    if _is_negation_of(other["formula"], source.right) and parsed_formula is not None and _is_negation_of(parsed_formula, source.left):
                        licensed = True
            if not licensed:
                add("rule.mt_mismatch", "MT, A→B ve ¬B'den ¬A çıkarır.")
        elif rule == "DNE" and require_counts(1, 0, "rule.dne_citation_count", "DNE bir satıra atıf yapmalıdır."):
            source = line_refs[0]["formula"]
            forward = source is not CONTRADICTION and source.kind == "negation" and source.body.kind == "negation" and parsed_formula is not None and _same(parsed_formula, source.body.body)
            backward = parsed_formula is not None and parsed_formula is not CONTRADICTION and parsed_formula.kind == "negation" and parsed_formula.body.kind == "negation" and _same(parsed_formula.body.body, source)
            if not (forward or backward):
                add("rule.dne_mismatch", "DNE yalnız A ile ¬¬A arasında geçiş yapar.")
        elif rule == "LEM":
            if citations:
                add("rule.lem_has_citations", "LEM atıf yapmaz.")
            if parsed_formula is None or parsed_formula is CONTRADICTION or parsed_formula.kind != "binary" or parsed_formula.operator != "∨" or not (_is_negation_of(parsed_formula.left, parsed_formula.right) or _is_negation_of(parsed_formula.right, parsed_formula.left)):
                add("rule.lem_mismatch", "LEM yalnız A∨¬A biçimini lisanslar.")
        elif rule == "DeM" and require_counts(1, 0, "rule.de_morgan_citation_count", "DeM bir satıra atıf yapmalıdır."):
            if parsed_formula is None or parsed_formula is CONTRADICTION or line_refs[0]["formula"] is CONTRADICTION or not _de_morgan_matches(line_refs[0]["formula"], parsed_formula):
                add("rule.de_morgan_mismatch", "DeM doğrudan De Morgan karşılığını verir.")
        elif rule == "∀E" and require_counts(1, 0, "rule.universal_elimination_citation_count", "∀E bir tümel satıra atıf yapmalıdır."):
            source = line_refs[0]["formula"]
            if source is CONTRADICTION or source.kind != "quantifier" or source.operator != "∀":
                add("rule.universal_elimination_source", "∀E kaynağı tümel niceleyicili olmalıdır.")
            elif parsed_formula is not None:
                names, vacuous = _substitution_names(source, parsed_formula, signature)
                if not names and not vacuous:
                    add("rule.universal_elimination_substitution", "Sonuç tümel gövdenin yakalamasız bir ad örneği değildir.")
        elif rule == "∃I" and require_counts(1, 0, "rule.existential_introduction_citation_count", "∃I bir örnek satıra atıf yapmalıdır."):
            if parsed_formula is None or parsed_formula.kind != "quantifier" or parsed_formula.operator != "∃":
                add("rule.existential_introduction_shape", "∃I sonucu varoluşsal niceleyicili olmalıdır.")
            else:
                names, vacuous = _substitution_names(parsed_formula, line_refs[0]["formula"], signature)
                if not names and not vacuous:
                    add("rule.existential_introduction_substitution", "Kaynak sonuç gövdesinin yakalamasız bir ad örneği değildir.")
        elif rule == "∀I" and require_counts(1, 0, "rule.universal_introduction_citation_count", "∀I bir örnek satıra atıf yapmalıdır."):
            if parsed_formula is None or parsed_formula.kind != "quantifier" or parsed_formula.operator != "∀":
                add("rule.universal_introduction_shape", "∀I sonucu tümel niceleyicili olmalıdır.")
            else:
                source_ref = line_refs[0]
                names, vacuous = _substitution_names(parsed_formula, source_ref["formula"], signature)
                if not names and not vacuous:
                    add("rule.universal_introduction_substitution", "Kaynak tümel gövdenin bir ad örneği değildir.")
                elif names:
                    blocked = set().union(
                        *(
                            _formula_names(dependency_formulas[token])
                            for token in source_ref["dependencies"]
                            if token in dependency_formulas
                        ),
                        set(),
                    )
                    if not any(name not in blocked for name in names):
                        add("rule.universal_introduction_name_not_fresh", "Genellenen ad, kaynak satırın açık varsayım veya öncül bağımlılığında geçiyor.")
        elif rule == "∃E" and require_counts(1, 1, "rule.existential_elimination_citation_count", "∃E bir varoluşsal satır ve bir alt kanıta atıf yapmalıdır."):
            existential = line_refs[0]
            subproof = subproof_refs[0]
            source = existential["formula"]
            if source is CONTRADICTION or source.kind != "quantifier" or source.operator != "∃":
                add("rule.existential_elimination_source", "∃E satır kaynağı varoluşsal olmalıdır.")
            elif parsed_formula is None or not _same(parsed_formula, subproof["end"]["formula"]):
                add("rule.existential_elimination_conclusion", "∃E sonucu alt kanıtın son formülüyle eşleşmelidir.")
            else:
                names, vacuous = _substitution_names(source, subproof["start"]["formula"], signature)
                if not names and not vacuous:
                    add("rule.existential_elimination_assumption", "Alt kanıt varsayımı varoluşsal gövdenin taze ad örneği değildir.")
                elif names:
                    outside_dependencies = set(existential["dependencies"]) | (
                        set(subproof["end"]["dependencies"])
                        - {("scope", subproof["scope"]["id"])}
                    )
                    outside_names = set().union(
                        *(
                            _formula_names(dependency_formulas[token])
                            for token in outside_dependencies
                            if token in dependency_formulas
                        ),
                        set(),
                    )
                    forbidden = _formula_names(source) | _formula_names(parsed_formula) | outside_names
                    if not any(name not in forbidden for name in names):
                        add("rule.existential_elimination_name_not_fresh", "Tanık adı varoluşsal öncülde, sonuçta veya dış bağımlılıkta geçiyor.")
        elif rule == "=I":
            if citations:
                add("rule.identity_introduction_has_citations", "=I atıf yapmaz.")
            if parsed_formula is None or parsed_formula is CONTRADICTION or parsed_formula.kind != "identity" or parsed_formula.terms[0].symbol != parsed_formula.terms[1].symbol:
                add("rule.identity_introduction_mismatch", "=I yalnız a=a biçimini lisanslar.")
        elif rule == "=E" and require_counts(2, 0, "rule.identity_elimination_citation_count", "=E bir kimlik ve bir formül satırına atıf yapmalıdır."):
            identities = [ref for ref in line_refs if ref["formula"] is not CONTRADICTION and ref["formula"].kind == "identity"]
            licensed = False
            for identity in identities:
                left_name = identity["formula"].terms[0].symbol
                right_name = identity["formula"].terms[1].symbol
                for source_ref in line_refs:
                    if source_ref is identity or parsed_formula is None or source_ref["formula"] is CONTRADICTION:
                        continue
                    licensed = licensed or _identity_substitution_matches(source_ref["formula"], parsed_formula, left_name, right_name)
                    licensed = licensed or _identity_substitution_matches(source_ref["formula"], parsed_formula, right_name, left_name)
            if not licensed:
                add("rule.identity_elimination_substitution", "=E yalnız eş adların seçilmiş oluşumlarını diğer adla değiştirebilir.")

        dependencies = set()
        if rule == "PR" and parsed_formula is not None:
            matching = [index for index, premise in parsed_premises if _same(parsed_formula, premise)]
            if matching:
                dependencies.add(("premise", matching[0]))
        elif rule == "AS" and opens is not None:
            token = ("scope", opens)
            dependencies.add(token)
            if parsed_formula is not None:
                dependency_formulas[token] = parsed_formula
        else:
            for ref in line_refs:
                dependencies.update(ref["dependencies"])
            for ref in subproof_refs:
                dependencies.update(ref["end"]["dependencies"])
                dependencies.discard(("scope", ref["scope"]["id"]))

        record = {
            "id": line_id,
            "formula": parsed_formula,
            "scope_path": scope_path,
            "depth": depth,
            "position": position,
            "rule": rule,
            "opens": opens,
            "closes": closes,
            "dependencies": frozenset(dependencies),
        }
        if line_id not in seen_lines:
            seen_lines[line_id] = record
        if active_scopes:
            scope_records[active_scopes[-1]]["last_direct_line_id"] = line_id
        last_line = record

    if require_complete:
        if active_scopes:
            issues.append(_issue("proof.scope_unclosed", "Tamamlanmış kanıtta açık alt kanıt kalamaz.", severity="incomplete"))
        if last_line is None:
            issues.append(_issue("proof.empty", "Tamamlanmış kanıt en az bir satır içermelidir.", severity="incomplete"))
        else:
            if last_line["scope_path"]:
                issues.append(_issue("proof.target_in_subproof", "Hedef kök kapsamda erişilebilir olmalıdır.", line_id=last_line["id"], severity="incomplete"))
            if parsed_target is not None and last_line["formula"] is not None and not _same(parsed_target, last_line["formula"]):
                issues.append(_issue("proof.target_not_reached", "Son kök satır hedefle eşleşmiyor.", line_id=last_line["id"], severity="incomplete"))

    return issues
