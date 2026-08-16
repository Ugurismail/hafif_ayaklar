"""Strict syntax support for the isolated first-order logic curriculum.

The learner-facing course does not import this module.  It gives Stage E a
small, deterministic parser so candidate examples can be checked as syntax
trees instead of being trusted as strings.  Semantics and proof rules are
deliberately outside this module's responsibility.
"""

from collections import Counter
from dataclasses import dataclass
from typing import Mapping


BINARY_CONNECTIVES = frozenset({"∧", "∨", "→", "↔"})
LOGICAL_SYMBOLS = frozenset({"¬", "∀", "∃", "=", "≠", *BINARY_CONNECTIVES})
PUNCTUATION = frozenset({"(", ")", ","})
SUBSCRIPT_DIGITS = frozenset("₀₁₂₃₄₅₆₇₈₉")
DEFAULT_VARIABLES = frozenset("stuvwxyz")


class FOLParseError(ValueError):
    """A stable, position-aware FOL syntax error."""

    def __init__(self, code: str, message: str, position: int | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.position = position


def _base_letter(symbol: str) -> str:
    return symbol[0] if symbol else ""


def _is_indexed_letter(symbol: str, *, uppercase: bool) -> bool:
    if not symbol:
        return False
    first = symbol[0]
    if uppercase and not ("A" <= first <= "Z"):
        return False
    if not uppercase and not ("a" <= first <= "z"):
        return False
    suffix = symbol[1:]
    if not suffix:
        return True
    if suffix.startswith("_"):
        return len(suffix) > 1 and suffix[1:].isdigit()
    return all(char in SUBSCRIPT_DIGITS for char in suffix)


class FOLSignature:
    """Vocabulary contract for one FOL exercise.

    Names and variables deliberately occupy disjoint letter ranges in the
    candidate notation. Predicate arity belongs to the signature, not to an
    individual formula guessed after parsing.
    """

    def __init__(
        self,
        *,
        names=(),
        predicates: Mapping[str, int] | None = None,
        variables=DEFAULT_VARIABLES,
    ):
        self.names = frozenset(names)
        self.variables = frozenset(variables)
        self.predicates = dict(predicates or {})
        self._validate()

    def _validate(self) -> None:
        overlap = self.names & self.variables
        if overlap:
            raise ValueError(
                "Ad ve değişken kümeleri ayrık olmalıdır: "
                + ", ".join(sorted(overlap))
            )

        for name in self.names:
            if not _is_indexed_letter(name, uppercase=False):
                raise ValueError(f"Geçersiz ad sembolü: {name!r}.")
            if not ("a" <= _base_letter(name) <= "r"):
                raise ValueError(
                    f"Aday gösterimde adlar a-r aralığında olmalıdır: {name!r}."
                )

        for variable in self.variables:
            if not _is_indexed_letter(variable, uppercase=False):
                raise ValueError(f"Geçersiz değişken sembolü: {variable!r}.")
            if not ("s" <= _base_letter(variable) <= "z"):
                raise ValueError(
                    "Aday gösterimde değişkenler s-z aralığında olmalıdır: "
                    f"{variable!r}."
                )

        for predicate, arity in self.predicates.items():
            if not _is_indexed_letter(predicate, uppercase=True):
                raise ValueError(f"Geçersiz yüklem sembolü: {predicate!r}.")
            if not isinstance(arity, int) or isinstance(arity, bool) or arity < 1:
                raise ValueError(
                    f"{predicate} yükleminin aritesi pozitif tam sayı olmalıdır."
                )

    def predicate_arity(self, symbol: str) -> int:
        try:
            return self.predicates[symbol]
        except KeyError as exc:
            raise FOLParseError(
                "predicate.unknown",
                f"{symbol} yüklemi sembol anahtarında tanımlı değil.",
            ) from exc


def signature_from_data(data: Mapping) -> FOLSignature:
    """Create a parser signature from a serialisable lesson key."""

    raw_names = data.get("names", {})
    names = raw_names.keys() if isinstance(raw_names, Mapping) else raw_names

    raw_predicates = data.get("predicates", {})
    predicates = {}
    for symbol, details in raw_predicates.items():
        predicates[symbol] = (
            details.get("arity") if isinstance(details, Mapping) else details
        )

    return FOLSignature(
        names=names,
        predicates=predicates,
        variables=data.get("variables", DEFAULT_VARIABLES),
    )


@dataclass(frozen=True)
class _Token:
    kind: str
    value: str
    start: int
    end: int


@dataclass(frozen=True)
class FOLTerm:
    symbol: str
    kind: str
    start: int
    end: int

    def render(self) -> str:
        return self.symbol


@dataclass(frozen=True)
class FOLFormula:
    """One parsed FOL formula node with source positions."""

    kind: str
    start: int
    end: int
    operator: str | None = None
    predicate: str | None = None
    terms: tuple[FOLTerm, ...] = ()
    left: "FOLFormula | None" = None
    right: "FOLFormula | None" = None
    body: "FOLFormula | None" = None
    variable: str | None = None

    def render(self) -> str:
        if self.kind == "predicate":
            terms = ",".join(term.render() for term in self.terms)
            return f"{self.predicate}({terms})"
        if self.kind == "identity":
            return f"{self.terms[0].render()}={self.terms[1].render()}"
        if self.kind == "negation":
            if self.body.kind == "identity":
                return (
                    f"{self.body.terms[0].render()}"
                    f"≠{self.body.terms[1].render()}"
                )
            return f"¬{self.body.render()}"
        if self.kind == "binary":
            return (
                f"({self.left.render()} {self.operator} "
                f"{self.right.render()})"
            )
        if self.kind == "quantifier":
            return f"{self.operator}{self.variable}{self.body.render()}"
        raise ValueError(f"Bilinmeyen FOL düğüm türü: {self.kind!r}.")

    @property
    def variable_occurrences(self) -> tuple[dict, ...]:
        return tuple(_analyse_variables(self)[0])

    @property
    def free_variables(self) -> frozenset[str]:
        occurrences, _warnings = _analyse_variables(self)
        return frozenset(
            occurrence["symbol"]
            for occurrence in occurrences
            if not occurrence["bound"]
        )

    @property
    def is_sentence(self) -> bool:
        return not self.free_variables

    @property
    def warnings(self) -> tuple[dict, ...]:
        return tuple(_analyse_variables(self)[1])


def _scan_identifier(source: str, index: int) -> tuple[str, int]:
    end = index + 1
    while end < len(source) and source[end] in SUBSCRIPT_DIGITS:
        end += 1
    if end < len(source) and source[end] == "_":
        digit_start = end + 1
        end = digit_start
        while end < len(source) and source[end].isdigit():
            end += 1
        if end == digit_start:
            raise FOLParseError(
                "symbol.invalid_index",
                "Alt indis alt çizgiden sonra en az bir rakam içermelidir.",
                index,
            )
    return source[index:end], end


def _tokenize(source: str) -> list[_Token]:
    if not isinstance(source, str) or not source.strip():
        raise FOLParseError("expression.empty", "FOL ifadesi boş olamaz.", 0)

    tokens = []
    index = 0
    while index < len(source):
        char = source[index]
        if char.isspace():
            index += 1
            continue
        if char in LOGICAL_SYMBOLS:
            tokens.append(_Token("symbol", char, index, index + 1))
            index += 1
            continue
        if char in PUNCTUATION:
            tokens.append(_Token("punctuation", char, index, index + 1))
            index += 1
            continue
        if ("A" <= char <= "Z") or ("a" <= char <= "z"):
            identifier, end = _scan_identifier(source, index)
            kind = "predicate" if "A" <= char <= "Z" else "term"
            tokens.append(_Token(kind, identifier, index, end))
            index = end
            continue
        raise FOLParseError(
            "symbol.unsupported",
            f"Desteklenmeyen FOL sembolü: {char!r}.",
            index,
        )
    return tokens


class _Parser:
    def __init__(self, tokens: list[_Token], signature: FOLSignature):
        self.tokens = tokens
        self.signature = signature
        self.position = 0

    def parse(self) -> FOLFormula:
        formula = self._parse_expression()
        trailing = self._peek()
        if trailing is not None:
            raise FOLParseError(
                "formula.trailing_symbol",
                f"Formülden sonra beklenmeyen sembol: {trailing.value!r}.",
                trailing.start,
            )
        return formula

    def _parse_expression(self) -> FOLFormula:
        left = self._parse_unit()
        token = self._peek()
        if token is None or token.value not in BINARY_CONNECTIVES:
            return left

        operator = self._take()
        if self._peek() is None:
            raise FOLParseError(
                "connective.right_missing",
                f"{operator.value} bağlacının sağında bir FOL formülü bulunmalıdır.",
                operator.start,
            )
        right = self._parse_unit()
        if self._peek() is not None and self._peek().value in BINARY_CONNECTIVES:
            raise FOLParseError(
                "connective.multiple_unparenthesized",
                "Bir kapsamda birden fazla ikili bağlaç parantezsiz bırakılamaz.",
                self._peek().start,
            )
        return FOLFormula(
            kind="binary",
            start=left.start,
            end=right.end,
            operator=operator.value,
            left=left,
            right=right,
        )

    def _parse_unit(self) -> FOLFormula:
        token = self._peek()
        if token is None:
            raise FOLParseError(
                "formula.incomplete",
                "FOL formülü tamamlanmadan sona erdi.",
            )

        if token.value == "¬":
            operator = self._take()
            body = self._parse_unit()
            return FOLFormula(
                kind="negation",
                start=operator.start,
                end=body.end,
                operator="¬",
                body=body,
            )

        if token.value in {"∀", "∃"}:
            operator = self._take()
            variable_token = self._peek()
            if (
                variable_token is None
                or variable_token.kind != "term"
                or variable_token.value not in self.signature.variables
            ):
                position = (
                    variable_token.start
                    if variable_token is not None
                    else operator.end
                )
                raise FOLParseError(
                    "quantifier.variable_expected",
                    f"{operator.value} işaretinden sonra tanımlı bir değişken gelmelidir.",
                    position,
                )
            variable = self._take()
            body = self._parse_unit()
            return FOLFormula(
                kind="quantifier",
                start=operator.start,
                end=body.end,
                operator=operator.value,
                variable=variable.value,
                body=body,
            )

        if token.value == "(":
            opening = self._take()
            formula = self._parse_expression()
            closing = self._peek()
            if closing is None or closing.value != ")":
                position = closing.start if closing is not None else formula.end
                raise FOLParseError(
                    "parenthesis.unclosed",
                    "Açılan parantezin kapanışı bulunamadı.",
                    position,
                )
            self._take()
            return FOLFormula(
                kind=formula.kind,
                start=opening.start,
                end=closing.end,
                operator=formula.operator,
                predicate=formula.predicate,
                terms=formula.terms,
                left=formula.left,
                right=formula.right,
                body=formula.body,
                variable=formula.variable,
            )

        if token.value == ")":
            raise FOLParseError(
                "parenthesis.unexpected_close",
                "Karşılıksız kapanış parantezi bulundu.",
                token.start,
            )
        if token.value in BINARY_CONNECTIVES:
            raise FOLParseError(
                "connective.left_missing",
                f"{token.value} bağlacının solunda bir FOL formülü bulunmalıdır.",
                token.start,
            )
        if token.kind == "predicate":
            return self._parse_predicate_formula()
        if token.kind == "term":
            return self._parse_identity_formula()

        raise FOLParseError(
            "formula.expected",
            f"Bu konumda FOL formülü bekleniyor; {token.value!r} bulundu.",
            token.start,
        )

    def _parse_predicate_formula(self) -> FOLFormula:
        predicate = self._take()
        if predicate.value not in self.signature.predicates:
            raise FOLParseError(
                "predicate.unknown",
                f"{predicate.value} yüklemi sembol anahtarında tanımlı değil.",
                predicate.start,
            )
        opening = self._peek()
        if opening is None or opening.value != "(":
            raise FOLParseError(
                "predicate.arguments_missing",
                f"{predicate.value} yükleminin terimleri parantez içinde yazılmalıdır.",
                predicate.end,
            )
        self._take()

        terms = []
        if self._peek() is not None and self._peek().value != ")":
            terms.append(self._parse_term())
            while self._peek() is not None and self._peek().value == ",":
                comma = self._take()
                if self._peek() is None or self._peek().value == ")":
                    raise FOLParseError(
                        "predicate.term_missing",
                        "Virgülden sonra bir terim bulunmalıdır.",
                        comma.end,
                    )
                terms.append(self._parse_term())

        closing = self._peek()
        if closing is None or closing.value != ")":
            position = closing.start if closing is not None else predicate.end
            raise FOLParseError(
                "predicate.arguments_unclosed",
                f"{predicate.value} yükleminin argüman listesi kapanmadı.",
                position,
            )
        self._take()

        expected_arity = self.signature.predicates[predicate.value]
        if len(terms) != expected_arity:
            raise FOLParseError(
                "predicate.arity_mismatch",
                f"{predicate.value} {expected_arity} terim ister; "
                f"{len(terms)} terim verildi.",
                predicate.start,
            )
        return FOLFormula(
            kind="predicate",
            start=predicate.start,
            end=closing.end,
            predicate=predicate.value,
            terms=tuple(terms),
        )

    def _parse_identity_formula(self) -> FOLFormula:
        left = self._parse_term()
        equals = self._peek()
        if equals is None or equals.value not in {"=", "≠"}:
            raise FOLParseError(
                "formula.term_without_identity",
                f"{left.symbol} bir terimdir; tek başına FOL formülü değildir.",
                left.start,
            )
        self._take()
        if self._peek() is None:
            raise FOLParseError(
                "identity.right_term_missing",
                "Kimlik işaretinin sağında bir terim bulunmalıdır.",
                equals.end,
            )
        right = self._parse_term()
        identity = FOLFormula(
            kind="identity",
            start=left.start,
            end=right.end,
            operator="=",
            terms=(left, right),
        )
        if equals.value == "=":
            return identity
        return FOLFormula(
            kind="negation",
            start=left.start,
            end=right.end,
            operator="¬",
            body=identity,
        )

    def _parse_term(self) -> FOLTerm:
        token = self._peek()
        if token is None or token.kind != "term":
            position = token.start if token is not None else None
            found = token.value if token is not None else "ifadenin sonu"
            raise FOLParseError(
                "term.expected",
                f"Bu konumda ad veya değişken bekleniyor; {found!r} bulundu.",
                position,
            )
        self._take()
        if token.value in self.signature.names:
            kind = "name"
        elif token.value in self.signature.variables:
            kind = "variable"
        else:
            raise FOLParseError(
                "term.unknown",
                f"{token.value} sembolü anahtarda ad veya değişken değil.",
                token.start,
            )
        return FOLTerm(
            symbol=token.value,
            kind=kind,
            start=token.start,
            end=token.end,
        )

    def _peek(self) -> _Token | None:
        if self.position >= len(self.tokens):
            return None
        return self.tokens[self.position]

    def _take(self) -> _Token:
        token = self._peek()
        if token is None:
            raise FOLParseError(
                "formula.incomplete",
                "FOL formülü tamamlanmadan sona erdi.",
            )
        self.position += 1
        return token


def parse_fol(source: str, signature: FOLSignature) -> FOLFormula:
    """Parse one strict FOL formula under the supplied vocabulary."""

    return _Parser(_tokenize(source), signature).parse()


def fol_structure_key(formula: FOLFormula) -> tuple:
    """Return an alpha-stable structural key for a parsed formula.

    Bound variables are represented by the binder that introduced them, not
    by their printed letter. Free variables and names retain their symbols.
    This makes ``∀xF(x)`` and ``∀yF(y)`` structurally identical without
    treating formulas with different free variables as interchangeable.
    """

    binder_counter = 0
    binders: dict[str, list[int]] = {}

    def term_key(term: FOLTerm) -> tuple:
        if term.kind == "name":
            return ("name", term.symbol)
        stack = binders.get(term.symbol, [])
        if stack:
            return ("bound", stack[-1])
        return ("free", term.symbol)

    def visit(node: FOLFormula) -> tuple:
        nonlocal binder_counter

        if node.kind == "predicate":
            return (
                "predicate",
                node.predicate,
                tuple(term_key(term) for term in node.terms),
            )
        if node.kind == "identity":
            terms = sorted(
                (term_key(node.terms[0]), term_key(node.terms[1])),
                key=repr,
            )
            return (
                "identity",
                terms[0],
                terms[1],
            )
        if node.kind == "negation":
            return ("negation", visit(node.body))
        if node.kind == "binary":
            return (
                "binary",
                node.operator,
                visit(node.left),
                visit(node.right),
            )
        if node.kind == "quantifier":
            binder_id = binder_counter
            binder_counter += 1
            stack = binders.setdefault(node.variable, [])
            stack.append(binder_id)
            body_key = visit(node.body)
            stack.pop()
            if not stack:
                binders.pop(node.variable, None)
            return ("quantifier", node.operator, body_key)
        raise ValueError(f"Bilinmeyen FOL düğüm türü: {node.kind!r}.")

    return visit(formula)


def formulas_alpha_equivalent(left: FOLFormula, right: FOLFormula) -> bool:
    """Return whether two formulas differ only in bound-variable names."""

    return fol_structure_key(left) == fol_structure_key(right)


def _term_binding_key(
    term: FOLTerm,
    binders: dict[str, list[object]],
) -> tuple:
    if term.kind == "name":
        return ("name", term.symbol)
    stack = binders.get(term.symbol, [])
    return ("bound", stack[-1]) if stack else ("free", term.symbol)


def _nodes_match_with_binders(
    candidate: FOLFormula,
    expected: FOLFormula,
    candidate_binders: dict[str, list[object]],
    expected_binders: dict[str, list[object]],
) -> bool:
    """Compare two nodes while preserving binders introduced above them."""

    if candidate.kind != expected.kind:
        return False
    if candidate.kind == "predicate":
        return (
            candidate.predicate == expected.predicate
            and len(candidate.terms) == len(expected.terms)
            and all(
                _term_binding_key(left, candidate_binders)
                == _term_binding_key(right, expected_binders)
                for left, right in zip(candidate.terms, expected.terms)
            )
        )
    if candidate.kind == "identity":
        candidate_terms = tuple(
            _term_binding_key(term, candidate_binders)
            for term in candidate.terms
        )
        expected_terms = tuple(
            _term_binding_key(term, expected_binders)
            for term in expected.terms
        )
        return (
            candidate_terms == expected_terms
            or candidate_terms == tuple(reversed(expected_terms))
        )
    if candidate.kind == "negation":
        return _nodes_match_with_binders(
            candidate.body,
            expected.body,
            candidate_binders,
            expected_binders,
        )
    if candidate.kind == "binary":
        return (
            candidate.operator == expected.operator
            and _nodes_match_with_binders(
                candidate.left,
                expected.left,
                candidate_binders,
                expected_binders,
            )
            and _nodes_match_with_binders(
                candidate.right,
                expected.right,
                candidate_binders,
                expected_binders,
            )
        )
    if candidate.kind == "quantifier":
        if candidate.operator != expected.operator:
            return False
        marker = object()
        candidate_stack = candidate_binders.setdefault(candidate.variable, [])
        expected_stack = expected_binders.setdefault(expected.variable, [])
        candidate_stack.append(marker)
        expected_stack.append(marker)
        matches = _nodes_match_with_binders(
            candidate.body,
            expected.body,
            candidate_binders,
            expected_binders,
        )
        candidate_stack.pop()
        expected_stack.pop()
        if not candidate_stack:
            candidate_binders.pop(candidate.variable, None)
        if not expected_stack:
            expected_binders.pop(expected.variable, None)
        return matches
    raise ValueError(f"Bilinmeyen FOL düğüm türü: {candidate.kind!r}.")


def _strip_leading_quantifiers(
    formula: FOLFormula,
) -> tuple[list[tuple[str, str]], FOLFormula]:
    prefix = []
    node = formula
    while node.kind == "quantifier":
        prefix.append((node.operator, node.variable))
        node = node.body
    return prefix, node


def _matrix_variable_mapping(
    candidate: FOLFormula,
    expected: FOLFormula,
) -> dict[str, str] | None:
    """Map candidate variables to expected variables by matrix role."""

    mapping = {}
    reverse = {}

    def term_matches(left: FOLTerm, right: FOLTerm) -> bool:
        if left.kind != right.kind:
            return False
        if left.kind == "name":
            return left.symbol == right.symbol
        mapped = mapping.get(left.symbol)
        reversed_symbol = reverse.get(right.symbol)
        if mapped is not None:
            return mapped == right.symbol
        if reversed_symbol is not None:
            return reversed_symbol == left.symbol
        mapping[left.symbol] = right.symbol
        reverse[right.symbol] = left.symbol
        return True

    def visit(left: FOLFormula, right: FOLFormula) -> bool:
        if left.kind != right.kind:
            return False
        if left.kind == "predicate":
            return (
                left.predicate == right.predicate
                and len(left.terms) == len(right.terms)
                and all(
                    term_matches(left_term, right_term)
                    for left_term, right_term in zip(left.terms, right.terms)
                )
            )
        if left.kind == "identity":
            return all(
                term_matches(left_term, right_term)
                for left_term, right_term in zip(left.terms, right.terms)
            )
        if left.kind == "negation":
            return visit(left.body, right.body)
        if left.kind == "binary":
            return (
                left.operator == right.operator
                and visit(left.left, right.left)
                and visit(left.right, right.right)
            )
        # This helper only compares matrices after the leading prefix.
        return False

    return mapping if visit(candidate, expected) else None


def _has_quantifier_order_mismatch(
    candidate: FOLFormula,
    expected: FOLFormula,
) -> bool:
    candidate_prefix, candidate_matrix = _strip_leading_quantifiers(candidate)
    expected_prefix, expected_matrix = _strip_leading_quantifiers(expected)
    if len(candidate_prefix) < 2 or len(candidate_prefix) != len(expected_prefix):
        return False

    mapping = _matrix_variable_mapping(candidate_matrix, expected_matrix)
    if mapping is None:
        return False

    candidate_by_expected = {}
    candidate_mapped_order = []
    for operator, variable in candidate_prefix:
        expected_variable = mapping.get(variable)
        if expected_variable is None or expected_variable in candidate_by_expected:
            return False
        candidate_by_expected[expected_variable] = operator
        candidate_mapped_order.append(expected_variable)

    expected_by_variable = {
        variable: operator for operator, variable in expected_prefix
    }
    if candidate_by_expected != expected_by_variable:
        return False
    expected_order = [variable for _operator, variable in expected_prefix]
    return candidate_mapped_order != expected_order


def _identity_usage(formula: FOLFormula) -> tuple[bool, bool]:
    """Return whether a formula uses equality and explicit distinctness."""

    if formula.kind == "identity":
        return True, False
    if formula.kind == "negation":
        if formula.body.kind == "identity":
            return False, True
        return _identity_usage(formula.body)
    if formula.kind == "binary":
        left_equality, left_distinctness = _identity_usage(formula.left)
        right_equality, right_distinctness = _identity_usage(formula.right)
        return (
            left_equality or right_equality,
            left_distinctness or right_distinctness,
        )
    if formula.kind == "quantifier":
        return _identity_usage(formula.body)
    return False, False


def _translation_mismatch_code(
    candidate: FOLFormula,
    expected: FOLFormula,
    candidate_binders: dict[str, list[object]] | None = None,
    expected_binders: dict[str, list[object]] | None = None,
) -> str:
    """Locate the first pedagogically useful structural mismatch."""

    candidate_binders = candidate_binders if candidate_binders is not None else {}
    expected_binders = expected_binders if expected_binders is not None else {}
    candidate_equality, candidate_distinctness = _identity_usage(candidate)
    expected_equality, expected_distinctness = _identity_usage(expected)
    if expected_distinctness and not candidate_distinctness:
        return "translation.distinctness_missing"
    if expected_equality and not candidate_equality:
        return "translation.identity_missing"
    if candidate_distinctness and not expected_distinctness:
        return "translation.distinctness_extra"
    if candidate_equality and not expected_equality:
        return "translation.identity_extra"
    if _has_quantifier_order_mismatch(candidate, expected):
        return "translation.quantifier_order"
    if candidate.kind != expected.kind:
        if "negation" in {candidate.kind, expected.kind}:
            return "translation.negation_scope"
        if "quantifier" in {candidate.kind, expected.kind}:
            return "translation.quantifier_scope"
        return "translation.structure_mismatch"

    if candidate.kind == "quantifier":
        if candidate.operator != expected.operator:
            return "translation.quantifier_kind"
        marker = object()
        candidate_stack = candidate_binders.setdefault(candidate.variable, [])
        expected_stack = expected_binders.setdefault(expected.variable, [])
        candidate_stack.append(marker)
        expected_stack.append(marker)
        code = _translation_mismatch_code(
            candidate.body,
            expected.body,
            candidate_binders,
            expected_binders,
        )
        candidate_stack.pop()
        expected_stack.pop()
        if not candidate_stack:
            candidate_binders.pop(candidate.variable, None)
        if not expected_stack:
            expected_binders.pop(expected.variable, None)
        return code

    if candidate.kind == "binary":
        if candidate.operator != expected.operator:
            return "translation.connective"
        if (
            candidate.operator == "→"
            and _nodes_match_with_binders(
                candidate.left,
                expected.right,
                candidate_binders,
                expected_binders,
            )
            and _nodes_match_with_binders(
                candidate.right,
                expected.left,
                candidate_binders,
                expected_binders,
            )
        ):
            return "translation.condition_direction"
        if not _nodes_match_with_binders(
            candidate.left,
            expected.left,
            candidate_binders,
            expected_binders,
        ):
            return _translation_mismatch_code(
                candidate.left,
                expected.left,
                candidate_binders,
                expected_binders,
            )
        return _translation_mismatch_code(
            candidate.right,
            expected.right,
            candidate_binders,
            expected_binders,
        )

    if candidate.kind == "negation":
        return _translation_mismatch_code(
            candidate.body,
            expected.body,
            candidate_binders,
            expected_binders,
        )

    if candidate.kind == "predicate":
        if candidate.predicate != expected.predicate:
            return "translation.predicate"
        if len(candidate.terms) != len(expected.terms):
            return "translation.arity"
        candidate_terms = tuple(
            _term_binding_key(term, candidate_binders)
            for term in candidate.terms
        )
        expected_terms = tuple(
            _term_binding_key(term, expected_binders)
            for term in expected.terms
        )
        if (
            candidate_terms != expected_terms
            and Counter(candidate_terms) == Counter(expected_terms)
        ):
            return "translation.argument_order"
        if candidate_terms != expected_terms:
            return "translation.term"
        return "translation.structure_mismatch"

    return "translation.structure_mismatch"


def assess_fol_symbolization(
    source: str,
    accepted_sources,
    signature: FOLSignature,
) -> dict:
    """Check a candidate against explicitly approved translation structures.

    This checker is intentionally narrower than semantic equivalence. Stage E
    assesses whether the learner captured the requested linguistic structure;
    model-theoretic equivalence remains a Stage F responsibility.
    """

    accepted_formulas = []
    for accepted_source in accepted_sources:
        formula = parse_fol(accepted_source, signature)
        if not formula.is_sentence:
            raise ValueError(
                "Kabul edilen sembolleştirme serbest değişken içeremez: "
                f"{accepted_source!r}."
            )
        accepted_formulas.append(formula)
    if not accepted_formulas:
        raise ValueError("En az bir kabul edilen sembolleştirme verilmelidir.")

    try:
        candidate = parse_fol(source, signature)
    except FOLParseError as exc:
        return {
            "accepted": False,
            "rendered": None,
            "matched_index": None,
            "issue_code": exc.code,
            "message": exc.message,
            "position": exc.position,
        }

    if not candidate.is_sentence:
        free = ", ".join(sorted(candidate.free_variables))
        return {
            "accepted": False,
            "rendered": candidate.render(),
            "matched_index": None,
            "issue_code": "translation.free_variable",
            "message": f"Cümlede serbest değişken kaldı: {free}.",
            "position": None,
        }

    for index, expected in enumerate(accepted_formulas):
        if formulas_alpha_equivalent(candidate, expected):
            return {
                "accepted": True,
                "rendered": candidate.render(),
                "matched_index": index,
                "issue_code": None,
                "message": "",
                "position": None,
            }

    issue_codes = [
        _translation_mismatch_code(candidate, expected)
        for expected in accepted_formulas
    ]
    priority = (
        "translation.condition_direction",
        "translation.identity_missing",
        "translation.distinctness_missing",
        "translation.distinctness_extra",
        "translation.identity_extra",
        "translation.quantifier_order",
        "translation.negation_scope",
        "translation.quantifier_kind",
        "translation.quantifier_scope",
        "translation.connective",
        "translation.free_variable",
        "translation.argument_order",
        "translation.predicate",
        "translation.arity",
        "translation.term",
        "translation.structure_mismatch",
    )
    issue_code = next(
        (code for code in priority if code in issue_codes),
        "translation.structure_mismatch",
    )
    return {
        "accepted": False,
        "rendered": candidate.render(),
        "matched_index": None,
        "issue_code": issue_code,
        "message": "Formül hedeflenen doğal dil yapısını korumuyor.",
        "position": None,
    }


def _analyse_variables(formula: FOLFormula) -> tuple[list[dict], list[dict]]:
    occurrences = []
    warnings = []

    def visit(node: FOLFormula, binders: dict[str, list[FOLFormula]]) -> None:
        if node.kind in {"predicate", "identity"}:
            for term in node.terms:
                if term.kind != "variable":
                    continue
                stack = binders.get(term.symbol, [])
                binder = stack[-1] if stack else None
                occurrences.append(
                    {
                        "symbol": term.symbol,
                        "start": term.start,
                        "end": term.end,
                        "bound": binder is not None,
                        "binder_start": binder.start if binder is not None else None,
                        "binder_operator": (
                            binder.operator if binder is not None else None
                        ),
                    }
                )
            return
        if node.kind == "negation":
            visit(node.body, binders)
            return
        if node.kind == "binary":
            visit(node.left, binders)
            visit(node.right, binders)
            return
        if node.kind == "quantifier":
            stack = binders.setdefault(node.variable, [])
            if stack:
                warnings.append(
                    {
                        "code": "quantifier.shadowing",
                        "message": (
                            f"{node.variable} değişkeni iç kapsamda yeniden "
                            "niceleyicilendi."
                        ),
                        "position": node.start,
                    }
                )
            before = len(occurrences)
            stack.append(node)
            visit(node.body, binders)
            stack.pop()
            if not stack:
                binders.pop(node.variable, None)
            bound_here = any(
                occurrence["binder_start"] == node.start
                for occurrence in occurrences[before:]
            )
            if not bound_here:
                warnings.append(
                    {
                        "code": "quantifier.vacuous",
                        "message": (
                            f"{node.operator}{node.variable} niceleyicisi "
                            "kapsamında hiçbir serbest oluşumu bağlamıyor."
                        ),
                        "position": node.start,
                    }
                )
            return
        raise ValueError(f"Bilinmeyen FOL düğüm türü: {node.kind!r}.")

    visit(formula, {})
    return occurrences, warnings


def classify_fol_expression(source: str, signature: FOLSignature) -> dict:
    """Classify a vocabulary item, term, open formula, or sentence."""

    tokens = _tokenize(source)
    if len(tokens) == 1:
        token = tokens[0]
        if token.kind == "predicate":
            if token.value not in signature.predicates:
                raise FOLParseError(
                    "predicate.unknown",
                    f"{token.value} yüklemi sembol anahtarında tanımlı değil.",
                    token.start,
                )
            return {
                "category": "predicate",
                "rendered": token.value,
                "formula": None,
                "free_variables": [],
                "occurrences": [],
                "warnings": [],
            }
        if token.kind == "term":
            if token.value in signature.names:
                category = "name"
            elif token.value in signature.variables:
                category = "variable"
            else:
                raise FOLParseError(
                    "term.unknown",
                    f"{token.value} sembolü anahtarda ad veya değişken değil.",
                    token.start,
                )
            return {
                "category": category,
                "rendered": token.value,
                "formula": None,
                "free_variables": (
                    [token.value] if category == "variable" else []
                ),
                "occurrences": [],
                "warnings": [],
            }

    formula = _Parser(tokens, signature).parse()
    free_variables = sorted(formula.free_variables)
    return {
        "category": "sentence" if formula.is_sentence else "open_formula",
        "rendered": formula.render(),
        "formula": formula,
        "free_variables": free_variables,
        "occurrences": list(formula.variable_occurrences),
        "warnings": list(formula.warnings),
    }


def audit_fol_expression(source: str, signature: FOLSignature) -> dict:
    """Return a serialisable classification or a stable syntax issue."""

    try:
        result = classify_fol_expression(source, signature)
    except FOLParseError as exc:
        return {
            "accepted": False,
            "category": None,
            "rendered": None,
            "free_variables": [],
            "occurrences": [],
            "warnings": [],
            "issue_code": exc.code,
            "message": exc.message,
            "position": exc.position,
        }
    return {
        "accepted": True,
        **{key: value for key, value in result.items() if key != "formula"},
        "issue_code": None,
        "message": "",
        "position": None,
    }
