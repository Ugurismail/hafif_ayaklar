"""Poll listing, voting, management, and embedded poll views."""

from collections import defaultdict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count, Prefetch, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.http import require_POST

from ..forms import PollForm
from ..models import Poll, PollOption, PollVote, Question


def _poll_can_manage(poll, user):
    return user.is_authenticated and (user.is_superuser or poll.created_by_id == user.id)


def _poll_options_queryset():
    return PollOption.objects.annotate(vote_count=Count('votes')).order_by('id')


def _polls_queryset():
    return (
        Poll.objects
        .select_related('created_by', 'related_question')
        .prefetch_related(Prefetch('options', queryset=_poll_options_queryset()))
    )


def _build_poll_cards(polls, user):
    polls = list(polls)
    poll_ids = [poll.id for poll in polls]
    user_vote_by_poll = {}

    if user and user.is_authenticated and poll_ids:
        user_vote_by_poll = dict(
            PollVote.objects
            .filter(user=user, option__poll_id__in=poll_ids)
            .values_list('option__poll_id', 'option_id')
        )

    cards = []
    for poll in polls:
        options = list(poll.options.all())
        total_votes = sum(option.vote_count for option in options)
        highest_vote_count = max((option.vote_count for option in options), default=0)
        selected_option_id = user_vote_by_poll.get(poll.id)
        options_data = []

        for option in options:
            percentage = (option.vote_count / total_votes * 100) if total_votes else 0
            options_data.append({
                'option': option,
                'text': option.option_text,
                'votes': option.vote_count,
                'percentage': round(percentage, 1),
                'is_selected': option.id == selected_option_id,
                'is_winner': bool(total_votes and option.vote_count == highest_vote_count),
            })

        cards.append({
            'poll': poll,
            'total_votes': total_votes,
            'options_data': options_data,
            'winner_text': ' · '.join(
                option.option_text
                for option in options
                if total_votes and option.vote_count == highest_vote_count
            ) or 'Henüz oy yok',
            'user_vote_option_id': selected_option_id,
            'has_voted': selected_option_id is not None,
            'can_vote': bool(user and user.is_authenticated and not selected_option_id and poll.is_active()),
            'can_manage': _poll_can_manage(poll, user),
            'can_edit': _poll_can_manage(poll, user) and total_votes == 0,
        })

    return cards


def _build_poll_initial(poll):
    initial = {
        'question_text': poll.question_text,
        'end_date': timezone.localtime(poll.end_date).strftime('%Y-%m-%dT%H:%M'),
        'is_anonymous': poll.is_anonymous,
    }
    options = list(poll.options.order_by('id').values_list('option_text', flat=True))
    for index, option_text in enumerate(options, start=1):
        initial[f'option_{index}'] = option_text
    return initial


def _build_polls_context(
    request,
    form=None,
    open_create_poll_modal=False,
    edit_form=None,
    editing_poll=None,
    open_edit_poll_modal=False,
):
    now = timezone.now()
    status = request.GET.get('status', 'active')
    if status not in {'active', 'expired'}:
        status = 'active'
    search_query = (request.GET.get('q') or '').strip()[:100]

    counts = Poll.objects.aggregate(
        active_count=Count('id', filter=Q(end_date__gt=now)),
        expired_count=Count('id', filter=Q(end_date__lte=now)),
    )

    polls = _polls_queryset()
    if status == 'active':
        polls = polls.filter(end_date__gt=now).order_by('end_date', '-created_at')
        per_page = 9
    else:
        polls = polls.filter(end_date__lte=now).order_by('-end_date', '-created_at')
        per_page = 20

    if search_query:
        polls = polls.filter(question_text__icontains=search_query)

    page_obj = Paginator(polls, per_page).get_page(request.GET.get('page'))
    poll_cards = _build_poll_cards(page_obj.object_list, request.user)

    return {
        'form': form or PollForm(),
        'edit_form': edit_form,
        'editing_poll': editing_poll,
        'open_create_poll_modal': open_create_poll_modal,
        'open_edit_poll_modal': open_edit_poll_modal,
        'status': status,
        'search_query': search_query,
        'active_count': counts['active_count'],
        'expired_count': counts['expired_count'],
        'active_polls_data': poll_cards if status == 'active' else [],
        'expired_polls_data': poll_cards if status == 'expired' else [],
        'page_obj': page_obj,
    }


def polls_home(request):
    return render(request, 'core/polls.html', _build_polls_context(request))


@login_required
def create_poll(request):
    if request.method != 'POST':
        return redirect('polls_home')

    form = PollForm(request.POST)
    if not form.is_valid():
        return render(
            request,
            'core/polls.html',
            _build_polls_context(request, form=form, open_create_poll_modal=True),
        )

    poll = Poll.objects.create(
        question_text=form.cleaned_data['question_text'],
        created_by=request.user,
        end_date=form.cleaned_data['end_date'],
        is_anonymous=form.cleaned_data['is_anonymous'],
    )
    PollOption.objects.bulk_create([
        PollOption(poll=poll, option_text=option_text)
        for option_text in form.cleaned_data['options']
    ])

    messages.success(request, 'Anket başarıyla oluşturuldu.')
    return redirect('polls_home')


