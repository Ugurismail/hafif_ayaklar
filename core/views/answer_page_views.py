"""
Answer page/create/edit/delete views.
"""

from collections import defaultdict
from urllib.parse import unquote

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, F, Max, Q
from django.shortcuts import get_object_or_404, redirect, render

from ..answer_git import attach_answer_revision_metadata, create_answer_revision, ensure_initial_revision
from ..forms import AnswerForm
from ..models import (
    Answer,
    AnswerFollow,
    Kenarda,
    Question,
    QuestionFollow,
    QuestionRelationship,
    SavedItem,
    StartingQuestion,
    UserProfile,
    Vote,
)
from ..querysets import get_active_left_frame_pin_q, get_today_questions_queryset
from ..services import VoteSaveService
from ..utils import paginate_queryset


@login_required
def add_answer(request, slug):
    from django.db import transaction
    from ..models import Definition
    from ..utils import extract_mentions, send_mention_notifications

    question = get_object_or_404(Question, slug=slug)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                question = Question.objects.select_for_update().get(slug=slug)

                answer = form.save(commit=False)
                answer.question = question
                answer.user = request.user
                answer.save()

                definition_text = request.POST.get('definition_text', '').strip()
                if definition_text:
                    Definition.objects.create(
                        user=request.user,
                        question=question,
                        definition_text=definition_text,
                        answer=None
                    )

            mentioned_usernames = extract_mentions(answer.answer_text)
            if mentioned_usernames:
                send_mention_notifications(answer, mentioned_usernames)

            Kenarda.objects.filter(user=request.user, question=question, is_sent=False).delete()
            return redirect('single_answer', slug=question.slug, answer_id=answer.id)
    else:
        form = AnswerForm()

    return render(request, 'core/add_answer.html', {
        'form': form,
        'question': question
    })


@login_required
def edit_answer(request, answer_id):
    from ..utils import extract_mentions, send_mention_notifications

    all_questions = get_today_questions_queryset()
    answer = get_object_or_404(Answer, id=answer_id, user=request.user)
    user_child_ids = QuestionRelationship.objects.filter(
        user=request.user
    ).values_list('child_id', flat=True).distinct()
    starting_questions = StartingQuestion.objects.filter(
        user=request.user
    ).exclude(
        question_id__in=user_child_ids
    ).annotate(
        total_subquestions=Count('question__child_relationships', filter=Q(question__child_relationships__user=request.user)),
        latest_subquestion_date=Max('question__child_relationships__created_at', filter=Q(question__child_relationships__user=request.user))
    ).order_by(F('latest_subquestion_date').desc(nulls_last=True))

    draft_content = None
    draft_id = request.GET.get('draft_id')
    if draft_id:
        try:
            draft = Kenarda.objects.get(id=draft_id, user=request.user, answer=answer)
            draft_content = draft.content
        except Kenarda.DoesNotExist:
            pass

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            updated_text = form.cleaned_data['answer_text']
            updated_answer = answer
            revision, created = create_answer_revision(
                answer,
                content=updated_text,
                created_by=request.user,
                source='author_edit',
                change_summary='Yazar düzenlemesi',
            )
            if created:
                updated_answer = revision.answer

            mentioned_usernames = extract_mentions(updated_answer.answer_text)
            if mentioned_usernames:
                send_mention_notifications(updated_answer, mentioned_usernames)

            if draft_id:
                try:
                    draft = Kenarda.objects.get(id=draft_id, user=request.user, answer=answer)
                    draft.delete()
                except Kenarda.DoesNotExist:
                    pass

            messages.success(request, 'Yanıt başarıyla güncellendi.')
            return redirect('question_detail', slug=answer.question.slug)
    else:
        if draft_content:
            form = AnswerForm(initial={'answer_text': draft_content})
        else:
            form = AnswerForm(instance=answer)

    return render(request, 'core/edit_answer.html', {
        'form': form,
        'answer': answer,
        'all_questions': all_questions,
        'starting_questions': starting_questions,
        'draft_content': draft_content
    })


@login_required
def delete_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id, user=request.user)
    next_url = request.GET.get('next', '')

    if request.method == 'POST':
        question_slug = answer.question.slug
        answer.delete()
        if not Question.objects.filter(slug=question_slug).exists():
            return redirect('user_homepage')
        if next_url:
            return redirect(unquote(next_url))
        return redirect('user_homepage')
    else:
        if next_url:
            return redirect(unquote(next_url))
        return redirect('user_homepage')


