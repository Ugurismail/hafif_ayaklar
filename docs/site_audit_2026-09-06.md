# Hafif Ayaklar: Site Geneli İnceleme ve İyileştirme Planı

İnceleme: 5-6 Eylül 2026. Rapor sürümü: 1.0. Uygulama düzeltmeleri: henüz başlamadı.

## 1. Yönetici Özeti

Site, kişisel notları ortak başlıklar, kaynaklar ve ilişkiler üzerinden birleştiren güçlü bir çekirdeğe sahip. Kitap oluşturma, düzeltme önerileri, diyagramlar ve mantık eğitimi bu çekirdeği tamamlıyor. Sorun özellik eksikliğinden çok, özelliklerin ortak güvenlik, veri doğruluğu, gezinme ve kalite kuralları altında yeterince birleşmemesi.

**Önerim: siteyi yeniden yazmak değil; önce güvenliği ve veri doğruluğunu sağlamlaştırmak, sonra ortak arayüzü sadeleştirmek ve özellikleri sırayla olgunlaştırmak.** Yeni dil, mikroservis veya tüm siteyi kapsayan frontend framework göçü bu incelemede gerekçelendirilmedi.

En önemli bulgular:

1. Git tarafından takip edilen `.env` içinde Django ve Agora anahtar alanları dolu; `DEBUG=True` var. Canlı anahtarlarla eşleşme ayrıca doğrulanmalı. Anahtar değerleri bu rapora alınmadı.
2. Bağımlılık dosyası ve kullanılan yerel ortam Django **4.2.2**. 4.2 serisinin güvenlik desteği sona ermiş durumda.
3. Cetvelde eski ekranın kaydedilmesi başka kullanıcının daha yeni değişikliğini kaybettirebiliyor.
4. Genel alışkanlık hedefi değişince önceki günlerin hedefi ve başarı yüzdesi de değişebiliyor.
5. Okunmamış bildirim filtresi, filtre çalışmadan önce bütün bildirimleri okundu yapıyor.
6. Giriş yapmamış bir ziyaretçi, geçerli CSRF tokenıyla radyo dinleyici sayısını değiştirebiliyor.
7. Eski çıkış testi URL'sinde eksik şablon ve eksik yönlendirme nedeniyle hata oluşuyor.
8. Mobil ana sayfada sol başlık listesi ilk ekranı kaplıyor; ilk entry ekranın altında kalıyor.

**581 test geçti; buna rağmen yukarıdaki davranış hataları ek senaryolarda ortaya çıktı.** Test sayısı, kullanıcı deneyiminin veya tüm güvenlik sınırlarının doğrulandığı anlamına gelmiyor.

## 2. Kapsam ve Kanıt Seviyesi

### Esas alınan sürüm

- Yerel `main` ve yerel `origin/main`: `43452d9` (`Expand habit tracking and reminders`). Bu incelemede uzaktan `fetch` yapılmadı; GitHub'ın o andaki son durumu ayrıca doğrulanmadı.
- Açık çalışma: `codex/diagram-editor-improvements`, taban `d19cb3e`, commit edilmemiş diyagram değişiklikleri var.
- Diğer çalışma dizini: `codex/map-improvements`, taban `43452d9`, commit edilmemiş harita değişiklikleri var.
- `codex/logic-lesson-review` üzerinde `main` dışında `adf61e0` ders inceleme commit'i bulunuyor.
- İnceleme için `main`den izole bir kopya ve yalnızca sentetik veriler içeren SQLite veritabanı oluşturuldu. Kullanıcının mevcut veritabanına ve üretim verilerine yazılmadı.
- Rapordaki dosya/satır referansları, aksi belirtilmedikçe **43452d9** sürümüne aittir. Açık diyagram branch'indeki satırlar farklı olabilir.

### İşaretler

- **D**: Yerel istek veya tarayıcı senaryosuyla yeniden üretildi.
- **K**: Koddan doğrulandı; üretimdeki etkisi veya bütün varyasyonları test edilmedi.
- **Ö**: İyileştirme önerisi / ürün kararı; mevcut hata olduğu iddiası değil.
- **A**: Ek doğrulama gerekiyor; kapanmış veya güvenli kabul edilmemeli.

Bu rapor bütün ana ürün alanlarını kapsayan bir teknik ve ürün denetimidir; tüm derslerin akademik doğrulaması, her temada tüm ekranların görsel testi, bağımsız sızma testi veya gerçek yük testi değildir. Bu eksikler aşağıda ayrı iş kalemleri olarak korunmuştur.

### Gerçekleştirilen kontroller

| Kontrol | Sonuç ve sınırı |
|---|---|
| Django test paketi | 581 test, 12.412 saniye, tümü başarılı; Python 3.11.9 / Django 4.2.2 / ayrı SQLite test DB |
| Temiz DB migration | 0062 dahil mevcut migration zinciri başarıyla uygulandı |
| Model/migration tutarlılığı | `makemigrations --check --dry-run`: değişiklik yok |
| Deployment kontrolü | Hosted ortam koşulu, açıkça kapalı DEBUG ve geçici güçlü anahtarla `check --deploy` başarılı; üretim ortamı doğrulaması değildir |
| Sayfa duman testi | 26 GET senaryosu: 25 başarılı yanıt, eski çıkış testi çözüm ekranında `TemplateDoesNotExist` |
| Ek davranış senaryoları | Bildirim, cetvel, alışkanlık geçmişi, radyo sayacı, IAT ve eski test POST yolu incelendi |
| Görsel kontrol | Yerel ana sayfa, harita, alışkanlık ekranı ve alışkanlık modalı; 1280x720 ve 390x844 örnekleri |
| Mobil somut ölçüm | Ana sayfada ilk entry üst kenarı 877.6 px; viewport yüksekliği 844 px. Sayfada yalnızca bir örnek başlık vardı |
| Modal kontrolü | Alışkanlık modalı animasyon sonrasında opak; mobil genişlik 374 px, yatay sayfa taşması yok. Kalıcı şeffaflık hatası bu örnekte tekrarlanmadı |

Bağımsız Python Playwright sürücüsü yerel dosya okuma/başlatma hatası verdi. Görsel inceleme uygulama içi tarayıcıyla sürdürüldü. Bu araç hatası sitenin hatası olarak sınıflandırılmadı. Safari/Firefox, tüm tema varyasyonları ve otomatik tam görsel regresyon çalıştırılmadı.

## 3. Önceliklendirme

