from collections import defaultdict
from difflib import HtmlDiff
from difflib import SequenceMatcher
from html import escape
import re
import textwrap

from django.db.models import Count
from django.db import transaction
from django.utils import timezone
from django.utils.safestring import mark_safe

from .models import AnswerRevision, AnswerRevisionApproval, AnswerSuggestion, Notification


def ensure_initial_revision(answer):
    current = answer.get_current_revision()
    if current:
        return current

    return AnswerRevision.objects.create(
        answer=answer,
        parent_revision=None,
        base_revision=None,
        created_by=answer.user,
        content=answer.answer_text,
        revision_no=1,
        source='initial',
        change_summary='İlk yayın',
        is_current=True,
    )


def render_answer_content_html(raw_text):
    from .templatetags.custom_tags import (
        safe_markdownify,
        spoiler_link,
        bkz_link,
        tanim_link,
        reference_link,
        ref_link,
        mention_link,
        collapsible_images,
    )

    rendered = safe_markdownify(raw_text or '', "default")
    rendered = spoiler_link(rendered)
    rendered = bkz_link(rendered)
    rendered = tanim_link(rendered)
    rendered = reference_link(rendered)
    rendered = ref_link(rendered)
    rendered = mention_link(rendered)
    rendered = collapsible_images(rendered)
    return str(rendered)


def build_answer_render_preview(raw_text, max_chars=700):
    raw_text = raw_text or ''
    preview_text = raw_text if len(raw_text) <= max_chars else raw_text[:max_chars].rsplit(' ', 1)[0] + '...'
    return render_answer_content_html(preview_text)


def _collect_contributor_ids(answer, *, upto_revision=None):
    revisions = answer.revisions.all()
    if upto_revision is not None:
        revisions = revisions.filter(revision_no__lte=upto_revision.revision_no)

    contributor_ids = set(
        user_id for user_id in revisions.values_list('created_by_id', flat=True) if user_id
    )
    contributor_ids.add(answer.user_id)
    contributor_ids.update(
        user_id
        for user_id in revisions.exclude(accepted_suggestion__isnull=True).values_list(
            'accepted_suggestion__proposed_by_id',
            flat=True,
        )
        if user_id
    )
    return contributor_ids


def _ensure_revision_approval_snapshot(revision):
    if revision is None:
        return
    _ensure_revision_approval_snapshots([revision])


def _ensure_revision_approval_snapshots(revisions):
    revisions = [revision for revision in revisions if revision is not None]
    if not revisions:
        return

    revision_ids = [revision.id for revision in revisions]
    existing_revision_ids = set(
        AnswerRevisionApproval.objects.filter(revision_id__in=revision_ids)
        .values_list('revision_id', flat=True)
        .distinct()
    )
    missing_revisions = [revision for revision in revisions if revision.id not in existing_revision_ids]
    if not missing_revisions:
        return
    approvals = []
    for revision in missing_revisions:
        contributor_ids = _collect_contributor_ids(revision.answer, upto_revision=revision)
        if not contributor_ids:
            contributor_ids = {revision.answer.user_id}

        approvals.extend(
            AnswerRevisionApproval(
                revision=revision,
                user_id=user_id,
                status='approved',
                note='Bu sürüm, onay sistemi eklenmeden önce yayınlanmıştı.',
                responded_at=revision.created_at,
            )
            for user_id in contributor_ids
        )
    if approvals:
        AnswerRevisionApproval.objects.bulk_create(approvals, batch_size=100)


