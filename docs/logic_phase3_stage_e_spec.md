# Faz 3E: Birinci derece mantığın dili

## Statü

Bu belge Faz E'nin kaynaklara dayalı **aday ders sözleşmesidir**. E27-E34
derslerinin akademik sırası, gösterimi, ölçme biçimi ve Faz D/F sınırları
burada sabitlenir. Aday veri ve denetleyici ayrı modüllerde geliştirilecek;
öğrenciye görünen dersler, mevcut ilerleme kayıtları ve canlı URL'ler bütün
yayın kapıları geçilene kadar değiştirilmeyecektir.

Faz E sekiz dersten oluşur. İlk yol haritasındaki “çoklu genellik” dersi,
bağıntıların yönü öğretilmeden önce geliyordu. Bu sıra düzeltilmiştir: öğrenci
önce bir ve çok yerli yüklemlerde argüman yerlerini okuyacak, sonra iki veya
daha fazla niceleyicinin bu yerleri nasıl bağladığını inceleyecektir. Böylece
`R(a,b)` ile `R(b,a)` ayrımı kurulmadan `∀x∃yR(x,y)` gibi cümlelere
geçilmeyecektir.

Bu belge öğrenciye açık içerik üretmez. Yalnız akademik ve teknik sözleşmeyi
belirler.

## Kaynak ve kapsam denetimi

