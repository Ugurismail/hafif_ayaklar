import uuid

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import signing
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from ..invitations import MAX_INVITATION_GRANT, cancel_invitation, transfer_invitation_quota
from ..models import Invitation, InvitationTransfer, UserProfile


TOKEN_SALT = 'invitation-quota-transfer'


class InvitationTransferForm(forms.Form):
    username = forms.CharField(label='Alıcı kullanıcı adı', max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    amount = forms.IntegerField(label='Aktarılacak hak', min_value=1, max_value=MAX_INVITATION_GRANT,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'inputmode': 'numeric'}))
    token = forms.CharField(widget=forms.HiddenInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            self.recipient = User.objects.get(username=username, is_active=True)
        except User.DoesNotExist:
            raise forms.ValidationError('Bu kullanıcı bulunamadı. Kullanıcı adını kontrol edin.')
        return username


@login_required
@never_cache
@require_http_methods(['GET', 'POST'])
def invitation_transfer(request):
    token = signing.dumps({'sender': request.user.pk, 'id': str(uuid.uuid4())}, salt=TOKEN_SALT)
    form = InvitationTransferForm(request.POST if request.method == 'POST' else None,
        initial={'amount': 1, 'token': token, 'username': request.GET.get('recipient', '')[:150]})
    if request.method == 'POST' and form.is_valid():
        try:
            payload = signing.loads(form.cleaned_data['token'], salt=TOKEN_SALT, max_age=3600)
            if payload['sender'] != request.user.pk:
                raise signing.BadSignature()
            transfer_id = uuid.UUID(payload['id'])
        except (signing.BadSignature, KeyError, ValueError, TypeError):
            form.add_error(None, 'İşlem süresi doldu veya doğrulanamadı. Sayfayı yenileyin.')
        else:
            try:
                transfer, created = transfer_invitation_quota(
                    request.user, form.recipient, form.cleaned_data['amount'], transfer_id,
                )
            except ValueError as exc:
                form.add_error(None, str(exc))
            else:
                if created:
                    messages.success(request, f'{transfer.recipient.username} kullanıcısına {transfer.amount} davet hakkı aktarıldı.')
                else:
                    messages.info(request, 'Bu aktarım zaten tamamlandı; tekrar hak düşülmedi.')
                return redirect('invitation_transfer')

    history = InvitationTransfer.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).select_related('sender', 'recipient')[:30]
    return render(request, 'core/invitation_transfer.html', {
        'form': form, 'transfers': history,
        'invitation_quota': UserProfile.objects.get(user=request.user).invitation_quota,
    })


@login_required
@never_cache
@require_http_methods(['GET', 'POST'])
def invitation_cancel(request, code):
    invitation = get_object_or_404(Invitation, code=code, sender=request.user)
    error = None
    if request.method == 'POST':
        try:
            invitation, cancelled = cancel_invitation(request.user, code)
        except Invitation.DoesNotExist:
            raise Http404
        except ValueError as exc:
            error = str(exc)
        else:
            if cancelled:
                messages.success(request, f'Davet iptal edildi. {invitation.quota_granted} davet hakkı bakiyene döndü.')
            else:
                messages.info(request, 'Bu davet zaten iptal edilmiş; ikinci kez hak eklenmedi.')
            return redirect(reverse('user_profile', args=[request.user.username]) + '?tab=davetler')
    return render(request, 'core/invitation_cancel.html', {
        'invitation': invitation, 'error': error,
    }, status=400 if error else 200)
