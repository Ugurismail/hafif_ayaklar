"""
Miscellaneous views
- user_homepage
- site_statistics
- about
- search
- search_suggestions
- user_search
- reference_search
- custom_404_view
- custom_403_view
- custom_500_view
- custom_502_view
- random_question_id
- shuffle_questions
- get_today_questions_queryset
- get_today_questions_page
- download_entries_json
- download_entries_xlsx
- download_entries_docx
- filter_answers
- insert_toc
- add_question_tree_to_docx
"""

import json
import random
import re
from collections import Counter
from datetime import timedelta
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count, Max, F
from django.db.models.functions import Coalesce
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.timezone import now
from django.views.decorators.http import require_POST

from openpyxl import Workbook
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from ..models import (
    Question, Answer, Vote, SavedItem, StartingQuestion,
    Reference, UserProfile, QuestionRelationship
)
from ..utils import paginate_queryset
from ..services import VoteSaveService
from ..querysets import get_today_questions_queryset


def get_today_questions_page(request, per_page=25):
    """Helper for paginating today's questions"""
    queryset = get_today_questions_queryset()
    return paginate_queryset(queryset, request, 'page', per_page)


def user_homepage(request):
    # Public view - anyone can see questions
    # But some features require login

    # Takip ettiklerim filtresi
    followed_param = request.GET.get('followed', '0')
    show_followed_only = followed_param == '1'

    # 1. Tüm Sorular (ve cevap sayısı) - Using new utility
    all_questions_qs = get_today_questions_queryset().select_related('user')

    # Takip ettiklerim filtresi uygulanırsa
    if show_followed_only and request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
            # UserProfile'dan User ID'lerini al
            followed_user_ids = user_profile.following.values_list('user_id', flat=True)
            all_questions_qs = all_questions_qs.filter(user_id__in=followed_user_ids)
        except UserProfile.DoesNotExist:
            # Kullanıcının profili yoksa boş sonuç döndür
            all_questions_qs = Question.objects.none()

    all_questions = paginate_queryset(all_questions_qs, request, 'page', 20)

    # 2. Rastgele Cevaplar -- OPTİMİZE (direkt order_by('?') kullan, daha hızlı)
    # values_list tüm tabloyı tararsa çok yavaş olur, bunun yerine doğrudan rastgele order kullan
    random_items = list(Answer.objects.select_related(
        'question',
        'user',
        'user__userprofile'
    ).order_by('?')[:20])

    # 3. Başlangıç Soruları (sadece login olmuş kullanıcılar için) - Using new utility
    if request.user.is_authenticated:
        starting_questions_qs = StartingQuestion.objects.filter(user=request.user).select_related('question').annotate(
            total_subquestions=Count('question__child_relationships', filter=Q(question__child_relationships__user=request.user)),
            latest_subquestion_date=Max('question__child_relationships__created_at', filter=Q(question__child_relationships__user=request.user))
        ).order_by(F('latest_subquestion_date').desc(nulls_last=True)).select_related('question__user')

        starting_questions = paginate_queryset(starting_questions_qs, request, 'starting_page', 10)
    else:
        starting_questions = None

    # 4-6. Vote and Save data - Using new VoteSaveService
    if random_items:
        VoteSaveService.annotate_user_votes(random_items, request.user, Answer)
        saved_answer_ids, answer_save_dict = VoteSaveService.get_save_info(random_items, request.user, Answer)
    else:
        saved_answer_ids = set()
        answer_save_dict = {}

    context = {
        'random_items': random_items,
        'saved_answer_ids': saved_answer_ids,
        'answer_save_dict': answer_save_dict,
        'all_questions': all_questions,  # Pagineli queryset
        'starting_questions': starting_questions,  # Pagineli queryset
        'show_followed_only': show_followed_only,
    }
    return render(request, 'core/user_homepage.html', context)


