# Genel Inceleme Takibi

## Baslangic: 2026-09-06

- Kaynak: origin/main, 6ba085d (yazar SEO ve herkese acik profiller).
- Branch: codex/genel_inceleme.
- Yerel eski depoda Git mmap zaman asimi oldugu icin temiz klon kullanildi.
- Eski calisma alaninin kaydedilmemis diyagram/profil degisiklikleri korunuyor.
- Ana rapor: site_audit_2026-09-06.md. Rapordaki 43452d9 inceleme tabani
  tarihsel kanittir; yeni main ile ilgili farklar bu dosyada takip edilir.
- Degisiklik oncesi 589 test gecti; gecici SQLite test veritabani kullanildi.

## Main Degisikliginin Degerlendirmesi

- Sayisal kimlikli /yazar/<id>/ sayfasi ve yazar yapisal verileri eklendi.
- /profile/<username>/ artik ziyaretcilere acik. Biyografi de HTML ve meta
  veride yayinlaniyor; bunu ozel biyografi olarak kabul etmemek gerekir.
- Taslaklar, kaydedilenler ve davetlere yetkisiz erisim testleri gecti.
- Hem yazar hem profil URL'si sitemap'e ekleniyor. Canonical ve iki sayfanin
  gorevi SEO asamasinda birlikte degerlendirilmeli; indeks garantisi yoktur.
- Mevcut testlerin gecmesi tum mahremiyet senaryolarinin denetlendigi anlamina gelmez.

## Adim 1: Profil Tanimlarinin Sirasi

- Sorun: Paginator siralanmamis Definition sorgusunu kullaniyordu.
- Degisiklik: created_at azalan, esit tarihlerde pk azalan siralama.
- Kabul: ayni tarihli yedi tanim iki sayfada kayipsiz ve tekrar olmadan listelenir.
- Yeni regresyon testi dahil 590 test gecti (12.633 saniye).
- Onceki UnorderedObjectListWarning kalkti; git diff --check temiz.
- Migration gerekmez. Commit/push/deploy yapilmadi.

## Sonraki Adim

SEC-01: Git'teki gizli degerler ve ortam yapilandirmasi. Uretim anahtarlari
otomatik degistirilmeyecek. Once .env yedegi, aktif anahtarlarin guvenli
dogrulanmasi ve deploy/geri donus adimlari netlestirilecek; anahtar degerleri
rapora veya test ciktisina yazilmayacak.

## Adim 2: Guvenlik ve Hiz Paketi 1

- Ayrintilar ve canliya gecis kapilari: security_rollout.md.
- Django/bagimlilik guvenlik guncellemeleri, uretimde DEBUG kapatma ve anahtar
  zorunlulugu, private cache basliklari, radyo/oy/kaydet yetki sinirlari,
  guvenli rapor yonlendirmesi ve mesaj listesi sorgu optimizasyonu eklendi.
- .env diskte korunarak Git takibinden cikarildi. Paket oncesi guncel sunucu
  yedegi dogrulanmadan push/pull yapilmamali.
- Sonuc: 608 test gecti; requirements pip-audit taramasinda bilinen acik yok.
  check --deploy simulasyonu, migration tutarliligi ve pip check temiz.
- Kullanici WSGI/virtualenv yollarini dogruladi; gizli deger yazdirmayan
  WSGI ayar kontrolu komutu verildi. Sonuc: Python 3.10.12 / Django 4.2.2,
  DEBUG=True, anahtar temel kontrolu False; HTTPS/secure cookies True,
  MySQL ve LocMemCache. 17:02 tekrar kontrolunde DEBUG=False dogrulandi;
  Kullanici Web Reload ve siteye erisimi teyit etti.
- 2026-09-07 Django anahtari kullaniciya verilen komutla sunucuda yenilendi;
  WSGI dogrulamasi basarili. Reload talimati sonrasi giris ve baslik acma
  kontrolu kullanici tarafindan teyit edildi. Eski yedek rotasyon oncesi,
  paket gecisi icin yeni yedek alinacak. Agora, MySQL ve CDN kontrolleri acik.
- Branch icin commit/push/paket deploy yapilmadi; canli DEBUG ve Django
  anahtari duzeltmeleri kullanici araciligiyla uygulandi.

## Adim 3: Kullanici Adi ve Entry SEO Iliskisi

