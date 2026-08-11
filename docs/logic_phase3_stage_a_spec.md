# Faz 3A: Akıl yürütme ve mantıksal ayrımlar

## Statü

Bu belge A aşamasının içerik sözleşmesidir. Henüz öğrenciye görünen ders verisini değiştirmez. Altı dersin tamamı akademik ve kullanıcı testi kapılarından geçtikten sonra uygulamaya alınacaktır.

11 Ağustos 2026 itibarıyla A1-A6'nın yayına kapalı aday verisi `core/logic_phase3_stage_a.py` içinde tamamlandı. Veri sözleşmesi, önkoşul sırası, alıştırma yanıtları, kaynak kimlikleri, erken biçimsel sembol kullanımı ve terminoloji ayrımları otomatik test altındadır. Mevcut 45 derslik öğrenci akışının değişmediği ayrıca doğrulanır. Yetkili inceleme ekranı `/mantik/inceleme/faz-3a/` adresindedir; ekran ilerleme verisi yazmaz ve öğrenci gezinmesinde yer almaz. İnsan içerik incelemesi, süre pilotu ve eski ilerleme kayıtlarının geçiş kararı tamamlanmadan aday veri canlı müfredata bağlanmayacaktır.

## İnceleme kaydı

| Kapı | Durum | Kanıt / sonraki iş |
| --- | --- | --- |
| Veri sözleşmesi ve önkoşul grafiği | Geçti | Otomatik testler A1-A6 sırasını ve alanları doğrular. |
| Öğrenci akışından yalıtım | Geçti | Canlı kurs 45 ders olarak kalır; aday modül öğrenci verisine bağlanmaz. |
| Yetkili, salt okunur önizleme | Geçti | Staff erişimi, mobil/masaüstü taşma ve ilerleme kancasının yokluğu doğrulandı. |
| A1 kaynak ve öğretim hizası | İlk teknik inceleme geçti | Soru, emir, yalın ünlem, bildirim ve bağlam hedefleri örnek ve ölçmeyle eşlendi. |
| A1 insan editör incelemesi | Bekliyor | Terimlerin açıklığı, örneklerin doğallığı ve görev yükü tek tek değerlendirilecek. |
| A1 süre doğrulaması | Bekliyor | 25 dakika geçici tahmindir; en az üç gerçek kullanıcı oturumuyla ölçülecek. |
| A2 kaynak ve öğretim hizası | İlk teknik inceleme geçti | Destek işlevi, gösterge sözcükleri, açıklama ayrımı, ara sonuç ve örtük öncül örnek ve ölçmeyle eşlendi. |
| A2 insan editör incelemesi | Bekliyor | Özellikle açıklama/argüman bağlamı ile örtük öncül dilinin gerçek kullanıcılarca nasıl okunduğu değerlendirilecek. |
| A2 süre doğrulaması | Bekliyor | 30 dakika geçici tahmindir; en az üç gerçek kullanıcı oturumuyla ölçülecek. |
| A3 kaynak ve öğretim hizası | İlk teknik inceleme geçti | Doğruluk, geçerlilik, sağlamlık ve destek türü karar sırası örnek, ölçme ve üretim göreviyle eşlendi. |
| A3 insan editör incelemesi | Bekliyor | “Kabul edilebilir durum” ve olasılıksal destek dilinin başlangıç öğrencisince doğru okunması değerlendirilecek. |
| A3 süre doğrulaması | Bekliyor | 30 dakika geçici tahmindir; en az üç gerçek kullanıcı oturumuyla ölçülecek. |
| A4 kaynak ve öğretim hizası | İlk teknik inceleme geçti | Kaba yüzey şeması ile biçimsel geçerlilik ayrıldı; biçim, karşı örnek ve karşı durum üretim görevinde ayrı ayrı ölçülüyor. |
| A4 insan editör incelemesi | Bekliyor | “Uygun örnekleme”, “sözcük anlamı” ve “karşı durum” ifadelerinin başlangıç öğrencisince doğru okunması değerlendirilecek. |
| A4 süre doğrulaması | Bekliyor | 30 dakika geçici tahmindir; en az üç gerçek kullanıcı oturumuyla ölçülecek. |
| A5 kaynak ve öğretim hizası | İlk teknik inceleme geçti | Standart çıkarımsal yön, yalnızca/ancak/-medikçe yapıları, koşul dışı karşıtlık kullanımı ve ters yön hatası örnek ve ölçmeyle eşlendi. |
| A5 insan editör incelemesi | Bekliyor | Türkçe örneklerin doğallığı ile “standart çıkarımsal okuma” uyarısının başlangıç öğrencisince anlaşılması değerlendirilecek. |
| A5 süre doğrulaması | Bekliyor | 35 dakika geçici tahmindir; en az üç gerçek kullanıcı oturumuyla ölçülecek. |
| A6 kaynak ve öğretim hizası | İlk teknik inceleme geçti | Kullanım/anma, nesne dili/üst dil ve sözdizimi/anlam ayrımları doğru kontrol örnekleri ile üretim görevinde ayrı ayrı ölçülüyor. |
| A6 insan editör incelemesi | Bekliyor | Tırnak kapsamı, oyuncak dil L ve “iyi kurulmuş fakat yanlış” ayrımının başlangıç öğrencisince doğru okunması değerlendirilecek. |
| A6 süre doğrulaması | Bekliyor | 30 dakika geçici tahmindir; en az üç gerçek kullanıcı oturumuyla ölçülecek. |

