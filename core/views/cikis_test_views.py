"""
Exit test (Cikis Testi) views
- cikis_testleri_list
- cikis_testi_create
- cikis_testi_detail
- cikis_soru_ekle
- cikis_sik_ekle
- cikis_dogru_sik_sec
- cikis_testi_coz
- cikis_testi_sonuc_list
- cikis_dogrusu_ayarla
- cikis_soru_edit
- cikis_soru_sil
- cikis_test_list
- cikis_test_coz
- cikis_sonuc_sil
- cikis_testi_sil
- cikis_sik_edit
"""

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from ..models import CikisTesti, CikisTestiSoru, CikisTestiSik, CikisTestiResult
from ..forms import CikisTestiForm, CikisTestiSoruForm, CikisTestiSikForm


@login_required
def cikis_testleri_list(request):
    testler = CikisTesti.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'core/cikis_testleri_list.html', {'testler': testler})


@login_required
def cikis_testi_create(request):
    if request.method == 'POST':
        form = CikisTestiForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.owner = request.user
            test.save()
            return redirect('cikis_testi_detail', test_id=test.id)
    else:
        form = CikisTestiForm()
    return render(request, 'core/cikis_testi_create.html', {'form': form})


@login_required
def cikis_testi_detail(request, test_id):
    test = get_object_or_404(CikisTesti, id=test_id, owner=request.user)
    sorular = test.sorular.all().order_by('order', 'id')
    return render(request, 'core/cikis_testi_detail.html', {'test': test, 'sorular': sorular})


@login_required
def cikis_soru_ekle(request, test_id):
    test = get_object_or_404(CikisTesti, id=test_id, owner=request.user)
    if request.method == 'POST':
        form = CikisTestiSoruForm(request.POST)
        if form.is_valid():
            soru = form.save(commit=False)
            soru.test = test
            soru.save()
            return redirect('cikis_testi_detail', test_id=test.id)
    else:
        form = CikisTestiSoruForm()
    return render(request, 'core/cikis_soru_ekle.html', {'form': form, 'test': test})


@login_required
def cikis_sik_ekle(request, soru_id):
    soru = get_object_or_404(CikisTestiSoru, id=soru_id, test__owner=request.user)
    if request.method == 'POST':
        form = CikisTestiSikForm(request.POST)
        if form.is_valid():
            sik = form.save(commit=False)
            sik.soru = soru
            sik.save()
            return redirect('cikis_testi_detail', test_id=soru.test.id)
    else:
        form = CikisTestiSikForm()
    return render(request, 'core/cikis_sik_ekle.html', {'form': form, 'soru': soru})


@login_required
def cikis_dogru_sik_sec(request, soru_id):
    soru = get_object_or_404(CikisTestiSoru, id=soru_id, test__owner=request.user)
    if request.method == 'POST':
        sik_id = request.POST.get('correct_option')
        try:
            sik = soru.siklar.get(id=sik_id)
            soru.correct_option = sik
            soru.save()
        except CikisTestiSik.DoesNotExist:
            pass
        return redirect('cikis_testi_detail', test_id=soru.test.id)
    siklar = soru.siklar.all()
    return render(request, 'core/cikis_dogru_sik_sec.html', {'soru': soru, 'siklar': siklar})


@login_required
def cikis_testi_coz(request, test_id):
    test = get_object_or_404(CikisTesti, id=test_id)
    sorular = test.sorular.all()
    if request.method == "POST":
        cevaplar = {}
        dogru = 0
        for soru in sorular:
            secilen = request.POST.get(f"soru_{soru.id}")
            cevaplar[soru.id] = secilen
            if secilen and soru.correct_option and int(secilen) == soru.correct_option.id:
                dogru += 1
        # Sonucu kaydet
        result = CikisTestiResult.objects.create(
            test=test,
            user=request.user,
            dogru_sayisi=dogru,
            toplam_soru=sorular.count(),
            cikis_dogrusu_uydu=(test.cikis_dogrusu is not None and dogru >= test.cikis_dogrusu)
        )
        return render(request, "core/cikis_testi_sonuc.html", {
            "test": test,
            "dogru": dogru,
            "toplam": sorular.count(),
            "cikis_dogrusu": test.cikis_dogrusu,
            "uydu": (test.cikis_dogrusu is not None and dogru >= test.cikis_dogrusu),
            "sonuc": result,
        })
    return render(request, "core/cikis_testi_coz.html", {"test": test, "sorular": sorular})


