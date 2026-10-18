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

### Entry Referanslari ve Bildirimleri: 2026-09-27

- `codex/entry-references`: #numara referansi, kalici /entry/numara/ adresi,
  entry menusunden referans/link kopyalama ve Word/PDF baglantilari eklendi.
- Referans verilen entry sahibine yayinlama ve yeni referans eklenen duzenleme
  sirasinda bildirim gider. Kendi entrysi, gecersiz hedef, taslak, onizleme,
  kod/formul ve tekrarlanan kayit bildirim uretmez.
- Kaynak/hedef bazli benzersiz bildirim gecmisi, kaldirip yeniden ekleme veya
  bildirimi silme sonrasi tekrari engeller. Ayni kayitta ayni yazara ait birden
  cok referans tek bildirimde birlesir. Bildirim kaynak entryyi acar.
- 38 odakli test gecti. Genel suite: 728 test, 723 basarili, 5 mevcut SQLite
  satir kilidi atlamasi. Chrome iki hesapla yayinlama/bildirim/baglanti akisi ve
  mobil referans kopyalama dogrulandi. Gecici QA hesaplari temizlendi.
- 0064 migration yerelde uygulandi; canli yayin icin migrate gerekecek.
  Main/push yapilmadi. Davranis ve sinirlar: entry_references.md.

### Bildirim Zili Sayaci: 2026-09-27

- Ilk HTML yanitinda eksik olan okunmamis bildirim/mesaj sayilari lazy context
  processor ile saglandi. Arama formuna bagimli JS sayac baslatma ayrildi.
- Gorunur sayfalarda 15 saniyede bir ve pencereye donuste yenileme yapilir;
  gizli sekmeler sorgulamaz. Eszamanli istekler engellenir, ag hatalarinda mevcut
  sayac korunur. Bildirim sayisi navbar onbelleginden degil canli sorgudan gelir.
- Bildirim listesini acmak artik tum bildirimleri okundu yapmaz. Hedefi acma,
  tekil okundu ve tumunu okundu islemleri CSRF korumali POST kullanir.
- 7 yeni Django ve 6 JavaScript testi gecti. Genel suite: 735 test,
  730 basarili, 5 mevcut SQLite satir kilidi atlamasi; hata yok.
- Yerel tarayicida ilk sayac, yenilemeden yeni bildirim, liste ziyareti ve
  tekil/tumunu okundu sayac davranislari dogrulandi. Gecici QA verisi temizlendi.
- Ek migration yok; ayni codex/entry-references dalinda, main/push yapilmadi.

### Entry Referanslari Yayin Onayi: 2026-09-27

- Kullanici referans sistemi ve bildirim zili duzeltmelerinin birlikte main'e
  alinip pushlanmasini onayladi. Oturum guvenligi dali bu yayina dahil degil.
- Yayin adimlari: git pull --ff-only origin main, migrate,
  collectstatic --noinput, check ve PythonAnywhere Web Reload.
- 0064 migration yeni bildirim gecmisini olusturur; eski entryler icin geriye
  donuk bildirim gonderilmez. Uzak canli uygulama testleri yayin sonrasi yapilir.

## Oturum Guvenligi: 2026-09-20

- Yanit eylemleri 48a9566 main'e pushlandi; uzak ref dogrulandi. Kullaniciya
  pull/collectstatic/check/Web Reload komutlari verildi. Canli deploy teyidi
  henuz alinmadi. Bu not onceki bolumun yerel/pushlanmadi durumunu gunceller.
- codex/oturum-guvenligi main 48a9566 uzerinden acildi. SEC-07 incelemesinde
  daha acil yeni SEC-10 bulundu: login.html remember-me ile parolayi acik
  localStorage'a yaziyordu. Bu riskin kod kaniti var; sizinti kaniti yok.
- Parola saklama kaldirildi, eski iki anahtar paylasilan sayfalarda okunmadan
  siliniyor. Oturum suresi korunuyor. SEC-08 icin POST+CSRF cikis, guvenli
  next donusu, no-store ve hassas parola alani isaretlemesi tamamlandi.