def _create_revision_review_requests(revision):
    implicit_approved_ids = {revision.answer.user_id, revision.created_by_id}
    if revision.accepted_suggestion_id and revision.accepted_suggestion and revision.accepted_suggestion.proposed_by_id:
        implicit_approved_ids.add(revision.accepted_suggestion.proposed_by_id)

    historical_contributor_ids = (
        _collect_contributor_ids(revision.answer, upto_revision=revision.parent_revision)
        if revision.parent_revision_id else {revision.answer.user_id}
    )

    approvals = []
    for user_id in sorted(historical_contributor_ids | implicit_approved_ids):
        if user_id in implicit_approved_ids:
            approvals.append(
                AnswerRevisionApproval(
                    revision=revision,
                    user_id=user_id,
                    status='approved',
                    note='Bu onay, yayınlama sırasında otomatik verildi.',
                    responded_at=timezone.now(),
                )
            )
        else:
            approvals.append(
                AnswerRevisionApproval(
                    revision=revision,
                    user_id=user_id,
                    status='pending',
                )
            )

    if approvals:
        AnswerRevisionApproval.objects.bulk_create(approvals, batch_size=100)

    user_model = revision.answer.user.__class__
    recipient_map = user_model.objects.in_bulk(
        [approval.user_id for approval in approvals if approval.status == 'pending']
    )
    for approval in approvals:
        if approval.status != 'pending':
            continue
        recipient = recipient_map.get(approval.user_id)
        if recipient is None:
            continue
        Notification.create_revision_review_notification(
            recipient=recipient,
            sender=revision.created_by,
            answer=revision.answer,
            revision=revision,
        )


def _sort_users_for_answer(users, owner_id):
    return sorted(users, key=lambda user: (0 if user.id == owner_id else 1, user.username.lower()))


def get_revision_approval_summaries(revisions, *, current_user=None):
    revisions = [revision for revision in revisions if revision is not None]
    if not revisions:
        return {}

    _ensure_revision_approval_snapshots(revisions)

    approvals = list(
        AnswerRevisionApproval.objects.filter(revision__in=revisions)
        .select_related('user', 'revision', 'revision__answer')
        .order_by('revision_id', 'user__username')
    )
    grouped = defaultdict(list)
    for approval in approvals:
        grouped[approval.revision_id].append(approval)

    summary_map = {}
    for revision in revisions:
        approved_users = []
        pending_users = []
        rejected_users = []
        current_user_approval = None

        for approval in grouped.get(revision.id, []):
            if current_user is not None and getattr(current_user, 'is_authenticated', False) and approval.user_id == current_user.id:
                current_user_approval = approval
            if approval.status == 'approved':
                approved_users.append(approval.user)
            elif approval.status == 'rejected':
                rejected_users.append(approval.user)
            else:
                pending_users.append(approval.user)

        approved_users = _sort_users_for_answer(approved_users, revision.answer.user_id)
        pending_users = _sort_users_for_answer(pending_users, revision.answer.user_id)
        rejected_users = _sort_users_for_answer(rejected_users, revision.answer.user_id)

        summary_map[revision.id] = {
            'approved_users': approved_users,
            'pending_users': pending_users,
            'rejected_users': rejected_users,
            'approved_usernames': [user.username for user in approved_users],
            'pending_usernames': [user.username for user in pending_users],
            'rejected_usernames': [user.username for user in rejected_users],
            'current_user_approval': current_user_approval,
        }

    return summary_map


def get_revision_approval_summary(revision, *, current_user=None):
    return get_revision_approval_summaries([revision], current_user=current_user).get(revision.id, {
        'approved_users': [],
        'pending_users': [],
        'rejected_users': [],
        'approved_usernames': [],
        'pending_usernames': [],
        'rejected_usernames': [],
        'current_user_approval': None,
    })


