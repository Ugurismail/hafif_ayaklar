"""Shared token normalization for Turkish word statistics and their filters."""

import re
import unicodedata


WORD_PATTERN = re.compile(r'\b\w+\b', re.UNICODE)
TURKISH_CASE_MAP = str.maketrans({'I': 'ı', 'İ': 'i'})


def normalize_word(text):
    return unicodedata.normalize('NFC', text or '').translate(TURKISH_CASE_MAP).lower().strip()


def word_tokens(text):
    return WORD_PATTERN.findall(normalize_word(text))


def excluded_word_set(text):
    return {normalize_word(word) for word in (text or '').split(',') if word.strip()}
