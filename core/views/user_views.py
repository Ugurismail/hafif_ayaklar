"""
User-related views
- profile
- user_profile
- user_settings
- user_list
- follow_user
- unfollow_user
- update_profile_photo
- get_user_id
- get_user_color
- get_top_words
- get_invitation_tree
- get_user_questions
"""

import re
import colorsys
from collections import Counter

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count, Sum
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from ..models import (
    Invitation, UserProfile, Question, Answer,
    SavedItem, PinnedEntry, Definition, Reference
)
from ..forms import ProfilePhotoForm


def profile(request):
    user = request.user
    user_profile = user.userprofile

    # Kullanıcının soruları ve yanıtları
    questions = Question.objects.filter(user=user)
    answers = Answer.objects.filter(user=user)

    # Takipçi ve takip edilen sayıları
    follower_count = user_profile.followers.count()
    following_count = user_profile.following.count()

    # Sabitlenmiş giriş (pinned_entry)
    try:
        pinned_entry = PinnedEntry.objects.get(user=user)
    except PinnedEntry.DoesNotExist:
        pinned_entry = None

    # En çok kullanılan kelimeler
    top_words = get_top_words(user)

    context = {
        'profile_user': user,
        'user_profile': user_profile,
        'questions': questions,
        'answers': answers,
        'follower_count': follower_count,
        'following_count': following_count,
        'pinned_entry': pinned_entry,
        'top_words': top_words,
    }
    return redirect('user_profile', username=request.user.username)


