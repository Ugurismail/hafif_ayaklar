from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from ..models import Answer, Question, SavedCollection, SavedCollectionItem, SavedItem


def _serialize_collections(user):
    collections = (
        SavedCollection.objects.filter(user=user)
        .annotate(item_count=Count('items'))
        .order_by('name', 'id')
    )
    return [
        {
            'id': collection.id,
            'name': collection.name,
            'description': collection.description,
            'item_count': collection.item_count,
        }
        for collection in collections
    ]


def saved_item_collection_options(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Kaydetmek için üye olmalısınız.'}, status=403)

    content_type = request.GET.get('content_type', '').strip()
    object_id = request.GET.get('object_id', '').strip()

    if not content_type or not object_id:
        return JsonResponse({'error': 'Missing content_type or object_id'}, status=400)

    try:
        object_id = int(object_id)
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid object_id'}, status=400)

    try:
        content_type_obj = ContentType.objects.get(model=content_type)
    except ContentType.DoesNotExist:
        return JsonResponse({'error': 'Invalid content_type'}, status=400)

    saved_item = (
        SavedItem.objects.filter(
            user=request.user,
            content_type=content_type_obj,
            object_id=object_id,
        )
        .prefetch_related('collection_links__collection')
        .first()
    )

    selected_ids = set()
    if saved_item:
        selected_ids = {link.collection_id for link in saved_item.collection_links.all()}

    save_count = SavedItem.objects.filter(
        content_type=content_type_obj,
        object_id=object_id,
    ).count()

    return JsonResponse({
        'status': 'ok',
        'is_saved': bool(saved_item),
        'saved_item_id': saved_item.id if saved_item else None,
        'save_count': save_count,
        'collections': [
            {
                **collection,
                'selected': collection['id'] in selected_ids,
            }
            for collection in _serialize_collections(request.user)
        ],
    })


@login_required
def saved_collections_home(request):
    q = request.GET.get('q', '').strip()
    collection_id = request.GET.get('collection', '').strip()

    question_ct = ContentType.objects.get_for_model(Question)
    answer_ct = ContentType.objects.get_for_model(Answer)

    saved_items_qs = SavedItem.objects.filter(user=request.user).select_related('content_type').prefetch_related('collection_links__collection').order_by('-saved_at')
    if collection_id.isdigit():
        saved_items_qs = saved_items_qs.filter(collection_links__collection_id=int(collection_id), collection_links__collection__user=request.user)

    saved_items = list(saved_items_qs)
    question_ids = [item.object_id for item in saved_items if item.content_type_id == question_ct.id]
    answer_ids = [item.object_id for item in saved_items if item.content_type_id == answer_ct.id]
    question_map = {q.id: q for q in Question.objects.filter(id__in=question_ids).select_related('user')}
    answer_map = {a.id: a for a in Answer.objects.filter(id__in=answer_ids).select_related('question', 'user')}

    rendered_items = []
    query_lower = q.lower()
    for item in saved_items:
        if item.content_type_id == question_ct.id:
            obj = question_map.get(item.object_id)
            if not obj:
                continue
            text = obj.question_text
            if q and query_lower not in text.lower():
                continue
            rendered_items.append({
                'saved_item': item,
                'type': 'question',
                'object': obj,
                'text': text,
                'detail_url': reverse('question_detail', args=[obj.slug]),
                'collections': [link.collection for link in item.collection_links.all()],
            })
        elif item.content_type_id == answer_ct.id:
            obj = answer_map.get(item.object_id)
            if not obj:
                continue
            search_blob = f"{obj.question.question_text}\n{obj.answer_text}".lower()
            if q and query_lower not in search_blob:
                continue
            rendered_items.append({
                'saved_item': item,
                'type': 'answer',
                'object': obj,
                'text': obj.answer_text,
                'detail_url': reverse('single_answer', args=[obj.question.slug, obj.id]),
                'question_url': reverse('question_detail', args=[obj.question.slug]),
                'collections': [link.collection for link in item.collection_links.all()],
            })

    context = {
        'collections': _serialize_collections(request.user),
        'saved_items': rendered_items,
        'selected_collection_id': int(collection_id) if collection_id.isdigit() else None,
        'search_query': q,
    }
    return render(request, 'core/saved_collections.html', context)


@login_required
def create_saved_collection(request):
    if request.method != 'POST':
        return redirect('saved_collections_home')

    name = request.POST.get('name', '').strip()
    description = request.POST.get('description', '').strip()
    if not name:
        messages.error(request, 'Koleksiyon adı boş olamaz.')
        return redirect('saved_collections_home')
    if len(name) > 80:
        messages.error(request, 'Koleksiyon adı çok uzun.')
        return redirect('saved_collections_home')

    _, created = SavedCollection.objects.get_or_create(
        user=request.user,
        name=name,
        defaults={'description': description[:160]},
    )
    if not created:
        messages.info(request, 'Bu isimde bir koleksiyon zaten var.')
    else:
        messages.success(request, 'Koleksiyon oluşturuldu.')
    return redirect('saved_collections_home')


@login_required
def delete_saved_collection(request, collection_id):
    if request.method != 'POST':
        return redirect('saved_collections_home')

    collection = get_object_or_404(SavedCollection, id=collection_id, user=request.user)
    collection.delete()
    messages.success(request, 'Koleksiyon silindi.')
    return redirect('saved_collections_home')


@login_required
def update_saved_item_collections(request, saved_item_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    saved_item = get_object_or_404(SavedItem, id=saved_item_id, user=request.user)
    raw_ids = request.POST.getlist('collection_ids[]') or request.POST.getlist('collection_ids')
    valid_ids = []
    for value in raw_ids:
        try:
            valid_ids.append(int(value))
        except (TypeError, ValueError):
            continue

    allowed_collections = list(SavedCollection.objects.filter(user=request.user, id__in=valid_ids))
    allowed_ids = {collection.id for collection in allowed_collections}

    SavedCollectionItem.objects.filter(saved_item=saved_item).exclude(collection_id__in=allowed_ids).delete()
    for collection in allowed_collections:
        SavedCollectionItem.objects.get_or_create(collection=collection, saved_item=saved_item)

    return JsonResponse({
        'status': 'ok',
        'collections': [
            {
                'id': collection.id,
                'name': collection.name,
            }
            for collection in allowed_collections
        ],
    })
