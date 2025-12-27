"""
Kenarda (draft) views
- kenarda_save
- kenarda_preview
- kenarda_list
- kenarda_sil
- kenarda_gonder
"""

import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
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
        content = (data.get("content") or "")
        title = (data.get("title") or "").strip()  # Yeni başlıklar için başlık metni
        draft_source = data.get("draft_source")  # Taslağın kaynağı

        # Maksimum uzunluk kontrolü (50,000 karakter)
        if len(content) > 50000:
            return JsonResponse({"status": "fail", "error": "İçerik çok uzun (max 50000 karakter)"}, status=400)

        # En az bir bağlam bilgisi olmalı; aksi halde taslak "başlangıç sorusu" gibi yanlış yerde açılabilir.
        if not answer_id and not question_id and not title:
            return JsonResponse(
                {"status": "fail", "error": "Taslak bağlamı eksik (answer_id/question_id/title gerekli)"},
                status=400,
            )

        # Kaynak bazlı basit doğrulamalar
        if draft_source in {"starting_question", "question_from_search"} and not title:
            return JsonResponse({"status": "fail", "error": "Başlık boş olamaz"}, status=400)

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

        # Bazı edge-case'lerde client answer_id göndermeyebilir; ancak kullanıcı bu soruda tek bir yanıt
        # yazdıysa, bunu "yanıt düzenleme" taslağı olarak yorumlayabiliriz (özellikle "ilk entry" durumu).
        if not answer and question and draft_source == "answer_edit":
            qs = Answer.objects.filter(question=question, user=request.user).order_by("created_at")
            if qs.count() == 1:
                answer = qs.first()
                question = answer.question

        # Eğer answer_id ile gelindiyse bu taslak kesinlikle "yanıt düzenleme" taslağıdır.
        # (Client yanlışlıkla draft_source göndermese bile sınıflandırma bozulmasın.)
        if answer:
            draft_source = "answer_edit"

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
            if draft_source:  # Kaynağı güncelle
                existing.draft_source = draft_source
            existing.updated_at = timezone.now()
            existing.save()
        else:
            Kenarda.objects.create(
                user=request.user,
                question=question,
                answer=answer,
                title=title if (not question and not answer) else None,  # Sadece yeni başlık için title
                content=content,
                draft_source=draft_source,
                is_sent=False
            )
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "fail", "error": "Yetkisiz veya geçersiz istek"})


@require_POST
@login_required
def kenarda_preview(request):
    """
    Render a private, server-side preview of a draft as if it were posted.
    This is meant to be used right after kenarda_save succeeds.
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "fail", "error": "Geçersiz JSON formatı"}, status=400)

    question_id = data.get("question_id")
    answer_id = data.get("answer_id")
    content = (data.get("content") or "")
    title = (data.get("title") or "").strip()

    if len(content) > 50000:
        return JsonResponse({"status": "fail", "error": "İçerik çok uzun (max 50000 karakter)"}, status=400)

    if not answer_id and not question_id and not title:
        return JsonResponse(
            {"status": "fail", "error": "Taslak bağlamı eksik (answer_id/question_id/title gerekli)"},
            status=400,
        )

    question = None
    if question_id:
        question = Question.objects.filter(id=question_id).first()

    if answer_id:
        answer = Answer.objects.filter(id=answer_id, user=request.user).select_related("question").first()
        if not answer:
            return JsonResponse({"status": "fail", "error": "Yanıt bulunamadı veya size ait değil"}, status=403)
        question = answer.question

    question_text = title or (question.question_text if question else "")
    preview_key = f"draft-{request.user.id}-{int(timezone.now().timestamp())}"

    html = render_to_string(
        "core/_answer_preview_card.html",
        {
            "preview_text": content,
            "preview_user": request.user,
            "preview_created_at": timezone.now(),
            "preview_question_text": question_text,
            "preview_question_slug": getattr(question, "slug", None),
            "preview_key": preview_key,
        },
        request=request,
    )

    return JsonResponse({"status": "ok", "html": html})


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
