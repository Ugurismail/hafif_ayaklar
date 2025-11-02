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

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from ..models import Question, Answer, SavedItem, Vote, StartingQuestion, Kenarda
from ..forms import AnswerForm, QuestionForm, StartingQuestionForm
from ..querysets import get_today_questions_queryset
from ..utils import paginate_queryset
from ..services import VoteSaveService


def get_user_color(user_id):
    """Helper function imported from user_views"""
    from .user_views import get_user_color as _get_user_color
    return _get_user_color(user_id)


@login_required
def get_user_questions(request):
    """This function is also in user_views.py - consider importing from there"""
    from .user_views import get_user_questions as _get_user_questions
    return _get_user_questions(request)


def question_detail(request, question_id):
    # Public view - anyone can see questions and answers
    # Soldaki tüm sorular ve pagination
    all_questions = get_today_questions_queryset()
    q_page_number = request.GET.get('q_page', 1)
    q_paginator = Paginator(all_questions, 20)
    all_questions_page = q_paginator.get_page(q_page_number)

    # Soru nesnesini al
    question = get_object_or_404(Question, id=question_id)

    # Filtre parametreleri
    my_answers = request.GET.get('my_answers')
    followed = request.GET.get('followed')
    username = request.GET.get('username', '').strip()
    keyword  = request.GET.get('keyword', '').strip()

    all_answers = question.answers.all().order_by('created_at')
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
            return redirect('question_detail', question_id=question.id)
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
    is_on_map = (question.id in starting_question_ids) or question.parent_questions.exists()

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
            # Yanıtı kaydet
            Answer.objects.create(
                question=question,
                user=request.user,
                answer_text=form.cleaned_data.get('answer_text', '')
            )
            return redirect('user_homepage')
    else:
        form = QuestionForm()
    return render(request, 'core/add_question.html', {'form': form})


@login_required
def add_subquestion(request, question_id):
    parent_question = get_object_or_404(Question, id=question_id)
    all_questions = get_today_questions_queryset()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            subquestion_text = form.cleaned_data['question_text']
            answer_text = form.cleaned_data.get('answer_text', '')
            # Yeni veya mevcut alt soruyu oluştururken 'user' bilgisini ekliyoruz
            subquestion, created = Question.objects.get_or_create(
                question_text=subquestion_text,
                defaults={'user': request.user}
            )
            subquestion.users.add(request.user)
            parent_question.subquestions.add(subquestion)
            # Yanıtı kaydet
            Answer.objects.create(
                question=subquestion,
                user=request.user,
                answer_text=answer_text
            )
            messages.success(request, 'Alt soru başarıyla eklendi.')
            return redirect('question_detail', question_id=subquestion.id)
    else:
        form = QuestionForm()
    context = {
        'form': form,
        'parent_question': parent_question,
        'all_questions': all_questions,
    }
    return render(request, 'core/add_subquestion.html', context)


@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

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
            return redirect('question_detail', question_id=question.id)
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

    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            # Yeni soru oluştur
            question = Question.objects.create(
                question_text=query,
                user=request.user,
                from_search=True  # Eğer modelinizde bu alan varsa
            )
            # Kullanıcıyı soru ile ilişkilendir
            question.users.add(request.user)

            # Yeni yanıt oluştur
            answer = answer_form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', question_id=question.id)
    else:
        answer_form = AnswerForm()
    return render(request, 'core/add_question_from_search.html', {
        'query': query,
        'answer_form': answer_form,
        'all_questions': all_questions,
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
        'question_nodes': json.dumps(question_nodes),
        'focus_question_id': question_id,
    })


@login_required
def map_data_view(request):
    user_ids = request.GET.getlist('user_id')
    filter_param = request.GET.get('filter')

    # Haritada görünmesi gereken sorular:
    # 1. Başlangıç soruları
    # 2. En az bir parent'ı olan sorular (alt sorular)
    # 3. En az bir subquestion'ı olan sorular (üst sorular)
    starting_question_ids = StartingQuestion.objects.values_list('question_id', flat=True)
    subquestion_ids = Question.objects.filter(parent_questions__isnull=False).values_list('id', flat=True)
    parent_question_ids = Question.objects.filter(subquestions__isnull=False).values_list('id', flat=True)
    question_ids = set(starting_question_ids) | set(subquestion_ids) | set(parent_question_ids)

    # Sadece bu question'ları çek
    queryset = Question.objects.filter(id__in=question_ids)

    # Filtre uygula
    if filter_param == 'me':
        queryset = queryset.filter(users=request.user)
    elif user_ids:
        queryset = queryset.filter(users__id__in=user_ids).distinct()

    # Düğümleri oluştur ve JSON olarak döndür
    data = generate_question_nodes(queryset)
    return JsonResponse(data, safe=False)


def generate_question_nodes(questions):
    nodes = []
    links = []

    # Prefetch answers and users to avoid N+1 queries
    questions = questions.prefetch_related(
        'users',
        'answers__user',
        'subquestions'
    )

    question_ids = set(q.id for q in questions)

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
            "size": 20 + 10 * (len(user_entries) - 1),
            "color": node_color,
            "question_id": question.id,
            "question_ids": [question.id],
        }
        nodes.append(node)

    for question in questions:
        for subquestion in question.subquestions.all():
            if subquestion.id in question_ids:
                links.append({
                    "source": f"q{question.id}",
                    "target": f"q{subquestion.id}",
                })

    return {
        "nodes": nodes,
        "links": links,
    }


def bkz_view(request, query):
    try:
        question = Question.objects.get(question_text__exact=query)
        return redirect('question_detail', question_id=question.id)
    except Question.DoesNotExist:
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
            Answer.objects.create(
                question=question,
                user=request.user,
                answer_text=form.cleaned_data['answer_text']
            )
            return redirect('user_homepage')
    else:
        form = StartingQuestionForm()
    return render(request, 'core/add_starting_question.html', {'form': form, 'all_questions': all_questions})


@login_required
def add_existing_subquestion(request, current_question_id):
    """Add current question as a subquestion to a selected parent question"""
    current_question = get_object_or_404(Question, id=current_question_id)

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

        # Zaten bağlı mı kontrolü
        if parent_question.subquestions.filter(id=current_question.id).exists():
            return JsonResponse({'success': False, 'error': 'Bu başlık zaten seçilen başlığın alt sorusu'}, status=400)

        # Döngüsel bağlantı kontrolü
        if would_create_cycle(parent_question, current_question):
            return JsonResponse({'success': False, 'error': 'Bu bağlantı döngüsel bir ilişki oluşturacak'}, status=400)

        # Bağlantıyı ekle: parent_question -> current_question
        parent_question.subquestions.add(current_question)

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

    # Kullanıcının yanıt verdiği VEYA başlangıç sorusu olarak eklediği soruları ara
    user_starting_questions = StartingQuestion.objects.filter(user=request.user).values_list('question_id', flat=True)

    questions = Question.objects.filter(
        Q(question_text__icontains=query),
        Q(users=request.user) | Q(id__in=user_starting_questions)
    ).exclude(
        id=current_question_id  # Kendisini hariç tut
    ).exclude(
        id__in=current_question.parent_questions.values_list('id', flat=True)  # Zaten parent olanları hariç tut
    ).distinct()[:10]

    results = [{
        'id': q.id,
        'text': q.question_text,
        'answer_count': q.answers.count()
    } for q in questions]

    return JsonResponse({'results': results})