@login_required
def edit_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if not _poll_can_manage(poll, request.user):
        raise PermissionDenied('Bu anketi düzenleme yetkiniz yok.')

    if PollVote.objects.filter(option__poll=poll).exists():
        messages.error(request, 'Oy alınmış anketlerin seçenekleri değiştirilemez.')
        return redirect('polls_home')

    if request.method == 'POST':
        form = PollForm(request.POST, prefix='edit')
        if form.is_valid():
            poll.question_text = form.cleaned_data['question_text']
            poll.end_date = form.cleaned_data['end_date']
            poll.is_anonymous = form.cleaned_data['is_anonymous']
            poll.save(update_fields=['question_text', 'end_date', 'is_anonymous'])

            poll.options.all().delete()
            PollOption.objects.bulk_create([
                PollOption(poll=poll, option_text=option_text)
                for option_text in form.cleaned_data['options']
            ])
            messages.success(request, 'Anket güncellendi.')
            return redirect('polls_home')

        return render(
            request,
            'core/polls.html',
            _build_polls_context(
                request,
                edit_form=form,
                editing_poll=poll,
                open_edit_poll_modal=True,
            ),
        )

    edit_form = PollForm(initial=_build_poll_initial(poll), prefix='edit')
    return render(
        request,
        'core/polls.html',
        _build_polls_context(
            request,
            edit_form=edit_form,
            editing_poll=poll,
            open_edit_poll_modal=True,
        ),
    )


@login_required
@require_POST
def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if not _poll_can_manage(poll, request.user):
        raise PermissionDenied('Bu anketi silme yetkiniz yok.')

    poll.delete()
    messages.success(request, 'Anket silindi.')
    return redirect('polls_home')


def _record_poll_vote(poll, user, option_id):
    with transaction.atomic():
        locked_poll = Poll.objects.select_for_update().get(pk=poll.pk)
        if not locked_poll.is_active():
            return 'expired'
        if PollVote.objects.filter(user=user, option__poll=locked_poll).exists():
            return 'duplicate'

        option = get_object_or_404(PollOption, id=option_id, poll=locked_poll)
        PollVote.objects.create(user=user, option=option)
        return 'created'


@login_required
@require_POST
def vote_poll(request, poll_id, option_id):
    poll = get_object_or_404(Poll, id=poll_id)
    result = _record_poll_vote(poll, request.user, option_id)
    if result == 'created':
        messages.success(request, 'Oyunuz kaydedildi.')
    elif result == 'duplicate':
        messages.error(request, 'Bu ankete daha önce oy verdiniz.')
    else:
        messages.error(request, 'Bu anketin süresi dolmuş.')
    return redirect('polls_home')


@login_required
def poll_question_redirect(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if poll.related_question:
        return redirect('question_detail', slug=poll.related_question.slug)

    question_text = f'anket:{poll.question_text}'
    question = Question.objects.filter(question_text=question_text).order_by('id').first()
    if not question:
        question = Question.objects.create(question_text=question_text, user=request.user)
    question.users.add(request.user)
    poll.related_question = question
    poll.save(update_fields=['related_question'])
    return redirect('question_detail', slug=question.slug)


def _single_poll_context(poll_id, user, include_voters=False):
    poll = get_object_or_404(_polls_queryset(), id=poll_id)
    card = _build_poll_cards([poll], user)[0]

    if include_voters and not poll.is_anonymous:
        voters_by_option = defaultdict(list)
        votes = (
            PollVote.objects
            .filter(option__poll=poll)
            .select_related('user')
            .order_by('voted_at')
        )
        for vote in votes:
            voters_by_option[vote.option_id].append(vote.user.username)
        for option_data in card['options_data']:
            option_data['voters'] = voters_by_option[option_data['option'].id]

    return card


@login_required
@require_POST
def vote_poll_ajax(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    option_id = request.POST.get('option_id')
    result = _record_poll_vote(poll, request.user, option_id)
    card = _single_poll_context(poll.id, request.user)
    context = {
        **card,
        'poll_expired': not card['poll'].is_active(),
        'user_vote': card['user_vote_option_id'],
    }
    html = render_to_string('core/poll_popover_content.html', context, request=request)
    if result == 'expired':
        return JsonResponse({'html': html, 'error': 'Bu anketin süresi doldu.'}, status=400)
    return JsonResponse({'html': html})


@login_required
def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if request.method == 'POST':
        result = _record_poll_vote(poll, request.user, request.POST.get('option'))
        if result == 'created':
            messages.success(request, 'Oyunuz kaydedildi.')
        elif result == 'duplicate':
            messages.error(request, 'Bu ankete zaten oy verdiniz.')
        else:
            messages.error(request, 'Bu anketin süresi dolmuş. Oy kullanamazsınız.')
        return redirect('poll_detail', poll_id=poll.id)

    card = _single_poll_context(poll.id, request.user, include_voters=True)
    return render(request, 'core/poll_detail.html', {
        **card,
        'poll_expired': not card['poll'].is_active(),
        'user_vote': card['user_vote_option_id'],
    })


@login_required
def poll_popover_content(request, poll_id):
    card = _single_poll_context(poll_id, request.user)
    context = {
        **card,
        'poll_expired': not card['poll'].is_active(),
        'user_vote': card['user_vote_option_id'],
    }
    html = render_to_string('core/poll_popover_content.html', context, request=request)
    return JsonResponse({'html': html})
