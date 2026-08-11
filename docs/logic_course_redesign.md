# Mantık Atölyesi: öğretim tasarımı

## Amaç

Program, kavram adlarını ezberleten uzun bir ders listesi olmak yerine öğrenciyi şu sırayla yetkinleştirmeyi hedefler:

1. Argümanı doğal dil içinde ayıklamak ve değerlendirmek.
2. Önermeler mantığının dilini ve semantiğini kullanmak.
3. Doğal türetimle gerekçeli kanıt kurmak.
4. Yüklem mantığında çeviri, model ve kanıt üretmek.
5. Çekirdek yeterlikten sonra metateoriye ve mantık felsefesine geçmek.

Çekirdek derslerde önerilen ustalık eşiği yüzde 70'tir. Çoktan seçmeli tanıma soruları tek başına ustalık kanıtı sayılmaz; üretim görevleri ve aşama kontrolleri müfredatın zorunlu tamamlayıcısıdır.

## Kaynak karşılaştırması

- [forall x: Calgary](https://forallx.openlogicproject.org/): temel kavramlar, önermeler mantığı, doğruluk tabloları, doğal türetim, yüklem mantığı, modeller ve yüklem mantığında türetim omurgası.
- [MIT OpenCourseWare Logic I](https://ocw.mit.edu/courses/24-241-logic-i-fall-2009/): geçerlilik/sağlamlık, sembolleştirme, doğruluk fonksiyonları, önermeler ve yüklem mantığı ile güvenirlik/tamlık kapsamı.
- [Carnap](https://carnap.io/about): çeviri, doğruluk tablosu ve türetim çalışmalarında anlık ve açıklayıcı geri bildirim modeli.
- [Sets, Logic, Computation](https://slc.openlogicproject.org/): çekirdek biçimsel mantıktan sonra metateori ve hesaplanabilirlik için ileri rota.

Bu kaynakların içeriği kopyalanmaz. Ortak yeterlik sırası, kapsam denetimi ve alıştırma türleri Türkçe öğrenme deneyimine uyarlanır.

## Müfredat haritası

| Aşama | Ders | Rota | Yeterlik kontrolü |
| --- | ---: | --- | --- |
| Akıl Yürütmenin Temelleri | 9 | Çekirdek | Metnin argüman şemasını çıkarıp geçerlilik iddiasını gerekçelendirme |
| Argüman Çözümleme Atölyesi | 5 | Çekirdek | Gerçek paragraftaki destek kusurunu gösterip daha güçlü sürümünü yazma |
| Önermeler Mantığı | 7 | Çekirdek | Sembolleştirme, doğruluk tablosu ve karşı satırla karar verme |
| Kanıt, Türetim ve Mantıksal Sonuç | 5 | Çekirdek | Aynı sonucu kanıt ve semantik yöntemle çözümleme |
| Yüklem Mantığı | 13 | Çekirdek | Çeviri, model/karşı model ve türetimi birlikte kullanma |
| İleri Mantık ve Metateori | 6 | Seçmeli | Sentaktik, semantik ve metateorik iddiaları ayrı ayrı açıklama |

## Ders sözleşmesi

Her ders şu parçaları taşır:

- Açık ve ölçülebilir öğrenme hedefleri.
- İlk kullanımda Türkçe karşılığı verilen tutarlı terminoloji.
- Kavram açıklaması, doğru örnek, yanlış örnek ve hata gerekçesi.
- Kontrollü alıştırma ve anında geri bildirim.
- Öğrencinin kendi çevirisini, tablosunu, modelini veya kanıtını ürettiği görev.
- Sonraki dersle kurulan açık bağlantı.

## Ölçme ilkeleri

- Başarı yalnız toplam puanla değil, beceri alanlarına göre raporlanır.
- Aynı test oturumu sayfa yenilendiğinde değişmez; yeni karışım kullanıcı kararıyla başlar.
- Yanıt değiştirilince eski değerlendirme geçersizleşir.
- Yanlış seçeneğin yanında doğru yanıt ve gerekçe görünür.
- Bitirme testi çekirdek rota ile ileri rotayı ileride ayrı raporlamalıdır.

## Editoryal sözlük

Terimler ilk kullanımda gerekirse İngilizcesi parantez içinde verilerek daha sonra Türkçe kullanılır:

- sound argument: sağlam argüman
- soundness (kanıt sistemi/metateorem): güvenirlik
- completeness: tamlık
- compactness: kompaktlık
- natural deduction: doğal türetim
- derived rule: türetilmiş kural
- function symbol: fonksiyon sembolü
- definite description: belirli betimleme
- prenex normal form: önek normal biçim
- truth tree: doğruluk ağacı

`→` maddi koşulu, `↔` çift yönlü koşulu ve `≡` metadil düzeyindeki eşdeğerliği gösterir. İçerik denetiminde bu üç gösterim birbirinin yerine kullanılmaz.

## Uygulama fazları

### Faz 1: omurga ve kullanılabilirlik

- Açık müfredat haritası ve doğrulanmış ders sırası.
- Ana sayfa arama/filtreleme ve devam et akışı.
- Kalıcı ders ilerlemesi, ustalık eşiği ve cihazda yanıt saklama.
- Okunabilir ders ekranı ve modüler bitirme testi.
- Mantık sayfaları için sitemap ve regresyon testleri.

### Faz 2: içerik ve üretim

- Tamamlandı: 45 dersin tamamında konuya özel, kontrol listeli üretim görevi var.
- Tamamlandı: önermeler ve yüklem mantığı için dört sembolleştirme laboratuvarı.
- Tamamlandı: iki doğruluk tablosu laboratuvarı; hücre bazlı geri bildirim ve kalıcı ilerleme.
- Tamamlandı: üç doğal türetim laboratuvarı; satır sıralama, kural gerekçesi ve hedefli hata ipucu.
- Tamamlandı: üç ayrı görevi olan model kurma laboratuvarı; yüklem ve ikili ilişki atamalarıyla koşul bazlı semantik geri bildirim.
- 45 dersin örnek, yanlış örnek, cevap ve sembol denetimi.
- Safsata bölümünü yalnız etiket tanımadan gerçek metin revizyonuna taşıma.

### Faz 3: müfredatın yeniden kurulması ve ustalık

- Mevcut derslerin önkoşul ve yetkinlik denetimi.
- Çekirdek, paralel atölye ve seçmeli rota ayrımı.
- Aşama sonu üretim görevleri, düzeltme rotaları ve gecikmeli geri çağırma.
- Her aşamanın akademik, otomatik ve gerçek kullanıcı testinden geçirilmesi.

Ayrıntılı kararlar için [Faz 3 denetim belgesine](logic_curriculum_phase3_audit.md) ve [A aşaması ders sözleşmesine](logic_phase3_stage_a_spec.md) bakılır.

### Faz 4: mantık ve dil felsefesi köprüsü

- Frege'de fonksiyon/argüman, kavram/nesne ve anlam/gönderim.
- Russell'da belirli betimlemeler ve mantıksal biçim.
- Mantıksal atomculuk, temsil, adlandırma ve önermenin dünya ile ilişkisi.

### Faz 5: erken Wittgenstein

- `Tractatus Logico-Philosophicus` için bölüm bölüm rehberli okuma.
- Resim kuramı, olgu, nesne, mantıksal biçim, doğruluk işlemleri ve totolojiler.
- Benlik, dünya, bilim, etik ve söylenebilirliğin sınırı.

### Faz 6: geç Wittgenstein

- Erken dönemden geç döneme yöntem değişimi.
- Dil oyunları, anlam ve kullanım, aile benzerliği, kural izleme ve özel dil.
- `Felsefi Soruşturmalar`, `Mavi ve Kahverengi Kitaplar` ve `Kesinlik Üstüne` için rehberli okuma.
- Bütün programın ilk dersten son okuma görevine kadar yeniden denetlenmesi.

## Yayın öncesi kontrol

- Her görünür ders tam bir aşamada ve yalnız bir kez yer alıyor mu?
- Her çoktan seçmeli sorunun doğru yanıtı seçenekler arasında mı?
- Sembolik eşdeğerlikler ve çıkarım yönleri doğru mu?
- Türkçe terim kullanımı tutarlı mı?
- Masaüstü ve mobilde metin, sabit paneller ve seçenekler çakışıyor mu?
- Giriş yapmış ve anonim kullanıcı ilerlemesi veri kaybetmeden çalışıyor mu?