@login_required
def site_statistics(request):
    # Kullanıcı sayısı (en az bir soru veya yanıt yazmış olanlar)
    user_count = User.objects.filter(
        Q(questions__isnull=False) | Q(answers__isnull=False)
    ).distinct().count()

    # Toplam soru ve yanıt sayısı
    total_questions = Question.objects.count()
    total_answers = Answer.objects.count()

    # Toplam beğeni ve beğenmeme sayısı
    total_likes = Vote.objects.filter(value=1).count()
    total_dislikes = Vote.objects.filter(value=-1).count()

    # En çok soru soran kullanıcılar
    top_question_users = User.objects.annotate(
        question_count=Count('questions')
    ).order_by('-question_count')[:5]

    # En çok yanıt veren kullanıcılar
    top_answer_users = User.objects.annotate(
        answer_count=Count('answers')
    ).order_by('-answer_count')[:5]

    # En çok beğenilen sorular (upvotes)
    top_liked_questions = Question.objects.annotate(
        like_count=F('upvotes')
    ).order_by('-like_count')[:5]

    # En çok beğenilen yanıtlar (upvotes)
    top_liked_answers = Answer.objects.annotate(
        like_count=F('upvotes')
    ).order_by('-like_count')[:5]

    # En çok kaydedilen sorular
    top_saved_questions = Question.objects.annotate(
        save_count=Count('saveditem')
    ).order_by('-save_count')[:5]

    # En çok kaydedilen yanıtlar
    top_saved_answers = Answer.objects.annotate(
        save_count=Count('saveditem')
    ).order_by('-save_count')[:5]

    active_tab = request.GET.get('tab', 'word-analysis')  # Varsayılan olarak "Kelime Analizi" sekmesi

    # --- KELİME ANALİZİ ve KELİME ARAMA ---
    question_texts = Question.objects.values_list('question_text', flat=True)
    answer_texts = Answer.objects.values_list('answer_text', flat=True)
    all_texts = list(question_texts) + list(answer_texts)

    # Küçük harfe çevir, birleştir (tüm kelimeleri görmek için)
    all_words = []
    for text in all_texts:
        if text:
            all_words.extend(re.findall(r'\b\w+\b', text.lower()))

    # Hariç tutulan kelimeleri işle
    exclude_words_input = request.GET.get('exclude_words', '')
    if exclude_words_input:
        exclude_words_list = re.split(r',\s*', exclude_words_input.strip())
        exclude_words = set(word.lower() for word in exclude_words_list if word.strip())
    else:
        exclude_words = set()

    # Hariç tutulanları çıkar
    filtered_words = [word for word in all_words if word not in exclude_words]

    # En çok geçen kelimeler
    word_counts = Counter(filtered_words)
    top_words = word_counts.most_common(10)

    # --- Anahtar kelime arama: tüm başlık ve yanıtlarda toplam kaç kere geçiyor? ---
    search_word = request.GET.get('search_word', '').strip().lower()
    search_word_count = None
    if search_word:
        # Hariç tutulan bir kelimeyle aynıysa, doğrudan 0 göster
        if search_word in exclude_words:
            search_word_count = 0
        else:
            # Tek tek başlık ve yanıtların hepsini say (her satırda birden fazla geçiş varsa onlar da dahil)
            search_word_pattern = re.compile(r'\b{}\b'.format(re.escape(search_word)), re.IGNORECASE)
            search_word_count = 0
            for text in all_texts:
                # Hariç tutulan kelimelerden biri bu text'te geçiyorsa, burayı tamamen atla
                if any(re.search(r'\b{}\b'.format(re.escape(exw)), text, re.IGNORECASE) for exw in exclude_words):
                    continue
                if text:
                    search_word_count += len(search_word_pattern.findall(text))

    # --- En çok kullanılan kaynaklar ---

    all_references = list(Reference.objects.all())
    all_references.sort(key=lambda ref: ref.get_usage_count(), reverse=True)
    paginator_references = Paginator(all_references, 20)  # Sayfa başına 20 kaynak
    reference_page_number = request.GET.get('reference_page', 1)
    top_references = paginator_references.get_page(reference_page_number)
    # --- Ek İstatistikler ---

    # Toplam girdi sayısı (soru + yanıt)
    total_entries = len(all_texts)

    # Toplam kelime ve karakter sayısı
    total_words = sum(len(re.findall(r'\b\w+\b', text)) for text in all_texts if text)
    total_characters = sum(len(text) for text in all_texts if text)

    # Ortalama girdi başına kelime ve karakter
    avg_words_per_entry = round(total_words / total_entries, 2) if total_entries else 0
    avg_chars_per_entry = round(total_characters / total_entries, 2) if total_entries else 0

    # Kullanıcı başına ortalama girdi (aktif kullanıcılar = user_count)
    avg_entries_per_user = round(total_entries / user_count, 2) if user_count else 0

    context = {
        'active_tab': active_tab,
        'user_count': user_count,
        'total_questions': total_questions,
        'total_answers': total_answers,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'top_question_users': top_question_users,
        'top_answer_users': top_answer_users,
        'top_liked_questions': top_liked_questions,
        'top_liked_answers': top_liked_answers,
        'top_saved_questions': top_saved_questions,
        'top_saved_answers': top_saved_answers,
        'top_words': top_words,
        'search_word_count': search_word_count,
        'search_word': search_word,
        'exclude_words': ', '.join(sorted(exclude_words)),
        'exclude_words_input': exclude_words_input,
        'top_references': top_references,
        'total_words': total_words,
        'total_characters': total_characters,
        'avg_words_per_entry': avg_words_per_entry,
        'avg_chars_per_entry': avg_chars_per_entry,
        'avg_entries_per_user': avg_entries_per_user,
    }
    return render(request, 'core/site_statistics.html', context)


