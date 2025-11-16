"""
Radio views
- Program list (all, live, upcoming)
- DJ program management (create, edit, delete)
- Start/stop broadcast
- Listen to broadcast
"""

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.core.exceptions import ValidationError, PermissionDenied
from django.db.models import Q
from datetime import timedelta
import uuid
import os

from ..models import RadioProgram, UserProfile


def radio_home(request):
    """
    Radyo ana sayfası - tüm programları listeler
    Canlı yayınlar, yaklaşan programlar ve geçmiş programlar
    """
    now = timezone.now()

    # Canlı yayınlar
    live_programs = RadioProgram.objects.filter(
        is_live=True,
        is_finished=False
    ).select_related('dj', 'dj__userprofile').order_by('-start_time')

    # Yaklaşan programlar (gelecek 7 gün)
    upcoming_programs = RadioProgram.objects.filter(
        start_time__gt=now,
        start_time__lte=now + timedelta(days=7),
        is_finished=False
    ).select_related('dj', 'dj__userprofile').order_by('start_time')[:10]

    # Geçmiş programlar (son 7 gün)
    past_programs = RadioProgram.objects.filter(
        Q(is_finished=True) | Q(end_time__lt=now),
        start_time__gte=now - timedelta(days=7)
    ).select_related('dj', 'dj__userprofile').order_by('-start_time')[:10]

    context = {
        'live_programs': live_programs,
        'upcoming_programs': upcoming_programs,
        'past_programs': past_programs,
    }

    return render(request, 'core/radio_home.html', context)


def program_detail(request, program_id):
    """
    Program detay sayfası - dinleme sayfası
    """
    program = get_object_or_404(
        RadioProgram.objects.select_related('dj', 'dj__userprofile'),
        id=program_id
    )

    # Eğer program canlı değilse sadece bilgi göster
    context = {
        'program': program,
    }

    return render(request, 'core/radio_program_detail.html', context)


@login_required
def dj_dashboard(request):
    """
    DJ kontrol paneli - DJ'nin kendi programlarını gösterir
    """
    # DJ kontrolü
    try:
        user_profile = request.user.userprofile
        if not user_profile.is_dj:
            messages.error(request, 'DJ yetkisine sahip değilsiniz.')
            return redirect('radio_home')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profil bulunamadı.')
        return redirect('radio_home')

    now = timezone.now()

    # DJ'nin programları
    live_programs = RadioProgram.objects.filter(
        dj=request.user,
        is_live=True,
        is_finished=False
    ).order_by('-start_time')

    # Başlamaya hazır programlar (zamanı geldi ama henüz başlatılmamış)
    ready_programs = RadioProgram.objects.filter(
        dj=request.user,
        start_time__lte=now,
        end_time__gt=now,
        is_live=False,
        is_finished=False
    ).order_by('start_time')

    upcoming_programs = RadioProgram.objects.filter(
        dj=request.user,
        start_time__gt=now,
        is_finished=False
    ).order_by('start_time')

    past_programs = RadioProgram.objects.filter(
        dj=request.user,
        is_finished=True
    ).order_by('-start_time')[:10]

    context = {
        'live_programs': live_programs,
        'ready_programs': ready_programs,
        'upcoming_programs': upcoming_programs,
        'past_programs': past_programs,
    }

    return render(request, 'core/dj_dashboard.html', context)


@login_required
def create_program(request):
    """
    DJ program oluşturma
    """
    # DJ kontrolü
    try:
        user_profile = request.user.userprofile
        if not user_profile.is_dj:
            messages.error(request, 'DJ yetkisine sahip değilsiniz.')
            return redirect('radio_home')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profil bulunamadı.')
        return redirect('radio_home')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')

        # Validasyon
        if not title or not start_time_str or not end_time_str:
            messages.error(request, 'Lütfen tüm gerekli alanları doldurun.')
            return redirect('create_program')

        try:
            # Tarih parse etme
            from django.utils.dateparse import parse_datetime
            start_time = parse_datetime(start_time_str)
            end_time = parse_datetime(end_time_str)

            if not start_time or not end_time:
                messages.error(request, 'Geçersiz tarih formatı.')
                return redirect('create_program')

            # Program oluştur
            program = RadioProgram(
                dj=request.user,
                title=title,
                description=description,
                start_time=start_time,
                end_time=end_time
            )

            # Validasyon (clean method çalıştırılır - çakışma kontrolü)
            program.full_clean()
            program.save()

            messages.success(request, 'Program başarıyla oluşturuldu.')
            return redirect('dj_dashboard')

        except ValidationError as e:
            messages.error(request, f'Hata: {", ".join(e.messages)}')
            return redirect('create_program')
        except Exception as e:
            messages.error(request, f'Beklenmeyen hata: {str(e)}')
            return redirect('create_program')

    return render(request, 'core/create_program.html')


