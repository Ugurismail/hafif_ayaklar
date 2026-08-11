# Faz 3B: Önermeler mantığının dili

## Statü

Bu belge Faz B'nin kaynaklara dayalı **aday ders sözleşmesidir**. Aday ders verisi yalnız ayrı bir modülde tutulur ve salt okunur yetkili inceleme ekranında gösterilir; öğrenciye görünen dersleri, ilerleme kayıtlarını, URL'leri veya mevcut 45 derslik rotayı değiştirmez. Bu aşamada veri geçişi veya öğrenciye açık ders ekranı üretilmez.

Faz B yedi dersten oluşur. Önceki altı derslik taslaktaki “ayrık bağlaç, koşul ve çift yönlülük” dersi ikiye ayrılmıştır. Ayrık bağlacın kapsayıcı/dışlayıcı okuması ile koşulun yönü farklı hata türleri doğurduğundan, gerçek öğrencinin aynı oturumda iki eşiği birden aşması beklenmeyecektir.

## Kaynak ve kapsam denetimi

| Kaynak | Faz B'deki işlevi |
| --- | --- |
| [forall x: Calgary, Bölüm 4](https://forallx.openlogicproject.org/html/Ch4.html) | Biçim sayesinde geçerlilik, atomik TFL cümleleri ve geçici sembol anahtarı |
| [forall x: Calgary, Bölüm 5](https://forallx.openlogicproject.org/html/Ch5.html) | Beş doğruluk işlevsel bağlacın doğal dildeki yaklaşık karşılıkları ve çeviri uyarıları |
| [forall x: Calgary, Bölüm 6](https://forallx.openlogicproject.org/html/Ch6.html) | TFL ifadeleri, tümevarımsal cümle tanımı, ana bağlaç, kapsam ve parantez uzlaşımları |
| [forall x: Calgary, Bölüm 7](https://forallx.openlogicproject.org/html/Ch7.html) | Sözcüksel, yapısal ve kapsam belirsizliği; belirsizlik ile bulanıklık ayrımı |
| [forall x: Calgary, Bölüm 8](https://forallx.openlogicproject.org/html/Ch8.html) | Nesne dili, üst dil, kullanım/anma ve üst değişkenler |
| [MIT OCW Logic I takvimi](https://ocw.mit.edu/courses/24-241-logic-i-fall-2009/pages/calendar) | Çeviri ve doğal dil sorunlarının doğruluk tablolarından önce kurulmasına yönelik ikinci müfredat kontrolü |
| [MIT Logic I final çalışma kılavuzu](https://www.ocw.mit.edu/courses/24-241-logic-i-fall-2009/56f43731bfb2513d7b46afa10236e072_MIT24_241F09_final_study_guide.pdf) | Sembol anahtarı, sözdizimi, ana bağlaç, doğal dil kayıpları ve üretim düzeyindeki çevirinin ölçülmesi |

`forall x` bağlaçları bir bölümde toplar; bu program gerçek başlangıç öğrencisinin bilişsel yükünü azaltmak için aynı içeriği üç öğretim adımına böler. MIT dersinde sözdizimi, semantik ve çeviri aynı hafta içinde ele alınır; burada öz-ilerlemeli kullanıcı için sözdizimi Faz B'de, değerleme ve doğruluk tabloları Faz C'de tutulur.

## Aşama sınırı

Faz B yalnız **dil ve sözdizimi** öğretir:

- TFL cümle harfleri ve sembol anahtarı;
- `¬`, `∧`, `∨`, `→`, `↔` bağlaçları;
- formül kurma, çözümleme, ana bağlaç, kapsam ve parantez;
- doğal dil belirsizliğini açık okumalara ayırma;
- yeni bir metni gerekçeli biçimde sembolleştirme.

Şunlar Faz B'de öğretilmez veya ustalık ölçütü yapılmaz:

- doğruluk değeri ataması ve değerleme;
- bağlaçların karakteristik doğruluk tabloları;
- totoloji, çelişki, tutarlılık ve mantıksal eşdeğerlik testleri;
- doğruluk tablosuyla geçerlilik;
- doğal türetim kuralları;
- niceleyiciler, yüklemler ve modeller.

Bağlaçların Türkçe yaklaşık okumaları verilir; fakat resmi semantik Faz C'ye bırakılır. Böylece öğrenci bir formülü kurmayı öğrenirken henüz öğrenmediği tablo yöntemini taklit etmek zorunda kalmaz.

## Gösterim sözleşmesi

1. **Nesne dili:** Atomik TFL cümleleri büyük Latin harfleriyle yazılır: `A`, `B`, `C`; gerekirse alt indis kullanılır.
2. **Sembol anahtarı:** Her harf, belirli çalışma bağlamında tam bir bildirim cümlesine bağlanır. Harf kişi, nesne, tek sözcük veya kavram adı için kullanılmaz.
3. **Üst dil:** Belirli bir TFL ifadesinden söz ederken tırnak kullanılır: `'A ∧ B' bir TFL cümlesidir.`
4. **Üst değişken:** `𝒜` ve `ℬ`, B11'e kadar kullanılmaz. B11'de bunların TFL cümlesi değil, herhangi bir TFL cümlesinden söz eden üst dil işaretleri olduğu açıkça kurulur.
5. **Parantez:** Aday derslerde dıştaki tek parantez çifti okunabilirlik için düşürülebilir; diğer parantezler korunur. Bağlaç önceliğine dayalı sessiz kısaltma kullanılmaz.
6. **Terim:** Öğrenci ekranında “TFL cümlesi” temel terimdir. “İyi kurulmuş formül” eş anlamlı teknik terim olarak açıklanır; iyi kurulmamış dizilere “formül” denmez.
7. **Okuma işareti:** `→` doğal dildeki her nedensel, zamansal veya açıklayıcı bağı tüketmez. Faz B'de “yaklaşık biçimselleştirme” ve “kaybedilen bilgi” her koşul çevirisinde ayrıca sorulur.

Bu gösterim, eski canlı derslerde kullanılan küçük `p`, `q`, `r` harflerinden farklıdır. Değişiklik ancak insan testleri ve eski ilerleme geçişi tamamlandıktan sonra uygulanabilir; aday aşamada mevcut veri dönüştürülmez.

## Aşama amacı

Öğrenci Faz B sonunda:

1. Doğal dildeki doğruluk işlevsel yapıyı atomik bildirimlerden ayırır.
2. Tutarlı ve yeterince ayrıntılı bir sembol anahtarı kurar.
3. Beş TFL bağlacını yön, kapsam ve parantez disiplinini koruyarak kullanır.
4. Bir işaret dizisinin TFL cümlesi olup olmadığını kurucu kurallarla gerekçelendirir.
5. Ana bağlacı ve her bağlacın kapsamını çözümler.
6. Belirsiz bir cümleye tek “doğru çeviri” dayatmak yerine savunulabilir okumaları ayrı formüllerle gösterir.
7. TFL'nin vurgu, karşıtlık, nedensellik, zaman sırası ve bulanıklık gibi bilgileri kaybedebileceğini açıklar.

## Aşama çıkış görevi

Öğrenciye daha önce görmediği, altı bildirim ve kısa bir argüman içeren doğal dil metni verilir. Öğrenci:

1. Bağlam için gerekli varsayımları yazar.
2. Atomik bildirimleri çıkarıp tutarlı bir sembol anahtarı kurar.
3. Altı bildirimi TFL'de sembolleştirir.
4. En az iki karmaşık formülün oluşum ağacını veya kurucu adımlarını gösterir.
5. Her formülün ana bağlacını ve kritik kapsamını işaretler.
6. Belirsiz bir cümlenin en az iki savunulabilir okumasını ayrı formüllerle verir.
7. Sembolleştirmenin koruduğu yapı ile kaybettiği en az iki doğal dil özelliğini açıklar.
8. Bütün metni doğal dile geri okuyup sembol anahtarındaki anlam kaymalarını düzeltir.

Çıkış görevi doğruluk tablosu, geçerlilik kararı veya kanıt istemez. Yalnız çoktan seçmeli puanla geçilemez.

## Ortak ders sözleşmesi

Her aday ders şu alanları taşıyacaktır:

```text
prerequisites: Önce tamamlanması gereken aday ders kimlikleri
competencies: Dersin ölçülebilir beceri kimlikleri
estimated_minutes: Pilotla doğrulanacak aktif çalışma süresi
mastery_evidence: Öğrencinin ürettiği ve incelenebilen kanıt
review_prompts: Sonraki derslerde gecikmeli geri çağırma soruları
```

Her derste sırasıyla kısa geri çağırma, tek yeni eşik, tam çözülmüş örnek, kısmen tamamlanmış örnek, hata düzeltme ve bağımsız üretim bulunur.

## B7 — Atomik cümleler ve sembol anahtarı

### Ders sözleşmesi

- **Tahmini süre:** 30 dakika (pilotla doğrulanacak)
- **Önkoşul:** A1, A4, A6
- **Ana eşik:** Cümle harfini sözcük kısaltması veya nesne adı olarak değil, belirli bir anahtar içindeki tam atomik bildirim için kullanılan TFL cümlesi olarak kurmak.
- **Yetkinlikler:** `tfl.atomic_identify`, `tfl.key_construct`, `tfl.abstraction_explain`

### Öğrenme hedefleri

1. Doğal dilde TFL açısından atomik bırakılacak bildirimleri ayırmak.
2. Her cümle harfine tek ve tam bir bildirim bağlayan sembol anahtarı kurmak.
3. Cümle harfinin iç yapıyı görünmez kıldığını ve anahtarın yalnız o çalışma bağlamında geçerli olduğunu açıklamak.

### Akademik not

“Atomik” gündelik dilde hiçbir iç yapısı olmayan cümle demek değildir. TFL'nin izleyeceği doğruluk işlevsel bağlaçlar bakımından daha fazla parçalanmayan birimdir. “Deniz Ankara'dadır” özne-yüklem yapısı taşısa da TFL içinde `A` ile atomik bırakılabilir; bu iç yapı daha sonra birinci derece mantıkta yeniden açılır.

### Kritik yanılgılar

- `D` harfini Deniz kişisinin adı sanmak.
- “Ankara” gibi tek bir terime cümle harfi vermek.
- Bağlaçlı bütün bir paragrafı tek atomik harfle kapatıp mantıksal yapıyı silmek.
- Aynı anahtar içinde aynı harfi iki farklı bildirim için kullanmak.
- Harfin anlamını bütün dersler için kalıcı sanmak.

### Kademeli pratik

- Tam örnek: “Deniz geldi ve Ece kaldı” cümlesinden iki atomik bildirim ve `D`, `E` anahtarı çıkarma.
- Sınır örneği: “Deniz ve Ece kardeştir” ifadesinde yüzeydeki `ve`nin iki tam cümleyi bağlamadığını gösterme.
- Yarı tamamlanmış örnek: Aynı kişi hakkında üç atomik bildirime tutarlı harf seçme.
- Hata düzeltme: `A: Ankara` ve `G: geldi` anahtarını tam bildirimlerle onarma.

### Bağımsız üretim

Beş cümlelik kısa bir duyurudan TFL açısından atomik bırakılacak bildirimleri çıkar; bir sembol anahtarı kur; her seçimin neden tam cümle olduğunu açıkla. Ardından aynı harflerin başka bir problemde yeniden tanımlanabileceğini gösteren ikinci, iki satırlı anahtar yaz.

### Ustalık kanıtı

- Anahtarın her sağ tarafı tek başına doğru veya yanlış olabilen tam bildirim olmalı.
- Aynı harf aynı anahtar içinde tek anlam taşımalı.
- En az bir yüzey `ve`si doğru gerekçeyle atomik cümlenin içinde bırakılmalı.
- Öğrenci TFL atomikliğinin doğal dilde mutlak basitlik olmadığını açıklamalı.

### Gecikmeli geri çağırma

- Bir cümle harfi neden kişi adı değildir?
- Cümle harfiyle gösterilen doğal dil cümlesinin hangi yapısı kaybolur?

## B8 — Olumsuzlama ve birleşim

### Ders sözleşmesi

- **Tahmini süre:** 35 dakika (pilotla doğrulanacak)
- **Önkoşul:** B7
- **Ana eşik:** Olumsuzlamanın kapsamını ve birleşimin iki cümle bileşenini yüzeydeki sözcük sırasına güvenmeden belirlemek.
- **Yetkinlikler:** `tfl.negation_scope`, `tfl.conjunction_build`, `tfl.component_recover`

### Öğrenme hedefleri

1. `¬A` ile `¬(A ∧ B)` yapılarını ayrı okumak.
2. `A ∧ B` formülünü iki TFL cümlesinden kurmak ve doğal dile geri çevirmek.
3. Türkçedeki `ve`, `ama`, `fakat`, `hem ... hem ...` yapılarının hangi bilgilerini `∧`nin koruyup hangilerini kaybettiğini belirtmek.

### Akademik not

`∧`, “ama”nın karşıtlık vurgusunu ve olayların zaman sırasını kodlamaz. “Ayağa kalktı ve konuştu” cümlesi bazı bağlamlarda sıralı olay anlatır; onu `A ∧ K` biçiminde göstermek yalnız iki bildirimin birlikte ileri sürüldüğü kısmı korur. Bu kayıp açıkça belirtilmeden çeviri “tam eş anlamlılık” diye sunulmaz.

### Kritik yanılgılar

- Her `ve` sözcüğünü otomatik `∧` yapmak.
- `¬A ∧ B` ile `¬(A ∧ B)`yi aynı okumak.
- “İkisi de değil” ile “ikisi birden değil” ayrımını silmek.
- “Mutsuz” sözcüğünü her bağlamda “mutlu değil” ile özdeş saymak.
- Parantezi yalnız görsel süs sanmak.

### Kademeli pratik

- Tam örnek: “Ada gelmedi ama Bora geldi” → `¬A ∧ B`; karşıtlık tonunun kaybedildiğini not etme.
- Tam örnek: “Ada ile Bora'nın ikisinin de geldiği doğru değil” → `¬(A ∧ B)`.
- Yarı tamamlanmış örnek: “Ada ne sessiz ne sakindir” için önce iki atomik bildirim çıkarma, ardından kapsamı kurma.
- Sınır örneği: “Ada ve Bora kardeştir” cümlesini otomatik iki TFL cümlesine bölmeme.

### Bağımsız üretim

Olumsuzlama ile birleşimin farklı kapsamlarını kullanan dört doğal dil cümlesi yaz ve sembolleştir: `¬A ∧ B`, `A ∧ ¬B`, `¬(A ∧ B)` ve `¬A ∧ ¬B`. Her biri için geri çeviri ve bir önceki biçimden fark açıklaması ekle.

### Ustalık kanıtı

- Dört hedef yapının tamamı farklı doğal dil okumalarıyla eşlenmeli.
- Atomik bileşenler sembol anahtarında tam cümle olmalı.
- En az bir örnekte `ama/fakat` vurgusunun TFL'de kaybolduğu söylenmeli.
- Kapsam farkı parantez ve ana dildeki yeniden yazımla gerekçelendirilmeli.

### Gecikmeli geri çağırma

- `¬A ∧ B` ile `¬(A ∧ B)` arasındaki kapsam farkı nedir?
- Her `ve` neden iki TFL cümlesini birleştirmez?

## B9 — Ayrık bağlaç ve dışlayıcı okuma

### Ders sözleşmesi

- **Tahmini süre:** 30 dakika (pilotla doğrulanacak)
- **Önkoşul:** B8
- **Ana eşik:** `∨` bağlacını standart kapsayıcı okuma ile kullanmak; dışlayıcılığı doğal dil bağlamından varsaymak yerine ayrıca formülleştirmek.
- **Yetkinlikler:** `tfl.disjunction_build`, `tfl.exclusive_or_construct`, `tfl.neither_nor_scope`

### Öğrenme hedefleri

1. Kapsayıcı `A ∨ B` ile dışlayıcı “ya A ya B, fakat ikisi birden değil” okumasını ayırmak.
2. Dışlayıcı okumayı `(A ∨ B) ∧ ¬(A ∧ B)` biçiminde kurmak.
3. `ne ... ne ...`, “en az biri” ve çoklu seçenek cümlelerinde bileşen sınırlarını korumak.

### Akademik not

Gündelik Türkçede `ya ... ya ...` bağlama göre kapsayıcı veya dışlayıcı olabilir. TFL'de yalın `∨` kapsayıcıdır. Öğrenciye gündelik cümlenin tek zorunlu okuması varmış gibi davranmak yerine hangi ek bağlamın dışlayıcılığı desteklediği sorulur.

### Kritik yanılgılar

- `∨`yi “tam olarak biri” diye ezberlemek.
- Dışlayıcı okuma için `A ∨ B`yi tek başına yeterli saymak.
- “Ne A ne B”yi `¬A ∨ ¬B` yapmak.
- Üç seçenekli ayrığı parantezsiz ve ana bağlacı belirsiz bırakmak.

### Kademeli pratik

- Tam örnek: “Çorba veya salata alabilirsin; ikisini de alabilirsin” → kapsayıcı `C ∨ S`.
- Tam örnek: “Dosya ya kabul edildi ya reddedildi; ikisi birden olamaz” → dışlayıcı yapı.
- Yarı tamamlanmış örnek: “Ne Deniz ne Ece geldi” ifadesinde iki olumsuzlamayı doğru yerleştirme.
- Bağlam karşılaştırması: Menü seçimi ile “mesaj e-posta veya uygulama üzerinden gelir” cümlelerinde dışlayıcılık kanıtını tartışma.

### Bağımsız üretim

Aynı `A`, `B`, `C` anahtarıyla kapsayıcı iki seçenek, dışlayıcı iki seçenek, hiçbir seçeneğin gerçekleşmediği durum ve üç seçenekten en az birinin gerçekleştiği durum için dört ayrı formül kur. Her formülün Türkçe geri okumasını yaz.

### Ustalık kanıtı

- Kapsayıcı ve dışlayıcı okumalar formülde açıkça ayrılmalı.
- Dışlayıcı formülde hem en az bir taraf hem birlikte olmama bileşeni bulunmalı.
- “Ne ... ne ...” örneğinde her iki bileşen de kapsam içinde olmalı.
- Parantezler farklı okumalara izin vermeyecek biçimde kullanılmalı.

### Gecikmeli geri çağırma

- `A ∨ B` iki tarafın birlikte doğru olmasını dışlar mı?
- Dışlayıcı “veya”yı yalnız `¬(A ∧ B)` ile göstermek neden yetmez?

## B10 — Koşul, yalnızca, çift yönlülük ve “-medikçe”

### Ders sözleşmesi

- **Tahmini süre:** 40 dakika (pilotla doğrulanacak)
- **Önkoşul:** A5, B9
- **Ana eşik:** Doğal dildeki koşulun yönünü garanti/gereklilik üzerinden kurmak ve tek yönlü `→` ile çift yönlü `↔`yi ayırmak.
- **Yetkinlikler:** `tfl.conditional_direction`, `tfl.biconditional_construct`, `tfl.unless_translate`

### Öğrenme hedefleri

1. “A ise B” ve “A yalnızca B ise” cümlelerinin yönünü doğru sembolleştirmek.
2. `A ↔ B`yi iki yönlü koşul olarak açmak.
3. “B olmadıkça A olmaz” gibi yapıları açık Türkçe yeniden yazımdan sonra sembolleştirmek.
4. Maddi koşulun nedensellik, açıklama, söz verme ve zaman sırasını tek başına kodlamadığını belirtmek.

### Akademik not

Bu ders A5'teki gerekli/yeterli koşul yönünü geri çağırır; `→` işaretini henüz doğruluk tablosuyla tanımlamaz. “Maddi koşul” terimi, resmi doğruluk koşulunun Faz C'de verileceği açıkça belirtilerek tanıtılır. `-medikçe` cümlelerinde standart TFL okuması öğretilebilir; fakat konuşma bağlamının dışlayıcılık veya çift yönlülük ima edebileceği ayrıca işaretlenir.

### Kritik yanılgılar

- Ok işaretini cümledeki sözcük sırasına göre çizmek.
- “Yalnızca”dan sonraki parçayı yeterli koşul saymak.
- Tek yönlü koşulu otomatik `↔` yapmak.
- `A ↔ B`yi `A → B`nin süslü yazımı sanmak.
- Koşulu nedensellik oku gibi yorumlamak.
- “-medikçe”nin her bağlamda tek ve tartışmasız okuması olduğunu varsaymak.

### Kademeli pratik

- Tam örnek: “Kart geçerliyse kapı açılır” → `K → A`.
- Tam örnek: “Kapı yalnızca kart geçerliyse açılır” → `A → K`.
- Tam örnek: “Sayı çifttir ancak ve ancak 2'ye kalansız bölünür” → `C ↔ B`.
- Yarı tamamlanmış örnek: “Şifre girilmedikçe hesap açılmaz” cümlesini önce koşul Türkçesine dönüştürme.
- Kayıp bilgi örneği: “Düğmeye basınca zil çaldı” ifadesinde zaman ve nedensellik bilgisinin yalın `B → Z` ile korunmadığını gösterme.

### Bağımsız üretim

Altı cümlelik bir erişim kuralı metni için anahtar ve formüller kur: düz koşul, `yalnızca`, gerekli koşul, yeterli koşul, çift yönlülük ve `-medikçe` örneklerinin her biri bulunmalı. Her cümlenin yönünü garanti/gereklilik diliyle gerekçelendir ve en az bir formülde kaybolan doğal dil bilgisini yaz.

### Ustalık kanıtı

- Altı koşul türünün yönü gerekçeyle doğru kurulmalı.
- `↔` iki ayrı `→` yönüyle açılabilmeli.
- “-medikçe” cümlesi açık ara cümleye dönüştürülmeden doğrudan sembol eşleştirmesi yapılmamalı.
- Öğrenci `→` ile nedensellik arasında özdeşlik kurmamalı.

### Gecikmeli geri çağırma

- “A yalnızca B ise” hangi koşul yönünü verir?
- `A ↔ B`, hangi iki tek yönlü koşulu birlikte ileri sürer?
- Bir koşul formülü doğal dildeki hangi bilgileri kaybedebilir?

## B11 — TFL cümlesi, ana bağlaç ve kapsam

### Ders sözleşmesi

- **Tahmini süre:** 40 dakika (pilotla doğrulanacak)
- **Önkoşul:** A6, B10
- **Ana eşik:** Bir işaret dizisini görünüşe göre değil, TFL'nin kurucu kurallarıyla cümle olarak tanımak ve yapısını atomik cümlelere kadar çözmek.
- **Yetkinlikler:** `tfl.wff_verify`, `tfl.main_connective`, `tfl.scope_parse`, `metalanguage.metavariable_use`

### Öğrenme hedefleri

1. TFL ifadesi ile TFL cümlesini ayırmak.
2. TFL cümlelerinin tümevarımsal kurucu tanımını uygulamak.
3. Ana bağlacı, doğrudan alt cümleleri ve bağlaç kapsamlarını bulmak.
4. Nesne dilindeki `A` ile üst dilde herhangi bir TFL cümlesini temsil eden `𝒜`yı ayırmak.

### Akademik not

Kurucu tanım “iyi görünen dizileri” listelemek yerine bütün ve yalnız TFL cümlelerini üretmeyi amaçlar. `𝒜` ve `ℬ` üst değişkendir; TFL alfabesinin atomik cümleleri değildir. Böylece A6'daki nesne dili/üst dil ayrımı ilk kez gerçek biçimsel dil üzerinde yeniden kullanılır.

### Kritik yanılgılar

- TFL sembollerinden oluşan her diziyi TFL cümlesi saymak.
- Ana bağlacı soldan görülen ilk bağlaç sanmak.
- Dış parantezi düşürme iznini iç parantezleri de silme izni saymak.
- `A → B → C` gibi belirsiz dizileri uzlaşımla kabul etmek.
- `𝒜`yı sembol anahtarındaki yeni bir atomik cümle sanmak.

### Kademeli pratik

- Tam örnek: `¬(A ∧ B)` formülünü kurucu adımlarla `A`, `B`, `A ∧ B`, `¬(A ∧ B)` biçiminde oluşturma.
- Tam örnek: `(A ∨ B) → ¬C` formülünde ana bağlacı ve doğrudan alt cümleleri bulma.
- Yarı tamamlanmış örnek: Bir eksik parantezli ve bir yanlış bağlaç dizisini kurucu tanımla düzeltme.
- Üst dil karşılaştırması: `'A' TFL'nin atomik cümlesidir` ile `𝒜 herhangi bir TFL cümlesi için üst değişkendir` ayrımı.

### Bağımsız üretim

Sekiz işaret dizisini “TFL cümlesi / yalnız TFL ifadesi” diye sınıflandır ve her karar için hangi kurucu kuralın uygulanabildiğini veya nerede tıkandığını göster. Geçerli iki karmaşık cümlenin oluşum ağacını çiz; ana bağlacı ve bütün bağlaç kapsamlarını işaretle.

### Ustalık kanıtı

- Kararlar yalnız dengeli parantez sayımına değil kurucu kurallara dayanmalı.
- En az iki karmaşık cümle atomik yapraklara kadar doğru ayrıştırılmalı.
- Ana bağlaç ile en soldaki bağlaç en az bir örnekte doğru ayrılmalı.
- Nesne dili harfleri ile üst değişkenler açıkça ayrılmalı.

### Gecikmeli geri çağırma

- TFL sembollerinden oluşan her ifade neden TFL cümlesi değildir?
- Ana bağlaç hangi kurucu adımı gösterir?
- `A` ile `𝒜` hangi iki dil düzeyinde görev yapar?

## B12 — Belirsizlik, bulanıklık ve savunulabilir okumalar

### Ders sözleşmesi

- **Tahmini süre:** 35 dakika (pilotla doğrulanacak)
- **Önkoşul:** B11
- **Ana eşik:** Belirsiz doğal dil cümlesine tek formül dayatmak yerine her savunulabilir okumayı açık yeniden yazım ve ayrı formülle göstermek.
- **Yetkinlikler:** `language.ambiguity_detect`, `language.reading_disambiguate`, `tfl.multiple_symbolizations`, `language.vagueness_distinguish`

### Öğrenme hedefleri

1. Sözcüksel, yapısal ve kapsam belirsizliğini örneklerde ayırmak.
2. Belirsizlik ile bulanıklığı aynı sorun sanmamak.
3. Bir cümlenin farklı okumalarını açık Türkçe ara cümlelere ve ayrı TFL formüllerine dönüştürmek.
4. Bağlamın bir okumayı desteklemesi ile diğer okumanın dilbilgisel olarak imkânsız olması arasındaki farkı açıklamak.

### Akademik not

Biçimsel dilin yapısal belirsizliği kaldırması, doğal dil yorumunu otomatik olarak çözmez. Öğrenci önce okumaları belirler; TFL ancak seçilen okumayı açıklaştırır. Bulanık bir yüklemin sınır vakaları ise parantez ekleyerek çözülmez ve klasik TFL'nin iki değerli çerçevesinde kayıp yaratır.

### Kritik yanılgılar

- En olası okumayı tek mantıksal olarak mümkün okuma saymak.
- Belirsizliği yazım hatası veya bilgisizlikle özdeşleştirmek.
- Bulanık “uzun”, “zengin”, “genç” yüklemlerini kapsam paranteziyle çözmeye çalışmak.
- Farklı formülleri açıklayan farklı Türkçe ara okumalar vermemek.
- Sembolleştirmenin yazarın gerçek niyetini kanıtladığını düşünmek.

### Kademeli pratik

- Tam örnek: “Film uzun ve sıkıcı değil” cümlesinin `¬(U ∧ S)` ile `U ∧ ¬S` okumaları.
- Tam örnek: “Küçük ve tehlikeli veya hızlı bir hayvan” cümlesinde iki kapsam okuması.
- Sözcüksel örnek: “Kazı gördüm” cümlesinde kazı çalışması ve belirli kaz okumaları için iki farklı anahtar.
- Bulanıklık karşıtı: “Ece uzundur” cümlesindeki sınır sorununun iki parantezleme ile çözülmemesi.

### Bağımsız üretim

Üç belirsiz cümle için olası okumaları açık Türkçeyle yaz, her okuma için ortak veya gerektiğinde farklı sembol anahtarı kur ve ayrı formüller üret. Bir bulanık cümleyi ayrıca seçerek neden aynı yöntemle “çözülemeyeceğini” açıkla. Son olarak bağlam ekleyip hangi okumanın neden öne çıktığını belirt.

### Ustalık kanıtı

- En az iki yapısal/kapsam belirsizliği iki doğru ve farklı formülle gösterilmeli.
- Her formülün karşılığı olan açık Türkçe okuma bulunmalı.
- Bulanıklık, çok anlamlılık ve kapsam belirsizliği karıştırılmamalı.
- Öğrenci bağlam desteğini mantıksal zorunluluk diye sunmamalı.

### Gecikmeli geri çağırma

- Biçimsel dil belirsizliği hangi aşamada giderir, hangi aşamada gidermez?
- Bulanıklık neden yalnız yeni parantez ekleyerek çözülemez?

## B13 — Kademeli sembolleştirme atölyesi

### Ders sözleşmesi

- **Tahmini süre:** 50 dakika (pilotla doğrulanacak)
- **Önkoşul:** B7-B12
- **Ana eşik:** Hazır anahtar veya seçenek olmadan yeni bir doğal dil metnini analiz etmek, sembolleştirmek, yapısal olarak doğrulamak ve kayıplarını açıklamak.
- **Yetkinlikler:** `tfl.translation_plan`, `tfl.translation_produce`, `tfl.translation_audit`, `tfl.loss_explain`

### Öğrenme hedefleri

1. Bağlamı belirleme, atomları çıkarma, anahtar kurma, açık ara cümle yazma, formül kurma ve geri okuma adımlarını bağımsız yürütmek.
2. Karmaşık cümleyi ana bağlaçtan başlayarak dıştan içe çözmek.
3. Formülü kurucu kurallarla doğrulamak ve alternatif okumaları gerekçelendirmek.
4. Sembolleştirmenin koruduğu mantıksal yapı ile kaybettiği doğal dil bilgisini raporlamak.

### Akademik not

Atölye bir sembol eşleştirme testi değildir. Öğrencinin ürettiği anahtar, ara yeniden yazımlar ve gerekçeler değerlendirme nesnesidir. Aynı doğal dil cümlesi için bağlama bağlı birden fazla savunulabilir cevap bulunabilir; rubrik yalnız tek diziyi değil okuma-formül uyumunu ölçer.

### Kritik yanılgılar

- Sembolleri anahtar yazmadan kullanmak.
- Cümleyi soldan sağa sözcük sözcük çevirmek.
- Ana bağlacı bulmadan parantez yerleştirmek.
- Formülü geri okumadan teslim etmek.
- Her ayrıntının TFL'de korunabildiğini varsaymak.
- Alternatif doğru okumayı cevap anahtarına uymadığı için yanlış saymak.

### Kademeli pratik

- Tam örnek: Üç cümlelik bir erişim politikasını adım adım anahtar ve formüle dönüştürme.
- Yarı tamamlanmış örnek: Atomları verilmiş fakat ana bağlacı ve parantezleri eksik kısa paragraf.
- Hata kliniği: Aynı metin için tutarsız harf, yanlış `yalnızca` yönü ve kayıp parantez içeren üç öğrenci çözümünü onarma.
- Karşılaştırmalı okuma: Aynı belirsiz cümlenin iki savunulabilir çözümünü rubrikle değerlendirme.

### Bağımsız üretim

Aşama çıkış görevini tamamla. Formüllerin yanında çözüm günlüğü tut: bağlam varsayımı, atomik bildirimler, anahtar, açık ara okumalar, formüller, ana bağlaç/kapsam denetimi, geri çeviri ve kayıp bilgi notu.

### Ustalık kanıtı

- Sembol anahtarı tutarlı, tam cümlelerden oluşmalı ve gereksiz atom üretmemeli.
- Bütün formüller B11'in kurucu kurallarına göre TFL cümlesi olmalı.
- Koşul yönü, kapsam ve dışlayıcılık kararları gerekçelendirilmiş olmalı.
- En az bir belirsizlik iki savunulabilir okumayla gösterilmeli.
- En az iki doğal dil kaybı doğru adlandırılmalı.
- Geri çeviri, öğrencinin amaçladığı okumayla uyuşmalı.

### Gecikmeli geri çağırma

- Bir sembolleştirme çözümünü teslim etmeden önce hangi yedi denetimi yaparsın?
- İki farklı formül hangi koşulda aynı doğal dil cümlesi için birlikte savunulabilir olabilir?

## Mevcut içerikten geçiş haritası

| Mevcut canlı ders | Aday kullanımı |
| --- | --- |
| Sembolleştirmeye Giriş | B7'nin başlangıç malzemesi; kişi/terim/cümle ayrımı ve geçici anahtar güçlendirilecek |
| Olumsuzlama ve Birleşim | B8'in çekirdeği; biçimsel semantik iddiaları Faz C'ye ayrılacak |
| Ayrık Bağlaç, Koşul ve Çift Yönlülük | B9 ve B10'a bölünecek |
| Doğruluk Tabloları I | Faz C'ye taşınacak; B11 için yalnız ana bağlaç/parantez malzemesi yeniden yazılacak |
| Doğruluk Tabloları II ve Geçerlilik | Faz C'ye taşınacak |
| Eşdeğerlik Kuralları I-II | Faz C ve D arasında semantik eşdeğerlik ile türetim lisansı olarak ayrılacak |
| A6 Kullanım/Anma | B11'de TFL nesne dili ve üst değişkenler üzerinde gecikmeli geri çağrılacak |

Eski URL, ilerleme ve ders kimliklerinin hangi aday derse taşınacağı, bütün rota tamamlanmadan belirlenmeyecektir.

## Ders üretim kaydı

Bu tablo Faz B'nin **aday geliştirme** durumunu gösterir; canlıya hazır olduğu anlamına gelmez. B7-B13 kendi içerik ve sınır testlerinden geçmiş, birlikte salt okunur yetkili önizlemede açılmıştır. İnsan incelemesi ve canlıya alma kapıları aşağıda ayrıca kapalıdır.

| Ders | Aday veri | Otomatik sınır testi | Yetkili aşama önizlemesi |
| --- | --- | --- | --- |
| B7 Atomik TFL Cümleleri ve Sembol Anahtarı | Hazır | Hazır | Hazır |
| B8 Olumsuzlama ve Birleşim | Hazır | Hazır | Hazır |
| B9 Ayrık Bağlaç ve Dışlayıcı Okuma | Hazır | Hazır | Hazır |
| B10 Koşul, Yalnızca, Çift Yönlülük ve “-medikçe” | Hazır | Hazır | Hazır |
| B11 TFL Cümlesi, Ana Bağlaç ve Kapsam | Hazır | Hazır | Hazır |
| B12 Belirsizlik, Bulanıklık ve Savunulabilir Okuma | Hazır | Hazır | Hazır |
| B13 Kademeli Sembolleştirme Atölyesi | Hazır | Hazır | Hazır |

## Aday geliştirme kapıları

- [x] Bölüm sınırları iki bağımsız müfredatla karşılaştırıldı.
- [x] Faz B ile Faz C arasındaki sözdizimi/semantik sınırı yazıldı.
- [x] Her dersin önkoşulu, ölçülebilir yetkinliği ve üretim kanıtı tanımlandı.
- [x] Türkçe doğal dil işaretlerinin mekanik sembol eşleştirmesine indirgenmemesi sözleşmeye bağlandı.
- [x] Aday ders verisi yazıldı.
- [x] Aday veri ve önkoşul grafiği otomatik test edildi.
- [x] Aday içerik yalıtılmış, salt okunur yetkili önizlemede doğrulandı.
- [x] Mevcut öğrenci rotasının ve ilerleme verisinin değişmediği regresyonla kanıtlandı.

## Canlıya alma kapıları

Aşağıdaki maddeler bütün aday rota tamamlandıktan sonra A1'den başlayarak yürütülecektir:

- [ ] Mantık/felsefe uzmanı dersleri ve cevapları tek tek inceledi.
- [ ] Türkçe editörü bütün örneklerin doğallığını ve koşul yönlerini denetledi.
- [ ] Konuyu bilmeyen kullanıcılarla sesli düşünme testi yapıldı.
- [ ] Farklı ön bilgi düzeylerinden küçük grupla aşama pilotu yapıldı.
- [ ] Ders süreleri gerçek oturumlarla ölçüldü.
- [ ] Klavye, ekran okuyucu, mobil ve masaüstü akışları doğrulandı.
- [ ] A1'den son projeye kadar uçtan uca öğrenme denetimi tamamlandı.
- [ ] Eski ilerleme verisi için açık geçiş ve geri dönüş planı onaylandı.

Bu kapılar tamamlanmadan Faz B canlı ders verisine bağlanmayacaktır.
