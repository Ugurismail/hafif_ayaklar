"""
Message-related views
- message_list
- message_detail
- sent_messages
- view_message
- send_message_from_answer
- send_message_from_user
- check_new_messages
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.cache import cache_control

from ..models import Message, Answer
from ..forms import MessageForm
from ..querysets import get_today_questions_queryset


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def message_list(request):
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).select_related('sender', 'recipient')

    # En yeni mesajı her kullanıcı için birleştir
    # Sadece diğer kullanıcı id'lerini çek
    user_ids = set(messages.values_list('sender', flat=True)) | set(messages.values_list('recipient', flat=True))
    user_ids.discard(request.user.id)
    other_users = User.objects.filter(id__in=user_ids)

    conversation_list = []
    for other_user in other_users:
        messages_with_user = messages.filter(
            Q(sender=other_user, recipient=request.user) |
            Q(sender=request.user, recipient=other_user)
        ).order_by('-timestamp')

        unread_count = messages_with_user.filter(
            sender=other_user,
            recipient=request.user,
            is_read=False
        ).count()

        # En son mesajın zamanını al (sıralama için)
        last_message = messages_with_user.first()
        last_message_time = last_message.timestamp if last_message else None

        conversation_list.append({
            'user': other_user,
            'user_messages': messages_with_user,
            'unread_count': unread_count,
            'last_message_time': last_message_time,
        })

    # En son mesaja göre sırala (en yeni en üstte)
    conversation_list.sort(key=lambda x: x['last_message_time'] if x['last_message_time'] else timezone.datetime.min.replace(tzinfo=timezone.utc), reverse=True)

    # Pagination: 20 konuşma per page
    paginator = Paginator(conversation_list, 20)
    page_number = request.GET.get('message_page', 1)
    page_obj = paginator.get_page(page_number)

    all_questions = get_today_questions_queryset().annotate(
        answers_count=Count('answers')
    )

    # Get show_followed_only parameter for the filter icon
    show_followed_only = request.GET.get('followed', '0') == '1'

    context = {
        'page_obj': page_obj,
        'all_questions': all_questions,
        'show_followed_only': show_followed_only,
    }
    return render(request, 'core/message_list.html', context)


@login_required
def message_detail(request, username):
    from ..models import Notification

    other_user = get_object_or_404(User, username=username)
    Message.objects.filter(sender=other_user, recipient=request.user, is_read=False).update(is_read=True)

    # Mark message notifications from this user as read
    Notification.objects.filter(
        recipient=request.user,
        sender=other_user,
        is_read=False
    ).update(is_read=True)

    # Mesajları doğru şekilde sıralayın: en eski önce, en yeni sonra
    conversation_messages = Message.objects.filter(
        Q(sender=request.user, recipient=other_user) |
        Q(sender=other_user, recipient=request.user)
    ).order_by('timestamp')  # 'timestamp' alanına göre artan sırada

    if request.method == 'POST':
        body = request.POST.get('body', '').strip()

        # Boş mesaj kontrolü
        if not body:
            from django.contrib import messages as django_messages
            django_messages.error(request, 'Mesaj boş olamaz.')
            return redirect('message_detail', username=username)

        # Maksimum uzunluk kontrolü
        if len(body) > 5000:
            from django.contrib import messages as django_messages
            django_messages.error(request, 'Mesaj çok uzun (max 5000 karakter).')
            return redirect('message_detail', username=username)

        # Rate limiting: Son 1 dakikada kaç mesaj göndermiş?
        from datetime import timedelta
        recent_messages_count = Message.objects.filter(
            sender=request.user,
            timestamp__gte=timezone.now() - timedelta(minutes=1)
        ).count()

        if recent_messages_count >= 10:
            from django.contrib import messages as django_messages
            django_messages.error(request, 'Çok hızlı mesaj gönderiyorsunuz. Lütfen 1 dakika bekleyin.')
            return redirect('message_detail', username=username)

        Message.objects.create(
            sender=request.user,
            recipient=other_user,
            body=body,
            timestamp=timezone.now(),
            is_read=False
        )
        # Diğer kullanıcının mesajlarını okunmuş olarak işaretlemek isteğe bağlıdır
        Message.objects.filter(sender=other_user, recipient=request.user).update(is_read=True)
        return redirect('message_detail', username=username)
    all_questions = get_today_questions_queryset()

    # Get show_followed_only parameter for the filter icon
    show_followed_only = request.GET.get('followed', '0') == '1'

    context = {
        'other_user': other_user,
        'conversation_messages': conversation_messages,
        'all_questions': all_questions,
        'show_followed_only': show_followed_only,
    }
    return render(request, 'core/message_detail.html', context)


@login_required
def sent_messages(request):
    sent_messages_list = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'core/sent_messages.html', {'sent_messages_list': sent_messages_list})


@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.recipient != request.user and message.sender != request.user:
        return redirect('inbox')
    if message.recipient == request.user:
        message.is_read = True
        message.save()
    return render(request, 'core/view_message.html', {'message': message})


@login_required
def send_message_from_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    recipient = answer.user

    # İlgili yanıta ait path ve tam URL

    answer_url_path = reverse('single_answer', args=[answer.question.slug, answer.id])  # Use slug instead of id
    answer_full_url = request.build_absolute_uri(answer_url_path)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            # Sadece POST aşamasında, bir kere ekliyoruz:
            message.body = f"{answer_full_url} {message.body}"
            message.timestamp = timezone.now()
            message.is_read = False
            message.save()
            return redirect('message_detail', username=recipient.username)
    else:
        # GET aşamasında link eklemiyoruz, sadece boş bir form dönüyoruz.
        form = MessageForm(initial={'recipient': recipient})

    context = {
        'form': form,
        'recipient': recipient,
        'answer': answer,
    }
    return render(request, 'core/send_message_from_answer.html', context)


@login_required
def check_new_messages(request):
    # Kullanıcının okunmamış mesajlarını say
    unread_count = Message.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({'unread_count': unread_count})


@login_required
def send_message_from_user(request, user_id):
    recipient = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.save()
            return redirect('message_detail', username=recipient.username)
    else:
        form = MessageForm()

    context = {
        'form': form,
        'recipient': recipient,
    }
    return render(request, 'core/send_message_from_answer.html', context)
