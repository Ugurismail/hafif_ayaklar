"""Private insertion history, independent of public citation usage statistics."""
from collections import Counter
from uuid import UUID

from django.db.models import Q
from django.utils import timezone

from .models import Kenarda, ReferenceUsage
from .utils import extract_reference_citations


def context_uuid(value):
    try:
        return UUID(str(value))
    except (ValueError, TypeError, AttributeError):
        return None


def bind_reference_history(user, data, *, answer=None, draft=None, prior_draft=None):
    """Only bind the writer's history after a successful content save."""
    context = context_uuid(data.get('reference_context'))
    selection = Q(pk__in=[])
    if context:
        selection |= Q(context_id=context, answer__isnull=True)
    if prior_draft:
        selection |= Q(draft=prior_draft)
    draft_id = data.get('draft_id')
    if isinstance(draft_id, (str, int)) and str(draft_id).isascii() and str(draft_id).isdigit() and len(str(draft_id)) < 19:
        own_draft = Kenarda.objects.filter(pk=draft_id, user=user).first()
        if own_draft:
            selection |= Q(draft=own_draft)
    if draft:
        selection |= Q(draft=draft)
    if answer:
        selection |= Q(answer=answer, status='published')
    ids = list(ReferenceUsage.objects.filter(selection, user=user).values_list('pk', flat=True))
    rows = ReferenceUsage.objects.filter(pk__in=ids, user=user)
    if answer:
        content, title, status = answer.answer_text, answer.question.question_text, 'published'
        rows.update(answer=answer, draft=None, title=title[:200], status=status)
    else:
        content = draft.content
        title = draft.title or (draft.question.question_text if draft.question else '')
        rows.update(draft=draft, title=title[:200], status='draft')
    # A removed occurrence stays in history; saving/reopening cannot change its time.
    counts = Counter((item['reference_id'], item['page'] or '') for item in extract_reference_citations(content))
    removed = []
    for row in rows.filter(removed_at__isnull=True).order_by('created_at', 'pk'):
        key = (row.reference_number, row.page)
        if counts[key]:
            counts[key] -= 1
        else:
            removed.append(row.pk)
    if removed:
        ReferenceUsage.objects.filter(pk__in=removed, user=user).update(removed_at=timezone.now())


def bind_saved_answer(request, answer):
    data = request.POST.copy()
    if not data.get('draft_id'):
        data['draft_id'] = request.GET.get('draft_id', '')
    bind_reference_history(request.user, data, answer=answer)