## Aşama amacı

Öğrenci biçimsel sembollere geçmeden önce şu ayrımları güvenilir biçimde kullanabilmelidir:

- ifade, bağlam içinde bildirim ve önerme;
- argüman, açıklama ve salt cümle dizisi;
- öncül, ara sonuç ve ana sonuç;
- doğruluk, geçerlilik, sağlamlık ve mantıksal sonuç;
- örnek, karşı örnek ve karşı durum;
- zorunlu ve yeterli koşul;
- dilin kullanımı ile dilsel ifadenin anılması;
- nesne dili ile üst dil.

## Aşama çıkış görevi

Öğrenciye daha önce görmediği kısa bir metin verilir. Öğrenci:

1. Bağlama bağlı ifadeleri açık hâle getirir.
2. Öncül, ara sonuç ve ana sonucu işaretler.
3. Argümanın geçerlilik iddiasını doğru terimlerle açıklar.
4. Geçersiz olduğunu düşünüyorsa öncülleri doğru, sonucu yanlış yapan bir durum üretir.
5. Metindeki gerekli/yeterli koşul dilini yönü koruyarak yeniden yazar.
6. Metin hakkında konuşurken kullanım ve anma işaretlerini doğru uygular.

Çıkış görevi yalnız çoktan seçmeli puanla geçilemez.

## Ortak ders sözleşmesi

Her ders şu veri alanlarını taşıyacaktır:

```text
prerequisites: Önce tamamlanması gereken ders kimlikleri
competencies: Dersin çalıştırdığı kararlı beceri kimlikleri
estimated_minutes: Hedef aktif çalışma süresi
mastery_evidence: Ustalık için gözlenecek öğrenci üretimi
review_prompts: Sonraki derslerde geri çağrılacak kısa sorular
```

Her derste tam çözülmüş örnekten sonra kısmen tamamlanmış örnek, ardından bağımsız üretim bulunacaktır.

## A1 — İfade, bağlam ve önerme

### Ders sözleşmesi

- **Tahmini süre:** 25 dakika (pilotla doğrulanacak)
- **Önkoşul:** Yok
- **Ana eşik:** Bir ifadenin tek başına dilbilgisel biçimine bakmak yerine, bağlam içinde doğru veya yanlış olabilen bir bildirim içerip içermediğini sınamak.
- **Yetkinlikler:** `claim.identify`, `context.resolve`, `proposition.distinguish`

### Öğrenme hedefleri

1. Soru, emir, yalın ünlem ve bildirim işlevlerini ayırmak.
2. Cümle ile o cümlenin bağlam içinde ifade ettiği önerme arasındaki çalışma ayrımını kullanmak.
3. `ben`, `burada`, `bugün`, `o` gibi bağlama bağlı ifadeleri değerlendirilebilir hâle getirmek.

### Akademik not

“Önerme”nin metafizik statüsü tartışmalıdır. Başlangıç dersinde bunu çözümlenmiş bir felsefi gerçek gibi sunmak yerine şu çalışma tanımı kullanılır: *Bağlam içinde bir bildirim cümlesinin doğru veya yanlış olabilen içeriği.* Bu tanım ileride Frege, Russell ve Wittgenstein tartışmalarında yeniden açılacaktır.

