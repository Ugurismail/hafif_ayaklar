"""Site/home related views."""

import random
import re
from collections import Counter
from datetime import timedelta
from itertools import chain

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import DatabaseError
from django.db.models import Q, Count, Max, F
from django.db.models.functions import TruncWeek, TruncMonth
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.utils.timezone import now

from ..answer_git import attach_answer_revision_metadata
from ..middleware import LastSeenMiddleware
from ..models import Answer, DailyVisitor, Question, QuestionRelationship, Reference, StartingQuestion, UserProfile, Vote
from ..querysets import get_active_left_frame_pin_q, get_today_questions_queryset
from ..services import VoteSaveService
from ..utils import build_reference_usage_counts, paginate_queryset

WORD_PATTERN = re.compile(r'\b\w+\b', re.UNICODE)


def get_today_questions_page(request, per_page=25):
    """Helper for paginating today's questions."""
    queryset = get_today_questions_queryset()
    return paginate_queryset(queryset, request, 'page', per_page)


def memur_exam(request):
    return render(request, 'core/memur_exam.html')


def user_homepage(request):
    followed_param = request.GET.get('followed', '0')
    show_followed_only = followed_param == '1'

    all_questions_qs = get_today_questions_queryset().select_related('user')

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

    all_questions = paginate_queryset(all_questions_qs, request, 'page', 20)

    random_items = list(
        Answer.objects.select_related('question', 'user', 'user__userprofile').order_by('?')[:20]
    )
    attach_answer_revision_metadata(random_items, current_user=request.user)

    if request.user.is_authenticated:
        user_child_ids = QuestionRelationship.objects.filter(user=request.user).values_list('child_id', flat=True).distinct()
        starting_questions_qs = (
            StartingQuestion.objects.filter(user=request.user)
            .exclude(question_id__in=user_child_ids)
            .select_related('question')
            .annotate(
                total_subquestions=Count(
                    'question__child_relationships',
                    filter=Q(question__child_relationships__user=request.user),
                ),
                latest_subquestion_date=Max(
                    'question__child_relationships__created_at',
                    filter=Q(question__child_relationships__user=request.user),
                ),
            )
            .order_by(F('latest_subquestion_date').desc(nulls_last=True))
            .select_related('question__user')
        )
        starting_questions = paginate_queryset(starting_questions_qs, request, 'starting_page', 10)
    else:
        starting_questions = None

    if random_items:
        VoteSaveService.annotate_user_votes(random_items, request.user, Answer)
        saved_answer_ids, answer_save_dict = VoteSaveService.get_save_info(random_items, request.user, Answer)
    else:
        saved_answer_ids = set()
        answer_save_dict = {}

    context = {
        'random_items': random_items,
        'saved_answer_ids': saved_answer_ids,
        'answer_save_dict': answer_save_dict,
        'all_questions': all_questions,
        'starting_questions': starting_questions,
        'show_followed_only': show_followed_only,
    }
    return render(request, 'core/user_homepage.html', context)


