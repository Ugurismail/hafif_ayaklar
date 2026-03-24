"""
Core queryset utilities
Reusable queryset generators
"""

from datetime import timedelta
from django.db.models import Q, Count, Max, F, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce
from django.utils.timezone import now
from .models import Question


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

    queryset = Question.objects.annotate(
        answers_count=Count('answers', distinct=True),
        latest_answer_date=Max('answers__created_at')
    ).filter(
        Q(created_at__gte=seven_days_ago) | Q(answers__created_at__gte=seven_days_ago) | active_pin_q
    ).distinct()

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