- 680 Django testi: 675 basarili, 5 SQLite concurrency atlamasi (18.652s).
  11 Node testi ve Chrome 1440/390px gercek yerel giris/cikis kontrolleri gecti.
  Migration ve bagimlilik degisikligi yok. Ayrintilar auth_session_security.md.
- Oturum paketi henuz main'e alinmadi/pushlanmadi. SEC-07 hiz siniri ve SEC-02
  Django gecisi acik. Paylasimli sayac ve guvenilir istemci IP siniri
  dogrulanmadan LocMemCache tabanli koruma tamamlandi diye sunulmayacak.

## Oturum Guvenliginin Guncel Main'e Uyarlanmasi: 2026-09-28

- b30a8ae main uzerinden codex/oturum-guvenligi-guncel acildi. Eski 5b4fad9
  yamasi tek tek incelenip uygulandi; sonraki tema, tarih ve bildirim
  degisiklikleri korundu. Rapor catismasinda iki donemin kayitlari da tutuldu.
- Duz metin sifre saklama kaldirildi; eski iki localStorage anahtari okunmadan
  silinir. Beni hatirla oturum suresini belirlemeye devam eder. Cikis POST+CSRF,
  giris donusu guvenli ayni-host URL, giris/cikis yanitlari no-store.
- 15 odakli Django ve 13 Node testi gecti. Genel suite: 750 test,
  745 basarili, 5 mevcut SQLite satir kilidi atlamasi, 19.461 saniye.
- Izole yerel DB ve sentetik hesapla tarayicida giris/donus/cikis/korumali
  sayfa kontrolu gecti. Migration/paket/uretim ayari degisikligi yok.
- Durum: yerelde dogrulandi, main/push/canli yayin YOK. SEC-08 ve SEC-10
  canlida kapanmis sayilmaz; yayin onayi ve deploy sonrasi kontrol gerekiyor.
- Sonraki is SEC-07: WSGI worker'lari arasinda paylasilan hiz siniri ve
  guvenilir istemci IP tespiti. SEC-02 Django gecisi ayrica acik.

## Giris Hiz Siniri: 2026-10-07

- Ayni codex/oturum-guvenligi-guncel dalinda normal/admin girislerine ortak,
  MySQL satir kilitli deneme sayaci eklendi. IP/subnet basina 60, hesap+IP
  basina 10 deneme/5 dakika. Genel hesap kilidi yok; reddedilen istekler sureyi
  uzatmaz. 429/Retry-After, hata halinde 503 ve Turkce bekleme ekrani var.
- CSRF kontrolunden sonra, sifre dogrulamadan once calisir. Raw sifre/kullanici
  adi/IP saklanmaz; HMAC anahtar kullanilir. 0065 migration ve suresi dolmus
  sayaclari temizleyen komut eklendi. Uretim bagimliliklari degismedi.
- PythonAnywhere X-Real-IP ve dogrulanmis Cloudflare IP aglari desteklenir;
  istemcinin X-Forwarded-For basligina guvenilmez. Cloudflare proxy ayari icin
  kullanicidan yanit bekleniyor. Dogrulama olmadan deploy yapilmayacak.
- Ilk MySQL paralel testinde sayac olusturma kilit cakismasi yakalandi ve
  duzeltildi. MySQL 8.0.46/PyMySQL test ortaminda 37 test, sifir atlama;
  yeni/mevcut/suresi dolmus sayacta 8 baglantidan yalniz izinli 3'u geciyor.
- Genel SQLite suite: 772 test, 766 basarili, 6 row-lock atlamasi; 22.628 s.
  Tarayicida gercek form POST'u ile 429 mesaji/donus akisi kontrol edildi.
- Yerel uygulama DB'sine veya canliya migration uygulanmadi. Main/push yok.
  SEC-07 uretimde tamamlandi sayilmaz. Devreye alma/temizlik ve sinirlar:
  login_rate_limit.md. Siradaki kapilar: Cloudflare teyidi ve yayin onayi.

