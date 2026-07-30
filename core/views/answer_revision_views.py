"""
Answer revision/history/suggestion views.
"""

import json
from uuid import uuid4

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Q, Subquery
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from ..answer_git import (
    accept_answer_suggestion,
    approve_revision_review,
    build_answer_diff_html,
    build_answer_history_graph,
    build_answer_inline_diff_html,
    create_answer_suggestion,
    ensure_initial_revision,
    get_answer_diff_stats,
    get_revision_approval_summary,
    get_revision_approval_summaries,
    reject_answer_suggestion,
    reject_revision_review,
    render_answer_content_html,
)
from ..content_limits import EDITOR_CONTENT_MAX_LENGTH
from ..forms import AnswerSuggestionForm
from ..models import Answer, AnswerRevision, AnswerSuggestion, Notification
from ..utils import paginate_queryset


def _can_access_suggestion(user, suggestion):
    if not user.is_authenticated:
        return False
    return bool(
        user.is_superuser
        or user.id == suggestion.answer.user_id
        or user.id == suggestion.proposed_by_id
    )


def _mark_suggestion_notifications_read(user, suggestion):
    updated = Notification.objects.filter(
        recipient=user,
        related_suggestion=suggestion,
        is_read=False,
    ).update(is_read=True)
    if updated:
        return

    if user.id == suggestion.answer.user_id:
        notification_type = 'answer_suggestion'
        sender_id = suggestion.proposed_by_id
    elif user.id == suggestion.proposed_by_id:
        notification_type = 'suggestion_result'
        sender_id = suggestion.answer.user_id
    else:
        return

    legacy_notification = Notification.objects.filter(
        recipient=user,
        sender_id=sender_id,
        related_answer_id=suggestion.answer_id,
        notification_type=notification_type,
        is_read=False,
    ).order_by('-created_at').first()
    if legacy_notification:
        legacy_notification.mark_as_read()


def _decorate_suggestion(suggestion, perspective):
    if hasattr(suggestion, 'current_revision_id'):
        suggestion.is_stale = bool(
            suggestion.status == 'open'
            and suggestion.current_revision_id
            and suggestion.current_revision_id != suggestion.base_revision_id
        )
    else:
        suggestion.is_stale = suggestion.is_outdated_against_current()
    suggestion.diff_stats = get_answer_diff_stats(
        suggestion.base_revision.content,
        suggestion.proposed_text,
    )
    if suggestion.is_stale:
        suggestion.display_status = 'Yanıt değişti'
        suggestion.status_tone = 'stale'
    elif suggestion.status == 'open':
        suggestion.display_status = (
            'Kararınızı bekliyor'
            if perspective == 'incoming'
            else 'Yanıt bekleniyor'
        )
        suggestion.status_tone = 'pending'
    elif suggestion.status == 'accepted':
        suggestion.display_status = 'Kabul edildi'
        suggestion.status_tone = 'accepted'
    elif suggestion.status == 'rejected':
        suggestion.display_status = 'Reddedildi'
        suggestion.status_tone = 'rejected'
    else:
        suggestion.display_status = 'Güncelliğini yitirdi'
        suggestion.status_tone = 'stale'
    return suggestion


