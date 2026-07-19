"""
Definition and reference views
- create_definition
- get_user_definitions
- edit_definition
- delete_definition
- get_all_definitions
- create_reference
- get_references
- edit_reference
- delete_reference
"""

import json
import re
from html import unescape
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Case, IntegerField, Q, Value, When
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST

from ..models import Question, Answer, Definition, Reference
from ..forms import DefinitionForm, ReferenceForm
from ..utils import REFERENCE_CITATION_PATTERN, build_reference_usage_counts, extract_reference_citations


@login_required
@require_POST
def create_definition(request, slug):
    question = get_object_or_404(Question, slug=slug)
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        data = json.loads(body)
        form = DefinitionForm(data)
        if form.is_valid():
            definition_obj = form.save(commit=False)
            definition_obj.user = request.user
            definition_obj.question = question
            # answer alanını boş bırak - tanım metnin içinde (tanim:...) olarak kullanılacak
            definition_obj.answer = None
            definition_obj.save()

            return JsonResponse({
                'status': 'success',
                'definition_id': definition_obj.id,
                'definition_text': definition_obj.definition_text,
                'question_text': question.question_text
            }, status=200)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    return JsonResponse({'status': 'invalid_method'}, status=405)


@login_required
def get_user_definitions(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        user = get_object_or_404(User, username=username) if username else request.user
        q = request.GET.get('q', '').strip()
        page_num = request.GET.get('page', '1')

        defs = Definition.objects.filter(user=user)
        if q:
            defs = defs.filter(
                Q(definition_text__icontains=q) |
                Q(question__question_text__icontains=q)
            )

        defs = defs.order_by('question__question_text')
        paginator = Paginator(defs, 5)
        try:
            page_obj = paginator.page(page_num)
        except:
            page_obj = paginator.page(1)

        data_list = []
        for d in page_obj.object_list:
            token_long = f'(tanim:{d.question.question_text}:{d.id})'
            token_short = f'(t:{d.question.question_text}:{d.id})'

            usage_count_self = Answer.objects.filter(user=user).filter(
                Q(answer_text__icontains=token_long) | Q(answer_text__icontains=token_short)
            ).count()
            usage_count_all = Answer.objects.filter(
                Q(answer_text__icontains=token_long) | Q(answer_text__icontains=token_short)
            ).count()

            data_list.append({
                'id': d.id,
                'question_id': d.question.id,
                'question_text': d.question.question_text,
                'definition_text': d.definition_text[:80] + '...' if len(d.definition_text) > 80 else d.definition_text,
                'usage_count_self': usage_count_self,
                'usage_count_all': usage_count_all,
            })

        response_data = {
            'definitions': data_list,
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'error': 'invalid method'}, status=405)


@login_required
def edit_definition(request, definition_id):
    definition = get_object_or_404(Definition, id=definition_id, user=request.user)
    if request.method == 'POST':
        # İçerik JSON veya form-data olabilir:
        if request.headers.get('Content-Type') == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.POST
        form = DefinitionForm(data, instance=definition)
        if form.is_valid():
            form.save()
            # Tanı nesnesini DB'den tazeleyelim
            definition.refresh_from_db()
            if definition.answer:
                definition.answer.answer_text = definition.definition_text
                definition.answer.save()
            else:
                # Eğer tanıya bağlı Answer yoksa yeni oluştur
                new_answer = Answer.objects.create(
                    question=definition.question,
                    user=definition.user,
                    answer_text=definition.definition_text
                )
                definition.answer = new_answer
                definition.save()
            messages.success(request, 'Tanım güncellendi.')
            # Değişikliklerin hemen görünmesi için, düzenlemeden sonra ilgili soru detayına yönlendirebilirsiniz:
            return redirect('question_detail', slug=definition.question.slug)
        else:
            messages.error(request, 'Form hataları: %s' % form.errors)
    else:
        form = DefinitionForm(instance=definition)

    return render(request, 'core/edit_definition.html', {
        'form': form,
        'definition': definition,
    })


@login_required
def delete_definition(request, definition_id):
    definition = get_object_or_404(Definition, id=definition_id, user=request.user)
    if request.method == 'POST':
        definition.delete()
        messages.success(request, 'Tanım silindi.')
        return redirect(f"{reverse('user_profile', args=[request.user.username])}?tab=tanimlar")
    # "GET" istek geldiğinde doğrulama penceresi (confirm) gösterebilirsiniz.
    return render(request, 'core/confirm_delete_definition.html', {'definition': definition})


