"""Question linking, unlinking, and admin merge views."""

from collections import defaultdict
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Count, Max, Q
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from ..models import (
    Answer,
    Definition,
    HashtagUsage,
    Kenarda,
    Notification,
    Question,
    QuestionFollow,
    QuestionRelationship,
    SavedItem,
    StartingQuestion,
    Vote,
)

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

        # Kullanıcı bu başlıkta entry yazmadıysa bağlayamasın
        if not Answer.objects.filter(question=current_question, user=request.user).exists():
            return JsonResponse(
                {'success': False, 'error': 'Bu başlığı üst başlığa bağlamak için önce bu başlığa entry girmeniz gerekir.'},
                status=400
            )

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
        affected_starting_questions = StartingQuestion.objects.filter(
            question=current_question,
            user=request.user
        )
        if affected_starting_questions.exists():
            # Önce eski başlangıç sorusunu sil (yalnızca bu kullanıcı için)
            affected_starting_questions.delete()
            # Parent bu kullanıcı için root ise başlangıç olarak işaretle
            parent_has_parent = QuestionRelationship.objects.filter(
                child=parent_question,
                user=request.user
            ).exists()
            if not parent_has_parent:
                StartingQuestion.objects.get_or_create(
                    user=request.user,
                    question=parent_question
                )

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
    Not: Unlink sonrası soru orphan kalsa bile otomatik olarak StartingQuestion yapılmaz;
    kullanıcı isterse ayrıca başlangıç sorusu olarak ekler.
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

    # Orphan kontrolü: Eğer kullanıcının bu sorunun hiç parent'ı kalmadıysa da
    # StartingQuestion kaydı oluşturmayız (normal başlık olarak kalır).

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
        moved_entry_count_by_user = defaultdict(int)
        for i, ans in enumerate(source_answers, start=1):
            shifted = base_time + timedelta(seconds=i)
            moved_entry_count_by_user[ans.user_id] += 1
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

        # 6.1) Notify users whose entries were moved
        notifications_to_create = []
        for recipient_id, moved_count in moved_entry_count_by_user.items():
            if moved_count == 1:
                message = (
                    f'"{source_title}" başlığındaki girdiniz '
                    f'"{target_title}" başlığına taşınmıştır.'
                )
            else:
                message = (
                    f'"{source_title}" başlığındaki {moved_count} girdiniz '
                    f'"{target_title}" başlığına taşınmıştır.'
                )
            notifications_to_create.append(
                Notification(
                    recipient_id=recipient_id,
                    sender=request.user,
                    notification_type='system',
                    message=message,
                    related_question=target,
                )
            )
        if notifications_to_create:
            Notification.objects.bulk_create(notifications_to_create)

        # 7) Finally delete the source question
        source.delete()

    messages.success(
        request,
        f'"{source_title}" başlığındaki entryler "{target_title}" başlığına taşındı ve eski başlık silindi.'
    )
    return redirect('question_detail', slug=target.slug)

