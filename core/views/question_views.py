"""
Question-related views
- question_detail
- add_question
- add_subquestion
- delete_question
- delete_question_and_subquestions
- add_question_from_search
- question_map
- map_data_view
- generate_question_nodes
- bkz_view
- add_starting_question
- get_user_questions
"""

import json
import re
from collections import defaultdict, deque
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q, Count, Max
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme

from ..models import (
    Question,
    Answer,
    SavedItem,
    Vote,
    StartingQuestion,
    Kenarda,
    UserProfile,
    QuestionFollow,
    AnswerFollow,
    QuestionRelationship,
    Definition,
    HashtagUsage,
    Notification,
)
from ..forms import AnswerForm, QuestionForm, StartingQuestionForm
from ..querysets import get_today_questions_queryset, get_active_left_frame_pin_q
from ..utils import paginate_queryset
from ..services import VoteSaveService
from ..answer_git import attach_answer_revision_metadata
from .user_views import get_user_color

UNICODE_ESCAPE_RE = re.compile(r'\\u([0-9a-fA-F]{4})')
HEX_ESCAPE_RE = re.compile(r'\\x([0-9a-fA-F]{2})')


def _decode_legacy_js_escapes(value: str) -> str:
    if not isinstance(value, str) or '\\' not in value:
        return value
    value = UNICODE_ESCAPE_RE.sub(lambda m: chr(int(m.group(1), 16)), value)
    value = HEX_ESCAPE_RE.sub(lambda m: chr(int(m.group(1), 16)), value)
    return value


