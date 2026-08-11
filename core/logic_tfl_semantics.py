"""Small, strict semantic core for release-candidate TFL lessons.

The learner-facing logic course does not import this module. It exists so
candidate examples and answer keys can be checked independently instead of
trusting hand-written truth values.
"""

from dataclasses import dataclass
from itertools import product
from typing import Iterable


BINARY_CONNECTIVES = frozenset({"∧", "∨", "→", "↔"})
TFL_SYMBOLS = frozenset({"¬", *BINARY_CONNECTIVES, "(", ")"})
SUBSCRIPT_DIGITS = frozenset("₀₁₂₃₄₅₆₇₈₉")
SUBSCRIPT_TO_ASCII = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
MAX_COMPLETE_TABLE_ATOMS = 8


class TFLParseError(ValueError):
    """Raised when a string is not a sentence of the supported TFL syntax."""


@dataclass(frozen=True)
class TFLFormula:
    """Parsed TFL sentence.

    ``operator`` is ``"atom"`` for sentence letters, ``"¬"`` for negation,
    or one of the binary connectives. Binary nodes use ``left`` and ``right``;
    negations use ``right``.
    """

    operator: str
    atom: str | None = None
    left: "TFLFormula | None" = None
    right: "TFLFormula | None" = None

    @property
    def main_connective(self) -> str | None:
        return None if self.operator == "atom" else self.operator

    @property
    def atoms(self) -> frozenset[str]:
        if self.operator == "atom":
            return frozenset({self.atom})
        if self.operator == "¬":
            return self.right.atoms
        return self.left.atoms | self.right.atoms

    def render(self) -> str:
        if self.operator == "atom":
            return self.atom
        if self.operator == "¬":
            child = self.right.render()
            return f"¬{child}"
        return f"({self.left.render()} {self.operator} {self.right.render()})"


def _tokenize(source: str) -> list[str]:
    if not isinstance(source, str) or not source.strip():
        raise TFLParseError("TFL cümlesi boş olamaz.")

    tokens = []
    index = 0
    while index < len(source):
        char = source[index]
        if char.isspace():
            index += 1
            continue
        if char in TFL_SYMBOLS:
            tokens.append(char)
            index += 1
            continue
        if "A" <= char <= "Z":
            end = index + 1
            while end < len(source) and source[end] in SUBSCRIPT_DIGITS:
                end += 1
            if end < len(source) and source[end] == "_":
                digit_start = end + 1
                end = digit_start
                while end < len(source) and source[end].isdigit():
                    end += 1
                if end == digit_start:
                    raise TFLParseError(
                        "Alt indis alt çizgiden sonra en az bir rakam içermelidir."
                    )
            tokens.append(source[index:end])
            index = end
            continue
        raise TFLParseError(
            f"Desteklenmeyen TFL sembolü: {char!r}."
        )
    return tokens


class _Parser:
    def __init__(self, tokens: list[str]):
        self.tokens = tokens
        self.position = 0

    def parse(self) -> TFLFormula:
        formula = self._parse_expression()
        if self._peek() is not None:
            raise TFLParseError(
                f"Beklenmeyen sembol: {self._peek()!r}. "
                "Her ikili kurulumda kapsamı parantezle açıkça göster."
            )
        return formula

    def _parse_expression(self) -> TFLFormula:
        left = self._parse_unit()
        if self._peek() not in BINARY_CONNECTIVES:
            return left

        operator = self._take()
        right = self._parse_unit()
        if self._peek() in BINARY_CONNECTIVES:
            raise TFLParseError(
                "Bir kapsamda birden fazla ikili bağlaç parantezsiz bırakılamaz."
            )
        return TFLFormula(operator=operator, left=left, right=right)

    def _parse_unit(self) -> TFLFormula:
        token = self._peek()
        if token is None:
            raise TFLParseError("TFL cümlesi tamamlanmadan sona erdi.")
        if token == "¬":
            self._take()
            return TFLFormula(operator="¬", right=self._parse_unit())
        if token == "(":
            self._take()
            formula = self._parse_expression()
            if self._peek() != ")":
                raise TFLParseError("Açılan parantezin kapanışı bulunamadı.")
            self._take()
            return formula
        if token == ")":
            raise TFLParseError("Karşılıksız kapanış parantezi bulundu.")
        if token in BINARY_CONNECTIVES:
            raise TFLParseError(
                f"{token} bağlacının solunda bir TFL cümlesi bulunmalıdır."
            )

        self._take()
        return TFLFormula(operator="atom", atom=token)

    def _peek(self) -> str | None:
        if self.position >= len(self.tokens):
            return None
        return self.tokens[self.position]

    def _take(self) -> str:
        token = self._peek()
        if token is None:
            raise TFLParseError("TFL cümlesi tamamlanmadan sona erdi.")
        self.position += 1
        return token


