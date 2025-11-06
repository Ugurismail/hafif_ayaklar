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

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from ..models import Question, Answer, Definition, Reference
from ..forms import DefinitionForm, ReferenceForm


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
            definition_obj.save()

            # TANIMI AYNI ZAMANDA ANSWER OLARAK DA KAYDET
            answer_obj = Answer.objects.create(
                question=question,
                user=request.user,
                answer_text=definition_obj.definition_text
            )
            # Oluşturulan answer'ı tanıma bağlayın
            definition_obj.answer = answer_obj
            definition_obj.save()

            return JsonResponse({
                'status': 'success',
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
            usage_count_self = Answer.objects.filter(
                user=user,
                answer_text__icontains=f'(tanim:{d.question.question_text}:{d.id})'
            ).count()
            usage_count_all = Answer.objects.filter(
                answer_text__icontains=f'(tanim:{d.question.question_text}:{d.id})'
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
            usage_count_all = Answer.objects.filter(
                answer_text__icontains=f'(tanim:{d.question.question_text}:{d.id})'
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
    """
    form = ReferenceForm(request.POST)
    if form.is_valid():
        # commit=False ile kaynağı oluşturuyoruz, ardından created_by alanını ekliyoruz
        reference_obj = form.save(commit=False)
        reference_obj.created_by = request.user
        reference_obj.save()
        data = {
            'status': 'success',
            'reference': {
                'id': reference_obj.id,
                'display': str(reference_obj),
            }
        }
        return JsonResponse(data, status=200)
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@login_required
def get_references(request):
    q = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 5))
    username = request.GET.get('username')
    user = get_object_or_404(User, username=username) if username else request.user

    references = Reference.objects.all()
    if q:
        references = references.filter(
            Q(author_surname__icontains=q) |
            Q(author_name__icontains=q) |
            Q(rest__icontains=q) |
            Q(abbreviation__icontains=q) |
            Q(metin_ismi__icontains=q) |
            Q(year__iexact=q)
        )
    references = references.order_by('author_surname', 'year')

    paginator = Paginator(references, page_size)
    page_obj = paginator.get_page(page)

    data = []
    for ref in page_obj.object_list:
        data.append({
            'id': ref.id,
            'author_surname': ref.author_surname,
            'author_name': ref.author_name,
            'year': ref.year,
            'rest': ref.rest,
            'abbreviation': ref.abbreviation or '',
            'display': str(ref),
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


@login_required
def edit_reference(request, reference_id):
    # Yalnızca kaynağı oluşturan kullanıcı düzenleyebilsin
    reference = get_object_or_404(Reference, id=reference_id, created_by=request.user)
    if request.method == 'POST':
        form = ReferenceForm(request.POST, instance=reference)
        if form.is_valid():
            form.save()
            messages.success(request, "Kaynak başarıyla güncellendi.")
            return redirect('user_profile', username=request.user.username)
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
        return redirect('user_profile', username=request.user.username)
    return render(request, 'core/confirm_delete_reference.html', {'reference': reference})
