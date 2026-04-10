"""Question map and schema views."""

from collections import defaultdict, deque

from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from ..models import Answer, Question, QuestionRelationship, StartingQuestion
from .user_views import get_user_color

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
    if filter_param == 'me' and request.user.is_authenticated:
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


def _build_answer_preview(raw_text, limit=320):
    normalized = " ".join((raw_text or "").split())
    if not normalized:
        return "(Bos icerik)", False
    if len(normalized) <= limit:
        return normalized, False
    return normalized[:limit].rstrip() + "...", True


def _render_schema_answer_html(raw_text):
    # Keep schema entry rendering aligned with normal answer rendering pipeline.
    from ..templatetags.custom_tags import (
        safe_markdownify,
        spoiler_link,
        bkz_link,
        tanim_link,
        reference_link,
        ref_link,
        mention_link,
        collapsible_images,
    )

    text = raw_text or ""
    rendered = safe_markdownify(text, "default")
    rendered = spoiler_link(rendered)
    rendered = bkz_link(rendered)
    rendered = tanim_link(rendered)
    rendered = reference_link(rendered)
    rendered = ref_link(rendered)
    rendered = mention_link(rendered)
    rendered = collapsible_images(rendered)
    return str(rendered)


def _to_roman(number):
    if number <= 0:
        return str(number)
    values = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
    ]
    result = []
    remaining = number
    for value, symbol in values:
        while remaining >= value:
            result.append(symbol)
            remaining -= value
    return "".join(result)


def _get_schema_users():
    User = get_user_model()
    relationship_user_ids = set(
        QuestionRelationship.objects.values_list('user_id', flat=True).distinct()
    )
    starting_user_ids = set(
        StartingQuestion.objects.values_list('user_id', flat=True).distinct()
    )
    schema_user_ids = sorted(relationship_user_ids | starting_user_ids)
    if not schema_user_ids:
        return []
    return list(
        User.objects.filter(id__in=schema_user_ids)
        .order_by('username')
        .values('id', 'username')
    )


def _resolve_schema_user_id(request, schema_users):
    if not schema_users:
        return None

    allowed_ids = {row['id'] for row in schema_users}
    requested_user_id = request.GET.get('user_id')
    if requested_user_id:
        try:
            requested_user_id = int(requested_user_id)
        except (TypeError, ValueError):
            requested_user_id = None
        if requested_user_id in allowed_ids:
            return requested_user_id

    if request.user.is_authenticated and request.user.id in allowed_ids:
        return request.user.id

    return schema_users[0]['id']


def _get_user_schema_root_ids(user_id):
    if not user_id:
        return []

    starting_ids = list(
        StartingQuestion.objects.filter(user_id=user_id)
        .order_by('question__question_text')
        .values_list('question_id', flat=True)
    )

    relationships = QuestionRelationship.objects.filter(user_id=user_id).values_list('parent_id', 'child_id')
    parent_ids = set()
    child_ids = set()
    for parent_id, child_id in relationships:
        parent_ids.add(parent_id)
        child_ids.add(child_id)

    inferred_root_ids = sorted(parent_ids - child_ids)

    seen = set()
    root_ids = []
    for question_id in starting_ids + inferred_root_ids:
        if question_id in seen:
            continue
        seen.add(question_id)
        root_ids.append(question_id)
    return root_ids


