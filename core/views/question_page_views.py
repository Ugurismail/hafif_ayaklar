"""
Question page/create/delete views.
"""

import re
from collections import defaultdict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q, Count
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from ..answer_git import attach_answer_revision_metadata
from ..forms import AnswerForm, QuestionForm, StartingQuestionForm
from ..models import (
    Answer,
    AnswerFollow,
    Definition,
    Kenarda,
    Question,
    QuestionFollow,
    QuestionRelationship,
    HashtagUsage,
    SavedItem,
    StartingQuestion,
    UserProfile,
    Vote,
)
from ..querysets import get_active_left_frame_pin_q, get_today_questions_queryset

UNICODE_ESCAPE_RE = re.compile(r'\\u([0-9a-fA-F]{4})')
HEX_ESCAPE_RE = re.compile(r'\\x([0-9a-fA-F]{2})')


def _decode_legacy_js_escapes(value: str) -> str:
    if not isinstance(value, str) or '\\' not in value:
        return value
    value = UNICODE_ESCAPE_RE.sub(lambda m: chr(int(m.group(1), 16)), value)
    value = HEX_ESCAPE_RE.sub(lambda m: chr(int(m.group(1), 16)), value)
    return value


def _redirect_back_with_writer_warning(request):
    messages.warning(request, "Bu başlığı açmak için yazar olmalısınız.")
    referer = request.META.get("HTTP_REFERER", "")
    if referer and url_has_allowed_host_and_scheme(
        referer,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(referer)
    return redirect("user_homepage")


def _normalize_answer_text(value: str) -> str:
    if not isinstance(value, str):
        return ""
    return value.replace("\r\n", "\n").replace("\r", "\n")


def question_detail(request, slug):
    followed_param = request.GET.get('followed', '0')
    show_followed_only = followed_param == '1'

    all_questions = get_today_questions_queryset()

    if show_followed_only and request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
            followed_user_ids = user_profile.following.values_list('user_id', flat=True)
            all_questions = all_questions.filter(
                get_active_left_frame_pin_q()
                | Q(user_id__in=followed_user_ids)
                | Q(answers__user_id__in=followed_user_ids)
            ).distinct()
        except UserProfile.DoesNotExist:
            all_questions = Question.objects.none()

    q_page_number = request.GET.get('q_page', 1)
    q_paginator = Paginator(all_questions, 20)
    all_questions_page = q_paginator.get_page(q_page_number)

    question = get_object_or_404(Question.objects.select_related('user'), slug=slug)

    my_answers = request.GET.get('my_answers')
    followed = request.GET.get('followed')
    username = request.GET.get('username', '').strip()
    keyword = request.GET.get('keyword', '').strip()

    all_answers = question.answers.select_related(
        'user',
        'user__userprofile'
    ).order_by('created_at')

    if my_answers == 'on':
        all_answers = all_answers.filter(user=request.user)
    if followed == 'on':
        followed_users = request.user.userprofile.following.all()
        all_answers = all_answers.filter(user__in=followed_users)
    if username:
        all_answers = all_answers.filter(user__username__iexact=username)
    if keyword:
        all_answers = all_answers.filter(answer_text__icontains=keyword)

    a_page_number = request.GET.get('a_page', 1)
    a_paginator = Paginator(all_answers, 10)
    answers_page = a_paginator.get_page(a_page_number)
    answers_page.object_list = attach_answer_revision_metadata(list(answers_page.object_list), current_user=request.user)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            new_answer = form.save(commit=False)
            new_answer.user = request.user
            new_answer.question = question
            new_answer.save()
            Kenarda.objects.filter(user=request.user, question=question, is_sent=False).delete()
            return redirect('single_answer', slug=question.slug, answer_id=new_answer.id)
    else:
        form = AnswerForm()

    content_type_question = ContentType.objects.get_for_model(Question)
    if request.user.is_authenticated:
        user_has_saved_question = SavedItem.objects.filter(
            user=request.user,
            content_type=content_type_question,
            object_id=question.id
        ).exists()
    else:
        user_has_saved_question = False
    question_save_count = SavedItem.objects.filter(
        content_type=content_type_question,
        object_id=question.id
    ).count()

    content_type_answer = ContentType.objects.get_for_model(Answer)
    page_answer_ids = [ans.id for ans in answers_page]

    if request.user.is_authenticated:
        user_votes = Vote.objects.filter(
            user=request.user,
            content_type=content_type_answer,
            object_id__in=page_answer_ids
        ).values('object_id', 'value')
        user_vote_dict = {vote['object_id']: vote['value'] for vote in user_votes}
        for ans in answers_page:
            ans.user_vote_value = user_vote_dict.get(ans.id, 0)
        saved_answer_ids = SavedItem.objects.filter(
            user=request.user,
            content_type=content_type_answer,
            object_id__in=page_answer_ids
        ).values_list('object_id', flat=True)
    else:
        for ans in answers_page:
            ans.user_vote_value = 0
        saved_answer_ids = []
    answer_save_counts = SavedItem.objects.filter(
        content_type=content_type_answer,
        object_id__in=page_answer_ids
    ).values('object_id').annotate(count=Count('id'))
    answer_save_dict = {item['object_id']: item['count'] for item in answer_save_counts}

    if request.user.is_authenticated:
        has_parent = QuestionRelationship.objects.filter(
            child=question,
            user=request.user
        ).exists()
    else:
        has_parent = False
    is_starting_question = StartingQuestion.objects.filter(question=question).exists()
    is_on_map = is_starting_question or has_parent

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

    question_tag_ids = list(
        question.hashtags.values_list('hashtag_id', flat=True)
    )
    related_questions = []
    if question_tag_ids:
        related_rows = list(
            HashtagUsage.objects.filter(
                hashtag_id__in=question_tag_ids,
                question__isnull=False,
            )
            .exclude(question=question)
            .values('question_id')
            .annotate(shared_count=Count('hashtag_id', distinct=True))
            .order_by('-shared_count', '-question_id')[:5]
        )
        related_question_map = {
            item.id: item
            for item in Question.objects.filter(
                id__in=[row['question_id'] for row in related_rows]
            ).select_related('user')
        }
        related_questions = [
            {
                'question': related_question_map[row['question_id']],
                'shared_count': row['shared_count'],
            }
            for row in related_rows
            if row['question_id'] in related_question_map
        ]

    user_is_following_question = False
    followed_answer_ids = []
    if request.user.is_authenticated:
        user_is_following_question = QuestionFollow.objects.filter(
            user=request.user,
            question=question
        ).exists()

        followed_answer_ids = list(AnswerFollow.objects.filter(
            user=request.user,
            answer__in=answers_page
        ).values_list('answer_id', flat=True))

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
        'form': form,
        'all_questions_page': all_questions_page,
        'answers_page': answers_page,
        'user_has_saved_question': user_has_saved_question,
        'question_save_count': question_save_count,
        'saved_answer_ids': list(saved_answer_ids),
        'answer_save_dict': answer_save_dict,
        'my_answers': my_answers,
        'followed': followed,
        'filter_username': username,
        'filter_keyword': keyword,
        'is_on_map': is_on_map,
        'show_followed_only': show_followed_only,
        'user_is_following_question': user_is_following_question,
        'followed_answer_ids': followed_answer_ids,
        'subquestions_list': subquestions_list,
        'parents_list': parents_list,
        'related_questions': related_questions,
        'draft_content': draft_content,
    }
    return render(request, 'core/question_detail.html', context)


