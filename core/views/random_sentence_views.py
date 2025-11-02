"""
Random sentence views
- ignore_random_sentence
- get_random_sentence
- add_random_sentence
"""

import random

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from ..models import RandomSentence
from ..forms import RandomSentenceForm


@login_required
@require_POST
def ignore_random_sentence(request):
    """
    POST ile gelen sentence_id parametresi üzerinden
    cümleyi ignore listesine ekler.
    """
    sentence_id = request.POST.get('sentence_id')
    if not sentence_id:
        return JsonResponse({'status': 'error', 'message': 'sentence_id parametresi bulunamadı.'}, status=400)

    try:
        sentence_obj = RandomSentence.objects.get(id=sentence_id)
    except RandomSentence.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Cümle bulunamadı.'}, status=404)

    # Kullanıcıyı ignore listesine ekle
    sentence_obj.ignored_by.add(request.user)
    return JsonResponse({'status': 'success', 'message': 'Cümle ignore listesine eklendi.'})


def get_random_sentence(request):
    if request.user.is_authenticated:
        # ignore ettiği cümleler hariç
        sentences = RandomSentence.objects.exclude(ignored_by=request.user)
    else:
        # anonimse hepsi arasından rastgele çek
        sentences = RandomSentence.objects.all()

    sentences_count = sentences.count()
    if sentences_count == 0:
        return JsonResponse({'sentence': 'Henüz eklenmiş (veya gösterilmeye uygun) cümle yok.'})

    random_index = random.randint(0, sentences_count - 1)
    sentence_obj = sentences[random_index]

    return JsonResponse({
        'id': sentence_obj.id,
        'sentence': sentence_obj.sentence
    })


@login_required
@require_POST
def add_random_sentence(request):
    form = RandomSentenceForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success', 'message': 'Cümle eklendi!'})
    else:
        # Form geçersiz ise hata mesajını döndür
        errors = form.errors.get_json_data()
        return JsonResponse({'status': 'error', 'errors': errors})