def attach_answer_revision_metadata(answers, current_user=None):
    answers = list(answers)
    if not answers:
        return answers

    answer_ids = [answer.id for answer in answers]

    current_revision_map = {
        revision.answer_id: revision
        for revision in AnswerRevision.objects.filter(
            answer_id__in=answer_ids,
            is_current=True,
        ).select_related('created_by')
    }
    revision_count_map = dict(
        AnswerRevision.objects.filter(answer_id__in=answer_ids)
        .values_list('answer_id')
        .annotate(total=Count('id'))
    )
    open_suggestion_map = dict(
        AnswerSuggestion.objects.filter(answer_id__in=answer_ids, status='open')
        .values_list('answer_id')
        .annotate(total=Count('id'))
    )

    current_revisions = []
    for answer in answers:
        current_revision = current_revision_map.get(answer.id) or ensure_initial_revision(answer)
        current_revisions.append(current_revision)

    _ensure_revision_approval_snapshots(current_revisions)

    approval_rows = list(
        AnswerRevisionApproval.objects.filter(
            revision_id__in=[revision.id for revision in current_revisions if revision]
        ).select_related('user')
    )
    approved_map = defaultdict(list)
    pending_map = defaultdict(list)
    rejected_map = defaultdict(list)
    current_user_approval_map = {}

    for approval in approval_rows:
        if current_user is not None and getattr(current_user, 'is_authenticated', False) and approval.user_id == current_user.id:
            current_user_approval_map[approval.revision_id] = approval
        if approval.status == 'approved':
            approved_map[approval.revision_id].append(approval.user)
        elif approval.status == 'rejected':
            rejected_map[approval.revision_id].append(approval.user)
        else:
            pending_map[approval.revision_id].append(approval.user)

    for answer in answers:
        current_revision = current_revision_map.get(answer.id) or ensure_initial_revision(answer)
        approved_users = _sort_users_for_answer(approved_map.get(current_revision.id, []), answer.user_id)
        pending_users = _sort_users_for_answer(pending_map.get(current_revision.id, []), answer.user_id)
        rejected_users = _sort_users_for_answer(rejected_map.get(current_revision.id, []), answer.user_id)
        contributor_usernames = [user.username for user in approved_users]

        answer.current_revision = current_revision
        answer.revision_count = revision_count_map.get(answer.id, 1)
        answer.open_suggestion_count = open_suggestion_map.get(answer.id, 0)
        answer.approved_contributors = approved_users
        answer.pending_contributors = pending_users
        answer.rejected_contributors = rejected_users
        answer.contributor_usernames = contributor_usernames
        answer.additional_contributors = [user.username for user in approved_users if user.id != answer.user_id]
        answer.pending_contributor_usernames = [user.username for user in pending_users]
        answer.rejected_contributor_usernames = [user.username for user in rejected_users]
        answer.last_revision_actor = current_revision.created_by.username if current_revision else answer.user.username
        answer.current_user_revision_approval = current_user_approval_map.get(current_revision.id)
        answer.current_user_can_review_revision = bool(
            answer.current_user_revision_approval
            and answer.current_user_revision_approval.status == 'pending'
            and current_revision.is_current
        )

    return answers


