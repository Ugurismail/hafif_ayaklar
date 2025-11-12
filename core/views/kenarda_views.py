"""
Kenarda (draft) views
- kenarda_save
- kenarda_list
- kenarda_sil
- kenarda_gonder
"""

import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_POST

from ..models import Kenarda, Question, Answer


@login_required
def kenarda_save(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"status": "fail", "error": "Geçersiz JSON formatı"}, status=400)

        question_id = data.get("question_id")
        content = data.get("content", "")

        # Maksimum uzunluk kontrolü (50,000 karakter)
        if len(content) > 50000:
            return JsonResponse({"status": "fail", "error": "İçerik çok uzun (max 50000 karakter)"}, status=400)

        # JSON.stringify doğal olarak newline'ları korur, ekstra işlem gerekmez
        # Eğer garip karakterler varsa JSON'dan geliyor olabilir ama
        # normalde json.loads zaten decode eder

        question = None
        if question_id:
            try:
                question = Question.objects.get(id=question_id)
            except Question.DoesNotExist:
                question = None
        # Mevcut taslak var mı?
        existing = Kenarda.objects.filter(user=request.user, question=question, is_sent=False).first()
        if existing:
            existing.content = content
            existing.updated_at = timezone.now()
            existing.save()
        else:
            Kenarda.objects.create(
                user=request.user,
                question=question,
                content=content,
                is_sent=False
            )
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "fail", "error": "Yetkisiz veya geçersiz istek"})


@login_required
def kenarda_list(request):
    taslaklar = Kenarda.objects.filter(user=request.user, is_sent=False).order_by('-updated_at')
    return render(request, 'core/kenarda_list.html', {'taslaklar': taslaklar})


@require_POST
@login_required
def kenarda_sil(request, pk):
    try:
        taslak = Kenarda.objects.get(pk=pk, user=request.user)
        taslak.delete()
        return JsonResponse({"status":"ok"})
    except Kenarda.DoesNotExist:
        return JsonResponse({"status":"fail"})


@require_POST
@login_required
def kenarda_gonder(request, pk):
    try:
        taslak = Kenarda.objects.get(pk=pk, user=request.user)

        # Taslak bir soruya bağlı mı kontrol et
        if taslak.question is None:
            return JsonResponse({"status":"fail", "error": "Taslak bir soruya bağlı değil"}, status=400)

        # Otomatik yanıt oluştur
        answer = Answer.objects.create(
            question=taslak.question,
            answer_text=taslak.content,
            user=request.user
        )

        # Mention bildirimleri gönder
        from ..utils import extract_mentions, send_mention_notifications
        mentioned_usernames = extract_mentions(answer.answer_text)
        if mentioned_usernames:
            send_mention_notifications(answer, mentioned_usernames)

        question_slug = taslak.question.slug
        answer_id = answer.id
        taslak.delete()

        return JsonResponse({
            "status": "ok",
            "question_slug": question_slug,
            "answer_id": answer_id
        })
    except Kenarda.DoesNotExist:
        return JsonResponse({"status":"fail", "error": "Taslak bulunamadı"}, status=404)
    except Exception as e:
        # Log the error for debugging
        import logging
        logging.error(f"kenarda_gonder error: {e}")
        return JsonResponse({"status":"fail", "error": "Bir hata oluştu"}, status=500)