- Kullanici talebi: kullanici adiyla aramalarda yazar ve yazilarinin bulunmasi.
- Main zaten entry basliginda kullanici adini, acik yazar sayfasini ve Person
  baglantisini iceriyor. Bu temel korundu; indeksleme/siralama garantisi verilmez.
- Yazar ProfilePage hasPart verisi sadece gorunen sayfanin en fazla 20 entrysini
  ayni Person kimligine bagliyor. Entry semasina kalici URL, mainEntityOfPage,
  kimlik ve degisiklik tarihi eklendi; paylasim aciklamalari yazar adini iceriyor.
- Mevcut sitemap.xml korundu. robots.txt uzerinden kesfedilen sitemap-entries.xml
  indeksi, entry URL'lerini 1000'lik sayfalara ayiriyor. Entry govdeleri sorgulanmaz;
  soru sluglari select_related ile alinir, her entry icin ek sorgu yapilmaz.
- Taslaklar, e-posta ve ozel hesap bilgileri eklenmedi. Pasif kullanicilarin
  entryleri yeni sitemap'e dahil edilmez. Yetki/oturum davranisi degistirilmedi.
- SEO'ya ozel 18 test gecti: sayfalama, mahremiyet, JSON/HTML kacislari,
  yazar kimligi, sorgu sayisi ve sitemap kesfedilebilirligi.
- Tum regresyon paketi: 613 test gecti (22.341 saniye, izole SQLite ortaminda).
- Canliya gecisten sonra Search Console'a sitemap-entries.xml eklenmeli;
  ornek yazar/entry URL'leri URL Inspection ve Rich Results Test ile incelenmeli.
  Canli Google taramasi bu yerel testlerin kapsami disindadir.
- Kaynak: https://developers.google.com/search/docs/appearance/structured-data/profile-page
- Migration yok; commit/push/deploy yapilmadi.

## SEO Yayini: 2026-09-07

- Kullanici talebiyle profildeki "Herkese acik yazar sayfasi" banner'i kaldirildi.
  Yazar URL'si ve SEO baglantilari korundu.
- SEO ve profil tanim siralama duzeltmeleri temiz origin/main uzerinden
  codex/seo-yayin branch'ine aktarildi. Guvenlik paketi, .env silinmesi,
  requirements ve settings bu yayina dahil edilmedi.
- Django 4.2.2 ile 596 test gecti; makemigrations --check --dry-run ve
  git diff --check temiz. 84b55ed commit'i main'e pushlandi; uzak ref dogrulandi.
- Kullanici sunucuda 84b55ed fast-forward pull, Web virtualenv aktivasyonu,
  collectstatic (0 copied, 179 unmodified) ve basarili manage.py check
  ciktisini paylasti. Bu SEO yayini icin Reload henuz teyit edilmedi.
- Bu inceleme branch'indeki ayni SEO degisiklikleri halen yerel fark olarak
  duruyor. Sonraki birlestirmede 84b55ed ile uzlastirilmali; guvenlik paketinin
  tamamini yanlislikla main'e gondermemek icin dosya bazli kontrol gerekli.

## Siradaki Kontrollu Adim

- Rapor tekrar okundu. SEC-01/02 ve OPS-02 kapsaminda guvenli yayin tabani
  tamamlanacak; yeni ozellik veya toplu main birlestirmesi yapilmayacak.
- Once rotasyon SONRASI .env ve etkin WSGI icin yeni ozel yedek alinacak.
  Bu yalniz ayar yedegidir, DB/media yedegi veya restore testi yerine gecmez.
- Ardindan DB/media yedek ve geri yukleme plani, ayri aday virtualenv/test DB,
  MySQL uyumluluk kontrolleri tamamlanmadan requirements canlida kurulmayacak.
- Strict Mode kapali bilgisi kayitli; uretimde habersiz etkinlestirilmeyecek.
- Kullanici rotasyon sonrasi ayar yedegini dogruladi:
  /home/uia1/.hafif-postrotation-6ypz13yj (env.backup, wsgi.backup).
  Komut kopyalarin kaynakla byte esitligini kontrol etti; site degismedi.
  Siradaki adim DB yedegi icin etkin DB adi, mysqldump ve disk on kontrolu.

## Siteye Ozel Saldiri Yuzeyi: 2026-09-07

