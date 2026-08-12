# Faz 3D: Önermeler mantığında doğal türetim

## Statü

Bu belge Faz D'nin kaynaklara dayalı **aday ders sözleşmesidir**. D20-D26 derslerinin akademik sırası, kural sistemi, gösterimi, ölçme biçimi ve Faz C/E sınırları burada sabitlenir. Üretim kaydı hangi aday ders verilerinin ve denetleyici kurallarının hazır olduğunu gösterir; yetkili önizleme ile öğrenciye açık ekran bu faz tamamlanana kadar ayrı tutulur.

Faz D yedi dersten oluşur. Mevcut canlı içerikte birbirinden kopuk görünen “çıkarım kuralları”, “doğal türetim” ve “reductio” başlangıçları tek bir Fitch çizgisinde birleştirilir: önce kanıt satırı ve erişilebilirlik, sonra bağlaç kuralları, alt kanıtlar, strateji, türetilmiş kurallar ve son olarak sentaktik türetilebilirlik ile semantik sonuç arasındaki ilişki.

Bu belge öğrenciye görünen dersleri, ilerleme kayıtlarını, URL'leri veya mevcut veri modelini değiştirmez.

## Kaynak ve kapsam denetimi

| Kaynak | Faz D'deki işlevi |
| --- | --- |
| [forall x: Calgary, Bölüm 16](https://forallx.openlogicproject.org/html/Ch16.html) | Doğruluk tablosu ile doğal türetimin farklı açıklayıcı rolleri; Fitch sisteminin amacı ve tarihsel konumu |
| [forall x: Calgary, Bölüm 17](https://forallx.openlogicproject.org/html/Ch17.html) | Satır, gerekçe, alt kanıt ve TFL bağlaçlarının temel giriş/eleme kuralları |
| [forall x: Calgary, Bölüm 18](https://forallx.openlogicproject.org/html/Ch18.html) | Hedeften geriye ve eldeki satırlardan ileri çalışma; koşul, olumsuzlama, ayrık bağlaç ve dolaylı kanıt stratejileri |
| [forall x: Calgary, Bölüm 19](https://forallx.openlogicproject.org/html/Ch19.html) | DS, MT, DNE, LEM ve De Morgan gibi ek kuralların kullanımı |
| [forall x: Calgary, Bölüm 20](https://forallx.openlogicproject.org/html/Ch20.html) | `⊢`, teorem, birlikte tutarsızlık ve karşılıklı türetilebilirlik gibi kanıt kuramsal kavramlar |
| [forall x: Calgary, Bölüm 21](https://forallx.openlogicproject.org/html/Ch21.html) | Türetilmiş kuralın temel kurallarla ikame edilebilir bir kanıt şeması olması |
| [forall x: Calgary, Bölüm 22](https://forallx.openlogicproject.org/html/Ch22.html) | `⊢` ile `⊨` ayrımı; güvenirlik ve tamlığın iki ayrı yönü |
| [MIT OCW Logic I](https://ocw.mit.edu/courses/24-241-logic-i-fall-2009/) | Biçimsel türetimler, önerme ve yüklem mantığı ile güvenirlik/tamlığın lisans düzeyi ikinci müfredat kontrolü |
| [Carnap derivation documentation](https://carnap.io/srv/doc/derivations.md) | Fitch kanıtlarının yapılandırılmış, satır bazlı ve otomatik denetlenebilir alıştırma olarak modellenmesi |
| [Carnap feedback documentation](https://carnap.io/srv/doc/faq.md) | Anlık doğru/yanlış geri bildirimi yerine gerektiğinde manuel veya yalnız sözdizimsel geri bildirim kullanma olanağı |

`forall x`, doğal türetimi doğruluk tablolarının yerine geçen tek yöntem olarak sunmaz. İki yöntem aynı geçerlilik ilişkisine farklı yollardan yaklaşır: tablo değerlemeleri tarar, türetim ise lisanslı kural adımlarını görünür kılar. Faz D bu ayrımı D20'de kurar, fakat güvenirlik ve tamlığı D26'ya kadar sonuç olarak kullanmaz.

## Aşama sınırı

Faz D yalnız **klasik iki değerli TFL için Fitch tarzı doğal türetimi** öğretir:

- kanıt satırı, satır numarası, formül, gerekçe ve atıf;
- öncül, geçici varsayım, açık ve kapalı alt kanıt;
- bir satırın hangi kapsamda erişilebilir olduğu;
- giriş (`I`) ve eleme (`E`) kuralı ayrımı;
- `∧`, `→`, `¬`, `∨` ve `↔` için temel kurallar;
- çelişki işareti `⊥`, olumsuzlama ve klasik dolaylı kanıt;
- hedeften geriye ve mevcut satırlardan ileri kanıt planlama;
- türetilmiş kurallar ile açıkça lisanslanmış eşdeğerlik dönüşümleri;
- `⊢`, teorem, karşılıklı türetilebilirlik ve sentaktik tutarsızlık;
- `⊢` ile `⊨` arasındaki güvenirlik ve tamlık köprüsü.

Şunlar Faz D'de öğretilmez veya ustalık ölçütü yapılmaz:

- niceleyici giriş/eleme kuralları, birey sabiti kısıtları ve kimlik;
- birinci derece model ve karşı model üretimi;
- doğruluk ağaçları, çözüm tabloları veya aksiyomatik sistemler;
- sekant hesabı, Gentzen ağaçları veya normalleştirme teoremi;
- güvenirlik ve tamlığın metateorik ispatı;
- sezgici, ilgili, paratutarlı veya modal doğal türetim sistemleri;
- eşdeğer görünen her formül çiftini gerekçesiz yeniden yazma yetkisi.

D22'deki dolaylı kanıt ve D23'teki ayrık durum analizi klasik TFL sistemi içinde öğretilir. Patlama (`X`) ve dışlanan orta gibi ilkeler kullanıldığında bunların sistem seçimine bağlı olduğu kısa bir sınır notuyla belirtilir; alternatif mantıkların teknik kuralları bu aşamaya taşınmaz.

## Gösterim ve kural sözleşmesi

1. **Cümle harfleri:** Faz B/C ile tutarlı olarak `A`, `B`, `C` kullanılır. Küçük `p`, `q`, `r` yalnız eski canlı içerikten geçiş örneğinde görülebilir.
2. **Üst değişkenler:** `𝒜`, `ℬ`, `𝒞` herhangi bir TFL cümlesinden söz eden üst değişkenlerdir; kanıt satırına TFL cümlesi gibi yazılmaz.
3. **Türetilebilirlik:** `Γ ⊢ 𝒞`, açık/boşaltılmamış varsayımları `Γ` içinde olan ve `𝒞` ile biten en az bir türetim bulunduğunu söyler. `⊢`, TFL'nin nesne dili bağlacı değildir.
4. **Semantik sonuç:** `Γ ⊨ 𝒞`, `Γ`'daki bütün cümleleri doğru ve `𝒞`'yi yanlış yapan değerleme bulunmadığını söyler. `⊢` ile `⊨` biçimce ve kavramca ayrı tutulur.
5. **Kanıt satırı:** Her satır `numara + kapsam derinliği + formül + gerekçe + atıf` alanlarını taşır. Doğru formül, gerekçesizse tamamlanmış kanıt satırı sayılmaz.
6. **Öncül:** `PR`, kanıt probleminin başlangıç verisidir. Öncül için başka satır atfı yazılmaz.
7. **Varsayım:** `AS`, yalnız açtığı alt kanıt içinde geçerli geçici varsayımdır. Alt kanıt kapanınca varsayım boşaltılır; fakat içeride üretilen satırlar dışarıdan tek tek kullanılamaz.
8. **Erişilebilirlik:** Bir satır, mevcut satırın bulunduğu kapsamda veya onu çevreleyen hâlâ açık bir kapsamda yer alıyorsa erişilebilirdir. Kapanmış kardeş/çocuk alt kanıtın iç satırı doğrudan atıf alamaz.
9. **Alt kanıt atfı:** `→I`, `¬I`, `IP` ve `∨E` gibi kurallar, kapattıkları alt kanıtın satır aralığına atıf yapar. Bu, içerideki son satırı dışarı taşımak değildir.
10. **Giriş ve çıkarım:** `I` kuralı ana bağlacı hedefte kurar; `E` kuralı ana bağlacı taşıyan erişilebilir bir satırdan bilgi çıkarır. Adlar ezber değil hedef/veri türü olarak öğretilir.
11. **Çelişki:** `⊥`, bu kanıt sisteminde her değerlemede yanlış olan özel işaret olarak kullanılır. `𝒜` ve `¬𝒜`dan `¬E` ile elde edilir.
12. **Patlama:** `⊥`dan herhangi bir TFL cümlesine geçiş `X` ile açıkça gerekçelendirilir. `⊥` elde edilmeden patlama kullanılamaz.
13. **Klasik dolaylı kanıt:** `IP`, `¬𝒜` varsayımından `⊥` türeterek `𝒜`ya geçer. Bu kural `¬I` ile aynı değildir ve klasik sistem seçimini görünür kılar.
14. **Çift yönlülük:** `↔I`, `𝒜` varsayımından `ℬ`ye ve `ℬ` varsayımından `𝒜`ya ulaşan iki alt kanıt gerektirir; `↔E`, çift yönlü cümle ile taraflardan birinden öteki tarafı çıkarır. Tek yön çift yönlülük için yeterli değildir.
15. **Türetilmiş kural:** DS, MT, DNE, LEM ve DeM, temel kurallar kullanılarak sistematik olarak ikame edilebilen kanıt şemalarıdır. Yeni türetilebilir sonuçlar eklemezler.
16. **Eşdeğerlik dönüşümü:** C17'de semantik olarak eşdeğer bulunmuş olmak, D25'ten önce bir kanıt satırını sessizce yeniden yazma lisansı vermez. D25'te yalnız sözleşmede listelenen dönüşümler kural adıyla kullanılabilir.
17. **Kanıt tamamlanması:** Son satırın hedef formülle eşleşmesi tek başına yeterli değildir. Hedef satır erişilebilir olmalı, bütün atıflar geçerli olmalı ve hedefe bağlı açık varsayım kalmamalıdır.
18. **Kural etiketleri:** Kullanıcı arayüzünde sembolik ad ile Türkçe işlev birlikte gösterilir: `∧I · Birleşim kur`, `→E · Koşulu uygula` gibi.

## Temel kural envanteri

| Kural | Girdi | Çıktı | Alt kanıt/kapsam koşulu |
| --- | --- | --- | --- |
| `R` | `𝒜` | `𝒜` | Kaynak satır erişilebilir olmalı |
| `∧I` | `𝒜`, `ℬ` | `𝒜 ∧ ℬ` | İki kaynak da erişilebilir olmalı |
| `∧E` | `𝒜 ∧ ℬ` | `𝒜` veya `ℬ` | Kaynak satır erişilebilir olmalı |
| `→E` | `𝒜 → ℬ`, `𝒜` | `ℬ` | İki kaynak da erişilebilir olmalı |
| `→I` | `𝒜` varsayımı altında `ℬ` | `𝒜 → ℬ` | İlgili alt kanıt kapanır ve `𝒜` boşaltılır |
| `¬E` | `𝒜`, `¬𝒜` | `⊥` | İki kaynak da aynı erişilebilir kapsamda olmalı |
| `¬I` | `𝒜` varsayımı altında `⊥` | `¬𝒜` | İlgili alt kanıt kapanır ve `𝒜` boşaltılır |
| `IP` | `¬𝒜` varsayımı altında `⊥` | `𝒜` | Klasik dolaylı kanıt; ilgili alt kanıt kapanır |
| `X` | `⊥` | `𝒜` | `⊥` erişilebilir olmalı |
| `∨I` | `𝒜` | `𝒜 ∨ ℬ` veya `ℬ ∨ 𝒜` | Eklenen ayrılan herhangi bir TFL cümlesi olabilir |
| `∨E` | `𝒜 ∨ ℬ`; `𝒜`dan `𝒞`; `ℬ`den `𝒞` | `𝒞` | İki kardeş alt kanıt da aynı `𝒞` ile bitmeli ve kapanmalı |
| `↔I` | `𝒜`dan `ℬ`; `ℬ`den `𝒜` | `𝒜 ↔ ℬ` | İki yön de lisanslı biçimde gösterilmeli |
| `↔E` | `𝒜 ↔ ℬ`, taraflardan biri | öteki taraf | Çift yönlülüğün seçilen yönü açık olmalı |

## Aşama amacı

Öğrenci Faz D sonunda:

1. Bir kanıt problemini öncüller, hedef ve açık varsayımlar olarak okur.
2. Her satırın formülünü, kuralını ve atıflarını denetler.
3. Açık ve kapalı alt kanıtların erişilebilirlik sınırlarını ihlal etmez.
4. Beş TFL bağlacı için giriş/eleme kurallarını hedefe ve mevcut satırlara göre seçer.
5. Doğrudan kanıt, koşullu kanıt, durumlara göre kanıt, olumsuzlama ve klasik dolaylı kanıt arasında gerekçeli seçim yapar.
6. Hedeften geriye ve öncüllerden ileri çalışmayı bir ara hedefte birleştirir.
7. Temel kural ile türetilmiş kuralı ayırır ve en az iki türetilmiş kuralın kanıt şemasını açar.
8. `Γ ⊢ 𝒞` ile `Γ ⊨ 𝒞`yi ayırır; güvenirlik ve tamlığın hangi yönleri bağladığını açıklar.
9. Kısa ve orta uzunlukta bir TFL türetimini bağımsız olarak kurar, denetler ve daha ekonomik hâle getirir.

## Aşama çıkış görevi

Öğrenciye daha önce görmediği, beş öncüllü bir TFL türetim problemi verilir. Problem `∧`, `→`, `¬`, `∨` ve `↔` kurallarından en az dördünü, en az iki alt kanıtı ve bir ara hedefi gerektirir. Öğrenci:

1. Öncülleri, hedefi ve hedefin ana bağlacını yazar.
2. Hedeften geriye en olası son kuralı ve onun alt hedeflerini planlar.
3. Öncüllerden ileri kullanılabilir eleme adımlarını çıkarır.
4. Her satırı formül, kural ve atıfla tamamlar.
5. Alt kanıtların açılış, erişim ve kapanış sınırlarını görünür tutar.
6. Kanıtı önce yalnız temel kurallarla tamamlar.
7. Aynı kanıtı en az bir türetilmiş kural kullanarak kısaltır ve hangi temel şemanın gizlendiğini açıklar.
8. Kanıttaki bir kapsam hatasını ve bir yanlış kural eşleşmesini teşhis edip düzeltir.
9. Elde ettiği `Γ ⊢ 𝒞` sonucunun `Γ ⊨ 𝒞` ile ilişkisini güvenirlik ve tamlık yönleriyle açıklar.
10. Başarısız bir kanıt aramasının neden tek başına `Γ ⊬ 𝒞` veya `Γ ⊭ 𝒞` göstermediğini belirtir.

Çıkış görevi yalnız son formülle geçilemez. Satır lisansları, bağımlılık/kapsam yapısı, strateji notu ve temel/türetilmiş kural karşılaştırması incelenebilir olmalıdır.

## Ortak ders sözleşmesi

Her aday ders şu alanları taşıyacaktır:

```text
prerequisites: Önce tamamlanması gereken aday ders kimlikleri
competencies: Dersin ölçülebilir beceri kimlikleri
estimated_minutes: Pilotla doğrulanacak aktif çalışma süresi
mastery_evidence: Öğrencinin ürettiği ve incelenebilen kanıt
review_prompts: Sonraki derslerde gecikmeli geri çağırma soruları
rule_scope: Derste ilk kez kullanılabilen ve yalnız geri çağrılan kurallar
```

Her derste kısa geri çağırma, tek yeni eşik, tam çözülmüş türetim, kısmen tamamlanmış türetim, hatalı kanıt denetimi ve bağımsız üretim bulunur. Otomatik denetleyici yalnız doğru/yanlış sonucu vermemeli; ilk bozuk satırı, kural eşleşmesini veya kapsam ihlalini açıklamalıdır. İpucu doğrudan doğru satırı yazmak yerine hedef türünü veya erişilebilir veri türünü hatırlatmalıdır.

## D20 — Kanıt fikri, satır bağımlılığı ve hedef okuma

### Ders sözleşmesi

- **Tahmini süre:** 40 dakika (pilotla doğrulanacak)
- **Önkoşul:** A4, A6, C18, C19
- **Ana eşik:** Bir Fitch türetimini sonuç listesi olarak değil, her satırı erişilebilir kaynaklar ve açık varsayımlar tarafından lisanslanan bağımlılık yapısı olarak okumak.
- **Yetkinlikler:** `nd.sequent_read`, `nd.line_audit`, `nd.scope_read`, `nd.target_classify`
- **İlk kurallar:** `PR`, `AS`, `R`

### Öğrenme hedefleri

1. `Γ ⊢ 𝒞` yazımını kanıtın varlığı hakkında üst dil iddiası olarak okumak.
2. Öncül, hedef, satır, gerekçe, atıf ve kapsam derinliğini ayırmak.
3. Bir satırın hangi önceki satırlara erişebildiğini belirlemek.
4. Hedefin ana bağlacından olası son kural türünü tahmin etmek; henüz kuralı uygulamamak.

### Akademik not

Kanıt, doğru cümlelerin sıralanması değildir. Aynı formül yanlış kapsamdan veya yanlış atıfla yazıldığında satır lisanssızdır. `Γ ⊢ 𝒞`, belirli ekrandaki denemenin başarıyla bitmesinden daha genel olarak uygun bir türetim bulunduğunu söyler.

### Kritik yanılgılar

- Son satır hedefe eşitse aradaki satırların otomatik doğru olduğunu sanmak.
- Kapanmış alt kanıttaki her satırı dışarıdan erişilebilir saymak.
- `⊢`yi TFL bağlacı veya `⊨`nin farklı yazı tipi sanmak.
- Başarısız birkaç denemeden hiçbir kanıt bulunmadığı sonucunu çıkarmak.

### Kademeli pratik

1. Hazır bir türetimde satır numarası, formül, gerekçe ve atıf alanlarını etiketleme.
2. İç içe iki alt kanıtta her satır için erişilebilir kaynakları seçme.
3. Beş hedefi ana bağlaçlarına göre olası giriş kuralıyla eşleme.
4. Kapanmış alt kanıt satırını kullanan bir kanıtı ilk bozuk satırda durdurma.

### Bağımsız üretim

Verilen kısa Fitch türetimini bağımlılık kenarlarıyla yeniden çiz; iki lisanssız satırı bul, erişilebilir kaynaklarla düzelt ve nedenini yaz.

### Ustalık kanıtı

- Sekiz satırlık türetimde bütün satır lisanslarını doğru sınıflandırma.
- Kapsam ihlalini yalnız “yanlış” diye değil, hangi satırın neden erişilemez olduğunu belirterek açıklama.
- `⊢` ve `⊨` ayrımını kendi örneğiyle doğru kurma.
- Yeni bir hedef için olası son kuralı ana bağlaçtan gerekçelendirme.

### Gecikmeli geri çağırma

- Kapanmış bir alt kanıtın son satırı neden doğrudan dışarı taşınamaz?
- `Γ ⊢ 𝒞` neyin varlığını bildirir?
- Doğru formül hangi iki nedenle yine de geçersiz kanıt satırı olabilir?

## D21 — Birleşim ve koşul kuralları

### Ders sözleşmesi

- **Tahmini süre:** 50 dakika (pilotla doğrulanacak)
- **Önkoşul:** D20, B8, B10, C14
- **Ana eşik:** `∧` ve `→` için giriş/eleme kurallarını hedef türü ile erişilebilir veri türünü birleştirerek uygulamak.
- **Yetkinlikler:** `nd.conjunction_rules`, `nd.conditional_eliminate`, `nd.conditional_introduce`, `nd.subproof_discharge`
- **İlk kurallar:** `∧I`, `∧E`, `→I`, `→E`

### Öğrenme hedefleri

1. Birleşimden iki yönde bileşen çıkarmak ve iki erişilebilir cümleden sıralı birleşim kurmak.
2. Koşul ile önbileşenden artbileşen üretmek.
3. Koşul hedefinde önbileşeni geçici varsayarak alt kanıt açmak ve boşaltmak.
4. `→I` ile `→E`yi aynı işaretin iki farklı kanıt rolü olarak ayırmak.

### Akademik not

`→I` sonunda elde edilen koşul, alt kanıt içindeki varsayımın dışarıda hâlâ doğru kabul edildiğini söylemez; varsayım boşaltılmıştır. Buna karşılık dış kapsamda erişilebilir öncüller alt kanıt içinde kullanılabilir.

### Kritik yanılgılar

- `𝒜 ∧ ℬ`den yalnız soldaki bileşenin çıkarılabileceğini sanmak.
- `∧I` ile kaynak sırasını görmezden gelip hedefteki bileşen sırasını yanlış kurmak.
- `𝒜 → ℬ`den önbileşen olmadan `ℬ` üretmek.
- `→I` sonrasında varsayım satırını dışarıda yeniden kullanmak.

### Kademeli pratik

1. Tek satırlık `∧E` ve iki kaynaklı `∧I` tamamlama.
2. `→E` için koşul ile tam eşleşen önbileşeni seçme.
3. Sonu koşul olan kanıt iskeletinde alt kanıt başlangıç/bitişini yerleştirme.
4. İç içe koşul hedefinde iki varsayımın hangi sırayla boşaltıldığını izleme.

### Bağımsız üretim

`A → (B → C), A ∧ B ⊢ C ∧ A` ve `A ∧ B ⊢ C → (A ∧ C)` türetimlerini kur; ikinci kanıtta alt kanıt bağımlılıklarını ayrıca işaretle.

### Ustalık kanıtı

- Dört kuralı en az bir kez doğru kullanan iki bağımsız türetim.
- `→I` kapanışında doğru satır aralığı ve boşaltılan varsayım.
- Yanlış yönlü `→E` ve kapsam dışı atfı teşhis etme.
- Hedefin ana bağlacına göre son kuralı açıklama.

### Gecikmeli geri çağırma

- `→I` neden bir alt kanıt ister?
- `𝒜 → ℬ` ile `ℬ` hangi sonucu lisanslamaz?
- Dış kapsamdaki bir öncül alt kanıt içinde ne zaman kullanılabilir?

## D22 — Olumsuzlama, alt kanıt ve çelişkiye indirgeme

### Ders sözleşmesi

- **Tahmini süre:** 55 dakika (pilotla doğrulanacak)
- **Önkoşul:** D21, C16, C17
- **Ana eşik:** Açık çelişki üretimini olumsuzlama girişi, patlama ve klasik dolaylı kanıt içinde kapsamı bozmadan kullanmak.
- **Yetkinlikler:** `nd.contradiction_build`, `nd.negation_rules`, `nd.explosion_apply`, `nd.indirect_proof`
- **İlk kurallar:** `¬I`, `¬E`, `X`, `IP`

### Öğrenme hedefleri

1. `𝒜` ile `¬𝒜`dan `⊥` üretmek.
2. `𝒜` varsayımı altında `⊥` türetip `¬𝒜` elde etmek.
3. `⊥`dan hedef cümleyi `X` ile açıkça üretmek.
4. `¬𝒜` varsayımı altında `⊥` türetip klasik `IP` ile `𝒜` elde etmek.
5. `¬I`, `IP` ve `X` kurallarının farklı girdi/çıktı yapılarını ayırmak.

### Akademik not

`¬I` ile klasik dolaylı kanıt aynı şema değildir: ilki `𝒜` varsayımını boşaltıp `¬𝒜`, ikincisi `¬𝒜` varsayımını boşaltıp `𝒜` üretir. Patlama ise bir alt kanıt kapatma kuralı değil, erişilebilir `⊥`dan yeni satır üretme kuralıdır.

### Kritik yanılgılar

- İki farklı cümleyi çelişki saymak; açık `𝒜`/`¬𝒜` çiftini göstermemek.
- Çelişki üretmeden `X` kullanmak.
- Hedef olumlu olduğu her durumda doğrudan `IP` açmak.
- Alt kanıt içinde oluşan `⊥`ı ilgili kuralı uygulamadan dışarı taşımak.

### Kademeli pratik

1. Hazır satırlar içinde gerçek çelişki çiftini seçme.
2. Eksik `¬I` iskeletinde varsayım, `⊥` ve kapanışı yerleştirme.
3. Aynı hedef için doğrudan yol ile `IP` yolunu karşılaştırma.
4. Patlamanın meşru ve gayrimeşru kullanımlarını ayırma.

### Bağımsız üretim

`A → B, A → ¬B ⊢ ¬A`, `¬¬A ⊢ A` ve `A, ¬A ⊢ C` türetimlerini o ana kadar açılmış kurallarla kur; her `⊥` için çelişen iki satırı açıkça belirt.

### Ustalık kanıtı

- `¬I`, `IP` ve `X` kullanan üç kısa türetimde doğru alt kanıt sınırı.
- Her `⊥` satırında tam çelişki çifti ve doğru atıf.
- Doğrudan yol varken gereksiz `IP` kullanımını teşhis etme.
- Patlamanın klasik TFL içindeki semantik gerekçesini, alternatif sistemlere genellemeden açıklama.

### Gecikmeli geri çağırma

- `¬I` ile `IP` hangi varsayımları boşaltır?
- `⊥` hangi durumda dış kapsamda kullanılabilir hâle gelir?
- Patlama neden “çelişki gibi görünen” iki satırdan uygulanamaz?

## D23 — Ayrık bağlaç ve çift yönlülük kuralları

### Ders sözleşmesi

- **Tahmini süre:** 55 dakika (pilotla doğrulanacak)
- **Önkoşul:** D22, B9, B10, C17
- **Ana eşik:** Ayrık olasılıkları iki kardeş alt kanıtta tüketmek ve çift yönlülüğün iki yönünü ayrı kanıt yükleri olarak kurmak.
- **Yetkinlikler:** `nd.disjunction_introduce`, `nd.cases_prove`, `nd.biconditional_rules`, `nd.sibling_scope_manage`
- **İlk kurallar:** `∨I`, `∨E`, `↔I`, `↔E`

### Öğrenme hedefleri

1. Erişilebilir bir cümleden uygun sırayla ayrık bağlaç üretmek.
2. `𝒜 ∨ ℬ` üzerinde iki kardeş alt kanıt açıp her ikisinden aynı `𝒞` sonucuna ulaşmak.
3. Çift yönlü koşuldan doğru yönü kullanarak çıkarım yapmak.
4. Çift yönlülüğü iki yönlü kanıt yükünü tamamlayarak kurmak.

### Akademik not

`∨E`, “hangi ayrılan doğru olursa olsun aynı sonuç” yapısını kanıtlar. İki alt kanıtın farklı sonuçlarla bitmesi yeterli değildir. `↔I` de tek bir koşuldan veya iki formülün birlikte doğru görünmesinden elde edilmez; iki yön ayrı ayrı lisanslanır.

### Kritik yanılgılar

- `𝒜 ∨ ℬ`den doğrudan `𝒜` veya doğrudan `ℬ` çıkarmak.
- `∨E` dallarını farklı sonuçlarla kapatmak.
- İlk dalın varsayımını ikinci dalda kullanmak.
- `𝒜 → ℬ`den `𝒜 ↔ ℬ` üretmek.

### Kademeli pratik

1. `∨I` hedefinde hangi ayrılanın hazır olduğunu belirleme.
2. `∨E` iskeletinde iki dalın ortak hedefini seçme.
3. Kardeş alt kanıtlar arasındaki erişim ihlalini bulma.
4. `↔I` için iki yönün ara hedeflerini kurma ve `↔E` yönünü seçme.

### Bağımsız üretim

`A ∨ B, A → C, B → C ⊢ C` ve `A ↔ B ⊢ (A ∧ B) ∨ (¬A ∧ ¬B)` türetimlerini kur; ikinci kanıtta seçtiğin doğrudan/dolaylı stratejiyi açıkla.

### Ustalık kanıtı

- İki doğru kardeş alt kanıtla tamamlanan bağımsız `∨E` türetimi.
- `↔I`de her iki yönün açıkça gösterilmesi.
- `↔E` yön hatası ve kardeş kapsam ihlalinin teşhisi.
- Ayrık bağlaç çevirisi ile kanıt içindeki durum analizi rolünü ayırma.

### Gecikmeli geri çağırma

- `∨E` dalları neden aynı cümleyle bitmelidir?
- Bir kardeş alt kanıttaki satır öteki dalda neden kullanılamaz?
- `↔I` için tek bir yön neden yetersizdir?

## D24 — Geriye doğru planlama ve kanıt stratejisi

### Ders sözleşmesi

- **Tahmini süre:** 55 dakika (pilotla doğrulanacak)
- **Önkoşul:** D23
- **Ana eşik:** Hedefin ana bağlacından geriye ve erişilebilir satırların ana bağlaçlarından ileri çalışarak iki aramayı gerekçeli ara hedefte buluşturmak.
- **Yetkinlikler:** `nd.backward_plan`, `nd.forward_expand`, `nd.subgoal_choose`, `nd.proof_repair`
- **Yeni kural:** Yok; D20-D23 kuralları stratejik olarak birleştirilir.

### Öğrenme hedefleri

1. Hedef formülün ana bağlacına göre olası son kuralı ve gereken alt hedefleri yazmak.
2. Öncül/varsayımların ana bağlaçlarına göre yararlı eleme adımlarını seçmek.
3. İleri ve geri aramayı ekonomik bir ara hedefte birleştirmek.
4. Kör `IP`, gereksiz patlama ve hedefsiz satır üretimini teşhis etmek.
5. Başarısız kanıt taslağını ilk stratejik çıkmazdan onarmak.

### Akademik not

Kanıt bulma için her problemi çözen mekanik bir tarif yoktur. Buna rağmen giriş kuralları hedef yapısını, çıkarım kuralları mevcut veri yapısını açtığı için arama tamamen rastgele değildir. İyi strateji, kural doğruluğuna ek bir başarı ölçütüdür; kural doğruluğunun yerini almaz.

### Kritik yanılgılar

- Her erişilebilir satıra uygulanabilecek her kuralı sırayla denemek.
- Hedefin ana bağlacını görmeden doğrudan `IP` açmak.
- Bir ara hedefin hangi sonraki kuralı açacağını açıklayamamak.
- Daha kısa kanıtı otomatik olarak daha doğru sanmak.

### Kademeli pratik

1. On hedef için olası son kuralı seçme.
2. On mevcut satır için yararlı eleme çıktısını seçme.
3. Yarım kanıtta ileri ve geri izler arasındaki eksik ara hedefi bulma.
4. İki geçerli kanıtı açıklık, kapsam derinliği ve satır ekonomisi bakımından karşılaştırma.

### Bağımsız üretim

Üç farklı orta uzunlukta kanıt problemi için önce yalnız kanıt planı yaz, sonra birini tamamla; tamamlanan kanıtta her ara hedefin hangi nihai adımı mümkün kıldığını kenar notunda belirt.

### Ustalık kanıtı

- Yeni bir problemde uygulanabilir geriye doğru plan.
- En az iki eleme adımını hedefle ilişkili seçme.
- Kör deneme yerine gerekçeli ara hedef üretme.
- Hatalı bir kanıtı ilk bozuk satır ve stratejik neden ile onarma.

### Gecikmeli geri çağırma

- Koşul hedefi hangi son kuralı düşündürür?
- Ayrık bir erişilebilir satır hangi tür ileri çalışma olanağı verir?
- Bir ara hedefin yararlı olduğunu nasıl anlarsın?

## D25 — Türetilmiş kurallar ve eşdeğerliklerin lisansı

### Ders sözleşmesi

- **Tahmini süre:** 50 dakika (pilotla doğrulanacak)
- **Önkoşul:** D24, C17
- **Ana eşik:** Türetilmiş kuralı yeni bir mantıksal güç değil, temel kurallarla her kullanımında ikame edilebilen denetlenmiş kanıt şeması olarak kullanmak.
- **Yetkinlikler:** `nd.derived_rule_expand`, `nd.derived_rule_apply`, `nd.equivalence_license`, `nd.proof_compress`
- **İlk kurallar:** `DS`, `MT`, `DNE`, `LEM`, `DeM`; açıkça listelenen eşdeğerlik dönüşümleri

### Öğrenme hedefleri

1. Türetilmiş kural ile temel kuralı ayırmak.
2. DS ve MT kullanımını temel kurallarla açmak.
3. DNE ve LEM'in klasik sistem bağımlılığını görünür tutmak.
4. De Morgan ve diğer izinli eşdeğerlikleri kural adıyla, yönü açık olarak uygulamak.
5. Kanıtı kısaltırken gizlenen temel şemayı açıklamak.

### Akademik not

Türetilmiş kuralın meşruiyeti tanıdık veya kısa görünmesinden değil, temel kurallarla sistematik olarak ikame edilebilmesinden gelir. Semantik eşdeğerlik kanıt içi yeniden yazma lisansını tek başına vermez; söz konusu kanıt sistemi bu dönüşümü kural olarak kabul etmelidir.

### Kritik yanılgılar

- Her geçerli çıkarım kalıbını kural listesine eklenmiş saymak.
- C17'de eşdeğer bulunan iki cümleyi kural adı olmadan satır içinde değiştirmek.
- DS veya MT'yi temel kural sanmak.
- DNE ile çift olumsuzlamanın doğal dildeki her kullanımının eş anlamlı olduğunu iddia etmek.

### Kademeli pratik

1. Kural listesini temel/türetilmiş olarak sınıflandırma.
2. Bir DS ve bir MT satırını temel kurallı alt kanıtlarla açma.
3. Aynı kanıtın uzun temel ve kısa türetilmiş sürümünü karşılaştırma.
4. Sessiz eşdeğerlik dönüşümü içeren kanıtı kural adlarıyla onarma.

### Bağımsız üretim

Bir kanıtı yalnız temel kurallarla, sonra DS/MT/DeM kullanarak iki sürümde yaz; her kısaltmanın arkasındaki temel kanıt şemasını ekle.

### Ustalık kanıtı

- En az iki türetilmiş kuralın doğru temel-kural açılımı.
- İzinli eşdeğerlik dönüşümünde doğru kaynak, yön ve kural etiketi.
- Temel/türetilmiş ayrımını “daha güçlü” dili kullanmadan açıklama.
- Klasik ilkenin sistem bağımlılığını doğru sınırlandırma.

### Gecikmeli geri çağırma

- Türetilmiş kural neden yeni türetilebilir sonuç eklemez?
- Semantik eşdeğerlik neden tek başına satır yeniden yazma lisansı değildir?
- DS'nin temel kurallı açılımında hangi iki alt kanıt gerekir?

## D26 — Kanıt ile semantik geçerlilik arasındaki ilişki

### Ders sözleşmesi

- **Tahmini süre:** 45 dakika (pilotla doğrulanacak)
- **Önkoşul:** D25, C18, C19
- **Ana eşik:** `Γ ⊢ 𝒞` ile `Γ ⊨ 𝒞`yi ayırmak ve güvenirlik/tamlığın iki yönünü uygulama düzeyinde doğru okumak.
- **Yetkinlikler:** `nd.turnstile_distinguish`, `nd.soundness_read`, `nd.completeness_read`, `nd.method_compare`
- **Yeni kural:** Yok; kanıt kuramsal kavramlar ve metateorik köprü kurulur.

### Öğrenme hedefleri

1. Türetilebilirlik, teorem, karşılıklı türetilebilirlik ve sentaktik tutarsızlığı tanımlamak.
2. `⊢` ile `⊨` işaretlerini nesne dili/üst dil ve yöntem bakımından ayırmak.
3. Güvenirliği `Γ ⊢ 𝒞` ise `Γ ⊨ 𝒞` yönü olarak okumak.
4. Tamlığı `Γ ⊨ 𝒞` ise `Γ ⊢ 𝒞` yönü olarak okumak.
5. Bir problemin amacına göre tablo veya türetim yöntemini seçmek.

### Akademik not

Bu derste güvenirlik ve tamlık **ispatlanmaz**; TFL için kabul edilen metateorik sonuçların anlamı ve kullanım sınırı kurulur. Bir tek doğru türetim güvenirliği, çok sayıda başarısız kanıt araması da eksikliği veya semantik geçersizliği kanıtlamaz.

### Kritik yanılgılar

- `⊢` ve `⊨` işaretlerini birbirinin yazı tipi varyantı sanmak.
- Güvenirlik ile tamlığın yönlerini ters çevirmek.
- Bir kanıt bulunca öncüllerin gerçek dünyada doğru veya argümanın sağlam olduğunu sanmak.
- Kanıt bulamayınca karşı değerleme elde edildiğini düşünmek.

### Kademeli pratik

1. Sekiz ifadeyi sentaktik/semantik olarak sınıflandırma.
2. Güvenirlik ve tamlık oklarını doğru yönde tamamlama.
3. Aynı geçerli argümanı tablo ve türetimle çözerek iki yöntemin verdiği bilgiyi karşılaştırma.
4. “Kanıt bulamadım” ve “karşı değerleme buldum” raporlarını kanıt gücü bakımından ayırma.

### Bağımsız üretim

Yeni bir argümanı hem doğal türetimle hem doğruluk tablosu/karşı değerleme yöntemiyle çöz; sonuçları `⊢` ve `⊨` ile yaz, iki yöntemin açıklayıcı ve hesaplama maliyetini karşılaştır.

### Ustalık kanıtı

- `⊢`/`⊨`, güvenirlik/tamlık ve geçerlilik/sağlamlık ayrımlarının tamamını doğru kurma.
- Aynı kanıt problemi için doğru türetim ve bağımsız semantik doğrulama.
- Başarısız kanıt aramasının kanıt gücünü doğru sınırlama.
- Yöntem seçimini yalnız kısalık değil amaç ve kanıt yüküyle gerekçelendirme.

### Gecikmeli geri çağırma

- Güvenirlik hangi oktur, tamlık hangi oktur?
- Bir türetim neden öncüllerin fiili doğruluğunu göstermez?
- Karşı değerleme ile başarısız kanıt araması arasındaki fark nedir?

## Faz C ve Faz E ile eklem noktaları

| Önceki/sonraki eşik | Faz D'deki bağlantı |
| --- | --- |
| C16 Totoloji/çelişki | D22'de `⊥` ve teorem fikrinin semantik karşılığı geri çağrılır; iki tanım özdeş sayılmaz |
| C17 Eşdeğerlik/tutarlılık | D25'te karşılıklı türetilebilirlik ve lisanslı dönüşümle karşılaştırılır |
| C18 Semantik sonuç | D20'de `⊨` ile `⊢` ayrılır, D26'da güvenirlik/tamlıkla yeniden bağlanır |
| C19 Yöntem seçimi | D24 ve D26'da tablo/türetim seçiminin kanıt yükü ve maliyeti karşılaştırılır |
| E27-E34 FOL dili | Faz D yalnız TFL kanıtı verir; niceleyici kuralları F dil/semantik temeli kurulmadan kullanılmaz |
| F38-F40 FOL kanıtı | D20-D26'daki kapsam ve alt kanıt disiplini niceleyici kısıtlarına temel olur |

## Mevcut içerikten geçiş haritası

| Mevcut içerik | Aday karşılık | Geçiş notu |
| --- | --- | --- |
| Çıkarım Kuralları I | D20-D22 | Kural ezberi kaldırılır; satır lisansı ve giriş/eleme ayrımı önce kurulur |
| Çıkarım Kuralları II ve Kısa İspatlar | D24 | İçine yanlışlıkla karışmış semantik statü içeriği Faz C'de kalır; yalnız kanıt stratejisi taşınır |
| Eşdeğerlik Kuralları I-II | C17 ve D25 | Semantik eşdeğerlik ile kanıt içi dönüşüm lisansı ayrılır |
| Doğal Türetim I | D20-D23 | İkinci bir başlangıç olmaktan çıkar; bağlaç kuralları tek sıraya yerleşir |
| Doğal Türetim II ve Reductio | D22-D24 | Reductio tek strateji gibi sunulmaz; doğrudan yollarla karşılaştırılır |
| Doğruluk Ağaçları ve Meta-Teori | D26 ve ileri seçmeli | D26 yalnız `⊢`/`⊨` köprüsünü kurar; doğruluk ağacı ve tam metateori çekirdek D'ye alınmaz |

## Aday veri ve kanıt denetleyicisi için teknik sözleşme

1. Ders kimlikleri `D20`-`D26`, sıraları `20`-`26` ve önkoşul grafiği döngüsüz olmalı.
2. Aday dersler `core/logic_phase3_stage_d.py` içinde, canlı `VISIBLE_LOGIC_LESSONS` listesinden ayrı tutulmalı.
3. Her ders en az bir tam türetim, bir eksik türetim, bir hatalı türetim ve bir bağımsız üretim görevi taşımalı.
4. Kanıt adımları düz metin değil yapılandırılmış veri olmalı: `id`, `formula`, `rule`, `citations`, `depth`, `opens`, `closes`.
5. Satır kimliği sıra numarasından ayrı ve kararlı olmalı; araya satır eklendiğinde atıflar bozulmamalı.
6. Denetleyici formül doğruluğu, kural şeması, atıf varlığı, atıf sırası, erişilebilirlik ve alt kanıt kapanışını ayrı hata kodlarıyla raporlamalı.
7. Kural doğrulaması yalnız metin eşleşmesine dayanmamalı; TFL formülleri ayrıştırılmış sözdizim ağacı üzerinden karşılaştırılmalı.
8. `→I`, `¬I`, `IP`, `∨E` ve `↔I` alt kanıt aralıklarının doğru başlangıç/son biçimini ve boşaltılan varsayımları denetlemeli.
9. Kapanmış alt kanıt iç satırına doğrudan atıf reddedilmeli; dış/üst açık kapsamdaki erişilebilir satıra atıf kabul edilmeli.
10. Son hedefe bağlı açık varsayım kalırsa kanıt tamamlanmış sayılmamalı.
11. D25 öncesinde türetilmiş kurallar ve eşdeğerlik dönüşümleri kapalı olmalı; her ders yalnız `rule_scope` içindeki kuralları etkinleştirmeli.
12. “İpucu” ilk bozuk satırı veya gereken kural ailesini gösterebilir; doğrudan eksik formülü otomatik yazmamalı.
13. Öğrenci kanıtı gönderilmeden önce taslak olarak yerel/oturumluk saklanmalı; aday aşamada canlı ilerleme modeline yazılmamalı.
14. Yetkili önizleme salt okunur olmalı; kanıt örneklerinin bütün formül, kural, atıf ve kapsam bilgilerini göstermeli.
15. D26 örnekleri aynı argümanın semantik değerlendirmesiyle bağımsız olarak çapraz doğrulanmalı.
16. Aday modül öğrenci rotasına, ilerleme kaydına, başarı yüzdesine veya mevcut ders URL'lerine bağlanmamalı.

## Ders üretim kaydı

Bu tablo Faz D'nin **aday geliştirme** durumunu gösterir; canlıya hazır olduğu anlamına gelmez.

| Ders | Sözleşme | Aday veri | Otomatik kural/sınır testi | Yetkili aşama önizlemesi |
| --- | --- | --- | --- | --- |
| D20 Kanıt Fikri, Satır Bağımlılığı ve Hedef Okuma | Hazır | Hazır | Hazır | Bekliyor |
| D21 Birleşim ve Koşul Kuralları | Hazır | Hazır | Hazır | Bekliyor |
| D22 Olumsuzlama, Alt Kanıt ve Çelişkiye İndirgeme | Hazır | Hazır | Hazır | Bekliyor |
| D23 Ayrık Bağlaç ve Çift Yönlülük Kuralları | Hazır | Hazır | Hazır | Bekliyor |
| D24 Geriye Doğru Planlama ve Kanıt Stratejisi | Hazır | Hazır | Hazır | Bekliyor |
| D25 Türetilmiş Kurallar ve Eşdeğerliklerin Lisansı | Hazır | Bekliyor | Bekliyor | Bekliyor |
| D26 Kanıt ile Semantik Geçerlilik Arasındaki İlişki | Hazır | Bekliyor | Bekliyor | Bekliyor |

## Aday geliştirme kapıları

- [x] Bölüm sınırları iki bağımsız müfredat/uygulama kaynağıyla karşılaştırıldı.
- [x] Faz C, Faz D ve Faz E/F arasındaki semantik/kanıt/niceleyici sınırı yazıldı.
- [x] Tek Fitch gösterimi ve temel kural envanteri sabitlendi.
- [x] Her dersin önkoşulu, ölçülebilir yetkinliği ve üretim kanıtı tanımlandı.
- [x] Türetilmiş kural ve eşdeğerlik dönüşümü lisansı sınırlandı.
- [x] Kanıt denetleyicisinin yapılandırılmış veri ve hata sözleşmesi yazıldı.
- [ ] Aday ders verisi yazıldı.
- [ ] Aday kanıt denetleyicisi ve sınır testleri yazıldı.
- [ ] Aday veri ve önkoşul grafiği otomatik test edildi.
- [ ] Aday içerik yalıtılmış, salt okunur yetkili önizlemede doğrulandı.
- [ ] Mevcut öğrenci rotasının ve ilerleme verisinin değişmediği regresyonla kanıtlandı.

## Canlıya alma kapıları

Aşağıdaki maddeler bütün aday rota tamamlandıktan sonra A1'den başlayarak yürütülecektir:

- [ ] En az bir mantık öğretmeni bütün D20-D26 kural örneklerini ve hata açıklamalarını inceledi.
- [ ] Gerçek başlangıç öğrencileri D20-D26'yı gözetimli pilotta tamamladı.
- [ ] Alt kanıt ve kapsam hataları için yardım metinleri pilot verisiyle düzeltildi.
- [ ] Kanıt denetleyicisinin kabul/ret kararları bağımsız referans kanıtlarla karşılaştırıldı.
- [ ] Erişilebilirlik, klavye kullanımı, küçük ekran ve uzun kanıt düzeni test edildi.
- [ ] Eski ilerleme kayıtları için geçiş ve geri alma planı onaylandı.
- [ ] Canlı görünürlük ayrıca ve bilinçli olarak etkinleştirildi.