### Kritik yanılgılar

- Her dilbilgisel cümleyi önerme saymak.
- Bir ifadenin fiilen doğru olup olmamasını, doğru veya yanlış olabilmesiyle karıştırmak.
- Bağlama bağlı bir ifadeyi otomatik olarak anlamsız saymak.
- Farklı cümlelerin hiçbir zaman aynı içeriği ifade edemeyeceğini varsaymak.

### Kademeli pratik

- Tam örnek: “Kapıyı kapat.” neden doğruluk değeri taşıyan bildirim değildir?
- Tam örnek: “Eyvah!” ile “Eyvah, anahtarı içeride unuttum!” neden aynı mantıksal işlevde değildir?
- Yarı tamamlanmış örnek: “Bugün hava soğuk.” ifadesinin değerlendirilebilmesi için hangi bağlam bilgileri gerekir?
- Karşıt örnek: “Dünya'nın iki uydusu vardır.” yanlıştır ama yine de önerme ifade eder.

### Bağımsız üretim

Sekiz farklı ifadeyi sınıflandır; soru, emir, yalın ünlem, yanlış bildirim ve bağlama bağlı bildirimin her birini kullan. Her sınıflama için tek cümlelik gerekçe yaz. Bağlama bağlı iki ifadeyi kişi, yer ve zaman bilgisi ekleyerek açık bildirime dönüştür.

### Ustalık kanıtı

- Sınıflamada en az bir soru, emir, yalın ünlem, yanlış bildirim ve bağlama bağlı bildirim doğru gerekçelendirilmiş olmalı.
- Öğrenci “yanlış” ile “önerme değil” ayrımını açıkça kullanmalı.
- Yeniden yazılan ifadeler artık belirli bir bağlamda doğru veya yanlış değerlendirilebilir olmalı.

### Gecikmeli geri çağırma

- Yanlış bir cümle neden yine de önerme ifade edebilir?
- “Ben buradayım” ifadesini değerlendirmek için hangi bilgiler gerekir?

## A2 — Argüman, gerekçe ve sonuç

### Ders sözleşmesi

- **Tahmini süre:** 30 dakika (pilotla doğrulanacak)
- **Önkoşul:** A1
- **Ana eşik:** Cümleleri yüzey işaretleyicilerine göre değil, metindeki destek işlevlerine göre sınıflandırmak.
- **Yetkinlikler:** `argument.identify`, `argument.map`, `reason.role`

### Öğrenme hedefleri

1. Argümanı açıklama, betimleme ve salt iddia dizisinden ayırmak.
2. Öncül, ara sonuç ve ana sonucu destek yönüne göre bulmak.
3. `çünkü`, `öyleyse`, `demek ki` gibi işaretleyicileri ipucu olarak kullanıp son kararı işleve göre vermek.

### Akademik not

Argüman ile açıklama yalnız cümle kalıbından ayrılmaz. Aynı “çünkü” cümlesi, hedef olgunun doğru olup olmadığı tartışılıyorsa gerekçe; olgu zaten kabul edilip nedeni soruluyorsa açıklama işlevi görebilir. Bazı metinler iki işlevi birlikte taşıyabilir. Çözümleme, yazarın erişilemeyen psikolojik niyetini tahmin etmek yerine metinde savunulabilen destek ilişkisine dayanır.

### Kritik yanılgılar

- Paragraftaki her cümleyi öncül saymak.
- “Çünkü” içeren her metni argüman saymak.
- Bir örneği veya açıklamayı otomatik olarak ana sonuç saymak.
- Yazarın psikolojik niyetiyle metnin mantıksal yapısını karıştırmak.

### Kademeli pratik

- Tam örnek: Tek öncül ve tek sonuç içeren kısa argümanın ok şeması.
- Yarı tamamlanmış örnek: Bir ara sonucu eksik bırakılmış üç basamaklı gerekçe zinciri.
- Karşıt örnek: Bir olayın neden olduğunu açıklayan metin ile o olayın olduğuna ikna etmeye çalışan metin.

### Bağımsız üretim

