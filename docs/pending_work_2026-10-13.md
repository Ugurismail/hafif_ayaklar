# Bekleyen Isler: 2026-10-13

## Kapsam ve Son Yayin

- Uzak main, fetch ve ls-remote ile dogrulandi: `719eac7`.
- Bu commit iptal edilen davetleri listeden/sayaclardan gizler ve verilen
  toplama ayni gonderenin aliciya yaptigi ek aktarimlari dahil eder.
- Yayin oncesi 804 Django testi: 792 basarili, 12 SQLite kilitleme atlamasi.
  Model/migration ve diff kontrolleri temiz. Yeni migration/paket yok.
- Push, PythonAnywhere deploy'u degildir. Son commit'in canlida calistigi
  bu incelemede dogrulanmadi. Canli ortamda istek/yuk testi yapilmadi.
- Bu belge branch/worktree envanteri ve mevcut raporun guncellenmesidir;
  tum moduller icin yeni bir sizma, akademik veya gorsel denetim degildir.
- Eski `site_audit_2026-09-06.md` tarihsel bulgulari icerir. Durum icin bu
  belge ve `general_review_progress.md` birlikte okunmali.

## Main Disindaki Calismalar

| Alan | Nerede / durum | Ne kaldi? |
|---|---|---|
| Giris denemesi siniri | `codex/oturum-guvenligi-guncel`, `149757b` | Hazir aday topluluk yayini sirasinda bilerek geri alindi. Cloudflare/PythonAnywhere gercek istemci IP siniri teyidi, yeni migration numarasi, guncel main'e dar kapsamli uyarlama ve MySQL testi gerekiyor. |
| Genel guvenlik/hiz paketi | `/Users/ugurismail/Desktop/hafif_ayaklar_genel_inceleme`, `codex/genel_inceleme`, commit edilmemis | Ortam yapilandirmasi, Git'ten .env takibini kaldirma, bagimlilik gecisi, private-cache ve mesaj sorgusu duzeltmeleri var. SEO/oy/rapor gibi bazi kisimlar zaten main'de; radyo kisimlari artik gereksiz. Paket topluca alinmamali. |
| Diyagram editoru | `/Users/ugurismail/Desktop/hafif_ayaklar`, `codex/diagram-editor-improvements`, commit edilmemis | Zoom/pan/fit, okunabilir ok aciklamalari, dugum/ok metin sinirlari, ok yazi boyutu, link gostergesi ve diyagram PDF aciklama sayfalari adayi. Guncel main'deki Word/PDF render sistemiyle uyum ve tarayici testleri gerekiyor. Ayni klasordeki eski SEO/profil farklari ayristirilmali. |
| Harita | `/Users/ugurismail/Desktop/hafif_ayaklar_habit_tracker`, `codex/map-improvements`, commit edilmemis | Cytoscape adayi, ortak baslik/kullanici aidiyeti, filtre/arama ve yeni gorunum. Yeni graph JS/CSS/vendor ve test dosyalari da takip disi. Guncel main'e uyarlama, cok kullanicili yollar, mobil ve buyuk veri kabul testleri gerekiyor. |
| Mantik ders incelemesi | Eski depoda `codex/logic-lesson-review`, `adf61e0` | A1-A3 aday derslerin kaynak, ornek, alistirma ve olcme iyilestirmeleri main'de yok. Insan editor/pilot ve ders ders inceleme tamamlanmis sayilmaz. Mevcut mufredat main'dedir; bekleyen, bu ek revizyon ve tum derslerin insan denetimidir. |
| Insanlarim / degerlendirme | Eski depoda `insanlarim` ve `codex/insanlarim-sifirdan` | Iki ayri deneysel urun dali; insan/ozellik takibi ve degerlendirme modelleri, ekranlari, migration'lari var. Urun karari, mahremiyet ve migration uyumlulugu incelenmeden alinmamali. |

Giris siniri icin eski `0065_login_rate_limit_bucket` dosyasi oldugu gibi
tasinamaz. Main `0067` seviyesinde; yeni numara ve bagimlilik zinciri gerekli.
Bu dal main'in atasi oldugundan normal merge, sonradan geri alinan ozelligi
tek basina yeniden etkinlestirmez. Icerik farki esas alinmali.