@login_required
def site_statistics(request):
    today = now().date()
    active_tab = request.GET.get('tab', 'word-analysis')

    if LastSeenMiddleware._should_track_unique_visitor(request):
        visitor_hash = LastSeenMiddleware._build_daily_visitor_hash(request, today)
        if visitor_hash:
            try:
                DailyVisitor.objects.get_or_create(date=today, visitor_hash=visitor_hash)
            except DatabaseError:
                pass

    today_unique_visitors = DailyVisitor.objects.filter(date=today).count()

    visitor_range_options = [
        ('7d', 'Son 7 Gün'),
        ('30d', 'Son 30 Gün'),
        ('90d', 'Son 90 Gün'),
        ('365d', 'Son 365 Gün'),
        ('all', 'Tüm Zamanlar'),
    ]
    visitor_group_options = [
        ('day', 'Günlük'),
        ('week', 'Haftalık'),
        ('month', 'Aylık'),
    ]

    visitor_range_days = {
        '7d': 7,
        '30d': 30,
        '90d': 90,
        '365d': 365,
        'all': None,
    }

    selected_visitor_range = request.GET.get('visitor_range', '30d')
    if selected_visitor_range not in visitor_range_days:
        selected_visitor_range = '30d'

    selected_visitor_group = request.GET.get('visitor_group', 'day')
    if selected_visitor_group not in {'day', 'week', 'month'}:
        selected_visitor_group = 'day'

    visitor_qs = DailyVisitor.objects.all()
    selected_days = visitor_range_days[selected_visitor_range]
    if selected_days:
        start_date = today - timedelta(days=selected_days - 1)
        visitor_qs = visitor_qs.filter(date__gte=start_date)

    visitor_labels = []
    visitor_values = []
    if selected_visitor_group == 'day':
        visitor_rows = visitor_qs.values('date').annotate(unique_visitors=Count('visitor_hash')).order_by('date')
        for row in visitor_rows:
            visitor_labels.append(row['date'].strftime('%d.%m.%Y'))
            visitor_values.append(row['unique_visitors'])
    elif selected_visitor_group == 'week':
        visitor_rows = visitor_qs.annotate(period=TruncWeek('date')).values('period').annotate(
            unique_visitors=Count('visitor_hash')
        ).order_by('period')
        for row in visitor_rows:
            period = row['period']
            period_date = period.date() if hasattr(period, 'date') else period
            iso = period_date.isocalendar()
            visitor_labels.append(f"{iso.year}-W{iso.week:02d}")
            visitor_values.append(row['unique_visitors'])
    else:
        visitor_rows = visitor_qs.annotate(period=TruncMonth('date')).values('period').annotate(
            unique_visitors=Count('visitor_hash')
        ).order_by('period')
        for row in visitor_rows:
            period = row['period']
            period_date = period.date() if hasattr(period, 'date') else period
            visitor_labels.append(period_date.strftime('%Y-%m'))
            visitor_values.append(row['unique_visitors'])

    visitor_chart_data = {
        'labels': visitor_labels,
        'values': visitor_values,
    }
    visitor_total_unique = sum(visitor_values)
    visitor_peak_unique = max(visitor_values) if visitor_values else 0

    user_count = User.objects.filter(Q(questions__isnull=False) | Q(answers__isnull=False)).distinct().count()
    total_questions = Question.objects.count()
    total_answers = Answer.objects.count()
    total_likes = Vote.objects.filter(value=1).count()
    total_dislikes = Vote.objects.filter(value=-1).count()

    top_question_users = User.objects.annotate(question_count=Count('questions')).order_by('-question_count')[:5]
    top_answer_users = User.objects.annotate(answer_count=Count('answers')).order_by('-answer_count')[:5]
    top_liked_questions = Question.objects.annotate(like_count=F('upvotes')).order_by('-like_count')[:5]
    top_liked_answers = Answer.objects.annotate(like_count=F('upvotes')).order_by('-like_count')[:5]
    top_saved_questions = Question.objects.annotate(save_count=Count('saveditem')).order_by('-save_count')[:5]
    top_saved_answers = Answer.objects.annotate(save_count=Count('saveditem')).order_by('-save_count')[:5]

    question_texts = list(Question.objects.values_list('question_text', flat=True))
    answer_texts = list(Answer.objects.values_list('answer_text', flat=True))

    all_texts = []
    word_counts = Counter()
    total_words = 0
    total_characters = 0

    for text in chain(question_texts, answer_texts):
        all_texts.append(text)
        if not text:
            continue
        total_characters += len(text)
        words = WORD_PATTERN.findall(text.lower())
        total_words += len(words)
        word_counts.update(words)

    reference_usage_counts = build_reference_usage_counts(answer_texts=answer_texts, use_cache=False)

    exclude_words_input = request.GET.get('exclude_words', '')
    if exclude_words_input:
        exclude_words_list = re.split(r',\s*', exclude_words_input.strip())
        exclude_words = set(word.lower() for word in exclude_words_list if word.strip())
    else:
        exclude_words = set()

    filtered_word_counts = Counter({word: count for word, count in word_counts.items() if word not in exclude_words})
    top_words = filtered_word_counts.most_common(10)

    search_word = request.GET.get('search_word', '').strip().lower()
    search_word_count = None
    if search_word:
        if search_word in exclude_words:
            search_word_count = 0
        else:
            search_word_count = word_counts.get(search_word, 0)

    all_references = list(Reference.objects.all())
    for ref in all_references:
        ref.usage_count = reference_usage_counts.get(ref.id, 0)

    all_references.sort(key=lambda ref: (ref.usage_count, ref.id), reverse=True)
    top_references = paginate_queryset(all_references, request, 'reference_page', 20)

    total_entries = len(all_texts)
    avg_words_per_entry = round(total_words / total_entries, 2) if total_entries else 0
    avg_chars_per_entry = round(total_characters / total_entries, 2) if total_entries else 0
    avg_entries_per_user = round(total_entries / user_count, 2) if user_count else 0
    total_references_count = Reference.objects.count()

    context = {
        'active_tab': active_tab,
        'today_unique_visitors': today_unique_visitors,
        'visitor_range_options': visitor_range_options,
        'visitor_group_options': visitor_group_options,
        'selected_visitor_range': selected_visitor_range,
        'selected_visitor_group': selected_visitor_group,
        'visitor_chart_data': visitor_chart_data,
        'visitor_total_unique': visitor_total_unique,
        'visitor_peak_unique': visitor_peak_unique,
        'visitor_data_points': len(visitor_values),
        'user_count': user_count,
        'total_questions': total_questions,
        'total_answers': total_answers,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'total_references_count': total_references_count,
        'top_question_users': top_question_users,
        'top_answer_users': top_answer_users,
        'top_liked_questions': top_liked_questions,
        'top_liked_answers': top_liked_answers,
        'top_saved_questions': top_saved_questions,
        'top_saved_answers': top_saved_answers,
        'top_words': top_words,
        'search_word_count': search_word_count,
        'search_word': search_word,
        'exclude_words': ', '.join(sorted(exclude_words)),
        'exclude_words_input': exclude_words_input,
        'top_references': top_references,
        'total_words': total_words,
        'total_characters': total_characters,
        'avg_words_per_entry': avg_words_per_entry,
        'avg_chars_per_entry': avg_chars_per_entry,
        'avg_entries_per_user': avg_entries_per_user,
    }
    return render(request, 'core/site_statistics.html', context)


def about(request):
    return render(request, 'core/about.html')


@require_POST
def random_question_id(request):
    ids = list(Question.objects.values_list('id', flat=True))
    if not ids:
        return JsonResponse({'question_id': None})
    random_id = random.choice(ids)
    return JsonResponse({'question_id': random_id})


def shuffle_questions(request):
    all_ids = list(Question.objects.values_list('id', flat=True))
    if not all_ids:
        return JsonResponse({'questions': []})
    sample_size = min(20, len(all_ids))
    selected_ids = random.sample(all_ids, sample_size)
    questions = (
        Question.objects.filter(id__in=selected_ids)
        .annotate(answers_count=Count('answers'))
        .values('id', 'slug', 'question_text', 'answers_count')
    )
    questions = list(questions)
    random.shuffle(questions)
    return JsonResponse({
        'questions': [
            {'id': q['id'], 'slug': q['slug'], 'text': q['question_text'], 'answers_count': q['answers_count']}
            for q in questions
        ]
    })