## Mesajlasma, Bildirim ve Davet Aktarimi: 2026-10-12

- Kullanici talebi: mesaj ekraninin sol paneli, eksik bildirimlerin kontrolu
  ve kullanicilarin kendi davet haklarini birbirine aktarabilmesi.
- Mesaj listesi/detayi artik ortak left_frame_context ve ortak baslik listesi
  kullaniyor. Eksik CSS, tarih/takip baglantilari ve sinirsiz sol liste
  giderildi. Mobilde sohbet once, baslik paneli sonra; uzun adlar sariliyor.
- Sohbet acmak ayni kisinin diger bildirimlerini de okundu yapiyordu; artik
  yalniz ilgili mesajlar okunur. Navbar cache hit durumunda mesaj sayaci da
  veritabanindan tazelenir; bildirim sayaci ile birbirine karistirilmaz.
- Bahsetmeler save akisinda merkezilestirildi. Kullanici adi harf farkindan
  kaynakli eksik bildirim, form+signal cift bildirimi ve revizyon yollarinda
  eksik bahsetme giderildi. Degismeyen bahsetme yeniden gonderilmez.
- Yeni QuestionRelationship olusturulunca ust basligi takip edenlere alt
  baslik bildirimi gider; gonderen baglantiyi ekleyen kisidir. Baslik/entry
  guncellemesi yalniz icerik degisince bildirilir, oy/sabitleme metadata'si
  yanlis guncelleme bildirimi uretmez. Kullanici takip/birakma POST+CSRF;
  tekrar takip ayni bildirimi cogaltmaz, kendini takip engellendi.
- Oy/kaydet bildirimlerinde sessiz except/pass kaldirildi. Bildirim ve
  eylem ayni transaction'da: bildirim yazilamazsa eylem de geri alinir.
- Davetler sekmesinde aktarim baglantisi, alici+adet formu ve taraflara ozel
  son 30 aktarim gecmisi eklendi. 0066 yeni ledger tablosu. Atomik borclandirma
  ve alacaklandirma, sabit sirali profil kilitleri, imzali kullaniciya bagli
  1 saatlik islem kimligi, tekrar gonderime karsi koruma, pozitif miktar ve
  tavan kontrolu var. Kendine/pasif hesaba/eksik bakiyeyle aktarim reddedilir.
  Aliciya site ici bildirim gider. Yeni hak uretilmez; aktarim geri alinamaz.
- Test: 796 Django testi, 786 basarili, SQLite'a ozgu 10 atlama (24.386s).
  Gecici MySQL 8.0.46/PyMySQL ortaminda 67 odakli testin tamami gecti
  (4.689s, atlama yok): paralel aktarim, tekrar token, ters yonlu aktarim,
  davetiye olusturmayla yarisan bakiye ve giris sayaclari dahil.
  Bilinen mysql.W003 slug uzunlugu uyarisi ayri inceleme konusu olarak suruyor.
- Referans, duzeltme onerisi/sonucu ve aliskanlik hatirlatma testleri genel
  suite icinde gecti. Bu kontrol site ici bildirimler icindir; e-posta/push
  teslim garantisi veya gecmis kayip bildirimleri yeniden gonderme yoktur.
- Tarayici: izole sentetik DB ile 1280px ve 390px mesaj/davet ekranlari,
  sohbet acinca zilin korunmasi ve gercek CSRF'li aktarim POST'u dogrulandi.
  Mobil yatay tasma yok. makemigrations --check ve git diff --check temiz.
- Dal: codex/oturum-guvenligi-guncel. Main/push/canli yayin YOK.
  Bu not onceki oturum ve hiz siniri paketlerinin yayin engellerini kaldirmaz:
  Cloudflare/IP teyidi halen bekleniyor. Canli DB/hesaplar degistirilmedi.

## Kenarda Dursun Ilk Tiklama: 2026-10-12

