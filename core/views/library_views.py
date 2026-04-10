"""File library related views."""

import os
from uuid import uuid4

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.files.storage import default_storage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from PIL import Image, UnidentifiedImageError

from ..forms import LibraryFileForm
from ..models import LibraryFile

ALLOWED_EDITOR_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
ALLOWED_EDITOR_IMAGE_MIME_TYPES = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}
MAX_EDITOR_IMAGE_SIZE = 5 * 1024 * 1024


@login_required
def file_library(request):
    query = request.GET.get('q', '').strip()
    profile = getattr(request.user, 'userprofile', None)
    can_upload = bool(getattr(profile, 'can_upload_files', False) or request.user.is_superuser)

    form = None
    if request.method == 'POST':
        if not can_upload:
            raise PermissionDenied("Dosya yukleme yetkiniz yok.")
        form = LibraryFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.uploaded_by = request.user
            new_file.save()
            messages.success(request, "Dosya yuklendi.")
            return redirect('file_library')
    elif can_upload:
        form = LibraryFileForm()

    return render(request, 'core/file_library.html', {
        'form': form,
        'can_upload': can_upload,
        'query': query,
    })


@login_required
@require_POST
def upload_editor_image(request):
    image_file = request.FILES.get('image')
    if not image_file:
        return JsonResponse({'error': 'Gorsel dosyasi bulunamadi.'}, status=400)

    if image_file.size > MAX_EDITOR_IMAGE_SIZE:
        return JsonResponse({'error': 'Dosya boyutu 5 MB sinirini asiyor.'}, status=400)

    extension = os.path.splitext(image_file.name or '')[1].lower()
    if extension not in ALLOWED_EDITOR_IMAGE_EXTENSIONS:
        return JsonResponse({'error': 'Sadece PNG, JPG, GIF veya WEBP desteklenir.'}, status=400)

    content_type = (getattr(image_file, 'content_type', '') or '').lower()
    if content_type and content_type not in ALLOWED_EDITOR_IMAGE_MIME_TYPES:
        return JsonResponse({'error': 'Desteklenmeyen dosya turu.'}, status=400)

    try:
        image_file.seek(0)
        with Image.open(image_file) as img:
            img.verify()
        image_file.seek(0)
    except (UnidentifiedImageError, OSError):
        return JsonResponse({'error': 'Gecersiz gorsel dosyasi.'}, status=400)

    subdir = now().strftime('editor_images/%Y/%m')
    filename = f'{uuid4().hex}{extension}'
    saved_path = default_storage.save(f'{subdir}/{filename}', image_file)

    return JsonResponse({
        'ok': True,
        'file_url': default_storage.url(saved_path),
    })


@login_required
def file_library_search(request):
    query = request.GET.get('q', '').strip()
    limit_param = request.GET.get('limit')
    if limit_param is None:
        limit = 10 if not query else 20
    else:
        try:
            limit = int(limit_param)
        except ValueError:
            limit = 12 if not query else 20

    limit = max(1, min(limit, 50))

    files_qs = LibraryFile.objects.select_related('uploaded_by').order_by('-uploaded_at')
    if query:
        files_qs = files_qs.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(file__icontains=query)
            | Q(uploaded_by__username__icontains=query)
        )

    total_count = files_qs.count()
    files_qs = files_qs[:limit]

    results = []
    for item in files_qs:
        results.append({
            'id': item.id,
            'title': item.title,
            'description': item.description,
            'filename': item.filename(),
            'size': item.human_size(),
            'uploaded_by': item.uploaded_by.username,
            'uploaded_at': item.uploaded_at.strftime('%d.%m.%Y %H:%M'),
            'file_url': item.file.url,
        })

    return JsonResponse({
        'results': results,
        'count': total_count,
        'shown': len(results),
        'query': query,
        'label': 'Son yuklenenler' if not query else 'Arama sonuclari',
    })


@login_required
def file_library_list(request):
    limit_param = request.GET.get('limit')
    offset_param = request.GET.get('offset')
    mine_param = request.GET.get('mine', '0')

    try:
        limit = int(limit_param) if limit_param is not None else 20
    except ValueError:
        limit = 20
    try:
        offset = int(offset_param) if offset_param is not None else 0
    except ValueError:
        offset = 0

    limit = max(1, min(limit, 50))
    offset = max(0, offset)
    only_mine = mine_param == '1'

    files_qs = LibraryFile.objects.select_related('uploaded_by').order_by('-uploaded_at')
    if only_mine:
        files_qs = files_qs.filter(uploaded_by=request.user)

    total_count = files_qs.count()
    files_qs = files_qs[offset:offset + limit]

    results = []
    for item in files_qs:
        results.append({
            'id': item.id,
            'title': item.title,
            'description': item.description,
            'filename': item.filename(),
            'size': item.human_size(),
            'uploaded_by': item.uploaded_by.username,
            'uploaded_at': item.uploaded_at.strftime('%d.%m.%Y %H:%M'),
            'file_url': item.file.url,
            'can_delete': request.user.is_superuser or item.uploaded_by_id == request.user.id,
        })

    return JsonResponse({
        'results': results,
        'count': total_count,
        'shown': len(results),
        'offset': offset,
        'limit': limit,
        'mine': only_mine,
        'has_more': offset + len(results) < total_count,
        'label': 'Benim dosyalarim' if only_mine else 'Tum dosyalar',
    })


@login_required
@require_POST
def file_library_delete(request, file_id):
    file_obj = get_object_or_404(LibraryFile, pk=file_id)
    if not (request.user.is_superuser or file_obj.uploaded_by_id == request.user.id):
        raise PermissionDenied("Bu dosyayi silme yetkiniz yok.")

    file_obj.file.delete(save=False)
    file_obj.delete()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'ok': True})

    messages.success(request, "Dosya silindi.")
    return redirect('file_library')
