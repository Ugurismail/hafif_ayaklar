"""
Core queryset utilities
Reusable queryset generators
"""

from datetime import timedelta
from django.db.models import (
    Q,
    Count,
    F,
    Case,
    When,
    Value,
    IntegerField,
    DateTimeField,
    Exists,
    OuterRef,
    Subquery,
)
from django.db.models.functions import Coalesce
from django.utils.timezone import now
from .models import Answer, Question


def get_active_left_frame_pin_q(reference_time=None):
    current_time = reference_time or now()
    return Q(left_frame_pinned=True) & (
        Q(left_frame_pin_until__isnull=True) | Q(left_frame_pin_until__gte=current_time)
    )


def get_today_questions_queryset():
    """
    Returns questions created or answered in the last 7 days
    Sorted by latest activity (answer date or creation date)

    Returns:
        QuerySet of Question objects annotated with:
        - answers_count: Number of answers
        - latest_answer_date: Date of most recent answer
        - sort_date: Latest activity date (answer or creation)
        Ordered by sort_date descending
    """
    seven_days_ago = now() - timedelta(days=7)

    current_time = now()
    active_pin_q = get_active_left_frame_pin_q(current_time)

    answer_rows = Answer.objects.filter(question_id=OuterRef('pk'))
    answer_counts = (
        answer_rows.order_by()
        .values('question_id')
        .annotate(total=Count('id'))
        .values('total')[:1]
    )
    latest_answer_dates = answer_rows.order_by('-created_at').values('created_at')[:1]
    recent_answers = answer_rows.filter(created_at__gte=seven_days_ago)

    # Correlated subqueries avoid multiplying every question by all of its
    # answers before pagination. That join became the dominant homepage query
    # as the answer table grew.
    queryset = Question.objects.annotate(
        has_recent_answer=Exists(recent_answers),
        answers_count=Coalesce(
            Subquery(answer_counts, output_field=IntegerField()),
            Value(0),
        ),
        latest_answer_date=Subquery(
            latest_answer_dates,
            output_field=DateTimeField(),
        ),
    ).filter(
        Q(created_at__gte=seven_days_ago) | Q(has_recent_answer=True) | active_pin_q
    )

    queryset = queryset.annotate(
        sort_date=Coalesce('latest_answer_date', 'created_at'),
        left_frame_pin_active=Case(
            When(active_pin_q, then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        ),
    ).order_by(
        F('left_frame_pin_active').desc(),
        'left_frame_pin_order',
        F('sort_date').desc()
    )

    return queryset