- single_answer ve edit_answer sablonlarinda textarea blur olunca baslangic
  yuksekligine donuyordu. Bu, fare dugmeye basarken form eylemlerini kaydirip
  ilk tiklamanin kaybolmasina neden olabiliyordu.
- Blur'da kucultme kaldirildi. Ilk focus'ta buyume bir kez uygulanir; zaten
  buyuk alan kucultulmez, sonraki focus elle ayarlanan boyutu bozmaz.
  Taslak endpoint'i ve yayinlama davranisi degistirilmedi.
- Gercek tarayicida her iki ekranda uzun metin ve tek Kenarda Dursun
  tiklamasi: basari bildirimi, kayitli taslak ve 324px -> 324px alan boyutu
  dogrulandi. Mevcut yayinlanmis entry degismedi (yalniz sentetik test DB).
- 6 yeni regresyon testi dahil 27 Node testi ve 7 odakli Django taslak/eylem
  testi gecti. git diff --check temiz. Main/push/canli yayin yok.

## Topluluk Yayin Paketi: 2026-10-12

- Kullanici main'e birlestirme ve push onayi verdi. Yayin dali:
  codex/topluluk-yayin. Oturum guvenligi, mesajlasma, bildirim, davet hakki
  aktarimi ve Kenarda Dursun ilk tiklama duzeltmesi bu pakette.
- Dogrulanmamis proxy ayariyla girisleri engellememek icin giris hiz siniri
  runtime/model/test/0065 migration bu yayindan cikarildi. Tam calisma
  codex/oturum-guvenligi-guncel dalinda 149757b commit'inde korunuyor.
  SEC-07 halen acik; sonraki entegrasyonda migration 0066 sonrasina alinmali.
- 0066_invitation_transfer dogrudan 0064_entry_reference_notifications'a
  bagli. Numara atlamasi kasitli; deploy sirasinda migrate gerekli.
- Son yayin agaci: 774 Django testi, 765 basarili, 9 SQLite kilitleme
  atlamasi; 27 Node testi basarili. makemigrations --check --dry-run ve
  git diff --check temiz. Onceki MySQL 67 test sonucu yukarida kayitli;
  hiz siniri ayrildiktan sonra MySQL suite yeniden calistirilmadi.
- Canli yayin kullanicinin pull, migrate, collectstatic, check ve Web Reload
  adimlarini yapmasini gerektirir. Genel site incelemesi tamamlanmis degildir.

## Mesaj Baglantilari: 2026-10-13

- codex/mesaj-baglantilari dalinda gelen/gonderilen mesajlarin HTTP(S)
  baglantilari yeni sekmede acilir. Sohbet ve diger navigasyon degismedi.
- Plain-text mesaj once escape edilir; mevcut Bleach kutuphanesiyle link
  uretilir. target=_blank ve rel=nofollow noopener noreferrer uygulanir.
  Kullanici HTML'i calistirilmaz; e-posta baglantilari korunur.
- 5 yeni link regresyon testi ve 13 bildirim testi gecti; diff kontrolu temiz.
  Migration veya yeni paket yok. Henuz main/push/canli yayin yapilmadi.

## Murekkep Temasi ve Mesaj Baglantilari Yayin Paketi: 2026-10-13

- Kullanici iki degisikligin main'e alinip pushlanmasini istedi.
- Renk Ayarlari'na Murekkep (Siyah & Beyaz) eklendi: notr beyaz/gri
  yuzeyler, siyah navbar, koyu metin ve sistem Georgia fontu. Tum mevcut
  temalar korundu; varsayilanlar veya baska kullanicilarin ayarlari degismez.
- Tum preset alanlari, profil kaydi/reset, kisisellik ve normal/hover
  renk eslesmelerinde en az 4.5:1 kontrast regresyon testleri eklendi.
