"""Private income and expense tracking used by the personal tracker."""

import json
from calendar import monthrange
from datetime import date
from decimal import Decimal, InvalidOperation

from django.contrib.auth.decorators import login_required
from django.db.models import Max, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_GET, require_POST

from ..models import MoneyCategory, MoneyTransaction


DEFAULT_CATEGORIES = {
    MoneyCategory.KIND_EXPENSE: (
        ('Market', 'basket2', '#B85C4A'),
        ('Yemek', 'cup-hot', '#A16A3A'),
        ('Ulaşım', 'train-front', '#3D6F8E'),
        ('Fatura', 'receipt', '#765A86'),
        ('Sağlık', 'heart-pulse', '#2F6B4F'),
        ('Eğitim', 'book', '#65743A'),
        ('Eğlence', 'ticket-perforated', '#B08D57'),
        ('Diğer', 'three-dots', '#4E5968'),
    ),
    MoneyCategory.KIND_INCOME: (
        ('Maaş', 'briefcase', '#2F6B4F'),
        ('Ek gelir', 'graph-up-arrow', '#3D6F8E'),
        ('İade', 'arrow-counterclockwise', '#65743A'),
        ('Diğer', 'three-dots', '#4E5968'),
    ),
}
MONEY_KINDS = set(DEFAULT_CATEGORIES)
MONEY_COLORS = {
    '#2F6B4F', '#B08D57', '#B85C4A', '#3D6F8E',
    '#765A86', '#65743A', '#A16A3A', '#4E5968',
}
MAX_CATEGORIES = 50
MAX_AMOUNT = Decimal('9999999999.99')


