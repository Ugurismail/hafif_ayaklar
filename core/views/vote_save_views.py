"""
Vote and save item views
- vote
- save_item
- get_saved_items
- pin_entry
- unpin_entry
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_POST

from ..content_targets import owned_collections, public_content_target
from ..models import Vote, SavedCollection, SavedCollectionItem, SavedItem, PinnedEntry, Answer, Question, Notification


@require_POST
def vote(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Oy verebilmek için üye olmalısınız.'}, status=403)

    try:
        model, content_type, object_id = public_content_target(
            request.POST.get('content_type'), request.POST.get('object_id'),
        )
        value = int(request.POST.get('value'))
        if value not in (1, -1):
            raise ValueError('Invalid vote value')
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid vote target or value'}, status=400)

    with transaction.atomic():
        # All voters lock the same content row before reading or changing votes.
        obj = get_object_or_404(model.objects.select_for_update(), pk=object_id)
        vote_obj, created = Vote.objects.get_or_create(
            user=request.user, content_type=content_type, object_id=object_id,
            defaults={'value': value},
        )
        if not created:
            if vote_obj.value == value:
                vote_obj.delete()
                value = 0
            else:
                vote_obj.value = value
                vote_obj.save(update_fields=['value'])

        totals = Vote.objects.filter(content_type=content_type, object_id=object_id).aggregate(
            upvotes=Count('pk', filter=Q(value=1)),
            downvotes=Count('pk', filter=Q(value=-1)),
        )
        # Do not overwrite entry edits or advance the content's edit timestamp.
        model.objects.filter(pk=object_id).update(**totals)

    try:
        if model is Answer and value and obj.user_id != request.user.id:
            Notification.create_answer_vote_notification(
                recipient=obj.user, sender=request.user, answer=obj, value=value,
            )
    except Exception:
        pass

    return JsonResponse({**totals, 'user_vote_value': value})


@require_POST
def save_item(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Kaydetmek için üye olmalısınız.'}, status=403)

    action = request.POST.get('action', '').strip()
    raw_ids = request.POST.getlist('collection_ids[]') or request.POST.getlist('collection_ids')
    new_name = request.POST.get('new_collection_name', '').strip()
    try:
        model, content_type, object_id = public_content_target(
            request.POST.get('content_type'), request.POST.get('object_id'),
        )
        if action not in ('', 'save', 'unsave') or len(new_name) > 80:
            raise ValueError('Invalid save action or collection name')
        selected_collections = owned_collections(request.user, raw_ids)
    except ValueError as exc:
        return JsonResponse({'error': str(exc)}, status=400)

    manage_collections = action == 'save' or bool(raw_ids) or bool(new_name)
    created_now = False
    with transaction.atomic():
        obj = get_object_or_404(model.objects.select_for_update(), pk=object_id)
        existing_item = SavedItem.objects.select_for_update().filter(
            user=request.user, content_type=content_type, object_id=object_id,
        ).first()
        if action == 'unsave' or (existing_item and not manage_collections):
            if existing_item:
                existing_item.delete()
            result = {'status': 'unsaved'}
        else:
            saved_item = existing_item
            if saved_item is None:
                saved_item = SavedItem.objects.create(
                    user=request.user, content_type=content_type, object_id=object_id,
                )
                created_now = True

            if new_name:
                collection, _ = SavedCollection.objects.get_or_create(
                    user=request.user, name=new_name, defaults={'description': ''},
                )
                if collection.pk not in {item.pk for item in selected_collections}:
                    selected_collections.append(collection)
            selected_ids = {collection.pk for collection in selected_collections}
            SavedCollectionItem.objects.filter(saved_item=saved_item).exclude(
                collection_id__in=selected_ids,
            ).delete()
            for collection in selected_collections:
                SavedCollectionItem.objects.get_or_create(collection=collection, saved_item=saved_item)
            result = {
                'status': 'saved',
                'saved_item_id': saved_item.pk,
                'collections': [
                    {'id': collection.pk, 'name': collection.name}
                    for collection in selected_collections
                ],
            }
        result['save_count'] = SavedItem.objects.filter(
            content_type=content_type, object_id=object_id,
        ).count()

    try:
        if created_now and model is Answer and obj.user_id != request.user.id:
            Notification.create_answer_save_notification(
                recipient=obj.user, sender=request.user, answer=obj,
            )
    except Exception:
        pass
    return JsonResponse(result)


@login_required
@require_GET
@never_cache
def get_saved_items(request):
    username = request.GET.get('username')
    if username and username != request.user.username:
        return JsonResponse({'error': 'Kaydedilenler yalnızca sahibine açıktır.'}, status=403)
    q = request.GET.get('q', '').strip().lower()
    question_ct = ContentType.objects.get_for_model(Question)
    answer_ct = ContentType.objects.get_for_model(Answer)
    saved_items = list(SavedItem.objects.filter(
        user=request.user, content_type__in=[question_ct, answer_ct],
    ))
    questions = Question.objects.in_bulk([
        item.object_id for item in saved_items if item.content_type_id == question_ct.pk
    ])
    answers = Answer.objects.select_related('question').in_bulk([
        item.object_id for item in saved_items if item.content_type_id == answer_ct.pk
    ])

    filtered_items = []
    for item in saved_items:
        is_question = item.content_type_id == question_ct.pk
        instance = (questions if is_question else answers).get(item.object_id)
        if instance is None:
            continue
        text = instance.question_text if is_question else instance.answer_text
        search_text = text if is_question else text + '\n' + instance.question.question_text
        if q and q not in search_text.lower():
            continue
        filtered_items.append({
            'type': 'question' if is_question else 'answer',
            'id': instance.pk,
            'text': text[:80] + '...' if len(text) > 80 else text,
            'detail_url': (
                reverse('question_detail', args=[instance.slug]) if is_question
                else reverse('single_answer', args=[instance.question.slug, instance.pk])
            ),
        })
    return JsonResponse({'saved_items': filtered_items})


@login_required
def pin_entry(request, answer_id):
    if request.method == 'POST':
        user = request.user
        answer = get_object_or_404(Answer, id=answer_id)
        if answer.user_id != user.id:
            messages.error(request, 'Sadece kendi girdini profiline sabitleyebilirsin.')
            return redirect(request.META.get('HTTP_REFERER', 'user_homepage'))
        # Mevcut sabitlenmiş girdiyi kaldır
        PinnedEntry.objects.filter(user=user).delete()
        # Yeni girdiyi sabitle
        PinnedEntry.objects.create(user=user, answer=answer)
    return redirect(request.META.get('HTTP_REFERER', 'user_homepage'))


@login_required
def unpin_entry(request):
    if request.method == 'POST':
        user = request.user
        PinnedEntry.objects.filter(user=user).delete()
    return redirect(request.META.get('HTTP_REFERER', 'user_homepage'))