- **P0:** Aktifse gizli anahtar/hesap güvenliği etkisi; diğer yayımlardan önce incele ve sınırla.
- **P1:** Veri kaybı, yetki sorunu, bozuk temel akış, destek dışı altyapı veya ciddi mobil erişim sorunu.
- **P2:** Performans, erişilebilirlik, tutarlılık ve özellik olgunlaştırma.
- **P3:** Kullanım verisi ve ürün kararına göre yapılacak ekler.

Durum sözlüğü: `Açık`, `İnceleniyor`, `Düzeltildi / test bekliyor`, `Doğrulandı`, `Ertelendi`. Aşağıdaki tüm işler başlangıçta **Açık**. Kod yazılması tek başına işi kapatmaz.

## 4. Önce Düzeltilmesi Gerekenler

### SEC-01 | P0 | K+A | Git'te ortam dosyası ve anahtarlar

**Kanıt:** `git ls-files .env` dosyayı döndürüyor. Değerleri göstermeyen incelemede `DJANGO_SECRET_KEY`, `AGORA_APP_ID`, `AGORA_APP_CERTIFICATE` alanları dolu; `DEBUG=True`. `hafifayaklar/settings.py:12` bilinen bir yedek SECRET_KEY tanımlıyor; `:18` ortam DEBUG değerini kabul ediyor.

**Etki:** Canlıda aynı anahtarlar kullanılıyorsa yetkisiz token üretimi ve imzalı verilerin güvenliği açısından risk. Yalnızca yerel/test değerleri ise etki daha sınırlı; eşleşme doğrulanmadan kesin canlı sızıntı iddiası kurulamaz.

**Yapılacak:** Yetkili operatörle üretim anahtarlarını karşılaştır; aktif olanları yenile; repo takibinden gerçek `.env`yi çıkar ve yalnızca örnek dosya bırak; geçmiş erişimini değerlendir; eksik production anahtarında uygulama açılmasın. Anahtar değişiminin oturumlara/yayına etkisini planla. Git geçmişini silmek tek başına çözüm değildir.

**Kabul:** Repo ve CI secret taraması temiz; production açıkça `DEBUG=False`; anahtarsız production startup başarısız; eski anahtarların iptali doğrulanmış. Raporu veya logları anahtarlarla doldurma.

### SEC-02 | P1 | K | Destek dışı Django

