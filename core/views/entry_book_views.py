"""Persistent entry-book selections used by the profile export workflow."""

import json

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models import Count, Exists, Max, OuterRef
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from ..models import Answer, EntryBook, EntryBookItem
from .answer_profile_views import serialize_answer_for_selector


MAX_BOOK_ENTRIES = 5000


def _error(message, status=400):
    return JsonResponse({'error': message}, status=status)


def _parse_payload(request):
    try:
        payload = json.loads(request.body or b'{}')
    except (TypeError, ValueError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def _validated_title(payload, user, current_book=None):
    title = str(payload.get('title') or '').strip()
    if not title:
        raise ValueError('Kitap adı gerekli.')
    if len(title) > EntryBook._meta.get_field('title').max_length:
        raise ValueError('Kitap adı en fazla 120 karakter olabilir.')

    duplicates = EntryBook.objects.filter(user=user, title__iexact=title)
    if current_book is not None:
        duplicates = duplicates.exclude(id=current_book.id)
    if duplicates.exists():
        raise ValueError('Bu adla bir kitabın zaten var.')
    return title


def _validated_answers(payload, user):
    raw_entry_ids = payload.get('entry_ids')
    if not isinstance(raw_entry_ids, list):
        raise ValueError('Entry listesi geçersiz.')
    if not raw_entry_ids:
        raise ValueError('Kitap için en az bir entry seç.')
    if len(raw_entry_ids) > MAX_BOOK_ENTRIES:
        raise ValueError(f'Bir kitap en fazla {MAX_BOOK_ENTRIES} entry içerebilir.')

    entry_ids = []
    seen_ids = set()
    for raw_entry_id in raw_entry_ids:
        if isinstance(raw_entry_id, bool):
            raise ValueError('Entry listesi geçersiz.')
        try:
            entry_id = int(raw_entry_id)
        except (TypeError, ValueError):
            raise ValueError('Entry listesi geçersiz.') from None
        if entry_id < 1:
            raise ValueError('Entry listesi geçersiz.')
        if entry_id not in seen_ids:
            entry_ids.append(entry_id)
            seen_ids.add(entry_id)

    answer_map = Answer.objects.filter(
        user=user,
        id__in=entry_ids,
    ).in_bulk()
    if len(answer_map) != len(entry_ids):
        raise ValueError('Seçim içinde sana ait olmayan veya silinmiş bir entry var.')
    return [answer_map[entry_id] for entry_id in entry_ids]


def _book_summary(book):
    item_count = getattr(book, 'item_count', None)
    if item_count is None:
        item_count = book.items.count()
    summary = {
        'id': book.id,
        'title': book.title,
        'item_count': item_count,
        'updated_at': book.updated_at.isoformat(),
    }
    if hasattr(book, 'contains_entry'):
        summary['contains_entry'] = bool(book.contains_entry)
    return summary


def _replace_book_items(book, answers):
    book.items.all().delete()
    EntryBookItem.objects.bulk_create([
        EntryBookItem(
            book=book,
            answer=answer,
            position=index,
        )
        for index, answer in enumerate(answers, start=1)
    ])


@login_required
@require_http_methods(['GET', 'POST'])
def entry_books(request):
    if request.method == 'GET':
        books = EntryBook.objects.filter(user=request.user)
        entry_id = request.GET.get('entry_id')
        if entry_id:
            try:
                entry_id = int(entry_id)
            except (TypeError, ValueError):
                return _error('Entry kimliği geçersiz.')
            if not Answer.objects.filter(id=entry_id, user=request.user).exists():
                return _error('Entry bulunamadı.', status=404)
            books = books.annotate(
                contains_entry=Exists(
                    EntryBookItem.objects.filter(
                        book_id=OuterRef('pk'),
                        answer_id=entry_id,
                    )
                )
            )

        books = (
            books
            .annotate(item_count=Count('items'))
            .order_by('-updated_at', '-id')
        )
        return JsonResponse({
            'books': [_book_summary(book) for book in books],
        })

    payload = _parse_payload(request)
    if payload is None:
        return _error('Geçersiz istek.')

    try:
        title = _validated_title(payload, request.user)
        answers = _validated_answers(payload, request.user)
        with transaction.atomic():
            book = EntryBook.objects.create(user=request.user, title=title)
            _replace_book_items(book, answers)
    except ValueError as error:
        return _error(str(error))
    except IntegrityError:
        return _error('Bu adla bir kitabın zaten var.')

    book.item_count = len(answers)
    return JsonResponse({'book': _book_summary(book)}, status=201)


@login_required
@require_http_methods(['GET', 'PUT', 'DELETE'])
def entry_book_detail(request, book_id):
    book = get_object_or_404(EntryBook, id=book_id, user=request.user)

    if request.method == 'GET':
        items = (
            book.items.select_related('answer__question')
            .order_by('position', 'id')
        )
        entries = [
            serialize_answer_for_selector(item.answer)
            for item in items
        ]
        book.item_count = len(entries)
        return JsonResponse({
            'book': {
                **_book_summary(book),
                'entries': entries,
            },
        })

    if request.method == 'DELETE':
        book.delete()
        return JsonResponse({'deleted': True})

    payload = _parse_payload(request)
    if payload is None:
        return _error('Geçersiz istek.')

    try:
        with transaction.atomic():
            book = EntryBook.objects.select_for_update().get(
                id=book.id,
                user=request.user,
            )
            title = _validated_title(payload, request.user, current_book=book)
            answers = _validated_answers(payload, request.user)
            book.title = title
            book.save(update_fields=['title', 'updated_at'])
            _replace_book_items(book, answers)
    except ValueError as error:
        return _error(str(error))
    except IntegrityError:
        return _error('Bu adla bir kitabın zaten var.')

    book.item_count = len(answers)
    return JsonResponse({'book': _book_summary(book)})


@login_required
@require_http_methods(['POST'])
def entry_book_add_entry(request, book_id):
    payload = _parse_payload(request)
    if payload is None:
        return _error('Geçersiz istek.')

    raw_entry_id = payload.get('entry_id')
    if isinstance(raw_entry_id, bool):
        return _error('Entry kimliği geçersiz.')
    try:
        entry_id = int(raw_entry_id)
    except (TypeError, ValueError):
        return _error('Entry kimliği geçersiz.')

    answer = Answer.objects.filter(
        id=entry_id,
        user=request.user,
    ).first()
    if answer is None:
        return _error('Entry bulunamadı.', status=404)

    with transaction.atomic():
        try:
            book = EntryBook.objects.select_for_update().get(
                id=book_id,
                user=request.user,
            )
        except EntryBook.DoesNotExist:
            return _error('Kitap bulunamadı.', status=404)
        current_count = book.items.count()
        if book.items.filter(answer=answer).exists():
            book.item_count = current_count
            book.contains_entry = True
            return JsonResponse({
                'book': _book_summary(book),
                'added': False,
                'message': 'Bu entry zaten kitapta.',
            })
        if current_count >= MAX_BOOK_ENTRIES:
            return _error(
                f'Bir kitap en fazla {MAX_BOOK_ENTRIES} entry içerebilir.'
            )

        max_position = (
            book.items.aggregate(max_position=Max('position'))['max_position']
            or 0
        )
        EntryBookItem.objects.create(
            book=book,
            answer=answer,
            position=max_position + 1,
        )
        book.save(update_fields=['updated_at'])

    book.item_count = current_count + 1
    book.contains_entry = True
    return JsonResponse({
        'book': _book_summary(book),
        'added': True,
        'message': f'Entry “{book.title}” kitabına eklendi.',
    })
