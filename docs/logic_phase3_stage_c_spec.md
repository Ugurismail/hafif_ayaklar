# Faz 3C: Önermeler mantığının semantiği

## Statü

Bu belge Faz C'nin kaynaklara dayalı **aday ders sözleşmesidir**. Kaynak, kapsam, gösterim, ölçme ve ders sınırları sabitlenmiştir. C14-C15 aday verisi ile bunları bağımsız doğrulayan tek-değerleme ve tam-tablo semantik çekirdeği hazırlanmıştır; C16-C19 aday verisi, etkileşimli tablo uygulaması, Faz C yetkili önizlemesi ve öğrenciye açık ekran henüz üretilmemiştir.

Faz C altı dersten oluşur. Mevcut canlı rotada iki derse sıkışan doğruluk tablosu içeriği burada altı ayrı öğrenme eşiğine bölünür: tek değerleme altında hesaplama, bütün değerlemeleri listeleme, tek cümleyi sınıflandırma, cümleler arasındaki semantik ilişkileri sınama, argüman geçerliliği ve son olarak hedefli/kısmi tablolar ile TFL'nin sınırları.

Bu belge öğrenciye görünen 45 derslik rotayı, ilerleme kayıtlarını, URL'leri veya mevcut veri modelini değiştirmez.

## Kaynak ve kapsam denetimi