### Eski Dallar Her Zaman Eksik Ozellik Degil

- `codex/entry-search-ranking` commit'i farkli kimlikle main'de mevcut;
  `git cherry` esdeger yama olarak isaretledi. Tekrar alinmamali.
- `codex/oturum-guvenligi` eski `5b4fad9` yamasi guncel main'e uyarlanip
  topluluk paketinde yayinlandi. Sifre saklama ve POST logout eksik degil;
  ondan ayri giris hiz siniri bekliyor.
- `codex/unified-word-pdf-exports` dalindaki `a9f3b9c` / `d38f02c` eski
  alternatif PDF uygulamasidir. Main'de yeni ortak Word/PDF sistemi ve
  diyagram export'u var. Bu iki eski commit'in yoklugu PDF ozelliginin
  eksik oldugu anlamina gelmez; yalniz yararli davranis farklari incelenmeli.
- Eski deponun `matematik` dali commit gecmisi guncel main'in atasi;
  ayri bir birlestirme bekleyen dal olarak sayilmadi.
- Davet, mesaj baglantisi, Murekkep/Astra tema, entry referansi/bildirimi,
  Gune Git, yanit eylemleri ve son kelime istatistigi duzeltmeleri main'de.
- Radyo/cikis testleri kasitli kaldirildi. Eski guvenlik paketinden geri
  getirilmeyecek. Bu dallarda ya da eski worktree'lerde dosya bulunmasi
  ozelligin yeniden yayinlanmasi gerektigi anlamina gelmez.
- Bulunamayan gecici worktree kayitlari var; bu tur silme/prune yapilmadi.
  Eski calisma alanlarindaki kullanici degisiklikleri korunuyor.

## Acik Inceleme Maddeleri

Asagidaki ilk yedi madde icin guncel main'de ilgili kod yeniden okundu.
Uretimde istismar/kapasite dogrulamasi yapilmadi.

| Oncelik / kimlik | Guncel durum | Kapanis kosulu |
|---|---|---|
| 1 / SEC-01, SEC-02 | Main hala `.env` takip ediyor; requirements Django 4.2.2. Canli DEBUG kapatma ve anahtar rotasyonu daha once kullanici tarafindan teyit edildi; repo/yapilandirma ve bagimlilik paketi bundan ayri. | Sir degerlerini yaymadan takip temizligi, production ayar sinirlari, hedef surum/bagimlilik uyumu, ayri ortamda kurulum ve MySQL kabul testi. Sunucu .env dosyasini pull sirasinda kaybetmeme plani. |
| 1 / SEC-07 | Davet atomikligi main'de; giris denemesi siniri main'de degil. | Guvenilir IP/proxy teyidi, ortak worker sayaci, migration ve temizlik gorevi, 429 ve mesru giris testleri. |
| 1 / DATA-01 | `attendance_save_state` tum sheets/marks'i yeniden yaziyor. Satir kilidi eski istemci ekranini tespit etmiyor. | Hucre bazli kayit veya surum/409; iki kullanicinin farkli hucreleri korunmali, ayni hucre catismasi sessizce ezilmemeli. |
| 1 / DATA-02 | `HabitEntry.effective_target` hedef yoksa guncel habit.target'i kullaniyor; varsayilan gunluk hedef null tutulabiliyor. | Genel hedef/program degisikligi gecmis basariyi degistirmemeli; tarihli plan veya snapshot ve acik gecmis-duzeltme politikasi. |
| 1 / SEC-04 | LibraryFileForm'da tur/boyut politikasi yok. Editor gorsel yuklemesi ayri akis. | Izinli tip/icerik/boyut/kota; mevcut dosyalarin erisim politikasi ve canli media basliklari kontrolu. |
| 1 / API-01, LEARN-02 | Cetvel/taslak/IAT gibi yollarda JSON nesnesi ve alan sinirlari ortak/tam degil. IAT bilimsel yorumlari ayri denetim istiyor. | Liste/null/bozuk UTF-8/eksik/asiri veri 4xx ile reddedilmeli, kayit yapilmamali; IAT gecersiz denemeden sonuc uretmemeli. |
| 2 / PERF-01, PERF-02 | Ortak sablon diyagram editoru ve MathJax'i yukluyor. Mesaj listesi sayfalama oncesi her konusmaya count/first sorgulari yapiyor. | Ihtiyaca gore asset yukleme; konusma sayisiyla dogrusal buyumeyen sorgular ve olculmus once/sonra karsilastirmasi. |