def about(request):
    return render(request, 'core/about.html')


def search_suggestions(request):
    query = request.GET.get('q', '')
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 20))  # Her seferinde 20 sonuç

    suggestions = []

    # Kullanıcıları ara (toplam kullanıcı sayısı genelde az olduğu için limit yok)
    if offset == 0:  # Sadece ilk yüklemede kullanıcıları ve etiketleri göster
        users = User.objects.filter(username__icontains=query)[:10]  # Max 10 kullanıcı
        for user in users:
            suggestions.append({
                'type': 'user',
                'label': '@' + user.username,
                'url': reverse('user_profile', args=[user.username])
            })

        # Hashtag araması - SADECE # ile başlıyorsa hashtag ara
        from core.models import Hashtag
        if query.startswith('#'):
            hashtag_query = query.lstrip('#')
            if hashtag_query:  # Boş değilse ara
                hashtags = Hashtag.objects.filter(name__icontains=hashtag_query).annotate(
                    usage_count=Count('usages')
                ).order_by('-usage_count')[:5]  # Max 5 hashtag
                for hashtag in hashtags:
                    suggestions.append({
                        'type': 'hashtag',
                        'label': '#' + hashtag.name,
                        'url': reverse('hashtag_view', args=[hashtag.name])
                    })

    # Soruları ara (sayfalama ile)
    questions = Question.objects.filter(
        question_text__icontains=query
    ).order_by('-created_at')[offset:offset + limit]

    for question in questions:
        suggestions.append({
            'type': 'question',
            'label': question.question_text,
            'url': reverse('question_detail', args=[question.slug])
        })

    # Toplam soru sayısını hesapla
    total_questions = Question.objects.filter(question_text__icontains=query).count()
    has_more = (offset + limit) < total_questions

    return JsonResponse({
        'suggestions': suggestions,
        'has_more': has_more,
        'total': total_questions,
        'next_offset': offset + limit if has_more else None
    })


def load_more_questions(request):
    """
    AJAX endpoint for lazy loading sidebar questions
    """
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
        'answers_count': q.answers_count
    } for q in questions]

    return JsonResponse({
        'questions': questions_data,
        'has_more': has_more,
        'total': total_questions,
        'next_offset': offset + limit if has_more else None
    })