@login_required
def get_all_definitions(request):
    """
    Tüm kullanıcıların tanımlarını JSON döndürür.
    ?q= => arama
    ?page= => sayfa
    Aynı şekilde usage_count içerir.
    """
    if request.method == 'GET':
        q = request.GET.get('q', '').strip()
        page_num = request.GET.get('page', '1')

        defs = Definition.objects.select_related('question', 'user').all()

        if q:
            defs = defs.filter(
                Q(definition_text__icontains=q) |
                Q(question__question_text__icontains=q) |
                Q(user__username__icontains=q)
            )

        # Alfabetik sıralama
        defs = defs.order_by('question__question_text')

        # Sayfalama
        paginator = Paginator(defs, 5)  # 5'erli
        try:
            page_obj = paginator.page(page_num)
        except:
            page_obj = paginator.page(1)

        data_list = []
        for d in page_obj.object_list:
            token_long = f'(tanim:{d.question.question_text}:{d.id})'
            token_short = f'(t:{d.question.question_text}:{d.id})'
            usage_count_all = Answer.objects.filter(
                Q(answer_text__icontains=token_long) | Q(answer_text__icontains=token_short)
            ).count()
            data_list.append({
                'id': d.id,
                'question_text': d.question.question_text,
                'definition_text': d.definition_text[:80] + '...' if len(d.definition_text) > 80 else d.definition_text,
                'username': d.user.username,
                'usage_count_all': usage_count_all,
            })
            data_list = sorted(data_list, key=lambda x: -x['usage_count_all'])

        return JsonResponse({
            'definitions': data_list,
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
        }, status=200)
    else:
        return JsonResponse({'error': 'invalid method'}, status=405)


@require_POST
@login_required
def create_reference(request):
    """
    AJAX ile yeni bir Reference (Kaynak) oluşturmak için.
    Aynı kaynağın duplicate olarak eklenmesini önlemek için kontrol yapar.
    """
    form = ReferenceForm(request.POST)
    if form.is_valid():
        def normalize_semicolon_list(value):
            parts = [p.strip() for p in (value or '').split(';') if p.strip()]
            return '; '.join(parts)

        author_surname = normalize_semicolon_list(form.cleaned_data.get('author_surname'))
        author_name = normalize_semicolon_list(form.cleaned_data.get('author_name'))
        year = form.cleaned_data.get('year')
        metin_ismi = (form.cleaned_data.get('metin_ismi') or '').strip()
        rest = (form.cleaned_data.get('rest') or '').strip()
        abbreviation = (form.cleaned_data.get('abbreviation') or '').strip()

        with transaction.atomic():
            existing_qs = Reference.objects.filter(
                created_by=request.user,
                author_surname=author_surname,
                author_name=author_name,
                year=year,
                rest=rest,
            )
            if metin_ismi:
                existing_qs = existing_qs.filter(metin_ismi=metin_ismi)
            else:
                existing_qs = existing_qs.filter(Q(metin_ismi__isnull=True) | Q(metin_ismi=''))
            if abbreviation:
                existing_qs = existing_qs.filter(abbreviation=abbreviation)
            else:
                existing_qs = existing_qs.filter(Q(abbreviation__isnull=True) | Q(abbreviation=''))

            existing_ref = existing_qs.order_by('id').first()
            if existing_ref:
                return JsonResponse({
                    'status': 'success',
                    'reference': {'id': existing_ref.id, 'display': str(existing_ref)},
                    'message': 'Bu kaynak zaten ekli. Mevcut kaynak kullanılacak.'
                }, status=200)

            reference_obj = form.save(commit=False)
            reference_obj.created_by = request.user
            reference_obj.author_surname = author_surname
            reference_obj.author_name = author_name
            reference_obj.metin_ismi = metin_ismi or None
            reference_obj.rest = rest
            reference_obj.abbreviation = abbreviation or None
            reference_obj.save()

        return JsonResponse({
            'status': 'success',
            'reference': {'id': reference_obj.id, 'display': str(reference_obj)},
            'message': 'Kaynak başarıyla eklendi!'
        }, status=200)
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@login_required
def get_references(request):
    q = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 5))
    username = request.GET.get('username')
    scope = request.GET.get('scope', 'user')  # 'user' (varsayılan) veya 'all'
    reference_sort = request.GET.get('sort', 'alpha')
    reference_order = request.GET.get('order', 'asc')

    # scope parametresine göre kaynakları filtrele
    if scope == 'all':
        # Tüm site kaynaklarını getir (yanıt yazarken kullanılacak)
        references = Reference.objects.all()
    else:
        # Sadece belirli kullanıcının kaynaklarını getir (profil sayfası için)
        user = get_object_or_404(User, username=username) if username else request.user
        references = Reference.objects.filter(created_by=user)
    if q:
        references = references.filter(
            Q(author_surname__icontains=q) |
            Q(author_name__icontains=q) |
            Q(rest__icontains=q) |
            Q(abbreviation__icontains=q) |
            Q(metin_ismi__icontains=q) |
            Q(year__iexact=q)
        )
    if reference_sort == 'relevance' and q:
        relevance_rules = [
            When(abbreviation__iexact=q, then=Value(0)),
            When(metin_ismi__iexact=q, then=Value(1)),
            When(author_surname__iexact=q, then=Value(2)),
            When(author_name__iexact=q, then=Value(3)),
            When(abbreviation__istartswith=q, then=Value(4)),
            When(metin_ismi__istartswith=q, then=Value(5)),
            When(author_surname__istartswith=q, then=Value(6)),
            When(author_name__istartswith=q, then=Value(7)),
            When(rest__istartswith=q, then=Value(8)),
        ]
        if q.isdigit():
            relevance_rules.insert(4, When(year=int(q), then=Value(4)))

        references = references.annotate(
            search_rank=Case(
                *relevance_rules,
                default=Value(10),
                output_field=IntegerField(),
            )
        ).order_by('search_rank', Lower('author_surname'), 'year', 'id')
        ref_items = None
    elif reference_sort == 'year':
        ordering = '-year' if reference_order == 'desc' else 'year'
        references = references.order_by(ordering, Lower('author_surname'), Lower('author_name'))
        ref_items = None
    elif reference_sort == 'created':
        ordering = '-id' if reference_order == 'desc' else 'id'
        references = references.order_by(ordering)
        ref_items = None
    elif reference_sort == 'usage':
        ref_items = list(references)
        usage_counts = build_reference_usage_counts(reference_ids=[ref.id for ref in ref_items])
        for ref in ref_items:
            ref.usage_count = usage_counts.get(ref.id, 0)
        ref_items.sort(
            key=lambda r: (r.usage_count, r.id),
            reverse=(reference_order != 'asc'),
        )
    else:
        references = references.order_by(Lower('author_surname'), 'year')
        ref_items = None

    paginator = Paginator(ref_items if ref_items is not None else references, page_size)
    page_obj = paginator.get_page(page)

    page_usage_counts = {}
    if ref_items is None:
        page_reference_ids = [ref.id for ref in page_obj.object_list]
        if page_reference_ids:
            page_usage_counts = build_reference_usage_counts(reference_ids=page_reference_ids)

    data = []
    for ref in page_obj.object_list:
        data.append({
            'id': ref.id,
            'author_surname': ref.author_surname,
            'author_name': ref.author_name,
            'year': ref.year,
            'metin_ismi': ref.metin_ismi or '',
            'rest': ref.rest,
            'abbreviation': ref.abbreviation or '',
            'usage_count': getattr(ref, 'usage_count', page_usage_counts.get(ref.id, 0)),
            'display': str(ref),
            'usage_url': reverse('reference_usage_data', args=[ref.id]),
        })

    response = {
        'references': data,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'total_count': paginator.count,
    }
    return JsonResponse(response, status=200)


