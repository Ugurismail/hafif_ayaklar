"""Stable entry references shared by HTML rendering and document exports."""

from contextvars import ContextVar
from html.parser import HTMLParser
import re

from django.urls import reverse


ENTRY_REFERENCE_RE = re.compile(r"(?<![\w/#\\=])#([1-9][0-9]{0,9})(?![\w])")
MAX_ENTRY_ID = 2147483647
preloaded_entry_ids = ContextVar("content_link_entries", default=None)
_collected_entry_ids = ContextVar("collected_entry_reference_ids", default=None)


def referenced_entry_ids(text):
    return {
        int(match.group(1)) for match in ENTRY_REFERENCE_RE.finditer(text or "")
        if int(match.group(1)) <= MAX_ENTRY_ID
    }


def available_entry_ids(ids):
    from .models import Answer

    ids = sorted(set(ids))
    available = set()
    # Stay below SQLite parameter limits as well as bounding individual queries.
    for offset in range(0, len(ids), 500):
        available.update(Answer.objects.filter(
            id__in=ids[offset:offset + 500], user__is_active=True,
        ).values_list("id", flat=True))
    return available


def entry_path(entry_id):
    return reverse("entry_permalink", args=[entry_id])


class _TextSpans(HTMLParser):
    """Locate text without reserializing SVG or altering sanitized HTML."""

    SKIP = {"a", "code", "pre", "script", "style", "svg", "math", "textarea"}

    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.offsets = [0]
        for match in re.finditer("\n", source):
            self.offsets.append(match.end())
        self.blocked = dict.fromkeys(self.SKIP, 0)
        self.spans = []
        self.feed(source)
        self.close()

    def handle_starttag(self, tag, attrs):
        if tag in self.blocked:
            self.blocked[tag] += 1

    def handle_endtag(self, tag):
        if tag in self.blocked:
            self.blocked[tag] = max(0, self.blocked[tag] - 1)

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_data(self, data):
        if not any(self.blocked.values()) and ENTRY_REFERENCE_RE.search(data):
            line, column = self.getpos()
            start = self.offsets[line - 1] + column
            self.spans.append((start, start + len(data), data))


def link_entry_references(html):
    spans = _TextSpans(html).spans
    ids = set().union(*(referenced_entry_ids(text) for _, _, text in spans)) if spans else set()
    if not ids:
        return html
    collected = _collected_entry_ids.get()
    if collected is not None:
        collected.update(ids)
        return html
    available = preloaded_entry_ids.get()
    if available is None:
        available = available_entry_ids(ids)

    def replace(match):
        entry_id = int(match.group(1))
        if entry_id not in available:
            return match.group(0)
        return (
            f'<a href="{entry_path(entry_id)}" class="entry-reference" '
            f'title="Entry #{entry_id}">#{entry_id}</a>'
        )

    for start, end, text in reversed(spans):
        html = html[:start] + ENTRY_REFERENCE_RE.sub(replace, text) + html[end:]
    return html


def published_entry_reference_ids(text):
    """Use the display parser so code, math and escaped references stay silent."""
    from .templatetags.custom_tags import safe_markdownify

    if not referenced_entry_ids(text):
        return set()
    collected = set()
    token = _collected_entry_ids.set(collected)
    try:
        safe_markdownify(text)
    finally:
        _collected_entry_ids.reset(token)
    return collected


def notify_entry_references(source, target_ids, *, using):
    from collections import defaultdict
    from django.db import transaction
    from .models import Answer, EntryReferenceNotice, Notification

    if not target_ids:
        return
    with transaction.atomic(using=using):
        recipients = defaultdict(list)
        target_ids = sorted(target_ids)
        for offset in range(0, len(target_ids), 500):
            targets = Answer.objects.using(using).filter(
                id__in=target_ids[offset:offset + 500], user__is_active=True,
            ).exclude(user_id=source.user_id).order_by('pk').values_list('pk', 'user_id')
            for target_id, recipient_id in targets:
                # A database constraint prevents repeat delivery, even after removal
                # and re-addition or two saves racing to publish the same reference.
                _, created = EntryReferenceNotice.objects.using(using).get_or_create(
                    source_id=source.pk, target_id=target_id,
                )
                if created:
                    recipients[recipient_id].append(target_id)

        notifications = []
        for recipient_id, ids in recipients.items():
            references = ', '.join(f'#{entry_id}' for entry_id in ids[:3])
            if len(ids) > 3:
                references += f' ve {len(ids) - 3} diğer'
            noun = 'entry’ne' if len(ids) == 1 else 'entry’lerine'
            notifications.append(Notification(
                recipient_id=recipient_id,
                sender_id=source.user_id,
                notification_type='entry_reference',
                message=f'{source.user.username}, {references} numaralı {noun} referans verdi.',
                related_answer_id=source.pk,
                related_question_id=source.question_id,
            ))
        Notification.objects.using(using).bulk_create(notifications, batch_size=100)


_PROTECTED_MARKDOWN = re.compile(
    r"```[\s\S]*?```|~~~[\s\S]*?~~~|`+[^`]*`+"
    r"|\$\$[\s\S]*?\$\$|(?<!\\)\$[^\n$]+\$"
    r"|!?\[[^\]\n]*\]\([^\n)]*\)|<[^>]*>"
    r"|https?://[^\s<>]+|(?m:^[ \t]{4,}[^\n]*)"
)


def entry_references_for_export(text, available):
    def replace(match):
        entry_id = int(match.group(1))
        if entry_id not in available:
            return match.group(0)
        return f"[#{entry_id}](https://hafifayaklar.com{entry_path(entry_id)})"

    return transform_markdown_prose(text, lambda part: ENTRY_REFERENCE_RE.sub(replace, part))


def transform_markdown_prose(text, transform):
    """Leave explicit links, code, formulas and attributes literal."""
    parts = []
    position = 0
    for match in _PROTECTED_MARKDOWN.finditer(text):
        parts.append(transform(text[position:match.start()]))
        parts.append(match.group(0))
        position = match.end()
    parts.append(transform(text[position:]))
    return "".join(parts)
