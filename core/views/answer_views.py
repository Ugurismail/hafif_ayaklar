"""
Answer-related views
- add_answer
- edit_answer
- delete_answer
- single_answer
- get_user_answers
"""

from urllib.parse import unquote

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Q, Count, Max, F
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from ..models import Question, Answer, SavedItem, Vote, StartingQuestion
from ..forms import AnswerForm
from ..querysets import get_today_questions_queryset
from ..utils import paginate_queryset
from ..services import VoteSaveService


@login_required
def get_user_answers(request):
    username = request.GET.get('username')
    q = request.GET.get('q', '').strip()
    user = get_object_or_404(User, username=username) if username else request.user

    answers = Answer.objects.filter(user=user)
    if q:
        answers = answers.filter(
            Q(answer_text__icontains=q) | Q(question__question_text__icontains=q)
        )
    data = []
    for answer in answers:
        data.append({
            'id': answer.id,
            'question_text': answer.question.question_text,
            'answer_text': answer.answer_text[:80] + '...' if len(answer.answer_text) > 80 else answer.answer_text,
            'detail_url': reverse('single_answer', args=[answer.question.id, answer.id]),
            'question_url': reverse('question_detail', args=[answer.question.id]),
            'created_at': answer.created_at.strftime("%d %b %Y %H:%M"),
        })
    return JsonResponse({'answers': data})


@login_required
def add_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.user = request.user
            answer.save()
            from ..models import Kenarda
            silinen = Kenarda.objects.filter(user=request.user, question=question, is_sent=False)
            deleted_count, _ = silinen.delete()
            return redirect('question_detail', question_id=question.id)
    else:
        form = AnswerForm()
    return render(request, 'core/add_answer.html', {'form': form, 'question': question})


@login_required
def edit_answer(request, answer_id):
    all_questions = get_today_questions_queryset()
    answer = get_object_or_404(Answer, id=answer_id, user=request.user)
        # Başlangıç sorularını al
    starting_questions = StartingQuestion.objects.filter(user=request.user).annotate(
        total_subquestions=Count('question__subquestions'),
        latest_subquestion_date=Max('question__subquestions__created_at')
    ).order_by(F('latest_subquestion_date').desc(nulls_last=True))

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Yanıt başarıyla güncellendi.')
            return redirect('question_detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)

    return render(request, 'core/edit_answer.html', {'form': form, 'answer': answer,'all_questions': all_questions,'starting_questions': starting_questions,})


@login_required
def delete_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id, user=request.user)
    next_url = request.GET.get('next', '')  # ?next=...

    if request.method == 'POST':
        answer.delete()
        if next_url:
            return redirect(unquote(next_url))
        else:
            # Varsayılan davranış (örneğin ana sayfa):
            return redirect('user_homepage')
    else:
        if next_url:
            return redirect(unquote(next_url))
        else:
            return redirect('user_homepage')


def single_answer(request, question_id, answer_id):
    # Public view - anyone can see single answer
    question = get_object_or_404(Question, id=question_id)
    focused_answer = get_object_or_404(Answer, id=answer_id, question=question)

    # Paginate questions using utility
    all_questions_qs = get_today_questions_queryset()
    all_questions_page = paginate_queryset(all_questions_qs, request, 'q_page', 20)

    # All answers for this question
    all_answers = list(Answer.objects.filter(question=question).select_related('user'))

    # Vote and Save data using VoteSaveService
    VoteSaveService.annotate_user_votes(all_answers, request.user, Answer)
    saved_answer_ids, answer_save_dict = VoteSaveService.get_save_info(all_answers, request.user, Answer)

    # Yanıt ekleme formu (only for authenticated users)
    if request.method == "POST" and request.user.is_authenticated:
        form = AnswerForm(request.POST)
        if form.is_valid():
            new_answer = form.save(commit=False)
            new_answer.question = question
            new_answer.user = request.user
            new_answer.save()
            return redirect('single_answer', question_id=question.id, answer_id=new_answer.id)
    else:
        form = AnswerForm() if request.user.is_authenticated else None

    context = {
        'question': question,
        'focused_answer': focused_answer,
        'all_answers': all_answers,
        'saved_answer_ids': saved_answer_ids,
        'answer_save_dict': answer_save_dict,
        'form': form,  # Yanıt ekleme formu
        # 'all_questions': all_questions,
        'all_questions_page': all_questions_page,
    }
    return render(request, 'core/single_answer.html', context)
