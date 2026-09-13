"""Shared quota reservation for both invitation creation interfaces."""

from django.db import transaction
from django.db.models import F

from .models import Invitation, UserProfile


MAX_INVITATION_GRANT = 2147483647


def issue_invitation(sender, quota_granted):
    if type(quota_granted) is not int or not 1 <= quota_granted <= MAX_INVITATION_GRANT:
        raise ValueError('Invalid invitation grant')

    with transaction.atomic():
        # The conditional write reserves quota without trusting a stale profile.
        reserved = UserProfile.objects.filter(
            user_id=sender.pk, invitation_quota__gte=quota_granted,
        ).update(invitation_quota=F('invitation_quota') - quota_granted)
        if not reserved:
            return None
        return Invitation.objects.create(sender=sender, quota_granted=quota_granted)