@login_required
def search(request):
    """
    Gelişmiş arama ve autocomplete destekli search view.
    Tüm GET parametreleri sayfalandırmada korunur.
    """
    # 1) AJAX araması/autocomplete
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' or request.GET.get('ajax') == '1'
    if is_ajax:
        query = request.GET.get('q', '').strip()
        results = []
        if query:
            from core.models import Hashtag
            from django.db.models import Count

            questions = Question.objects.filter(question_text__icontains=query)
            users = User.objects.filter(username__icontains=query)

            # Hashtag araması - SADECE # ile başlıyorsa hashtag ara
            hashtags = []
            if query.startswith('#'):
                hashtag_query = query.lstrip('#')
                if hashtag_query:
                    hashtags = Hashtag.objects.filter(name__icontains=hashtag_query).annotate(
                        usage_count=Count('usages')
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

    # 2) GET parametrelerini çek
    q_param = request.GET.get('q', '').strip()
    username = request.GET.get('username', '').strip()
    date_from = request.GET.get('date_from', '').strip()
    date_to = request.GET.get('date_to', '').strip()
    keywords = request.GET.get('keywords', '').strip()
    hashtag_param = request.GET.get('hashtag', '').strip()
    followed_only = request.GET.get('followed_only', '') == '1'
    search_in = request.GET.get('search_in', 'all')

    # 3) Temel querysetler
    questions = Question.objects.all()
    answers = Answer.objects.all()
    users_found = User.objects.none()

    # 4) Basit q araması
    if q_param:
        questions = questions.filter(question_text__icontains=q_param)
        answers = answers.filter(answer_text__icontains=q_param)
        users_found = User.objects.filter(username__icontains=q_param)

    # 5) Gelişmiş filtreler
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

    # Hashtag filtresi
    if hashtag_param:
        from core.models import Hashtag
        try:
            hashtag = Hashtag.objects.get(name__iexact=hashtag_param)
            # HashtagUsage üzerinden hem question hem answer'ları filtrele
            question_ids = hashtag.usages.filter(
                question__isnull=False
            ).values_list('question_id', flat=True)
            answer_ids = hashtag.usages.filter(
                answer__isnull=False
            ).values_list('answer_id', flat=True)

            questions = questions.filter(id__in=question_ids)
            answers = answers.filter(id__in=answer_ids)
        except Hashtag.DoesNotExist:
            # Hashtag yoksa sonuç yok
            questions = Question.objects.none()
            answers = Answer.objects.none()

    # Takip ettiklerim filtresi
    if followed_only and request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
            # UserProfile'dan User ID'lerini al
            followed_user_ids = user_profile.following.values_list('user_id', flat=True)
            questions = questions.filter(user_id__in=followed_user_ids)
            answers = answers.filter(user_id__in=followed_user_ids)
        except UserProfile.DoesNotExist:
            # Kullanıcının profili yoksa boş sonuç döndür
            questions = Question.objects.none()
            answers = Answer.objects.none()

    # 6) Arama yeri seçimi
    if search_in == 'question':
        answers = Answer.objects.none()
    elif search_in == 'answer':
        questions = Question.objects.none()

    # 7) Sonuçları birleştir, tarihe göre sırala
    combined_results = [
        {"type": "question", "object": q, "created_at": q.created_at}
        for q in questions
    ] + [
        {"type": "answer", "object": a, "created_at": a.created_at}
        for a in answers
    ]
    combined_results.sort(key=lambda x: x['created_at'], reverse=False)

    # 8) Pagination: tüm GET parametrelerini taşı
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

    # 9) Mevcut GET parametrelerini string olarak aktar
    get_params = request.GET.copy()
    if 'page' in get_params:
        del get_params['page']
    if 'users_page' in get_params:
        del get_params['users_page']
    querystring = get_params.urlencode()

    # 10) Template context
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
    """
    AJAX endpoint for lazy loading advanced search results
    """
    # GET parametrelerini al
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

    # Temel querysetler
    questions = Question.objects.all()
    answers = Answer.objects.all()

    # Basit q araması
    if q_param:
        questions = questions.filter(question_text__icontains=q_param)
        answers = answers.filter(answer_text__icontains=q_param)

    # Gelişmiş filtreler
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

    # Hashtag filtresi
    if hashtag_param:
        from core.models import Hashtag
        try:
            hashtag = Hashtag.objects.get(name__iexact=hashtag_param)
            question_ids = hashtag.usages.filter(
                question__isnull=False
            ).values_list('question_id', flat=True)
            answer_ids = hashtag.usages.filter(
                answer__isnull=False
            ).values_list('answer_id', flat=True)

            questions = questions.filter(id__in=question_ids)
            answers = answers.filter(id__in=answer_ids)
        except Hashtag.DoesNotExist:
            questions = Question.objects.none()
            answers = Answer.objects.none()

    # Takip ettiklerim filtresi
    if followed_only and request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
            # UserProfile'dan User ID'lerini al
            followed_user_ids = user_profile.following.values_list('user_id', flat=True)
            questions = questions.filter(user_id__in=followed_user_ids)
            answers = answers.filter(user_id__in=followed_user_ids)
        except UserProfile.DoesNotExist:
            questions = Question.objects.none()
            answers = Answer.objects.none()

    # Arama yeri seçimi
    if search_in == 'question':
        answers = Answer.objects.none()
    elif search_in == 'answer':
        questions = Question.objects.none()

    # Sonuçları birleştir, tarihe göre sırala
    combined_results = [
        {"type": "question", "object": q, "created_at": q.created_at}
        for q in questions
    ] + [
        {"type": "answer", "object": a, "created_at": a.created_at}
        for a in answers
    ]
    combined_results.sort(key=lambda x: x['created_at'], reverse=False)

    # Sayfalama için dilimle
    total_results = len(combined_results)
    paginated_results = combined_results[offset:offset + limit]
    has_more = (offset + limit) < total_results

    # JSON formatında döndür
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
                'created_at': q.created_at.strftime('%d %b %Y, %H:%M')
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
                'created_at': a.created_at.strftime('%d %b %Y, %H:%M')
            })

    return JsonResponse({
        'results': results_data,
        'has_more': has_more,
        'total': total_results,
        'next_offset': offset + limit if has_more else None
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
                'text': question.question_text
            })
    return JsonResponse({'results': results})


