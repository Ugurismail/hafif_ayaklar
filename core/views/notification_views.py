"""
Notification views for the application
Handles notification list, marking as read, and follow/unfollow functionality
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q

from ..models import Notification, QuestionFollow, AnswerFollow, Question, Answer
from ..utils import paginate_queryset


@login_required
def notification_list(request):
    """
    Display list of notifications for the logged-in user
    """
    # Get all notifications for the current user
    notifications = Notification.objects.filter(
        recipient=request.user
    ).select_related('sender', 'related_question', 'related_answer')

    # Filter by type if specified
    notification_type = request.GET.get('type', '')
    if notification_type:
        notifications = notifications.filter(notification_type=notification_type)

    # Filter by read/unread status
    status = request.GET.get('status', '')
    if status == 'unread':
        notifications = notifications.filter(is_read=False)
    elif status == 'read':
        notifications = notifications.filter(is_read=True)

    # Paginate
    notifications_page = paginate_queryset(notifications, request, 'page', 20)

    # Get unread count
    unread_count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()

    context = {
        'notifications': notifications_page,
        'unread_count': unread_count,
        'current_type': notification_type,
        'current_status': status,
    }
    return render(request, 'core/notifications.html', context)


@login_required
@require_POST
def mark_notification_read(request, notification_id):
    """
    Mark a single notification as read
    """
    notification = get_object_or_404(
        Notification,
        id=notification_id,
        recipient=request.user
    )
    notification.mark_as_read()

    return JsonResponse({'success': True})


@login_required
@require_POST
def mark_all_notifications_read(request):
    """
    Mark all notifications as read for the current user
    """
    updated = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).update(is_read=True)

    return JsonResponse({'success': True, 'count': updated})


@login_required
def get_unread_notification_count(request):
    """
    AJAX endpoint to get unread notification count
    """
    count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()

    return JsonResponse({'count': count})


@login_required
@require_POST
def follow_question(request, question_id):
    """
    Follow a question
    """
    question = get_object_or_404(Question, id=question_id)

    # Create follow relationship if it doesn't exist
    follow, created = QuestionFollow.objects.get_or_create(
        user=request.user,
        question=question
    )

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'created': created,
            'message': 'Başlık takip ediliyor' if created else 'Zaten takip ediyorsunuz'
        })

    return redirect('question_detail', question_id=question_id)


@login_required
@require_POST
def unfollow_question(request, question_id):
    """
    Unfollow a question
    """
    question = get_object_or_404(Question, id=question_id)

    # Delete follow relationship
    deleted_count, _ = QuestionFollow.objects.filter(
        user=request.user,
        question=question
    ).delete()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'deleted': deleted_count > 0,
            'message': 'Başlık takipten çıkarıldı' if deleted_count > 0 else 'Zaten takip etmiyorsunuz'
        })

    return redirect('question_detail', question_id=question_id)


@login_required
@require_POST
def follow_answer(request, answer_id):
    """
    Follow an answer
    """
    answer = get_object_or_404(Answer, id=answer_id)

    # Create follow relationship if it doesn't exist
    follow, created = AnswerFollow.objects.get_or_create(
        user=request.user,
        answer=answer
    )

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'created': created,
            'message': 'Yanıt takip ediliyor' if created else 'Zaten takip ediyorsunuz'
        })

    return redirect('question_detail', question_id=answer.question.id)


@login_required
@require_POST
def unfollow_answer(request, answer_id):
    """
    Unfollow an answer
    """
    answer = get_object_or_404(Answer, id=answer_id)

    # Delete follow relationship
    deleted_count, _ = AnswerFollow.objects.filter(
        user=request.user,
        answer=answer
    ).delete()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'deleted': deleted_count > 0,
            'message': 'Yanıt takipten çıkarıldı' if deleted_count > 0 else 'Zaten takip etmiyorsunuz'
        })

    return redirect('question_detail', question_id=answer.question.id)