@login_required
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data['question_text']
            question, created = Question.objects.get_or_create(
                question_text=question_text,
                defaults={'user': request.user}
            )
            question.users.add(request.user)
            question.save()
            StartingQuestion.objects.create(user=request.user, question=question)

            definition_text = request.POST.get('definition_text', '').strip()
            answer_text = _normalize_answer_text(form.cleaned_data.get('answer_text', ''))

            answer = Answer.objects.create(
                question=question,
                user=request.user,
                answer_text=answer_text
            )

            if definition_text:
                Definition.objects.create(
                    user=request.user,
                    question=question,
                    definition_text=definition_text,
                    answer=answer
                )

            return redirect('user_homepage')
    else:
        form = QuestionForm()

    user_definitions = Definition.objects.filter(user=request.user).select_related('question').order_by('-created_at')[:10]

    return render(request, 'core/add_question.html', {
        'form': form,
        'user_definitions': user_definitions,
    })


@login_required
def add_subquestion(request, slug):
    parent_question = get_object_or_404(Question, slug=slug)
    all_questions = get_today_questions_queryset()
    draft_title = None
    draft_content = None

    draft_id = request.GET.get('draft_id')
    if draft_id:
        try:
            taslak = Kenarda.objects.get(
                pk=draft_id,
                user=request.user,
                question=parent_question,
                answer__isnull=True,
                is_sent=False,
                draft_source='subquestion',
            )
            draft_title = taslak.title
            draft_content = taslak.content
        except Kenarda.DoesNotExist:
            pass

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            subquestion_text = form.cleaned_data['question_text']
            answer_text = form.cleaned_data.get('answer_text', '')
            definition_text = request.POST.get('definition_text', '')

            subquestion, created = Question.objects.get_or_create(
                question_text=subquestion_text,
                defaults={'user': request.user}
            )
            subquestion.users.add(request.user)
            QuestionRelationship.objects.get_or_create(
                parent=parent_question,
                child=subquestion,
                user=request.user
            )

            answer = Answer.objects.create(
                question=subquestion,
                user=request.user,
                answer_text=answer_text
            )

            if definition_text:
                Definition.objects.create(
                    user=request.user,
                    question=subquestion,
                    definition_text=definition_text,
                    answer=answer
                )

            messages.success(request, 'Alt soru başarıyla eklendi.')
            return redirect('question_detail', slug=subquestion.slug)
    else:
        form = QuestionForm(initial={
            'question_text': draft_title or '',
            'answer_text': draft_content or '',
        })

    user_definitions = Definition.objects.filter(user=request.user).select_related('question').order_by('-created_at')[:10]

    context = {
        'form': form,
        'parent_question': parent_question,
        'all_questions': all_questions,
        'user_definitions': user_definitions,
        'draft_title': draft_title,
        'draft_content': draft_content,
    }
    return render(request, 'core/add_subquestion.html', context)