def custom_400_view(request, exception):
    response = render(request, 'core/400.html')
    response.status_code = 400
    return response


def custom_404_view(request, exception):
    response = render(request, 'core/404.html')
    response.status_code = 404
    return response


def custom_403_view(request, exception):
    response = render(request, 'core/403.html')
    response.status_code = 403
    return response


def custom_500_view(request):
    response = render(request, 'core/500.html')
    response.status_code = 500
    return response


def custom_502_view(request):
    response = render(request, 'core/502.html')
    response.status_code = 502
    return response


@require_POST
def random_question_id(request):
    ids = list(Question.objects.values_list('id', flat=True))
    if not ids:
        return JsonResponse({'question_id': None})
    random_id = random.choice(ids)
    return JsonResponse({'question_id': random_id})


def shuffle_questions(request):
    all_ids = list(Question.objects.values_list('id', flat=True))
    if not all_ids:
        return JsonResponse({'questions': []})
    # Rastgele 20 id seç
    sample_size = min(20, len(all_ids))
    selected_ids = random.sample(all_ids, sample_size)
    # Sırayı karıştır, başlıkları çek
    questions = (Question.objects
                 .filter(id__in=selected_ids)
                 .annotate(answers_count=Count('answers'))
                 .values('id', 'slug', 'question_text', 'answers_count'))
    # Rastgele sıralamayı korumak için shuffle
    questions = list(questions)
    random.shuffle(questions)
    return JsonResponse({'questions': [
        {'id': q['id'], 'slug': q['slug'], 'text': q['question_text'], 'answers_count': q['answers_count']} for q in questions
    ]})