- Mobil kontrolde koyu navbar'da kaybolan Bootstrap menu simgesi goruldu;
  mevcut Bootstrap Icons simgesi ve header-text-color ile duzeltildi.
  Gercek tarayicida tema secme/kaydetme, masaustu ve 390px mobil gorunum,
  menusunun acilmasi ve yatay tasma olmamasi dogrulandi. Sentetik DB kullanildi.
- Mesaj linkleri ve tema birlikte yayinlanir. Yeni migration/paket yok.
  PythonAnywhere: pull, collectstatic, check ve Web Reload gerekli.
- Son yayin agacinda 783 Django testi: 774 basarili, 9 SQLite kilitleme
  atlamasi (21.137s). 27 Node testi gecti. makemigrations --check --dry-run
  ve git diff --check temiz.

## Davet Iptali ve Kelime Analizi: 2026-10-13

- Dal: codex/davet-iptal-kelime-analizi. Kullanici main'e birlestirme ve
  push icin onay verdi. Canli yayin PythonAnywhere adimlariyla yapilacak.
- Kullanilmamis davetlerde iptal onayi eklendi. Kayit silinmez;
  0067_invitation_cancelled_at iptal zamanini saklar. Signup iptal edilen
  kodlari reddeder. Yalniz daveti olusturan kullanici POST+CSRF ile iptal
  edebilir; ayirdigi kota bir kez geri verilir. Kullanilmis davetler,
  tutarsiz used_by kayitlari ve kota tasmasi reddedilir.
- Signup ile ayni Invitation satir kilidi kullanilir. Paralel iki iptal,
  iptal/kayit yarisi ve iptal/hak aktarimi test edildi. Basarisiz iptal
  kaydinda kota iadesi de transaction ile geri alinir.
- Buyuk aktarim baglantisi kaldirildi. Kullanilan davetin alici adinin
  yaninda title='Ek davet' ve erisilebilir etiketli + simgesi var;
  aktarim formu alici adiyla acilir. Mevcut kisisel aktarim gecmisi korunur.
  Kullanilmamis kodun durum alaninda iptal simgesi; iptal edilen kodda
  tekrar iptal/kopyala kontrolu yok. Tablo sutunlari daraltildi.
- Istatistik bulgusu: entry tumden elenmiyordu; haric tutulan kelimenin
  aramasi hem site hem profil ekraninda 0 donuyordu. Sik kelime listesi
  filtresi ve tam veri uzerindeki arama sayaci ayrildi. Diger kelimeler,
  entry/kelime/karakter toplamlari ve ortalamalar haric tutmadan etkilenmez.
  Turkce I/i ve I-noktali normalizasyonu ortaklastirildi; bosluklu filtreler
  duzeltildi. Profilde cikarma/geri alma sirasinda arama korunur.
- Test: 800 Django testi, 788 basarili, 12 SQLite kilitleme atlamasi
  (21.808s). Izole MySQL 8.0.46/PyMySQL'de 42 davet/kelime testi, atlamasiz
  basarili (2.696s). Bilinen Question.slug mysql.W003 uyarisi devam ediyor.
  Migration model uyumu ve diff kontrolu temiz.
- Tarayici: sentetik DB'de ek davet formu/gercek POST ve onayli iptal/
  hak iadesi dogrulandi. 390px mobil form ve sayfada yatay tasma yok;
  davet tablosu kendi yatay kaydirma alaninda kalir. Canli veriler degismedi.
- Yayinlandiginda migrate gerekli. Bekleyen SEC-07 hiz siniri migration'i
  artik 0067 sonrasina (0068 veya siradaki uygun numara) alinmali.
- PythonAnywhere: git pull --ff-only origin main, dogru virtualenv ile
  manage.py migrate, collectstatic --noinput, check ve Web Reload.
  Yeni paket kurulumu gerekmiyor.

## Davet Listesi ve Toplam Hak: 2026-10-13

- Dal: codex/iptal-davetleri-gizle. Kullanici main'e birlestirme ve push
  onayi verdi. Canli yayin ayrica PythonAnywhere adimlarini gerektirir.
