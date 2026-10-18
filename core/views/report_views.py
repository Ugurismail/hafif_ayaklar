from functools import wraps

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode, url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from ..content_reports import can_manage_reports, save_content_report
from ..models import Answer, ContentReport, Notification, Question


@login_required
def report_content(request):
    content_type = request.GET.get('content_type') or request.POST.get('content_type')
    object_id = request.GET.get('object_id') or request.POST.get('object_id')
    next_url = request.GET.get('next') or request.POST.get('next') or reverse('user_homepage')
    if not url_has_allowed_host_and_scheme(
        next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure(),
    ):
        next_url = reverse('user_homepage')

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
            return redirect(request.path + '?' + urlencode({
                'content_type': content_type, 'object_id': object_id, 'next': next_url,
            }))

        report, created = save_content_report(request.user, obj, reason, details)
        if not created:
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

    save_content_report(request.user, obj, reason, details)
    return JsonResponse({'status': 'ok', 'message': 'Rapor kaydedildi.'})


def report_manager_required(view):
    @login_required
    @never_cache
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if not can_manage_reports(request.user):
            response = HttpResponseForbidden('Bu sayfaya erişim yetkiniz yok.')
        else:
            response = view(request, *args, **kwargs)
        response['X-Robots-Tag'] = 'noindex, nofollow'
        return response
    return wrapped


class ReportReviewForm(forms.Form):
    status = forms.ChoiceField(label='Durum', choices=ContentReport.STATUS_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-select'}))
    resolution_note = forms.CharField(label='İnceleme notu', required=False, max_length=2000,
                                     widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    version = forms.CharField(widget=forms.HiddenInput)


@report_manager_required
@require_http_methods(['GET'])
def report_inbox(request):
    status = request.GET.get('status', 'open')
    if status not in dict(ContentReport.STATUS_CHOICES) and status != 'all':
        status = 'open'
    reports = ContentReport.objects.select_related('reporter', 'reviewed_by', 'content_type')
    counts = dict(ContentReport.objects.values('status').annotate(total=Count('pk')).values_list('status', 'total'))
    if status != 'all':
        reports = reports.filter(status=status)
    page = Paginator(reports.order_by('-updated_at', '-pk'), 25).get_page(request.GET.get('page'))
    return render(request, 'core/report_inbox.html', {
        'reports': page, 'current_status': status,
        'status_tabs': [(key, label, counts.get(key, 0)) for key, label in ContentReport.STATUS_CHOICES]
                       + [('all', 'Tümü', sum(counts.values()))],
    })


@report_manager_required
@require_http_methods(['GET', 'POST'])
def report_review(request, pk):
    report = get_object_or_404(ContentReport.objects.select_related('reporter', 'reviewed_by', 'content_type'), pk=pk)
    form = ReportReviewForm(request.POST if request.method == 'POST' else None, initial={
        'status': report.status, 'resolution_note': report.resolution_note, 'version': report.updated_at.isoformat(),
    })
    response_status = 200
    if request.method == 'POST':
        if form.is_valid():
            with transaction.atomic():
                report = get_object_or_404(ContentReport.objects.select_for_update(), pk=pk)
                if form.cleaned_data['version'] != report.updated_at.isoformat():
                    form.add_error(None, 'Rapor bu sırada değişti. Sayfayı yenileyip güncel kaydı inceleyin.')
                    response_status = 409
                else:
                    report.status = form.cleaned_data['status']
                    report.resolution_note = form.cleaned_data['resolution_note']
                    report.reviewed_by = request.user
                    report.reviewed_at = timezone.now()
                    report.save(update_fields=['status', 'resolution_note', 'reviewed_by', 'reviewed_at', 'updated_at'])
                    Notification.objects.filter(recipient=request.user, related_report=report, is_read=False).update(is_read=True)
                    messages.success(request, 'İnceleme kaydedildi.')
                    return redirect('report_review', pk=report.pk)
        else:
            response_status = 400
    obj = report.content_object
    target_url = None
    title = None
    excerpt = None
    if isinstance(obj, Answer):
        title = obj.question.question_text
        excerpt = obj.answer_text[:4000]
        target_url = reverse('entry_permalink', args=[obj.pk])
    elif isinstance(obj, Question):
        title = obj.question_text
        target_url = reverse('question_detail', args=[obj.slug])
    return render(request, 'core/report_review.html', {
        'report': report, 'form': form, 'target_url': target_url,
        'content_title': title, 'content_excerpt': excerpt,
    }, status=response_status)