@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    user_profile = profile_user.userprofile
    active_tab = request.GET.get('tab', 'girdiler')
    is_own_profile = (request.user == profile_user)

    # Handle invitation creation POST request
    if request.method == 'POST' and is_own_profile and active_tab == 'davetler':
        from django.db import transaction
        from ..forms import InvitationForm

        form = InvitationForm(request.POST)
        if form.is_valid():
            quota_granted = form.cleaned_data.get('quota_granted', 0)
            if user_profile.invitation_quota >= quota_granted:
                with transaction.atomic():
                    invitation = form.save(commit=False)
                    invitation.sender = request.user
                    invitation.quota_granted = quota_granted
                    invitation.save()

                    user_profile.invitation_quota -= quota_granted
                    user_profile.save()

                messages.success(request, f'Davetiye kodu oluşturuldu: {invitation.code}')
            else:
                messages.error(request, 'Yetersiz davet hakkı.')

        # Redirect to same page to prevent form resubmission
        return redirect(f'/profile/{username}/?tab=davetler')

    context = {
        'profile_user': profile_user,
        'user_profile': user_profile,
        'is_own_profile': is_own_profile,
        'active_tab': active_tab,
        'answers': None,
        'definitions_page': None,
        'references_page': None,
        'saved_items_page': None,
        'top_words': None,
        'exclude_words': None,
        'exclude_words_list': None,
        'search_word': None,
        'search_word_count': None,
    }

    # Takip ve takipçi sayısı
    context['follower_count'] = user_profile.followers.count()
    context['following_count'] = user_profile.following.count()
    context['is_following'] = (
        request.user.is_authenticated and
        request.user != profile_user and
        request.user.userprofile.following.filter(user=profile_user).exists()
    )

    # Sabitlenmiş entry
    try:
        context['pinned_entry'] = PinnedEntry.objects.select_related('answer__question').get(user=profile_user)
    except PinnedEntry.DoesNotExist:
        context['pinned_entry'] = None

    # Sadece ilgili sekmenin contextini doldur
    if active_tab == 'girdiler':
        answers_list = Answer.objects.filter(user=profile_user).select_related('question', 'user').order_by('-created_at')
        answer_paginator = Paginator(answers_list, 10)
        answer_page = request.GET.get('answer_page', 1)
        try:
            context['answers'] = answer_paginator.page(answer_page)
        except (PageNotAnInteger, EmptyPage):
            context['answers'] = answer_paginator.page(1)

    elif active_tab == 'tanimlar':
        definitions_qs = Definition.objects.filter(user=profile_user).select_related('question')
        search_query = request.GET.get('q', '').strip()
        if search_query:
            definitions_qs = definitions_qs.filter(
                Q(definition_text__icontains=search_query) |
                Q(question__question_text__icontains=search_query)
            )
        def_paginator = Paginator(definitions_qs, 5)
        def_page = request.GET.get('d_page', 1)
        try:
            context['definitions_page'] = def_paginator.page(def_page)
        except (PageNotAnInteger, EmptyPage):
            context['definitions_page'] = def_paginator.page(1)

    elif active_tab == 'kaynaklarim':
        user_references = Reference.objects.filter(created_by=profile_user)
        search_query = request.GET.get('q', '').strip()
        if search_query:
            user_references = user_references.filter(
                Q(author_surname__icontains=search_query) |
                Q(author_name__icontains=search_query) |
                Q(rest__icontains=search_query) |
                Q(abbreviation__icontains=search_query)
            )
        ref_paginator = Paginator(user_references, 5)
        r_page = request.GET.get('r_page', 1)
        try:
            context['references_page'] = ref_paginator.page(r_page)
        except (PageNotAnInteger, EmptyPage):
            context['references_page'] = ref_paginator.page(1)

    elif active_tab == 'kaydedilenler' and is_own_profile:
        question_ct = ContentType.objects.get_for_model(Question)
        answer_ct = ContentType.objects.get_for_model(Answer)

        user_saved = SavedItem.objects.filter(user=profile_user).order_by('-saved_at')
        question_ids = [si.object_id for si in user_saved if si.content_type_id == question_ct.id]
        answer_ids = [si.object_id for si in user_saved if si.content_type_id == answer_ct.id]
        question_map = {q.id: q for q in Question.objects.filter(id__in=question_ids)}
        answer_map = {a.id: a for a in Answer.objects.select_related('question').filter(id__in=answer_ids)}

        saved_items_list = []
        for item in user_saved:
            if item.content_type_id == question_ct.id:
                obj = question_map.get(item.object_id)
                if obj:
                    saved_items_list.append({'type': 'question', 'object': obj})
            elif item.content_type_id == answer_ct.id:
                obj = answer_map.get(item.object_id)
                if obj:
                    saved_items_list.append({'type': 'answer', 'object': obj})

        s_page = request.GET.get('s_page', 1)
        saved_paginator = Paginator(saved_items_list, 5)
        try:
            context['saved_items_page'] = saved_paginator.page(s_page)
        except (PageNotAnInteger, EmptyPage):
            context['saved_items_page'] = saved_paginator.page(1)

    elif active_tab in ['istatistikler', 'kelimeler']:
        questions_list = Question.objects.filter(user=profile_user)
        answers_list = Answer.objects.filter(user=profile_user)
        question_texts = list(questions_list.values_list('question_text', flat=True))
        answer_texts = list(answers_list.values_list('answer_text', flat=True))
        all_entries = [q for q in question_texts if q] + [a for a in answer_texts if a]
        total_words = sum(len(re.findall(r'\b\w+\b', entry)) for entry in all_entries)
        total_chars = sum(len(entry.replace(" ", "")) for entry in all_entries)
        total_entries = len(all_entries)
        avg_words_per_entry = total_words / total_entries if total_entries else 0
        all_texts_joined = (' '.join(question_texts) + ' ' + ' '.join(answer_texts)).lower()
        words = re.findall(r'\b\w+\b', all_texts_joined)
        exclude_words_str = request.GET.get('exclude_words', '')
        exclude_words_list = [w.strip() for w in exclude_words_str.split(',') if w.strip()]
        exclude_words_set = set(word.lower() for word in exclude_words_list)
        exclude_word = request.GET.get('exclude_word', '').strip().lower()
        total_upvotes = ((questions_list.aggregate(total=Sum('upvotes'))['total'] or 0) +
                 (answers_list.aggregate(total=Sum('upvotes'))['total'] or 0))
        total_downvotes = ((questions_list.aggregate(total=Sum('downvotes'))['total'] or 0) +
                   (answers_list.aggregate(total=Sum('downvotes'))['total'] or 0))
        if exclude_word:
            exclude_words_set.add(exclude_word)
        include_word = request.GET.get('include_word', '').strip().lower()
        if include_word and include_word in exclude_words_set:
            exclude_words_set.remove(include_word)
        exclude_words_list = sorted(list(exclude_words_set))
        exclude_words_str = ', '.join(exclude_words_list)
        filtered_words = [word for word in words if word not in exclude_words_set]
        word_counts = Counter(filtered_words)
        top_words = word_counts.most_common(20)
        search_word = request.GET.get('search_word', '').strip().lower()
        search_word_count = None
        if search_word:
            search_word_count = word_counts.get(search_word, 0)

        content_type_question = ContentType.objects.get_for_model(Question)
        content_type_answer = ContentType.objects.get_for_model(Answer)
        total_saves_questions = SavedItem.objects.filter(
            content_type=content_type_question, object_id__in=questions_list
        ).count()
        total_saves_answers = SavedItem.objects.filter(
            content_type=content_type_answer, object_id__in=answers_list
        ).count()
        total_saves = total_saves_questions + total_saves_answers

        most_upvoted_question = questions_list.order_by('-upvotes').first()
        most_upvoted_answer = answers_list.order_by('-upvotes').first()
        most_upvoted_entry = max(
            (e for e in [most_upvoted_question, most_upvoted_answer] if e),
            key=lambda x: x.upvotes,
            default=None
        )
        most_downvoted_question = questions_list.order_by('-downvotes').first()
        most_downvoted_answer = answers_list.order_by('-downvotes').first()
        most_downvoted_entry = max(
            (e for e in [most_downvoted_question, most_downvoted_answer] if e),
            key=lambda x: x.downvotes,
            default=None
        )
        most_saved_question = questions_list.annotate(save_count=Count('saveditem')).order_by('-save_count').first()
        most_saved_answer = answers_list.annotate(save_count=Count('saveditem')).order_by('-save_count').first()
        most_saved_entry = max(
            (e for e in [most_saved_question, most_saved_answer] if e),
            key=lambda x: getattr(x, 'save_count', 0),
            default=None
        )

        context.update({
            'total_words': total_words,
            'total_chars': total_chars,
            'avg_words_per_entry': round(avg_words_per_entry, 2),
            'top_words': top_words,
            'exclude_words': exclude_words_str,
            'exclude_words_list': exclude_words_list,
            'search_word': search_word,
            'search_word_count': search_word_count,
            'total_upvotes': total_upvotes,
            'total_downvotes': total_downvotes,
            'total_saves': total_saves,
            'most_upvoted_entry': most_upvoted_entry,
            'most_downvoted_entry': most_downvoted_entry,
            'most_saved_entry': most_saved_entry,
        })

    if active_tab == 'davetler' and is_own_profile:
        invitations = Invitation.objects.filter(sender=request.user).order_by('-created_at')
        total_invitations = invitations.count()
        used_invitations = invitations.filter(is_used=True).count()
        remaining_invitations = user_profile.invitation_quota - total_invitations
        context.update({
            'invitations': invitations,
            'total_invitations': total_invitations,
            'used_invitations': used_invitations,
            'remaining_invitations': remaining_invitations,
        })

    if active_tab == 'davet_aagac' and is_own_profile:
        context['invitation_tree'] = get_invitation_tree(request.user)

    return render(request, 'core/user_profile.html', context)