Kütüphanenin sınav haftasında gece 23.00'e kadar açık kalması gerektiğini savunan verilen paragrafı numaralı yalın önermelere çevir; destek oklarını çiz; varsa ara sonuç ve ana sonucu adlandır. Açıkça yazılmamış normatif bağlantıyı yalnız gerektiği ölçüde belirt ve neden daha güçlü bir örtük öncül seçmediğini açıkla.

### Ustalık kanıtı

- Destek yönü doğru olmalı.
- Ara sonuç hem önceki cümlelerin sonucu hem sonraki sonucun desteği olarak gösterilmeli.
- Öğrenci işaretleyici sözcük bulunmayan en az bir metni işlev üzerinden çözümlemeli.

### Gecikmeli geri çağırma

- Bir cümle aynı argümanda nasıl hem sonuç hem öncül olabilir?
- Açıklama ile argümanı ayırmak için hangi soru sorulur?

## A3 — Doğruluk, geçerlilik ve sağlamlık

### Ders sözleşmesi

- **Tahmini süre:** 30 dakika (pilotla doğrulanacak)
- **Önkoşul:** A2
- **Ana eşik:** Sonucun fiilen doğru olmasına bakmadan, öncüllerin doğru ve sonucun yanlış olduğu bir durumun mümkün olup olmadığını sınamak.
- **Yetkinlikler:** `validity.evaluate`, `soundness.evaluate`, `consequence.explain`

### Öğrenme hedefleri

1. Doğruluğun önerme veya cümle içeriğine, geçerliliğin argümana yüklenen farklı özellikler olduğunu açıklamak.
2. Geçerli, sağlam ve sağlam olmayan argümanları ayırmak.
3. Mantıksal sonucu “öncüller doğruyken sonucun yanlış olamaması” üzerinden ifade etmek.

### Akademik not

Bu derste geçerlilik, hangi “durumların” hesaba katıldığı sorusunu tamamen çözmeden ilk kez kurulur. A4 biçimsel geçerlilik fikrini ekler; C ve F aşamaları “durum” kavramını değerleme ve model olarak kesinleştirir. Ayrıca Türkçede argümanın *soundness* özelliği için **sağlamlık**, bir kanıt sisteminin *soundness* metateoremi için **güvenirlik** kullanılacaktır.

### Kritik yanılgılar

- Doğru sonuçtan geçerli argüman sonucu çıkarmak.
- Yanlış bir öncül gördüğünde argümanı doğrudan geçersiz saymak.
- Sağlamlığı yalnız bütün cümlelerin doğru olması sanmak.
- Geçerliliği ikna edicilik veya olasılıkla karıştırmak.

### Kademeli pratik

- Tam örnek: Yanlış öncüllü fakat geçerli bir kategorik biçim.
- Yarı tamamlanmış örnek: Öncülleri ve sonucu doğru fakat destek ilişkisi geçersiz bir argüman.
- Karşıt örnek: Güçlü tümevarımsal destek ile tümdengelimsel geçerlilik ayrımı.

### Bağımsız üretim

Dört akıl yürütmede önce zorunlu sonuç mu, olasılıksal destek mi amaçlandığını belirle. Tümdengelimsel olanları “geçerli/geçersiz” diye sınıflandır; yalnız geçerlilik kararından sonra öncüllerin fiilî doğruluğunu inceleyerek sağlamlık kararı ver. En az bir geçerli fakat sağlam olmayan ve bir doğru sonuçlu fakat geçersiz örneği gerekçelendir.

### Ustalık kanıtı

- En az bir geçerli fakat sağlam olmayan örnek doğru açıklanmalı.
- En az bir doğru sonuçlu fakat geçersiz örnek doğru açıklanmalı.
- Geçersizlik gerekçesi, sonuçla ilgisiz bir eleştiri değil olası karşı durum fikri taşımalı.

### Gecikmeli geri çağırma

- Yanlış öncüllü bir argüman nasıl geçerli olabilir?
- Sonucun doğru olması neden tek başına geçerlilik kanıtı değildir?

## A4 — Biçim, karşı örnek ve karşı durum

### Ders sözleşmesi

- **Tahmini süre:** 30 dakika (pilotla doğrulanacak)
- **Önkoşul:** A3
- **Ana eşik:** Bir iddiayı veya argümanı çürütürken eleştirinin hedef türüne uygun tanık üretmek.
- **Yetkinlikler:** `form.abstract`, `counterexample.construct`, `countercase.construct`