- Kullanici yedek hazirligini durdurup site kodundaki saldiri yollarina
  odaklanilmasini istedi. Inceleme canlidaki 84b55ed tabaninda yapildi.
- Canli istek veya gercek DB yazimi olmadan RequestFactory/mock kontrolu:
  report_content gecersiz icerik + harici next ile dis adrese 302 donuyor.
- update_listener_count anonim request ile mock program sayacini degistirip
  200 donuyor. Bu gorunum fonksiyonu yetki testidir; CSRF middleware atlandi,
  dolayisiyla CSRF acigi veya canli istismar testi olarak yorumlanmamali.
- LibraryFileForm zararsiz probe.html dosyasini kabul etti. Yukleme rol ile
  sinirli; zararlı aktif icerigin etkisi medya origin/MIME/indirme basliklarina
  bagli. Editor gorsel yolu ayrica tur/boyut/Pillow kontrolu iceriyor.
- Export'taki dogrudan openpyxl hucre atamasina '=1+1' verildiginde data_type=f.
  Bu temel formül yorumlama kaniti; dis veri sizdirma/istemci kod calistirma
  testi yapilmadi. Kullanici metinleri literal string hucre olarak yazilmali.
- Login kodunda uygulama hiz siniri yok; Cloudflare korumasi henuz bilinmiyor.
  send_invitation kota kontrolu transaction disinda ve satir kilidi yok;
  yaris kosulu kodda mevcut, paralel MySQL testi yapilmadi.
- XSS/SQL injection/genel hesaplar arasi veri sizintisi bu kontrollerle
  kanitlanmadi. mark_safe tek basina XSS kaniti degildir.
- Bu tur uygulama kodu degistirilmedi veya pushlanmadi. Yerel guvenlik
  paketindeki rapor/radyo/oy duzeltmeleri halen canliya aktarilmadi.

## Radyo ve Cikis Testlerini Kaldirma

- Son kullanici talebi: iki ozelligi kaldir, diger ozellikleri koru.
- Calisma: /tmp/hafif-seo-release, codex/ozellik-kaldirma, main 84b55ed tabani.
- View/template/admin/menu, Agora yardimcilari ve global radyo sorgusu kaldirildi.
  Eski URL'ler 410/noindex; tarihi modeller/tablo ve kayitlar korunuyor.
- Cetvel yetkisi can_manage_attendance olarak adlandirildi; is_dj DB sutunu
  aynen korundu. 0063 yalniz migration state'ini degistiriyor, SQL no-op.
- Django 4.2.2 ile 602 test gecti; model/migration tutarliligi ve diff temiz.
- Commit/push/deploy yapilmadi. Ayrintilar feature_retirement.md dosyasinda.
- Bekleyen guvenlik paketindeki radyo dosyalari/testleri daha sonra
  birlestirilmemeli; ozelligi tekrar eklememek icin paket yeniden ayrilacak.

## Kaldirma Paketi Yayini: 2026-09-11

- Kullanici sonraki adima gecmeyi onayladi. Django 4.2.2 ile 602 test tekrar
  gecti (13.012 saniye); migration tutarliligi ve diff temiz.
- 93841c7 main'e pushlandi. Guvenlik paketi/.env kaldirilmasi ve Django
  yukseltmesi dahil degil. Sunucuda pull/migrate/collectstatic/check ve Reload
  sonrasi cetvel erisimi kullanici tarafindan teyit edilmeli.

## Icerik ve Export Yayini: 2026-09-12

Bu bolum onceki tarihli yayin durumlarinin guncel devamidir. Eski guvenlik
paketinin tamami main'e alinmadi; tamamlandi sanilmamali.

- Kullanici cetvelin canlida calistigini teyit etti. Radyo/cikis testi kaldirma
  paketi 93841c7 main'de; SEC-03/FLOW-01 kaldirilan ozellikler kapsaminda kapali.
- SEC-05/06: rapor yonlendirmesi ve oy/kaydet/koleksiyon yetki/atomiklik
  duzeltmeleri yerelde dogrulandi. Ayrintilar content_security.md.
- EXPORT-01 ve DIAG-02'nin basili cikti kismi: Word/PDF ortak icerik, diyagram,
  ok aciklamalari, dipnot/kaynakca. Derin liste ve davet kopyalama duzeltmeleri
  dahil. Editorun diger branch'teki degisiklikleri dahil DEGIL.