- Iptal edilmis davetler profil listesinden ve sayaclarindan cikarilir;
  denetim kaydi, kullanilamaz kod ve tek seferlik hak iadesi korunur.
- Verilen toplam sutunu ilk davet kotasina ayni gonderenin ayni aliciya
  yaptigi ek aktarimlari ekler. Ilk kota degistirilmez; iade/kayit mantigi
  etkilenmez. Onceki aktarimlar da mevcut islem kayitlarindan hesaplanir.
- Toplam, alicinin kalan bakiyesi degildir. Baska gonderenlerden gelen,
  baska alicilara giden veya ters yondeki aktarimlar dahil edilmez.
  Kullanici adi degisimi hesabi bozmaz. Tekrar POST ve basarisiz aktarim
  toplami artirmaz. Bekleyen davetlere ek aktarim eklenmez.
- Aktarimlar tek toplu sorguyla hesaplanir; davet basina sorgu yok.
- Kontrol: 804 Django testi, 792 basarili; SQLite nedeniyle 12 kilitleme
  testi atlandi (21.178s). Migration model uyumu ve diff kontrolu temiz.
- Yeni migration veya paket yok. Canli yayin icin pull, collectstatic,
  check ve Web Reload yeterli (0067 onceki surumde uygulanmis olmali).

## Yayin ve Bekleyen Is Envanteri: 2026-10-13

- Davet listesi/toplam hak duzeltmesi `719eac7` ile main'e pushlandi;
  uzak ref dogrulandi. Canli PythonAnywhere deploy'u bu turda yapilmadi.
- Iki ayri Git deposunun dallari, dort mevcut calisma alani ve tarihsel rapor
  karsilastirildi. Ayrintili guncel envanter: `pending_work_2026-10-13.md`.
- Eski arama yamasi esdeger; eski oturum yamasi uyarlanarak zaten main'de.
  Giris siniri ise bilerek geri alinmis durumda. Git ancestor/merge bilgisi
  tek basina ozelligin etkin oldugunu kanitlamiyor.
- Diyagram/harita/guvenlik alanlarindaki commit edilmemis calismalara
  dokunulmadi. Mantik ek incelemesi ve iki deneysel insanlar/degerlendirme
  dali korunuyor. Toplu merge, branch silme veya worktree prune yapilmadi.

## Profil, Mesaj ve Taslak Tespiti: 2026-10-18

- Taban: guncel origin/main `90a22fe`; yeni dal `codex/profil-mesaj-kontrolleri`.
  Main calisma alani temizdi. Eski diyagram, harita ve genel guvenlik
  alanlarindaki commit edilmemis degisiklikler korunuyor.
- Kullanici alt baslik taslaginda once tespit istedi; uretim koduna
  dokunulmadi. Izole Django test DB'sinde X ustune Y alt baslik taslagi:
  title=Y, question=X olarak kaydoluyor, yayinlanmis Answer olusmuyor.
  Taslak karti title yerine question.question_text kullandigi icin X
  gosteriyor. Yeniden duzenleme formu Y basligini/metnini dogru yukluyor.
- Daha ciddi ek bulgu: ayni X altina Z taslagi kaydi, mevcut Y taslaginin
  uzerine yaziyor. kenarda_save parent+source ile eslestiriyor; ayri alt
  baslik taslak kimligi yok. Yeniden uretim betigi gecici test alaninda;
  bu bozuk davranisi kalici basarili regresyon testi olarak sabitlemedik.
  Sonraki duzeltme: taslak kimligi, alt baslik gosterimi, ayni ustte birden
  fazla taslak ve yayinlama/dogrudan gonderme sinirlarini birlikte ele al.
- Rapor akisi incelendi: yalniz question/answer hedefleri; ContentReport
  kaydi Django admin'de ContentReportAdmin ile listeleniyor. Reason/details
  saklanir, status=open. Ayni raporlayan ayni icerigi yeniden raporlarsa
  kayit guncellenir/yeniden acilir, onceki inceleme alanlari temizlenir.
  Admin listesi filtre/arama ve manuel durum/karar alanlari sunuyor;
  otomatik yonetici bildirimi/e-posta, otomatik silme/yasaklama veya karar
  bildirimi yok. Bu tur raporlama davranisi degistirilmedi.
