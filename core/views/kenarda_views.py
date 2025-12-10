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
        answer_id = data.get("answer_id")  # Var olan yanıt düzenleme taslağı için
        content = data.get("content", "")
        title = data.get("title", "")  # Yeni başlıklar için başlık metni

        # Maksimum uzunluk kontrolü (50,000 karakter)
        if len(content) > 50000:
            return JsonResponse({"status": "fail", "error": "İçerik çok uzun (max 50000 karakter)"}, status=400)

        question = None
        answer = None

        if question_id:
            try:
                question = Question.objects.get(id=question_id)
            except Question.DoesNotExist:
                question = None

        if answer_id:
            try:
                answer = Answer.objects.get(id=answer_id, user=request.user)
                question = answer.question  # Answer'dan question'ı al
            except Answer.DoesNotExist:
                return JsonResponse({"status": "fail", "error": "Yanıt bulunamadı veya size ait değil"}, status=403)

        # Mevcut taslak var mı?
        if answer:
            # Var olan yanıtın düzenleme taslağı
            existing = Kenarda.objects.filter(user=request.user, answer=answer, is_sent=False).first()
        elif question:
            # Soruya yeni yanıt taslağı
            existing = Kenarda.objects.filter(user=request.user, question=question, answer__isnull=True, is_sent=False).first()
        elif title:
            # Yeni başlık taslağı
            existing = Kenarda.objects.filter(user=request.user, title=title, question__isnull=True, answer__isnull=True, is_sent=False).first()
        else:
            existing = None

        if existing:
            existing.content = content
            if title and not existing.question and not existing.answer:  # Sadece yeni başlık taslağında title güncelle
                existing.title = title
            existing.updated_at = timezone.now()
            existing.save()
        else:
            Kenarda.objects.create(
                user=request.user,
                question=question,
                answer=answer,
                title=title if (not question and not answer) else None,  # Sadece yeni başlık için title
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

        # Var olan yanıtın düzenleme taslağı mı, yoksa yeni yanıt mı?
        if taslak.answer:
            # Var olan yanıtı güncelle
            answer = taslak.answer
            answer.answer_text = taslak.content
            answer.save()
        else:
            # Yeni yanıt oluştur
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