@login_required
def download_entries_json(request, username):
    target_user = get_object_or_404(User, username=username)
    if request.user != target_user and not request.user.is_superuser:
        return JsonResponse(
            {'error': 'Bu işlemi yapmaya yetkiniz yok.'},
            status=403
        )

    user_questions = Question.objects.filter(user=target_user).order_by('created_at')

    questions_data = []
    for q in user_questions:
        q_answers = q.answers.filter(user=target_user).order_by('created_at')

        answers_data = []
        for ans in q_answers:
            answers_data.append({
                'answer_text': ans.answer_text,
                'answer_created_at': ans.created_at.isoformat(),
                'answer_user': ans.user.username,
            })
        questions_data.append({
            'question_text': q.question_text,
            'question_created_at': q.created_at.isoformat(),
            'answers': answers_data
        })

    final_data = {
        'username': target_user.username,
        'questions': questions_data,
    }

    json_string = json.dumps(
        final_data,
        ensure_ascii=False,
        indent=2
    )

    response = HttpResponse(json_string, content_type='application/json; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="entries.json"'
    return response


@login_required
def download_entries_xlsx(request, username):
    target_user = get_object_or_404(User, username=username)
    if request.user != target_user and not request.user.is_superuser:
        return JsonResponse(
            {'error': 'Bu işlemi yapmaya yetkiniz yok.'},
            status=403
        )

    user_questions = Question.objects.filter(user=target_user).order_by('created_at')

    wb = Workbook()
    ws = wb.active
    ws.title = "Entries"

    row_idx = 1

    for question in user_questions:
        ws.cell(row=row_idx, column=1, value=question.question_text)

        user_answers = question.answers.filter(user=target_user).order_by('created_at')

        answer_start_row = row_idx

        for i, ans in enumerate(user_answers):
            current_row = answer_start_row + i
            ws.cell(row=current_row, column=2, value=ans.answer_text)

        row_idx = answer_start_row + max(len(user_answers), 1)
        row_idx += 1

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="entries.xlsx"'

    wb.save(response)
    return response


def insert_toc(paragraph):
    run = paragraph.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.text = 'TOC \\o "1-3" \\h \\z \\u'
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)


def add_question_tree_to_docx(doc, question, target_user, level=1, visited=None):
    if visited is None:
        visited = set()
    if question.id in visited:
        return
    visited.add(question.id)

    doc.add_heading(question.question_text, level=level)

    user_answers = question.answers.filter(user=target_user).order_by('created_at')
    for answer in user_answers:
        date_str = answer.created_at.strftime("%Y-%m-%d %H:%M")
        p = doc.add_paragraph()
        run = p.add_run(date_str + "  ")
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(140, 140, 140)
        run.italic = True
        p.add_run(answer.answer_text)
        doc.add_paragraph("")

    # Kullanıcının bu sorunun alt sorularını al (kullanıcı-bazlı)
    subquestions_rels = QuestionRelationship.objects.filter(
        parent=question,
        user=target_user
    ).select_related('child').order_by('created_at')
    for rel in subquestions_rels:
        add_question_tree_to_docx(doc, rel.child, target_user, level=min(level+1, 9), visited=visited)


