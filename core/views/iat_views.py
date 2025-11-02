"""
IAT (Implicit Association Test) views
- game_of_life
- iat_start
- iat_test
- iat_result_page
- iat_result
"""

import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from ..models import IATResult


def game_of_life(request):
    return render(request, "core/game_of_life.html")


def iat_start(request):
    return render(request, 'core/iat_start.html')


@login_required
def iat_test(request):
    # test_type: "gender" veya "ethnicity"
    test_type = request.GET.get('test_type')
    if test_type not in ["gender", "ethnicity"]:
        return redirect('iat_start')
    # Bu sayfada gerçek testi başlatacağız
    return render(request, 'core/iat_test.html', {'test_type': test_type})


@login_required
def iat_result_page(request):
    data = request.session.get('iat_result')
    if not data:
        return redirect("iat_start")

    if data['test_type'] == 'gender':
        reading = [
            {"title": "IAT nedir? (Bilinçdışı cinsiyet çağrışımı)", "url": "https://implicit.harvard.edu/implicit/takeatest.html"},
            {"title": "Toplumsal cinsiyet rolleri ve önyargı (makale)", "url": "https://psycnet.apa.org/record/2002-11021-009"},
            {"title": "Kadın-Erkek IAT analizleri", "url": "https://www.apa.org/research/action/sex-differences"},
        ]
    else:
        reading = [
            {"title": "Etnik önyargı ve çağrışımlar (IAT)", "url": "https://implicit.harvard.edu/implicit/takeatest.html"},
            {"title": "Türkiye'de Etnisite ve Önyargı", "url": "https://dergipark.org.tr/tr/download/article-file/224166"},
            {"title": "Kürt ve Türk kimliklerinde sosyal psikoloji", "url": "https://www.sciencedirect.com/science/article/pii/S0191886911003717"},
        ]

    ranking = data.get("ranking", [])
    return render(request, "core/iat_result.html", {
        "result": data,
        "reading": reading,
        "ranking": ranking,
    })


@login_required
@csrf_exempt
def iat_result(request):
    if request.method == "POST":
        data = json.loads(request.body)
        responses = data.get('responses', [])
        test_type = data.get('test_type', 'gender')

        # Aşamaları ayır: (0,2) = bir kategoriye karşı diğeri; (1,3) = kombinasyon eşleşmeleri
        stage_times = {i: [] for i in range(4)}
        stage_errors = {i: 0 for i in range(4)}
        for resp in responses:
            stage = resp['stage']
            rt = resp['rt']
            correct = resp['correct']
            if not correct:
                rt += 600   # Yanlış cevaplara 600 ms ekle
                stage_errors[stage] += 1
            stage_times[stage].append(rt)

        # D-score (Greenwald, 2003)
        # Anahtar bloklar: 2 ve 3 (kombinasyonlar)
        def safe_mean(x):
            return sum(x) / len(x) if x else 0
        def pooled_std(a, b):
            from math import sqrt
            aa = a if a else [1]
            bb = b if b else [1]
            mean_a = safe_mean(aa)
            mean_b = safe_mean(bb)
            var_a = sum((v - mean_a) ** 2 for v in aa) / (len(aa) - 1 if len(aa) > 1 else 1)
            var_b = sum((v - mean_b) ** 2 for v in bb) / (len(bb) - 1 if len(bb) > 1 else 1)
            return ((var_a + var_b) / 2) ** 0.5

        rt2 = [rt for rt in stage_times[2] if 200 < rt < 3000]
        rt3 = [rt for rt in stage_times[3] if 200 < rt < 3000]
        mean2 = safe_mean(rt2)
        mean3 = safe_mean(rt3)
        std_pooled = pooled_std(rt2, rt3) or 1
        dscore = (mean3 - mean2) / std_pooled

        # Yorum ve etiket
        if abs(dscore) < 0.15:
            bias_label = "Belirgin bir önyargı/çağrışım tespit edilmedi."
            bias_side = "neutral"
        elif dscore > 0.15:
            if test_type == "gender":
                bias_label = "Kadınları iyiyle, erkekleri kötüyle daha hızlı eşlediniz (Kadın lehine ön yargılarınız olabilir)."
            else:
                bias_label = "Türkleri iyiyle, Kürtleri kötüyle daha hızlı eşlediniz (Türk lehine önyargılarınız olabilir)."
            bias_side = "left"
        else:
            if test_type == "gender":
                bias_label = "Erkekleri iyiyle, kadınları kötüyle daha hızlı eşlediniz (Erkek lehine ön yargılarınız olabilir.)."
            else:
                bias_label = "Kürtleri iyiyle, Türkleri kötüyle daha hızlı eşlediniz (Kürt lehine önyargılarınız olabilir.)."
            bias_side = "right"

        # Sonucu kaydet
        result_obj = IATResult.objects.create(
            user=request.user,
            test_type=test_type,
            dscore=round(dscore, 3),
            bias_side=bias_side,
            errors=sum(stage_errors.values()),
            avg_rt=round((mean2 + mean3) / 2 if (mean2 + mean3) > 0 else 0)
        )

        # Sıralama listesi (aynı test tipine göre, yüksekten düşüğe)
        all_results = IATResult.objects.filter(test_type=test_type).order_by('-dscore')
        ranking = []
        user_rank = None
        for idx, res in enumerate(all_results, 1):
            is_me = (res.user == request.user)
            if is_me:
                user_rank = idx
            ranking.append({
                "rank": idx,
                "username": res.user.username if is_me else f"Kullanıcı #{idx}",
                "dscore": res.dscore,
                "is_me": is_me,
            })

        # Session ile sonucu ve sıralamayı gönder
        request.session['iat_result'] = {
            "test_type": test_type,
            "dscore": round(dscore, 3),
            "label": bias_label,
            "errors": sum(stage_errors.values()),
            "avg_rt": round((mean2 + mean3) / 2 if (mean2 + mean3) > 0 else 0),
            "bias_side": bias_side,
            "user_rank": user_rank,
            "ranking": ranking,
        }
        return JsonResponse({"result_url": reverse("iat_result_page")})

    return HttpResponse(status=405)
