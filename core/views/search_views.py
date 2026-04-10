import re
import unicodedata

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from ..models import Answer, Question, UserProfile


def search_suggestions(request):
    query = request.GET.get('q', '')
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 20))

    suggestions = []

    if offset == 0:
        users = User.objects.filter(username__icontains=query)[:10]
        for user in users:
            suggestions.append({
                'type': 'user',
                'label': '@' + user.username,
                'url': reverse('user_profile', args=[user.username]),
            })

        from core.models import Hashtag
        if query.startswith('#'):
            hashtag_query = query.lstrip('#')
            if hashtag_query:
                hashtags = Hashtag.objects.filter(
                    name__icontains=hashtag_query
                ).annotate(
                    usage_count=Count('usages')
                ).filter(
                    usage_count__gt=0
                ).order_by('-usage_count')[:5]
                for hashtag in hashtags:
                    suggestions.append({
                        'type': 'hashtag',
                        'label': '#' + hashtag.name,
                        'url': reverse('hashtag_view', args=[hashtag.name]),
                    })

    questions = Question.objects.filter(
        question_text__icontains=query
    ).order_by('-created_at')[offset:offset + (limit * 3)]

    def normalize_search_label(value):
        normalized = unicodedata.normalize('NFKC', value or '')
        normalized = normalized.replace('’', "'").replace('`', "'").replace('´', "'")
        normalized = re.sub(r'\s+', ' ', normalized).strip().casefold()
        return normalized

    seen_question_labels = set()
    appended_question_count = 0
    for question in questions:
        normalized_label = normalize_search_label(question.question_text)
        if not normalized_label or normalized_label in seen_question_labels:
            continue
        seen_question_labels.add(normalized_label)
        suggestions.append({
            'type': 'question',
            'label': question.question_text,
            'url': reverse('question_detail', args=[question.slug]),
        })
        appended_question_count += 1
        if appended_question_count >= limit:
            break

    total_questions = Question.objects.filter(question_text__icontains=query).values('question_text').distinct().count()
    has_more = (offset + limit) < total_questions

    return JsonResponse({
        'suggestions': suggestions,
        'has_more': has_more,
        'total': total_questions,
        'next_offset': offset + limit if has_more else None,
    })


def load_more_questions(request):
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 20))

    questions = Question.objects.select_related('user').annotate(
        answers_count=Count('answers')
    ).order_by('-created_at')[offset:offset + limit]

    total_questions = Question.objects.count()
    has_more = (offset + limit) < total_questions

    questions_data = [{
        'slug': q.slug,
        'text': q.question_text,
        'answers_count': q.answers_count,
    } for q in questions]

    return JsonResponse({
        'questions': questions_data,
        'has_more': has_more,
        'total': total_questions,
        'next_offset': offset + limit if has_more else None,
    })