- Profil girdilerinin altina Sayfa N / Toplam eklendi. Tek sayfada 1/1,
  bos listede sayac yok; mevcut sayfa secicisi, onceki/sonraki ve sekme
  davranisi korundu. Seciciye erisilebilir etiket eklendi.
- Yalniz bire bir mesaj formunda Enter=requestSubmit, Shift+Enter=satir.
  IME/composition, degistirici tuslar, event.repeat, bos/bosluk mesaji ve
  bekleyen formun tekrar gonderimi kontrol ediliyor. Geri/ileri onbelleginde
  form yeniden etkinlesiyor. POST/CSRF ve mevcut backend degismedi.
- Eski gecici venv OS tarafindan kismen temizlenmisti. Mevcut requirements
  ile /private/tmp/hafif-validation-20261018 yeniden kuruldu; repo paket
  surumleri veya canli ortam degistirilmedi.
- Test: 808 Django testi, 796 basarili, 12 SQLite kilitleme atlamasi
  (23.254s); 33 Node testi gecti. Ayrica taslak teshisi+profil/mesaj/icerik
  guvenligi kosusu 30 test: 28 basarili, 2 kilitleme atlamasi.
  makemigrations --check --dry-run ve git diff --check temiz.
- Gercek Chrome/Playwright: 1280x900 profil 2/3 -> 3/3, 390x844 profil
  ve mesaj formu kontrol edildi. Shift+Enter yeni satir, Enter bir CSRF'li
  POST, bosluk mesaji reddi; JS hatasi ve mobil yatay tasma yok.
  Tamamen sentetik DB; mevcut 8000 sunucusuna dokunulmadi. Onizleme 8031.
- Yeni migration/paket yok. Main'e birlestirme, commit veya push yapilmadi.

## Alt Baslik Taslak Duzeltmesi: 2026-10-18

- Kullanici tespiti onaylayarak duzeltme ve main'e push istedi. Yukaridaki
  profil sayfalama ve mesaj klavye kontrolleri de bu surume dahil.
- Alt baslik taslaklari artik acik draft_id ile guncelleniyor. Yeni form
  ayni ust baslikta, hatta ayni baslik metninde ayri kayit acar. Yeniden
  adlandirma mevcut taslagi gunceller; kardes taslagi ezmez. Kimlik hem
  hidden input hem URL'de korunur; yenileme taslagi geri yukler. Bekleyen
  kayit sirasinda kaydet/yayinla butonlari ikinci istegi engeller.
- Liste alt baslik adini ve ikincil olarak ust basligi gosterir.
  Yayinlama taslak sahibini, ust basligi ve kaynak turunu dogrular;
  transaction icinde alt baslik/iliski/entry olusturur ve yalniz ilgili
  taslagi siler. Hatada geri alinir. Silinmis taslakla tekrar yayinlama
  reddedilir. Dogrudan taslak gonder endpoint'i alt basligi ust basliga
  entry olarak gonderemez. Form dogrulama hatalari gorunur.
- Ust basliga normal entry yazmanin iki endpoint'i de alt baslik
  taslaklarini korur. Normal yanit editorleri alt baslik taslagini yuklemez.
- Gecmis kayitlarin title/content bilgileri korunur; daha once uzerine
  yazilarak kaybedilmis taslak metinleri bu yama ile geri gelmez.
  Ayni taslagi iki sekmede duzenleme icin surum/cakisma denetimi ve ilk
  kaydin yaniti kayboldugunda idempotent yeniden deneme bu kapsamda degil.