| Kaynak | Faz E'deki işlevi |
| --- | --- |
| [forall x: Calgary, Bölüm 23](https://forallx.openlogicproject.org/html/Ch23.html) | TFL'nin atom içini neden açamadığı; ad, yüklem, niceleyici ve alanın temel rolleri |
| [forall x: Calgary, Bölüm 24](https://forallx.openlogicproject.org/html/Ch24.html) | Tek niceleyicili yaygın kalıplar, boş yüklemler, alan seçimi, yeniden ifade ve kapsam |
| [forall x: Calgary, Bölüm 25](https://forallx.openlogicproject.org/html/Ch25.html) | Çok yerli yüklem, argüman sırası, çoklu niceleyici, bağımlılık ve kademeli sembolleştirme |
| [forall x: Calgary, Bölüm 26](https://forallx.openlogicproject.org/html/Ch26.html) | Kimlik, “başka”, “yalnız”, “hariç” ve en az/en çok/tam olarak sayı kalıpları |
| [forall x: Calgary, Bölüm 27](https://forallx.openlogicproject.org/html/Ch27.html) | Terim, atomik formül, tümevarımsal formül tanımı, serbest/bağlı değişken ve cümle |
| [forall x: Calgary, Bölüm 29](https://forallx.openlogicproject.org/html/Ch29.html) | Kapsam belirsizliğini birden fazla açık FOL cümlesiyle çözümleme |
| [MIT OCW Logic I takvimi](https://ocw.mit.edu/courses/24-241-logic-i-fall-2009/pages/calendar/) | Niceleyici, değişken, sabit, yüklem ve alanı; açık cümle, kapsam, çoklu niceleme, kimlik ve çeviriyle izleyen ikinci lisans müfredatı kontrolü |

`forall x` bağıntıları ve çoklu niceleyicileri aynı bölümde kurar. Bu program,
öz-ilerlemeli başlangıç öğrencisinin iki farklı hata türünü ayırabilmesi için
önce bağıntı yönünü E29'da, niceleyici sırasını E30'da öğretir. MIT'nin
takvimi de yüklem mantığının dilini ve çevirisini, resmi yorumlar ile türetim
kurallarından önce konumlandırır.

## Aşama sınırı

Faz E yalnız **klasik, fonksiyon sembolsüz birinci derece mantığın dili,
sözdizimi ve doğal dilden sembolleştirilmesini** öğretir:

- söylem alanı;
- ad/sabit, değişken ve bir ya da çok yerli yüklem;
- terim, atomik formül, açık formül ve cümle;
- `∀` ve `∃` niceleyicileri;
- kısıtlı tümel ve varoluşsal cümle kalıpları;
- çok yerli yüklemlerde argüman sırası;
- çoklu niceleyici sırası ve bağımlılık okumaları;
- niceleyici, bağlaç ve olumsuzlamanın kapsamı;
- kimlik ve kimliksizlik;
- en az, en çok ve tam olarak sayı ifadeleri;
- serbest ve bağlı **değişken oluşumları**;
- değişkeni yeniden adlandırma ve yakalanmayı önleyen yerine koyma;
- belirsiz doğal dil cümlesine birden fazla savunulabilir biçimselleştirme;
- biçimselleştirmenin koruduğu ve kaybettiği içerik.

Şunlar Faz E'de öğretilmez veya ustalık ölçütü yapılmaz:

- bir FOL cümlesinin belirli bir modelde doğru olup olmadığını hesaplamak;
- gönderim fonksiyonu, yüklem uzantısı ve değişken atamasıyla resmi semantik;
- model veya karşı model kurarak geçerlilik kararı vermek;
- `∀I`, `∀E`, `∃I`, `∃E` veya kimlik kanıt kuralları;
- niceleyici eşdeğerliklerinin metateorik ispatı;
- fonksiyon sembolleri ve karmaşık terimler;
- önek normal biçim, Skolemleştirme veya çözüm yöntemi;
- belirli betimlemelerin Russellcı çözümlemesi;
- “çoğu”, “hemen hemen hepsi” ve genelleştirilmiş niceleyiciler;
- boş alanlı veya serbest mantık sistemleri.

E31'de niceleyici olumsuzlamaları, doğru geri okuma ve çeviri için standart
eşdeğer yeniden ifadeler olarak kullanılacaktır. Bu eşdeğerliklerin model
kuramsal gerekçesi Faz F'de kurulacaktır. E32'de `=` işaretinin sabit mantıksal
okuması tanıtılacak, fakat kimlik içeren çıkarım kuralları F40'a bırakılacaktır.

## Gösterim ve dil sözleşmesi

1. **Alan:** Her sembol anahtarı boş olmayan bir söylem alanı bildirir.
   Niceleyiciler yalnız bu alanın üyeleri üzerinde dolaşır.
2. **Adlar/sabitler:** `a`-`r` küçük harfleri ad olarak kullanılır. Her ad alanın
   tam bir üyesine gönderimde bulunur. Ayrı adların ayrı nesneleri göstermesi
   zorunlu değildir; alandaki her nesnenin bir adı olması da gerekmez.
3. **Değişkenler:** `s`-`z` küçük harfleri değişkendir. Değişken tek başına ad
   değildir; açık oluşumu bir niceleyici veya daha sonra semantikte bir atama
   olmadan belirli bir nesneyi göstermez.
4. **Yüklemler:** Büyük Latin harfleri yüklem sembolüdür. Ariteleri sembol
   anahtarında açıkça yazılır: `F(x)`, `R(x,y)`, `B(x,y,z)`.
5. **Atomik formül:** `F(a)`, `R(a,b)` ve `x=y` atomik formüldür. Yüklemin
   aldığı terim sayısı ilan edilen aritesiyle tam eşleşmelidir.
6. **Uygulama yazımı:** Yüklem uygulamasında parantez ve virgül korunur.
   Eski canlı içerikteki `Fa` ve `Rab` kısaltmaları aday Faz E'de kullanılmaz.
7. **Niceleyiciler:** `∀x 𝒜` ve `∃x 𝒜` yazımında niceleyicinin kapsamı `𝒜`dır.
   Bir bağlaç içeriyorsa kapsam parantezle açık gösterilir.
8. **Bağlaçlar:** Faz B'deki `¬`, `∧`, `∨`, `→`, `↔` ve parantez sözleşmesi
   aynen korunur. İkili bağlaçların sessiz önceliğine güvenilmez.
9. **Kimlik:** `t₁=t₂`, iki terimin tek ve aynı nesneyi gösterdiğini söyler.
   `=` öğrenci tarafından yeniden tanımlanan sıradan bir yüklem değildir.
10. **Üst dil:** `𝒜(x)` gibi şemalar nesne dilinin gerçek formülleri değil,
    herhangi bir uygun formülden söz eden üst dil işaretleridir.
11. **Cümle:** Serbest değişken oluşumu bulunmayan FOL formülü “cümle”dir.
    “Serbest değişken” kısaltması kullanılabilse de bağlanmışlık her zaman
    değişkenin tek tek **oluşumlarına** aittir.
12. **Yeniden adlandırma:** Bağlı değişken, yalnız tüm bağlı oluşumlarıyla ve
    değişken yakalaması üretmeden yeniden adlandırılabilir.
13. **Boş yüklem:** `∀x(F(x)→G(x))`, hiçbir `F` yoksa doğru olabilir ve tek
    başına `F`lerin varlığını ileri sürmez. Bu dilsel sonuç E28'de görünür
    tutulur; resmi doğruluk koşulu F35'te türetilir.
14. **Sembol anahtarı:** Her yüklem için doğal dildeki argüman sırası açıkça
    yazılır: `L(x,y): x, y'yi seviyor`. Etken/edilgen yüzey biçimi bu sırayı
    sessizce değiştiremez.

## Öğretim sırasının gerekçesi

| Ders | Yeni eşik | Neden bu sırada? |
| --- | --- | --- |
| E27 | Alan, ad, yüklem, değişken ve açık formül | TFL'nin kaybettiği iç yapı açılır; henüz niceleyici kalıbı ezberletilmez |
| E28 | Tek niceleyici ve kısıtlı nicelik | Öğrenci `∀`/`∃` ile koşul/birleşim farkını tek değişken üzerinde görür |
| E29 | Çok yerli yüklem ve bağıntı yönü | Çoklu niceleyiciden önce `R(a,b) ≠ R(b,a)` ayrımı güvenceye alınır |
| E30 | Çoklu niceleyici ve bağımlılık | Niceleyici sırası artık bilinen bağıntı yerlerini bağlar |
| E31 | Kapsam ve niceleyici olumsuzlaması | Tek ve çoklu yapı görüldükten sonra geniş/dar kapsam karşılaştırılır |
| E32 | Kimlik ve sayısal ifadeler | “Başka”, “yalnız”, en az/en çok/tam olarak kalıpları için önce çoklu nicelik gerekir |
| E33 | Resmi sözdizim, serbest/bağlı oluşum ve yerine koyma | Kullanılan yapıların kesin kurucu tanımı, öğrenci örnek repertuvarı oluşunca sistemleştirilir |
| E34 | Belirsizlik ve sembolleştirme atölyesi | Bütün dil araçları yeni, gerçek metinlerde gerekçeli olarak birleştirilir |

## Aşama amacı

Öğrenci Faz E sonunda:

1. TFL'nin görünmez bıraktığı nesne-yüklem ve bağıntı yapısını FOL'de açar.
2. Bir problem için yeterli alan ve aritesi açık sembol anahtarı kurar.
3. Ad, değişken, terim, yüklem, atomik formül, açık formül ve cümleyi ayırır.
4. Tek niceleyicili yaygın Türkçe kalıpları koşul/birleşim yönünü koruyarak
   sembolleştirir.
5. Çok yerli yüklemlerde argüman sırasını doğal dile doğru geri okur.
6. `∀x∃y` ile `∃y∀x` yapılarını bağımlılık bakımından ayırır.
7. Olumsuzlamanın ve niceleyicilerin geniş/dar kapsam okumalarını görünür kılar.
8. Kimlikle farklılık, en az, en çok ve tam olarak sayısal iddialar kurar.
9. Her değişken oluşumunun bağlayıcısını veya serbestliğini belirler.
10. Belirsiz bir cümle için tek cevap dayatmak yerine, bağlam varsayımlarını
    ve birbirinden farklı doğruluk koşullarına sahip savunulabilir okumaları
    açıklar.

## Aşama çıkış görevi

Öğrenciye daha önce görmediği, kişiler ve kurumlar arasında tek ve çok yerli
ilişkiler içeren kısa bir doğal dil metni verilir. Metinde tek niceleme,
çoklu niceleme, olumsuzlama, kimlik ve en az bir gerçek kapsam belirsizliği
bulunur. Öğrenci:

1. Söylem alanını ve gerekçesini yazar.
2. Adları ve ariteleri açık yüklemleri içeren tutarlı sembol anahtarı kurar.
3. Sekiz cümleyi FOL'de sembolleştirir.
4. En az bir `∀∃`/`∃∀` çiftini doğal dile geri okuyup bağımlılık farkını açıklar.
5. Kimlik içeren bir “tam olarak” cümlesi kurar ve tüm farklılık koşullarını
   gösterir.
6. Karmaşık bir formülde her değişken oluşumunun bağlayıcısını işaretler.
7. Belirsiz cümleye en az iki savunulabilir form verir; hangi bağlamda hangisini
   seçtiğini söyler.
8. Biçimselleştirmenin koruduğu ve kaybettiği en az iki doğal dil özelliğini
   açıklar.
9. Bütün formülleri doğal dile geri okuyarak sembol anahtarı, yön, kapsam ve
   değişken çakışmalarını düzeltir.

Çıkış görevi model kurma, doğruluk hesabı veya FOL türetimi istemez. Yalnız
çoktan seçmeli puanla geçilemez.

## Ortak ders sözleşmesi

Her aday ders şu ortak alanları taşıyacaktır:

```text
prerequisites: Önce tamamlanması gereken aday ders slug'ları
competencies: Dersin ölçülebilir beceri kimlikleri
estimated_minutes: Pilotla doğrulanacak aktif çalışma süresi
mastery_evidence: Öğrencinin ürettiği ve incelenebilen kanıt
review_prompts: Sonraki derslerde gecikmeli geri çağırma soruları
fol_signature: Derste kullanılan ad, değişken ve yüklem aritesi sözleşmesi
syntax_fixtures: Denetleyicinin kabul/ret ve uyarı örnekleri
symbolization_fixtures: Doğal dil, anahtar, kabul edilen biçimler ve hata sınıfları
```

Her derste kısa geri çağırma, tek yeni eşik, tam çözülmüş örnek, bazı adımları
boş bırakılmış örnek, ilk hata noktasını onarma ve bağımsız üretim bulunur.
Otomatik geri bildirim “yanlış” demekle yetinmez; alan, kategori, arite, yön,
niceleyici türü, bağlaç, kapsam, bağlanma veya kimlik hatasını ayrı sınıflar.

## E27 — Alan, adlar, yüklemler ve açık cümleler

### Ders sözleşmesi

- **Tahmini süre:** 35 dakika (pilotla doğrulanacak)
- **Önkoşul:** B7, D26
- **Ana eşik:** TFL'de tek atom olarak bırakılan bir bildirimi alan, ad, yüklem
  ve terim yerlerine ayırmak; değişken içeren açık formülü cümle sanmamak.
- **Yetkinlikler:** `fol.domain_choose`, `fol.name_distinguish`,
  `fol.predicate_key`, `fol.open_formula_read`, `fol.tfl_limit_explain`

### Öğrenme hedefleri

1. TFL'nin nesne-yüklem iç yapısını neden koruyamadığını bir argüman üzerinden
   göstermek.
2. Alan, ad, değişken, bir yerli yüklem ve atomik formülü ayırmak.
3. Bir yüklem anahtarını boşluk/argüman yeri açık olacak biçimde kurmak.
4. `F(a)` cümlesiyle `F(x)` açık formülünü sezgisel olarak ayırmak.
5. Ayrı adların aynı nesneyi gösterebileceğini ve her alan üyesinin adlandırılmış
   olmak zorunda olmadığını belirtmek.

### Kritik yanılgılar

- Ad sembolünü TFL cümle harfi gibi tam bildirim sanmak.
- `F` yüklemini tek başına doğru veya yanlış bir cümle saymak.
- `F(x)` içindeki `x`i belirli ama bilinmeyen bir kişinin adı gibi okumak.
- Alanı, yüklemin uzantısı veya “hakkında konuşulan tek sınıf” ile karıştırmak.
- Farklı adların zorunlu olarak farklı nesneleri gösterdiğini varsaymak.

### Ustalık kanıtı

- Yeni bir bağlam için savunulabilir alan seçimi.
- En az üç ad ve iki bir yerli yüklem içeren aritesi açık anahtar.
- Altı ifadeyi ad/yüklem/terim/atomik formül/açık formül olarak doğru sınıflama.
- Aynı içeriğin TFL ve FOL gösteriminde neyin kaybolduğunu açıklama.

## E28 — Tek niceleyicili cümleler

### Ders sözleşmesi

- **Tahmini süre:** 40 dakika (pilotla doğrulanacak)
- **Önkoşul:** E27, B10
- **Ana eşik:** Tümel kısıtlamayı koşulla, varoluşsal ortak özelliği birleşimle
  kurmak; “yalnız”, “hiçbiri” ve “hepsi değil” yönlerini ayırmak.
- **Yetkinlikler:** `fol.universal_restrict`, `fol.existential_restrict`,
  `fol.only_direction`, `fol.empty_predicate_read`, `fol.paraphrase_step`

### Öğrenme hedefleri

1. “Her F, G'dir” cümlesini `∀x(F(x)→G(x))` biçiminde kurmak.
2. “Bazı F, G'dir” cümlesini `∃x(F(x)∧G(x))` biçiminde kurmak.
3. “Hiçbir F, G değildir”, “her F, G değildir” ve “her F'nin G olduğu doğru
   değildir” cümlelerini ayırmak.
4. “Yalnız F'ler G'dir” cümlesinde koşul yönünü doğru çevirmek.
5. Tümel cümlenin tek başına `F`lerin varlığını ileri sürmediğini açıklamak.

### Kritik yanılgılar

- Tümel kısıtlamada `∧`, varoluşsal örnekte `→` kullanmak.
- “Yalnız F'ler G'dir”i “her F, G'dir” diye ters çevirmek.
- `∃`yi “tam olarak bir” veya “çoğu” diye okumak.
- Tümel cümleden sessizce varoluş sonucu çıkarmak.
- Alanı doğal dildeki kısıtlayıcı yüklemle aynı şey saymak.

### Ustalık kanıtı

- Altı yaygın tek-niceleyici kalıbın yeni sözcük dağarcığıyla doğru çevirisi.
- Aynı formülün seçilen alan değiştiğinde nasıl geri okunduğunu açıklama.
- Bir koşul/birleşim ve bir “yalnız” yön hatasını teşhis edip onarma.
- Boş `F` sınıfında tümel cümlenin neden varoluş bildirmediğini doğru ifade etme.

## E29 — Çok yerli yüklemler ve bağıntı yönü

### Ders sözleşmesi

- **Tahmini süre:** 35 dakika (pilotla doğrulanacak)
- **Önkoşul:** E28
- **Ana eşik:** Yüklemin aritesini ve her argüman yerinin rolünü sembol
  anahtarında sabitlemek; etken/edilgen yüzeyden bağımsız doğru yönü korumak.
- **Yetkinlikler:** `fol.arity_validate`, `fol.argument_order`,
  `fol.relation_key`, `fol.active_passive_normalize`

### Öğrenme hedefleri

1. Bir, iki ve üç yerli yüklemleri ayırmak.
2. `L(a,b)`, `L(b,a)` ve `L(a,a)` cümlelerini doğru geri okumak.
3. İlişki anahtarında birinci, ikinci ve varsa üçüncü argüman rolünü açık yazmak.
4. Etken ve edilgen cümlelerin aynı doğruluk koşullarını koruyan yönünü bulmak.
5. Arite eksikliği/fazlalığı ile yanlış argüman sırasını ayrı hata olarak tanımak.

### Kritik yanılgılar

- İki yerli yüklemi tek terimle tamamlamak.
- Doğal dilde adı önce geçen kişiyi otomatik ilk argüman yapmak.
- Simetrik olmayan ilişkiyi sessizce ters çevirmek.
- Aynı terimin iki farklı yerde kullanılmasını sözdizim hatası saymak.
- Edilgen çatının bağıntı yönünü zorunlu olarak tersine çevirdiğini sanmak.

### Ustalık kanıtı

- En az bir üç yerli yüklem için rol etiketli sembol anahtarı.
- Etken/edilgen ve dönüşlü okumalar içeren sekiz atomik formülün geri çevirisi.
- Arite ile yön hatalarını birbirinden ayıran iki onarım.
- Bir ilişkinin simetrik olup olmadığının dil anahtarından değil, ayrıca ileri
  sürülecek bir özellik olduğunu açıklama.

## E30 — Çoklu genellik, niceleyici sırası ve bağımlılık

### Ders sözleşmesi

- **Tahmini süre:** 45 dakika (pilotla doğrulanacak)
- **Önkoşul:** E29
- **Ana eşik:** `∀x∃y` ile `∃y∀x` yapılarını “her biri için ayrı olabilir” ve
  “hepsi için tek bir tanık” bağımlılık farkıyla okumak.
- **Yetkinlikler:** `fol.quantifier_order`, `fol.dependency_read`,
  `fol.multiple_generalize`, `fol.variable_plan`

### Öğrenme hedefleri

1. İki niceleyicili cümlede her değişkenin hangi argüman yerini doldurduğunu
   göstermek.
2. Aynı tür niceleyicilerin sırası ile farklı tür niceleyicilerin sırasını
   karşılaştırmak.
3. `∀∃` ve `∃∀` okumalarını tanık bağımlılığı bakımından ayırmak.
4. Değişken çakışmasını önlemek için kademeli ara çeviri kullanmak.
5. Niceleyici kaydırma hatasını geçersiz bir çıkarım kalıbı olarak tanımak.

### Kritik yanılgılar

- Aynı iki niceleyici sembolü bulunduğu için sırayı önemsiz saymak.
- Doğal dil sözcük sırasını düşünmeden doğrudan sembol sırasına kopyalamak.
- `∀x∃y` içindeki `y`nin bütün `x`ler için aynı olması gerektiğini sanmak.
- Tek değişkeni iç içe iki farklı niceleyicinin hizmetine verip gölgelemek.
- Bağımlılık farkını yalnız nicelik miktarı farkı diye anlatmak.

### Ustalık kanıtı

- Aynı cümlenin iki kapsam okumasını doğru `∀∃`/`∃∀` çiftleriyle verme.
- Her formülü iki küçük alan senaryosunda sözlü olarak sınama.
- Bir niceleyici kaydırma çıkarımına somut karşı senaryo üretme.
- En az bir üç niceleyicili cümleyi ara basamaklarla sembolleştirme.

## E31 — Kapsam ve niceleyici olumsuzlaması

### Ders sözleşmesi

- **Tahmini süre:** 40 dakika (pilotla doğrulanacak)
- **Önkoşul:** E30, C17
- **Ana eşik:** Olumsuzlamanın niceleyiciye mi, kısıtlayıcı yükleme mi, ana
  yükleme mi uygulandığını ayırmak ve geniş/dar kapsam okumalarını açık yazmak.
- **Yetkinlikler:** `fol.scope_mark`, `fol.quantifier_negate`,
  `fol.not_all_distinguish`, `fol.wide_narrow_read`

### Öğrenme hedefleri

1. `¬∀x𝒜`, `∀x¬𝒜`, `¬∃x𝒜` ve `∃x¬𝒜` yapılarını ayrı geri okumak.
2. “Hepsi değil” ile “hiçbiri” ayrımını korumak.
3. Niceleyici olumsuzlamalarını standart eşdeğer yeniden ifadelerle çevirmek.
4. Bir cümlede hangi işlecin geniş, hangisinin dar kapsam aldığını göstermek.
5. Belirsiz bir yüzey cümlesinde karar vermek yerine olası okumaları kaydetmek.

### Kritik yanılgılar

- “Herkes gelmedi”yi bağlam sormadan tek formüle zorlamak.
- Olumsuzluğu içeri taşırken niceleyici türünü değiştirmemek.
- “Hepsi değil”i “hiçbiri” ile özdeş saymak.
- Parantezi düşürerek kapsamı belirsiz bırakmak.
- Standart eşdeğerliği Faz E'de model kuramsal olarak ispatladığını sanmak.

### Ustalık kanıtı

- Dört temel olumsuz niceleme yapısının doğru ve birbirinden farklı geri okuması.
- İki belirsiz Türkçe cümle için kapsamı açık ikişer formül.
- Bir yanlış niceleyici olumsuzlamasının ilk bozuk adımını teşhis etme.
- Her okuma için anlamı ayıran küçük bir doğal dil senaryosu.

## E32 — Kimlik ve sayısal ifadeler

### Ders sözleşmesi

- **Tahmini süre:** 45 dakika (pilotla doğrulanacak)
- **Önkoşul:** E31
- **Ana eşik:** Aynı nesne ile nitelikçe benzer nesneyi ayırmak; farklılığı ve
  en az/en çok/tam olarak sayı koşullarını kimlikle açık kurmak.
- **Yetkinlikler:** `fol.identity_read`, `fol.distinctness_construct`,
  `fol.cardinality_at_least`, `fol.cardinality_at_most`,
  `fol.cardinality_exactly`

### Öğrenme hedefleri

1. `a=b`yi iki adın aynı nesneyi gösterdiği iddiası olarak okumak.
2. “Başka”, “kendisi dışında”, “yalnız” ve “hariç” kalıplarında kimliği kullanmak.
3. En az iki nesne için tüm gerekli farklılık koşullarını yazmak.
4. En çok bir ve en çok iki kalıplarını koşullu kimlikle kurmak.
5. “Tam olarak n”i en az n ile en çok n bileşimi olarak açıklamak.

### Kritik yanılgılar

- `=` işaretini benzerlik veya aynı özelliklere sahip olma diye okumak.
- İki varoluş niceleyicisinin kendiliğinden iki farklı nesne seçtiğini sanmak.
- Üç nesnenin farklılığı için yalnız `x≠y` ve `y≠z` yazmak.
- “En çok bir” cümlesini varoluş iddiası sanmak.
- “Tam olarak bir” cümlesinin yalnız varlık veya yalnız teklik yarısını yazmak.

### Ustalık kanıtı

- Aynı nesneyi gösteren iki ad ile farklı nesneleri zorunlu kılan iki formu ayırma.
- En az üç için bütün ikili farklılık koşullarını eksiksiz yazma.
- En çok iki ve tam olarak iki kalıplarını yeni bir yüklemle kurma.
- “Yalnız/hariç” içeren iki doğal dil cümlesinde varlık önkabullerini ayrıca
  açıklama.

## E33 — Serbest/bağlı değişken, yerine koyma ve iyi kurulmuş formül

### Ders sözleşmesi

- **Tahmini süre:** 50 dakika (pilotla doğrulanacak)
- **Önkoşul:** E32, B11
- **Ana eşik:** FOL ifadelerini kurucu sözdizim kurallarıyla denetlemek; her
  değişken oluşumunu en yakın uygun niceleyiciye bağlamak ve yakalamasız yerine
  koyma yapmak.
- **Yetkinlikler:** `fol.term_classify`, `fol.formula_parse`,
  `fol.occurrence_bind`, `fol.sentence_classify`, `fol.substitute_safe`,
  `fol.alpha_rename`

### Öğrenme hedefleri

1. Sembol, ifade, terim, atomik formül, formül ve cümleyi ayırmak.
2. Bir formülü tümevarımsal kurucu kurallarla ayrıştırmak.
3. Her değişken oluşumunun serbest mi bağlı mı olduğunu ve bağlayıcısını bulmak.
4. Boş niceleme ve değişken gölgelemesini sözdizimsel kabul ile öğretimsel uyarı
   olarak ayırmak.
5. Bağlı değişkeni alfa-yeniden-adlandırmak ve serbest değişken yakalamasından
   kaçınmak.

### Kritik yanılgılar

- Bir harfi bütün formül boyunca ya serbest ya bağlı ilan etmek.
- Aynı değişken harfi yeniden kullanıldığında her oluşumu en dış niceleyiciye
  bağlamak.
- Serbest değişken içeren formülü doğru/yanlış bir cümle saymak.
- Bağlı değişkenin adını tek bir oluşumda değiştirip bağı koparmak.
- Yerine koymanın serbest değişkeni içteki niceleyici tarafından yakalamasına
  izin vermek.

### Ustalık kanıtı

- Sekiz ifadeyi terim/atomik formül/formül/cümle/hatalı dizi olarak gerekçeli
  sınıflama.
- Karmaşık bir formülde her değişken oluşumunu bağlayıcısına çizgiyle bağlama.
- İki güvenli, bir yakalama üreten yerine koyma örneğini ayırma ve onarma.
- Alfa-eşdeğer iki formülle serbest değişkeni değiştirmenin neden aynı işlem
  olmadığını açıklama.

## E34 — Birinci derece mantıkta belirsizlik ve sembolleştirme atölyesi

### Ders sözleşmesi

- **Tahmini süre:** 55 dakika (pilotla doğrulanacak)
- **Önkoşul:** E33, B12, B13
- **Ana eşik:** Gerçek bir doğal dil metnini alan, anahtar, ara yeniden ifade,
  kapsam alternatifleri ve geri çeviriyle savunulabilir biçimde çözümlemek.
- **Yetkinlikler:** `fol.translation_plan`, `fol.ambiguity_branch`,
  `fol.back_translate`, `fol.loss_report`, `fol.stage_project`

### Öğrenme hedefleri

1. Sembolleştirmeden önce alanı, adları, yüklem aritelerini ve bağlam
   varsayımlarını yazmak.
2. Karmaşık cümleyi doğal dil/FOL karışımı geçici basamaklarla çözmek; nihai
   yanıtta karışık ifadeyi bırakmamak.
3. Niceleyici sırası, olumsuzlama ve “yalnız” kaynaklı gerçek belirsizlikleri
   ayrı formüllerle görünür kılmak.
4. Formülü doğal dile geri okuyup yön, kapsam ve değişken çakışmasını denetlemek.
5. FOL'nin vurgu, zaman, nedensellik, bağlamsal ima ve bulanıklık gibi hangi
   bilgileri dışarıda bıraktığını raporlamak.

### Kritik yanılgılar

- Belirsiz cümleye bağlam vermeden tek resmi cevap dayatmak.
- Sözcük sırasını doğrudan niceleyici sırası sanmak.
- Ara çalışma için yazılan doğal dil/FOL karışımını nihai formül olarak bırakmak.
- Anahtardaki bağıntı yönünü örnekler arasında değiştirmek.
- Mantıksal eşdeğerliği doğal dilde bütün anlam ayrıntılarının eşitliği sanmak.

### Ustalık kanıtı

- Aşama çıkış görevinin tüm dokuz parçasını içeren yeni bir çözüm dosyası.
- En az bir gerçek kapsam belirsizliğinde iki savunulabilir form ve bağlam
  gerekçesi.
- Otomatik sözdizim denetiminden geçen bütün nihai formüller.
- Başka bir öğrencinin çözümünde ilk kategori/yön/kapsam/bağlanma hatasını bulup
  açıklayıcı düzeltme önerisi.

## Faz D ve Faz F ile eklem noktaları

| Önceki/sonraki eşik | Faz E'deki bağlantı |
| --- | --- |
| B7 atomik TFL cümlesi | E27, TFL'de görünmez bırakılan iç yapıyı ad ve yüklemle açar |
| B10 koşul yönü | E28'de tümel kısıtlama ve “yalnız” yönü için yeniden kullanılır |
| B11 kapsam/WFF | E31 ve E33'te niceleyici kapsamı ile tümevarımsal FOL sözdizimine genişler |
| B12-B13 belirsizlik/atölye | E34'te niceleyici ve bağıntı yapısıyla daha güçlü çözümleme olur |
| C17 eşdeğerlik | E31'de standart niceleyici olumsuzlamaları kullanılır; semantik gerekçe F35'e ertelenir |
| D20-D26 kanıt disiplini | E'de kanıt kuralı açılmaz; yalnız yapı ve üst dil ayrımları korunur |
| F35-F37 yorum/model | E'deki alan, ad ve yüklem anahtarına uzantı ve gönderim işlevi ekler |
| F38-F40 niceleyici/kimlik kanıtı | E'de kurulan dil tamamlanmadan hiçbir FOL kanıt kuralı açılmaz |

## Mevcut içerikten geçiş haritası

| Mevcut canlı içerik | Aday karşılık | Geçiş notu |
| --- | --- | --- |
| Niceleyicilere Giriş | E27-E28 | Alan, ad, değişken ve yüklem niceleyici kalıplarından önce ayrılır |
| Niceleyici Olumsuzlamaları | E31 | Tek niceleyici temelinden ve çoklu kapsamdan sonra konumlanır |
| Çoklu Niceleyici ve Kapsam | E29-E31 | Bağıntı yönü ayrı önkoşul olur; sıra ve olumsuzluk aynı derse yığılmaz |
| Kimlik, Yüklemler ve Alan | E27, E29, E32 | Üç farklı eşik üç ayrı derse dağıtılır |
| Doğal Dilden Yüklem Mantığına I-II | E28-E31, E34 | Kalıp ezberi kademeli çeviri ve geri okuma atölyesine dönüşür |
| Formel Sözdizim ve Serbest/Bağlı Değişken | E33 | Oluşum düzeyi bağlanma ve yakalamasız yerine koyma eklenir |
| Yüklem Mantığında Semantik ve Modeller | F35-F37 | Faz E'den çıkarılır; dil ile model doğruluğu karıştırılmaz |
| Yüklem Mantığında Türetim | F38-F40 | Dil ve semantik kurulmadan kural ezberine başlanmaz |
| Fonksiyon Sembolleri | İleri seçmeli | Wittgenstein çekirdeği için zorunlu tutulmaz |
| Önek Normal Biçim | İleri seçmeli | Çekirdek dil derslerinden çıkarılır |
| Belirli Betimlemeler | Russell/erken Wittgenstein köprüsü | Salt teknik alıştırma değil, mantıksal biçim problemi olarak geri döner |

## Aday veri ve FOL denetleyicisi için teknik sözleşme

1. Ders kimlikleri `E27`-`E34`, sıraları `27`-`34` ve önkoşul grafiği
   döngüsüz olmalı.
2. Aday dersler `core/logic_phase3_stage_e.py` içinde canlı
   `VISIBLE_LOGIC_LESSONS` listesinden ayrı tutulmalı.
3. Sözdizim motoru `core/logic_fol.py` içinde TFL motorundan ayrı olmalı;
   canlı ders modülleri onu dolaylı olarak içe aktarmamalı.
4. Ayrıştırıcı ad, değişken, yüklem, niceleyici, kimlik, bağlaç, parantez ve
   virgülü yapılandırılmış sözdizim ağacına çevirmeli.
5. Yüklem aritesi formül metninden tahmin edilmemeli; alıştırmanın ilan edilmiş
   `fol_signature` verisiyle doğrulanmalı.
6. Ayrıştırıcı terim, atomik formül, olumsuzlama, ikili bağlaç ve niceleyici
   düğümlerini ayırmalı; her düğüm kaynak metindeki konumunu korumalı.
7. Denetleyici kategori, bilinmeyen sembol, arite, eksik terim, fazla terim,
   parantez, kapsam, serbest oluşum ve değişken yakalama hatalarını ayrı kodlarla
   raporlamalı.
8. Serbest/bağlı hesabı değişken harfi düzeyinde değil, her AST oluşumu
   düzeyinde yapılmalı; en yakın uygun niceleyici bağlayıcı olarak kaydedilmeli.
9. Değişken gölgeleme ve boş niceleme sözdizimsel olarak kabul edilebilir,
   fakat başlangıç derslerinde ayrı öğretimsel uyarı üretmeli.
10. Alfa-yeniden-adlandırma ve yerine koyma, serbest değişken yakalanacaksa
    işlemi reddetmeli veya güvenli yeni değişken önermeli.
11. E27-E34 sözdizim örnekleri ayrıştırıcıyla; kabul edilen çeviri anahtarları
    ise yapı karşılaştırmasıyla otomatik denetlenmeli.
12. Çeviri denetimi yalnız düz metin eşitliği kullanmamalı; parantez ve bağlı
    değişken yeniden adlandırma farklarını AST üzerinde ele almalı.
13. Semantik olarak eşdeğer olabilecek her form otomatik doğru sayılmamalı.
    Dersin hedeflediği dilsel okuma, onaylı biçim listesi ve geri çeviriyle
    sınanmalı.
14. Birden fazla savunulabilir okuma varsa veri tek `answer` yerine
    `accepted_readings` ve her okumanın `context_condition` alanını taşımalı.
15. İpucu doğru formülü yazmamalı; ilk hata sınıfını ve kontrol edilecek alan,
    arite, yön, niceleyici veya kapsam katmanını göstermeli.
16. FOL denetleyicisi model doğruluğu, geçerlilik veya kanıt kuralı hakkında
    karar vermemeli; bunlar Faz F motorlarının sorumluluğudur.
17. Yetkili önizleme salt okunur olmalı; sembol anahtarını, kabul edilen
    okumaları, hata kodlarını ve sözdizim denetim sonucunu görünür kılmalı.
18. Aday modül öğrenci rotasına, ilerleme modeline, başarı yüzdesine veya
    mevcut ders URL'lerine bağlanmamalı.

## Ders üretim kaydı

Bu tablo Faz E'nin **aday geliştirme** durumunu gösterir; canlıya hazır olduğu
anlamına gelmez.

| Ders | Sözleşme | Aday veri | Otomatik sözdizim/sınır testi | Yetkili aşama önizlemesi |
| --- | --- | --- | --- | --- |
| E27 Alan, Adlar, Yüklemler ve Açık Cümleler | Hazır | Hazır | Hazır | Bekliyor |
| E28 Tek Niceleyicili Cümleler | Hazır | Hazır | Hazır | Bekliyor |
| E29 Çok Yerli Yüklemler ve Bağıntı Yönü | Hazır | Hazır | Hazır | Bekliyor |
| E30 Çoklu Genellik, Niceleyici Sırası ve Bağımlılık | Hazır | Hazır | Hazır | Bekliyor |
| E31 Kapsam ve Niceleyici Olumsuzlaması | Hazır | Hazır | Hazır | Bekliyor |
| E32 Kimlik ve Sayısal İfadeler | Hazır | Hazır | Hazır | Bekliyor |
| E33 Serbest/Bağlı Değişken, Yerine Koyma ve WFF | Hazır | Hazır | Hazır | Bekliyor |
| E34 Belirsizlik ve Sembolleştirme Atölyesi | Hazır | Hazır | Hazır | Bekliyor |

## Aday geliştirme kapıları

- [x] Bölüm sınırları iki bağımsız müfredat kaynağıyla karşılaştırıldı.
- [x] Bağıntı yönü, çoklu niceleyici sırasından önce konumlandırıldı.
- [x] Faz E dil/sözdizimi ile Faz F semantik/kanıt sınırı yazıldı.
- [x] Alan, ad, değişken, yüklem aritesi, kimlik ve cümle gösterimi sabitlendi.
- [x] Her dersin önkoşulu, ölçülebilir yetkinliği ve ustalık kanıtı tanımlandı.
- [x] FOL ayrıştırıcı ve çeviri denetleyicisinin hata sözleşmesi yazıldı.
- [x] Aday ders verisi yazıldı.
- [x] Aday FOL denetleyicisi ve sınır testleri yazıldı.
- [x] Aday veri ve önkoşul grafiği otomatik test edildi.
- [ ] Aday içerik yalıtılmış, salt okunur yetkili önizlemede doğrulandı.
- [x] Mevcut öğrenci rotasının ve ilerleme verisinin değişmediği regresyonla
  kanıtlandı.

## Canlıya alma kapıları

Aşağıdaki maddeler bütün aday rota tamamlandıktan sonra A1'den başlayarak
yürütülecektir:

- [ ] En az bir mantık öğretmeni E27-E34 anahtarlarını, çevirilerini ve hata
  açıklamalarını inceledi.
- [ ] Gerçek başlangıç öğrencileri E27-E34'ü gözetimli pilotta tamamladı.
- [ ] Alan, koşul/birleşim, bağıntı yönü, kapsam ve değişken bağlama yardımları
  pilot verisiyle düzeltildi.
- [ ] Ayrıştırıcının kabul/ret kararları bağımsız referans örneklerle
  karşılaştırıldı.
- [ ] Erişilebilirlik, klavye kullanımı, ekran okuyucu, küçük ekran ve uzun
  formül düzeni test edildi.
- [ ] Eski ilerleme kayıtları ile `Fa`/`Rab` gösterimi için geçiş ve geri alma
  planı onaylandı.
- [ ] Canlı görünürlük ayrıca ve bilinçli olarak etkinleştirildi.