def build_answer_history_graph(answer, approval_summary_map=None):
    revisions = list(
        answer.revisions.select_related('created_by', 'accepted_suggestion', 'accepted_suggestion__proposed_by')
        .order_by('revision_no', 'created_at')
    )
    suggestions = list(
        answer.git_suggestions.select_related('base_revision', 'proposed_by', 'reviewed_by')
        .order_by('base_revision__revision_no', 'created_at', 'id')
    )

    node_width = 224
    node_height = 86
    top_padding = 84
    row_gap = 208
    branch_gap = 136
    revision_x = 72
    branch_start_x = 420
    branch_lane_gap = 340

    nodes = []
    edges = []
    revision_node_ids = {}
    revision_y_map = {}
    max_branch_depth = 0
    accepted_revision_by_suggestion_id = {
        revision.accepted_suggestion_id: revision
        for revision in revisions
        if revision.accepted_suggestion_id
    }

    for idx, revision in enumerate(revisions):
        summary = (
            approval_summary_map.get(revision.id)
            if approval_summary_map is not None
            else get_revision_approval_summary(revision)
        )
        node_id = f"revision-{revision.id}"
        revision_node_ids[revision.id] = node_id
        y = top_padding + idx * row_gap
        revision_y_map[revision.id] = y
        nodes.append({
            'id': node_id,
            'kind': 'revision',
            'x': revision_x,
            'y': y,
            'width': node_width,
            'height': node_height,
            'label': f"r{revision.revision_no}",
            'title': f"Sürüm r{revision.revision_no}",
            'meta': (
                f"{revision.created_by.username} · {revision.get_source_display()} · "
                f"Onay {len(summary['approved_users'])} · Bekleyen {len(summary['pending_users'])} · "
                f"Red {len(summary['rejected_users'])}"
            ),
            'status': 'current' if revision.is_current else 'published',
            'preview_html': build_answer_render_preview(revision.content, 520),
        })
        if revision.parent_revision_id and revision.parent_revision_id in revision_node_ids:
            edges.append({
                'from_id': revision_node_ids[revision.parent_revision_id],
                'to_id': node_id,
                'kind': 'main',
            })

    branch_counts = defaultdict(int)
    for suggestion in suggestions:
        base_y = revision_y_map.get(suggestion.base_revision_id, 48)
        branch_index = branch_counts[suggestion.base_revision_id]
        branch_counts[suggestion.base_revision_id] += 1
        lane_index = branch_index
        max_branch_depth = max(max_branch_depth, lane_index + 1)
        node_x = branch_start_x + lane_index * branch_lane_gap
        node_y = base_y + branch_index * branch_gap
        suggestion_node_id = f"suggestion-{suggestion.id}"
        nodes.append({
            'id': suggestion_node_id,
            'kind': 'suggestion',
            'x': node_x,
            'y': node_y,
            'width': node_width,
            'height': node_height,
            'label': f"Ö#{suggestion.id}",
            'title': f"Öneri #{suggestion.id}",
            'meta': f"{suggestion.proposed_by.username} · {suggestion.get_status_display()}",
            'status': suggestion.status,
            'preview_html': build_answer_render_preview(suggestion.proposed_text, 520),
        })
        if suggestion.base_revision_id in revision_node_ids:
            edges.append({
                'from_id': revision_node_ids[suggestion.base_revision_id],
                'to_id': suggestion_node_id,
                'kind': suggestion.status,
            })
        accepted_revision = accepted_revision_by_suggestion_id.get(suggestion.id)
        if accepted_revision and accepted_revision.id in revision_node_ids:
            edges.append({
                'from_id': suggestion_node_id,
                'to_id': revision_node_ids[accepted_revision.id],
                'kind': 'merge',
            })

    layout_height = max((node['y'] + node['height'] for node in nodes), default=0) + 72
    layout_width = max((node['x'] + node['width'] for node in nodes), default=0) + 140
    node_map = {node['id']: node for node in nodes}
    for edge in edges:
        source = node_map.get(edge['from_id'])
        target = node_map.get(edge['to_id'])
        if not source or not target:
            edge['path'] = ''
            continue
        if edge['kind'] == 'main':
            start_x = source['x'] + source['width'] / 2
            start_y = source['y'] + source['height']
            end_x = target['x'] + target['width'] / 2
            end_y = target['y']
            elbow_y = start_y + max((end_y - start_y) / 2, 28)
            edge['path'] = (
                f"M {start_x} {start_y} "
                f"L {start_x} {elbow_y} "
                f"L {end_x} {elbow_y} "
                f"L {end_x} {end_y}"
            )
        elif source['kind'] == 'revision' and target['kind'] == 'suggestion':
            start_x = source['x'] + source['width']
            start_y = source['y'] + source['height'] / 2
            end_x = target['x']
            end_y = target['y'] + target['height'] / 2
            elbow_x = start_x + max((end_x - start_x) / 2, 86)
            edge['path'] = (
                f"M {start_x} {start_y} "
                f"L {elbow_x} {start_y} "
                f"L {elbow_x} {end_y} "
                f"L {end_x} {end_y}"
            )
        else:
            start_x = source['x']
            start_y = source['y'] + source['height'] / 2
            end_x = target['x'] + target['width'] / 2
            end_y = target['y']
            elbow_x = start_x - max((start_x - end_x) / 2, 94)
            edge['path'] = (
                f"M {start_x} {start_y} "
                f"L {elbow_x} {start_y} "
                f"L {elbow_x} {end_y} "
                f"L {end_x} {end_y}"
            )

    return {
        'nodes': nodes,
        'edges': edges,
        'width': layout_width,
        'height': layout_height,
        'lanes': (
            [{'label': 'Ana Hat', 'x': revision_x + node_width / 2}]
            + [
                {'label': f'Dal {index + 1}', 'x': branch_start_x + index * branch_lane_gap + node_width / 2}
                for index in range(max_branch_depth)
            ]
        ),
    }


