"""Shared, read-only date navigation for the three main content pages."""

import re
from datetime import date, datetime, time, timedelta

from django.core.paginator import Paginator
from django.db.models import Count, Exists, OuterRef, Q, Subquery
from django.utils import timezone

from .models import Answer, Question, UserProfile
from .querysets import get_active_left_frame_pin_q, get_today_questions_queryset


def day_answers(day):
    zone = timezone.get_default_timezone()
    start = timezone.make_aware(datetime.combine(day, time.min), zone)
    end = timezone.make_aware(datetime.combine(day + timedelta(days=1), time.min), zone)
    return Answer.objects.filter(created_at__gte=start, created_at__lt=end)


def day_questions(day):
    answers = day_answers(day)
    rows = answers.filter(question_id=OuterRef('pk'))
    counts = rows.order_by().values('question_id').annotate(total=Count('pk')).values('total')[:1]
    return Question.objects.filter(pk__in=answers.order_by().values('question_id')).annotate(
        first_day_entry=Subquery(rows.order_by('created_at', 'pk').values('created_at')[:1]),
        answers_count=Subquery(counts),
    ).order_by('first_day_entry', 'pk')


def left_frame_context(request, page_param):
    today = timezone.localdate(timezone=timezone.get_default_timezone())
    raw_day = request.GET.get('day', '')
    selected_day = None
    error = ''
    if raw_day:
        try:
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', raw_day):
                raise ValueError
            selected_day = date.fromisoformat(raw_day)
            if selected_day < date(1970, 1, 1) or selected_day > today:
                raise ValueError
        except ValueError:
            selected_day = None
            error = 'Geçerli bir geçmiş tarih veya bugün seçin.'

    followed = request.user.is_authenticated and request.GET.get('followed') == '1'
    if error:
        questions = Question.objects.none()
    elif selected_day:
        questions = day_questions(selected_day)
    else:
        questions = get_today_questions_queryset()

    if followed:
        followed_ids = UserProfile.objects.filter(followers__user=request.user).values('user_id')
        if selected_day:
            matching_answers = day_answers(selected_day).filter(
                question_id=OuterRef('pk'), user_id__in=followed_ids,
            )
            questions = questions.alias(has_followed_day_entry=Exists(matching_answers)).filter(
                Q(user_id__in=followed_ids) | Q(has_followed_day_entry=True),
            )
        else:
            questions = questions.filter(
                get_active_left_frame_pin_q() | Q(user_id__in=followed_ids)
                | Q(answers__user_id__in=followed_ids),
            ).distinct()

    page = Paginator(questions.select_related('user'), 20).get_page(request.GET.get(page_param))

    def link(**changes):
        query = request.GET.copy()
        query.pop(page_param, None)
        for key, value in changes.items():
            if value is None:
                query.pop(key, None)
            else:
                query[key] = str(value)
        return '?' + query.urlencode() if query else request.path

    nav_query = []
    if selected_day:
        nav_query.extend([f'day={selected_day.isoformat()}', f'q_page={page.number}'])
    if followed:
        nav_query.append('followed=1')

    return {
        'all_questions': page, 'all_questions_page': page,
        'show_followed_only': followed, 'left_page_param': page_param,
        'left_day': selected_day, 'left_day_active': bool(raw_day), 'left_day_error': error,
        'left_today': today, 'left_date_value': (selected_day or today).isoformat(),
        'left_current_url': link(day=None),
        'left_prev_day_url': link(day=selected_day - timedelta(days=1))
        if selected_day and selected_day > date(1970, 1, 1) else '',
        'left_next_day_url': link(day=selected_day + timedelta(days=1))
        if selected_day and selected_day < today else '',
        'left_nav_query': '&'.join(nav_query),
        'left_form_query': [(key, value) for key, value in request.GET.items()
                            if key not in {'day', page_param}],
    }