### Öğrenme hedefleri

1. Birden fazla argümanın paylaştığı biçimi içerikten ayırmak.
2. Evrensel bir iddiaya karşı örnek ile tümdengelimsel argümana karşı durum arasındaki farkı kullanmak.
3. Geçersizliği, öncüllerin doğru ve sonucun yanlış olduğu tek bir durumla göstermek.

Tek bir doğal dil argümanının geçerli olması, ondan çıkarılan kaba yüzey şemasının biçimsel olarak geçerli olduğunu göstermez. Örnek, “göz doktoru” ile “doktor” arasındaki anlam bağlantısı gibi içeriksel bir nedenle başarılı olabilir. Biçimsel geçerlilik iddiası, yer tutucular uygun yeni içeriklerle doldurulduğunda da sonucun korunmasını gerektirir.

Biçimsel “karşı model” terimi, yorum ve model semantiğinin kurulacağı F aşamasına bırakılır. Bu derste öğrenci aynı fikrin doğal dildeki öncülü olan karşı durumu üretir.

Bazı mantık kitapları evrensel iddiayı çürüten örneğe de argümanın geçersizliğini gösteren duruma da “karşı örnek” der. Bu program işlem türlerini görünür kılmak için ilkine **karşı örnek**, ikincisine şimdilik **karşı durum**, model semantiği kurulduktan sonra **karşı model** diyecektir.

### Kritik yanılgılar

- Her itirazı karşı örnek diye adlandırmak.
- İddiayla ilgisiz istisna üretmek.
- Bir argümanın öncüllerinden birini yanlışlamayı geçersizlik kanıtı sanmak.
- Tek bir başarısız örnekten olasılıksal eğilimi tamamen çürüttüğünü düşünmek.

### Kademeli pratik

- Tam örnek: “Bütün kuşlar uçar” iddiasına uygun ve uygunsuz karşı örnekler.
- Yarı tamamlanmış örnek: Sonucu onaylama biçimine karşı aynı biçimli yeni içerik.
- Karşıt örnek: Evrensel iddia, olasılıksal genelleme ve tümdengelimsel argüman için farklı eleştiri araçları.

### Bağımsız üretim

Bir evrensel iddiaya gerçek karşı örnek üret. Verilen geçersiz argümanı, terimlerin tekrar ve destek rollerini koruyan yer tutucularla şemalaştır; ardından aynı biçimde öncülleri doğru, sonucu yanlış yapan kurmaca ama tutarlı bir durum üret. Neden farklı araçlar kullandığını açıkla.

### Ustalık kanıtı

- Karşı örnek hedef iddianın kapsamına gerçekten girmeli.
- Argümanın biçimi, terim tekrarlarını ve öncül-sonuç rollerini korumalı.
- Karşı durumda bütün öncüller doğru, sonuç yanlış olmalı.
- Öğrenci “öncül yanlış” ile “argüman geçersiz” eleştirilerini ayırmalı.

### Gecikmeli geri çağırma

- Geçersizliği gösteren karşı durumda hangi cümleler doğru, hangisi yanlış olmalıdır?
- Olasılıksal bir genellemeyi tek istisna her zaman çürütür mü?

## A5 — Zorunlu ve yeterli koşullar

### Ders sözleşmesi

- **Tahmini süre:** 35 dakika (pilotla doğrulanacak)
- **Önkoşul:** A3, A4
- **Ana eşik:** Koşul dilini konuşma sırasına göre değil, hangi durumun hangisini garanti ettiği veya gerektirdiğine göre yönlendirmek.
- **Yetkinlikler:** `condition.necessary`, `condition.sufficient`, `condition.direction`

### Öğrenme hedefleri

1. Yeterli koşulu sonucu garanti eden taraf, zorunlu koşulu sonuç için bulunması gereken taraf olarak okumak.
2. Koşul kuran “ise”, “yalnızca”, “ancak”, “-medikçe” yapılarında yönü gerekçelendirmek; aynı sözcüklerin koşul kurmayan kullanımlarını ayırmak.
3. Tek yönlü koşulu çift yönlü tanım gibi kullanmamak.

### Akademik not