@login_required
def cikis_testi_sonuc_list(request, test_id):
    test = get_object_or_404(CikisTesti, id=test_id)
    # Doğru sayısına göre azalan, eşitse en güncel önde
    sonuclar = test.sonuclar.select_related('user').all().order_by('-dogru_sayisi', '-completed_at')
    return render(request, "core/cikis_testi_sonuc_list.html", {
        "test": test,
        "sonuclar": sonuclar,
        "cikis_dogrusu": test.cikis_dogrusu
    })


@login_required
def cikis_dogrusu_ayarla(request, test_id):
    test = get_object_or_404(CikisTesti, id=test_id, owner=request.user)
    if request.method == "POST":
        try:
            yeni_dogruluk = int(request.POST.get("cikis_dogrusu"))
            if 0 <= yeni_dogruluk <= test.sorular.count():
                test.cikis_dogrusu = yeni_dogruluk
                test.save()
        except (ValueError, TypeError):
            pass
        return redirect("cikis_testi_detail", test_id=test.id)
    # Detaydan çağırıyorsan burası çalışmamalı!
    return redirect("cikis_testi_detail", test_id=test.id)


@login_required
def cikis_soru_edit(request, soru_id):
    soru = get_object_or_404(CikisTestiSoru, id=soru_id, test__owner=request.user)
    if request.method == "POST":
        form = CikisTestiSoruForm(request.POST, instance=soru)
        if form.is_valid():
            form.save()
            return redirect('cikis_testi_detail', test_id=soru.test.id)
    else:
        form = CikisTestiSoruForm(instance=soru)
    return render(request, 'core/cikis_soru_edit.html', {'form': form, 'soru': soru})


@login_required
def cikis_soru_sil(request, soru_id):
    soru = get_object_or_404(CikisTestiSoru, id=soru_id, test__owner=request.user)
    test_id = soru.test.id
    if request.method == "POST":
        soru.delete()
        return redirect('cikis_testi_detail', test_id=test_id)
    return render(request, 'core/cikis_soru_sil.html', {'soru': soru})


def cikis_test_list(request):
    tests = CikisTesti.objects.all().order_by('-created_at')
    return render(request, 'core/cikis_test_list.html', {'tests': tests})


@login_required
def cikis_test_coz(request, test_id):
    test = get_object_or_404(CikisTesti, id=test_id)
    sorular = test.sorular.all()
    # Kullanıcı daha önce çözdüyse sonucu göster, yoksa cevaplamasını sağla
    if request.method == "POST":
        # Yanıtları kaydet ve sonucu hesapla
        # ...
        return redirect('cikis_test_sonuc', test_id=test.id)
    return render(request, 'core/cikis_test_coz.html', {'test': test, 'sorular': sorular})


@login_required
def cikis_sonuc_sil(request, sonuc_id):
    sonuc = get_object_or_404(CikisTestiResult, id=sonuc_id)
    if sonuc.user != request.user:
        return HttpResponseForbidden("Bunu silemezsiniz.")
    if request.method == "POST":
        sonuc.delete()
        # AJAX için uygun döndür
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"status": "ok"})
        # Normal redirect (eski usül link tıklandıysa)
        return redirect("cikis_testi_sonuc_list", test_id=sonuc.test.id)
    return HttpResponseForbidden("Geçersiz istek")


@login_required
def cikis_testi_sil(request, test_id):
    test = get_object_or_404(CikisTesti, id=test_id, owner=request.user)
    if request.method == "POST":
        test.delete()
        return redirect('cikis_testleri_list')  # Kullanıcının test listesine yönlendir
    return render(request, 'core/cikis_testi_sil.html', {'test': test})


@login_required
def cikis_sik_edit(request, sik_id):
    sik = get_object_or_404(CikisTestiSik, id=sik_id, soru__test__owner=request.user)
    if request.method == "POST":
        form = CikisTestiSikForm(request.POST, instance=sik)
        if form.is_valid():
            form.save()
            return redirect('cikis_testi_detail', test_id=sik.soru.test.id)
    else:
        form = CikisTestiSikForm(instance=sik)
    return render(request, 'core/cikis_sik_edit.html', {'form': form, 'sik': sik})