REFERENCE_CONTEXT_MARKER = 'HAFIFAYAKLARREFMARKERZXQ'
REFERENCE_SENTENCE_BOUNDARY_PATTERN = re.compile(
    r'(?<=[.!?])\s+|(?<=[a-zçğıöşü0-9][.!?])(?=[A-ZÇĞİÖŞÜ])|\n+'
)


def _clean_reference_context(text):
    text = REFERENCE_CITATION_PATTERN.sub('', text)
    text = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'\((?:bkz|t|tanim|def):[^)]+\)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<!\\)[*_]{1,3}', '', text)
    text = unescape(strip_tags(text)).replace('\r\n', '\n').replace('\r', '\n')
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r' *\n+ *', '\n', text)
    text = re.sub(r'\s+([,.;:!?])', r'\1', text)
    return text.strip()


def _reference_context(answer_text, reference_id):
    text = answer_text or ''
    target_match = next(
        (
            match for match in REFERENCE_CITATION_PATTERN.finditer(text)
            if int(match.group('reference_id')) == reference_id
        ),
        None,
    )
    if not target_match:
        return {'before': '', 'sentence': '', 'after': ''}

    marked_text = (
        text[:target_match.start()]
        + f' {REFERENCE_CONTEXT_MARKER} '
        + text[target_match.end():]
    )
    cleaned_text = _clean_reference_context(marked_text)
    sentences = [
        sentence.strip()
        for sentence in REFERENCE_SENTENCE_BOUNDARY_PATTERN.split(cleaned_text)
        if sentence.strip()
    ]
    marker_index = next(
        (index for index, sentence in enumerate(sentences) if REFERENCE_CONTEXT_MARKER in sentence),
        None,
    )
    if marker_index is None:
        return {'before': '', 'sentence': '', 'after': ''}

    marker_sentence = sentences[marker_index]
    marker_position = marker_sentence.index(REFERENCE_CONTEXT_MARKER)
    text_before_marker = marker_sentence[:marker_position]

    def without_marker(sentence):
        value = sentence.replace(REFERENCE_CONTEXT_MARKER, '').strip()
        value = re.sub(r'\s+', ' ', value)
        value = re.sub(r'\s+([,.;:!?])', r'\1', value)
        return value if re.search(r'\w', value, flags=re.UNICODE) else ''

    primary_index = marker_index
    if not re.search(r'\w', text_before_marker, flags=re.UNICODE):
        previous_index = marker_index - 1
        while previous_index >= 0 and not without_marker(sentences[previous_index]):
            previous_index -= 1
        if previous_index >= 0:
            primary_index = previous_index

    citation_sentence = without_marker(sentences[primary_index])
    if not citation_sentence:
        citation_sentence = without_marker(marker_sentence)
        primary_index = marker_index

    before = ''
    for index in range(primary_index - 1, -1, -1):
        before = without_marker(sentences[index])
        if before:
            break

    after = ''
    for index in range(primary_index + 1, len(sentences)):
        after = without_marker(sentences[index])
        if after:
            break

    return {
        'before': before,
        'sentence': citation_sentence,
        'after': after,
    }


