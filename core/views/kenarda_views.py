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
        data = json.loads(request.body)
        question_id = data.get("question_id")
        content = data.get("content")
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
        # Otomatik yanıt oluştur
        Answer.objects.create(
            question=taslak.question,
            answer_text=taslak.content,
            user=request.user
        )
        taslak.delete()
        return JsonResponse({"status":"ok"})
    except Exception as e:
        return JsonResponse({"status":"fail", "error": str(e)})