@login_required
def correction_inbox(request):
    perspective = request.GET.get('view', 'incoming')
    if perspective not in {'incoming', 'outgoing'}:
        perspective = 'incoming'

    status_filter = request.GET.get('status', 'pending')
    if status_filter not in {'pending', 'resolved', 'all'}:
        status_filter = 'pending'

    search_query = (request.GET.get('q') or '').strip()
    incoming_base = AnswerSuggestion.objects.filter(answer__user=request.user)
    outgoing_base = AnswerSuggestion.objects.filter(proposed_by=request.user)
    suggestions = incoming_base if perspective == 'incoming' else outgoing_base

    if status_filter == 'pending':
        suggestions = suggestions.filter(status='open')
    elif status_filter == 'resolved':
        suggestions = suggestions.exclude(status='open')

    if search_query:
        search_filter = (
            Q(answer__question__question_text__icontains=search_query)
            | Q(change_summary__icontains=search_query)
        )
        if perspective == 'incoming':
            search_filter |= Q(proposed_by__username__icontains=search_query)
        else:
            search_filter |= Q(answer__user__username__icontains=search_query)
        suggestions = suggestions.filter(search_filter)

    current_revision_ids = AnswerRevision.objects.filter(
        answer_id=OuterRef('answer_id'),
        is_current=True,
    ).values('id')[:1]
    suggestions = (
        suggestions
        .select_related(
            'answer',
            'answer__question',
            'answer__user',
            'base_revision',
            'proposed_by',
            'reviewed_by',
        )
        .annotate(current_revision_id=Subquery(current_revision_ids))
        .order_by('-created_at')
    )
    suggestions_page = paginate_queryset(
        suggestions,
        request,
        page_param='page',
        per_page=12,
    )
    for suggestion in suggestions_page.object_list:
        _decorate_suggestion(suggestion, perspective)

    notification_types = (
        ['answer_suggestion']
        if perspective == 'incoming'
        else ['suggestion_result']
    )
    Notification.objects.filter(
        recipient=request.user,
        notification_type__in=notification_types,
        is_read=False,
    ).update(is_read=True)

    return render(
        request,
        'core/correction_inbox.html',
        {
            'suggestions': suggestions_page,
            'perspective': perspective,
            'status_filter': status_filter,
            'search_query': search_query,
            'incoming_pending_count': incoming_base.filter(status='open').count(),
            'outgoing_pending_count': outgoing_base.filter(status='open').count(),
        },
    )


def answer_git_history(request, answer_id):
    answer = get_object_or_404(
        Answer.objects.select_related('question', 'user'),
        id=answer_id,
    )
    current_revision = answer.get_current_revision() or ensure_initial_revision(answer)
    revisions = list(
        answer.revisions.select_related(
            'created_by',
            'accepted_suggestion',
            'accepted_suggestion__proposed_by',
        )
    )
    approval_summary_map = get_revision_approval_summaries(revisions, current_user=request.user)
    suggestions_query = answer.git_suggestions.select_related(
        'proposed_by',
        'reviewed_by',
        'base_revision',
    )
    if request.user.is_authenticated and (
        request.user == answer.user or request.user.is_superuser
    ):
        pass
    elif request.user.is_authenticated:
        suggestions_query = suggestions_query.filter(proposed_by=request.user)
    else:
        suggestions_query = suggestions_query.none()
    suggestions = list(suggestions_query)
    for index, revision in enumerate(revisions):
        revision.previous_revision = revisions[index + 1] if index + 1 < len(revisions) else None
        revision.rendered_html = render_answer_content_html(revision.content)
        revision.previous_rendered_html = (
            render_answer_content_html(revision.previous_revision.content)
            if revision.previous_revision else ''
        )
        revision.diff_html = build_answer_diff_html(
            revision.previous_revision.content if revision.previous_revision else '',
            revision.content,
        )
        revision.inline_diff = build_answer_inline_diff_html(
            revision.previous_revision.content if revision.previous_revision else '',
            revision.content,
        )
        revision.approval_summary = approval_summary_map.get(revision.id) or get_revision_approval_summary(revision, current_user=request.user)
        revision.current_user_can_review = bool(
            revision.is_current
            and revision.approval_summary['current_user_approval']
            and revision.approval_summary['current_user_approval'].status == 'pending'
        )

    current_approval_summary = get_revision_approval_summary(current_revision, current_user=request.user)
    contributors = current_approval_summary['approved_users']

    return render(
        request,
        'core/answer_git_history.html',
        {
            'answer': answer,
            'question': answer.question,
            'current_revision': current_revision,
            'revisions': revisions,
            'suggestions': suggestions,
            'visible_open_suggestion_count': sum(
                suggestion.status == 'open'
                for suggestion in suggestions
            ),
            'contributors': contributors,
            'current_approval_summary': current_approval_summary,
            'can_suggest': request.user.is_authenticated and request.user != answer.user,
            'can_review': request.user.is_authenticated and (
                request.user == answer.user or request.user.is_superuser
            ),
            'history_graph': build_answer_history_graph(
                answer,
                approval_summary_map=approval_summary_map,
                suggestions=suggestions,
            ),
        },
    )


