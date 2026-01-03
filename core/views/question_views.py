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
from collections import defaultdict
from datetime import timedelta

from django.contrib import messages
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
)
from ..forms import AnswerForm, QuestionForm, StartingQuestionForm
from ..querysets import get_today_questions_queryset
from ..utils import paginate_queryset
from ..services import VoteSaveService
from .user_views import get_user_color


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
                Q(user_id__in=followed_user_ids) |  # Soruyu oluşturan takip edilen biri
                Q(answers__user_id__in=followed_user_ids)  # Cevap veren takip edilen biri
            ).distinct()
        except UserProfile.DoesNotExist:
            all_questions = Question.objects.none()

    q_page_number = request.GET.get('q_page', 1)
    q_paginator = Paginator(all_questions, 20)
    all_questions_page = q_paginator.get_page(q_page_number)

    # Soru nesnesini al (slug ile)
    question = get_object_or_404(Question, slug=slug)

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

    starting_question_ids = set(StartingQuestion.objects.values_list('question_id', flat=True))

    # Kullanıcı-bazlı parent kontrolü
    if request.user.is_authenticated:
        has_parent = QuestionRelationship.objects.filter(
            child=question,
            user=request.user
        ).exists()
    else:
        has_parent = False
    is_on_map = (question.id in starting_question_ids) or has_parent

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
        form = QuestionForm()

    # Kullanıcının önceki tanımlarını getir
    from ..models import Definition
    user_definitions = Definition.objects.filter(user=request.user).select_related('question').order_by('-created_at')[:10]

    context = {
        'form': form,
        'parent_question': parent_question,
        'all_questions': all_questions,
        'user_definitions': user_definitions,
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


@login_required
def add_question_from_search(request):
    all_questions = get_today_questions_queryset()
    query = request.GET.get('q', '').strip()

    # Taslak yükleme (draft_id parametresi varsa)
    draft_content = None
    draft_id = request.GET.get('draft_id')
    if draft_id:
        try:
            taslak = Kenarda.objects.get(pk=draft_id, user=request.user)
            draft_content = taslak.content
            # Query yoksa, taslak başlığından al
            if not query and taslak.title:
                query = taslak.title
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


@login_required
def question_map(request):
    question_id = request.GET.get('question_id', None)
    # Başlangıç soruları
    starting_question_ids = StartingQuestion.objects.values_list('question_id', flat=True)
    # Haritada görünmesi gereken sorular:
    # 1. Başlangıç soruları
    # 2. En az bir parent'ı olan sorular (alt sorular)
    # 3. En az bir subquestion'ı olan sorular (üst sorular)
    questions = Question.objects.filter(
        Q(id__in=starting_question_ids) |
        Q(parent_questions__isnull=False) |
        Q(subquestions__isnull=False)
    ).distinct()

    nodes = {}
    links = []
    question_text_to_ids = defaultdict(list)

    # Build nodes dictionary keyed by question_text
    for question in questions:
        key = question.question_text
        question_text_to_ids[key].append(question.id)
        if key not in nodes:
            associated_users = list(question.users.all())
            user_ids = [user.id for user in associated_users]
            node = {
                "id": f"q{hash(key)}",  # Unique ID based on question_text
                "label": question.question_text,
                "users": user_ids,
                "size": 20 + 10 * (len(user_ids) - 1),
                "color": '',
                "question_id": question.id,  # Store a valid question ID
                "question_ids": [question.id],  # List of question IDs with same text
            }
            # Assign color based on user IDs
            if len(user_ids) == 1:
                node["color"] = get_user_color(user_ids[0])
            elif len(user_ids) > 1:
                node["color"] = '#CCCCCC'  # Grey for multiple users
            else:
                node["color"] = '#000000'  # Black if no user
            nodes[key] = node
        else:
            # Merge user IDs and update size
            existing_node = nodes[key]
            new_user_ids = [user.id for user in question.users.all()]
            combined_user_ids = list(set(existing_node["users"] + new_user_ids))
            existing_node["users"] = combined_user_ids
            existing_node["size"] = 20 + 5 * (len(combined_user_ids) - 1)
            existing_node["question_ids"].append(question.id)
            # Update color
            if len(combined_user_ids) == 1:
                existing_node["color"] = get_user_color(combined_user_ids[0])
            elif len(combined_user_ids) > 1:
                existing_node["color"] = '#CCCCCC'
            else:
                existing_node["color"] = '#000000'

    # Build links using question_text as keys
    link_set = set()
    for question in questions:
        source_key = question.question_text
        for subquestion in question.subquestions.all():
            target_key = subquestion.question_text
            if target_key in nodes:
                link_id = (nodes[source_key]["id"], nodes[target_key]["id"])
                if link_id not in link_set:
                    links.append({
                        "source": nodes[source_key]["id"],
                        "target": nodes[target_key]["id"]
                    })
                    link_set.add(link_id)

    question_nodes = {
        "nodes": list(nodes.values()),
        "links": links
    }
    return render(request, 'core/question_map.html', {
        'question_nodes': question_nodes,
        'focus_question_id': question_id,
    })


@login_required
def map_data_view(request):
    user_ids = request.GET.getlist('user_id')
    filter_param = request.GET.get('filter')
    hashtag_name = request.GET.get('hashtag')

    # Haritada görünmesi gereken sorular:
    # 1. Başlangıç soruları
    # 2. En az bir parent'ı olan sorular (QuestionRelationship'te child olarak)
    # 3. En az bir child'ı olan sorular (QuestionRelationship'te parent olarak)
    starting_question_ids = StartingQuestion.objects.values_list('question_id', flat=True)

    # QuestionRelationship'ten child olan soruları al
    child_question_ids = QuestionRelationship.objects.values_list('child_id', flat=True).distinct()

    # QuestionRelationship'ten parent olan soruları al
    parent_question_ids = QuestionRelationship.objects.values_list('parent_id', flat=True).distinct()

    question_ids = set(starting_question_ids) | set(child_question_ids) | set(parent_question_ids)

    # Sadece bu question'ları çek
    queryset = Question.objects.filter(id__in=question_ids)

    # Filtre uygula
    if filter_param == 'me':
        queryset = queryset.filter(users=request.user)
    elif user_ids:
        queryset = queryset.filter(users__id__in=user_ids).distinct()

    # Hashtag filtresi
    if hashtag_name:
        from core.models import Hashtag
        try:
            hashtag = Hashtag.objects.get(name=hashtag_name)
            # Get all answers that use this hashtag
            answer_ids = hashtag.usages.values_list('answer_id', flat=True)
            # Filter questions that have answers with this hashtag
            queryset = queryset.filter(answers__id__in=answer_ids).distinct()
        except Hashtag.DoesNotExist:
            queryset = queryset.none()

    # Düğümleri oluştur ve JSON olarak döndür
    # user_filter: Eğer user_ids belirtilmişse sadece o kullanıcıların ilişkilerini göster
    filter_user_ids = None
    if filter_param == 'me' and request.user.is_authenticated:
        filter_user_ids = [request.user.id]
    elif user_ids:
        filter_user_ids = [int(uid) for uid in user_ids]

    data = generate_question_nodes(queryset, user_filter=filter_user_ids)
    return JsonResponse(data, safe=False)


def generate_question_nodes(questions, user_filter=None):
    """
    Generate nodes and links for the question map.

    Args:
        questions: QuerySet of questions to include in the map
        user_filter: List of user IDs to filter relationships by (None = show all users' relationships)
    """
    nodes = []
    links = []

    # Prefetch answers and users to avoid N+1 queries
    questions = questions.prefetch_related(
        'users',
        'answers__user'
    )

    question_ids = set(q.id for q in questions)

    # Build nodes first
    for question in questions:
        user_entries = []

        # Build a lookup dict for answers by user_id
        answers_by_user = {}
        for answer in question.answers.all():
            user_id = answer.user.id
            if user_id not in answers_by_user:
                answers_by_user[user_id] = answer
            elif answer.created_at < answers_by_user[user_id].created_at:
                # Keep the earliest answer
                answers_by_user[user_id] = answer

        for user in question.users.all():
            answer = answers_by_user.get(user.id)
            answer_id = answer.id if answer else None
            user_entries.append({
                "id": user.id,
                "username": user.username,
                "answer_id": answer_id,
            })

        user_ids = [entry["id"] for entry in user_entries]

        # Color logic: single user gets their color, multiple users get neutral colors based on activity
        if len(user_ids) == 1:
            node_color = get_user_color(user_ids[0])
        elif len(user_ids) >= 5:
            node_color = '#ff6b6b'  # Red for very active nodes (5+ users)
        elif len(user_ids) >= 2:
            node_color = '#9370db'  # Purple for multi-user nodes (2-4 users)
        else:
            node_color = '#87ceeb'  # Sky blue fallback

        node = {
            "id": f"q{question.id}",
            "label": question.question_text,
            "users": user_entries,
            "user_ids": user_ids,  # Add user_ids for statistics calculation
            "size": 20 + 10 * (len(user_entries) - 1),  # Will be updated based on links
            "color": node_color,
            "question_id": question.id,
            "question_ids": [question.id],
            "slug": question.slug,  # Add slug for navigation
        }
        nodes.append(node)

    # Build links from QuestionRelationship model
    link_count = {}  # Track how many links each node has

    # Query QuestionRelationship with user filter
    relationship_query = QuestionRelationship.objects.filter(
        parent_id__in=question_ids,
        child_id__in=question_ids
    ).select_related('parent', 'child', 'user')

    # Apply user filter if specified
    if user_filter:
        relationship_query = relationship_query.filter(user_id__in=user_filter)

    # Build links from relationships
    for rel in relationship_query:
        parent_id = f"q{rel.parent_id}"
        child_id = f"q{rel.child_id}"

        links.append({
            "source": parent_id,
            "target": child_id,
            "user_id": rel.user_id,  # Track which user created this link
        })

        # Increment link count for both nodes
        link_count[parent_id] = link_count.get(parent_id, 0) + 1
        link_count[child_id] = link_count.get(child_id, 0) + 1

    # Update node sizes based on link count (each link adds 0.1 to size)
    for node in nodes:
        node_id = node["id"]
        num_links = link_count.get(node_id, 0)
        # Base size + user-based size + link-based size (0.1 per link)
        base_size = 20 + 10 * (len(node["users"]) - 1)
        node["size"] = base_size + (num_links * 0.1)

    return {
        "nodes": nodes,
        "links": links,
    }


def bkz_view(request, query):
    # Birden fazla aynı isimli soru olabilir, ilkini al (büyük/küçük harf duyarsız)
    question = Question.objects.filter(question_text__iexact=query).first()
    if question:
        return redirect('question_detail', slug=question.slug)
    else:
        # Soru bulunamazsa, add_question_from_search sayfasına yönlendirin
        return redirect(f'{reverse("add_question_from_search")}?q={query}')


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


@login_required
def add_existing_subquestion(request, slug):
    """Add current question as a subquestion to a selected parent question"""
    current_question = get_object_or_404(Question, slug=slug)

    if request.method == 'POST':
        parent_question_id = request.POST.get('subquestion_id')  # Confusingly named in JS, but this is the parent
        if not parent_question_id:
            return JsonResponse({'success': False, 'error': 'Soru ID eksik'}, status=400)

        try:
            parent_question = Question.objects.get(id=parent_question_id)
        except Question.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Soru bulunamadı'}, status=404)

        # Kendine bağlama kontrolü
        if current_question.id == parent_question.id:
            return JsonResponse({'success': False, 'error': 'Bir soru kendisine alt soru olarak eklenemez'}, status=400)

        # Zaten bağlı mı kontrolü (kullanıcı bazlı)
        if QuestionRelationship.objects.filter(
            parent=parent_question,
            child=current_question,
            user=request.user
        ).exists():
            return JsonResponse({'success': False, 'error': 'Bu başlık zaten seçilen başlığın alt sorusu'}, status=400)

        # Döngüsel bağlantı kontrolü
        if would_create_cycle_user_based(parent_question, current_question, request.user):
            return JsonResponse({'success': False, 'error': 'Bu bağlantı döngüsel bir ilişki oluşturacak'}, status=400)

        # İki başlangıç sorusu birbirine eklenemez kontrolü
        parent_is_starting = StartingQuestion.objects.filter(question=parent_question, user=request.user).exists()
        child_is_starting = StartingQuestion.objects.filter(question=current_question, user=request.user).exists()

        if parent_is_starting and child_is_starting:
            return JsonResponse({'success': False, 'error': 'İki başlangıç sorusu birbirine eklenemez'}, status=400)

        # Kullanıcı-bazlı bağlantıyı ekle: parent_question -> current_question
        QuestionRelationship.objects.create(
            parent=parent_question,
            child=current_question,
            user=request.user
        )

        # Başlangıç sorusu yönetimi:
        # Eğer current_question birilerinin başlangıç sorusuysa,
        # o kullanıcılar için parent_question yeni başlangıç sorusu olur
        affected_starting_questions = StartingQuestion.objects.filter(question=current_question)
        if affected_starting_questions.exists():
            for sq in affected_starting_questions:
                user = sq.user
                # Önce eski başlangıç sorusunu sil
                sq.delete()
                # Sonra parent'ı yeni başlangıç sorusu yap (eğer zaten değilse)
                StartingQuestion.objects.get_or_create(user=user, question=parent_question)

        return JsonResponse({
            'success': True,
            'message': f'Bu başlık "{parent_question.question_text}" başlığının alt sorusu olarak eklendi',
            'parent_question_id': parent_question.id,
            'parent_question_text': parent_question.question_text
        })

    return JsonResponse({'success': False, 'error': 'Geçersiz istek'}, status=400)


def would_create_cycle(parent, potential_child):
    """Check if adding potential_child as subquestion would create a cycle"""
    visited = set()

    def has_path_to(current, target):
        """Check if there's a path from current to target following parent_questions"""
        if current.id == target.id:
            return True
        if current.id in visited:
            return False
        visited.add(current.id)

        # Check all parents of current
        for parent_q in current.parent_questions.all():
            if has_path_to(parent_q, target):
                return True
        return False

    # If parent is already an ancestor of potential_child, adding this link would create a cycle
    # Because: parent -> ... -> potential_child (already exists) + potential_child -> parent (new link) = cycle
    return has_path_to(parent, potential_child)


def would_create_cycle_user_based(parent, potential_child, user):
    """
    Kullanıcı-bazlı döngü kontrolü.
    Kullanıcının mevcut bağlantılarında parent'tan potential_child'a bir yol varsa döngü oluşur.
    """
    visited = set()

    def has_path_to(current, target):
        """Kullanıcının bağlantılarında current'tan target'a yol var mı?"""
        if current.id == target.id:
            return True
        if current.id in visited:
            return False
        visited.add(current.id)

        # Kullanıcının bu sorunun parent'ları arasında kontrol et
        parent_relationships = QuestionRelationship.objects.filter(
            child=current,
            user=user
        ).select_related('parent')

        for rel in parent_relationships:
            if has_path_to(rel.parent, target):
                return True
        return False

    return has_path_to(parent, potential_child)


@login_required
def search_questions_for_linking(request):
    """AJAX endpoint to search questions that current question can be added as subquestion to"""
    query = request.GET.get('q', '').strip()
    current_question_id = request.GET.get('parent_id')  # Actually current question, not parent

    if not query or not current_question_id:
        return JsonResponse({'results': []})

    try:
        current_question = Question.objects.get(id=current_question_id)
    except Question.DoesNotExist:
        return JsonResponse({'results': []})

    # Kullanıcının mevcut parent'larını al (kullanıcı-bazlı)
    user_parent_ids = QuestionRelationship.objects.filter(
        child=current_question,
        user=request.user
    ).values_list('parent_id', flat=True)

    # Tüm soruları ara (herkesin haritasındaki sorular dahil)
    questions = Question.objects.filter(
        question_text__icontains=query
    ).exclude(
        id=current_question_id  # Kendisini hariç tut
    ).exclude(
        id__in=user_parent_ids  # Kullanıcının bu sorusu için zaten parent olanları hariç tut
    ).distinct()[:10]

    results = [{
        'id': q.id,
        'text': q.question_text,
        'answer_count': q.answers.count()
    } for q in questions]

    return JsonResponse({'results': results})


@login_required
def unlink_from_parent(request, slug, parent_id):
    """
    Child question'ın perspective'inden: Bu soruyu belirtilen parent'tan ayırır.
    Eğer unlinking sonrası soru orphan kalırsa (hiç parent'ı yoksa),
    otomatik olarak StartingQuestion olarak eklenir.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST metodu gerekli'}, status=400)

    # Current question (child)
    current_question = get_object_or_404(Question, slug=slug)
    # Parent question
    parent_question = get_object_or_404(Question, id=parent_id)

    # İlişkinin gerçekten var olup olmadığını kontrol et (kullanıcı-bazlı)
    relationship_exists = QuestionRelationship.objects.filter(
        parent=parent_question,
        child=current_question,
        user=request.user
    ).exists()

    if not relationship_exists:
        return JsonResponse({'success': False, 'error': 'Bu soru zaten üst soru değil veya sizin bağlantınız yok'}, status=400)

    # İlişkiyi kaldır (sadece bu kullanıcı için)
    QuestionRelationship.objects.filter(
        parent=parent_question,
        child=current_question,
        user=request.user
    ).delete()

    # Orphan kontrolü: Eğer kullanıcının bu sorunun hiç parent'ı kalmadıysa, StartingQuestion olarak ekle
    user_parent_count = QuestionRelationship.objects.filter(
        child=current_question,
        user=request.user
    ).count()

    if user_parent_count == 0:
        # Eğer zaten StartingQuestion değilse ekle
        if not StartingQuestion.objects.filter(question=current_question, user=request.user).exists():
            # Bağlantıyı koparan kullanıcı için starting question olarak ekle
            StartingQuestion.objects.create(
                user=request.user,
                question=current_question
            )

    # Parent kontrolü: Bu kullanıcı için parent'ın başka child'ı var mı?
    parent_children_count = QuestionRelationship.objects.filter(
        parent=parent_question,
        user=request.user
    ).count()

    if parent_children_count == 0:
        # Parent'ın artık hiç child'ı yok (bu kullanıcı için)
        # Parent'ın StartingQuestion kaydını sil (ilişki kaydı, Question nesnesi değil)
        StartingQuestion.objects.filter(
            question=parent_question,
            user=request.user
        ).delete()

    return JsonResponse({
        'success': True,
        'message': f'"{parent_question.question_text}" sorusundan bağlantı kaldırıldı'
    })


@login_required
def search_questions_for_merging(request):
    """
    Admin-only search endpoint for merging questions.
    Returns {id, slug, text, answer_count} results.
    """
    if not request.user.is_superuser:
        return HttpResponseForbidden("Bu işlem sadece admin içindir.")

    query = (request.GET.get('q') or '').strip()
    exclude_id = request.GET.get('exclude_id')
    if len(query) < 2:
        return JsonResponse({'results': []})

    qs = Question.objects.filter(question_text__icontains=query)
    if exclude_id:
        try:
            qs = qs.exclude(id=int(exclude_id))
        except (TypeError, ValueError):
            pass

    qs = qs.annotate(answer_count=Count('answers')).order_by('-created_at')[:10]
    results = [
        {'id': q.id, 'slug': q.slug, 'text': q.question_text, 'answer_count': q.answer_count}
        for q in qs
    ]
    return JsonResponse({'results': results})


@require_POST
@login_required
def admin_merge_question(request, slug):
    """
    Admin-only: move ALL answers from the source question into the target question,
    then delete the source question.

    Rules:
    - Only admin (superuser) can run.
    - Move all Answer rows (entryler) to target.
    - Delete question-level votes/saves/follows for source (answer-level stays).
    - Move map relations (StartingQuestion + QuestionRelationship) to target.
    - Keep other user content that is question-bound (e.g. drafts/definitions/hashtags) by re-pointing.
    """
    if not request.user.is_superuser:
        return HttpResponseForbidden("Bu işlem sadece admin içindir.")

    target_id = request.POST.get('target_id')
    confirm = request.POST.get('confirm_merge')
    if not target_id or confirm != '1':
        messages.error(request, "Hedef başlık seçin ve onaylayın.")
        return redirect('question_detail', slug=slug)

    try:
        target_id_int = int(target_id)
    except (TypeError, ValueError):
        messages.error(request, "Geçersiz hedef başlık.")
        return redirect('question_detail', slug=slug)

    with transaction.atomic():
        source = get_object_or_404(Question.objects.select_for_update(), slug=slug)
        target = get_object_or_404(Question.objects.select_for_update(), id=target_id_int)

        if source.id == target.id:
            messages.error(request, "Kaynak ve hedef aynı olamaz.")
            return redirect('question_detail', slug=slug)

        source_title = source.question_text
        target_title = target.question_text

        # 0) Transfer legacy Question.subquestions graph (older map model)
        # Move outgoing links (source -> child) to (target -> child)
        for child in source.subquestions.all():
            if child.id != target.id:
                target.subquestions.add(child)
        # Move incoming links (parent -> source) to (parent -> target)
        for parent in source.parent_questions.all():
            if parent.id != target.id:
                parent.subquestions.add(target)
            parent.subquestions.remove(source)

        # 1) Move answers (entryler) and append them to the end of the target thread.
        # We preserve the relative order of moved answers, but shift their timestamps
        # to be after the latest existing answer in the target question.
        target_latest = Answer.objects.filter(question=target).aggregate(latest=Max('created_at')).get('latest')
        base_time = target_latest or timezone.now()

        source_answers = list(
            Answer.objects.select_for_update()
            .filter(question=source)
            .order_by('created_at', 'id')
        )
        for i, ans in enumerate(source_answers, start=1):
            shifted = base_time + timedelta(seconds=i)
            ans.question = target
            ans.created_at = shifted
            ans.updated_at = shifted
        if source_answers:
            Answer.objects.bulk_update(source_answers, ['question', 'created_at', 'updated_at'])

        # 2) Move user-generated question-bound content that should not disappear
        Definition.objects.filter(question=source).update(question=target)
        Kenarda.objects.filter(question=source).update(question=target)
        HashtagUsage.objects.filter(question=source).update(question=target)

        # 3) Merge question users set (used by map/node coloring)
        target.users.add(*source.users.all())

        # 4) Move map relations: StartingQuestion
        starting_rows = list(StartingQuestion.objects.select_for_update().filter(question=source))
        for sq in starting_rows:
            if StartingQuestion.objects.filter(user=sq.user, question=target).exists():
                sq.delete()
            else:
                sq.question = target
                sq.save(update_fields=['question'])

        # 5) Move map relations: user-based QuestionRelationship edges
        rel_rows = list(
            QuestionRelationship.objects.select_for_update().filter(
                Q(parent=source) | Q(child=source)
            )
        )
        for rel in rel_rows:
            new_parent = target if rel.parent_id == source.id else rel.parent
            new_child = target if rel.child_id == source.id else rel.child

            # Drop self-links
            if new_parent.id == new_child.id:
                rel.delete()
                continue

            exists = QuestionRelationship.objects.filter(
                parent=new_parent,
                child=new_child,
                user=rel.user
            ).exists()
            if not exists:
                QuestionRelationship.objects.create(
                    parent=new_parent,
                    child=new_child,
                    user=rel.user,
                    created_at=rel.created_at,
                )
            rel.delete()

        # 6) Delete question-level interactions for source
        content_type_question = ContentType.objects.get_for_model(Question)
        SavedItem.objects.filter(content_type=content_type_question, object_id=source.id).delete()
        Vote.objects.filter(content_type=content_type_question, object_id=source.id).delete()
        QuestionFollow.objects.filter(question=source).delete()

        # 7) Finally delete the source question
        source.delete()

    messages.success(
        request,
        f'"{source_title}" başlığındaki entryler "{target_title}" başlığına taşındı ve eski başlık silindi.'
    )
    return redirect('question_detail', slug=target.slug)