def single_answer(request, slug, answer_id):
    question = get_object_or_404(Question.objects.select_related('user'), slug=slug)

    followed_param = request.GET.get('followed', '0')
    show_followed_only = followed_param == '1'

    all_questions_qs = get_today_questions_queryset()

    if show_followed_only and request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
            followed_user_ids = user_profile.following.values_list('user_id', flat=True)
            all_questions_qs = all_questions_qs.filter(
                get_active_left_frame_pin_q()
                | Q(user_id__in=followed_user_ids)
                | Q(answers__user_id__in=followed_user_ids)
            ).distinct()
        except UserProfile.DoesNotExist:
            all_questions_qs = Question.objects.none()

    all_questions_page = paginate_queryset(all_questions_qs, request, 'q_page', 20)

    all_answers = list(
        Answer.objects.filter(question=question).select_related('user', 'question', 'question__user')
    )
    attach_answer_revision_metadata(all_answers, current_user=request.user)
    focused_answer = next((answer for answer in all_answers if answer.id == answer_id), None)
    if focused_answer is None:
        focused_answer = get_object_or_404(
            Answer.objects.select_related('user', 'question', 'question__user'),
            id=answer_id,
            question=question,
        )
        attach_answer_revision_metadata([focused_answer], current_user=request.user)

    focused_current_revision = focused_answer.current_revision
    focused_recent_revisions = list(
        focused_answer.revisions.select_related('created_by', 'accepted_suggestion', 'accepted_suggestion__proposed_by')[:6]
    )
    focused_open_suggestions = list(
        focused_answer.git_suggestions.select_related('proposed_by', 'reviewed_by').filter(status='open')[:5]
    )
    focused_contributors = focused_answer.approved_contributors

    VoteSaveService.annotate_user_votes(all_answers, request.user, Answer)
    saved_answer_ids, answer_save_dict = VoteSaveService.get_save_info(all_answers, request.user, Answer)

    if request.method == "POST" and request.user.is_authenticated:
        form = AnswerForm(request.POST)
        if form.is_valid():
            new_answer = form.save(commit=False)
            new_answer.question = question
            new_answer.user = request.user
            new_answer.save()
            return redirect('single_answer', slug=question.slug, answer_id=new_answer.id)
    else:
        form = AnswerForm() if request.user.is_authenticated else None

    is_starting_question = StartingQuestion.objects.filter(question=question).exists()
    has_any_parent = QuestionRelationship.objects.filter(child=question).exists()
    is_on_map = is_starting_question or has_any_parent

    question_saved_ids, question_save_dict = VoteSaveService.get_save_info([question], request.user, Question)
    user_has_saved_question = question.id in question_saved_ids
    question_save_count = question_save_dict.get(question.id, 0)

    content_type_question = ContentType.objects.get_for_model(Question)
    if request.user.is_authenticated:
        question_vote = Vote.objects.filter(
            user=request.user,
            content_type=content_type_question,
            object_id=question.id
        ).first()
        question.user_vote_value = question_vote.value if question_vote else 0
    else:
        question.user_vote_value = 0

    user_is_following_question = False
    followed_answer_ids = []
    user_is_following_focused_answer = False
    if request.user.is_authenticated:
        user_is_following_question = QuestionFollow.objects.filter(
            user=request.user,
            question=question
        ).exists()

        followed_answer_ids = list(AnswerFollow.objects.filter(
            user=request.user,
            answer__in=all_answers
        ).values_list('answer_id', flat=True))

        user_is_following_focused_answer = focused_answer.id in followed_answer_ids

    subquestion_rels = QuestionRelationship.objects.filter(
        parent=question
    ).select_related('child', 'child__user', 'user').order_by('created_at')

    subquestions_map = defaultdict(list)
    for rel in subquestion_rels:
        subquestions_map[rel.child].append(rel.user)

    subquestions_list = [
        {'question': child, 'added_by_users': users}
        for child, users in subquestions_map.items()
    ]

    parent_rels = QuestionRelationship.objects.filter(
        child=question
    ).select_related('parent', 'parent__user', 'user').order_by('created_at')

    parents_map = defaultdict(list)
    for rel in parent_rels:
        parents_map[rel.parent].append(rel.user)

    parents_list = [
        {'question': parent, 'added_by_users': users}
        for parent, users in parents_map.items()
    ]

    draft_content = None
    if request.user.is_authenticated:
        draft_id = request.GET.get('draft_id')
        if draft_id:
            try:
                taslak = Kenarda.objects.get(pk=draft_id, user=request.user, question=question)
                draft_content = taslak.content
            except Kenarda.DoesNotExist:
                pass

    context = {
        'question': question,
        'focused_answer': focused_answer,
        'all_answers': all_answers,
        'saved_answer_ids': saved_answer_ids,
        'answer_save_dict': answer_save_dict,
        'form': form,
        'all_questions_page': all_questions_page,
        'show_followed_only': show_followed_only,
        'is_on_map': is_on_map,
        'user_has_saved_question': user_has_saved_question,
        'question_save_count': question_save_count,
        'user_is_following_question': user_is_following_question,
        'draft_content': draft_content,
        'followed_answer_ids': followed_answer_ids,
        'user_is_following_focused_answer': user_is_following_focused_answer,
        'subquestions_list': subquestions_list,
        'parents_list': parents_list,
        'focused_current_revision': focused_current_revision,
        'focused_recent_revisions': focused_recent_revisions,
        'focused_open_suggestions': focused_open_suggestions,
        'focused_contributors': focused_contributors,
        'focused_pending_contributors': focused_answer.pending_contributors,
        'focused_rejected_contributors': focused_answer.rejected_contributors,
    }
    return render(request, 'core/single_answer.html', context)
