"""
Poll-related views
- polls_home
- create_poll
- vote_poll
- poll_question_redirect
- vote_poll_ajax
- poll_detail
- poll_popover_content
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.http import require_POST

from ..models import Poll, PollOption, PollVote, Question
from ..forms import PollForm


def polls_home(request):
    return render(request, 'core/polls.html', _build_polls_context(user=request.user))


def _poll_can_manage(poll, user):
    return user.is_authenticated and (user.is_superuser or poll.created_by_id == user.id)


def _build_poll_initial(poll):
    initial = {
        'question_text': poll.question_text,
        'end_date': poll.end_date.strftime('%Y-%m-%dT%H:%M'),
        'is_anonymous': poll.is_anonymous,
    }
    options = list(poll.options.order_by('id').values_list('option_text', flat=True))
    for index, option_text in enumerate(options, start=1):
        initial[f'option_{index}'] = option_text
    return initial


def _build_polls_context(user=None, form=None, open_create_poll_modal=False, edit_form=None, editing_poll=None, open_edit_poll_modal=False):
    # Aktif anketler (end_date > şu an)
    active_polls = Poll.objects.filter(end_date__gt=timezone.now()).order_by('-created_at')
    # Süresi geçmiş anketler (end_date <= şu an)
    expired_polls = Poll.objects.filter(end_date__lte=timezone.now()).order_by('-created_at')

    active_polls_data = []
    for poll in active_polls:
        total_votes = sum(opt.votes.count() for opt in poll.options.all())
        options_data = []
        for opt in poll.options.all():
            options_data.append({
                'option': opt,
                'votes': opt.votes.count(),
                'percentage': (100 * opt.votes.count() / total_votes) if total_votes > 0 else 0
            })
        active_polls_data.append({
            'poll': poll,
            'total_votes': total_votes,
            'options_data': options_data,
            'can_manage': _poll_can_manage(poll, user),
            'can_edit': _poll_can_manage(poll, user) and total_votes == 0,
        })
    # Süresi geçmiş anketler için yüzdeleri hesaplayalım
    expired_polls_data = []
    for poll in expired_polls:
        options_data = []
        total_votes = sum([opt.votes.count() for opt in poll.options.all()])
        for opt in poll.options.all():
            if total_votes > 0:
                percentage = (opt.votes.count() / total_votes) * 100
            else:
                percentage = 0
            options_data.append({
                'text': opt.option_text,
                'percentage': f"{percentage:.2f}"
            })
        expired_polls_data.append({
            'poll': poll,
            'options_data': options_data,
            'total_votes': total_votes,
            'can_manage': _poll_can_manage(poll, user),
            'can_edit': _poll_can_manage(poll, user) and total_votes == 0,
        })

    return {
        'active_polls': active_polls,
        'expired_polls_data': expired_polls_data,
        'form': form or PollForm(),
        'edit_form': edit_form,
        'editing_poll': editing_poll,
        'active_polls_data': active_polls_data,
        'open_create_poll_modal': open_create_poll_modal,
        'open_edit_poll_modal': open_edit_poll_modal,
    }


@login_required
def create_poll(request):
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data['question_text']
            end_date = form.cleaned_data['end_date']
            is_anonymous = form.cleaned_data['is_anonymous']
            options = form.cleaned_data['options']

            poll = Poll.objects.create(
                question_text=question_text,
                created_by=request.user,
                end_date=end_date,
                is_anonymous=is_anonymous
            )
            for opt_text in options:
                PollOption.objects.create(poll=poll, option_text=opt_text)

            messages.success(request, 'Anket başarıyla oluşturuldu.')
            return redirect('polls_home')
        else:
            return render(
                request,
                'core/polls.html',
                _build_polls_context(user=request.user, form=form, open_create_poll_modal=True),
            )
    else:
        return redirect('polls_home')


@login_required
def edit_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if not _poll_can_manage(poll, request.user):
        raise PermissionDenied("Bu anketi düzenleme yetkiniz yok.")

    if PollVote.objects.filter(option__poll=poll).exists():
        messages.error(request, 'Oy alınmış anketlerin seçenekleri değiştirilemez.')
        return redirect('polls_home')

    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            poll.question_text = form.cleaned_data['question_text']
            poll.end_date = form.cleaned_data['end_date']
            poll.is_anonymous = form.cleaned_data['is_anonymous']
            poll.save(update_fields=['question_text', 'end_date', 'is_anonymous'])

            poll.options.all().delete()
            for opt_text in form.cleaned_data['options']:
                PollOption.objects.create(poll=poll, option_text=opt_text)

            messages.success(request, 'Anket güncellendi.')
            return redirect('polls_home')

        return render(
            request,
            'core/polls.html',
            _build_polls_context(user=request.user, edit_form=form, editing_poll=poll, open_edit_poll_modal=True),
        )

    edit_form = PollForm(initial=_build_poll_initial(poll))
    return render(
        request,
        'core/polls.html',
        _build_polls_context(user=request.user, edit_form=edit_form, editing_poll=poll, open_edit_poll_modal=True),
    )


@login_required
@require_POST
def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if not _poll_can_manage(poll, request.user):
        raise PermissionDenied("Bu anketi silme yetkiniz yok.")

    poll.delete()
    messages.success(request, 'Anket silindi.')
    return redirect('polls_home')


@login_required
def vote_poll(request, poll_id, option_id):
    poll = get_object_or_404(Poll, id=poll_id)
    option = get_object_or_404(PollOption, id=option_id, poll=poll)

    if PollVote.objects.filter(user=request.user, option__poll=poll).exists():
        messages.error(request, 'Bu ankete daha önce oy verdiniz.')
        return redirect('polls_home')

    # -------- Tarih kontrolü --------
    if poll.end_date and timezone.now() > poll.end_date:
        messages.error(request, 'Bu anketin süresi dolmuş.')
        return redirect('polls_home')

    if poll.is_active():
        PollVote.objects.create(user=request.user, option=option)
        messages.success(request, 'Oyunuz kaydedildi.')
    else:
        messages.error(request, 'Bu anket süresi dolmuş.')
    return redirect('polls_home')


@login_required
def poll_question_redirect(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if poll.related_question:
        # Soru mevcutsa direkt oraya git
        return redirect('question_detail', slug=poll.related_question.slug)
    else:
        # Aynı soru metni varsa mevcut olanı kullan
        q, created = Question.objects.get_or_create(
            question_text=f"anket:{poll.question_text}",
            defaults={'user': request.user}
        )
        q.users.add(request.user)
        poll.related_question = q
        poll.save()
        return redirect('question_detail', slug=q.slug)


@login_required
def vote_poll_ajax(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    # ---- Tarih kontrolü EKLENECEK! ----
    if poll.end_date and timezone.now() > poll.end_date:
        # Süresi geçmiş: Sonucu döndür + hata mesajı
        options = poll.options.all()
        total_votes = sum(opt.votes.count() for opt in options)
        user_vote = PollVote.objects.filter(option__poll=poll, user=request.user).first()
        context = {
            'poll': poll,
            'options': options,
            'total_votes': total_votes,
            'user_vote': user_vote,
            'poll_expired': True,  # yeni context anahtarı!
        }
        html = render_to_string('core/poll_popover_content.html', context, request)
        return JsonResponse({'html': html, 'error': "Bu anketin süresi doldu."}, status=400)

    # --- Normal oy verme ---
    if request.method == 'POST':
        option_id = request.POST.get('option_id')
        if PollVote.objects.filter(user=request.user, option__poll=poll).exists():
            # Zaten oy vermiş
            pass
        else:
            option = get_object_or_404(PollOption, id=option_id, poll=poll)
            PollVote.objects.create(user=request.user, option=option)
    # Sonuçları tekrar gönder
    options = poll.options.all()
    total_votes = sum(opt.votes.count() for opt in options)
    user_vote = PollVote.objects.filter(option__poll=poll, user=request.user).first()
    context = {
        'poll': poll,
        'options': options,
        'total_votes': total_votes,
        'user_vote': user_vote,
        'poll_expired': False,  # yeni context anahtarı!
    }
    html = render_to_string('core/poll_popover_content.html', context, request)
    return JsonResponse({'html': html})


@login_required
def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    options = poll.options.all()
    total_votes = sum(opt.votes.count() for opt in options)
    user_vote = None

    if request.user.is_authenticated:
        # Kullanıcı daha önce oy vermiş mi?
        for opt in options:
            if opt.votes.filter(user=request.user).exists():
                user_vote = opt.id
                break

    # Oy kullanma işlemi (POST)
    if request.method == "POST":
        # Önce: Süre kontrolü
        if poll.end_date and timezone.now() > poll.end_date:
            messages.error(request, "Bu anketin süresi dolmuş. Oy kullanamazsınız.")
            return redirect('poll_detail', poll_id=poll.id)
        if not user_vote:
            option_id = request.POST.get("option")
            option = get_object_or_404(PollOption, id=option_id, poll=poll)
            PollVote.objects.create(user=request.user, option=option)
            return redirect('poll_detail', poll_id=poll.id)
        else:
            messages.error(request, "Bu ankete zaten oy verdiniz.")
            return redirect('poll_detail', poll_id=poll.id)

    # Her seçenek için yüzdeleri hesapla
    options_data = []
    for opt in options:
        votes = opt.votes.count()
        percentage = (votes / total_votes * 100) if total_votes > 0 else 0
        options_data.append({
            'option': opt,
            'votes': votes,
            'percentage': round(percentage, 2)
        })

    context = {
        'poll': poll,
        'options_data': options_data,
        'total_votes': total_votes,
        'user_vote': user_vote,
    }
    return render(request, 'core/poll_detail.html', context)


@login_required
def poll_popover_content(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    options = poll.options.all()
    total_votes = sum(opt.votes.count() for opt in options)
    user_vote = None
    if request.user.is_authenticated:
        user_vote = PollVote.objects.filter(user=request.user, option__poll=poll).first()
    # Her option için yüzdeyi hesapla ve diziye ekle:
    options_data = []
    for opt in options:
        votes = opt.votes.count()
        percentage = (votes / total_votes * 100) if total_votes > 0 else 0
        options_data.append({
            'option': opt,
            'votes': votes,
            'percentage': round(percentage, 1)
        })
    context = {
        'poll': poll,
        'options_data': options_data,
        'user_vote': user_vote,
        'poll_expired': poll.end_date and timezone.now() > poll.end_date,
        'total_votes': total_votes,
    }
    html = render_to_string('core/poll_popover_content.html', context)
    return JsonResponse({'html': html})