- 643 test: 641 basarili, SQLite'ta iki kilit testi atlandi; bu iki test onceki
  MySQL 8.0.46 kosusunda gecti. Word/PDF HTTP indirmeleri yerelde dogrulandi.
- Kullanici main pushunu onayladi. Canli deploy ve PythonAnywhere PDF native
  kutuphane kontrolu henuz yapilmadi. Ayrintilar content_export_improvements.md.
- Siradaki is SEC-09: XLSX kullanici metinlerini formul olmadan literal saklama.
  Once regresyon testi, sonra dar kapsamli duzeltme, tam test ve ayri onay.
- SEC-01 repo/env temizligi ve SEC-02 desteklenen Django gecisi acik; canlida
  DEBUG/anahtar rotasyonu kullanici tarafindan daha once dogrulandi. Diger
  yukleme, giris/davet kotasi, API, veri kaybi ve performans maddeleri acik.

## Yayin Dogrulamasi ve SEC-09: 2026-09-12

- Onaylanan icerik/export/etkilesim paketi d13dc0b main'e pushlandi.
  `git ls-remote origin refs/heads/main` ile uzak commit dogrulandi.
  PythonAnywhere pull/kurulum/Reload henuz teyit edilmedi; push deploy degildir.
- Siradaki is icin bu commit'ten codex/xlsx-guvenligi branch'i acildi.
- SEC-09 once regresyonla tekrarlandi: XLSX XML'inde kullanici metninden
  formul dugumleri olusuyordu; #N/A metni hata turune donusuyordu.
- Soru, entry ve kaynak metinleri artik acik string hucre turunde yaziliyor.
  Gorunen metne apostrof eklenmiyor; yil/kaynak numarasi sayisal kaliyor.
  Siralama, secim, sahiplik ve Word/PDF kodu korunuyor.
- Bes yeni test: gruplanmis ve ozel sirali cikti, kaynaklar, formul benzeri
  onekler/hata metni/Turkce/satir sonlari, yetki. Kaydedilen XLSX yeniden
  acilarak deger/tur dogrulandi; XML'de formul ve externalLinks yok.
- Tam suite: 648 test, 646 basarili, iki MySQL kilit testi SQLite'ta atlandi
  (16.560 saniye). git diff --check temiz. Yeni migration/bagimlilik yok.
- Excel/LibreOffice arayuzunde bu yama icin dosya acma denenmedi. Dosya turu
  ve serilestirme dogrulamasi yapildi; canli istismar veya uretim DB yazimi yok.
- SEC-09 yerelde dogrulandi, henuz commit/push/deploy edilmedi.
- Bir sonraki aday SEC-07: davet kotasinin eszamanli isteklerle asilmasini
  onleme. Giris hiz siniri icin paylasimli cache/CDN kosullari ayrica
  dogrulanmali; LocMemCache'i cok worker'li koruma gibi kabul etmeyecegiz.

## SEC-07 Davet Kotasi: 2026-09-13

- Kullaniciya main d13dc0b icin pull, Web virtualenv, requirements, WeasyPrint
  native kontrolu, collectstatic/check ve Reload adimlari verildi. Canli
  sonuc henuz gelmedi. Excel/davet degisiklikleri bu pull'a dahil degil.
- SEC-09 yerel 438b20b commit'inde korundu; pushlanmadi.
- codex/davet-guvenligi bu commit uzerinde ilerliyor. Ayrintilar
  invitation_security.md. Eski codex/genel_inceleme topluca birlestirilmedi.
- Iki davet olusturma yolunda kosullu atomik kota dusumu + kod olusturma,
  insert basarisizliginda rollback ve dogru kalan kota gosterimi tamamlandi.
- Tema, fotograf ve kelime tercihi kayitlari eski kotayi geri yazamasin diye
  yalniz degisen alanlari kaydediyor. Bu kapsam yeni regresyonlarla dogrulandi.
- Kayit anindaki mevcut tek kullanim kilidi korundu ve ayni kodla iki paralel
  kayit denemesinden yalniz birinin hesap olusturdugu MySQL'de dogrulandi.
- 662 test: 657 gecti, SQLite'ta 5 concurrency testi atlandi (17.876s).
  MySQL 8.0.46'da ilgili 44 testin tamami gecti (1.965s), atlanan test yok.
  Migration/bagimlilik degisikligi yok. Uretim verisine dokunulmadi.
