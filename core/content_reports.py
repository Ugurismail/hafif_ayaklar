from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Q

from .models import ContentReport, Notification


def can_manage_reports(user):
    return user.is_authenticated and user.is_active and (user.is_staff or user.is_superuser)


@transaction.atomic
def save_content_report(reporter, obj, reason, details):
    report, created = ContentReport.objects.get_or_create(
        reporter=reporter, content_type=ContentType.objects.get_for_model(obj),
        object_id=obj.pk, defaults={'reason': reason, 'details': details[:2000]},
    )
    # Serialize repeat submissions and reviews against the same report.
    report = ContentReport.objects.select_for_update().get(pk=report.pk)
    reopened = not created and report.status != 'open'
    if not created and (reopened or report.reason != reason or report.details != details[:2000]):
        report.reason = reason
        report.details = details[:2000]
        report.status = 'open'
        report.reviewed_by = None
        report.reviewed_at = None
        report.resolution_note = ''
        report.save(update_fields=[
            'reason', 'details', 'status', 'reviewed_by', 'reviewed_at',
            'resolution_note', 'updated_at',
        ])
    if created or reopened:
        managers = get_user_model().objects.filter(
            Q(is_staff=True) | Q(is_superuser=True), is_active=True,
        ).values_list('pk', flat=True)
        # Keep private report text out of notification previews.
        message = f'İçerik raporu #{report.pk} ' + ('yeniden açıldı.' if reopened else 'inceleme bekliyor.')
        Notification.objects.bulk_create([
            Notification(recipient_id=pk, notification_type='content_report',
                         related_report=report, message=message)
            for pk in managers
        ])
    return report, created