Bu ders gerekli ve yeterli koşulları önce standart çıkarımsal okumayla öğretir: bir taraf ötekini garanti ediyorsa ilki yeterli, garanti edilen taraf ilki için zorunludur. Bu karşılıklılık doğal dildeki her koşulun nedensel, zamansal veya açıklayıcı anlamını tüketmez. “Ancak” karşıtlık, “ise” konu veya karşılaştırma işlevi de görebilir. Bu nedenle öğrenci önce cümlenin gerçekten koşul kurup kurmadığını belirler; koşul işareti B aşamasında, doğruluk işlevsel maddi koşul semantiği ise C aşamasında kurulacaktır.

### Kritik yanılgılar

- Sözcük sırasını doğrudan mantıksal yön sanmak.
- “Ancak” veya “ise” geçen her cümleyi koşul cümlesi saymak.
- Koşulun tersini otomatik doğru kabul etmek.
- Gerekli koşulu tek başına yeterli saymak.
- Gündelik nedensellik ile maddi koşulun daha sonra kurulacak biçimsel anlamını özdeş saymak.

### Kademeli pratik

- Tam örnek: Kare olmak, dörtgen olmak için yeterlidir; dörtgen olmak kare olmak için yeterli değildir.
- Yarı tamamlanmış örnek: “Yalnızca”, koşul kuran “ancak” ve “-medikçe” ile kurulmuş üç cümlede ortak gerekli koşul.
- Karşıt örnek: Koşul kuran “ancak” ile “Rapor uzundu; ancak anlaşılırdı” cümlesindeki karşıtlık kullanımı.
- Yön sınaması: Aynı iki özellik arasında tek yön ve çift yön iddiaları.

### Bağımsız üretim

Verilen altı doğal dil cümlesinde önce koşul kurulup kurulmadığını belirle. Koşul kuran beş cümleyi garanti ve gereklilik diliyle yeniden yaz; gerekli ve yeterli tarafı ayrı adlandır. Koşul kurmayan karşıtlık kullanımını gerekçesiyle ayır ve bir koşulun tersini karşı durumla çürüt.

### Ustalık kanıtı

- “Ancak/yalnızca” içeren en az iki örnekte yön doğru olmalı.
- Koşul kurmayan “ancak” kullanımı otomatik olarak şemalaştırılmamalı.
- Öğrenci tek yön ile çift yön arasındaki farkı yeni örnekle açıklamalı.
- Tersini geçersiz kılan karşı durum gerçekten ön koşulu/sonucu doğru yerlerde tutmalı.

### Gecikmeli geri çağırma

- “A yalnızca B ise” hangi yönü söyler?
- Bir cümledeki “ancak” sözcüğünün koşul mu, karşıtlık mı kurduğunu nasıl anlarsın?
- Bir koşulun tersi neden asıl koşuldan çıkmaz?

## A6 — Kullanım, anma, nesne dili ve üst dil

### Ders sözleşmesi

- **Tahmini süre:** 30 dakika (pilotla doğrulanacak)
- **Önkoşul:** A1, A3
- **Ana eşik:** Bir nesne hakkında konuşmak ile o nesneyi gösteren sözcük ya da ifade hakkında konuşmayı işaret düzeyinde ayırmak.
- **Yetkinlikler:** `language.use_mention`, `language.object_meta`, `syntax_semantics.distinguish`

### Öğrenme hedefleri

1. Bir ifadeyi kullanmak ile ifadeden söz etmek arasındaki farkı tırnak ve tipografik işaretlerle göstermek.
2. İncelenen dil ile o dili açıklayan üst dili ayırmak.
3. Bir ifadenin biçimi hakkındaki iddia ile doğruluğu/anlamı hakkındaki iddiayı karıştırmamak.

### Akademik not

Bu ders kullanım/anma ayrımını doğal dil ve iki işaretli oyuncak bir dil üzerinden ilk kez kurar. Tırnak, bu aşamada anılan ifadenin sınırını görünür kılan çalışma uzlaşımıdır; doğrudan aktarım ve ironi gibi başka tırnak işlevlerinin varlığı ayrıca belirtilir. Önermeler mantığının sözdizimi öğrenildikten sonra B aşamasında aynı ayrım formüller, üst değişkenler ve biçimsel alıntı kurallarıyla ikinci kez ele alınacaktır. Böylece öğrenci henüz tanımadığı sembollerle sınanmaz.

### Kritik yanılgılar