def _build_user_schema_graph(user_id):
    root_ids = _get_user_schema_root_ids(user_id)
    relationships = list(
        QuestionRelationship.objects
        .filter(user_id=user_id)
        .values_list('parent_id', 'child_id')
    )

    children_by_parent = defaultdict(list)
    all_ids = set(root_ids)
    parent_ids = set()
    child_ids = set()

    for parent_id, child_id in relationships:
        children_by_parent[parent_id].append(child_id)
        all_ids.add(parent_id)
        all_ids.add(child_id)
        parent_ids.add(parent_id)
        child_ids.add(child_id)

    for parent_id, child_list in children_by_parent.items():
        children_by_parent[parent_id] = sorted(set(child_list))

    if not root_ids and all_ids:
        inferred_roots = sorted(parent_ids - child_ids)
        root_ids = inferred_roots if inferred_roots else sorted(all_ids)

    depth_by_id = {}
    parent_by_id = {}
    queue = deque()

    for root_id in root_ids:
        if root_id in depth_by_id:
            continue
        depth_by_id[root_id] = 0
        parent_by_id[root_id] = None
        queue.append(root_id)

        while queue:
            current_id = queue.popleft()
            for child_id in children_by_parent.get(current_id, []):
                if child_id in depth_by_id:
                    continue
                depth_by_id[child_id] = depth_by_id[current_id] + 1
                parent_by_id[child_id] = current_id
                queue.append(child_id)

    # If there are disconnected/cyclic nodes, keep them searchable as standalone.
    for question_id in sorted(all_ids):
        if question_id not in depth_by_id:
            depth_by_id[question_id] = 0
            parent_by_id[question_id] = None

    return {
        'root_ids': root_ids,
        'all_ids': sorted(all_ids),
        'children_by_parent': dict(children_by_parent),
        'depth_by_id': depth_by_id,
        'parent_by_id': parent_by_id,
    }


def _build_schema_path_ids(node_id, parent_by_id, max_hops=300):
    path = []
    current = node_id
    seen = set()

    while current is not None and current not in seen and len(path) < max_hops:
        path.append(current)
        seen.add(current)
        current = parent_by_id.get(current)

    path.reverse()
    return path


def question_schema(request):
    schema_users = _get_schema_users()
    selected_user_id = _resolve_schema_user_id(request, schema_users)
    root_ids = _get_user_schema_root_ids(selected_user_id)

    if not root_ids:
        return render(request, 'core/question_schema.html', {
            'root_nodes': [],
            'schema_users': schema_users,
            'selected_schema_user_id': selected_user_id,
        })

    child_count_rows = (
        QuestionRelationship.objects
        .filter(user_id=selected_user_id, parent_id__in=root_ids)
        .values('parent_id')
        .annotate(child_count=Count('child_id', distinct=True))
    )
    child_count_by_parent = {row['parent_id']: row['child_count'] for row in child_count_rows}

    answer_count_rows = (
        Answer.objects
        .filter(question_id__in=root_ids, user_id=selected_user_id)
        .values('question_id')
        .annotate(answer_count=Count('id'))
    )
    answer_count_by_question = {row['question_id']: row['answer_count'] for row in answer_count_rows}

    root_questions = Question.objects.filter(id__in=root_ids)
    question_by_id = {q.id: q for q in root_questions}

    root_nodes = []
    for question_id in root_ids:
        question = question_by_id.get(question_id)
        if not question:
            continue
        root_nodes.append({
            'id': question.id,
            'text': question.question_text,
            'slug': question.slug,
            'detail_url': reverse('question_detail', args=[question.slug]),
            'child_count': child_count_by_parent.get(question.id, 0),
            'answer_count': answer_count_by_question.get(question.id, 0),
        })

    return render(request, 'core/question_schema.html', {
        'root_nodes': root_nodes,
        'schema_users': schema_users,
        'selected_schema_user_id': selected_user_id,
    })


def question_schema_children(request, question_id):
    schema_users = _get_schema_users()
    selected_user_id = _resolve_schema_user_id(request, schema_users)
    if not selected_user_id:
        return JsonResponse({'children': []})

    relationships = (
        QuestionRelationship.objects
        .filter(user_id=selected_user_id, parent_id=question_id)
        .select_related('child')
        .order_by('child__question_text')
    )

    child_ids = [rel.child_id for rel in relationships]
    if not child_ids:
        return JsonResponse({'children': []})

    child_count_rows = (
        QuestionRelationship.objects
        .filter(user_id=selected_user_id, parent_id__in=child_ids)
        .values('parent_id')
        .annotate(child_count=Count('child_id', distinct=True))
    )
    child_count_by_parent = {row['parent_id']: row['child_count'] for row in child_count_rows}

    answer_count_rows = (
        Answer.objects
        .filter(question_id__in=child_ids, user_id=selected_user_id)
        .values('question_id')
        .annotate(answer_count=Count('id'))
    )
    answer_count_by_question = {row['question_id']: row['answer_count'] for row in answer_count_rows}

    children = []
    for rel in relationships:
        child = rel.child
        children.append({
            'id': child.id,
            'text': child.question_text,
            'slug': child.slug,
            'detail_url': reverse('question_detail', args=[child.slug]),
            'child_count': child_count_by_parent.get(child.id, 0),
            'answer_count': answer_count_by_question.get(child.id, 0),
        })

    return JsonResponse({'children': children})