| Kaynak | Faz C'deki işlevi |
| --- | --- |
| [forall x: Calgary, Bölüm 8](https://forallx.openlogicproject.org/html/Ch8.html) | Nesne dili, üst dil, kullanım/anma ve üst değişken ayrımının C16-C18'de geri çağrılması |
| [forall x: Calgary, Bölüm 9](https://forallx.openlogicproject.org/html/Ch9.html) | Beş TFL bağlacının karakteristik doğruluk tabloları; kapsayıcı ayrık bağlaç ve maddi koşul |
| [forall x: Calgary, Bölüm 10](https://forallx.openlogicproject.org/html/Ch10.html) | Doğruluk işlevselliği, sembolleştirme ile tam çeviri arasındaki fark ve maddi koşulun sınırları |
| [forall x: Calgary, Bölüm 11](https://forallx.openlogicproject.org/html/Ch11.html) | Değerleme, tam doğruluk tablosu, `2^n` satır düzeni, alt cümleler ve ana bağlaç sütunu |
| [forall x: Calgary, Bölüm 12](https://forallx.openlogicproject.org/html/Ch12.html) | Totoloji, çelişki, eşdeğerlik, ortak doyurulabilirlik, semantik sonuç ve `⊨` |
| [forall x: Calgary, Bölüm 13](https://forallx.openlogicproject.org/html/Ch13.html) | TFL'nin iç yapı, bulanıklık, maddi koşul ve doğruluk işlevselliğinden doğan ifade sınırları |
| [forall x: Calgary, Bölüm 14](https://forallx.openlogicproject.org/html/Ch14.html) | Tam satır uzayını koruyan güvenli doğruluk tablosu kısaltmaları |
| [forall x: Calgary, Bölüm 15](https://forallx.openlogicproject.org/html/Ch15.html) | Tek değerlemelik kısmi tablolar ve varlık/yokluk iddialarındaki kanıt yükü asimetrisi |
| [MIT OCW Logic I takvimi](https://ocw.mit.edu/courses/24-241-logic-i-fall-2009/pages/calendar/) | Doğruluk işlevselliği, tablo, mantıksal özellik ve geçerliliğin türetimlerden önce ayrı basamaklarda kurulmasına yönelik ikinci müfredat kontrolü |
| [MIT Logic I final çalışma kılavuzu](https://www.ocw.mit.edu/courses/24-241-logic-i-fall-2009/56f43731bfb2513d7b46afa10236e072_MIT24_241F09_final_study_guide.pdf) | Değer ataması, tablo üretimi, tek cümle ve cümle kümelerinin semantik özellikleri ile geçerliliğin ayrı ölçülmesi |

`forall x`, karakteristik tabloları değerlemeden hemen önce verir; sonra tam tabloları, semantik kavramları, ifade sınırlarını ve kısmi tabloları ayrı bölümlere ayırır. MIT Logic I de doğruluk işlevselliği ve TFL semantiğini, mantıksal özellikleri ve geçerliliği türetim sisteminden önce ayrı derslerde işler. Faz C bu ortak sırayı korur; ancak gerçek başlangıç öğrencisinin “tek değerleme”, “bütün değerlemeler”, “tek cümlenin statüsü”, “cümle kümesinin statüsü” ve “argüman ilişkisi” düzeylerini birbirine karıştırmaması için daha ince basamaklandırır.

## Aşama sınırı

Faz C yalnız **klasik iki değerli TFL semantiğini** öğretir:

- `T` ve `F` doğruluk değerleri;
- değerlemeler ve doğruluk işlevleri;
- beş TFL bağlacının karakteristik doğruluk koşulları;
- tek bir değerleme altında bileşik TFL cümlesinin değerini hesaplama;
- tam doğruluk tablosu üretme;
- totoloji, çelişki ve olumsallık;
- mantıksal eşdeğerlik ve ortak doyurulabilirlik/tutarlılık;
- semantik sonuç, geçerlilik ve karşı değerleme;
- güvenli tablo kısaltmaları ve tek satırlık kısmi tablolar;
- TFL ile sembolleştirmenin ifade sınırları.

Şunlar Faz C'de öğretilmez veya ustalık ölçütü yapılmaz:

- doğal türetim, çıkarım kuralları ve kanıt satırları;
- `⊢`, alt kanıt, varsayım boşaltma, reductio, güvenirlik veya tamlık;
- eşdeğerlikleri kanıt içinde yeniden yazma lisansı;
- doğruluk ağaçları, normal biçimler veya doğruluk işlevsel tamlık;
- niceleyiciler, yüklemler, birey alanları ve birinci derece modeller;
- çok değerli, bulanık, modal, zamansal veya karşıolgusal mantıkların teknik semantiği.

C17'de semantik eşdeğerlik yalnız aynı değerleme davranışı olarak sınanır. Bir eşdeğerliği kanıt satırında dönüşüm lisansı olarak kullanmak D25'e bırakılır. C18'de `⊨` tanıtılır; `⊢` ise D aşamasına kadar görünmez. Böylece semantik sonuç ile türetilebilirlik daha öğrenilmeden aynı işaret ailesi altında birleştirilmez.

## Gösterim ve terim sözleşmesi

1. **Doğruluk değerleri:** Öğrenci ekranında `Doğru (T)` ve `Yanlış (F)` birlikte gösterilir. `T` ile `F`, doğruluk değerlerinin üst dildeki kısaltmalarıdır; TFL cümle harfi veya TFL'nin nesne dili sabitleri değildir.
2. **Değerleme:** `v`, TFL cümle harflerine doğruluk değeri atayan üst dil aracıdır. `v(A)=T` yazımı “`v` değerlemesi `A` cümlesini doğru kılar” diye okunur.
3. **Üst değişken:** `𝒜` ve `ℬ`, herhangi bir TFL cümlesinden söz eden üst değişkenlerdir. Bunlar TFL cümle harfi değildir.
4. **Cümle değeri:** `v(𝒜)=T` ifadesi, belirli bir değerleme altında belirli bir TFL cümlesinin doğru olduğunu söyler. Bu, `𝒜`nın totoloji olduğunu söylemez.
5. **Totoloji:** “Totoloji (tautology)” ilk kullanımda iki adla verilir; sonrasında “totoloji” kullanılır. Bir TFL cümlesi ancak her değerlemede doğruysa totolojidir.
6. **Çelişki ve tutarsızlık:** “Çelişki” tek TFL cümlesinin her değerlemede yanlış olmasına ayrılır. Birden çok cümle için birincil teknik terim “birlikte doyurulamaz”dır; “semantik olarak tutarsız” eş anlamlı açıklama olarak verilir.
7. **Olumsallık:** Bir TFL cümlesi en az bir değerlemede doğru ve en az bir değerlemede yanlışsa olumsaldır.
8. **Eşdeğerlik:** C17'de `𝒜` ile `ℬ`nin mantıksal eşdeğer olduğu sözel olarak yazılır. Yeni bir `≡` işareti kullanılmaz; böylece üst dildeki eşdeğerlik iddiası, nesne dilindeki `𝒜 ↔ ℬ` cümlesiyle karıştırılmaz.
9. **Semantik sonuç:** `𝒜₁, ..., 𝒜ₙ ⊨ 𝒞`, bütün soldaki cümleleri doğru ve `𝒞`yi yanlış yapan hiçbir değerleme olmadığını söyleyen üst dil ifadesidir. `⊨` TFL'nin bir bağlacı değildir.
10. **Karşı değerleme:** Bütün öncülleri doğru, sonucu yanlış yapan değerlemeye “karşı değerleme” denir. Birinci derece mantıktaki yapılandırılmış karşı model kavramı F aşamasına bırakılır.
11. **Koşul ayrımı:** `𝒜 → ℬ` bir TFL cümlesidir ve her değerlemede bir doğruluk değeri alır. `𝒜 ⊨ ℬ` ise iki TFL cümlesi arasındaki semantik sonuç ilişkisini bildiren üst dil cümlesidir.
12. **Tablo düzeni:** Aday içerikte atomik cümle harfleri alfabetik sırada verilir; her farklı harf yalnız bir kez sayılır; ana bağlaç sütunu renk dışında ayrıca başlık, kalın çizgi ve metin etiketiyle belirtilir.

## Aşama amacı

Öğrenci Faz C sonunda:

1. Bir değerleme ile gerçek dünyadaki fiili doğruluğu ve bütün değerlemeler üzerindeki mantıksal statüyü ayırır.
2. Beş TFL bağlacının doğruluk koşullarını tek bir değerleme altında içten dışa uygular.
3. Farklı cümle harfi sayısından eksiksiz ve tekrarsız tam doğruluk tablosu üretir.
4. Ana bağlaç sütununu kullanarak bir TFL cümlesini totoloji, çelişki veya olumsal olarak sınıflandırır.
5. İki TFL cümlesinin mantıksal eşdeğerliğini ve bir cümle kümesinin ortak doyurulabilirliğini sınar.
6. Bir argümanın geçerliliğini karşı değerleme bulunup bulunmamasına göre kararlaştırır.
7. `→`, `↔` ve `⊨` işaretlerinin farklı dil düzeylerinde oynadığı rolleri açıklar.
8. İddianın yönüne göre tam tablo, kısaltılmış tam tablo veya tek satırlık kısmi tablo seçer.
9. TFL'nin bir doğal dil argümanını neden yanlış değerlendirebileceğini sembolleştirme kaybı üzerinden teşhis eder.

## Aşama çıkış görevi

Öğrenciye daha önce görmediği, dört atomik bildirim içeren kısa bir politika metni ve bu metinden çıkarıldığı ileri sürülen bir sonuç verilir. Metinde bir koşul, bir dışlayıcı ayrım, bir belirsiz kapsam ve TFL'nin koruyamayacağı bir doğal dil ayrıntısı bulunur. Öğrenci:

1. Bağlam varsayımını ve sembol anahtarını yazar.
2. Belirsiz cümle için seçtiği okumayı açık ara cümleyle belirtip metni TFL'de sembolleştirir.
3. Bir bileşik cümleyi verilen tek değerleme altında içten dışa hesaplar.
4. Bir hedef cümlenin tam doğruluk tablosunu kurup onu totoloji, çelişki veya olumsal olarak sınıflandırır.
5. İki hedef cümlenin eşdeğer olup olmadığını ve üç cümlenin birlikte doyurulabilir olup olmadığını tabloyla gerekçelendirir.
6. Argümanın geçerliliğini sınar; geçersizse karşı değerlemeyi açıkça yazar, geçerliyse hiçbir kötü satır kalmadığını gösterir.
7. `→` ile `⊨` arasındaki nesne dili/üst dil farkını kendi çözümünden bir örnekle açıklar.
8. Seçtiği tablo yönteminin neden iddiasını kanıtlamaya yeterli olduğunu belirtir.
9. TFL sembolleştirmesinin doğal dil metninden kaybettiği en az iki özelliği raporlar.

Çıkış görevi yalnız sonuç hücreleriyle geçilemez. Sembol anahtarı, ara hesap, kritik sütun/satır işaretlemesi, yöntem gerekçesi ve doğal dil açıklaması incelenebilir olmalıdır.

## Ortak ders sözleşmesi

Her aday ders şu alanları taşıyacaktır:

```text
prerequisites: Önce tamamlanması gereken aday ders kimlikleri
competencies: Dersin ölçülebilir beceri kimlikleri
estimated_minutes: Pilotla doğrulanacak aktif çalışma süresi
mastery_evidence: Öğrencinin ürettiği ve incelenebilen kanıt
review_prompts: Sonraki derslerde gecikmeli geri çağırma soruları
```

Her derste kısa geri çağırma, tek yeni eşik, tam çözülmüş örnek, kısmen tamamlanmış örnek, hata düzeltme ve bağımsız üretim bulunur. Otomatik değerlendirilebilen tablo hücreleri yanında en az bir yöntem veya kavram açıklaması zorunludur.

## C14 — Değerlemeler ve doğruluk işlevleri

### Ders sözleşmesi

- **Tahmini süre:** 40 dakika (pilotla doğrulanacak)
- **Önkoşul:** A6, B10, B11, B13
- **Ana eşik:** Bir TFL cümlesinin doğruluk değerini, verilen tek bir değerleme altında karakteristik doğruluk koşullarını içten dışa uygulayarak hesaplamak.
- **Yetkinlikler:** `tfl.valuation_read`, `tfl.truth_function_apply`, `tfl.semantic_trace`, `tfl.material_conditional_evaluate`

### Öğrenme hedefleri

1. Değerlemeyi cümle harflerine `T` veya `F` atayan üst dil aracı olarak okumak ve yazmak.
2. `¬`, `∧`, `∨`, `→`, `↔` bağlaçlarının karakteristik doğruluk koşullarını uygulamak.
3. Karmaşık bir TFL cümlesini ana bağlaç ve alt cümle ağacına göre içten dışa değerlendirmek.
4. Doğruluk işlevsel bağlaç ile doğal dilde yalnızca doğruluk değerleriyle belirlenmeyen ifade türlerini ayırmak.

### Akademik not

Bir değerleme, cümle harflerine yapılan herhangi bir doğruluk değeri atamasıdır; gerçek dünyada hangi atomik cümlenin fiilen doğru olduğunu keşfetme yöntemi değildir. `→`, TFL içinde maddi koşuldur: yalnız önbileşen doğru ve artbileşen yanlışken yanlıştır. Bu doğruluk işlevsel tanım, nedensel, zamansal veya karşıolgusal bütün “eğer” kullanımlarının eksiksiz çevirisi diye sunulmaz.

### Kritik yanılgılar

- `T` ve `F`yi TFL cümle harfleri sanmak.
- Tek bir değerlemede doğru çıkan cümleyi totoloji ilan etmek.
- Maddi koşulu önbileşen yanlışken yanlış saymak.
- `∨`yi varsayılan olarak dışlayıcı okumak.
- `↔`yi iki tarafın ikisi de doğru olduğunda ve yalnız o durumda doğru sanmak; iki tarafın ikisi de yanlışken de doğru olduğunu unutmak.
- Ana bağlaçtan başlayıp gerekli alt cümle değerlerini hesaplamadan sonuç yazmak.

### Kademeli pratik

- Tam örnek: `v(A)=T`, `v(B)=F` altında `¬(A ∧ B) → B` cümlesini alt cümle ağacıyla değerlendirme.
- Koşul kliniği: Dört önbileşen/artbileşen birleşiminde yalnız `T/F` satırının maddi koşulu yanlış yaptığını gerekçelendirme.
- Yarı tamamlanmış örnek: Üç alt cümlesi verilmiş bir `↔` cümlesinin eksik değerlerini tamamlama.
- Sınır örneği: Aynı doğruluk değerlerine sahip iki doğal dil cümlesinin “zorunlu olarak” önekinden sonra farklı davranabileceğini açıklama.

### Bağımsız üretim

Verilen üç değerleme altında iki karmaşık TFL cümlesini değerlendir. Her çözümde alt cümle sırasını göster; sonucun hangi karakteristik koşuldan geldiğini bir cümleyle açıkla. Ardından doğal dildeki bir karşıolgusal koşulun neden otomatik olarak `→` ile tüketilemeyeceğini belirt.

### Ustalık kanıtı

- Bütün atomik atamalar doğru okunmalı.
- Her bileşik cümlede alt cümleler ana bağlaçtan önce değerlendirilmiş olmalı.
- Beş bağlacın doğruluk koşulları en az bir kez doğru uygulanmalı.
- Öğrenci tek değerleme altındaki doğruluk ile totolojiyi ayırmalı.
- Maddi koşulun en az bir doğal dil sınırı doğru adlandırılmalı.

### Gecikmeli geri çağırma

- `v(A)=T` ne söyler, ne söylemez?
- `A → B` hangi tek durumda yanlıştır?

## C15 — Tam doğruluk tablosu kurma

### Ders sözleşmesi

- **Tahmini süre:** 45 dakika (pilotla doğrulanacak)
- **Önkoşul:** C14, B11
- **Ana eşik:** Bir TFL cümlesindeki farklı atomları ve alt cümle bağımlılıklarını izleyerek bütün değerlemeleri tam ve tekrarsız listelemek.
- **Yetkinlikler:** `tfl.table_rows_generate`, `tfl.table_dependencies_order`, `tfl.table_complete`, `tfl.main_column_identify`

### Öğrenme hedefleri

1. `n` farklı cümle harfi için `2^n` satır gerektiğini açıklamak ve uygulamak.
2. Atom sütunlarını sistematik `T/F` bloklarıyla eksiksiz üretmek.
3. Alt cümle sütunlarını oluşum ağacına göre sıralamak.
4. Bütün cümlenin değerini veren ana bağlaç sütununu işaretlemek ve denetlemek.

### Akademik not

Tam doğruluk tablosunun her satırı bir değerlemeyi, tablonun bütünü ise ilgili cümle harfleri üzerindeki bütün değerlemeleri temsil eder. Aynı harfin formülde kaç kez geçtiği satır sayısını artırmaz; yalnız farklı harflerin sayısı önemlidir. Tam tablo sonuçtan geriye sezgisel tahmin değil, sonlu ve tekrarlanabilir bir hesap yöntemidir.

### Kritik yanılgılar

- Harf tekrarlarını ayrı atomlar saymak.
- Üç atom için altı satır gibi eksik bir liste üretmek.
- Satır tekrar etmek veya bir değerlemeyi atlamak.
- Ana bağlaç yerine son yazılan sembolün sütununu sonuç sütunu sanmak.
- İç alt cümle hesaplanmadan dış sütunu doldurmak.
- Parantezleri düşürüp farklı cümleleri aynı tabloya dönüştürmek.

### Kademeli pratik

- Tam örnek: `(A ∧ B) → ¬C` için sekiz satırı, atom örüntülerini ve alt sütunları adım adım kurma.
- Tekrarlı harf örneği: `(A ↔ A) ∨ ¬A` için yalnız iki satır gerektiğini gösterme.
- Yarı tamamlanmış örnek: `¬(A ∨ B) ↔ (¬A ∧ ¬B)` tablosunda eksik alt sütunları tamamlama.
- Hata düzeltme: Satır sırası düzensiz, bir satırı tekrarlı ve ana sütunu yanlış işaretli tabloyu onarma.

### Bağımsız üretim

Daha önce görülmemiş üç atomlu bir TFL cümlesi için tam tablo kur. Farklı atom sayısını, satır sayısını ve alt cümle hesap sırasını tablonun üstünde yaz; ana bağlaç sütununu renk dışında metin etiketiyle de belirt; iki satırı bağımsız yeniden hesaplayarak denetle.

### Ustalık kanıtı

- Bütün `2^n` değerlemeler tam ve tekrarsız bulunmalı.
- Alt cümle sütunları sözdizim ağacıyla uyumlu sırada hesaplanmalı.
- Ana bağlaç sütunu doğru seçilmeli.
- En az iki satır karakteristik tablolarla geri denetlenmeli.
- Sonuç henüz totoloji/çelişki etiketi ezberine dayandırılmamalı; önce tablo doğrulanmalı.

### Gecikmeli geri çağırma

- Aynı cümle harfinin beş kez geçmesi satır sayısını neden değiştirmez?
- Ana bağlaç sütunundan önce hangi sütunların hazır olması gerekir?

## C16 — Totoloji, çelişki ve olumsallık

### Ders sözleşmesi

- **Tahmini süre:** 35 dakika (pilotla doğrulanacak)
- **Önkoşul:** A3, A6, C15
- **Ana eşik:** Bir TFL cümlesinin tek bir değerlemedeki doğruluk değerini, bütün değerlemelerdeki semantik statüsünden ayırmak.
- **Yetkinlikler:** `tfl.status_classify`, `tfl.status_justify`, `tfl.truth_vs_tautology_distinguish`, `metalanguage.formula_status_state`

### Öğrenme hedefleri

1. Totoloji, çelişki ve olumsallığı bütün değerlemeler üzerinden tanımlamak.
2. Tam tablonun ana sütunundan tek bir TFL cümlesinin statüsünü çıkarmak.
3. “Doğru cümle” ile “totoloji”, “yanlış cümle” ile “çelişki” ayrımını açıklamak.
4. TFL totolojisinin doğal dildeki bütün zorunlu doğruları yakalamadığını belirtmek.

### Akademik not

Totoloji, her değerlemede doğru olan TFL cümlesidir; gerçek dünya bilgisine bağlı fiili doğruluk değildir. Benzer biçimde çelişki, her değerlemede yanlış olan TFL cümlesidir. `2+2=4` zorunlu doğru olsa da TFL'de atomik bir harfle gösterildiğinde totoloji çıkmaz; TFL yalnız temsil ettiği doğruluk işlevsel yapıyı sınar.

### Kritik yanılgılar

- Çoğu satırda doğru olmayı totoloji saymak.
- Fiilen doğru bir atomik cümleyi totoloji saymak.
- Tek satırda yanlış çıkan her cümleyi çelişki saymak.
- “Totoloji”yi argümanın, “geçerli”yi tek cümlenin etiketi olarak kullanmak.
- Doğal dilde zorunlu doğru olan her şeyi TFL totolojisi sanmak.
- Cümlenin kendisi ile cümlenin adını kullanım/anma açısından karıştırmak.

### Kademeli pratik

- Tam örnek: `A ∨ ¬A`, `A ∧ ¬A` ve `A → B` tablolarını karşılaştırıp üç statüyü ayırma.
- Kavram kliniği: “`A → B` bu değerlemede doğrudur” ile “`A → B` totolojidir” iddialarını ayırma.
- Yarı tamamlanmış örnek: Ana sütunu verilmiş üç tabloya statü ve gerekçe ekleme.
- Hata düzeltme: Üç satırı doğru olan dört satırlık cümleyi totoloji ilan eden çözümü onarma.

### Bağımsız üretim

Bir totoloji, bir çelişki ve bir olumsal TFL cümlesi üret; her biri için tam tablo kur; statüyü nicelikli tanımla (“her”, “hiçbir”, “en az bir ... ve en az bir ...”). Ardından gerçek dünyada doğru olabilecek fakat TFL bakımından olumsal bir atomik cümle örneği ver.

### Ustalık kanıtı

- Üç statü tam ve doğru niceliklerle tanımlanmalı.
- Sınıflandırma ana sütunun bütün satırlarına dayanmalı.
- “Doğru” ile “totoloji” açıkça ayrılmalı.
- TFL statüsünün seçilen sembolleştirmeye bağlı olduğu en az bir örnekle açıklanmalı.

### Gecikmeli geri çağırma

- Bir cümlenin üç satırda doğru, bir satırda yanlış olması hangi statüyü verir?
- Zorunlu doğru bir doğal dil cümlesi neden TFL'de atomik bırakıldığında totoloji çıkmayabilir?

## C17 — Mantıksal eşdeğerlik ve tutarlılık

### Ders sözleşmesi

- **Tahmini süre:** 45 dakika (pilotla doğrulanacak)
- **Önkoşul:** C16, B11
- **Ana eşik:** Tek cümlenin statüsü ile iki cümlenin eşdeğerliği ve bir cümle kümesinin ortak doyurulabilirliği arasındaki semantik tür farkını korumak.
- **Yetkinlikler:** `tfl.equivalence_test`, `tfl.satisfiability_test`, `tfl.semantic_relation_witness`, `tfl.single_vs_set_property_distinguish`

### Öğrenme hedefleri

1. İki TFL cümlesini her değerlemede aynı doğruluk değerini alıp almamalarına göre eşdeğerlik açısından sınamak.
2. Birden çok TFL cümlesinin en az bir ortak doğru değerlemesi bulunup bulunmadığını belirlemek.
3. Eşdeğer olmamayı ayıran bir değerlemeyle, doyurulabilirliği ortak doğru bir değerlemeyle tanıklamak.
4. Çelişki ile birlikte doyurulamaz küme; olumsal cümle ile tutarlı cümle kümesi ayrımlarını açıklamak.

### Akademik not

İki cümle mantıksal olarak eşdeğerse her değerlemede aynı doğruluk değerini alır; aynı yazı dizisi olmaları gerekmez. Bir cümle kümesi, üyelerinin hepsini aynı anda doğru yapan en az bir değerleme varsa birlikte doyurulabilirdir. Tek tek olumsal cümlelerden oluşan bir küme yine de birlikte doyurulamaz olabilir: `A` ve `¬A` bunun en küçük örneğidir.

### Kritik yanılgılar

- İki cümlenin bir satırda aynı değeri almasını eşdeğerlik için yeterli saymak.
- `A ↔ B` cümlesi ile “`A` ve `B` eşdeğerdir” üst dil iddiasını aynı tür sanmak.
- Her üyesi tek başına olumsal olan bir kümeyi otomatik tutarlı saymak.
- Kümenin en az bir üyesi doğruysa kümeyi birlikte doyurulabilir saymak.
- “Çelişki”yi tek cümle ve cümle kümesi için ölçüsüz kullanmak.
- Eşdeğerliği D aşamasındaki yeniden yazma lisansıyla karıştırmak.

### Kademeli pratik

- Tam örnek: `¬(A ∨ B)` ile `¬A ∧ ¬B`nin ana sütunlarını karşılaştırma.
- Ayırıcı değerleme: `A → B` ile `B → A`yı eşdeğer olmaktan çıkaran bir satır bulma.
- Ortak değerleme: `A ∨ B`, `A → C`, `B → C` cümlelerini birlikte doğru yapan bir değerleme üretme.
- Tutarsız küme: `A → B`, `A`, `¬B` için ortak doğru satırın bulunmadığını gösterme.

### Bağımsız üretim

İki cümle çifti ve iki cümle kümesini sınayan ortak atom sütunlu tablolar kur. Bir eşdeğer çift için bütün satır eşleşmesini, eşdeğer olmayan çift için ayırıcı değerlemeyi, doyurulabilir küme için ortak doğru değerlemeyi ve birlikte doyurulamaz küme için bütün aday satırların neden elendiğini yaz.

### Ustalık kanıtı

- Eşdeğerlik kararı iki ana sütunun bütün satırlarıyla gerekçelendirilmeli.
- Eşdeğer olmama halinde en az bir ayırıcı değerleme açıkça gösterilmeli.
- Doyurulabilirlik halinde bütün cümleleri aynı anda doğru yapan satır gösterilmeli.
- Birlikte doyurulamazlık halinde hiçbir ortak doğru satır kalmadığı gösterilmeli.
- Tek cümle özelliği ile cümle kümesi özelliği doğru terimlerle ayrılmalı.

### Gecikmeli geri çağırma

- Her biri olumsal iki cümle neden birlikte doyurulamaz olabilir?
- `A ↔ B` ile “`A` ve `B` mantıksal olarak eşdeğerdir” arasındaki dil düzeyi farkı nedir?

## C18 — Geçerlilik ve karşı değerleme

### Ders sözleşmesi

- **Tahmini süre:** 45 dakika (pilotla doğrulanacak)
- **Önkoşul:** A3, A4, A6, C17
- **Ana eşik:** Geçerliliği sonucun fiili doğruluğuyla değil, bütün öncüllerin doğru ve sonucun yanlış olduğu bir değerlemenin imkânsızlığıyla sınamak.
- **Yetkinlikler:** `tfl.entailment_test`, `tfl.validity_decide`, `tfl.countervaluation_construct`, `metalanguage.turnstile_distinguish`

### Öğrenme hedefleri

1. TFL'de semantik sonucu ve argüman geçerliliğini değerlemeler üzerinden tanımlamak.
2. Bir doğruluk tablosunda yalnız bütün öncüllerin doğru ve sonucun yanlış olduğu kötü satırları aramak.
3. Geçersizliği tek bir karşı değerlemeyle göstermek; geçerlilikte hiçbir karşı değerleme kalmadığını gerekçelendirmek.
4. `⊨`, `⊭`, `→` ve `↔` işaretlerinin farklı görevlerini ayırmak.

### Akademik not

`𝒜₁, ..., 𝒜ₙ ⊨ 𝒞`, soldaki bütün TFL cümlelerini doğru, `𝒞`yi yanlış yapan hiçbir değerleme olmadığını söyleyen üst dil cümlesidir. `⊨`, TFL'nin bir bağlacı değildir. `𝒜 → 𝒞` ise TFL içinde daha uzun bir cümledir. Tek öncül durumunda `𝒜 ⊨ 𝒞` olması ile `𝒜 → 𝒞`nin totoloji olması bağlantılıdır; fakat iki yazım aynı dilsel nesne değildir.

### Kritik yanılgılar

- Sonuç fiilen doğruysa argümanı geçerli saymak.
- Bir öncül yanlış çıktığı için argümanı geçersiz ilan etmek.
- Öncüllerin ve sonucun hepsinin doğru olduğu satırı karşı değerleme sanmak.
- Karşı değerlemenin yalnız sonucu yanlış yapmasını yeterli saymak.
- `⊨` işaretini TFL formülünün ana bağlacı gibi değerlendirmek.
- `⊭ 𝒞` sonucundan otomatik olarak `⊨ ¬𝒞` çıkarmak.
- Geçerli argüman için tek iyi satırı yeterli kanıt saymak.

### Kademeli pratik

- Tam örnek: `A → B, A ⊨ B` için bütün kötü satır adaylarını eleme.
- Karşı değerleme: `A → B, B ⊭ A` için `A=F`, `B=T` satırını tanık olarak yazma.
- Tür kliniği: `A → B`, `A ↔ B` ve `A ⊨ B` ifadelerinden hangilerinin TFL cümlesi olduğunu ayırma.
- Hata düzeltme: Sonucu doğru olan tek satıra bakıp geçerlilik ilan eden çözümü onarma.

### Bağımsız üretim

Biri geçerli, biri geçersiz iki yeni argümanı ortak sütunlu tam tablolarla sınayarak raporla. Geçersiz argüman için karşı değerlemeyi ayrı satır olarak yaz; geçerli argüman için bütün kötü satır adaylarının neden elendiğini göster. Son olarak her raporda `→` ile `⊨` işaretlerinin rolünü bir cümleyle açıkla.

### Ustalık kanıtı

- Bütün öncül ve sonuç sütunları doğru hesaplanmalı.
- Kötü satır ölçütü niceliksel olarak doğru ifade edilmeli.
- Geçersizlik gerçek bir karşı değerlemeyle gösterilmeli.
- Geçerlilik tek iyi örnekle değil, karşı değerleme yokluğuyla gerekçelendirilmeli.
- `⊨` ile `→` nesne dili/üst dil ayrımı doğru açıklanmalı.

### Gecikmeli geri çağırma

- Bir karşı değerleme hangi sütunları hangi doğruluk değerlerinde bırakır?
- `A → B` ile `A ⊨ B` neden aynı tür ifade değildir?

## C19 — Kısmi tablolar ve TFL'nin sınırları

### Ders sözleşmesi

- **Tahmini süre:** 50 dakika (pilotla doğrulanacak)
- **Önkoşul:** B12, B13, C18
- **Ana eşik:** İddianın kanıt yüküne göre tam, kısaltılmış tam veya tek satırlık kısmi tablo seçmek ve sonucu TFL'nin ifade gücüyle sınırlı yorumlamak.
- **Yetkinlikler:** `tfl.table_method_select`, `tfl.partial_table_construct`, `tfl.proof_burden_explain`, `tfl.expressiveness_limit_diagnose`

### Öğrenme hedefleri

1. Tam tablo içindeki güvenli hücre atlamaları ile yalnız hedef bir değerlemeyi kuran kısmi tabloyu ayırmak.
2. Evrensel ve varoluşsal semantik iddialarda hangi yönde tek tanığın, hangi yönde bütün değerlemelerin gerektiğini belirlemek.
3. Geçersizlik, eşdeğer olmama ve doyurulabilirlik için tek değerlemelik tanık üretmek.
4. TFL'nin iç yapı, bulanıklık, zorunluluk, karşıolgusallık, nedensellik, zaman sırası ve pragmatik vurgu sınırlarını teşhis etmek.

### Akademik not

Kısaltılmış tam tablo bütün değerleme satırlarını korur; yalnız sonucu değiştiremeyecek ara hücreleri boş bırakır. Kısmi tablo ise belirli bir iddia için gereken bir veya birkaç değerlemeyi hedefler. Bir cümlenin totoloji olduğunu, bir kümenin birlikte doyurulamaz olduğunu veya bir argümanın geçerli olduğunu göstermek genel olarak bütün ilgili değerlemeleri dışlamayı gerektirir. Buna karşılık totoloji olmadığını, eşdeğer olmadığını, doyurulabilir olduğunu veya geçersiz olduğunu göstermek için uygun tek bir değerleme yeterli olabilir.

### Kanıt yükü tablosu

| Soru | “Evet” için | “Hayır” için |
| --- | --- | --- |
| Totoloji mi? | Tam/kısaltılmış tam tablo | Yanlış yapan tek değerleme |
| Çelişki mi? | Tam/kısaltılmış tam tablo | Doğru yapan tek değerleme |
| Eşdeğer mi? | Tam/kısaltılmış tam tablo | Farklı değer veren tek değerleme |
| Birlikte doyurulabilir mi? | Hepsini doğru yapan tek değerleme | Tam/kısaltılmış tam tablo |
| Geçerli mi? | Tam/kısaltılmış tam tablo | Öncülleri doğru, sonucu yanlış yapan tek değerleme |

### Kritik yanılgılar

- Bir tek başarılı satırla totoloji veya geçerlilik kanıtlamak.
- Kısaltılmış tam tablo ile kısmi tabloyu aynı yöntem sanmak.
- Boş bırakılan hücrenin değerinin hiçbir koşulda önemli olmadığını varsaymak.
- Karşı değerleme kurarken alt cümle koşullarının birlikte gerçekleştirilebilirliğini denetlememek.
- TFL testinin olumsuz sonucunu doğal dil argümanının kesin geçersizliği saymak; sembolleştirme kaybını incelememek.
- TFL'nin sınırlı olmasını yöntemin yararsız veya keyfi olduğu şeklinde yorumlamak.

### Kademeli pratik

- Tam örnek: Bir koşulun yanlış olmasını hedefleyerek tek satırlık değerleme kurma.
- Yöntem seçimi: Beş farklı iddia için tam, kısaltılmış tam veya kısmi tablo kararı verme.
- Kısaltma örneği: Sonuç doğru olduğu için kötü satır olamayacak satırlarda öncül hücrelerini hesaplamama.
- Sınır kliniği: “Daisy'nin dört bacağı vardır; öyleyse ikiden fazla bacağı vardır” argümanının TFL atomlaştırmasında neden yapısal bağını kaybettiğini açıklama.
- Koşul sınırı: Karşıolgusal bir doğal dil koşulunun maddi koşulla neden eksik temsil edildiğini gösterme.

### Bağımsız üretim

Dört semantik iddia için en ekonomik yeterli yöntemi seç ve uygula: bir cümlenin totoloji olmadığı, iki cümlenin eşdeğer olmadığı, bir kümenin birlikte doyurulabilir olduğu ve bir argümanın geçersiz olduğu. Her çözümde tek satırın neden yeterli olduğunu açıkla. Ardından TFL'de zayıf temsil edilen bir doğal dil argümanını seç; kaybolan yapıyı, tablonun verdiği sonucu ve daha uygun inceleme aracının hangi tür bilgiye ihtiyaç duyacağını yaz.

### Ustalık kanıtı

- Yöntem seçimi kanıt yüküyle gerekçelendirilmeli.
- Her kısmi tablo atomik atamalardan hedef ana sütuna kadar tutarlı olmalı.
- Tek tanığın yeterli olmadığı en az iki iddia doğru belirlenmeli.
- Sembolleştirme kaybı ile tablo hesap hatası birbirinden ayrılmalı.
- TFL'nin en az üç farklı ifade sınırı doğru örneklerle açıklanmalı.

### Gecikmeli geri çağırma

- Geçersizliği göstermek için neden tek karşı değerleme yeterliyken geçerlilik için tek iyi satır yetmez?
- TFL'de geçersiz görünen doğal dil argümanı hangi durumda yine de iyi bir argüman olabilir?

## Faz B ve Faz D ile eklem noktaları

| Önceki/sonraki içerik | Faz C'deki kullanım veya sınır |
| --- | --- |
| A3 Doğruluk, geçerlilik ve sağlamlık | C16'da cümle doğruluğu/statüsü, C18'de argüman geçerliliği olarak geri çağrılır |
| A4 Karşı durum | C18'de resmi karşı değerlemeye dönüşür |
| A6 Nesne dili ve üst dil | C14'te `v`, C16-C17'de cümle statüsü, C18'de `⊨` üzerinden geri çağrılır |
| B9 Kapsayıcı/dışlayıcı ayrım | C14'te `∨`nin karakteristik tablosu ve dışlayıcı yapının bileşik hesabı yapılır |
| B10 Maddi koşul | C14'te resmi doğruluk koşulu verilir; C19'da doğal dil sınırı yeniden incelenir |
| B11 Ana bağlaç ve kapsam | C14-C15'te alt cümle hesap sırasının sözdizimsel temeli olur |
| B12 Belirsizlik/bulanıklık | C19'da tablo sonucunun seçilen okumaya ve TFL'nin iki değerli sınırına bağlı olduğu gösterilir |
| B13 Sembolleştirme atölyesi | C çıkış görevinde tablo öncesi sembolleştirme denetimi olarak korunur |
| D20-D24 Doğal türetim | C18'de yalnız semantik sonuç öğretilir; hiçbir kanıt kuralı öne çekilmez |
| D25 Eşdeğerliklerin lisansı | C17'de yalnız semantik eşdeğerlik kurulur; yeniden yazma lisansı D25'e bırakılır |
| D26 Kanıt ve semantik geçerlilik | `⊨` ile ilerideki `⊢` ilişkisi burada açıklanmaz; yalnız köprü sorusu bırakılır |

## Mevcut içerikten geçiş haritası

| Mevcut canlı ders | Aday kullanımı |
| --- | --- |
| Doğruluk Tabloları I | C14 ve C15'e ayrılacak; karakteristik tablo ile tam tablo birbirine karıştırılmayacak |
| Doğruluk Tabloları II ve Geçerlilik | C16, C17 ve C18'e ayrılacak; tek cümle, cümle kümesi ve argüman özellikleri ayrı ölçülecek |
| Eşdeğerlik Kuralları I-II | Semantik eşdeğerlik örnekleri C17'ye; kanıt içi yeniden yazma lisansı D25'e taşınacak |
| Sembolleştirmeye Giriş ve bağlaç dersleri | Faz B adayları üzerinden C14-C19'a önkoşul olacak; mevcut küçük `p`, `q`, `r` gösterimi aday aşamada dönüştürülmeyecek |
| Doğruluk Ağaçları ve Meta-Teori | Faz C'ye alınmayacak; seçmeli ileri rota ve D/F köprüleri ayrıca denetlenecek |

Eski URL, ilerleme ve ders kimliklerinin hangi aday derse taşınacağı, bütün rota tamamlanmadan belirlenmeyecektir.

## Aday veri için teknik sözleşme

Aday ders verisi yazılırken aşağıdaki sınırlar otomatik test edilecektir:

1. Ders kimlikleri `C14`-`C19`, sıraları `14`-`19` ve önkoşul grafiği döngüsüz olmalı.
2. C14 tek değerleme, C15 tam tablo, C16 tek cümle statüsü, C17 cümle ilişkisi/kümesi, C18 argüman, C19 yöntem seçimi/sınırlar dışına taşmamalı.
3. `⊢`, doğal türetim kuralları, niceleyiciler ve birinci derece model görevleri aday veride bulunmamalı.
4. Her tablo uyaranının atom sayısı, beklenen satır sayısı, ana bağlacı ve doğruluk sonucu programatik olarak yeniden hesaplanabilmeli.
5. Eşdeğerlik, doyurulabilirlik ve geçerlilik cevapları yalnız yazılı anahtara güvenmeden bağımsız semantik değerlendiriciyle doğrulanmalı.
6. C14-C18'in her birinde en az bir kavram açıklaması; C15-C19'un her birinde en az bir bağımsız tablo üretimi bulunmalı.
7. C19'daki yöntem seçimleri kanıt yükü tablosuyla çelişmemeli.
8. Aday modül öğrenci rotasına, ilerleme kaydına, başarı yüzdesine veya mevcut ders URL'lerine bağlanmamalı.

## Ders üretim kaydı

Bu tablo Faz C'nin **aday geliştirme** durumunu gösterir; canlıya hazır olduğu anlamına gelmez. Kaynak ve ders sözleşmesi tamamlanmıştır. C14-C15, yalıtılmış aday veri ve semantik sınır testi düzeyindedir; Faz C'nin yetkili önizlemesi ancak aşamanın tamamı üretildikten sonra açılacaktır.

| Ders | Aday veri | Otomatik sınır testi | Yetkili aşama önizlemesi |
| --- | --- | --- | --- |
| C14 Değerlemeler ve Doğruluk İşlevleri | Hazır | Hazır | Aşama tamamlanmasını bekliyor |
| C15 Tam Doğruluk Tablosu Kurma | Hazır | Hazır | Aşama tamamlanmasını bekliyor |
| C16 Totoloji, Çelişki ve Olumsallık | Bekliyor | Bekliyor | Bekliyor |
| C17 Mantıksal Eşdeğerlik ve Tutarlılık | Bekliyor | Bekliyor | Bekliyor |
| C18 Geçerlilik ve Karşı Değerleme | Bekliyor | Bekliyor | Bekliyor |
| C19 Kısmi Tablolar ve TFL'nin Sınırları | Bekliyor | Bekliyor | Bekliyor |

## Aday geliştirme kapıları

- [x] Bölüm sınırları iki bağımsız müfredatla karşılaştırıldı.
- [x] Faz B, Faz C ve Faz D arasındaki sözdizimi/semantik/kanıt sınırı yazıldı.
- [x] Gösterim, üst dil ve semantik terim sözleşmesi yazıldı.
- [x] Her dersin önkoşulu, ölçülebilir yetkinliği ve üretim kanıtı tanımlandı.
- [x] Tam, kısaltılmış tam ve kısmi tablo yöntemlerinin kanıt yükü sınırı yazıldı.
- [ ] Aday ders verisi yazıldı.
- [ ] Aday doğruluk tablosu değerlendiricisi ve sınır testleri yazıldı.
- [ ] Aday veri ve önkoşul grafiği otomatik test edildi.
- [ ] Aday içerik yalıtılmış, salt okunur yetkili önizlemede doğrulandı.
- [ ] Mevcut öğrenci rotasının ve ilerleme verisinin değişmediği regresyonla kanıtlandı.

## Canlıya alma kapıları

Aşağıdaki maddeler bütün aday rota tamamlandıktan sonra A1'den başlayarak yürütülecektir:

- [ ] Mantık/felsefe uzmanı dersleri, tablo cevaplarını ve terimleri tek tek inceledi.
- [ ] Türkçe editörü bütün örneklerin doğallığını ve yöntem açıklamalarını denetledi.
- [ ] Konuyu bilmeyen kullanıcılarla sesli düşünme testi yapıldı.
- [ ] Farklı ön bilgi düzeylerinden küçük grupla aşama pilotu yapıldı.
- [ ] Ders süreleri gerçek oturumlarla ölçüldü.
- [ ] Klavye, ekran okuyucu, renk dışı tablo işaretleri, mobil ve masaüstü akışları doğrulandı.
- [ ] A1'den son projeye kadar uçtan uca öğrenme denetimi tamamlandı.
- [ ] Eski ilerleme verisi için açık geçiş ve geri dönüş planı onaylandı.

Bu kapılar tamamlanmadan Faz C canlı ders verisine bağlanmayacaktır.
