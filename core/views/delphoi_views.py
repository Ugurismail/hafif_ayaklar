"""
Delphoi prophecy views
- delphoi_home
- delphoi_result
"""

from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from ..models import Question, DelphoiProphecy, DelphoiRequest
from ..forms import DelphoiProphecyForm


@login_required
def delphoi_home(request):
    user = request.user
    question = Question.objects.first()

    positive_count = DelphoiProphecy.objects.filter(user=user, question=question, type='positive').count()
    negative_count = DelphoiProphecy.objects.filter(user=user, question=question, type='negative').count()
    positive_limit = positive_count >= 3
    negative_limit = negative_count >= 3
    disable_form = positive_limit and negative_limit

    edit_id = request.GET.get("edit")
    updated_id = request.GET.get("updated_id")
    edit_id = int(edit_id) if edit_id else None
    updated_id = int(updated_id) if updated_id else None
    update_message = "Kehanet güncellendi!" if updated_id else None

    # SİLME İŞLEMİ
    if request.method == 'POST' and 'delete_id' in request.POST:
        to_delete = get_object_or_404(DelphoiProphecy, id=request.POST['delete_id'], user=user)
        to_delete.delete()
        return redirect('delphoi_home')

    # DÜZENLEME İŞLEMİ
    edit_form = None
    if edit_id:
        edit_prophecy = get_object_or_404(DelphoiProphecy, id=edit_id, user=user)
        if request.method == 'POST' and 'save_edit' in request.POST:
            edit_form = DelphoiProphecyForm(request.POST)
            if edit_prophecy.type == 'positive':
                edit_form.fields['negative'].required = False
            else:
                edit_form.fields['positive'].required = False
            if edit_form.is_valid():
                new_text = (
                    edit_form.cleaned_data['positive'] if edit_prophecy.type == 'positive'
                    else edit_form.cleaned_data['negative']
                )
                if edit_prophecy.text != new_text:
                    edit_prophecy.text = new_text
                    edit_prophecy.save()
                return redirect(f"{request.path}?edit={edit_prophecy.id}&updated_id={edit_prophecy.id}")
        else:
            edit_form = DelphoiProphecyForm(initial={
                'positive': edit_prophecy.text if edit_prophecy.type == 'positive' else '',
                'negative': edit_prophecy.text if edit_prophecy.type == 'negative' else '',
            })
        if edit_prophecy.type == 'positive':
            edit_form.fields['negative'].required = False
        else:
            edit_form.fields['positive'].required = False

    # EKLEME
    if request.method == 'POST' and not edit_id and 'delete_id' not in request.POST:
        form = DelphoiProphecyForm(request.POST)
        if form.is_valid() and not disable_form:
            if not positive_limit and form.cleaned_data['positive'].strip():
                DelphoiProphecy.objects.create(
                    user=user, question=question, type='positive', text=form.cleaned_data['positive'].strip()
                )
            if not negative_limit and form.cleaned_data['negative'].strip():
                DelphoiProphecy.objects.create(
                    user=user, question=question, type='negative', text=form.cleaned_data['negative'].strip()
                )
            return redirect('delphoi_home')
    else:
        form = DelphoiProphecyForm()

    prophecies = DelphoiProphecy.objects.filter(user=user, question=question).order_by('-created_at')

    # --- YANITI DUY (KAHİNE GÜNLÜK) KONTROLÜ ---
    now = timezone.now()
    last_request = DelphoiRequest.objects.filter(user=user, question=question).order_by('-requested_at').first()
    can_request_prophecy = True
    wait_until = None
    if last_request and (now - last_request.requested_at) < timedelta(seconds=24):
        can_request_prophecy = False
        wait_until = last_request.requested_at + timedelta(seconds=24)

    prophecy_result = request.GET.get('prophecy_result')  # Sadece istek sonrası döner (redirectte)

    context = {
        'form': form,
        'can_request_prophecy': can_request_prophecy,
        'wait_until': wait_until,
        'prophecy_result': prophecy_result,
        'disable_form': disable_form,
        'positive_count': positive_count,
        'negative_count': negative_count,
        'prophecies': prophecies,
        'edit_id': edit_id,
        'edit_form': edit_form,
        'updated_id': updated_id,
        'update_message': update_message,
    }
    return render(request, 'core/delphoi_home.html', context)


@login_required
def delphoi_result(request):
    user = request.user
    question = Question.objects.first()

    # Günlük tıklama kontrolü
    now = timezone.now()

    # Transaction içinde atomik kontrol ve kayıt
    with transaction.atomic():
        # Son isteği kilitle ve kontrol et
        last_request = DelphoiRequest.objects.filter(
            user=user,
            question=question
        ).select_for_update().order_by('-requested_at').first()

        if last_request and (now - last_request.requested_at) < timedelta(seconds=24):
            # Hala süresi dolmadıysa, ana sayfaya bekleme zamanı ile dön
            wait_until = last_request.requested_at + timedelta(seconds=24)
            return redirect(f"{request.build_absolute_uri('/delphoi/')}?wait_until={wait_until.isoformat()}")

        # Rastgele prophecy seçimi (veritabanı seviyesinde)
        prophecy = DelphoiProphecy.objects.filter(question=question).order_by('?').first()
        if not prophecy:
            prophecy_result = "Henüz bir kehanet yok."
        else:
            prophecy_result = prophecy.text

        # Kullanıcıya yeni request kaydı aç
        DelphoiRequest.objects.create(user=user, question=question)

    # Sonucu ana sayfaya querystring ile dön
    return redirect(f"{request.build_absolute_uri('/delphoi/')}?prophecy_result={prophecy_result}")