- Dogrulama: 819 Django testi, 807 basarili, SQLite kilit destegi nedeniyle
  12 atlama (21.072s); 33 Node testi basarili. Yeni 11 taslak testi; sahiplik,
  CSRF, kimlik/veri dogrulama, kardes kayit, yayinlama ve rollback kapsami.
  makemigrations --check --dry-run ve git diff --check temiz.
- Gercek Chrome/Playwright, sentetik DB: kaydet/yenile/yeniden adlandir,
  ikinci taslak, birini yayinla ve digerini koru senaryolari gecti.
  1280x900 ve 390x844 gorunumleri kontrol edildi; JS hatasi/yatay tasma yok.
- Raporlar Django admin Content reports listesindedir. Superuser veya
  gerekli model yetkisine sahip staff gorebilir. Otomatik zil/e-posta yok.
- Yeni migration/paket yok; yayin icin pull, collectstatic, check ve
  PythonAnywhere Web Reload yeterli. Diger worktree'ler degistirilmedi.

## Site Ici Rapor Yonetimi: 2026-10-19

- Taban `a30a34c`; dal `codex/rapor-yonetimi`. Kullanici raporlari ayri
  sayfada yonetmek ve admin/superuser hesaplarina zil bildirimi istedi.
- `/yonetim/raporlar/`: durum filtreleri, sayaclar ve 25 kayitlik sayfalama.
  `/yonetim/raporlar/<id>/`: raporlayan, gerekce/aciklama, icerik baglantisi,
  duz metin onizlemesi, durum ve yonetici inceleme notu. Masaustu/mobil
  Muteferrik > Araclar menusune Raporlar eklendi. Django admin korunuyor.
- Erisim politikasi: aktif is_staff VEYA is_superuser. Normal kullanici
  dogrudan URL/POST ile erisemez; CSRF zorunlu. noindex ve no-store basliklari.
  Icerik/aciklama HTML olarak calistirilmaz; silinmis icerik guvenle gosterilir.
- Ortak rapor kayit servisi iki mevcut raporlama endpoint'ini kapsar.
  Yeni/yeniden acilan rapor icin tum aktif yoneticilere birer okunmamis
  content_report bildirimi. Ayni acik raporun tekrari/guncellenmesi ek
  bildirim uretmez. Bildirim rapor detayina gider; ozel aciklama metnini
  tasimaz. Eski raporlar listede gorunur, gecmise toplu bildirim yok.
- Kayit ve bildirim ayni transaction'da; rapor uzerinde satir kilidi.
  Inceleme formu updated_at surum kontroluyle eski ekrandan yeni rapor veya
  diger yonetici kararinin ezilmesini 409 ile engeller. Inceleyen ve zaman
  kaydedilir; yalniz inceleyen yoneticinin ilgili bildirimleri okunur olur.
- Durum kaydi icerigi otomatik silmez, hesabi yasaklamaz veya raporlayana
  mesaj gondermez. E-posta/push degil mevcut site ici zil sistemi kullanilir.
- Migration `0068_report_management_notifications`: nullable related_report
  FK (SET_NULL) ve bildirim turu. Paket degisikligi yok. Canlida pull ardindan
  migrate, collectstatic, check ve Web Reload gerekli.
- Test: 831 Django testi, 819 basarili, 12 SQLite kilit testi atlamasi
  (21.448s). 12 yeni rapor testi: yetki/CSRF, iki gonderim yolu, tekrar,
  yeniden acma, rollback, zil/baglanti, eski form cakismasi, silinmis hedef,
  escaping ve filtre/sayfalama. Migration uyumu ve diff kontrolu temiz.
- Sentetik DB'de 0068 uygulandi. Gercek Chrome 1280x900 ve 390x844:
  zil 1 -> inceleme -> 0, durum filtresi ve not kaydi dogrulandi; JS
  hatasi/yatay tasma yok. Yalniz bu sayfalarda sabit yardim/sohbet dugmeleri
  not alanini ortmemesi icin normal sayfa akisina alindi. Onizleme 8031;
  kullanicinin 8000 sunucusuna ve diger worktree'lere dokunulmadi.