def question_schema_content(request, question_id):
    schema_users = _get_schema_users()
    selected_user_id = _resolve_schema_user_id(request, schema_users)
    if not selected_user_id:
        return JsonResponse({'question': {}, 'total_answers': 0, 'shown_answers': 0, 'has_more': False, 'answers': []})

    question = get_object_or_404(Question, id=question_id)
    limit = request.GET.get('limit', '12')
    try:
        limit = int(limit)
    except (TypeError, ValueError):
        limit = 12
    limit = max(1, min(limit, 25))

    answers_qs = (
        Answer.objects
        .filter(question_id=question.id, user_id=selected_user_id)
        .select_related('user')
        .order_by('created_at')
    )
    total_answers = answers_qs.count()

    answers = []
    for index, answer in enumerate(answers_qs[:limit], start=1):
        preview, is_truncated = _build_answer_preview(answer.answer_text, limit=340)
        answers.append({
            'id': answer.id,
            'user': answer.user.username,
            'created_at': timezone.localtime(answer.created_at).strftime('%Y-%m-%d %H:%M'),
            'roman': _to_roman(index),
            'rendered_html': _render_schema_answer_html(answer.answer_text),
            'preview': preview,
            'is_truncated': is_truncated,
            'answer_url': reverse('single_answer', args=[question.slug, answer.id]),
        })

    return JsonResponse({
        'question': {
            'id': question.id,
            'text': question.question_text,
            'slug': question.slug,
            'detail_url': reverse('question_detail', args=[question.slug]),
        },
        'total_answers': total_answers,
        'shown_answers': len(answers),
        'has_more': total_answers > len(answers),
        'answers': answers,
    })


def question_schema_search(request):
    schema_users = _get_schema_users()
    selected_user_id = _resolve_schema_user_id(request, schema_users)
    if not selected_user_id:
        return JsonResponse({'results': []})

    query = (request.GET.get('q') or '').strip()
    if not query:
        return JsonResponse({'results': []})

    limit_raw = request.GET.get('limit', '10')
    try:
        limit = int(limit_raw)
    except (TypeError, ValueError):
        limit = 10
    limit = max(1, min(limit, 30))

    graph = _build_user_schema_graph(selected_user_id)
    node_ids = graph['all_ids']
    if not node_ids:
        return JsonResponse({'results': []})

    question_rows = list(
        Question.objects
        .filter(id__in=node_ids)
        .values('id', 'question_text', 'slug')
    )
    question_by_id = {row['id']: row for row in question_rows}
    root_set = set(graph['root_ids'])
    normalized_query = query.casefold()

    matches = []
    for row in question_rows:
        text = (row.get('question_text') or '').strip()
        if not text:
            continue
        if normalized_query not in text.casefold():
            continue

        node_id = row['id']
        depth = graph['depth_by_id'].get(node_id, 0)
        path_ids = _build_schema_path_ids(node_id, graph['parent_by_id'])
        path_titles = [
            question_by_id[path_id]['question_text']
            for path_id in path_ids
            if path_id in question_by_id and question_by_id[path_id].get('question_text')
        ]

        if len(path_titles) > 4:
            path_label = '... > ' + ' > '.join(path_titles[-4:])
        else:
            path_label = ' > '.join(path_titles)

        matches.append({
            'id': node_id,
            'text': text,
            'slug': row['slug'],
            'detail_url': reverse('question_detail', args=[row['slug']]),
            'kind': 'root' if node_id in root_set else 'child',
            'depth': depth,
            'path_ids': path_ids,
            'path_label': path_label,
        })

    matches.sort(key=lambda item: (
        0 if item['text'].casefold().startswith(normalized_query) else 1,
        item['depth'],
        item['text'].casefold(),
    ))

    return JsonResponse({'results': matches[:limit]})


