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