@login_required
def answer_suggest_edit(request, answer_id):
    answer = get_object_or_404(Answer.objects.select_related('question', 'user'), id=answer_id)
    if request.user == answer.user:
        messages.info(request, 'Kendi yanıtınız için doğrudan düzenleme ekranını kullanın.')
        return redirect('edit_answer', answer_id=answer.id)

    current_revision = answer.get_current_revision() or ensure_initial_revision(answer)
    if request.method == 'POST':
        form = AnswerSuggestionForm(request.POST)
        if form.is_valid():
            proposed_text = form.cleaned_data['answer_text']
            change_summary = form.cleaned_data['change_summary'].strip()
            if proposed_text == current_revision.content:
                form.add_error(
                    'answer_text',
                    'Metinde bir değişiklik yapmadan öneri gönderemezsiniz.',
                )
            else:
                suggestion = create_answer_suggestion(
                    answer,
                    proposed_by=request.user,
                    proposed_text=proposed_text,
                    change_summary=change_summary,
                )
                messages.success(request, 'Düzeltme önerisi gönderildi.')
                return redirect('answer_suggestion_detail', suggestion_id=suggestion.id)
    else:
        form = AnswerSuggestionForm(
            initial={'answer_text': current_revision.content},
        )

    return render(
        request,
        'core/answer_suggestion_form.html',
        {
            'answer': answer,
            'question': answer.question,
            'base_revision': current_revision,
            'base_rendered_html': render_answer_content_html(current_revision.content),
            'form': form,
        },
    )


@login_required
@require_POST
def answer_live_preview(request):
    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'status': 'fail', 'error': 'Geçersiz JSON formatı.'}, status=400)

    content = data.get('content') or ''
    question_text = (data.get('question_text') or '').strip()
    question_slug = (data.get('question_slug') or '').strip()

    if len(content) > EDITOR_CONTENT_MAX_LENGTH:
        return JsonResponse(
            {
                'status': 'fail',
                'error': f'İçerik çok uzun (max {EDITOR_CONTENT_MAX_LENGTH} karakter).',
            },
            status=400,
        )

    html = render_to_string(
        'core/_answer_preview_card.html',
        {
            'preview_text': content,
            'preview_user': request.user,
            'preview_created_at': None,
            'preview_question_text': question_text,
            'preview_question_slug': question_slug or None,
            'preview_key': f'live-{uuid4().hex}',
            'preview_header': 'Canlı önizleme',
            'preview_badge': 'Önizleme',
            'preview_show_meta': False,
        },
    )
    return JsonResponse({'status': 'ok', 'html': html})


@login_required
def answer_suggestion_detail(request, suggestion_id):
    suggestion = get_object_or_404(
        AnswerSuggestion.objects.select_related(
            'answer',
            'answer__question',
            'answer__user',
            'base_revision',
            'proposed_by',
            'reviewed_by',
        ),
        id=suggestion_id,
    )
    if not _can_access_suggestion(request.user, suggestion):
        return HttpResponseForbidden('Bu düzeltme önerisini görüntüleyemezsiniz.')

    _mark_suggestion_notifications_read(request.user, suggestion)
    current_revision = suggestion.answer.get_current_revision() or ensure_initial_revision(suggestion.answer)
    perspective = (
        'incoming'
        if request.user.id == suggestion.answer.user_id
        else 'outgoing'
    )
    _decorate_suggestion(suggestion, perspective)
    return render(
        request,
        'core/answer_suggestion_detail.html',
        {
            'suggestion': suggestion,
            'answer': suggestion.answer,
            'question': suggestion.answer.question,
            'current_revision': current_revision,
            'inline_diff': build_answer_inline_diff_html(
                suggestion.base_revision.content,
                suggestion.proposed_text,
            ),
            'base_rendered_html': render_answer_content_html(suggestion.base_revision.content),
            'proposed_rendered_html': render_answer_content_html(suggestion.proposed_text),
            'can_review': request.user == suggestion.answer.user or request.user.is_superuser,
            'is_outdated': suggestion.is_stale,
            'perspective': perspective,
        },
    )