def parse_tfl(source: str) -> TFLFormula:
    """Parse a strict TFL sentence, allowing only the outer parentheses to drop."""

    return _Parser(_tokenize(source)).parse()


def _normalise_truth_value(value: bool | str, atom: str) -> bool:
    if isinstance(value, bool):
        return value
    if value == "T":
        return True
    if value == "F":
        return False
    raise ValueError(
        f"{atom} için doğruluk değeri bool, 'T' veya 'F' olmalıdır."
    )


def _evaluate_node(node: TFLFormula, valuation: dict[str, bool | str]) -> bool:
    if node.operator == "atom":
        if node.atom not in valuation:
            raise ValueError(f"Değerlemede {node.atom} atomu eksik.")
        return _normalise_truth_value(valuation[node.atom], node.atom)

    if node.operator == "¬":
        return not _evaluate_node(node.right, valuation)

    left = _evaluate_node(node.left, valuation)
    right = _evaluate_node(node.right, valuation)
    if node.operator == "∧":
        return left and right
    if node.operator == "∨":
        return left or right
    if node.operator == "→":
        return (not left) or right
    if node.operator == "↔":
        return left == right
    raise ValueError(f"Bilinmeyen TFL bağlacı: {node.operator}")


def evaluate_tfl(
    formula: str | TFLFormula,
    valuation: dict[str, bool | str],
) -> bool:
    """Evaluate one TFL sentence under one supplied valuation."""

    parsed = parse_tfl(formula) if isinstance(formula, str) else formula
    return _evaluate_node(parsed, valuation)


def evaluation_trace(
    formula: str | TFLFormula,
    valuation: dict[str, bool | str],
) -> list[dict[str, str]]:
    """Return a post-order, inside-out evaluation trace for one valuation."""

    parsed = parse_tfl(formula) if isinstance(formula, str) else formula
    steps = []

    def visit(node: TFLFormula) -> None:
        if node.left is not None:
            visit(node.left)
        if node.right is not None:
            visit(node.right)
        steps.append(
            {
                "formula": node.render(),
                "value": "T" if _evaluate_node(node, valuation) else "F",
            }
        )

    visit(parsed)
    return steps


def _atom_sort_key(atom: str) -> tuple[str, int, str]:
    suffix = atom[1:]
    if not suffix:
        return atom[0], -1, atom
    if suffix.startswith("_"):
        suffix = suffix[1:]
    else:
        suffix = suffix.translate(SUBSCRIPT_TO_ASCII)
    return atom[0], int(suffix), atom


def ordered_atoms(formula: str | TFLFormula) -> list[str]:
    """Return distinct sentence letters in stable alphabetical/index order."""

    parsed = parse_tfl(formula) if isinstance(formula, str) else formula
    return sorted(parsed.atoms, key=_atom_sort_key)


def generate_valuations(
    atoms: Iterable[str],
    *,
    max_atoms: int = MAX_COMPLETE_TABLE_ATOMS,
) -> list[dict[str, str]]:
    """Generate every valuation in the standard T-first block pattern."""

    unique_atoms = sorted(set(atoms), key=_atom_sort_key)
    if not unique_atoms:
        raise ValueError("En az bir TFL cümle harfi gereklidir.")
    if len(unique_atoms) > max_atoms:
        raise ValueError(
            "Tam tablo güvenlik sınırını aşıyor: "
            f"en fazla {max_atoms} farklı atom kullanılabilir."
        )
    for atom in unique_atoms:
        parsed = parse_tfl(atom)
        if parsed.operator != "atom" or parsed.atom != atom:
            raise ValueError(f"Geçersiz TFL cümle harfi: {atom!r}.")

    return [
        {
            atom: "T" if value else "F"
            for atom, value in zip(unique_atoms, values)
        }
        for values in product((True, False), repeat=len(unique_atoms))
    ]