def generate_question_nodes(questions, user_filter=None):
    """
    Generate nodes and links for the question map.

    Args:
        questions: QuerySet of questions to include in the map
        user_filter: List of user IDs to filter relationships by (None = show all users' relationships)
    """
    nodes = []
    links = []

    # Prefetch answers to avoid N+1 queries
    questions = questions.prefetch_related(
        'answers__user'
    )

    question_ids = set(q.id for q in questions)

    # Map: question_id -> set(user_id) who linked this question as child or made it a starting question
    link_user_ids_by_question = defaultdict(set)

    # Starting questions -> treat the starter as a linker for that node
    starting_qs = StartingQuestion.objects.filter(question_id__in=question_ids)
    if user_filter:
        starting_qs = starting_qs.filter(user_id__in=user_filter)
    for sq in starting_qs:
        link_user_ids_by_question[sq.question_id].add(sq.user_id)

    # Query QuestionRelationship with user filter
    relationship_query = QuestionRelationship.objects.filter(
        parent_id__in=question_ids,
        child_id__in=question_ids
    ).select_related('parent', 'child', 'user')

    # Apply user filter if specified
    if user_filter:
        relationship_query = relationship_query.filter(user_id__in=user_filter)

    # Linkers are tracked on the child node
    for rel in relationship_query:
        link_user_ids_by_question[rel.child_id].add(rel.user_id)

    # Build nodes first
    for question in questions:
        user_entries = []
        link_user_entries = []

        # Build a lookup dict for answers by user_id
        answers_by_user = {}
        for answer in question.answers.all():
            user_id = answer.user.id
            if user_id not in answers_by_user:
                answers_by_user[user_id] = answer
            elif answer.created_at < answers_by_user[user_id].created_at:
                # Keep the earliest answer
                answers_by_user[user_id] = answer

        link_user_ids = link_user_ids_by_question.get(question.id, set())
        for user_id, answer in answers_by_user.items():
            entry = {
                "id": user_id,
                "username": answer.user.username,
                "answer_id": answer.id,
            }
            user_entries.append(entry)
            if user_id in link_user_ids:
                link_user_entries.append(entry)

        user_ids = [entry["id"] for entry in user_entries]
        linker_ids = list(link_user_ids)

        # Color logic: reflect who linked the node into a chain, not who answered
        if len(linker_ids) == 1:
            node_color = get_user_color(linker_ids[0])
        elif len(linker_ids) > 1:
            node_color = '#CCCCCC'  # Grey for intersections (multiple linkers)
        else:
            node_color = '#87ceeb'  # Sky blue fallback

        node = {
            "id": f"q{question.id}",
            "label": question.question_text,
            "users": user_entries,
            "link_users": link_user_entries,
            "user_ids": user_ids,  # Add user_ids for statistics calculation
            "link_user_ids": linker_ids,
            "size": 20 + max(0, len(linker_ids) - 1),  # Grow only with chain count (unique linkers)
            "color": node_color,
            "question_id": question.id,
            "question_ids": [question.id],
            "slug": question.slug,  # Add slug for navigation
        }
        nodes.append(node)

    # Build links from relationships
    for rel in relationship_query:
        parent_id = f"q{rel.parent_id}"
        child_id = f"q{rel.child_id}"

        links.append({
            "source": parent_id,
            "target": child_id,
            "user_id": rel.user_id,  # Track which user created this link
        })

    return {
        "nodes": nodes,
        "links": links,
    }