@login_required
def download_entries_docx(request, username):
    target_user = get_object_or_404(User, username=username)
    if request.user != target_user and not request.user.is_superuser:
        return JsonResponse({'error': 'Bu işlemi yapmaya yetkiniz yok.'}, status=403)

    # Kullanıcının başlangıç sorularını al
    starting_question_ids = StartingQuestion.objects.filter(user=target_user).values_list('question_id', flat=True)
    user_questions = Question.objects.filter(id__in=starting_question_ids).order_by('created_at').distinct()

    document = Document()

    document.add_heading(f"{target_user.username} Entries", 0)

    toc_paragraph = document.add_paragraph()
    insert_toc(toc_paragraph)

    instruction_text = (
        "Belgeyi açtıktan sonra içindekiler bölümünü görmek için, Word içerisinde "
        "alanı (veya tüm belgeyi) güncellemeniz gerekir (sağ tıklayıp 'Update Field' veya Ctrl+A ardından F9'a basabilirsiniz)."
    )
    document.add_paragraph(instruction_text)

    document.add_page_break()

    for q in user_questions:
        add_question_tree_to_docx(document, q, target_user, level=1)

    f = BytesIO()
    document.save(f)
    f.seek(0)

    response = HttpResponse(
        f.read(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename="{target_user.username}_entries.docx"'
    return response


@login_required
def download_entries_pdf(request, username):
    """
    PDF export for user entries using ReportLab
    """
    target_user = get_object_or_404(User, username=username)
    if request.user != target_user and not request.user.is_superuser:
        return JsonResponse({'error': 'Bu işlemi yapmaya yetkiniz yok.'}, status=403)

    # Kullanıcının başlangıç sorularını al
    starting_question_ids = StartingQuestion.objects.filter(user=target_user).values_list('question_id', flat=True)
    user_questions = Question.objects.filter(id__in=starting_question_ids).order_by('created_at').distinct()

    # Create PDF buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)

    # Container for PDF elements
    elements = []

    # Register Turkish-compatible font
    # Try to use Helvetica or Arial which support Turkish characters
    try:
        import os

        # Try Helvetica first (available on macOS)
        helvetica_path = '/System/Library/Fonts/Helvetica.ttc'
        if os.path.exists(helvetica_path):
            # For TTC files, we need to specify subfontIndex
            pdfmetrics.registerFont(TTFont('TurkishFont', helvetica_path, subfontIndex=0))
            pdfmetrics.registerFont(TTFont('TurkishFont-Bold', helvetica_path, subfontIndex=1))
            font_name = 'TurkishFont'
        else:
            # Try Arial as fallback
            arial_path = '/System/Library/Fonts/ArialHB.ttc'
            if os.path.exists(arial_path):
                pdfmetrics.registerFont(TTFont('TurkishFont', arial_path, subfontIndex=0))
                font_name = 'TurkishFont'
            else:
                # Last resort: use built-in Helvetica (may not support all Turkish chars)
                font_name = 'Helvetica'
    except Exception as e:
        # If font registration fails, use built-in Helvetica
        font_name = 'Helvetica'

    # Define styles
    styles = getSampleStyleSheet()

    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=24,
        textColor='#2c3e50',
        spaceAfter=30,
        alignment=TA_CENTER
    )

    # Heading styles for different levels
    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=16,
        textColor='#2c3e50',
        spaceAfter=12,
        spaceBefore=12
    )

    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontName=font_name,
        fontSize=14,
        textColor='#34495e',
        spaceAfter=10,
        spaceBefore=10,
        leftIndent=20
    )

    h3_style = ParagraphStyle(
        'CustomH3',
        parent=styles['Heading3'],
        fontName=font_name,
        fontSize=12,
        textColor='#7f8c8d',
        spaceAfter=8,
        spaceBefore=8,
        leftIndent=40
    )

    # Answer text style
    answer_style = ParagraphStyle(
        'AnswerText',
        parent=styles['BodyText'],
        fontName=font_name,
        fontSize=10,
        textColor='#2c3e50',
        spaceAfter=12,
        leftIndent=20
    )

    # Date style
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=8,
        textColor='#95a5a6',
        spaceAfter=6,
        leftIndent=20
    )

    # Add title
    title = Paragraph(f"{target_user.username} - Entry'ler", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))

    # Helper function to escape HTML entities and handle special chars
    def clean_text(text):
        if not text:
            return ""
        # Replace HTML-like characters
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        # Handle line breaks
        text = text.replace('\n', '<br/>')
        return text

    # Recursive function to add questions and their tree
    def add_question_tree(question, level=1, visited=None):
        if visited is None:
            visited = set()
        if question.id in visited:
            return
        visited.add(question.id)

        # Choose heading style based on level
        if level == 1:
            heading_style = h1_style
        elif level == 2:
            heading_style = h2_style
        else:
            heading_style = h3_style

        # Add question heading
        question_para = Paragraph(clean_text(question.question_text), heading_style)
        elements.append(question_para)
        elements.append(Spacer(1, 0.1*inch))

        # Add user's answers to this question
        user_answers = question.answers.filter(user=target_user).order_by('created_at')
        for answer in user_answers:
            # Add date
            date_str = answer.created_at.strftime("%Y-%m-%d %H:%M")
            date_para = Paragraph(f"<i>{date_str}</i>", date_style)
            elements.append(date_para)

            # Add answer text
            answer_para = Paragraph(clean_text(answer.answer_text), answer_style)
            elements.append(answer_para)
            elements.append(Spacer(1, 0.15*inch))

        # Process subquestions recursively (kullanıcı-bazlı)
        subquestions_rels = QuestionRelationship.objects.filter(
            parent=question,
            user=target_user
        ).select_related('child').order_by('created_at')
        for rel in subquestions_rels:
            add_question_tree(rel.child, level=min(level+1, 3), visited=visited)

    # Add all questions
    for question in user_questions:
        add_question_tree(question, level=1)
        # Add page break after each main question
        elements.append(PageBreak())

    # Build PDF
    doc.build(elements)

    # Get PDF from buffer
    buffer.seek(0)
    pdf_content = buffer.read()

    # Create response
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{target_user.username}_entries.pdf"'
    return response