def compound_subformulas(
    formula: str | TFLFormula,
) -> list[TFLFormula]:
    """Return distinct compound subformulas in dependency order."""

    parsed = parse_tfl(formula) if isinstance(formula, str) else formula
    ordered = []
    seen = set()

    def visit(node: TFLFormula) -> None:
        if node.left is not None:
            visit(node.left)
        if node.right is not None:
            visit(node.right)
        if node.operator != "atom" and node not in seen:
            seen.add(node)
            ordered.append(node)

    visit(parsed)
    return ordered


def complete_truth_table(
    formula: str | TFLFormula,
    *,
    max_atoms: int = MAX_COMPLETE_TABLE_ATOMS,
) -> dict:
    """Build a complete table without assigning a later semantic-status label."""

    parsed = parse_tfl(formula) if isinstance(formula, str) else formula
    atoms = ordered_atoms(parsed)
    valuations = generate_valuations(atoms, max_atoms=max_atoms)
    compounds = compound_subformulas(parsed)
    main_column = parsed.render()
    columns = [
        {
            "formula": atom,
            "kind": "atom",
            "is_main": parsed.operator == "atom" and atom == main_column,
        }
        for atom in atoms
    ]
    columns.extend(
        {
            "formula": node.render(),
            "kind": "subformula",
            "is_main": node == parsed,
        }
        for node in compounds
    )

    rows = []
    for valuation in valuations:
        values = dict(valuation)
        for node in compounds:
            values[node.render()] = (
                "T" if evaluate_tfl(node, valuation) else "F"
            )
        rows.append({"valuation": valuation, "values": values})

    return {
        "formula": parsed.render(),
        "atoms": atoms,
        "row_count": len(rows),
        "columns": columns,
        "main_column": main_column,
        "rows": rows,
    }


def classify_semantic_status(
    formula: str | TFLFormula,
    *,
    max_atoms: int = MAX_COMPLETE_TABLE_ATOMS,
) -> dict:
    """Classify one TFL formula from every row of its complete table."""

    table = complete_truth_table(formula, max_atoms=max_atoms)
    main_column = table["main_column"]
    true_valuations = []
    false_valuations = []

    for row in table["rows"]:
        target = (
            true_valuations
            if row["values"][main_column] == "T"
            else false_valuations
        )
        target.append(dict(row["valuation"]))

    if not false_valuations:
        status = "tautology"
    elif not true_valuations:
        status = "contradiction"
    else:
        status = "contingency"

    return {
        "formula": table["formula"],
        "status": status,
        "row_count": table["row_count"],
        "true_count": len(true_valuations),
        "false_count": len(false_valuations),
        "true_valuations": true_valuations,
        "false_valuations": false_valuations,
    }


def analyze_semantic_equivalence(
    left: str | TFLFormula,
    right: str | TFLFormula,
    *,
    max_atoms: int = MAX_COMPLETE_TABLE_ATOMS,
) -> dict:
    """Compare two TFL formulas under every valuation of their shared space."""

    parsed_left = parse_tfl(left) if isinstance(left, str) else left
    parsed_right = parse_tfl(right) if isinstance(right, str) else right
    atoms = sorted(
        parsed_left.atoms | parsed_right.atoms,
        key=_atom_sort_key,
    )
    valuations = generate_valuations(atoms, max_atoms=max_atoms)
    separating_valuations = []

    for valuation in valuations:
        if evaluate_tfl(parsed_left, valuation) != evaluate_tfl(
            parsed_right,
            valuation,
        ):
            separating_valuations.append(dict(valuation))

    return {
        "left_formula": parsed_left.render(),
        "right_formula": parsed_right.render(),
        "atoms": atoms,
        "row_count": len(valuations),
        "equivalent": not separating_valuations,
        "separating_valuations": separating_valuations,
    }


