"""
Authentication and invitation views
- signup
- user_login
- user_logout
- send_invitation
- create_invitation
"""

import uuid
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect

from ..models import Invitation, UserProfile
from ..forms import SignupForm, LoginForm, InvitationForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            invitation_code = form.cleaned_data['invitation_code']
            try:
                # Kodun geçerli bir UUID olup olmadığını kontrol et
                from django.core.exceptions import ValidationError
                code_uuid = uuid.UUID(str(invitation_code))
                invitation = Invitation.objects.get(code=code_uuid, is_used=False)
            except (ValueError, ValidationError, Invitation.DoesNotExist):
                messages.error(request, 'Geçersiz veya kullanılmış davetiye kodu.')
                return render(request, 'core/signup.html', {'form': form})

            user = form.save()
            # Kullanıcıya profil oluştur
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            if user.is_superuser:
                user_profile.invitation_quota = 999999999
            user_profile.invitation_quota += invitation.quota_granted
            user_profile.save()

            # Davetiyeyi kullanılmış yap
            invitation.is_used = True
            invitation.used_by = user
            invitation.save()

            login(request, user)
            return redirect('user_homepage')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user_homepage')
        else:
            messages.error(request, "Kullanıcı adı veya şifre hatalı.")
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('user_homepage')


@login_required
def send_invitation(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            quota_granted = form.cleaned_data['quota_granted']
            if user_profile.invitation_quota >= quota_granted:
                with transaction.atomic():
                    # Davet kodunu oluştur
                    invitation = form.save(commit=False)
                    invitation.sender = request.user
                    invitation.quota_granted = quota_granted
                    invitation.save()

                    # Kullanıcının davet hakkını düşür
                    user_profile.invitation_quota -= quota_granted
                    user_profile.save()

                # Oluşturulan kodu ve güncel davet hakkını şablona aktar
                return render(request, 'core/send_invitation.html', {
                    'form': InvitationForm(),  # Yeni davetler için boş form
                    'invitation_code': invitation.code,
                    'quota_granted': quota_granted,
                    'invitation_quota': user_profile.invitation_quota,
                })
            else:
                messages.error(request, 'Yeterli davet hakkınız yok.')
    else:
        form = InvitationForm()

    return render(request, 'core/send_invitation.html', {
        'form': form,
        'invitation_quota': user_profile.invitation_quota,
    })


@login_required
def create_invitation(request):
    """Redirect to profile page with invitations tab"""
    return redirect(f'/profile/{request.user.username}/?tab=davetler')