@login_required
def user_settings(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        if 'reset' in request.POST:
            # Varsayılan değerlere dön
            profile.background_color = '#F5F5F5'
            profile.text_color = '#000000'
            profile.header_background_color = '#F5F5F5'
            profile.header_text_color = '#333333'
            profile.link_color = '#6E8CA7'
            profile.link_hover_color = '#4E647E'
            profile.button_background_color = '#6E8CA7'
            profile.button_hover_background_color = '#4E647E'
            profile.button_text_color = '#ffffff'
            profile.hover_background_color = '#f0f0f0'
            profile.icon_color = '#333333'
            profile.icon_hover_color = '#007bff'
            profile.answer_background_color = '#F5F5F5'
            profile.content_background_color = '#ffffff'
            profile.tab_background_color = '#f8f9fa'
            profile.tab_text_color = '#000000'
            profile.tab_active_background_color = '#ffffff'
            profile.tab_active_text_color = '#000000'
            profile.dropdown_text_color = '#333333'
            profile.dropdown_hover_background_color = '#f2f2f2'
            profile.dropdown_hover_text_color = '#0056b3'
            profile.nav_link_hover_color = '#007bff'
            profile.nav_link_hover_bg = '#f5f5f5'

            #benim eklediklerim
            profile.message_bubble_color="#d1e7ff"
            profile.tbas_color="#000000"

            profile.font_size='16'

            profile.pagination_background_color = '#ffffff'
            profile.pagination_text_color = '#000000'
            # profile.pagination_active_background_color = '#007bff'
            # profile.pagination_active_text_color = '#ffffff'

            profile.cemil = '#ffffff'
            profile.yanit_card='#ffffff'
            profile.secondary_button_background_color = '#6c757d'
            profile.secondary_button_text_color = '#ffffff'
            profile.secondary_button_hover_background_color= '#495057'

            profile.font_family = 'EB Garamond'
            # Diğer renk alanlarını da varsayılan değerlere ayarlayın
            profile.save()
            messages.success(request, 'Renk ayarlarınız varsayılan değerlere döndürüldü.')
            return redirect('user_settings')
        else:
            # Formdan gelen değerleri kaydet
            profile.secondary_button_background_color = request.POST.get('secondary_button_background_color','#6c757d')
            profile.secondary_button_text_color = request.POST.get('secondary_button_text_color','#ffffff')
            profile.secondary_button_hover_background_color = request.POST.get('secondary_button_hover_background_color','#495057')

            profile.font_size = int(request.POST.get('font_size', 16))  # Sayıya çeviriyoruz

            #benim eklediklerim
            profile.message_bubble_color = request.POST.get('message_bubble_color', '#d1e7ff')
            profile.tbas_color = request.POST.get('tbas_color', '#000000')
            profile.background_color = request.POST.get('background_color', '#F5F5F5')
            profile.text_color = request.POST.get('text_color', '#000000')
            profile.header_background_color = request.POST.get('header_background_color', '#F5F5F5')
            profile.header_text_color = request.POST.get('header_text_color', '#333333')
            profile.link_color = request.POST.get('link_color', '#6E8CA7')
            profile.link_hover_color = request.POST.get('link_hover_color', '#4E647E')
            profile.button_background_color = request.POST.get('button_background_color', '#6E8CA7')
            profile.button_hover_background_color = request.POST.get('button_hover_background_color', '#4E647E')
            profile.button_text_color = request.POST.get('button_text_color', '#ffffff')
            profile.hover_background_color = request.POST.get('hover_background_color', '#f0f0f0')
            profile.icon_color = request.POST.get('icon_color', '#333333')
            profile.icon_hover_color = request.POST.get('icon_hover_color', '#007bff')
            profile.answer_background_color = request.POST.get('answer_background_color', '#F5F5F5')
            profile.content_background_color = request.POST.get('content_background_color', '#ffffff')
            profile.tab_background_color = request.POST.get('tab_background_color', '#f8f9fa')
            profile.tab_text_color = request.POST.get('tab_text_color', '#000000')
            profile.tab_active_background_color = request.POST.get('tab_active_background_color', '#ffffff')
            profile.tab_active_text_color = request.POST.get('tab_active_text_color', '#000000')
            profile.dropdown_text_color = request.POST.get('dropdown_text_color', '#333333')
            profile.dropdown_hover_background_color = request.POST.get('dropdown_hover_background_color', '#f2f2f2')
            profile.dropdown_hover_text_color = request.POST.get('dropdown_hover_text_color', '#0056b3')
            profile.nav_link_hover_color = request.POST.get('nav_link_hover_color', '#007bff')
            profile.nav_link_hover_bg = request.POST.get('nav_link_hover_bg', '#f5f5f5')

            profile.pagination_background_color = request.POST.get('pagination_background_color', '#ffffff')
            profile.pagination_text_color = request.POST.get('pagination_text_color', '#000000')
            # profile.pagination_active_background_color = request.POST.get('pagination_active_background_color', '#007bff')
            # profile.pagination_active_text_color = request.POST.get('pagination_active_text_color', '#ffffff')
            profile.yanit_card= request.POST.get('yanit_card','#ffffff')
            profile.font_family = request.POST.get('font_family', 'EB Garamond')
            # Diğer renk alanlarını da kaydedin
            profile.save()
            messages.success(request, 'Renk ayarlarınız güncellendi.')
            return redirect('user_settings')
    return render(request, 'core/user_settings.html', {'user_profile': profile})


def user_list(request):
    users = User.objects.filter(is_active=True) \
                        .exclude(id=request.user.id) \
                        .annotate(username_lower=Lower('username')) \
                        .order_by('username_lower')
    paginator = Paginator(users, 36)  # Sayfa başına 36 kullanıcı
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/user_list.html', {'users': page_obj})


@login_required
def follow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    user_profile = request.user.userprofile
    target_profile = target_user.userprofile
    user_profile.following.add(target_profile)
    return redirect('user_profile', username=username)


@login_required
def unfollow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    user_profile = request.user.userprofile
    target_profile = target_user.userprofile
    user_profile.following.remove(target_profile)
    return redirect('user_profile', username=username)


@login_required
def update_profile_photo(request):
    profile_user = request.user
    user_profile = profile_user.userprofile

    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES, instance=user_profile)
        remove_photo = (request.POST.get('remove_photo') == 'true')

        if remove_photo:
            if user_profile.photo:
                user_profile.photo.delete(save=False)
            user_profile.photo = None
            user_profile.save()
            messages.success(request, 'Fotoğrafınız kaldırıldı.')
            return redirect('user_profile', username=profile_user.username)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profil fotoğrafınız güncellendi.')
            return redirect('user_profile', username=profile_user.username)
        else:
            # Form hatalıysa modal tekrar açılsın diye user_profile.html'i tekrar render ediyoruz.
            return render(request, 'core/user_profile.html', {
                'profile_user': profile_user,
                'user_profile': user_profile,
                'form': form,
                'is_own_profile': True,  # Kendi profilimiz olduğunu varsayıyoruz
            })
    else:
        # GET isteğinde direkt profiline yönlendir
        return redirect('user_profile', username=profile_user.username)


