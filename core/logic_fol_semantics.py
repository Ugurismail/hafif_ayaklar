"""Finite interpretation semantics for isolated FOL curriculum candidates.

The learner-facing course does not import this module. It evaluates the strict
syntax trees from :mod:`core.logic_fol` in explicitly supplied finite models.
Finite sample search can establish a countermodel, but deliberately never
claims general FOL validity when no countermodel is found.
"""

from dataclasses import dataclass
from typing import Hashable, Mapping

from .logic_fol import FOLFormula, FOLSignature, parse_fol


COUNTERMODEL_FOUND = "countermodel_found"
NO_COUNTERMODEL_IN_SAMPLE = "no_countermodel_in_sample"


class FOLSemanticError(ValueError):
    """A stable semantic/model validation error."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True)
class FOLInterpretation:
    """One finite interpretation for a fixed FOL signature."""

    signature: FOLSignature
    domain: tuple[Hashable, ...]
    names: Mapping[str, Hashable]
    predicates: Mapping[str, frozenset[tuple[Hashable, ...]]]
    label: str = ""

    def __post_init__(self):
        if not isinstance(self.signature, FOLSignature):
            raise FOLSemanticError(
                "model.signature_invalid",
                "Yorum geçerli bir FOL imzası taşımalıdır.",
            )

        try:
            domain = tuple(self.domain)
            domain_set = set(domain)
        except (TypeError, ValueError) as exc:
            raise FOLSemanticError(
                "model.domain_unhashable",
                "Alan üyeleri birbirinden ayırt edilebilir ve hashlenebilir olmalıdır.",
            ) from exc
        if not domain:
            raise FOLSemanticError(
                "model.domain_empty",
                "Klasik FOL yorumunun alanı boş olamaz.",
            )
        if len(domain_set) != len(domain):
            raise FOLSemanticError(
                "model.domain_duplicate",
                "Alan aynı üyeyi birden fazla kez içeremez.",
            )

        names = dict(self.names)
        expected_names = set(self.signature.names)
        supplied_names = set(names)
        if supplied_names != expected_names:
            missing = sorted(expected_names - supplied_names)
            extra = sorted(supplied_names - expected_names)
            detail = []
            if missing:
                detail.append("eksik: " + ", ".join(missing))
            if extra:
                detail.append("fazla: " + ", ".join(extra))
            raise FOLSemanticError(
                "model.name_key_mismatch",
                "Ad gönderimleri imzayla eşleşmiyor (" + "; ".join(detail) + ").",
            )
        for symbol, referent in names.items():
            if referent not in domain_set:
                raise FOLSemanticError(
                    "model.name_outside_domain",
                    f"{symbol} adı alan dışındaki {referent!r} nesnesine gönderilemez.",
                )

        raw_predicates = dict(self.predicates)
        expected_predicates = set(self.signature.predicates)
        supplied_predicates = set(raw_predicates)
        if supplied_predicates != expected_predicates:
            missing = sorted(expected_predicates - supplied_predicates)
            extra = sorted(supplied_predicates - expected_predicates)
            detail = []
            if missing:
                detail.append("eksik: " + ", ".join(missing))
            if extra:
                detail.append("fazla: " + ", ".join(extra))
            raise FOLSemanticError(
                "model.predicate_key_mismatch",
                "Yüklem uzantıları imzayla eşleşmiyor (" + "; ".join(detail) + ").",
            )

        predicates = {}
        for symbol, extension in raw_predicates.items():
            arity = self.signature.predicates[symbol]
            normalized = set()
            for raw_tuple in extension:
                if arity == 1 and not isinstance(raw_tuple, (tuple, list)):
                    item = (raw_tuple,)
                else:
                    try:
                        item = tuple(raw_tuple)
                    except TypeError as exc:
                        raise FOLSemanticError(
                            "model.extension_tuple_invalid",
                            f"{symbol}/{arity} uzantısındaki her üye {arity}'li olmalıdır.",
                        ) from exc
                if len(item) != arity:
                    raise FOLSemanticError(
                        "model.extension_arity",
                        f"{symbol}/{arity} uzantısında {len(item)} öğeli tuple bulundu.",
                    )
                outside = [value for value in item if value not in domain_set]
                if outside:
                    raise FOLSemanticError(
                        "model.extension_outside_domain",
                        f"{symbol} uzantısı alan dışı üye içeriyor: {outside[0]!r}.",
                    )
                normalized.add(item)
            predicates[symbol] = frozenset(normalized)

        object.__setattr__(self, "domain", domain)
        object.__setattr__(self, "names", names)
        object.__setattr__(self, "predicates", predicates)


def interpretation_from_data(data: Mapping, signature: FOLSignature) -> FOLInterpretation:
    """Build and validate one interpretation from serialisable lesson data."""

    if not isinstance(data, Mapping):
        raise FOLSemanticError(
            "model.data_invalid",
            "Yorum verisi bir sözlük olmalıdır.",
        )
    return FOLInterpretation(
        signature=signature,
        domain=tuple(data.get("domain", ())),
        names=data.get("names", {}),
        predicates=data.get("predicates", {}),
        label=data.get("label", ""),
    )


def interpretation_to_data(model: FOLInterpretation) -> dict:
    """Return a deterministic, serialisable representation of a model."""

    predicates = {}
    for symbol in sorted(model.predicates):
        arity = model.signature.predicates[symbol]
        extension = sorted(model.predicates[symbol], key=repr)
        predicates[symbol] = [
            item[0] if arity == 1 else list(item)
            for item in extension
        ]
    return {
        "label": model.label,
        "domain": list(model.domain),
        "names": {symbol: model.names[symbol] for symbol in sorted(model.names)},
        "predicates": predicates,
    }


def _parsed_formula(formula, signature: FOLSignature) -> FOLFormula:
    if isinstance(formula, FOLFormula):
        return formula
    if isinstance(formula, str):
        return parse_fol(formula, signature)
    raise TypeError("FOL formülü metin veya FOLFormula olmalıdır.")


def _validated_assignment(
    formula: FOLFormula,
    model: FOLInterpretation,
    assignment: Mapping[str, Hashable] | None,
) -> dict[str, Hashable]:
    values = dict(assignment or {})
    unknown = sorted(set(values) - set(model.signature.variables))
    if unknown:
        raise FOLSemanticError(
            "assignment.variable_unknown",
            f"Atamada imza dışı değişken var: {unknown[0]}.",
        )
    for variable, value in values.items():
        if value not in model.domain:
            raise FOLSemanticError(
                "assignment.outside_domain",
                f"{variable} değişkeni alan dışındaki {value!r} değerini alamaz.",
            )
    missing = sorted(formula.free_variables - set(values))
    if missing:
        raise FOLSemanticError(
            "assignment.free_variable_missing",
            "Açık formül için serbest değişken ataması eksik: "
            + ", ".join(missing)
            + ".",
        )
    return values


def _term_value(term, model: FOLInterpretation, assignment: Mapping):
    if term.kind == "name":
        return model.names[term.symbol]
    try:
        return assignment[term.symbol]
    except KeyError as exc:
        raise FOLSemanticError(
            "assignment.variable_missing",
            f"{term.symbol} değişkeninin bu değerlendirmede değeri yok.",
        ) from exc


def _evaluate_node(node: FOLFormula, model: FOLInterpretation, assignment: dict) -> bool:
    if node.kind == "predicate":
        values = tuple(_term_value(term, model, assignment) for term in node.terms)
        return values in model.predicates[node.predicate]
    if node.kind == "identity":
        return _term_value(node.terms[0], model, assignment) == _term_value(
            node.terms[1], model, assignment
        )
    if node.kind == "negation":
        return not _evaluate_node(node.body, model, assignment)
    if node.kind == "binary":
        left = _evaluate_node(node.left, model, assignment)
        right = _evaluate_node(node.right, model, assignment)
        if node.operator == "∧":
            return left and right
        if node.operator == "∨":
            return left or right
        if node.operator == "→":
            return (not left) or right
        if node.operator == "↔":
            return left == right
        raise FOLSemanticError(
            "formula.operator_unknown",
            f"Bilinmeyen ikili bağlaç: {node.operator!r}.",
        )
    if node.kind == "quantifier":
        branch_values = []
        had_previous = node.variable in assignment
        previous = assignment.get(node.variable)
        try:
            for value in model.domain:
                assignment[node.variable] = value
                branch_values.append(_evaluate_node(node.body, model, assignment))
        finally:
            if had_previous:
                assignment[node.variable] = previous
            else:
                assignment.pop(node.variable, None)
        return all(branch_values) if node.operator == "∀" else any(branch_values)
    raise FOLSemanticError(
        "formula.kind_unknown",
        f"Bilinmeyen FOL düğüm türü: {node.kind!r}.",
    )


def evaluate_fol(
    formula: str | FOLFormula,
    model: FOLInterpretation,
    assignment: Mapping[str, Hashable] | None = None,
) -> bool:
    """Evaluate one FOL formula in one interpretation and assignment."""

    parsed = _parsed_formula(formula, model.signature)
    values = _validated_assignment(parsed, model, assignment)
    return _evaluate_node(parsed, model, values)


def evaluation_trace(
    formula: str | FOLFormula,
    model: FOLInterpretation,
    assignment: Mapping[str, Hashable] | None = None,
) -> dict:
    """Return an inside-out evaluation trace with quantifier branches."""

    parsed = _parsed_formula(formula, model.signature)
    values = _validated_assignment(parsed, model, assignment)
    steps = []

    def visit(node: FOLFormula, local_assignment: dict) -> bool:
        if node.kind == "predicate":
            denotations = tuple(
                _term_value(term, model, local_assignment) for term in node.terms
            )
            value = denotations in model.predicates[node.predicate]
            detail = {
                "denotations": list(denotations),
                "extension_member": value,
            }
        elif node.kind == "identity":
            denotations = tuple(
                _term_value(term, model, local_assignment) for term in node.terms
            )
            value = denotations[0] == denotations[1]
            detail = {"denotations": list(denotations)}
        elif node.kind == "negation":
            child = visit(node.body, local_assignment)
            value = not child
            detail = {"body_value": child}
        elif node.kind == "binary":
            left = visit(node.left, local_assignment)
            right = visit(node.right, local_assignment)
            if node.operator == "∧":
                value = left and right
            elif node.operator == "∨":
                value = left or right
            elif node.operator == "→":
                value = (not left) or right
            elif node.operator == "↔":
                value = left == right
            else:
                raise FOLSemanticError(
                    "formula.operator_unknown",
                    f"Bilinmeyen ikili bağlaç: {node.operator!r}.",
                )
            detail = {"left_value": left, "right_value": right}
        elif node.kind == "quantifier":
            branches = []
            had_previous = node.variable in local_assignment
            previous = local_assignment.get(node.variable)
            try:
                for domain_value in model.domain:
                    local_assignment[node.variable] = domain_value
                    branches.append(
                        {
                            "assigned_value": domain_value,
                            "body_value": _evaluate_node(
                                node.body,
                                model,
                                local_assignment,
                            ),
                        }
                    )
            finally:
                if had_previous:
                    local_assignment[node.variable] = previous
                else:
                    local_assignment.pop(node.variable, None)
            branch_values = [branch["body_value"] for branch in branches]
            value = all(branch_values) if node.operator == "∀" else any(branch_values)
            decisive = next(
                (
                    branch["assigned_value"]
                    for branch in branches
                    if branch["body_value"] == (node.operator == "∃")
                ),
                None,
            )
            detail = {
                "variable": node.variable,
                "branches": branches,
                (
                    "witness" if node.operator == "∃" else "counterexample"
                ): decisive,
            }
        else:
            raise FOLSemanticError(
                "formula.kind_unknown",
                f"Bilinmeyen FOL düğüm türü: {node.kind!r}.",
            )

        steps.append(
            {
                "formula": node.render(),
                "kind": node.kind,
                "value": value,
                "assignment": dict(local_assignment),
                "detail": detail,
            }
        )
        return value

    value = visit(parsed, values)
    return {
        "formula": parsed.render(),
        "value": value,
        "steps": steps,
    }


def search_countermodel(
    premises,
    conclusion,
    models,
    signature: FOLSignature,
) -> dict:
    """Search supplied finite models without inferring validity from failure."""

    parsed_premises = [_parsed_formula(item, signature) for item in premises]
    parsed_conclusion = _parsed_formula(conclusion, signature)
    for formula in [*parsed_premises, parsed_conclusion]:
        if not formula.is_sentence:
            raise FOLSemanticError(
                "consequence.open_formula",
                "Semantik sonuç denetimi yalnız kapalı FOL cümleleri kullanır.",
            )

    checked = 0
    for model in models:
        if not isinstance(model, FOLInterpretation):
            model = interpretation_from_data(model, signature)
        if model.signature is not signature:
            if (
                model.signature.names != signature.names
                or model.signature.variables != signature.variables
                or model.signature.predicates != signature.predicates
            ):
                raise FOLSemanticError(
                    "model.signature_mismatch",
                    "Karşı model bankasındaki yorum farklı bir FOL imzası kullanıyor.",
                )
        checked += 1
        premise_values = [evaluate_fol(item, model) for item in parsed_premises]
        conclusion_value = evaluate_fol(parsed_conclusion, model)
        if all(premise_values) and not conclusion_value:
            return {
                "status": COUNTERMODEL_FOUND,
                "countermodel": interpretation_to_data(model),
                "premise_values": premise_values,
                "conclusion_value": conclusion_value,
                "checked_model_count": checked,
                "entails": False,
            }

    return {
        "status": NO_COUNTERMODEL_IN_SAMPLE,
        "countermodel": None,
        "checked_model_count": checked,
        "entails": None,
        "warning": (
            "Bu sonlu örneklemde karşı model bulunmadı; bu sonuç genel FOL "
            "geçerliliğini kanıtlamaz."
        ),
    }


def analyze_binary_relation(model: FOLInterpretation, predicate: str) -> dict:
    """Check standard properties of one binary relation with counterexamples."""

    if predicate not in model.signature.predicates:
        raise FOLSemanticError(
            "relation.predicate_unknown",
            f"{predicate} yüklemi model imzasında bulunmuyor.",
        )
    if model.signature.predicates[predicate] != 2:
        raise FOLSemanticError(
            "relation.arity",
            f"{predicate} ikili bir yüklem değildir.",
        )

    domain = tuple(model.domain)
    extension = model.predicates[predicate]

    reflexive_failure = next((value for value in domain if (value, value) not in extension), None)
    irreflexive_failure = next((value for value in domain if (value, value) in extension), None)
    symmetric_failure = next(
        ((left, right) for left, right in extension if (right, left) not in extension),
        None,
    )
    asymmetric_failure = next(
        ((left, right) for left, right in extension if (right, left) in extension),
        None,
    )
    antisymmetric_failure = next(
        (
            (left, right)
            for left, right in extension
            if left != right and (right, left) in extension
        ),
        None,
    )
    transitive_failure = next(
        (
            (left, middle, right)
            for left, middle in extension
            for candidate_middle, right in extension
            if middle == candidate_middle and (left, right) not in extension
        ),
        None,
    )
    serial_failure = next(
        (
            left
            for left in domain
            if not any((left, right) in extension for right in domain)
        ),
        None,
    )

    def result(counterexample):
        return {
            "holds": counterexample is None,
            "counterexample": counterexample,
        }

    return {
        "predicate": predicate,
        "extension": [list(item) for item in sorted(extension, key=repr)],
        "properties": {
            "reflexive": result(reflexive_failure),
            "irreflexive": result(irreflexive_failure),
            "symmetric": result(symmetric_failure),
            "asymmetric": result(asymmetric_failure),
            "antisymmetric": result(antisymmetric_failure),
            "transitive": result(transitive_failure),
            "serial": result(serial_failure),
        },
    }
