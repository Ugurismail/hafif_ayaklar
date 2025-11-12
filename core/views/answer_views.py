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

from ..models import Question, Answer, SavedItem, Vote, StartingQuestion, UserProfile, QuestionFollow, AnswerFollow
from ..forms import AnswerForm
from ..querysets import get_today_questions_queryset
from ..utils import paginate_queryset
from ..services import VoteSaveService


@login_required
def get_user_answers(request):
    username = request.GET.get('username')
    q = request.GET.get('q', '').strip()
    user = get_object_or_404(User, username=username) if username else request.user

    answers = Answer.objects.filter(user=user).select_related('question')
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
            'detail_url': reverse('single_answer', args=[answer.question.slug, answer.id]),
            'question_url': reverse('question_detail', args=[answer.question.slug]),
            'created_at': answer.created_at.strftime("%d %b %Y %H:%M"),
        })
    return JsonResponse({'answers': data})


@login_required
def add_answer(request, slug):
    from django.db import transaction

    question = get_object_or_404(Question, slug=slug)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            # Atomic block ile race condition önleme
            with transaction.atomic():
                # select_for_update ile question'ı kilitle
                question = Question.objects.select_for_update().get(slug=slug)

                # Şimdi güvenli şekilde kontrol et
                is_first_answer = not question.answers.exists()

                answer = form.save(commit=False)
                answer.question = question
                answer.user = request.user
                answer.save()

                # Eğer tanım girilmişse ve bu ilk girdiyse, Definition oluştur
                definition_text = request.POST.get('definition_text', '').strip()
                if definition_text and is_first_answer:
                    from ..models import Definition
                    Definition.objects.create(
                        user=request.user,
                        question=question,
                        definition_text=definition_text,
                        answer=answer
                    )

            # Transaction dışında mention bildirimleri gönder (daha hızlı)
            from ..utils import extract_mentions, send_mention_notifications
            mentioned_usernames = extract_mentions(answer.answer_text)
            if mentioned_usernames:
                send_mention_notifications(answer, mentioned_usernames)

            # Taslak silme
            from ..models import Kenarda
            silinen = Kenarda.objects.filter(user=request.user, question=question, is_sent=False)
            deleted_count, _ = silinen.delete()
            return redirect('question_detail', slug=question.slug)
    else:
        form = AnswerForm()

    return render(request, 'core/add_answer.html', {
        'form': form,
        'question': question,
        'is_first_answer': is_first_answer
    })


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
            updated_answer = form.save()

            # Mention bildirimleri gönder
            from ..utils import extract_mentions, send_mention_notifications
            mentioned_usernames = extract_mentions(updated_answer.answer_text)
            if mentioned_usernames:
                send_mention_notifications(updated_answer, mentioned_usernames)

            messages.success(request, 'Yanıt başarıyla güncellendi.')
            return redirect('question_detail', slug=answer.question.slug)
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


def single_answer(request, slug, answer_id):
    # Public view - anyone can see single answer
    question = get_object_or_404(Question, slug=slug)
    focused_answer = get_object_or_404(Answer, id=answer_id, question=question)

    # Takip ettiklerim filtresi (sidebar için)
    followed_param = request.GET.get('followed', '0')
    show_followed_only = followed_param == '1'

    # Paginate questions using utility
    all_questions_qs = get_today_questions_queryset()

    # Takip ettiklerim filtresi uygulanırsa
    if show_followed_only and request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
            # UserProfile'dan User ID'lerini al
            followed_user_ids = user_profile.following.values_list('user_id', flat=True)
            all_questions_qs = all_questions_qs.filter(user_id__in=followed_user_ids)
        except UserProfile.DoesNotExist:
            all_questions_qs = Question.objects.none()

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
            return redirect('single_answer', slug=question.slug, answer_id=new_answer.id)
    else:
        form = AnswerForm() if request.user.is_authenticated else None

    # Check if question is on map
    starting_question_ids = set(StartingQuestion.objects.values_list('question_id', flat=True))
    is_on_map = (question.id in starting_question_ids) or question.parent_questions.exists()

    # Save count for question
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

    # Vote value for question
    if request.user.is_authenticated:
        question_vote = Vote.objects.filter(
            user=request.user,
            content_type=content_type_question,
            object_id=question.id
        ).first()
        question.user_vote_value = question_vote.value if question_vote else 0
    else:
        question.user_vote_value = 0

    # Takip bilgileri
    user_is_following_question = False
    followed_answer_ids = []
    user_is_following_focused_answer = False
    if request.user.is_authenticated:
        user_is_following_question = QuestionFollow.objects.filter(
            user=request.user,
            question=question
        ).exists()

        # Hangi yanıtları takip ediyor
        followed_answer_ids = list(AnswerFollow.objects.filter(
            user=request.user,
            answer__in=all_answers
        ).values_list('answer_id', flat=True))

        user_is_following_focused_answer = focused_answer.id in followed_answer_ids

    context = {
        'question': question,
        'focused_answer': focused_answer,
        'all_answers': all_answers,
        'saved_answer_ids': saved_answer_ids,
        'answer_save_dict': answer_save_dict,
        'form': form,  # Yanıt ekleme formu
        # 'all_questions': all_questions,
        'all_questions_page': all_questions_page,
        'show_followed_only': show_followed_only,
        'is_on_map': is_on_map,
        'user_has_saved_question': user_has_saved_question,
        'question_save_count': question_save_count,
        'user_is_following_question': user_is_following_question,
        'followed_answer_ids': followed_answer_ids,
        'user_is_following_focused_answer': user_is_following_focused_answer,
    }
    return render(request, 'core/single_answer.html', context)