@login_required
def edit_program(request, program_id):
    """
    Program düzenleme
    """
    program = get_object_or_404(RadioProgram, id=program_id)

    # Yetki kontrolü - sadece program sahibi veya admin düzenleyebilir
    if program.dj != request.user and not request.user.is_staff:
        raise PermissionDenied("Bu programı düzenleme yetkiniz yok.")

    # Canlı veya bitmiş program düzenlenemez
    if program.is_live or program.is_finished:
        messages.error(request, 'Canlı veya bitmiş program düzenlenemez.')
        return redirect('dj_dashboard')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')

        if not title or not start_time_str or not end_time_str:
            messages.error(request, 'Lütfen tüm gerekli alanları doldurun.')
            return redirect('edit_program', program_id=program_id)

        try:
            from django.utils.dateparse import parse_datetime
            start_time = parse_datetime(start_time_str)
            end_time = parse_datetime(end_time_str)

            if not start_time or not end_time:
                messages.error(request, 'Geçersiz tarih formatı.')
                return redirect('edit_program', program_id=program_id)

            program.title = title
            program.description = description
            program.start_time = start_time
            program.end_time = end_time

            program.full_clean()
            program.save()

            messages.success(request, 'Program başarıyla güncellendi.')
            return redirect('dj_dashboard')

        except ValidationError as e:
            messages.error(request, f'Hata: {", ".join(e.messages)}')
            return redirect('edit_program', program_id=program_id)
        except Exception as e:
            messages.error(request, f'Beklenmeyen hata: {str(e)}')
            return redirect('edit_program', program_id=program_id)

    context = {
        'program': program,
    }
    return render(request, 'core/edit_program.html', context)


@login_required
def delete_program(request, program_id):
    """
    Program silme
    """
    program = get_object_or_404(RadioProgram, id=program_id)

    # Yetki kontrolü
    if program.dj != request.user and not request.user.is_staff:
        raise PermissionDenied("Bu programı silme yetkiniz yok.")

    # Canlı program silinemez
    if program.is_live:
        messages.error(request, 'Canlı program silinemez. Önce yayını bitirin.')
        return redirect('dj_dashboard')

    if request.method == 'POST':
        program.delete()
        messages.success(request, 'Program başarıyla silindi.')
        return redirect('dj_dashboard')

    context = {
        'program': program,
    }
    return render(request, 'core/delete_program.html', context)


@login_required
def start_broadcast(request, program_id):
    """
    Yayın başlatma - AJAX
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    program = get_object_or_404(RadioProgram, id=program_id)

    # Yetki kontrolü
    if program.dj != request.user:
        return JsonResponse({'error': 'Bu yayını başlatma yetkiniz yok.'}, status=403)

    # Zaten canlı mı kontrol et
    if program.is_live:
        return JsonResponse({'error': 'Program zaten canlı.'}, status=400)

    # Bitmiş mi kontrol et
    if program.is_finished:
        return JsonResponse({'error': 'Bitmiş program tekrar başlatılamaz.'}, status=400)

    # Başka canlı yayın var mı kontrol et (conflict check)
    existing_live = RadioProgram.objects.filter(is_live=True, is_finished=False).exists()
    if existing_live:
        return JsonResponse({'error': 'Şu anda başka bir canlı yayın var.'}, status=400)

    # Yayını başlat
    program.is_live = True
    program.save()

    return JsonResponse({
        'success': True,
        'message': 'Yayın başlatıldı!',
        'agora_channel_name': program.agora_channel_name
    })


@login_required
def stop_broadcast(request, program_id):
    """
    Yayın bitirme - AJAX
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    program = get_object_or_404(RadioProgram, id=program_id)

    # Yetki kontrolü
    if program.dj != request.user and not request.user.is_staff:
        return JsonResponse({'error': 'Bu yayını bitirme yetkiniz yok.'}, status=403)

    # Canlı mı kontrol et
    if not program.is_live:
        return JsonResponse({'error': 'Program canlı değil.'}, status=400)

    # Yayını bitir
    program.is_live = False
    program.is_finished = True
    program.save()

    return JsonResponse({
        'success': True,
        'message': 'Yayın sonlandırıldı!'
    })


@login_required
def get_agora_token(request, program_id):
    """
    Agora.io token alma - AJAX
    DJ için broadcaster token, dinleyici için audience token
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    program = get_object_or_404(RadioProgram, id=program_id)

    # Program canlı mı kontrol et
    if not program.is_live:
        return JsonResponse({'error': 'Program şu anda canlı değil.'}, status=400)

    # DJ mi dinleyici mi kontrol et
    is_broadcaster = (program.dj == request.user)

    # Agora token generation
    try:
        from ..agora_token import generate_dj_token, generate_listener_token, is_agora_configured

        if not is_agora_configured():
            return JsonResponse({
                'error': 'Agora.io yapılandırması eksik. Lütfen AGORA_APP_ID ve AGORA_APP_CERTIFICATE ayarlayın.'
            }, status=500)

        # Generate appropriate token based on role
        if is_broadcaster:
            token = generate_dj_token(program.agora_channel_name, request.user.id)
        else:
            token = generate_listener_token(program.agora_channel_name, request.user.id)

        return JsonResponse({
            'success': True,
            'channel_name': program.agora_channel_name,
            'token': token,
            'uid': request.user.id,
            'role': 'broadcaster' if is_broadcaster else 'audience',
            'app_id': os.environ.get('AGORA_APP_ID')
        })

    except ImportError as e:
        return JsonResponse({
            'error': 'Agora token paketi kurulu değil. Lütfen: pip install agora-token'
        }, status=500)
    except Exception as e:
        return JsonResponse({
            'error': f'Token oluşturulurken hata: {str(e)}'
        }, status=500)


def update_listener_count(request, program_id):
    """
    Dinleyici sayısını güncelleme - AJAX
    Frontend Agora SDK'den gerçek dinleyici sayısını gönderir
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    program = get_object_or_404(RadioProgram, id=program_id)

    # Get listener count from request body
    try:
        import json
        data = json.loads(request.body)
        count = data.get('count', 0)

        # Update program's listener count
        program.listener_count = count

        # Update max_listeners if this is higher
        if count > program.max_listeners:
            program.max_listeners = count

        program.save()
    except (json.JSONDecodeError, KeyError):
        # If no count provided, just return current count
        pass

    return JsonResponse({
        'success': True,
        'listener_count': program.listener_count
    })
