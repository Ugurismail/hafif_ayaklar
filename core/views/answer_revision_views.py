"""
Answer revision/history/suggestion views.
"""

import json
from uuid import uuid4

from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    get_revision_approval_summary,
    get_revision_approval_summaries,
    reject_answer_suggestion,
    reject_revision_review,
    render_answer_content_html,
)
from ..forms import AnswerForm
from ..models import Answer, AnswerRevision, AnswerSuggestion


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
    suggestions = list(
        answer.git_suggestions.select_related(
            'proposed_by',
            'reviewed_by',
            'base_revision',
        )
    )
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
            'contributors': contributors,
            'current_approval_summary': current_approval_summary,
            'can_suggest': request.user.is_authenticated and request.user != answer.user,
            'can_review': request.user.is_authenticated and request.user == answer.user,
            'history_graph': build_answer_history_graph(answer, approval_summary_map=approval_summary_map),
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
        form = AnswerForm(request.POST)
        if form.is_valid():
            proposed_text = form.cleaned_data['answer_text']
            change_summary = (request.POST.get('change_summary') or '').strip()
            if proposed_text == current_revision.content:
                messages.error(request, 'Öneri boş kaldı; mevcut sürümle birebir aynı içerik gönderilemez.')
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
        form = AnswerForm(initial={'answer_text': current_revision.content})

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

    if len(content) > 50000:
        return JsonResponse({'status': 'fail', 'error': 'İçerik çok uzun (max 50000 karakter).'}, status=400)

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
        request=request,
    )
    return JsonResponse({'status': 'ok', 'html': html})


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
    current_revision = suggestion.answer.get_current_revision() or ensure_initial_revision(suggestion.answer)
    diff_html = build_answer_diff_html(suggestion.base_revision.content, suggestion.proposed_text)
    inline_diff = build_answer_inline_diff_html(suggestion.base_revision.content, suggestion.proposed_text)
    return render(
        request,
        'core/answer_suggestion_detail.html',
        {
            'suggestion': suggestion,
            'answer': suggestion.answer,
            'question': suggestion.answer.question,
            'current_revision': current_revision,
            'diff_html': diff_html,
            'inline_diff': inline_diff,
            'base_rendered_html': render_answer_content_html(suggestion.base_revision.content),
            'proposed_rendered_html': render_answer_content_html(suggestion.proposed_text),
            'current_rendered_html': render_answer_content_html(current_revision.content),
            'can_review': request.user.is_authenticated and request.user == suggestion.answer.user,
            'is_outdated': suggestion.is_outdated_against_current(),
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

    reject_answer_suggestion(
        suggestion,
        reviewed_by=request.user,
        review_note=(request.POST.get('review_note') or '').strip(),
    )
    messages.info(request, 'Düzeltme önerisi reddedildi.')
    return redirect('answer_suggestion_detail', suggestion_id=suggestion.id)