### Raporda Acik, Bu Tur Yeniden Tam Denetlenmeyenler

- DATA-04: coklu sekme/eski istek/offline donusunde taslak metnini koruma.
  Kenarda Dursun dugmesinin ilk tiklamasi duzeldi; bu ayri veri-kaybi riski.
- OPS-01/02: otomatik CI, MySQL entegrasyonu, yayin/geri donus kilavuzu,
  DB+media geri yukleme tatbikati. Main'de `.github` workflow'u bulunamadi;
  harici CI kurulumu oldugu/bulunmadigi teyit edilmedi.
- Canli MySQL strict mode, slug indeks uyumu, cache/edge/media ayarlari:
  onceki bulgularin kapanisi icin guncel sunucu kaniti gerekiyor.
- PRIV-01/02 ve AUTH-01: personel verisinin repodan ayrilmasi, veri saklama/
  silme, sifre sifirlama, hesap/veri yonetimi ve mahremiyet matrisi.
- UX/UI/A11Y: tum temalar, klavye, mobil, uzun metin ve hata ekranlari;
  tek tek arayuz duzeltmeleri genel erisilebilirlik denetimi degildir.
- MAP/DIAG: veri aidiyeti, ortak dugumler, renk disi ayirt etme, buyuk
  grafikler, cikti/editor veri semasinin uyumu ve hafif izleyici.
- EXPORT-02/PERF-03: buyuk gercek belge ve eksik kaynak/gorsel senaryolari.
  Kullanici PDF sorununun duzeldigini bildirdi; evrensel kapasite garantisi
  yok. Eski timeout'u yeni bir kesin ariza olarak tekrar raporlamiyoruz.
- LEARN-01/03/04: mantik puaninin anlami, ders bazli akademik/pilot onay,
  Almanca olcme/uretim/ilerleme; etik iceriklerin akademik denetimi.
- HABIT-01/02, PERF-04, MONEY-01: plansiz gun/eksik veri ayrimi, tarihsel
  hedefler, saat dilimi ve kacirilmis hatirlatma, buyuk dashboard olcumu,
  para birimi/bakiye/iade/duzenli gider urun kurallari.
- COMMUNITY-01: anket/kaynak/oneri/moderasyon icin capraz rol ve eski
  nesne senaryolari. Son bildirim duzeltmeleri tum olaylarin gelecekte
  hatasiz teslim edilecegi garantisi degildir.
- SEO: yazar/entry teknik duzeltmeleri main'de. Gercek indeks/sorgu/siralama
  icin Search Console verisi gerekiyor; yeni bir kod paketiyle karistirilmaz.

## Onerilen Ilerleme Sirasi

1. Repo/production ayar ve bagimlilik paketini guncel main'e kucuk parcalar
   halinde uyarla; canli guvenilir IP teyidiyle giris sinirini tamamla.
2. Cetvel eszamanli kayit ve aliskanlik gecmisi sorunlarini ayri yamalarla kapat.
3. Yukleme/JSON sinirlarini ve geri yukleme/CI kapilarini tamamla.
4. Mesaj sorgulari ve gereksiz global script yuklerini olcerek azalt.
5. Diyagram ve haritayi ayri entegrasyonlarla bitir; ardindan mantik ders
   incelemesine kullanicinin istedigi ders ders yontemle don.

Bu sira sonraki uygulama icin oneridir; bu rapor turunde yeni ozellik,
eski branch birlestirmesi veya canli ortam ayari degistirilmedi.