def _request_payload(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def _selected_month(value):
    today = timezone.localdate()
    try:
        year, month = (int(part) for part in str(value or '').split('-', 1))
        selected = date(year, month, 1)
    except (TypeError, ValueError):
        selected = today.replace(day=1)
    return min(selected, today.replace(day=1))


def _month_bounds(selected_month):
    return selected_month, selected_month.replace(day=monthrange(selected_month.year, selected_month.month)[1])


def _previous_month(selected_month):
    if selected_month.month == 1:
        return selected_month.replace(year=selected_month.year - 1, month=12)
    return selected_month.replace(month=selected_month.month - 1)


def _money_string(value):
    return f'{value or Decimal("0"):.2f}'


def _ensure_default_categories(user):
    existing = set(
        MoneyCategory.objects.filter(user=user).values_list('kind', 'name')
    )
    additions = []
    for kind, definitions in DEFAULT_CATEGORIES.items():
        for position, (name, icon, color) in enumerate(definitions, start=1):
            if (kind, name) not in existing:
                additions.append(MoneyCategory(
                    user=user,
                    name=name,
                    kind=kind,
                    color=color,
                    icon=icon,
                    position=position,
                    is_default=True,
                ))
    if additions:
        MoneyCategory.objects.bulk_create(additions, ignore_conflicts=True)


def _category_payload(category):
    return {
        'id': category.id,
        'name': category.name,
        'kind': category.kind,
        'color': category.color,
        'icon': category.icon,
        'isDefault': category.is_default,
    }


def _transaction_payload(item):
    return {
        'id': item.id,
        'kind': item.kind,
        'amount': _money_string(item.amount),
        'date': item.date.isoformat(),
        'note': item.note,
        'category': _category_payload(item.category) if item.category else None,
    }


def _money_payload(user, month_value=None):
    _ensure_default_categories(user)
    selected_month = _selected_month(month_value)
    month_start, month_end = _month_bounds(selected_month)
    today = timezone.localdate()

    month_items = MoneyTransaction.objects.filter(
        user=user,
        date__range=(month_start, month_end),
    )
    totals = {
        item['kind']: item['total'] or Decimal('0')
        for item in month_items.values('kind').annotate(total=Sum('amount'))
    }
    income = totals.get(MoneyTransaction.KIND_INCOME, Decimal('0'))
    expense = totals.get(MoneyTransaction.KIND_EXPENSE, Decimal('0'))

    previous_start = _previous_month(selected_month)
    previous_end = _month_bounds(previous_start)[1]
    previous_expense = MoneyTransaction.objects.filter(
        user=user,
        kind=MoneyTransaction.KIND_EXPENSE,
        date__range=(previous_start, previous_end),
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    expense_change = None
    if previous_expense:
        expense_change = round(float(((expense - previous_expense) / previous_expense) * 100))

    day_totals = {
        (item['date'], item['kind']): item['total'] or Decimal('0')
        for item in month_items.values('date', 'kind').annotate(total=Sum('amount'))
    }
    daily = []
    for day_number in range(1, month_end.day + 1):
        current = selected_month.replace(day=day_number)
        daily_income = day_totals.get((current, MoneyTransaction.KIND_INCOME), Decimal('0'))
        daily_expense = day_totals.get((current, MoneyTransaction.KIND_EXPENSE), Decimal('0'))
        daily.append({
            'date': current.isoformat(),
            'label': str(day_number),
            'income': _money_string(daily_income),
            'expense': _money_string(daily_expense),
            'future': current > today,
        })

    categories = list(MoneyCategory.objects.filter(user=user).order_by('kind', 'position', 'name'))
    category_totals = {
        item['category_id']: item['total'] or Decimal('0')
        for item in month_items.filter(
            kind=MoneyTransaction.KIND_EXPENSE,
            category__isnull=False,
        ).values('category_id').annotate(total=Sum('amount'))
    }
    breakdown = []
    for category in categories:
        if category.kind != MoneyCategory.KIND_EXPENSE:
            continue
        total = category_totals.get(category.id, Decimal('0'))
        if not total:
            continue
        breakdown.append({
            **_category_payload(category),
            'total': _money_string(total),
            'rate': round(float((total / expense) * 100)) if expense else 0,
        })
    breakdown.sort(key=lambda item: Decimal(item['total']), reverse=True)

    transactions = month_items.select_related('category').order_by('-date', '-created_at')[:150]
    return {
        'month': selected_month.strftime('%Y-%m'),
        'today': today.isoformat(),
        'summary': {
            'income': _money_string(income),
            'expense': _money_string(expense),
            'balance': _money_string(income - expense),
            'expenseChange': expense_change,
            'transactionCount': month_items.count(),
        },
        'daily': daily,
        'breakdown': breakdown,
        'categories': [_category_payload(category) for category in categories],
        'transactions': [_transaction_payload(item) for item in transactions],
    }


def _parse_amount(value):
    try:
        amount = Decimal(str(value).strip().replace(',', '.')).quantize(Decimal('0.01'))
    except (InvalidOperation, TypeError, ValueError):
        return None
    if amount <= 0 or amount > MAX_AMOUNT:
        return None
    return amount


def _clean_transaction(user, payload):
    kind = str(payload.get('kind', '')).strip()
    if kind not in MONEY_KINDS:
        return None, 'Gelir veya gider türünü seçin.'
    amount = _parse_amount(payload.get('amount'))
    if amount is None:
        return None, 'Sıfırdan büyük, geçerli bir tutar girin.'

    transaction_date = parse_date(str(payload.get('date', ''))) or timezone.localdate()
    if transaction_date > timezone.localdate():
        return None, 'İleri tarihli para hareketi eklenemez.'

    try:
        category_id = int(payload.get('categoryId') or 0)
    except (TypeError, ValueError):
        category_id = 0
    category = MoneyCategory.objects.filter(
        id=category_id,
        user=user,
        kind=kind,
    ).first()
    if not category:
        return None, 'Bu türe ait bir kategori seçin.'

    return {
        'kind': kind,
        'amount': amount,
        'category': category,
        'date': transaction_date,
        'note': str(payload.get('note', '')).strip()[:160],
    }, None


def _money_response(request, message, month=None, status=200):
    return JsonResponse({
        'ok': True,
        'message': message,
        'data': _money_payload(request.user, month),
    }, status=status)


@login_required
@require_GET
def money_tracker_data(request):
    return JsonResponse({
        'ok': True,
        'data': _money_payload(request.user, request.GET.get('month')),
    })


@login_required
@require_POST
def money_transaction_create(request):
    payload = _request_payload(request)
    if payload is None:
        return JsonResponse({'error': 'Geçersiz veri.'}, status=400)
    _ensure_default_categories(request.user)
    cleaned, error = _clean_transaction(request.user, payload)
    if error:
        return JsonResponse({'error': error}, status=400)
    MoneyTransaction.objects.create(user=request.user, **cleaned)
    return _money_response(request, 'Para hareketi eklendi.', payload.get('month'), status=201)


@login_required
@require_POST
def money_transaction_update(request, transaction_id):
    item = get_object_or_404(MoneyTransaction, id=transaction_id, user=request.user)
    payload = _request_payload(request)
    if payload is None:
        return JsonResponse({'error': 'Geçersiz veri.'}, status=400)
    cleaned, error = _clean_transaction(request.user, payload)
    if error:
        return JsonResponse({'error': error}, status=400)
    for field, value in cleaned.items():
        setattr(item, field, value)
    item.save(update_fields=[*cleaned.keys(), 'updated_at'])
    return _money_response(request, 'Para hareketi güncellendi.', payload.get('month'))


@login_required
@require_POST
def money_transaction_delete(request, transaction_id):
    item = get_object_or_404(MoneyTransaction, id=transaction_id, user=request.user)
    payload = _request_payload(request) or {}
    item.delete()
    return _money_response(request, 'Para hareketi silindi.', payload.get('month'))


@login_required
@require_POST
def money_category_create(request):
    payload = _request_payload(request)
    if payload is None:
        return JsonResponse({'error': 'Geçersiz veri.'}, status=400)
    if MoneyCategory.objects.filter(user=request.user).count() >= MAX_CATEGORIES:
        return JsonResponse({'error': f'En fazla {MAX_CATEGORIES} kategori ekleyebilirsiniz.'}, status=400)

    kind = str(payload.get('kind', '')).strip()
    if kind not in MONEY_KINDS:
        return JsonResponse({'error': 'Kategori türü geçersiz.'}, status=400)
    name = str(payload.get('name', '')).strip()[:40]
    if not name:
        return JsonResponse({'error': 'Kategori adı boş olamaz.'}, status=400)
    if MoneyCategory.objects.filter(user=request.user, kind=kind, name__iexact=name).exists():
        return JsonResponse({'error': 'Bu isimde bir kategori zaten var.'}, status=400)

    color = str(payload.get('color', '')).upper()
    if color not in MONEY_COLORS:
        color = '#B85C4A' if kind == MoneyCategory.KIND_EXPENSE else '#2F6B4F'
    max_position = MoneyCategory.objects.filter(
        user=request.user,
        kind=kind,
    ).aggregate(position=Max('position'))['position'] or 0
    category = MoneyCategory.objects.create(
        user=request.user,
        name=name,
        kind=kind,
        color=color,
        icon='tag',
        position=min(max_position + 1, 999),
    )
    return JsonResponse({
        'ok': True,
        'message': 'Kategori eklendi.',
        'category': _category_payload(category),
    }, status=201)