@login_required
def reference_usage_data(request, reference_id):
    reference = get_object_or_404(
        Reference.objects.select_related('created_by'),
        id=reference_id,
    )
    candidate_answers = (
        Answer.objects.filter(
            Q(answer_text__icontains='(kaynak') | Q(answer_text__icontains='(k')
        )
        .filter(answer_text__icontains=str(reference.id))
        .select_related('question', 'user')
        .order_by('-updated_at', '-id')
    )

    entries = []
    total_citation_count = 0
    for answer in candidate_answers:
        citations = extract_reference_citations(answer.answer_text, reference.id)
        if not citations:
            continue

        pages = []
        for citation in citations:
            page = citation['page']
            if page and page not in pages:
                pages.append(page)

        answer.reference_context = _reference_context(answer.answer_text, reference.id)
        answer.reference_pages = pages
        answer.reference_citation_count = len(citations)
        total_citation_count += len(citations)
        entries.append(answer)

    entries_page = Paginator(entries, 8).get_page(request.GET.get('page'))
    entry_data = [
        {
            'id': answer.id,
            'title': answer.question.question_text,
            'author': answer.user.username,
            'updated_at': answer.updated_at.isoformat(),
            'context_before': answer.reference_context['before'],
            'citation_sentence': answer.reference_context['sentence'],
            'context_after': answer.reference_context['after'],
            'pages': answer.reference_pages,
            'usage_count': answer.reference_citation_count,
            'url': reverse('single_answer', args=[answer.question.slug, answer.id]),
        }
        for answer in entries_page.object_list
    ]
    return JsonResponse({
        'reference': {
            'id': reference.id,
            'display': str(reference),
            'details': reference.rest,
            'abbreviation': reference.abbreviation or '',
        },
        'counts': {
            'entries': len(entries),
            'usages': total_citation_count,
        },
        'entries': entry_data,
        'pagination': {
            'page': entries_page.number,
            'has_next': entries_page.has_next(),
            'next_page': entries_page.next_page_number() if entries_page.has_next() else None,
            'total_pages': entries_page.paginator.num_pages,
        },
    })


@login_required
def edit_reference(request, reference_id):
    # Yalnızca kaynağı oluşturan kullanıcı düzenleyebilsin
    reference = get_object_or_404(Reference, id=reference_id, created_by=request.user)
    if request.method == 'POST':
        form = ReferenceForm(request.POST, instance=reference)
        if form.is_valid():
            form.save()
            messages.success(request, "Kaynak başarıyla güncellendi.")
            # Get tab parameter from GET or default to 'kaynaklarim'
            params = {'tab': request.GET.get('tab', 'kaynaklarim')}
            for key in ('sort', 'order', 'q', 'r_page'):
                val = (request.GET.get(key) or '').strip()
                if val:
                    params[key] = val
            return redirect(f"{reverse('user_profile', kwargs={'username': request.user.username})}?{urlencode(params)}")
    else:
        form = ReferenceForm(instance=reference)
    return render(request, 'core/edit_reference.html', {'form': form})


@login_required
def delete_reference(request, reference_id):
    # Yalnızca kaynağı oluşturan kullanıcı silebilsin
    reference = get_object_or_404(Reference, id=reference_id, created_by=request.user)
    if request.method == 'POST':
        reference.delete()
        messages.success(request, "Kaynak başarıyla silindi.")
        params = {'tab': request.GET.get('tab', 'kaynaklarim')}
        for key in ('sort', 'order', 'q', 'r_page'):
            val = (request.GET.get(key) or '').strip()
            if val:
                params[key] = val
        return redirect(f"{reverse('user_profile', kwargs={'username': request.user.username})}?{urlencode(params)}")
    return render(request, 'core/confirm_delete_reference.html', {'reference': reference})
