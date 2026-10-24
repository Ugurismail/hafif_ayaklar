import csv
import io
import json
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_POST

from ..models import Kenarda, Reference, ReferenceUsage
from ..reference_history import context_uuid


@login_required
@never_cache
@require_POST
def record_reference_usage(request):
    if len(request.body) > 4096:
        return JsonResponse({'error': 'İstek çok büyük.'}, status=413)
    try:
        data = json.loads(request.body)
        if not isinstance(data, dict):
            raise ValueError
        event = context_uuid(data.get('event_id'))
        context = context_uuid(data.get('context_id'))
        ref_id = data.get('reference_id')
        page, title = data.get('page', ''), data.get('title', '')
        if not event or not context or type(ref_id) is not int or not 0 < ref_id < 2147483648:
            raise ValueError
        if not isinstance(page, str) or not isinstance(title, str) or len(page) > 100 or len(title) > 200:
            raise ValueError
        if any(char in page for char in '()\r\n'):
            raise ValueError
    except (ValueError, TypeError, UnicodeDecodeError):
        return JsonResponse({'error': 'Geçersiz kaynak kaydı.'}, status=400)
    with transaction.atomic():
        # Serialize the per-account limit and duplicate checks across workers.
        User.objects.select_for_update().get(pk=request.user.pk)
        existing = ReferenceUsage.objects.filter(user=request.user, event_id=event).first()
        if existing:
            if (existing.context_id != context or existing.reference_number != ref_id or existing.page != page.strip()):
                return JsonResponse({'error': 'Bu işlem kimliği başka bir kayıt için kullanılmış.'}, status=409)
            return JsonResponse({'id': existing.pk, 'created_at': existing.created_at.isoformat()})
        if ReferenceUsage.objects.filter(user=request.user, created_at__gte=timezone.now() - timedelta(hours=1)).count() >= 300:
            response = JsonResponse({'error': 'Saatlik kaynak ekleme sınırına ulaşıldı.'}, status=429)
            response['Retry-After'] = '3600'
            return response
        reference = get_object_or_404(Reference, pk=ref_id)
        draft = None
        if data.get('draft_id'):
            draft_id = str(data['draft_id'])
            if not draft_id.isascii() or not draft_id.isdigit() or len(draft_id) > 18:
                return JsonResponse({'error': 'Geçersiz taslak.'}, status=400)
            draft = get_object_or_404(Kenarda, pk=draft_id, user=request.user, is_sent=False)
        usage = ReferenceUsage.objects.create(
            user=request.user, event_id=event, context_id=context,
            reference=reference, reference_number=reference.pk,
            citation=f'{reference}. {reference.rest}'[:4000], page=page.strip(), title=title.strip(),
            draft=draft,
        )
    return JsonResponse({'id': usage.pk, 'created_at': usage.created_at.isoformat()}, status=201)


def filtered_history(request):
    rows = ReferenceUsage.objects.filter(user=request.user).select_related('answer__question', 'draft')
    query = request.GET.get('q', '').strip()[:200]
    if query:
        rows = rows.filter(Q(citation__icontains=query) | Q(title__icontains=query))
    status = request.GET.get('status', '')
    if status in {'writing', 'draft', 'published'}:
        rows = rows.filter(status=status)
    for parameter, lookup in [('from', 'created_at__date__gte'), ('to', 'created_at__date__lte')]:
        try:
            value = parse_date(request.GET.get(parameter, ''))
        except ValueError:
            value = None
        if value:
            rows = rows.filter(**{lookup: value})
    return rows


def csv_cell(value):
    value = str(value or '')
    # Spreadsheet apps must not execute user-provided bibliographic text.
    return "'" + value if value.lstrip().startswith(('=', '+', '-', '@')) or value.startswith(('\t', '\r', '\n')) else value


@login_required
@never_cache
@require_GET
def reference_history(request):
    rows = filtered_history(request)
    if request.GET.get('format') == 'csv':
        def lines():
            output = io.StringIO()
            writer = csv.writer(output)
            yield '\ufeff'
            writer.writerow(['Eklenme zamanı', 'Kaynak', 'Sayfa', 'Başlık', 'Durum', 'Kaldırılma zamanı'])
            yield output.getvalue()
            for item in rows.order_by('created_at', 'pk').iterator(chunk_size=500):
                output.seek(0)
                output.truncate(0)
                writer.writerow([timezone.localtime(item.created_at).isoformat(), csv_cell(item.citation),
                                 csv_cell(item.page), csv_cell(item.title), item.get_status_display(),
                                 timezone.localtime(item.removed_at).isoformat() if item.removed_at else ''])
                yield output.getvalue()
        response = StreamingHttpResponse(lines(), content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="kaynak-gecmisim.csv"'
        response['X-Content-Type-Options'] = 'nosniff'
        return response
    params = request.GET.copy()
    params.pop('page', None)
    params.pop('format', None)
    return render(request, 'core/reference_history.html', {
        'page_obj': Paginator(rows, 30).get_page(request.GET.get('page')),
        'filters': params.urlencode(),
    })