- Ankara'nın altı harfi olduğunu söylemek ile “Ankara” sözcüğünün altı harfi olduğunu söylemeyi karıştırmak.
- Bir ifadenin doğru olduğunu söylemek ile ifadenin belirli sayıda sözcük içerdiğini söylemeyi aynı düzeyde görmek.
- Üst dili daha “yüksek” veya daha doğru bir doğal dil sanmak.
- Tırnak işaretini yalnız vurgu amacıyla kullanmak.
- İyi kurulmamış bir işaret dizisini, doğru veya yanlış olabilen sıradan bir cümle gibi sınıflandırmak.

### Kademeli pratik

- Tam örnek: Ankara bir şehirdir; “Ankara” altı harfli bir sözcüktür.
- Yarı tamamlanmış örnek: Tek başına gösterilen `A` nesne dili cümlesi ile Türkçe üst dilde anılan “A” ifadesi.
- Karşıt örnek: İyi kurulmuş fakat yanlış bir cümle ile oyuncak dilde iyi kurulmamış bir işaret dizisi.

### Bağımsız üretim

Altı kullanım/anma örneğini değerlendir; hatalı olanları düzelt, doğru kontrol örneklerini gerekçesiyle koru. Ardından yalnız `A` ve `B` cümlelerinden oluşan oyuncak L dili için tek başına bir nesne dili satırı, iki sözdizimsel ve iki anlamsal Türkçe üst dil cümlesi üret.

### Ustalık kanıtı

- Sözcük ile gönderimde bulunduğu nesne doğru ayrılmalı.
- Öğrenci en az iki sözdizimsel ve iki anlam/doğruluk özelliği bildiren üst dil cümlesi üretmeli.
- Tırnaklar, vurgu için değil anılan ifadeyi sınırlandırmak için kullanılmalı.
- İyi kurulmuş fakat yanlış cümle, iyi kurulmamış işaret dizisinden ayrılmalı.

### Gecikmeli geri çağırma

- “Kar beyazdır.” ile “‘Kar beyazdır’ iki sözcükten oluşur.” cümlelerinde aynı söz dizisi nasıl farklı rol oynar?
- Bir ifadenin kaç sözcük içerdiğini söylemek ile ne anlama geldiğini söylemek hangi iki farklı soru türüdür?

## Mevcut içerikten geçiş haritası

| Mevcut ders | Yeni kullanım |
| --- | --- |
| Önerme Nedir? | A1'in başlangıç malzemesi; bağlam ve çalışma tanımı güçlendirilecek |
| Argüman, Öncül ve Sonuç | A2'nin çekirdeği |
| Geçerlilik ve Doğruluk | A3'ün çekirdeği; mantıksal sonuç tanımı eklenecek |
| Mantık Bağlaçları | B aşamasına taşınacak |
| Zorunlu ve Yeterli Koşul | A5'in çekirdeği |
| Geçerli Kalıplar ve Yön Hataları | A4/A5 ve D aşamasına bölünecek |
| Metin İçinde Argüman... | A2 ile paralel argüman atölyesine bölünecek |
| Karşı Örnek, Şema... | A4'ün çekirdeği; ileri metin çözümlemesi paralel atölyeye gidecek |
| Tanım ve Kavramsal Çerçeve | Paralel argüman atölyesine taşınacak |
| Yeni A6 | Kullanım/anma ve nesne/üst dil için yeni çekirdek ders |

Bu harita onaylanmadan eski ilerleme kayıtları için veri taşıma veya yönlendirme yazılmayacaktır.

## Uygulama öncesi kontrol listesi

- Her tanım, en az bir doğru örnek ve sınır örneğiyle denetlendi mi?
- “Önerme” çalışma tanımı felsefi tartışmayı kapatıyormuş gibi sunuluyor mu?
- Geçerlilik örneklerinde gerçek doğruluk ile biçim birbirine karışıyor mu?
- Karşı örnek ile karşı model terimleri tutarlı mı?
- Türkçedeki “ancak”, “yalnızca” ve “-medikçe” örnekleri doğal mı?
- Kullanım/anma örneklerinde tırnaklar erişilebilir biçimde okunuyor mu?
- Çıkış görevi, altı dersin tamamını gerçekten ölçüyor mu?
- Eski bağlantı ve ilerleme kayıtlarının geçiş planı yazıldı mı?