- SEC-07 KISMEN dogrulandi; giris denemesi/hiz siniri halen acik. Bu paketi
  tam hesap guvenligi veya bagimsiz sizma testi olarak yorumlamiyoruz.
- Siradaki is: giris/kayit/davet kotasindan ayri istek-hizi korumasi icin
  mevcut CDN ve cok worker'li depolama kosullarini dogrulayip dar plan cikarmak.
  Destek disi Django ve diger rapor maddeleri halen acik.

## Export Bekleme ve Buyuk PDF: 2026-09-14

- Davet paketi yerel a8b712d commit'inde korundu; Excel 438b20b ile birlikte
  henuz pushlanmadi. Main son onayli yayin d13dc0b.
- Kullanici d13dc0b pull, requirements, WeasyPrint/Pango ve Django check
  basarili ciktilarini paylasti. Ayni secim Word olarak (~20 MB) iniyor;
  PDF canlida 60 saniye sinirina takiliyor. Bu canli sorun acik tutuluyor.
- Araya alinan is: indirme bekleme bildirimi, sayfadan ayrilmadan hata/iptal,
  secimi koruma ve tekrarli istegi onleme. Ayrintilar download_progress.md.
- Tekrarlanan PDF bicim cozumlemesi ve gereksiz dipnot yerlesim gecisi
  azaltildi. Sure/guvenlik limitleri veya cikti anlami gevsetilmedi.
- 666 Django testi: 661 basarili, 5 SQLite concurrency atlamasi. Ilgili MySQL
  senaryolari onceki 44 testte gecti. Ek 8 JavaScript testi ve desktop/mobile
  Chrome bekleme/503/iptal/yeniden-deneme kontrolleri basarili.
- Sentetik hiz olcumleri sadece yerel kanit. Gercek buyuk secim yeniden
  denenmeden timeout maddesi kapatilmayacak. Arkaplan export altyapisi yok.
- Kullanici onayi olmadan yeni paket push/deploy edilmeyecek. Guvenlik
  raporundaki istek-hizi korumasi ve desteklenen Django gecisi halen acik.

## Main Yayin Onayi: 2026-09-19

- Kullanici 438b20b (XLSX), a8b712d (davet kotasi) ve 63cb0d3
  (indirme bekleme/PDF optimizasyonu) paketlerinin main'e alinmasini onayladi.
- Yayin oncesi sabitlenmis requirements ile izole test ortami yeniden kuruldu:
  666 Django testi, 661 basarili, 5 SQLite concurrency atlamasi (19.401s).
  Sekiz JavaScript testi gecti. Migration kontrolu ve git diff --check temiz.
- Yeni bagimlilik veya migration yok. PythonAnywhere pull, collectstatic,
  check ve Web Reload kullanici tarafindan yapilmali; push deploy degildir.
- Buyuk PDF timeout maddesi ACIK. Deploy sonrasinda ayni secim denenmeli.
  Devam ederse kullanicinin paylasmayi uygun gordugu Word ciktisiyle yerelde
  tekrar uretim ve asama bazli sure olcumu yapilacak. Dosya boyutu tek basina
  neden belirlemek icin yeterli degil. Sure limitleri korundu; canli veriye
  erisim veya ucuncu taraf donusturucu kullanimi yapilmadi.

## Yanit Eylemleri: 2026-09-19

- ef1dfca main'e pushlandi ve uzak ref dogrulandi. Kullanici indirme sorununun
  cozulmus gorundugunu bildirdi; tum buyuk belgeler icin garanti verilmiyor.
- Araya alinan kullanici istegi: Guncelle/Kenarda Dursun dugmeleri uzun canli
  onizlemenin altinda kalmasin. codex/yanit-eylemleri dalinda sekiz yanit/baslik/
  duzeltme formunda mevcut eylemler metin alanindan sonra, onizlemeden once.
- Alti taslakli formun dugmeleri mobilde sarilan tek bir eylem satirinda.
  Mevcut ID, submit turu, CSRF, taslak ve yayinlama davranislari korundu;
  sunucu kaydetme kodu veya yeni API/migration/bagimlilik degisikligi yok.
