"""Request-scoped bulk loading for links embedded in answer content."""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
import re
import unicodedata

from django.contrib.auth.models import User
from django.db.models import Q

from .models import Definition, Question, Reference


DEFINITION_RE = re.compile(r"\((?:tanim|t):[^:]+:(\d+)\)", re.IGNORECASE)
REFERENCE_RE = re.compile(r"\((?:kaynak|k):(\d+)", re.IGNORECASE)
QUESTION_REFERENCE_RE = re.compile(r"\((?:ref|r):([^\)]+)\)", re.IGNORECASE)
MENTION_RE = re.compile(r"@([\w.\-\u00A0 ]{1,50})")

_definitions = ContextVar("content_link_definitions", default=None)
_references = ContextVar("content_link_references", default=None)
_questions = ContextVar("content_link_questions", default=None)
_users = ContextVar("content_link_users", default=None)


def _normalize_mention(value):
    candidate = unicodedata.normalize("NFKC", value or "").replace("\u00A0", " ")
    for dash in ("‐", "‑", "‒", "–", "—", "−"):
        candidate = candidate.replace(dash, "-")
    return " ".join(candidate.split())


def _build_case_insensitive_filter(field_name, values):
    query = Q()
    for value in values:
        query |= Q(**{f"{field_name}__iexact": value})
    return query


@contextmanager
def preload_content_links(texts):
    texts = [str(text or "") for text in texts]
    definition_ids = {
        int(match.group(1))
        for text in texts
        for match in DEFINITION_RE.finditer(text)
    }
    reference_ids = {
        int(match.group(1))
        for text in texts
        for match in REFERENCE_RE.finditer(text)
    }
    question_labels = {
        match.group(1).strip()
        for text in texts
        for match in QUESTION_REFERENCE_RE.finditer(text)
        if match.group(1).strip()
    }

    username_candidates = set()
    for text in texts:
        for match in MENTION_RE.finditer(text):
            words = _normalize_mention(match.group(1)).split()
            username_candidates.update(
                " ".join(words[:index])
                for index in range(1, len(words) + 1)
            )

    definition_map = {
        item.id: item
        for item in Definition.objects.filter(id__in=definition_ids)
        .select_related("user")
        .only("id", "definition_text", "user__username")
    } if definition_ids else {}
    reference_map = Reference.objects.only(
        "id",
        "author_surname",
        "author_name",
        "year",
        "metin_ismi",
        "rest",
        "abbreviation",
    ).in_bulk(reference_ids) if reference_ids else {}

    question_map = {}
    if question_labels:
        questions = Question.objects.only("question_text", "slug").filter(
            _build_case_insensitive_filter("question_text", question_labels)
        )
        question_map = {item.question_text.casefold(): item for item in questions}

    user_map = {}
    if username_candidates:
        users = User.objects.only("username").filter(
            _build_case_insensitive_filter("username", username_candidates)
        )
        user_map = {item.username.casefold(): item for item in users}

    tokens = (
        (_definitions, _definitions.set(definition_map)),
        (_references, _references.set(reference_map)),
        (_questions, _questions.set(question_map)),
        (_users, _users.set(user_map)),
    )
    try:
        yield
    finally:
        for variable, token in reversed(tokens):
            variable.reset(token)


def get_preloaded_definition(definition_id):
    mapping = _definitions.get()
    return mapping is not None, mapping.get(int(definition_id)) if mapping is not None else None


def get_preloaded_reference(reference_id):
    mapping = _references.get()
    return mapping is not None, mapping.get(int(reference_id)) if mapping is not None else None


def get_preloaded_question(label):
    mapping = _questions.get()
    return mapping is not None, mapping.get(label.casefold()) if mapping is not None else None


def get_preloaded_user(username):
    mapping = _users.get()
    return mapping is not None, mapping.get(username.casefold()) if mapping is not None else None
