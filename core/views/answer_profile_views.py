"""
Answer profile/list helper views.
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse

from ..models import Answer, QuestionRelationship, StartingQuestion


def get_all_descendant_question_ids(root_question_id, user):
    descendant_ids = set()
    to_process = [root_question_id]

    while to_process:
        current_id = to_process.pop()
        descendant_ids.add(current_id)

        child_relationships = QuestionRelationship.objects.filter(
            parent_id=current_id,
            user=user
        ).values_list('child_id', flat=True)

        for child_id in child_relationships:
            if child_id not in descendant_ids:
                to_process.append(child_id)

    return list(descendant_ids)


@login_required
def get_user_answers(request):
    username = request.GET.get('username')
    q = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 50))
    root_question_id = request.GET.get('root_question_id', '').strip()

    user = get_object_or_404(User, username=username) if username else request.user

    answers = Answer.objects.filter(user=user).select_related('question').order_by('created_at')

    if root_question_id:
        try:
            root_id = int(root_question_id)
            question_ids = get_all_descendant_question_ids(root_id, user)
            answers = answers.filter(question_id__in=question_ids)
        except (ValueError, TypeError):
            pass

    if q:
        answers = answers.filter(
            Q(answer_text__icontains=q) | Q(question__question_text__icontains=q)
        )

    total = answers.count()
    start = (page - 1) * page_size
    end = start + page_size
    paginated_answers = answers[start:end]

    data = []
    for answer in paginated_answers:
        data.append({
            'id': answer.id,
            'question_text': answer.question.question_text,
            'answer_text': answer.answer_text[:80] + '...' if len(answer.answer_text) > 80 else answer.answer_text,
            'detail_url': reverse('single_answer', args=[answer.question.slug, answer.id]),
            'question_url': reverse('question_detail', args=[answer.question.slug]),
            'created_at': answer.created_at.strftime("%d %b %Y %H:%M"),
        })

    return JsonResponse({
        'answers': data,
        'total': total,
        'page': page,
        'page_size': page_size,
        'has_more': end < total
    })


@login_required
def get_root_questions(request):
    username = request.GET.get('username')
    user = get_object_or_404(User, username=username) if username else request.user

    answered_question_ids = Answer.objects.filter(user=user).values_list('question_id', flat=True).distinct()
    user_child_ids = QuestionRelationship.objects.filter(
        user=user
    ).values_list('child_id', flat=True).distinct()

    starting_questions = StartingQuestion.objects.filter(
        user=user,
        question_id__in=answered_question_ids
    ).exclude(
        question_id__in=user_child_ids
    ).select_related('question').order_by('question__question_text')

    data = {
        'root_questions': [
            {
                'id': sq.question.id,
                'question_text': sq.question.question_text,
            }
            for sq in starting_questions
        ]
    }

    return JsonResponse(data)