- Uc regresyon testi: sekiz formun gercek HTML sirasi/form aidiyeti, uzun
  duzenleme taslagini yayinlamadan kaydetme/geri acma, mevcut guncelleme POST'u.
- Tam suite: 669 test, 664 basarili, 5 SQLite concurrency atlamasi (17.830s).
  Chrome 1440px ve 390px: 6900px uzun onizlemede dugme kutunun hemen altinda;
  gercek yerel taslak POST'u basarili, metin ve sayfa korunuyor. Ekran
  goruntuleri incelendi. Canli veriye dokunulmadi; bu UI yamasi pushlanmadi.
- Sonraki rapor isi halen SEC-07 istek-hizi korumasi ve desteklenen Django
  gecisinin planlanmasi; eski guvenlik dali topluca alinmayacak.

## Gune Git: 2026-09-20

- Yanit eylemleri 48a9566 ile main'e yayinlandi. Kullanici istegiyle yeni
  codex/gune-git dali bu main commit'inden acildi; canliya push yapilmadi.
- Secilen gunde entry girilen basliklar solda birer kez listeleniyor.
  Siralama o gunun ilk entry saatine gore eskiden yeniye; esitlikte baslik ID.
  Saat ve o gunku entry sayisi gorunuyor. Merkez akis degistirilmedi.
- Gun sinirlari Europe/Istanbul saatine gore hesaplanir. Sorgu tarih araligi
  kullanir, created_at uzerine tarih donusumu uygulamaz. 20 basliklik sayfalama,
  onceki/sonraki gun ve Guncel'e donus var. Gecersiz/gelecek tarih bos sonuc
  ve acik hata verir; sessizce baska gunun basliklarini gostermez.
- Takip filtresi secilen tarihi korur. Basligin sahibi veya o gun entry yazan
  kisi takip ediliyorsa baslik dahil edilir. Eski bir takipli entry yeterli
  degildir. Tarih/paginasyon secimi eski rastgele listeyi gecersiz kilar.
- Doldur/Git aciklamali simgelere, tarih acilir alana donustu. Ana sayfanin
  mobil baslik sutunundaki sabit yukseklik boslugu azaltildi; detay sayfasinin
  mevcut mobil acilir paneli korundu.
- 10 yeni test; tam suite 679 test: 674 basarili, 5 SQLite concurrency
  atlamasi (17.692s). Yeni gun listesinde sayim ve sayfa 2 sorgu, N+1 yok.
  Migration kontrolu ve git diff --check temiz. Yeni bagimlilik yok.
- Chrome 1440/390px: tarih formu, konu linkinde tarihi koruma, onceki gun,
  Doldur/Guncel, eski sessionStorage listesinin temizlenmesi, girisli Takip
  ac/kapat dogrulandi. Ekran goruntuleri incelendi; panel tasmasi giderildi.
- 127.0.0.1:8000 yerel SQLite kopyasiyla acik. Kaynak veritabani, canli veri
  ve kullanici sifreleri degistirilmedi. Yerel kopyada bulunmayan eski medya
  dosyalari ayrica 404 verebilir; bu paket medya tasimasi yapmiyor.
- Oturum guvenligi calismasi codex/oturum-guvenligi dalinda 5b4fad9 olarak
  ayri tutuluyor; bu dal/main paketine dahil degil. Siradaki guvenlik isi
  yayin onayi ve SEC-07 hiz siniri/Django surum gecisi; genel rapor devam ediyor.

### Sol Arac Cubugu Gorsel Revizyonu

- Kullanici ilk tasarimi reddetti: tarih fazla merkezi, Doldur/Git belirsiz,
  baslik ve siralama aciklamalari gereksizdi. Onceki gorunum yerine iki sutunlu,
  esit agirlikli Doldur/Git/Takip/Tarih araclari kullanildi; gorunur bolum
  basligi, toplam sayisi ve siralama aciklamasi kaldirildi.
- Tarih formu sadece istenince acilir; Escape kapatir ve odagi dugmeye verir.
  Secili gun varsa kucuk tarih/onceki/sonraki/sifirla satiri gorunur. Rastgele
  mod dugmenin secili durumuyla belirtilir. Liste ismi erisilebilirlik etiketi
  olarak korunur; veri sorgulari ve kronolojik siralama degistirilmedi.
