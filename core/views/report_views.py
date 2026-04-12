from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from ..models import Answer, ContentReport, Question


@login_required
def report_content(request):
    content_type = request.GET.get('content_type') or request.POST.get('content_type')
    object_id = request.GET.get('object_id') or request.POST.get('object_id')
    next_url = request.GET.get('next') or request.POST.get('next') or reverse('user_homepage')

    if content_type not in {'question', 'answer'}:
        messages.error(request, 'Raporlanacak içerik bulunamadı.')
        return redirect(next_url)

    model = Question if content_type == 'question' else Answer
    obj = get_object_or_404(model, id=object_id)

    if getattr(obj, 'user_id', None) == request.user.id:
        messages.info(request, 'Kendi içeriğini raporlayamazsın.')
        return redirect(next_url)

    if request.method == 'POST':
        reason = request.POST.get('reason', '').strip()
        details = request.POST.get('details', '').strip()
        if reason not in dict(ContentReport.REASON_CHOICES):
            messages.error(request, 'Geçerli bir rapor nedeni seç.')
            return redirect(request.path + f'?content_type={content_type}&object_id={object_id}&next={next_url}')

        content_type_obj = ContentType.objects.get_for_model(model)
        report, created = ContentReport.objects.get_or_create(
            reporter=request.user,
            content_type=content_type_obj,
            object_id=obj.id,
            defaults={
                'reason': reason,
                'details': details[:2000],
            },
        )
        if not created:
            report.reason = reason
            report.details = details[:2000]
            report.status = 'open'
            report.reviewed_by = None
            report.reviewed_at = None
            report.resolution_note = ''
            report.save(update_fields=['reason', 'details', 'status', 'reviewed_by', 'reviewed_at', 'resolution_note', 'updated_at'])
            messages.success(request, 'Rapor güncellendi.')
        else:
            messages.success(request, 'Rapor gönderildi.')
        return redirect(next_url)

    context = {
        'reported_type': content_type,
        'reported_object': obj,
        'reason_choices': ContentReport.REASON_CHOICES,
        'next_url': next_url,
    }
    return render(request, 'core/report_content.html', context)


@login_required
def report_content_ajax(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    content_type = request.POST.get('content_type', '').strip()
    object_id = request.POST.get('object_id', '').strip()
    reason = request.POST.get('reason', '').strip()
    details = request.POST.get('details', '').strip()

    if content_type not in {'question', 'answer'}:
        return JsonResponse({'error': 'Geçersiz içerik tipi.'}, status=400)
    if reason not in dict(ContentReport.REASON_CHOICES):
        return JsonResponse({'error': 'Geçerli bir neden seç.'}, status=400)

    model = Question if content_type == 'question' else Answer
    obj = get_object_or_404(model, id=object_id)
    if getattr(obj, 'user_id', None) == request.user.id:
        return JsonResponse({'error': 'Kendi içeriğini raporlayamazsın.'}, status=400)

    content_type_obj = ContentType.objects.get_for_model(model)
    report, created = ContentReport.objects.get_or_create(
        reporter=request.user,
        content_type=content_type_obj,
        object_id=obj.id,
        defaults={'reason': reason, 'details': details[:2000]},
    )
    if not created:
        report.reason = reason
        report.details = details[:2000]
        report.status = 'open'
        report.reviewed_by = None
        report.reviewed_at = None
        report.resolution_note = ''
        report.save(update_fields=['reason', 'details', 'status', 'reviewed_by', 'reviewed_at', 'resolution_note', 'updated_at'])

    return JsonResponse({'status': 'ok', 'message': 'Rapor kaydedildi.'})