@login_required
def filter_answers(request, slug):
    """
    Ajax filtre endpoint'i.
    Soruya ait yanıtları, my_answers / followed / username / keyword'e göre süzer
    ve 'core/_answers_list.html' partial'ını döndürür.
    """
    question = get_object_or_404(Question, slug=slug)

    # Parametreler
    my_answers = request.GET.get('my_answers')
    followed = request.GET.get('followed')
    username = request.GET.get('username', '').strip()
    keyword = request.GET.get('keyword', '').strip()

    # Tüm yanıtlar (bu soru altındaki)
    answers = question.answers.all().order_by('created_at')

    # 1) Kendi yanıtlarım
    if my_answers == 'on':
        answers = answers.filter(user=request.user)

    # 2) Takip ettiklerim
    if followed == 'on':
        user_profile = request.user.userprofile
        followed_profiles = user_profile.following.all()
        followed_users = [p.user for p in followed_profiles]
        answers = answers.filter(user__in=followed_users)

    # 3) Kullanıcı adı (kısmi eşleşme)
    if username:
        answers = answers.filter(user__username__icontains=username)

    # 4) Kelime arama
    if keyword:
        answers = answers.filter(answer_text__icontains=keyword)

    # Kaydetme/Oylama bilgileri
    content_type_answer = ContentType.objects.get_for_model(Answer)
    answer_ids = answers.values_list('id', flat=True)

    # Kaydedilme sayıları
    saved_items = SavedItem.objects.filter(
        content_type=content_type_answer,
        object_id__in=answer_ids
    ).values('object_id').annotate(count=Count('id'))
    answer_save_dict = {item['object_id']: item['count'] for item in saved_items}

    # Kullanıcının kaydettiği yanıtlar
    saved_answer_ids = SavedItem.objects.filter(
        user=request.user,
        content_type=content_type_answer,
        object_id__in=answer_ids
    ).values_list('object_id', flat=True)

    # Kullanıcının oy bilgisi
    user_votes = Vote.objects.filter(
        user=request.user,
        content_type=content_type_answer,
        object_id__in=answer_ids
    ).values('object_id', 'value')
    user_vote_dict = {v['object_id']: v['value'] for v in user_votes}

    # up/down hesaplama
    for ans in answers:
        ans.user_vote_value = user_vote_dict.get(ans.id, 0)
        ans.upvotes = Vote.objects.filter(object_id=ans.id, value=1).count()
        ans.downvotes = Vote.objects.filter(object_id=ans.id, value=-1).count()

    # partial HTML döndür
    html_content = render_to_string(
        'core/_answers_list.html',
        {
            'answers': answers,
            'question': question,
            'answer_save_dict': answer_save_dict,
            'saved_answer_ids': saved_answer_ids,
            'search_keyword': keyword,
        },
        request=request
    )
    return HttpResponse(html_content)