@login_required
def delete_question(request, slug):
    question = get_object_or_404(Question, slug=slug)

    if request.method == 'POST':
        if request.user == question.user:
            with transaction.atomic():
                Answer.objects.filter(question=question, user=request.user).delete()
                question.users.remove(request.user)
                if question.users.count() == 0:
                    delete_question_and_subquestions(question)
                    messages.success(request, 'Soru ve alt soruları başarıyla silindi.')
                else:
                    messages.success(request, 'Soru sizin için silindi.')
            return redirect('user_homepage')
        else:
            messages.error(request, 'Bu soruyu silme yetkiniz yok.')
            return redirect('question_detail', slug=question.slug)
    else:
        return render(request, 'core/confirm_delete_question.html', {'question': question})


def delete_question_and_subquestions(question):
    subquestions = question.subquestions.all()
    for sub in subquestions:
        delete_question_and_subquestions(sub)
    question.delete()


def add_question_from_search(request):
    all_questions = get_today_questions_queryset()
    query = _decode_legacy_js_escapes(request.GET.get('q', '').strip())

    if not request.user.is_authenticated:
        return _redirect_back_with_writer_warning(request)

    draft_content = None
    draft_id = request.GET.get('draft_id')
    if draft_id:
        try:
            taslak = Kenarda.objects.get(pk=draft_id, user=request.user)
            draft_content = taslak.content
            if not query and taslak.title:
                query = _decode_legacy_js_escapes(taslak.title)
        except Kenarda.DoesNotExist:
            pass

    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            question, created = Question.objects.get_or_create(
                question_text=query,
                defaults={'user': request.user, 'from_search': True}
            )
            question.users.add(request.user)

            definition_text = request.POST.get('definition_text', '').strip()
            answer_text = _normalize_answer_text(answer_form.cleaned_data.get('answer_text', ''))

            answer = answer_form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.answer_text = answer_text
            answer.save()

            if definition_text:
                Definition.objects.create(
                    user=request.user,
                    question=question,
                    definition_text=definition_text,
                    answer=answer
                )

            return redirect('single_answer', slug=question.slug, answer_id=answer.id)
    else:
        answer_form = AnswerForm()

    user_definitions = Definition.objects.filter(user=request.user).select_related('question').order_by('-created_at')[:10]

    return render(request, 'core/add_question_from_search.html', {
        'query': query,
        'answer_form': answer_form,
        'all_questions': all_questions,
        'user_definitions': user_definitions,
        'draft_content': draft_content,
    })


def bkz_view(request, query):
    question = Question.objects.filter(question_text__iexact=query).first()
    if question:
        return redirect('question_detail', slug=question.slug)
    else:
        if not request.user.is_authenticated:
            return _redirect_back_with_writer_warning(request)
        from urllib.parse import urlencode
        return redirect(f'{reverse("add_question_from_search")}?{urlencode({"q": query})}')


@login_required
def add_starting_question(request):
    all_questions = get_today_questions_queryset()
    if request.method == 'POST':
        form = StartingQuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data['question_text']
            question, created = Question.objects.get_or_create(
                question_text=question_text,
                defaults={'user': request.user}
            )
            question.users.add(request.user)
            question.save()
            StartingQuestion.objects.create(user=request.user, question=question)

            definition_text = request.POST.get('definition_text', '').strip()
            answer_text = _normalize_answer_text(form.cleaned_data['answer_text'])

            Answer.objects.create(
                question=question,
                user=request.user,
                answer_text=answer_text
            )

            if definition_text:
                Definition.objects.create(
                    user=request.user,
                    question=question,
                    definition_text=definition_text,
                    answer=None
                )

            return redirect('question_detail', slug=question.slug)
    else:
        form = StartingQuestionForm()

    user_definitions = Definition.objects.filter(user=request.user).select_related('question').order_by('-created_at')[:10]

    draft_title = None
    draft_content = None
    draft_id = request.GET.get('draft_id')
    if draft_id:
        try:
            taslak = Kenarda.objects.get(pk=draft_id, user=request.user)
            draft_title = taslak.title
            draft_content = taslak.content
        except Kenarda.DoesNotExist:
            pass

    return render(request, 'core/add_starting_question.html', {
        'form': form,
        'all_questions': all_questions,
        'user_definitions': user_definitions,
        'draft_title': draft_title,
        'draft_content': draft_content,
    })