@transaction.atomic
def create_answer_revision(answer, *, content, created_by, source='author_edit', change_summary='', accepted_suggestion=None):
    current = answer.get_current_revision() or ensure_initial_revision(answer)
    if current.content == content:
        return current, False

    AnswerRevision.objects.filter(answer=answer, is_current=True).update(is_current=False)
    next_revision_no = (AnswerRevision.objects.filter(answer=answer).order_by('-revision_no').values_list('revision_no', flat=True).first() or 0) + 1
    revision = AnswerRevision.objects.create(
        answer=answer,
        parent_revision=current,
        base_revision=current,
        accepted_suggestion=accepted_suggestion,
        created_by=created_by,
        content=content,
        revision_no=next_revision_no,
        source=source,
        change_summary=change_summary or '',
        is_current=True,
    )
    answer.answer_text = content
    answer.save(update_fields=['answer_text', 'updated_at'])
    _create_revision_review_requests(revision)
    return revision, True


def create_answer_suggestion(answer, *, proposed_by, proposed_text, change_summary=''):
    base_revision = answer.get_current_revision() or ensure_initial_revision(answer)
    suggestion = AnswerSuggestion.objects.create(
        answer=answer,
        base_revision=base_revision,
        proposed_by=proposed_by,
        proposed_text=proposed_text,
        change_summary=change_summary or '',
    )
    if answer.user_id != proposed_by.id:
        Notification.create_answer_suggestion_notification(
            recipient=answer.user,
            sender=proposed_by,
            answer=answer,
        )
    return suggestion


@transaction.atomic
def accept_answer_suggestion(suggestion, *, reviewed_by, review_note=''):
    if suggestion.status != 'open':
        return None

    current = suggestion.answer.get_current_revision() or ensure_initial_revision(suggestion.answer)
    if current.id != suggestion.base_revision_id:
        suggestion.status = 'outdated'
        suggestion.reviewed_by = reviewed_by
        suggestion.reviewed_at = timezone.now()
        suggestion.review_note = review_note or 'Bu öneri, yeni bir sürüm yayınlandığı için eski kaldı.'
        suggestion.save(update_fields=['status', 'reviewed_by', 'reviewed_at', 'review_note', 'updated_at'])
        return None

    revision, created = create_answer_revision(
        suggestion.answer,
        content=suggestion.proposed_text,
        created_by=reviewed_by,
        source='suggestion_merge',
        change_summary=suggestion.change_summary or 'Düzeltme önerisi kabul edildi.',
        accepted_suggestion=suggestion,
    )
    if not created:
        suggestion.status = 'accepted'
        suggestion.reviewed_by = reviewed_by
        suggestion.reviewed_at = timezone.now()
        suggestion.review_note = review_note or 'Öneri kabul edildi; ancak içerik zaten güncel sürümle aynıydı.'
        suggestion.save(update_fields=['status', 'reviewed_by', 'reviewed_at', 'review_note', 'updated_at'])
        return current

    suggestion.status = 'accepted'
    suggestion.reviewed_by = reviewed_by
    suggestion.reviewed_at = timezone.now()
    suggestion.review_note = review_note or 'Öneri kabul edildi.'
    suggestion.save(update_fields=['status', 'reviewed_by', 'reviewed_at', 'review_note', 'updated_at'])
    if suggestion.proposed_by_id != reviewed_by.id:
        Notification.create_suggestion_result_notification(
            recipient=suggestion.proposed_by,
            sender=reviewed_by,
            answer=suggestion.answer,
            accepted=True,
        )
    return revision


def reject_answer_suggestion(suggestion, *, reviewed_by, review_note=''):
    if suggestion.status != 'open':
        return suggestion

    suggestion.status = 'rejected'
    suggestion.reviewed_by = reviewed_by
    suggestion.reviewed_at = timezone.now()
    suggestion.review_note = review_note or 'Öneri reddedildi.'
    suggestion.save(update_fields=['status', 'reviewed_by', 'reviewed_at', 'review_note', 'updated_at'])
    if suggestion.proposed_by_id != reviewed_by.id:
        Notification.create_suggestion_result_notification(
            recipient=suggestion.proposed_by,
            sender=reviewed_by,
            answer=suggestion.answer,
            accepted=False,
        )
    return suggestion