def _redirect_back_with_writer_warning(request):
    messages.warning(request, "Bu başlığı açmak için yazar olmalısınız.")
    referer = request.META.get("HTTP_REFERER", "")
    if referer and url_has_allowed_host_and_scheme(
        referer,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(referer)
    return redirect("user_homepage")


def question_detail(request, slug):
    # Public view - anyone can see questions and answers

    # Takip ettiklerim filtresi (sidebar için)
    followed_param = request.GET.get('followed', '0')
    show_followed_only = followed_param == '1'

    # Soldaki tüm sorular ve pagination
    all_questions = get_today_questions_queryset()

    # Takip ettiklerim filtresi uygulanırsa
    if show_followed_only and request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
            # UserProfile'dan User ID'lerini al
            followed_user_ids = user_profile.following.values_list('user_id', flat=True)
            # Takip edilen kullanıcıların ya soru oluşturduğu ya da cevap verdiği başlıkları göster
            all_questions = all_questions.filter(
                get_active_left_frame_pin_q() |
                Q(user_id__in=followed_user_ids) |  # Soruyu oluşturan takip edilen biri
                Q(answers__user_id__in=followed_user_ids)  # Cevap veren takip edilen biri
            ).distinct()
        except UserProfile.DoesNotExist:
            all_questions = Question.objects.none()

    q_page_number = request.GET.get('q_page', 1)
    q_paginator = Paginator(all_questions, 20)
    all_questions_page = q_paginator.get_page(q_page_number)

    # Soru nesnesini al (slug ile)
    question = get_object_or_404(Question.objects.select_related('user'), slug=slug)

    # Filtre parametreleri
    my_answers = request.GET.get('my_answers')
    followed = request.GET.get('followed')
    username = request.GET.get('username', '').strip()
    keyword  = request.GET.get('keyword', '').strip()

    # Optimize with select_related to prevent N+1 queries
    all_answers = question.answers.select_related(
        'user',
        'user__userprofile'
    ).order_by('created_at')

    if my_answers == 'on':
        all_answers = all_answers.filter(user=request.user)
    if followed == 'on':
        followed_users = request.user.userprofile.following.all()
        all_answers = all_answers.filter(user__in=followed_users)
    if username:
        all_answers = all_answers.filter(user__username__iexact=username)
    if keyword:
        all_answers = all_answers.filter(answer_text__icontains=keyword)

    a_page_number = request.GET.get('a_page', 1)
    a_paginator = Paginator(all_answers, 10)
    answers_page = a_paginator.get_page(a_page_number)
    answers_page.object_list = attach_answer_revision_metadata(list(answers_page.object_list), current_user=request.user)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            new_answer = form.save(commit=False)
            new_answer.user = request.user
            new_answer.question = question
            new_answer.save()
            Kenarda.objects.filter(user=request.user, question=question, is_sent=False).delete()
            return redirect('single_answer', slug=question.slug, answer_id=new_answer.id)
    else:
        form = AnswerForm()

    content_type_question = ContentType.objects.get_for_model(Question)
    if request.user.is_authenticated:
        user_has_saved_question = SavedItem.objects.filter(
            user=request.user,
            content_type=content_type_question,
            object_id=question.id
        ).exists()
    else:
        user_has_saved_question = False
    question_save_count = SavedItem.objects.filter(
        content_type=content_type_question,
        object_id=question.id
    ).count()

    content_type_answer = ContentType.objects.get_for_model(Answer)
    page_answer_ids = [ans.id for ans in answers_page]

    if request.user.is_authenticated:
        user_votes = Vote.objects.filter(
            user=request.user,
            content_type=content_type_answer,
            object_id__in=page_answer_ids
        ).values('object_id', 'value')
        user_vote_dict = {vote['object_id']: vote['value'] for vote in user_votes}
        for ans in answers_page:
            ans.user_vote_value = user_vote_dict.get(ans.id, 0)
        saved_answer_ids = SavedItem.objects.filter(
            user=request.user,
            content_type=content_type_answer,
            object_id__in=page_answer_ids
        ).values_list('object_id', flat=True)
    else:
        for ans in answers_page:
            ans.user_vote_value = 0
        saved_answer_ids = []
    answer_save_counts = SavedItem.objects.filter(
        content_type=content_type_answer,
        object_id__in=page_answer_ids
    ).values('object_id').annotate(count=Count('id'))
    answer_save_dict = {item['object_id']: item['count'] for item in answer_save_counts}

    # Kullanıcı-bazlı parent kontrolü
    if request.user.is_authenticated:
        has_parent = QuestionRelationship.objects.filter(
            child=question,
            user=request.user
        ).exists()
    else:
        has_parent = False
    is_starting_question = StartingQuestion.objects.filter(question=question).exists()
    is_on_map = is_starting_question or has_parent

    # Bu sorunun TÜM alt sorularını al (kim eklerse eklesin)
    # Her bir unique child için, onu ekleyen kullanıcıları da bilmemiz gerekiyor
    subquestion_rels = QuestionRelationship.objects.filter(
        parent=question
    ).select_related('child', 'child__user', 'user').order_by('created_at')

    # Alt soruları grupla: {child_question: [users who added it]}
    from collections import defaultdict
    subquestions_map = defaultdict(list)
    for rel in subquestion_rels:
        subquestions_map[rel.child].append(rel.user)

    # Liste formatına çevir
    subquestions_list = [
        {'question': child, 'added_by_users': users}
        for child, users in subquestions_map.items()
    ]

    # Bu soruyu alt soru olarak ekleyen TÜM üst soruları al
    parent_rels = QuestionRelationship.objects.filter(
        child=question
    ).select_related('parent', 'parent__user', 'user').order_by('created_at')

    # Üst soruları grupla: {parent_question: [users who added this link]}
    parents_map = defaultdict(list)
    for rel in parent_rels:
        parents_map[rel.parent].append(rel.user)

    # Liste formatına çevir
    parents_list = [
        {'question': parent, 'added_by_users': users}
        for parent, users in parents_map.items()
    ]

    # Takip bilgileri
    user_is_following_question = False
    followed_answer_ids = []
    if request.user.is_authenticated:
        user_is_following_question = QuestionFollow.objects.filter(
            user=request.user,
            question=question
        ).exists()

        # Hangi yanıtları takip ediyor
        followed_answer_ids = list(AnswerFollow.objects.filter(
            user=request.user,
            answer__in=answers_page
        ).values_list('answer_id', flat=True))

    # Taslak yükleme (draft_id parametresi varsa)
    draft_content = None
    if request.user.is_authenticated:
        draft_id = request.GET.get('draft_id')
        if draft_id:
            try:
                taslak = Kenarda.objects.get(pk=draft_id, user=request.user, question=question)
                draft_content = taslak.content
            except Kenarda.DoesNotExist:
                pass

    context = {
        'question': question,
        'form': form,
        'all_questions_page': all_questions_page,
        'answers_page': answers_page,
        'user_has_saved_question': user_has_saved_question,
        'question_save_count': question_save_count,
        'saved_answer_ids': list(saved_answer_ids),
        'answer_save_dict': answer_save_dict,
        'my_answers': my_answers,
        'followed': followed,
        'filter_username': username,
        'filter_keyword': keyword,
        'is_on_map': is_on_map,
        'show_followed_only': show_followed_only,
        'user_is_following_question': user_is_following_question,
        'followed_answer_ids': followed_answer_ids,
        'subquestions_list': subquestions_list,
        'parents_list': parents_list,
        'draft_content': draft_content,
    }
    return render(request, 'core/question_detail.html', context)


@login_required
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data['question_text']
            # Aynı soru metni varsa mevcut olanı kullan
            question, created = Question.objects.get_or_create(
                question_text=question_text,
                defaults={'user': request.user}
            )
            question.users.add(request.user)
            question.save()
            # Başlangıç sorusu olarak ekle
            StartingQuestion.objects.create(user=request.user, question=question)

            # Tanım varsa al (Definition modeli için)
            definition_text = request.POST.get('definition_text', '').strip()

            # Yanıt metnini al (frontend zaten tanımı eklemiş olabilir)
            answer_text = form.cleaned_data.get('answer_text', '').strip()

            # Yanıt oluştur
            answer = Answer.objects.create(
                question=question,
                user=request.user,
                answer_text=answer_text  # Frontend zaten birleştirdi
            )

            # Eğer tanım girilmişse, Definition oluştur
            if definition_text:
                from ..models import Definition
                Definition.objects.create(
                    user=request.user,
                    question=question,
                    definition_text=definition_text,
                    answer=answer
                )

            return redirect('user_homepage')
    else:
        form = QuestionForm()

    # Kullanıcının önceki tanımlarını getir
    from ..models import Definition
    user_definitions = Definition.objects.filter(user=request.user).select_related('question').order_by('-created_at')[:10]

    return render(request, 'core/add_question.html', {
        'form': form,
        'user_definitions': user_definitions,
    })


@login_required
def add_subquestion(request, slug):
    parent_question = get_object_or_404(Question, slug=slug)
    all_questions = get_today_questions_queryset()
    draft_title = None
    draft_content = None

    draft_id = request.GET.get('draft_id')
    if draft_id:
        try:
            taslak = Kenarda.objects.get(
                pk=draft_id,
                user=request.user,
                question=parent_question,
                answer__isnull=True,
                is_sent=False,
                draft_source='subquestion',
            )
            draft_title = taslak.title
            draft_content = taslak.content
        except Kenarda.DoesNotExist:
            pass

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            subquestion_text = form.cleaned_data['question_text']
            answer_text = form.cleaned_data.get('answer_text', '')
            definition_text = request.POST.get('definition_text', '')

            # Yeni veya mevcut alt soruyu oluştururken 'user' bilgisini ekliyoruz
            subquestion, created = Question.objects.get_or_create(
                question_text=subquestion_text,
                defaults={'user': request.user}
            )
            subquestion.users.add(request.user)
            # Kullanıcı-bazlı ilişki oluştur
            QuestionRelationship.objects.get_or_create(
                parent=parent_question,
                child=subquestion,
                user=request.user
            )

            # Yanıtı kaydet
            answer = Answer.objects.create(
                question=subquestion,
                user=request.user,
                answer_text=answer_text
            )

            # Eğer tanım girilmişse, Definition oluştur
            if definition_text:
                from ..models import Definition
                Definition.objects.create(
                    user=request.user,
                    question=subquestion,
                    definition_text=definition_text,
                    answer=answer
                )

            messages.success(request, 'Alt soru başarıyla eklendi.')
            return redirect('question_detail', slug=subquestion.slug)
    else:
        form = QuestionForm(initial={
            'question_text': draft_title or '',
            'answer_text': draft_content or '',
        })

    # Kullanıcının önceki tanımlarını getir
    from ..models import Definition
    user_definitions = Definition.objects.filter(user=request.user).select_related('question').order_by('-created_at')[:10]

    context = {
        'form': form,
        'parent_question': parent_question,
        'all_questions': all_questions,
        'user_definitions': user_definitions,
        'draft_title': draft_title,
        'draft_content': draft_content,
    }
    return render(request, 'core/add_subquestion.html', context)


@login_required
def delete_question(request, slug):
    question = get_object_or_404(Question, slug=slug)

    if request.method == 'POST':
        if request.user == question.user:
            with transaction.atomic():
                # Delete all answers associated with the question by the user
                Answer.objects.filter(question=question, user=request.user).delete()
                # Remove the user from the question's users
                question.users.remove(request.user)
                if question.users.count() == 0:
                    # If no users are associated, delete the question and its subquestions
                    delete_question_and_subquestions(question)
                    messages.success(request, 'Soru ve alt soruları başarıyla silindi.')
                else:
                    messages.success(request, 'Soru sizin için silindi.')
            return redirect('user_homepage')
        else:
            messages.error(request, 'Bu soruyu silme yetkiniz yok.')
            return redirect('question_detail', slug=question.slug)
    else:
        return render(request, 'core/confirm_delete_question.html', {'question': question})


def delete_question_and_subquestions(question):
    subquestions = question.subquestions.all()
    for sub in subquestions:
        delete_question_and_subquestions(sub)
    question.delete()


def add_question_from_search(request):
    all_questions = get_today_questions_queryset()
    query = _decode_legacy_js_escapes(request.GET.get('q', '').strip())

    if not request.user.is_authenticated:
        return _redirect_back_with_writer_warning(request)

    # Taslak yükleme (draft_id parametresi varsa)
    draft_content = None
    draft_id = request.GET.get('draft_id')
    if draft_id:
        try:
            taslak = Kenarda.objects.get(pk=draft_id, user=request.user)
            draft_content = taslak.content
            # Query yoksa, taslak başlığından al
            if not query and taslak.title:
                query = _decode_legacy_js_escapes(taslak.title)
        except Kenarda.DoesNotExist:
            pass

    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            # Aynı soru metni varsa mevcut olanı kullan
            question, created = Question.objects.get_or_create(
                question_text=query,
                defaults={'user': request.user, 'from_search': True}
            )
            # Kullanıcıyı soru ile ilişkilendir
            question.users.add(request.user)

            # Tanım varsa al (Definition modeli için)
            definition_text = request.POST.get('definition_text', '').strip()

            # Yanıt metnini al (frontend zaten tanımı eklemiş olabilir)
            answer_text = answer_form.cleaned_data.get('answer_text', '').strip()

            # Yeni yanıt oluştur
            answer = answer_form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.answer_text = answer_text  # Frontend zaten birleştirdi
            answer.save()

            # Eğer tanım girilmişse, Definition oluştur
            if definition_text:
                from ..models import Definition
                Definition.objects.create(
                    user=request.user,
                    question=question,
                    definition_text=definition_text,
                    answer=answer
                )

            return redirect('single_answer', slug=question.slug, answer_id=answer.id)
    else:
        answer_form = AnswerForm()

    # Kullanıcının önceki tanımlarını getir
    from ..models import Definition
    user_definitions = Definition.objects.filter(user=request.user).select_related('question').order_by('-created_at')[:10]

    return render(request, 'core/add_question_from_search.html', {
        'query': query,
        'answer_form': answer_form,
        'all_questions': all_questions,
        'user_definitions': user_definitions,
        'draft_content': draft_content,
    })


from .question_map_views import (
    question_map,
    map_data_view,
    _build_answer_preview,
    _render_schema_answer_html,
    _to_roman,
    _get_schema_users,
    _resolve_schema_user_id,
    _get_user_schema_root_ids,
    _build_user_schema_graph,
    _build_schema_path_ids,
    question_schema,
    question_schema_children,
    question_schema_content,
    question_schema_search,
    generate_question_nodes,
)
def bkz_view(request, query):
    # Birden fazla aynı isimli soru olabilir, ilkini al (büyük/küçük harf duyarsız)
    question = Question.objects.filter(question_text__iexact=query).first()
    if question:
        return redirect('question_detail', slug=question.slug)
    else:
        if not request.user.is_authenticated:
            return _redirect_back_with_writer_warning(request)
        # Soru bulunamazsa, add_question_from_search sayfasına yönlendirin
        from urllib.parse import urlencode
        return redirect(f'{reverse("add_question_from_search")}?{urlencode({"q": query})}')


@login_required
def add_starting_question(request):
    all_questions = get_today_questions_queryset()
    if request.method == 'POST':
        form = StartingQuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data['question_text']
            question, created = Question.objects.get_or_create(
                question_text=question_text,
                defaults={'user': request.user}
            )
            question.users.add(request.user)
            question.save()
            StartingQuestion.objects.create(user=request.user, question=question)

            # Tanım varsa al (Definition modeli için)
            definition_text = request.POST.get('definition_text', '').strip()

            # Yanıt metnini al (frontend zaten tanımı eklemiş olabilir)
            answer_text = form.cleaned_data['answer_text'].strip()

            # Yanıt oluştur
            answer = Answer.objects.create(
                question=question,
                user=request.user,
                answer_text=answer_text  # Frontend zaten birleştirdi
            )

            # Eğer tanım girilmişse, Definition oluştur
            if definition_text:
                from ..models import Definition
                Definition.objects.create(
                    user=request.user,
                    question=question,
                    definition_text=definition_text,
                    answer=None  # Tanım metnin içinde gömülü
                )

            return redirect('question_detail', slug=question.slug)
    else:
        form = StartingQuestionForm()

    # Kullanıcının önceki tanımlarını getir
    from ..models import Definition
    user_definitions = Definition.objects.filter(user=request.user).select_related('question').order_by('-created_at')[:10]

    # Taslak yükleme (draft_id parametresi varsa)
    draft_title = None
    draft_content = None
    draft_id = request.GET.get('draft_id')
    if draft_id:
        try:
            taslak = Kenarda.objects.get(pk=draft_id, user=request.user)
            draft_title = taslak.title
            draft_content = taslak.content
        except Kenarda.DoesNotExist:
            pass

    return render(request, 'core/add_starting_question.html', {
        'form': form,
        'all_questions': all_questions,
        'user_definitions': user_definitions,
        'draft_title': draft_title,
        'draft_content': draft_content,
    })


from .question_link_views import (
    add_existing_subquestion,
    would_create_cycle,
    would_create_cycle_user_based,
    search_questions_for_linking,
    unlink_from_parent,
    search_questions_for_merging,
    admin_merge_question,
)