def analyze_joint_satisfiability(
    formulas: Iterable[str | TFLFormula],
    *,
    max_atoms: int = MAX_COMPLETE_TABLE_ATOMS,
) -> dict:
    """Find valuations that make every formula in a non-empty set true."""

    parsed_formulas = [
        parse_tfl(formula) if isinstance(formula, str) else formula
        for formula in formulas
    ]
    if not parsed_formulas:
        raise ValueError("En az bir TFL cümlesi gereklidir.")

    atoms = sorted(
        set().union(*(formula.atoms for formula in parsed_formulas)),
        key=_atom_sort_key,
    )
    valuations = generate_valuations(atoms, max_atoms=max_atoms)
    satisfying_valuations = [
        dict(valuation)
        for valuation in valuations
        if all(
            evaluate_tfl(formula, valuation)
            for formula in parsed_formulas
        )
    ]

    return {
        "formulas": [formula.render() for formula in parsed_formulas],
        "atoms": atoms,
        "row_count": len(valuations),
        "jointly_satisfiable": bool(satisfying_valuations),
        "satisfying_valuations": satisfying_valuations,
    }


def analyze_semantic_consequence(
    premises: Iterable[str | TFLFormula],
    conclusion: str | TFLFormula,
    *,
    max_atoms: int = MAX_COMPLETE_TABLE_ATOMS,
) -> dict:
    """Test whether every valuation making the premises true makes the conclusion true."""

    parsed_premises = [
        parse_tfl(premise) if isinstance(premise, str) else premise
        for premise in premises
    ]
    parsed_conclusion = (
        parse_tfl(conclusion) if isinstance(conclusion, str) else conclusion
    )
    atoms = sorted(
        set().union(
            parsed_conclusion.atoms,
            *(premise.atoms for premise in parsed_premises),
        ),
        key=_atom_sort_key,
    )
    valuations = generate_valuations(atoms, max_atoms=max_atoms)
    countervaluations = []
    premise_true_valuations = []

    for valuation in valuations:
        if all(
            evaluate_tfl(premise, valuation)
            for premise in parsed_premises
        ):
            premise_true_valuations.append(dict(valuation))
            if not evaluate_tfl(parsed_conclusion, valuation):
                countervaluations.append(dict(valuation))

    return {
        "premises": [premise.render() for premise in parsed_premises],
        "conclusion": parsed_conclusion.render(),
        "atoms": atoms,
        "row_count": len(valuations),
        "entails": not countervaluations,
        "premise_true_valuations": premise_true_valuations,
        "countervaluations": countervaluations,
    }


def find_target_valuations(
    requirements: Iterable[tuple[str | TFLFormula, bool | str]],
    *,
    max_atoms: int = MAX_COMPLETE_TABLE_ATOMS,
) -> dict:
    """Find valuations satisfying a non-empty set of formula/value targets."""

    parsed_requirements = []
    for formula, target_value in requirements:
        parsed = parse_tfl(formula) if isinstance(formula, str) else formula
        parsed_requirements.append(
            (
                parsed,
                _normalise_truth_value(target_value, parsed.render()),
            )
        )
    if not parsed_requirements:
        raise ValueError("En az bir hedef doğruluk koşulu gereklidir.")

    atoms = sorted(
        set().union(*(formula.atoms for formula, _ in parsed_requirements)),
        key=_atom_sort_key,
    )
    valuations = generate_valuations(atoms, max_atoms=max_atoms)
    matching_valuations = [
        dict(valuation)
        for valuation in valuations
        if all(
            evaluate_tfl(formula, valuation) == target
            for formula, target in parsed_requirements
        )
    ]

    return {
        "requirements": [
            {
                "formula": formula.render(),
                "target": "T" if target else "F",
            }
            for formula, target in parsed_requirements
        ],
        "atoms": atoms,
        "row_count": len(valuations),
        "matching_valuations": matching_valuations,
    }