- 11 ilgili Django testi gecti. Chrome 1440/1024/390px: tasma yok; tarih,
  klavye odagi, Takip, Doldur ve sifirlama akislari gecti, JS hatasi yok.
  Ekran goruntuleri incelendi. CSS/JS onbellek anahtari day2 olarak yenilendi.
- Main/push yapilmadi; codex/gune-git dalinda yerel onay bekliyor.

### Astra ve Kompakt Sifirlama

- Kullanicinin ek geri bildirimiyle rastgele listeyi sifirlama simgesi ayri
  satirdan Doldur/Git satirina alindi. Secili tarihin kaldirma dugmesi tarih
  satirinda kalir. Rastgele modda arac alani masaustunde 86px; eski 124px
  bosluk kullanilmiyor. Dar ekranlarda metin/ikon tasmasi test edildi.
- Astra, mevcut Hazir Tema secicisine eklendi: acik gri/beyaz yuzeyler,
  grafit navbar, petrol yesili birincil ve murdum ikincil vurgu, Georgia 18px.
  Var olan profil renk/font alanlarini kullanir; yeni migration, bagimlilik,
  varsayilan tema degisikligi veya diger kullanicilara otomatik uygulama yok.
- Uc yeni tema testi: secim/sistem fontu, tum kalici alanlarin kaydi ve
  varsayilana donus, diger hesap/kota korunmasi, ana renk ciftlerinde en az
  4.5 kontrast. Testteki ana sayfa onbellegi temizlenerek suite izolasyonu
  saglandi; uretim onbellek davranisi degistirilmedi.
- Tam suite 683 test: 678 basarili, 5 SQLite concurrency atlamasi (17.984s).
  Chrome 1440/1024/390px: ayarlardan gercek tema kaydi, yeni sayfada kalicilik,
  tarih, Doldur ve kompakt sifirlama; JS hatasi veya yatay tasma yok.
  Ekran goruntuleri incelendi. Yalniz ayri yerel test hesabi kullanildi.
- CSS/JS day3 onbellek anahtariyla yenilendi. Main'e alinmadi/pushlanmadi.

### Tema Incelemesi ve Font Katalogu: 2026-09-21

- Kullanici genel tema yorumu ve daha fazla yazi tipi istedi. 28 presetin
  temel renk ciftleri incelendi; ayrintilar theme_typography_review.md.
  Old Money/The Philosopher ve diger paletler degistirilmedi. Zayif kontrast,
  eksik preset alanlari ve okuma/arayuz fontunun ayrilmasi sonraki adimlar.
- Bes mevcut gruba 40 font eklendi, toplam 95. Google Fonts CSS cevabi ve
  font cmap tablosuyla her eklenen ailenin Turkce harfleri kontrol edildi.
  Eksik harfli Assistant ve eski Atkinson Hyperlegible alinmadi; Next alindi.
- Yeni fontlar topluca yuklenmez. Ayarlarda kayitli font icin yinelenen
  dinamik istek kaldirildi; secim degisiminde tek dinamik stylesheet kalir.
  Font secimi mobilde tam genislikte; boyut etiketi dogru inputa baglandi.
  Alt form boslugu sabit sohbet/yardim kontrollerine yer birakir.
- 685 Django testi: 680 basarili, 5 SQLite concurrency atlamasi (18.122s).
  40 fontun her biri POST/yeniden acmada secili olarak dogrulandi. Chrome'da
  Literata, Atkinson Hyperlegible Next, IBM Plex Mono ve Space Grotesk gercek
  font yuklemesi/kalicilik testi gecti; 95 font icin toplu istek yok.
  1440/390px ekran goruntuleri incelendi. Yeni migration/bagimlilik yok.
- codex/gune-git dalinda; main/push yok. Yerel site 8000 portunda acik.

### Sol Alan: Gorunum ve Islem Ayrimi

- Kullanici dort parcali arac duzenini tekrar uygun bulmadi. Iki sutunlu
  Doldur/Git/Takip/Tarih izgarasi kaldirildi. Ustte Tumu/Takip gorunum secimi,
  altta tek satir Doldur/Git/Tarih araclari var. Baslik veya sayac aciklamasi
  eklenmedi. Geri donus simgesi secim satirinin saginda kalir.
