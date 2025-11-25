"""
Vote and save item views
- vote
- save_item
- get_saved_items
- pin_entry
- unpin_entry
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie

from ..models import Vote, SavedItem, PinnedEntry, Answer


@require_POST
@ensure_csrf_cookie
def vote(request):
    if request.method == 'POST':
        # Login kontrolü
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Oy verebilmek için üye olmalısınız.'}, status=403)

        content_type = request.POST.get('content_type')
        object_id = request.POST.get('object_id')
        value = request.POST.get('value')

        if not content_type or not object_id or not value:
            return JsonResponse({'error': 'Missing data'}, status=400)

        try:
            content_type_obj = ContentType.objects.get(model=content_type)
            model_class = content_type_obj.model_class()

            if model_class is None:
                return JsonResponse({'error': 'Invalid content type'}, status=400)

            # object_id'yi integer'a çevir
            try:
                object_id = int(object_id)
            except (ValueError, TypeError):
                return JsonResponse({'error': 'Invalid object_id format'}, status=400)

            obj = model_class.objects.get(id=object_id)
        except ContentType.DoesNotExist:
            return JsonResponse({'error': 'Invalid content_type'}, status=400)
        except Exception as e:
            # Model's DoesNotExist veya diğer hatalar
            return JsonResponse({'error': 'Object not found'}, status=404)

        # Vote value validation
        try:
            value = int(value)
            if value not in [1, -1]:
                return JsonResponse({'error': 'Invalid vote value'}, status=400)
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid vote value format'}, status=400)

        # Get or create the vote
        vote_obj, created = Vote.objects.get_or_create(
            user=request.user,
            content_type=content_type_obj,
            object_id=object_id,
            defaults={'value': value}
        )
        if not created:
            if vote_obj.value == value:
                # Remove the vote if it's the same
                vote_obj.delete()
                value = 0
            else:
                # Update the vote value
                vote_obj.value = value
                vote_obj.save()

        # Recalculate total upvotes and downvotes
        upvotes = Vote.objects.filter(content_type=content_type_obj, object_id=object_id, value=1).count()
        downvotes = Vote.objects.filter(content_type=content_type_obj, object_id=object_id, value=-1).count()

        # Update the object's vote counts
        obj.upvotes = upvotes
        obj.downvotes = downvotes
        obj.save()

        return JsonResponse({
            'upvotes': upvotes,
            'downvotes': downvotes,
            'user_vote_value': value
        })


@require_POST
@ensure_csrf_cookie
def save_item(request):
    if request.method == 'POST':
        # Login kontrolü
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Kaydetmek için üye olmalısınız.'}, status=403)

        content_type = request.POST.get('content_type')
        object_id = request.POST.get('object_id')

        if not content_type or not object_id:
            return JsonResponse({'error': 'Missing content_type or object_id'}, status=400)

        try:
            content_type_obj = ContentType.objects.get(model=content_type)
        except ContentType.DoesNotExist:
            return JsonResponse({'error': 'Invalid content_type'}, status=400)

        # Daha önce kaydedilmiş mi kontrol edin
        existing_item = SavedItem.objects.filter(
            user=request.user,
            content_type=content_type_obj,
            object_id=object_id
        ).first()

        if existing_item:
            # Eğer kaydedilmişse, kaydı silerek "kaydetmeyi kaldır" işlemi yapın
            existing_item.delete()
            # Kaydedilme sayısını alın
            save_count = SavedItem.objects.filter(
                content_type=content_type_obj,
                object_id=object_id
            ).count()
            return JsonResponse({'status': 'unsaved', 'save_count': save_count})
        else:
            # Yeni bir kayıt oluşturun
            saved_item = SavedItem.objects.create(
                user=request.user,
                content_type=content_type_obj,
                object_id=object_id
            )
            # Kaydedilme sayısını alın
            save_count = SavedItem.objects.filter(
                content_type=content_type_obj,
                object_id=object_id
            ).count()
            return JsonResponse({'status': 'saved', 'save_count': save_count})


@login_required
def get_saved_items(request):
    username = request.GET.get('username')
    q = request.GET.get('q', '').strip()
    user = get_object_or_404(User, username=username) if username else request.user

    saved_items = SavedItem.objects.filter(user=user)
    filtered_items = []
    for item in saved_items:
        instance = item.content_type.get_object_for_this_type(id=item.object_id)
        if item.content_type.model == 'question':
            text = instance.question_text
            matches = not q or q.lower() in text.lower()
        elif item.content_type.model == 'answer':
            text = instance.answer_text
            matches = (
                not q
                or q.lower() in text.lower()
                or q.lower() in instance.question.question_text.lower()
            )
        else:
            text = ''
            matches = False
        if matches:
            filtered_items.append({
                'type': item.content_type.model,
                'id': instance.id,
                'text': text[:80] + '...' if len(text) > 80 else text,
                'detail_url': reverse('question_detail', args=[instance.slug]) if item.content_type.model == 'question' else reverse('single_answer', args=[instance.question.slug, instance.id]),  # Use slug instead of id
            })
    return JsonResponse({'saved_items': filtered_items})


@login_required
def pin_entry(request, answer_id):
    if request.method == 'POST':
        user = request.user
        # Mevcut sabitlenmiş girdiyi kaldır
        PinnedEntry.objects.filter(user=user).delete()
        # Yeni girdiyi sabitle
        answer = get_object_or_404(Answer, id=answer_id)
        PinnedEntry.objects.create(user=user, answer=answer)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def unpin_entry(request):
    if request.method == 'POST':
        user = request.user
        PinnedEntry.objects.filter(user=user).delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))
