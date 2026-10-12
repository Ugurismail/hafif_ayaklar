"""Shared quota reservation for both invitation creation interfaces."""

from django.db import transaction
from django.db.models import F

from .models import Invitation, InvitationTransfer, Notification, UserProfile


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


def transfer_invitation_quota(sender, recipient, amount, transfer_id):
    if type(amount) is not int or not 1 <= amount <= MAX_INVITATION_GRANT:
        raise ValueError('Geçerli bir hak sayısı girin.')
    if sender.pk == recipient.pk:
        raise ValueError('Kendinize davet hakkı aktaramazsınız.')

    with transaction.atomic():
        # A fixed lock order also protects opposite-direction transfers from deadlocks.
        profiles = {
            p.user_id: p for p in UserProfile.objects.select_for_update()
            .filter(user_id__in=[sender.pk, recipient.pk]).order_by('user_id')
        }
        previous = InvitationTransfer.objects.filter(pk=transfer_id).first()
        if previous:
            if (previous.sender_id, previous.recipient_id, previous.amount) != (sender.pk, recipient.pk, amount):
                raise ValueError('Bu işlem daha önce farklı bilgilerle kullanıldı. Sayfayı yenileyin.')
            return previous, False
        if len(profiles) != 2 or not recipient.is_active:
            raise ValueError('Aktarım yapılabilecek bir kullanıcı bulunamadı.')
        if profiles[sender.pk].invitation_quota < amount:
            raise ValueError('Yeterli davet hakkınız yok.')
        if profiles[recipient.pk].invitation_quota > MAX_INVITATION_GRANT - amount:
            raise ValueError('Alıcının davet hakkı sınırı aşılacak.')
        UserProfile.objects.filter(user_id=sender.pk).update(invitation_quota=F('invitation_quota') - amount)
        UserProfile.objects.filter(user_id=recipient.pk).update(invitation_quota=F('invitation_quota') + amount)
        transfer = InvitationTransfer.objects.create(id=transfer_id, sender=sender, recipient=recipient, amount=amount)
        Notification.objects.create(
            recipient=recipient, sender=sender, notification_type='system',
            message=f'{sender.username} sana {amount} davet hakkı aktardı.',
        )
        return transfer, True