def get_user_id(request, username):
    try:
        user = User.objects.get(username=username)
        return JsonResponse({'user_id': user.id})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


def get_user_color(user_id):
    hue = (user_id * 137.508) % 360  # Altın açı
    rgb = colorsys.hsv_to_rgb(hue / 360, 0.5, 0.95)
    hex_color = '#%02x%02x%02x' % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
    return hex_color


def get_top_words(user):
    answers = Answer.objects.filter(user=user)
    questions = Question.objects.filter(user=user)

    text = ' '.join([a.answer_text for a in answers] + [q.question_text for q in questions])
    words = re.findall(r'\w+', text.lower())
    word_counts = Counter(words)
    top_words = word_counts.most_common(10)

    return top_words


def get_invitation_tree(user):
    invitations = Invitation.objects.filter(sender=user)
    tree = []
    for invite in invitations:
        if invite.is_used and invite.used_by:
            invited_user = invite.used_by
            subtree = get_invitation_tree(invited_user)
            tree.append({'user': invited_user, 'children': subtree})
        else:
            tree.append({'code': invite.code, 'children': []})
    return tree


@login_required
def get_user_questions(request):
    username = request.GET.get('username')  # Profil sahibinin username'i
    q = request.GET.get('q', '').strip()
    user = get_object_or_404(User, username=username) if username else request.user

    questions = Question.objects.filter(user=user)
    if q:
        questions = questions.filter(question_text__icontains=q)
    data = []
    for question in questions:
        data.append({
            'id': question.id,
            'question_text': question.question_text,
            'detail_url': reverse('question_detail', args=[question.id]),
        })
    return JsonResponse({'questions': data})