def approve_revision_review(revision, *, user, note=''):
    _ensure_revision_approval_snapshot(revision)
    approval = revision.approvals.select_related('revision__answer').filter(user=user).first()
    if not approval or approval.status != 'pending':
        return approval

    approval.status = 'approved'
    approval.note = note or 'Yeni sürüm onaylandı.'
    approval.responded_at = timezone.now()
    approval.save(update_fields=['status', 'note', 'responded_at'])
    return approval


def reject_revision_review(revision, *, user, note=''):
    _ensure_revision_approval_snapshot(revision)
    approval = revision.approvals.select_related('revision__answer').filter(user=user).first()
    if not approval or approval.status != 'pending':
        return approval

    approval.status = 'rejected'
    approval.note = note or 'Bu sürüm katkıcı tarafından onaylanmadı.'
    approval.responded_at = timezone.now()
    approval.save(update_fields=['status', 'note', 'responded_at'])
    return approval


def _prepare_diff_lines(text):
    content = (text or '').replace('\r\n', '\n').replace('\r', '\n')
    if not content:
        return ['']

    prepared = []
    for raw_line in content.split('\n'):
        if not raw_line:
            prepared.append('')
            continue

        if len(raw_line) <= 140:
            prepared.append(raw_line)
            continue

        wrapped = textwrap.wrap(
            raw_line,
            width=110,
            break_long_words=False,
            break_on_hyphens=False,
        )
        prepared.extend(wrapped or [raw_line])
    return prepared


def build_answer_diff_html(old_text, new_text):
    diff = HtmlDiff(tabsize=2, wrapcolumn=80)
    table = diff.make_table(
        _prepare_diff_lines(old_text),
        _prepare_diff_lines(new_text),
        fromdesc='Önceki',
        todesc='Yeni',
        context=True,
        numlines=1,
    )
    return mark_safe(table)


def _tokenize_for_inline_diff(text):
    return re.findall(r'\S+|\s+', text or '', flags=re.UNICODE)


def _render_inline_diff_tokens(tokens, token_class):
    rendered = []
    for token in tokens:
        escaped = escape(token).replace('\n', '<br>')
        if token.isspace():
            rendered.append(escaped.replace(' ', '&nbsp;'))
        else:
            rendered.append(f'<span class="{token_class}">{escaped}</span>')
    return ''.join(rendered)


def build_answer_inline_diff_html(old_text, new_text):
    old_tokens = _tokenize_for_inline_diff(old_text)
    new_tokens = _tokenize_for_inline_diff(new_text)
    matcher = SequenceMatcher(None, old_tokens, new_tokens)

    before_parts = []
    after_parts = []

    for opcode, i1, i2, j1, j2 in matcher.get_opcodes():
        old_chunk = old_tokens[i1:i2]
        new_chunk = new_tokens[j1:j2]
        if opcode == 'equal':
            before_parts.append(_render_inline_diff_tokens(old_chunk, 'inline-diff-context'))
            after_parts.append(_render_inline_diff_tokens(new_chunk, 'inline-diff-context'))
        elif opcode == 'delete':
            before_parts.append(_render_inline_diff_tokens(old_chunk, 'inline-diff-removed'))
        elif opcode == 'insert':
            after_parts.append(_render_inline_diff_tokens(new_chunk, 'inline-diff-added'))
        else:
            before_parts.append(_render_inline_diff_tokens(old_chunk, 'inline-diff-removed'))
            after_parts.append(_render_inline_diff_tokens(new_chunk, 'inline-diff-added'))

    return {
        'before_html': mark_safe(''.join(before_parts) or '<span class="inline-diff-context"></span>'),
        'after_html': mark_safe(''.join(after_parts) or '<span class="inline-diff-context"></span>'),
    }