- Takip checkbox'i ayni GET degerlerini kullanan erisilebilir radio grubuna
  donustu. Tumu=0 ve Takip=1, secilen gunu korur. Gorunumler arasi gecis
  eski rastgele listeyi temizler. Dar sutunda islem isimleri korunur,
  sadece dekoratif ikonlar gizlenir; mobilde dokunma yuksekligi 40px.
- 19 ilgili Django testi gecti. Chrome 1440/1024/390px: Tumu/Takip,
  tarih, Doldur ve sifirlama dogrulandi; yatay tasma/JS hatasi yok.
  Ekran goruntuleri incelendi. CSS/JS day4; main/push yok.

### Onaylanan A Tasarimi ve Yazar SEO Kontrolu: 2026-09-26

- Kullanici iki taslaktan A'yi secti. Sol alan tek satira indirildi:
  Tumu/Takip native select ve Doldur/Git/Tarih simgeleri. Tooltip ve
  erisilebilir isimler var; gun, takip, rastgele liste ve sifirlama korunur.
  Dar sutunda araclar ikinci satira gecer; dokunmatik hedefler 44px.
  CSS anahtari day5. Chrome 1440/1024/390px ve dokunmatik mobil kontrolu:
  tasma ve JS hatasi yok; tarih/takip/rastgele/sifirlama akislari gecti.
- Canli arama taramasinda Ugur Ismail Aygun'un profil, yazar ve entry
  sayfalari bulundu. Bu, Google'daki sira veya Google tarafindan secilen
  canonical icin kanit degildir; Search Console URL denetimi bekleniyor.
- Profil entry sayfalari hep ilk sayfaya canonical veriyordu. Artik
  answer_page>1 kendi temiz adresini kullanir; gecersiz sayfa ilk sayfaya
  doner. Tarih esitliginde pk siralamasi sayfa sinirlarini sabit tutar.
- Profil ve entry schema'larindaki Person ayni sabit yazar adresini kullanir.
  Yazar schema'sindaki entry'lere gorunur ozet, yazar adi ve dateModified
  eklendi. Ana sayfa ve ortak entry kartlarinda misafir yazar baglantilari
  ayni kimlik adresine gider; oturum acanlar normal profile gider.
- AuthorSitemap'in entry x baslik JOIN carpimi bagimsiz alt sorgulara
  donusturuldu; gercek acik icerik guncellemesinden lastmod eklenir.
  Taslaklar/aktif olmayan yazarlar dahil degil. Profilde istenmeyen ek
  yazar sayfasi baglantisi geri eklenmedi. URL tasinmadi; migration yok.
- 43 ilgili test ve check gecti. Genel suite bu ortamda Word/diyagram
  aktarimindaki reportlab.graphics.svgpath importunda ilerlemedi ve
  durduruldu; tam suite basarili kabul edilmemeli. Bu moduller degistirilmedi.
- Dal codex/gune-git. Main/push yapilmadi; yerel onay bekleniyor.

SEO kaynaklari:
- https://developers.google.com/search/docs/appearance/structured-data/profile-page
- https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls

### Genel Test Engelinin Kapatilmasi: 2026-09-26

- Onceki Word/diyagram test takilmasi temiz ortamda yeniden incelendi.
  Eski Desktop venv'inde ReportLab shapes.py `compressed,dataless` idi;
  paket metadata kontrolu de ilerlemedi. Sinirli tekil import daha sonra
  basarili oldu. Yerel dosya/ortam sorunu bulgusu var; uygulamada
  deterministik kilitlenme kaniti yok.
- Mevcut requirements.txt ile /private/tmp/hafif-validation-20260926
  ortaminda sifirdan kurulum yapildi. Eski ortam, paket surumleri ve
  calisan/canli veritabani degistirilmedi. Uygulama koduna bypass eklenmedi.
- Gercek Word/PDF ve diyagram uretimi: 17/17 test, 3.516s.
- Genel suite: 690 test, 685 basarili, 5 SQLite satir kilidi atlamasi;
  hata yok, 17.992s. Onceki "genel suite tamamlanamadi" durumu kapandi.
- Indirme JavaScript testleri 8/8; pip check temiz; migration farki yok.
- Atlanan iki oy ve uc davet eszamanlilik testi ayri MySQL/PostgreSQL test
  veritabaninda calistirilmali; canli DB'de degil. Uretim garantisi verilmedi.
- Tekrarlanabilir ortam/komutlar: local_validation.md. Main/push yok.