@login_required
def search(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' or request.GET.get('ajax') == '1'
    if is_ajax:
        query = request.GET.get('q', '').strip()
        results = []
        if query:
            from core.models import Hashtag

            questions = Question.objects.filter(question_text__icontains=query)
            users = User.objects.filter(username__icontains=query)

            hashtags = []
            if query.startswith('#'):
                hashtag_query = query.lstrip('#')
                if hashtag_query:
                    hashtags = Hashtag.objects.filter(
                        name__icontains=hashtag_query
                    ).annotate(
                        usage_count=Count('usages')
                    ).filter(
                        usage_count__gt=0
                    ).order_by('-usage_count')[:5]

            results += [
                {'type': 'question', 'id': q.id, 'slug': q.slug, 'text': q.question_text, 'url': reverse('question_detail', args=[q.slug])}
                for q in questions
            ]
            results += [
                {'type': 'user', 'id': u.id, 'username': u.username, 'text': '@' + u.username, 'url': reverse('user_profile', args=[u.username])}
                for u in users
            ]
            results += [
                {'type': 'hashtag', 'id': h.id, 'text': '#' + h.name, 'usage_count': h.usage_count, 'url': reverse('hashtag_view', args=[h.name])}
                for h in hashtags
            ]
        return JsonResponse({'results': results})

    q_param = request.GET.get('q', '').strip()
    username = request.GET.get('username', '').strip()
    date_from = request.GET.get('date_from', '').strip()
    date_to = request.GET.get('date_to', '').strip()
    keywords = request.GET.get('keywords', '').strip()
    hashtag_param = request.GET.get('hashtag', '').strip()
    followed_only = request.GET.get('followed_only', '') == '1'
    search_in = request.GET.get('search_in', 'all')

    questions = Question.objects.all()
    answers = Answer.objects.all()
    users_found = User.objects.none()

    if q_param:
        questions = questions.filter(question_text__icontains=q_param)
        answers = answers.filter(answer_text__icontains=q_param)
        users_found = User.objects.filter(username__icontains=q_param)

    if username:
        questions = questions.filter(user__username__icontains=username)
        answers = answers.filter(user__username__icontains=username)
    if date_from:
        questions = questions.filter(created_at__date__gte=date_from)
        answers = answers.filter(created_at__date__gte=date_from)
    if date_to:
        questions = questions.filter(created_at__date__lte=date_to)
        answers = answers.filter(created_at__date__lte=date_to)
    if keywords:
        questions = questions.filter(question_text__icontains=keywords)
        answers = answers.filter(answer_text__icontains=keywords)

    if hashtag_param:
        from core.models import Hashtag
        try:
            hashtag = Hashtag.objects.get(name__iexact=hashtag_param)
            question_ids = hashtag.usages.filter(question__isnull=False).values_list('question_id', flat=True)
            answer_ids = hashtag.usages.filter(answer__isnull=False).values_list('answer_id', flat=True)
            questions = questions.filter(id__in=question_ids)
            answers = answers.filter(id__in=answer_ids)
        except Hashtag.DoesNotExist:
            questions = Question.objects.none()
            answers = Answer.objects.none()

    if followed_only and request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
            followed_user_ids = user_profile.following.values_list('user_id', flat=True)
            questions = questions.filter(user_id__in=followed_user_ids)
            answers = answers.filter(user_id__in=followed_user_ids)
        except UserProfile.DoesNotExist:
            questions = Question.objects.none()
            answers = Answer.objects.none()

    if search_in == 'question':
        answers = Answer.objects.none()
    elif search_in == 'answer':
        questions = Question.objects.none()

    combined_results = [
        {"type": "question", "object": q, "created_at": q.created_at}
        for q in questions
    ] + [
        {"type": "answer", "object": a, "created_at": a.created_at}
        for a in answers
    ]
    combined_results.sort(key=lambda x: x['created_at'], reverse=False)

    page_number = request.GET.get('page', 1)
    paginator = Paginator(combined_results, 15)
    try:
        page_obj = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    users_page_number = request.GET.get('users_page', 1)
    users_paginator = Paginator(users_found.order_by('username'), 10)
    try:
        users_paginated = users_paginator.page(users_page_number)
    except (PageNotAnInteger, EmptyPage):
        users_paginated = users_paginator.page(1)

    get_params = request.GET.copy()
    if 'page' in get_params:
        del get_params['page']
    if 'users_page' in get_params:
        del get_params['users_page']
    querystring = get_params.urlencode()

    context = {
        'results': page_obj,
        'users': users_paginated,
        'query': q_param,
        'username': username,
        'date_from': date_from,
        'date_to': date_to,
        'keywords': keywords,
        'search_in': search_in,
        'page_obj': page_obj,
        'users_page_obj': users_paginated,
        'querystring': querystring,
        'request': request,
    }
    return render(request, 'core/search_results.html', context)


@login_required
def load_more_search_results(request):
    q_param = request.GET.get('q', '').strip()
    username = request.GET.get('username', '').strip()
    date_from = request.GET.get('date_from', '').strip()
    date_to = request.GET.get('date_to', '').strip()
    keywords = request.GET.get('keywords', '').strip()
    hashtag_param = request.GET.get('hashtag', '').strip()
    followed_only = request.GET.get('followed_only', '') == '1'
    search_in = request.GET.get('search_in', 'all')
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 15))

    questions = Question.objects.all()
    answers = Answer.objects.all()

    if q_param:
        questions = questions.filter(question_text__icontains=q_param)
        answers = answers.filter(answer_text__icontains=q_param)

    if username:
        questions = questions.filter(user__username__icontains=username)
        answers = answers.filter(user__username__icontains=username)
    if date_from:
        questions = questions.filter(created_at__date__gte=date_from)
        answers = answers.filter(created_at__date__gte=date_from)
    if date_to:
        questions = questions.filter(created_at__date__lte=date_to)
        answers = answers.filter(created_at__date__lte=date_to)
    if keywords:
        questions = questions.filter(question_text__icontains=keywords)
        answers = answers.filter(answer_text__icontains=keywords)

    if hashtag_param:
        from core.models import Hashtag
        try:
            hashtag = Hashtag.objects.get(name__iexact=hashtag_param)
            question_ids = hashtag.usages.filter(question__isnull=False).values_list('question_id', flat=True)
            answer_ids = hashtag.usages.filter(answer__isnull=False).values_list('answer_id', flat=True)
            questions = questions.filter(id__in=question_ids)
            answers = answers.filter(id__in=answer_ids)
        except Hashtag.DoesNotExist:
            questions = Question.objects.none()
            answers = Answer.objects.none()

    if followed_only and request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
            followed_user_ids = user_profile.following.values_list('user_id', flat=True)
            questions = questions.filter(user_id__in=followed_user_ids)
            answers = answers.filter(user_id__in=followed_user_ids)
        except UserProfile.DoesNotExist:
            questions = Question.objects.none()
            answers = Answer.objects.none()

    if search_in == 'question':
        answers = Answer.objects.none()
    elif search_in == 'answer':
        questions = Question.objects.none()

    combined_results = [
        {"type": "question", "object": q, "created_at": q.created_at}
        for q in questions
    ] + [
        {"type": "answer", "object": a, "created_at": a.created_at}
        for a in answers
    ]
    combined_results.sort(key=lambda x: x['created_at'], reverse=False)

    total_results = len(combined_results)
    paginated_results = combined_results[offset:offset + limit]
    has_more = (offset + limit) < total_results

    results_data = []
    for item in paginated_results:
        if item['type'] == 'question':
            q = item['object']
            results_data.append({
                'type': 'question',
                'id': q.id,
                'slug': q.slug,
                'text': q.question_text,
                'username': q.user.username,
                'created_at': q.created_at.strftime('%d %b %Y, %H:%M'),
            })
        elif item['type'] == 'answer':
            a = item['object']
            results_data.append({
                'type': 'answer',
                'id': a.id,
                'text': a.answer_text,
                'question_text': a.question.question_text,
                'question_slug': a.question.slug,
                'username': a.user.username,
                'created_at': a.created_at.strftime('%d %b %Y, %H:%M'),
            })

    return JsonResponse({
        'results': results_data,
        'has_more': has_more,
        'total': total_results,
        'next_offset': offset + limit if has_more else None,
    })


def user_search(request):
    query = request.GET.get('q', '').strip()
    users = User.objects.filter(username__icontains=query)[:10]
    results = [{'id': user.id, 'username': user.username} for user in users]
    return JsonResponse({'results': results})


def reference_search(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        questions = Question.objects.filter(question_text__icontains=query)
        for question in questions:
            results.append({
                'id': question.id,
                'text': question.question_text,
            })
    return JsonResponse({'results': results})