**Kanıt:** `requirements.txt:7`, yerel runtime: `4.2.2`. Django'nun resmi destek tablosunda 4.2 desteği 7 Nisan 2026'da bitiyor. [Resmi destek tablosu](https://www.djangoproject.com/download/#supported-versions).

**Yapılacak:** PythonAnywhere Python/MySQL sürümlerini doğrulayarak desteklenen bir hedefe kontrollü geçiş. Python 3.10 uyumluluğu gerekiyorsa 5.2 LTS makul adaydır; geçişteki güncel yama ve tüm bağımlılık uyumu ayrıca doğrulanmalı. Bağımlılık taramasını düzenli CI kontrolüne ekle.

**Kabul:** Temiz ortamdan kurulum, MySQL integration testleri, auth/CSRF/export/şablon testleri ve staging smoke başarılı. Toplu kör `pip upgrade` uygulanmamalı.

### DATA-01 | P1 | D | Cetvelde sessiz değişiklik kaybı

**Kanıt:** `core/views/attendance_views.py:283` tüm `sheets` ve `marks` nesnesini istemciden alıp değiştiriyor. `select_for_update` yazmaları sıralıyor ama eski istemci verisini tespit etmiyor. İki eski ekranı temsil eden ardışık kayıtta birinci kişinin işareti kayboldu, ikincininki kaldı.

**Yapılacak:** Hücre bazlı değişiklik API'si veya sürüm/ETag ile optimistic concurrency; çatışmada 409 ve yenile/birleştir akışı. Yapısal personel düzenlemesiyle günlük işaretleri ayrı kaydet. Değişiklik günlüğü ve geri alma ekle.

**Kabul:** A ve B farklı hücreleri değiştirirse ikisi de kalır. Aynı hücre değişikliği sessizce ezilmez. Eski günlük kayıt, yeni izin aralığını silemez. İki tarayıcı ve MySQL ile doğrula.

### DATA-02 | P1 | D | Alışkanlık geçmişi değişiyor

**Kanıt:** `core/views/habit_views.py:123`, `HabitEntry.effective_target`: kayıtta hedef yoksa bugünkü `habit.target` kullanılıyor. Dün 20/20 olan kayıt, genel hedef 40 yapılınca 20/40 oluyor. Gün programının değişmesi de geçmiş istatistiği etkileyebilir; bunun ayrı testi gerekli.

**Yapılacak:** Günlük hedef/program için tarihsel snapshot veya yürürlük tarihli plan. Genel düzenlemede “bundan sonrası” varsayılanı; geçmişi değiştirme açık ayrı işlem olsun. Mevcut null hedeflerin gerçek geçmiş değerleri geri kazanılamıyorsa bunu dürüstçe belirt.

**Kabul:** Genel hedefi/programı değiştirmek dünkü hedefi, tamamlanma oranını ve seriyi değiştirmiyor; kullanıcı açıkça geçmiş düzeltmesi yapabiliyor.

### DATA-03 | P1 | D | Okunmamış bildirim filtresi boşalıyor

**Kanıt:** `core/views/notification_views.py:16`: liste GET'i önce tüm okunmamış bildirimleri okundu yapıyor, sonra `status=unread` filtresi uyguluyor. Sentetik okunmamış bildirim filtre ekranı açıldığında okundu oldu.

**Yapılacak:** Listeyi açmak tüm sayfaları okundu yapmasın; tek bildirime ve açık “tümünü okundu” eylemine dayalı durum güncellemesi. Mesaj detayı `core/views/message_views.py:96` aynı göndericinin mesaj dışı bildirimlerini de kapatabiliyor; tür/nesne kapsamını daralt.

**Kabul:** Okunmamış filtresi gerçek okunmamışları gösterir; başka sayfadaki bildirimler korunur; bir sohbeti açmak düzeltme/oy bildirimlerini kapatmaz; navbar sayacı tutarlı güncellenir.

### SEC-03 | P1 | D | Radyo sayacı istemciye güveniyor

**Kanıt:** `core/views/radio_views.py:429`, oturum şartı yok. Giriş yapmamış test istemcisi normal CSRF kontrolünü geçerli tokenla geçerek `987654` değerini kaydetti. CSRF, kimlik veya yetki kontrolünün yerine geçmiyor.

**Yapılacak:** Sayıyı güvenilir oturum/presence veya sağlayıcı verisinden türet. İstemci isteği tüm sayacı belirlemesin. Tip, sınır, yayın durumu, kimlik ve hız kontrolü koy.

**Kabul:** Misafir/yetkisiz kullanıcı sayacı yazamaz; negatif, metin, aşırı değer ve tekrar eden tablar veriyi bozmaz; kopan dinleyici TTL sonrası çıkar.

### FLOW-01 | P1 | D | Eski çıkış testi yolu çalışmıyor

**Kanıt:** `core/urls.py:237`, `core/views/cikis_test_views.py:190`. `/cikis-test/<id>/coz/` GET'i eksik `core/cikis_test_coz.html` nedeniyle hata; POST'u bulunmayan `cikis_test_sonuc` adına yönleniyor. Alternatif `/cikis_testleri/<id>/coz/` akışı mevcut.

**Yapılacak:** Tek çözüm akışı seç; eski URL'yi doğru yere yönlendir; bağlı linkleri temizle. Eski URL'yi sadece silerek kullanıcı bağlantılarını bozma.

**Kabul:** Eski/yeni link, boş test, hatalı seçenek, sonuç kaydı ve tekrar çözme akışı 500 vermiyor; katılımcı sonuç görünürlüğü açık ürün kuralına bağlı.

### API-01 | P1 | D+K | JSON ve form doğrulaması parçalı

**Kanıt:** `iat_result` ve `attendance_save_state` içine JSON liste gönderilmesi `AttributeError` oluşturdu. IAT'ye `{}` gönderilmesi 200 ve sonuç üretimiyle karşılandı. `core/views/logic_views.py:460`, `kenarda_views.py:50` gibi yollar da gövdenin nesne olmasını varsayıyor.

**Yapılacak:** Paylaşılan küçük JSON nesne doğrulayıcısı, endpoint bazlı alan/tip/sınır doğrulaması; bozuk UTF-8, null/liste/sayı, geçersiz tarih/ID ve çok büyük içerik için 4xx. API oturumu bittiğinde HTML login yerine tanımlı hata akışı.

**Kabul:** Bozuk girdiler 400/401/403/404/413/422 gibi belirlenmiş yanıt verir, veri yazılmaz ve 500 oluşmaz. Başarısız kayıtta UI veriyi korur, yeniden deneme güvenlidir.

### UX-01 | P1 | D | Mobil ana sayfa önce boş listeyi gösteriyor

**Kanıt:** `core/templates/core/user_homepage.html:12` ve `static/css/styles.css:2404`. 390x844 görünümde tek başlıklı listenin ardından ilk entry `y=877.6` noktasında başlıyor. İlk ekranda geniş boşluk, entry yok. Ana sayfada `main` landmark ve `h1` da gözlenmedi.

**Yapılacak:** Mobilde entry akışını öne al; başlık listesi açılır panel veya ayrı sekme olsun. Masaüstünün viewport yüksekliğini mobilde üst üste yığılmış kolonlara taşıma. Ana içerik landmark'ı ve tutarlı başlık hiyerarşisi ekle.

**Kabul:** 360/390/768 px, tek ve çok başlıklı veride ilk içerik erişilebilir; iç içe kaydırma tuzağı yok; sekmeden dönüş konumu korunur; klavyeyle akışa geçilebilir.

### SEC-04 | P1 | K | Dosya kütüphanesi yükleme politikası eksik

**Kanıt:** `core/forms.py:373` ve `core/models.py:831`: genel kütüphane dosyasında açık tür/boyut doğrulayıcısı yok. Editör görseli endpoint'i ayrı, daha sıkı kontroller kullanıyor. `FILE_UPLOAD_MAX_MEMORY_SIZE` yükleme üst sınırı değildir; bellekte mi diskte mi tutulacağını belirler.

**Yapılacak:** İzin verilen türler, gerçek içerik kontrolü, kişi/site kotası, boyut sınırı ve depolama temizliği; aktif içerikleri güvenilmeyen dosya olarak sunma. Üretimde media origin, Content-Disposition ve içerik türlerini doğrula. [Django dosya güvenliği](https://docs.djangoproject.com/en/5.2/topics/security/#user-uploaded-content).

**Kabul:** İzinli yükleyici dahi sınırsız/istenmeyen aktif içerik yükleyemez; özel dosya beklentisi varsa doğrudan URL anonim erişimi ayrıca engellenir. Mevcut dosya erişim politikası kullanıcıya açıkça anlatılır.

## 5. Diğer Teknik ve Ürün İşleri

Bu tablodaki her satır bağımsız takip edilecek. Kabul sütunu işin kapanma koşuludur.

| ID / Öncelik / Kanıt | Bulgu ve önerilen değişiklik | Kanıt / kabul ölçütü |
|---|---|---|
| SEC-05 / P1 / K | Raporlama `next` adresi izin kontrolü olmadan yönlendirmeye giriyor. Güvenli aynı-origin dönüş uygula. | `report_views.py:12`; dış host/protokol-relative adres reddedilir, meşru dönüş korunur. Açık yönlendirme için lokal regresyon ekle. |
| SEC-06 / P1 / K+A | Oy endpoint'i `ContentType.objects.get(model=...)` ile genel model çözüyor. Yalnız desteklenen içeriklere izin ver; sayaç güncellemelerini atomik tut. | `vote_save_views.py:21`; question/answer dışı model ID'leri reddedilir; eşzamanlı oy sayaçları gerçek oy kayıtlarıyla eşleşir. |
| SEC-07 / P1 / K+A | Girişte uygulama düzeyinde hız sınırı görülmedi; davetiye kotası kontrolünde kilit olmadan okuma/yazma var. | `auth_views.py:89,123`; brute-force testine 429/backoff, paralel davetiye kullanımında kota aşımı yok. CDN koruması ayrıca doğrulanmalı. |
| SEC-08 / P2 / K | Logout GET ile durum değiştiriyor; girişte güvenli `next` dönüşü kullanılmıyor. | `auth_views.py:111`; logout POST+CSRF, giriş sonrası izinli hedefe geri dönüş; dış hedef yok. |
| SEC-09 / P1 / K+A | XLSX'ye kullanıcı metni doğrudan hücre değeri yazılıyor; `=` ile başlayan metin formül olabilir. | `export_views.py:221`; başlık, entry, kaynak alanlarında literal metin tipiyle yazım; Excel/LibreOffice formül enjeksiyonu regresyonu. Bu turda dosya üzerinde istismar denenmedi. |
| DATA-04 / P2 / K+A | Draft ve bazı sayaç akışlarında eski isteklerin yeni veriyi ezme riski. | `kenarda_views.py:108`; iki tab, geciken ağ yanıtı, çift tıklama ve offline dönüş testleri. Taslak sürümü/çakışma bildirimi; metin kaybı yok. |
| AUTH-01 / P2 / K+Ö | Şifre değiştirme var; route envanterinde şifremi unuttum ve hesap/veri yönetimi akışı yok. | `core/urls.py`; güvenli şifre sıfırlama, token süresi, kullanıcı varlığını ifşa etmeyen yanıt; silme/ihracat için ürün politikası. |
| PRIV-01 / P1 / K+A | Personel isimleri kaynak kodda varsayılan veri; cetvel erişimi radyo DJ rolüne bağlı. | `attendance_views.py:24,95`; özel cetvel yetkisi ve veri kurulumu; gerçek personel repo dışında. DJ rolü tek başına personel erişimi vermemeli. |
| PRIV-02 / P2 / K+A | Alışkanlık/para özel kapsamlı; veri saklama, hesap silme ve takip politikası görünür bir bütün oluşturmuyor. | `habit_views.py`, `money_views.py`, `context_processors.py`; veri envanteri, yetki matrisi, saklama/silme planı; GA ve ziyaret kaydının kullanıcı beklentisiyle uyumu. Hukuki uygunluk ayrıca uzman değerlendirmesi ister. |
| PERF-01 / P2 / K+D | Diyagram editörü/CSS, MathJax ve ortak modallar her sayfaya yükleniyor. | `base.html:58,179`, `_base_shared_scripts.html:20`; diyagramsız sayfa editörü indirmez, matematik yoksa MathJax ertelenir. Editör JS 219450 byte, CSS 53325 byte, sıkıştırılmamış. |
| PERF-02 / P2 / K | Mesaj listesinde sayfalama öncesi her konuşma için count/first sorgusu çalışıyor. | `message_views.py:29`; 10 ve 1000 konuşmada sorgu sayısı konuşmayla doğrusal büyümez; sıralama ve okunmamış sayısı aynı kalır. |
| PERF-03 / P2 / K+A | Harita, kaynak kullanım araması ve export için büyüyen veriye göre sınırlar/ölçümler gerekli. | `question_map_views.py`, `definition_reference_views.py:485`, `export_views.py`; kademeli veri, seçili alan yükleme ve export sınırı; ölçmeden cache/kütüphane değişikliği yok. |
| PERF-04 / P2 / K+A | Alışkanlık güncellemesi dashboard hesaplamasını tekrar yapıyor; 365 günlük kayıtlar taranıyor. | `habit_views.py:101,382`; 100 alışkanlık/1 yıllık kayıtta ölçüm, gerekirse artımlı güncelleme; tarihsel doğruluk korunur. |
| OPS-01 / P1 / K+A | Repo içinde CI workflow, bütünlüklü kurulum/yayın/rollback runbook'u görülmedi. | `.github` envanteri, requirements; temiz kurulum, MySQL job'u, smoke, migration ve statik kontrolü otomatik olmalı. Dışarıda CI varsa bağlantısı rapora eklenmeli. |
| OPS-02 / P1 / A | Yedek dosyası bulunması geri yüklemenin çalıştığını kanıtlamaz. | Üretim DB+media birlikte restore tatbikatı; RPO/RTO hedefleri, erişim ve şifreleme, geri dönüş sorumlusu kayıtlı. Bu turda üretim yedeği açılmadı. |
| OPS-03 / P2 / K+A | Server-Timing iyi başlangıç; istek korelasyonu, 5xx alarmı ve prod performans dağılımı eksik doğrulama alanları. | `middleware.py:16`; request ID, endpoint bazlı p50/p95/p99, DB süresi, worker/edge ayrımı. Önceki PythonAnywhere kesintileri bütün gecikmelerin kanıtı sayılmamalı. |
| UI-01 / P2 / D+Ö | “Müteferrik” altında birbirinden uzak birçok iş var; seçenek bulunabilirliği zayıf. | `_base_navbar.html:44`; Oku/Keşfet, Yaz/Arşivle, Öğren, Kişisel Araçlar gruplarıyla kullanıcı testi. Düzeltmeler ve kitaplar kolay bulunmalı. |
| UI-02 / P2 / K+Ö | Tema değişkenleri, inline CSS, Bootstrap, Font Awesome ve ikon fontları birlikte yönetiliyor. | `base.html`, `styles.css`; modal/yüzey/form/focus/z-index için ortak token ve bileşen kuralları; bütün temalarda görsel regresyon. |
| UI-03 / P2 / K | ITC Galliard adı gerçek fontun her cihazda kullanıldığını garantilemiyor; local fallback listesi var. | `styles.css:1`; lisanslı webfont veya dürüst font adı/fallback; Windows/macOS/mobil gerçek font kontrolü. |
| A11Y-01 / P2 / D+K+A | Ana sayfa landmark eksik; ikonların bir kısmı karakter olarak okunuyor; kontrast, focus ve grafik alternatifleri sistematik değil. | Navbar/ana sayfa AX incelemesi; WCAG 2.2 AA hedefi, klavye, ekran okuyucu, 200% zoom, renk dışı anlam ve tablo özeti. |
| SEO-01 / P2 / K+A | Base canonical URL query string'i devralıyor; tüm sayfalar için default index/follow. | `base.html:16,45`; sayfa bazlı canonical/index politikası, private/arama/filtre URL'leri, doğrulanmış sitemap; Search Console örnek URL karşılaştırması. |
| SEO-02 / P2 / K+Ö | Sitemap mantık ve sorulara odaklı; Almanca/etik gibi public içerikler değerlendirilmemiş. Özel AI meta etiketleri başarı göstergesi değil. | `sitemaps.py`, `base.html:49`; gerçek crawl/index verisi; yalnız canonical/public/değerli sayfaları listele. Standart dışı etiketleri sadeleştir. |
| MAP-01 / P1 / K | Main haritasının ilk HTML verisi eski M2M, veri API'si kullanıcı ilişkisi kullanıyor; metin/hash tabanlı kimlik var. | `question_map_views.py:15,103`; tek veri kaynağı, kalıcı ID; aynı başlıklı ayrı nesneler yanlış birleşmez. Bekleyen branch aday çözüm, henüz doğrulanmış main özelliği değil. |
| MAP-02 / P2 / K+Ö | Çok kullanıcılı başlangıç/bağlantı tek gri düğümle yeterince anlatılmıyor. | `question_map_views.py`, ayrı map branch'i; kullanıcı efsanesi, seçilen kişinin yolu, ortak kenarda katkıcı listesi ve renk dışı ayırt etme. Yüzlerce ayrı rengi çözüm sayma. |
| MAP-03 / P2 / D+Ö | Main mobil haritada filtre paneli ilk ekranı kaplıyor. | 390x844 görsel örnek; harita önce görünür, filtre dar panel; zoom/fit, arama odağı, geri dönüş ve boş durum korunur. |
| DIAG-01 / P2 / K+A | Görüntüleyici, editör ve Python SVG renderer paralel davranış taşıyor; export eşitliği riski var. | `diagram_markup.py`, `diagram_editor.js`; tek veri sözleşmesi ve ortak fixture'lar; kaydet/yükle/entry/SVG/PNG/PDF karşılaştırması. |
| DIAG-02 / P2 / Ö+A | Ok açıklaması, bağlantı göstergesi ve basılı açıklama düzeni ayrı kabul senaryosu olmalı. | Önceki kullanıcı talepleri ve bekleyen branch; okun üzerinde işaret, klavye/touch erişimi, basılı çıktıda numaralı açıklama listesi. Hover'a bağımlı bilgi yok. |
| EXPORT-01 / P1 / K | PDF yolu entry metnini escape edip satır sonlarını dönüştürüyor; Paper Word render hattıyla aynı değil. | `export_views.py:566`, `paper_export.py`; aynı başlık/dipnot/kaynak/diyagram anlamını koruyan ortak içerik modeli. PDF'de ham editör işaretleri kalmamalı. |
| EXPORT-02 / P2 / Ö+A | Büyük kitapta durum, iptal, eksik kaynak/görsel bildirimi ve sayfa önizleme geliştirilmeli. | Export/book akışları; küçük örnekte senkron, eşik üstünde kuyruk/iş durumu ancak kapasiteye göre. Dosya bütünlüğü ve tekrar indirilebilirlik ölçülmeli. |
| LEARN-01 / P2 / K | Mantık ilerleme endpoint'i istemcinin verdiği puanı kabul ediyor. | `logic_views.py:474`; kişisel öz-değerlendirme ise açık adlandır; yeterlik/sertifika iddiası varsa cevapları server'da doğrula ve müfredat sürümünü bağla. |
| LEARN-02 / P1 / D+K+A | IAT boş veriden yorum üretiyor; puanlama ve sıralama kişilik/önyargı sonucu gibi algılanabilir. | `iat_views.py:68`; yeterli/geçerli deneme olmadan sonuç yok; bilimsel yöntem ve sınırlılık denetimi; sıralama yerine kişisel, ihtiyatlı öğrenme deneyimi. |
| LEARN-03 / P2 / Ö+A | Mantıkta çok test var fakat akademik editör ve gerçek öğrenci incelemesi tamamlanmış sayılmaz. | `logic_curriculum.py`, phase dokümanları; ders bazında kaynak, hedef, çözüm, yaygın yanlış, alternatif cevap ve okuma köprüsü kontrol listesi. |
| LEARN-04 / P2 / K+Ö | Almanca testleri istemci tarafında; kalıcı öğrenme ilerlemesi mantıkla ortak değil. | `german_views.py`, `german_course.js`; ses/telaffuz/üretim alıştırmaları ve kayıtlı ilerleme ihtiyacını öğrenme hedeflerine göre planla. |
| HABIT-01 / P2 / K+Ö | Planlı olmayan günler grafiklerde sıfır gibi temsil ediliyor; tam sayı/üst hedef sınırı her alışkanlığa uymuyor. | `habit_views.py:139,318`; plansız/eksik veri/gerçek sıfır ayrı, yüzde yanında birim, esnek günlük/haftalık hedef; yeni hesap geçmişi başarısız gösterilmez. |
| HABIT-02 / P2 / K+Ö | Hatırlatma navbar heartbeat'inde üretiliyor, bağımsız zamanlayıcı/push değil. UI bunu açıklıyor; aynı gün tek teslim kaydı var. | `habit_reminders.py`, `navbar_views.py`; saat geçince ve ertesi gün ilk ziyaret senaryoları açık. Kaçırılmış hatırlatma ve zaman dilimi politikası belirlenmeli. |
| MONEY-01 / P2 / Ö+A | Kişisel gelir/gider çekirdeği var; hesap bakiyesi ve gelir-gider farkı aynı kavram değil. | `money_views.py`; para birimi, açılış bakiyesi, transfer/iade, yinelenen gider, kategori düzenleme, CSV export ürün kapsamı netleşsin; tahmini bakiyeyi gerçek banka bakiyesi diye sunma. |
| COMMUNITY-01 / P2 / K+Ö | Anket/kaynak/düzeltme özellikleri daha olgun; kapsamlı çapraz rol ve moderasyon akışları gerekiyor. | `poll_views.py`, `answer_revision_views.py`, `report_views.py`; kapalı/anonim anket, stale öneri, silinen kaynak, engellenen kullanıcı ve itiraz senaryoları. |

## 6. Özellik Özellik Hedef Deneyim

Bu bölüm yalnızca hataları değil, özelliğin nasıl daha iyi bir ürün olabileceğini tarif eder. Önce ilgili P0/P1 işleri tamamlanır.

| Alan | Korunacak değer | Eksik / fazla / geliştirme yönü |
|---|---|---|
| Ana sayfa ve okuma | Başlık/entry ilişkisi, yazar sesi, takip filtresi | Mobil içerik önceliği; okunmamış/yeni/izlenen ayrımı; uzun metinde okuma konumu. Aynı ekranda rastgele keşif ile günlük okuma yarışmasın. |
| Arama | Başlık, kullanıcı, kaynak, etiket yolları | Sonuç tiplerini belirgin ayır; Türkçe İ/ı, tam eşleşme, typo, boş sonuç ve filtre korunmasını test et. Tek ortak arama davranışı; her modül ayrı mini arama sistemi olmasın. |
| Başlık oluşturma ve bağlantılar | Kullanıcıya ait ilişki kurma | Aynı isimli başlık, kök taşıma, döngü, başlık birleştirme ve çok yazarlı silmede açık önizleme/etki özeti. Eski M2M ve yeni ilişki modeli tekleştirilmeli. |
| Entry editörü | Güçlü metin işaretleme, önizleme | Kademeli araç çubuğu; kaydedilme durumu, taslak kurtarma, uzun metin ve offline davranışı. Yeni kullanıcının işaret sözdizimini ezberlemesi gerekmemeli. |
| Kaynaklar ve tanımlar | Ortak kaynak tekrar kullanımı, bağlamdan kaynak açma | Künye/alıntı/sayfa/kişisel tanımı ayır; eksik/silinmiş kaynağı görünür yap; yinelenen kaynak birleştirme ve kullanım etkisi. Ortak kaynağı düzenlemenin tüm entry'lere etkisi bildirilmeli. |
| Düzeltme ve sürüm ağacı | Öneri inbox'ı, diff, geçmiş | Kullanıcıya önce “ne değişti / kimden / ne yapmalıyım”; karmaşık ağaç isteğe bağlı. Çakışma, geri alma ve öneri sonrası kaynak/diyagram bütünlüğü fixture'larla korunmalı. |
| Kitaplar ve dışa aktarım | Sıralı entry seçimi, Paper Word çıktısı | Kitap seçimi ile geçici seçim durumunu ayır; export önizleme, içindekiler, eksik içerik uyarıları. Word/PDF/JSON/SVG aynı metnin farklı yorumları olmamalı. |
| Kaydedilenler ve koleksiyonlar | Kişisel arşivleme | Kitap ve koleksiyon farkı belirgin olsun: koleksiyon okuma/etiketleme, kitap sıralı yayımlama. İki menüde aynı işi tekrar ettirme; toplu düzenleme ve silinmiş içerik durumu. |
| Kenardakiler | Yazıya dönmeden saklama | Tek taslak merkezi, ait olduğu başlık/entry, son kayıt zamanı, geri yükleme. Başlık taslağı/entry taslağı yanlış bağlama açılmamalı. |
| Harita | İnsanların düşünce yollarını birlikte görme | Ortak düğüm/ayrı kullanıcı yolları; sabit kimlik, odak/komşuluk, anlamlı renk efsanesi, kalabalıkta kademeli ayrıntı. Harita salt renkli ağ olmamalı. |
| Şema | Metin ağırlıklı, daha kolay taranabilir ilişki görünümü | Haritayla aynı veri doğruluğu; derin yol breadcrumbs, çoklu ebeveyn ve döngü etiketi; sanallaştırma ancak ölçülen ihtiyaçta. |
| Diyagram | Metnin içinde akış, şekil, küme ve çizim | Ok yönü/bağlantı aidiyeti, görünür açıklama, taşınabilir yazı, zoom/fit, klavye erişimi. İzleyici hafif; tam editör gerektiğinde yüklenmeli. |
| Profil ve tema | Kişisel kimlik ve okuma tercihleri | İçerik/profil/ayarlar/analitik ayrımı; font garantisi ve kontrast. Çok sayıda bağımsız renk yerine güvenli hazır tema + kontrollü özelleştirme. |
| Mesajlar ve sohbet | Bire bir iletişim ve ortak alan | Engelle/sustur/raporla, sayfalı geçmiş, gönderiliyor/başarısız ayrımı. Ortak poll mekanizması; kapalı sohbet gereksiz yük oluşturmamalı. |
| Bildirimler | Takip, mesaj, öneri ve hatırlatmayı bağlama | Okunmamışları koru; tür bazlı tercihler; aynı olayları grupla; bildirimin hedef nesnesi silindiğinde anlaşılır sonuç. |
| Anketler | Oluşturma, seçenekler, anonimlik | Oy gizliliği ve kapanış kuralları açık; oy sonrası seçenek değişikliklerinin etkisi denetlenebilir; küçük örneklemden aşırı yorum çıkarma. |
| Alışkanlıklar | Günlük miktar ve hedef, görev grafikleri | Geçmişi koruyan hedef; kaçırıldı/plansız/atlandı ayrımı; günlük ve haftalık ritim, seri baskısını azaltan esnek rapor. |
| Para | Kategorili kişisel gelir/gider | Miktar ve para birimi doğruluğu; filtre/arama/export; bütçe ve nakit akışı ayrımı; gizlilik ve silme. Banka entegrasyonu ilk iş olmamalı. |
| Cetvel | Ortak günlük işaretler ve izin aralıkları | Eşzamanlı güvenli kayıt, ayrı yetki, işlem geçmişi, baskı önizleme. Kişi kimliği metin/sıra değişimine bağlı olmamalı. |
| Mantık | Kaynaklı müfredat, türetim/semantik araçlar | Ders ders insan incelemesi, kademeli alıştırma, cevap gerekçesi, kalıcı ilerleme sürümü. Wittgenstein'a hazırlık bir ders sayısı değil, okuma ve yorumlama kazanımı olarak ölçülmeli. |
| Almanca | Seviye ve ders yapısı | Dinleme, konuşma ve serbest üretim; cevapların açıklanması; mantıkla ortak ilerleme UX'i. Sadece çoktan seçmeli doğruluk dili kullanabilmeyi kanıtlamaz. |
| Etik Atlası | Kavramsal keşif | Terim/iddia/kaynak ayrımı; entry ve haritaya geçiş; görüşlerin karşılaştırılması. İçerik doğruluğu bu turda akademik olarak satır satır incelenmedi. |
| IAT | Çağrışımları düşünmeye açan etkinlik | Eksik veriyi reddet; yöntemi uzmanla doğrula; kişisel tanı/kişilik ölçümü izlenimini ve gereksiz skor yarışını kaldır. |
| Çıkış testleri | Kullanıcı üretimi değerlendirme | Çift URL/yarım akışları birleştir; yazar/katılımcı rolü; sürümlenmiş sorular ve sonuç gizliliği. |
| Dosyalar | Ortak dosya bulma/yükleme | Tür ve kota; arama/paginasyon; özel/açık erişim beyanı; dosya silinince entry'deki bağlantı yönetimi. |
| Radyo | Topluluk yayını ve sohbet | Yetki/sayaç/token süresi, yeniden bağlanma, aynı hesabın iki sekmesi, PC müzik+mikrofon matrisi. 100/400/1000 dinleyici kapasitesi ölçülmeden veya sağlayıcı hesabı doğrulanmadan vaat edilmemeli. |
| İstatistikler | Kullanımı anlama | Ziyaretçi/oturum/kullanıcı kavramlarını açık tut; bot/arka plan poll ayrımı; ürün kararına yarayan anonim toplu metrikler. |
| Delphoi / rastgele cümle / Game of Life | Deneysel keşif ve topluluk karakteri | “Keşif/Laboratuvar” altında isteğe bağlı; ana iş akışını gölgelememeli. Kullanım düşük diye veri kaybettiren otomatik kaldırma yapılmamalı. |
| Moderasyon / davet / admin | Kontrollü topluluk | Ayrı yetkiler, inceleme kuyruğu, itiraz, kota tutarlılığı ve denetim izi. Admin URL'sini değiştirmek güvenlik yerine geçmez. |

### Main dışında kalan ürünler

Matematik, değerlendirme/insanlarım ve eski radyo çalışmalarını canlı özellik varsaymadım. Route envanteri, branch adıyla aynı şey değildir. Özellikle eski değerlendirme branch'inde main'den bağımsız modeller/migration'lar bulunuyor; güncel main'e bütün branch'i körlemesine taşıma yerine ortak atadan fark ve migration uyumluluğu ayrıca incelenmeli. Bu alanların ayrıntılı UI/işlev denetimi henüz yapılmadı.

## 7. Neler Fazla veya Gereksiz?

Silme kararı değil, sadeleştirme önerileri:

- Aynı işin iki URL/view/şablonla yarım yürütülmesi: eski çıkış testi yolu örneği.
- Her sayfada diyagram editörü, matematik motoru ve kullanılmayan modal yüklemek.
- Tek arayüzde farklı ikon kütüphaneleri, özel CSS düzeltmeleri ve çok sayıda z-index istisnası.
- Bütün seçenekleri “Müteferrik” altında biriktirmek; keşfedilmesini kullanıcıya bırakmak.
- Fontun gerçek kaynağını ayırmadan ticari font adını vaat etmek.
- Standart dışı AI meta etiketlerini SEO çalışmasının yerine koymak.
- Kişisel takipte kullanıcı amacını anlamadan her yere yüzde/seri eklemek.
- Bilimsel araçları skor/yarış mekanizmasına dönüştürmek.
- Ölçüm olmadan mikroservis, WebSocket, arama sunucusu veya tam frontend göçü başlatmak.

**Korunmalı:** Django'nun sunucu taraflı sayfaları, ORM ve oturum güvenliği; mevcut anonimlik/nesne sahipliği kontrolleri; düzeltme diff'i; kitap sıralaması; diyagramın normalize/escape kontrolleri; kaynaklı mantık omurgası; sentetik testler. Bunları toplu yeniden yazımın yan etkisi olarak kaybetmemeliyiz.

## 8. Mimari Yön

1. Django tabanlı modüler monolit devam etsin. Önce sürüm desteği ve modül sınırları düzelsin.
2. Modelleri hemen onlarca app'e bölmeyelim. Önce auth/permissions, JSON yanıtları, içerik render ve export gibi gerçek ortak davranışları tekleştirelim.
3. JavaScript modüllerini özellik bazlı yükleyelim. Build zinciri eklenirse ölçülebilir bundle/cache/test faydası olmalı.
4. Harita için bekleyen Cytoscape adayını ayrı değerlendirelim; dil/kütüphane değişmesi veri aidiyeti ve kalabalık ağ problemini kendiliğinden çözmez.
5. Diyagramda ortak şema ve fixture sözleşmesi; server ve client aynı girdiyi farklı anlamlandırmamalı.
6. Büyük export ve zamanlanmış işlerde kuyruk ancak gerçek ihtiyaçla; üretim worker sınırına uygun küçük görevler, zaman aşımı, iptal ve tekrar deneme.
7. SQLite hızlı testte kalabilir; kritik transaction/constraint davranışları üretimle aynı MySQL sürümünde test edilmeli.

## 9. Uygulama Fazları ve Çıkış Kapıları

| Faz | İçerik | Bağımlılık | Bitmiş sayılma koşulu |
|---|---|---|---|
| 0: Güvenli taban | SEC-01/02, OPS-01/02, branch/migration envanteri | Yok | Gizli anahtar ve DEBUG kontrolü, yedek geri yükleme, destekli hedef sürüm ve staging planı |
| 1: Veri ve yetki | DATA-01/02/03, SEC-03/04/05/06/07/09, API-01, FLOW-01, PRIV-01 | Faz 0 | Her hata önce başarısız regresyonla gösterilir; sonra test geçer; iki kullanıcı ve MySQL doğrulaması |
| 2: Ortak UX | UX-01, UI-01/02/03, A11Y-01, AUTH-01 | Faz 1'de kritik blokajların kapanması | Mobil ana akış, modal, klavye, tema ve hata davranışı kabul testi |
| 3: Bilgi üretimi | Arama, editör, kaynak, taslak, düzeltme, kitap/export | Faz 1-2 | Yaz -> kaynak ekle -> öneri -> kabul -> kitap -> Word/PDF uçtan uca senaryosu |
| 4: Harita ve diyagram | MAP-01/02/03, DIAG-01/02, şema | Faz 3 içerik sözleşmesi | Çok kullanıcılı ortak başlık, renk dışı aidiyet, büyük veri, mobil ve export eşitliği |
| 5: Kişisel/topluluk araçları | Habit/para/bildirim/radyo/anket/cetvel olgunlaştırma | Faz 1 doğruluk ve Faz 2 ortak UI | Tarihsel veri, kaçırılmış hatırlatma, gizlilik, ses kopması ve maliyet/kapsam testleri |
| 6: Eğitim ve yayın kalitesi | Mantık/Almanca/IAT/etik, SEO, performans ölçümleri | Temel altyapı ve ilgili feature testleri | Ders bazlı içerik onayı; teknik testten ayrı insan doğrulaması; prod ölçüm ve yayın kontrolü |

Fazlar toplu tek commit değildir. Her küçük değişiklik bağımsız branch/PR, geri dönüş planı ve test kanıtıyla ilerler. Düşük riskli bir P2 işi, kritik güvenlik işini bekletmemek şartıyla bağımsız yürüyebilir.

## 10. Test ve Yayın Sözleşmesi

Her değişiklik için:

- Referans issue ID, değişecek dosyalar, korunacak davranışlar ve migration ihtiyacı yazılır.
- Hata düzeltmesinde önce eski davranışı yakalayan test; ürün geliştirmesinde ölçülebilir kabul senaryosu.
- Roller: misafir, kullanıcı A, kullanıcı B, staff ve özellik yetkilisi.
- Durumlar: boş/normal/uzun veri, bozuk girdi, yetkisizlik, silinmiş nesne, eski açık ekran, çift gönderim ve ağ kesilmesi.
- Ekranlar: 360/390/768/1280/1440 px; en az açık/koyu/yüksek kontrast tema, uzun Türkçe etiket, %200 zoom.
- Kritik yayın akışlarında CSRF açık, DEBUG kapalı, secure cookie/proxy ayarları ve gerçek production DB motoruyla staging testi.
- İlgili testler + tüm paket + migration check + JS kontrolü; görsel değişiklikte screenshot/klavye testi.
- Release commit, migration, statik asset sürümü, yedek, reload ve yayın sonrası smoke kaydedilir.
- Sonra durum `Doğrulandı` yapılır; test sonucu veya commit olmadan “bitti/pushlandı” denmez.

### Temsilî uçtan uca senaryolar

1. Kullanıcı A entry yazar, B öneri yapar, A öneriyi inceler/kabul eder; kaynaklar ve diyagramlar doğru kalır.
2. Aynı başlığa iki kullanıcı farklı yollar bağlar; birinin bağlantısını kaldırması diğerininkini etkilemez.
3. Kitap seç, seçimi kaldır, yeni entry seç, sırala, Word/PDF indir; içerik ve kaynak numarası eşleşir.
4. Cetveli iki kullanıcı eşzamanlı açar; farklı ve aynı hücrelerde değişiklik yapar; kayıp veya sessiz üzerine yazma yok.
5. Dünkü alışkanlık hedefini tamamla, bugünkü planı değiştir; dünkü başarı korunur.
6. Okunmamış düzeltme/mesaj/hatırlatma varken filtrele ve sohbeti aç; ilgisiz bildirimler korunur.
7. Radyo yayını, token yenileme, kopma/geri dönme, PC ses paylaşımı, iki tab ve çok dinleyici; sağlayıcı/staging üzerinde ayrı doğrulama.
8. İleri mantık alıştırmasında yanlış/eksik/geçerli alternatif çözüm; açıklama ve ilerleme kaydı tutarlı.

## 11. Performans ve Başarı Ölçümü

Yerel sentetik örneklerde giriş yapılmış HTML yanıtları yaklaşık 99-219 KB aralığındaydı; JS/CSS buna dahil değil. Örnek başlık sayfası 23 sorgu, boş mesaj listesi 6 sorgu üretti. Bunlar küçük SQLite verisiyle tekil ölçümler; production hız/kullanıcı kapasitesi göstergesi değildir.

Başlangıç hedefleri ürün ve hosting kapasitesiyle kalibre edilmeli:

- Gerçek kullanıcı ölçümünde mobile p75 LCP <= 2.5 s, INP <= 200 ms, CLS <= 0.1 hedefi; henüz ölçülmedi.
- Önemli endpoint'lerde p95/p99, 5xx oranı, sorgu sayısı ve bekleme süresi; worker kuyruğu ile Django süresini ayır.
- Arama/harita için 100, 1000, 10000 düğüm ve paylaşılan yollar; render süresi, bellek ve etkileşim gecikmesi ölç.
- 10/100/500 entry kitaplarında export süresi, çıktı boyutu ve eksik görselleri ölç; eşik üstünde korumalı akış.
- Kullanıcı görevi başarısı: “öneriyi bul”, “kitabı indir”, “arkadaşının yolunu ayırt et” görevlerinde ilk denemede tamamlanma, hata ve geri dönüş sayısı.

Bu hedefler mevcut sonuç değil, kabul planıdır. Üretimde izinsiz yük testi yapılmadı.

## 12. Açık Doğrulamalar

- GitHub'daki güncel main ve üretimde gerçekten çalışan commit/env/virtualenv.
- Takipteki anahtarların gerçek/canlı olup olmadığı; repository görünürlüğü ve erişim geçmişi.
- Üretim MySQL sürümü, strict mode, indeks/lock davranışı; eski konsol uyarıları güncel durum kanıtı değildir.
- PythonAnywhere/edge dosya boyutu, media sunumu, cache ve rate-limit ayarları.
- Gerçek içerikle bütün tema/cihaz/uzun metin ekranları; bu rapor yalnız örnek görselleri doğruladı.
- Word/PDF'nin gerçek sayfa sayfa render doğrulaması ve bütün diyagram/citation kombinasyonları.
- Ders ders akademik doğruluk, kaynak lisansı, alıştırmaların insan öğrenmesine etkisi.
- Radyo hesabı, sağlayıcı paketi/fatura ve gerçek çok dinleyici testleri.
- Kullanıcı verisi dışa aktarımı/silme, moderasyon ve gizlilik politikaları için ürün sahibi kararları.

## 13. Sonraki Çalışmada Kullanım

İlk başlanacak iş **SEC-01** olmalı. Ardından SEC-02 ile altyapı geçişi planlanırken DATA-01, DATA-02 ve DATA-03 küçük, ayrı düzeltmeler olarak hazırlanabilir. Mevcut diyagram/harita/derse ait çalışmaları kaybetmeden main tabanlı ayrı worktree kullanılmalı.

Her iş için raporun sonuna şu kayıt eklenir:

```text
ID:
Durum:
Branch / taban commit:
Uygulama commit'i:
Değişen davranış:
Korunan davranış:
Test komutu / sonuç:
Tarayıcı / viewport / roller:
Migration / veri dönüşümü:
Yayın sonrası doğrulama:
Kalan risk:
```

Bir sonraki asistana güvenli başlangıç: git durumunu yeniden oku; rapordaki tarihi commit'i güncel sanma; açık işleri tamamlanmış sayma; anahtar değerlerini isteme veya loglama; kullanıcı verilerini test fixture'ı olarak yayımlama.

## Kaynaklar

- [Django sürüm desteği](https://www.djangoproject.com/download/#supported-versions): bağımlılık yaşam döngüsü.
- [Django güvenlik rehberi](https://docs.djangoproject.com/en/5.2/topics/security/): dosya yükleme, CSRF, escape ve güven sınırları.
- [WCAG 2.2 hızlı başvuru](https://www.w3.org/WAI/WCAG22/quickref/): erişilebilirlik kabul çerçevesi.

Kod bulguları bu raporda belirtilen yerel commit ve sentetik senaryolardan gelir. Dış kaynaklar siteye ait test sonucu veya güvenlik sertifikası değildir.


## Guncel Takip Notu: 2026-09-12

Bu rapor tarihsel inceleme tabanidir. Guncel is/yayin durumlari
`general_review_progress.md`, `content_security.md` ve
`content_export_improvements.md` dosyalarinda tutulur. Buradaki baslangic
"Acik" durumlari tek basina bugunku durumu ifade etmez.