@login_required
@require_POST
def answer_revision_approve(request, revision_id):
    revision = get_object_or_404(
        AnswerRevision.objects.select_related('answer', 'answer__question', 'answer__user'),
        id=revision_id,
    )
    if not revision.is_current:
        messages.warning(request, 'Yalnız güncel sürüm için onay verebilirsiniz.')
        return redirect('answer_git_history', answer_id=revision.answer_id)

    approval = revision.approvals.filter(user=request.user).first()
    if not approval or approval.status != 'pending':
        return HttpResponseForbidden('Bu sürüm için bekleyen bir onay görevin yok.')

    approve_revision_review(
        revision,
        user=request.user,
        note=(request.POST.get('review_note') or '').strip(),
    )
    messages.success(request, 'Yeni sürümü onayladın. Adın katkı verenler arasında kalacak.')
    return redirect('answer_git_history', answer_id=revision.answer_id)


@login_required
@require_POST
def answer_revision_reject(request, revision_id):
    revision = get_object_or_404(
        AnswerRevision.objects.select_related('answer', 'answer__question', 'answer__user'),
        id=revision_id,
    )
    if not revision.is_current:
        messages.warning(request, 'Yalnız güncel sürüm için yanıt verebilirsiniz.')
        return redirect('answer_git_history', answer_id=revision.answer_id)

    approval = revision.approvals.filter(user=request.user).first()
    if not approval or approval.status != 'pending':
        return HttpResponseForbidden('Bu sürüm için bekleyen bir onay görevin yok.')

    reject_revision_review(
        revision,
        user=request.user,
        note=(request.POST.get('review_note') or '').strip(),
    )
    messages.info(request, 'Bu sürümü onaylamadın. Adın onaylamayan katkıcılar arasında görünecek.')
    return redirect('answer_git_history', answer_id=revision.answer_id)


@login_required
@require_POST
def answer_suggestion_accept(request, suggestion_id):
    suggestion = get_object_or_404(AnswerSuggestion.objects.select_related('answer', 'answer__user'), id=suggestion_id)
    if request.user != suggestion.answer.user and not request.user.is_superuser:
        return HttpResponseForbidden('Bu öneriyi yalnız yanıt sahibi kabul edebilir.')
    if suggestion.status != 'open':
        messages.info(request, 'Bu düzeltme önerisi daha önce sonuçlandırılmış.')
        return redirect('answer_suggestion_detail', suggestion_id=suggestion.id)

    revision = accept_answer_suggestion(
        suggestion,
        reviewed_by=request.user,
        review_note=(request.POST.get('review_note') or '').strip(),
    )
    if revision is None:
        messages.warning(request, 'Öneri eski kaldı; bu sırada yanıtın yeni bir sürümü yayınlanmış.')
    else:
        messages.success(request, 'Düzeltme önerisi kabul edildi ve yeni sürüm yayınlandı.')
    return redirect('answer_suggestion_detail', suggestion_id=suggestion.id)


@login_required
@require_POST
def answer_suggestion_reject(request, suggestion_id):
    suggestion = get_object_or_404(AnswerSuggestion.objects.select_related('answer', 'answer__user'), id=suggestion_id)
    if request.user != suggestion.answer.user and not request.user.is_superuser:
        return HttpResponseForbidden('Bu öneriyi yalnız yanıt sahibi reddedebilir.')
    if suggestion.status != 'open':
        messages.info(request, 'Bu düzeltme önerisi daha önce sonuçlandırılmış.')
        return redirect('answer_suggestion_detail', suggestion_id=suggestion.id)

    reject_answer_suggestion(
        suggestion,
        reviewed_by=request.user,
        review_note=(request.POST.get('review_note') or '').strip(),
    )
    messages.info(request, 'Düzeltme önerisi reddedildi.')
    return redirect('answer_suggestion_detail', suggestion_id=suggestion.id)
