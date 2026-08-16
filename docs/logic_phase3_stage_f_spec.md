# Faz 3F: Birinci derece mantığın semantiği ve kanıtı

## Statü

Bu belge Faz F'nin kaynaklara dayalı **aday ders sözleşmesidir**. F35-F41
derslerinin akademik sırasını, model ve kanıt motorlarının sınırlarını ve Faz E
ile felsefi köprü arasındaki geçişi sabitler. Aday veri, semantik motoru ve kanıt
denetleyicisi canlı öğrenci rotasından ayrı geliştirilecektir.

Faz F yedi dersten oluşur. Öğrenci önce bir FOL cümlesinin tek bir yorumda
nasıl değerlendirildiğini öğrenir; sonra geçersizliği gösteren karşı model
kurar; bağıntı özelliklerini model üzerinde okur. Ancak bu semantik temel
kurulduktan sonra niceleyici ve kimlik kanıt kuralları açılır. Son ders aynı
argümanı çeviri, model ve kanıt düzeylerinde karşılaştırır.

## Kaynak ve kapsam denetimi

| Kaynak | Faz F'deki işlevi |
| --- | --- |
| [forall x: Calgary, Bölüm 30](https://forallx.openlogicproject.org/html/Ch30.html) | Boş olmayan alan, adların gönderimi, yüklem uzantıları, sıralı ikililer ve kimliğin sabit yorumu |
| [forall x: Calgary, Bölüm 31](https://forallx.openlogicproject.org/html/Ch31.html) | Atomik, bağlaçlı ve niceleyicili formüller için doğruluk ve değişken ataması |
| [forall x: Calgary, Bölüm 32-34](https://forallx.openlogicproject.org/html/Ch32.html) | Mantıksal sonuç, model/karşı model ve tek tek model taramanın geçerlilik için yetersizliği |
| [forall x: Calgary, Bölüm 35](https://forallx.openlogicproject.org/html/Ch35.html) | İkili bağıntıların yansımalı, simetrik ve geçişli gibi özellikleri |
| [forall x: Calgary, Bölüm 36-38](https://forallx.openlogicproject.org/html/Ch36.html) | `∀E`, `∃I`, `∀I`, `∃E`, serbest yerine koyma ve özad kısıtları |
| [forall x: Calgary, Bölüm 39-41](https://forallx.openlogicproject.org/html/Ch39.html) | Kimlik kuralları, türetilmiş niceleyici kuralları ve kanıt-semantiği ilişkisi |
| [MIT OCW Logic I takvimi](https://ocw.mit.edu/courses/24-241-logic-i-fall-2009/pages/calendar/) | Yorum/atama semantiğinin türetimden önce gelmesi ve güvenirlik/tamlık sınırının ayrı tutulması |

## Aşama sınırı

Faz F şu yetkinlikleri öğretir:

- sonlu bir örnek yorumun boş olmayan alanını, ad gönderimlerini ve yüklem
  uzantılarını okuma ve kurma;
- açık formülleri değişken ataması altında, cümleleri yalnız yorum altında
  değerlendirme;
- niceleyici doğruluğunu alanın her üyesi veya en az bir üyesi üzerinden
  gerekçelendirme;
- bir argümanın geçersizliğini tüm öncülleri doğru, sonucu yanlış yapan tek
  karşı modelle gösterme;
- sonlu bir örnek bankasında karşı model bulunamamasını geçerlilik kanıtı
  saymama;
- ikili bağıntıların yansımalı, yansımasız, simetrik, asimetrik,
  ters-simetrik, geçişli ve seri özelliklerini uzantı üzerinden denetleme;
- `∀E`, `∃I`, `∀I`, `∃E` kurallarını yakalamasız yerine koyma ve özad
  kısıtlarıyla kullanma;
- kimlik özdeşliği ve kimlik yerine koyma kurallarını kullanma;
- doğal dil, FOL çevirisi, model ve Fitch kanıtı arasında kontrollü geçiş.

Faz F şunları tamamlanmış bir sonuç gibi öğretmez:

- sonlu model taramasıyla genel FOL geçerliliği kararı;
- otomatik teorem ispatlayıcının bulamadığı kanıttan geçersizlik çıkarma;
- güvenirlik veya tamlığın metateorik ispatı;
- sonsuz modelleri sonlu bir çizimle tüketme;
- boş alan semantiği, serbest mantık veya özdeşliksiz alternatif sistemler;
- fonksiyon sembolleri, karmaşık terimler, Skolemleştirme veya çözümleme;
- küme kuramı ile model kuramını özdeş sayma;
- belirli betimlemelerin Russellcı çözümlemesi. Bu konu felsefi köprüde
  mantıksal biçim problemi olarak ele alınır.

## Semantik sözleşmesi

1. **Alan:** Her yorum sonlu örneklerde dahi boş olmayan, üyeleri birbirinden
   ayırt edilebilir bir alan taşır.
2. **Ad:** İmzadaki her ad alanın tam bir üyesine gönderilir. Farklı adlar aynı
   üyeye gidebilir; her alan üyesinin adı olmak zorunda değildir.
3. **Yüklem uzantısı:** `n` yerli yüklemin uzantısı alandan alınmış sıralı
   `n`liler kümesidir. `R(a,b)` ile `R(b,a)` ancak iki sıralı ikili de
   uzantıdaysa birlikte doğrudur.
4. **Kimlik:** `=` yorum tarafından serbestçe atanmaz; iki terim aynı alan
   üyesini gösteriyorsa doğrudur.
5. **Atama:** Değişken ataması yalnız değişkenleri alan üyelerine gönderir.
   Açık formülün doğruluğu yorum ve atamaya göredir; kapalı cümlenin sonucu
   başlangıç atamasından bağımsızdır.
6. **Bağlaçlar:** `¬`, `∧`, `∨`, `→`, `↔` Faz C'deki doğruluk-fonksiyonlu
   koşulları korur.
7. **Tümel niceleyici:** `∀x𝒜`, alanın her üyesi `x`e atanarak `𝒜` doğru
   kalıyorsa doğrudur. İlk başarısız üye bir karşı örnek tanığıdır.
8. **Varoluş niceleyicisi:** `∃x𝒜`, alanın en az bir üyesi `x`e atanarak `𝒜`
   doğru oluyorsa doğrudur. Böyle bir üye bir doğruluk tanığıdır.
9. **Gölgeleme:** İç niceleyicinin aynı harfi kullanması dış atamayı geçici
   olarak gölgeler; iç kapsam bitince önceki atama geri gelir.
10. **Mantıksal sonuç:** `Γ ⊨ 𝒜`, her yorumda Γ'daki bütün cümleler doğruysa
    `𝒜`nın da doğru olmasıdır. Tek karşı model bu iddiayı çürütür.
11. **Arama sınırı:** Bir yazılımın sağlanan veya sonlu üretilmiş örnek
    modellerde karşı model bulamaması yalnız `örneklemde karşı model yok`
    sonucunu üretir; `geçerli` sonucunu üretmez.
12. **İz:** Otomatik değerlendirme yalnız son değeri değil, terim
    gönderimlerini, atomik üyelikleri ve niceleyici tanık/karşı örneklerini
    yapılandırılmış olarak verir.

## Kanıt sözleşmesi

1. Faz D'nin klasik Fitch kapsam, satır atfı ve alt kanıt kuralları korunur.
2. `∀E`, `∀x𝒜(x)`den yakalamasız bir `𝒜(c)` örneği çıkarır. Yalnız
   niceleyicinin serbest bağladığı oluşumlar değiştirilir.
3. `∃I`, bir `𝒜(c)` örneğinden `∃x𝒜(x)` çıkarır; sonuçtaki bazı `c`
   oluşumlarının bırakılması ancak gerçekten bir yerine koyma örneği
   oluşturuyorsa kabul edilir.
4. `∀I`, `𝒜(c)`den `∀x𝒜(x)` çıkarırken `c` hiçbir açık varsayımda ve
   çıkarılmamış bağımlılıkta geçemez. `c` keyfi nesneyi temsil etmelidir.
5. `∃E`, `∃x𝒜(x)` ve `𝒜(c)` varsayımıyla başlayan kapalı alt kanıttan sonuç
   çıkarır. `c`, varoluşsal öncülde, sonuçta veya alt kanıt dışındaki açık
   varsayımlarda geçemez.
6. `=I`, herhangi bir ad için `a=a` yazılmasına izin verir; satır atfı istemez.
7. `=E`, `a=b` ve içinde `a` geçen bir formülden, seçilen serbest `a`
   oluşumları `b` ile değiştirilmiş formüle geçer. Ters yön de kimliğin
   simetrisi nedeniyle lisanslıdır; değişken yakalama yasaktır.
8. Kanıt denetleyicisi biçimsel olarak yanlış giriş, kapsam, atıf, yerine
   koyma ve özad tazeliği hatalarını ayrı kodlarla raporlar.
9. Doğrulanmamış kanıt, argümanın geçersiz olduğunu göstermez. Karşı model
   bulunan bir argüman için doğrulanmış kanıt ise yayın engelleyen güvenirlik
   çatışmasıdır.

## Öğretim sırası

| Ders | Yeni eşik | Neden bu sırada? |
| --- | --- | --- |
| F35 | Yorum, gönderim, uzantı, atama ve doğruluk | E'deki sözdizim işaretleri ilk kez belirli bir yapıda anlam kazanır |
| F36 | Model ve karşı model kurma | Tek cümle doğruluğundan argüman düzeyinde semantik sonuca geçilir |
| F37 | Bağıntı özellikleri | Sıralı ikili uzantıları artık sistematik olarak okunabilir |
| F38 | `∀E` ve `∃I`; yerine koyma örnekleri | Kısıtsız niceleyici kuralları önce kurulur |
| F39 | `∀I` ve `∃E`; özad disiplini | Tazelik ve alt kanıt kısıtları ayrı bir kavramsal eşiktir |
| F40 | Kimlik ve karma niceleyici kanıt stratejisi | Kimlik ancak niceleyici kapsamı ve özad disiplini kurulduktan sonra eklenir |
| F41 | Çeviri-model-kanıt aşama projesi | Üç temsil düzeyi tek gerçek argümanda çapraz denetlenir |

## Aşama amacı

Öğrenci Faz F sonunda:

1. Bir yorumun alan, ad gönderimi ve yüklem uzantısı bileşenlerini eksiksiz
   kurar.
2. Atomik, bağlaçlı ve niceleyicili bir FOL cümlesini içten dışa değerlendirir.
3. Açık formül ile cümlenin değerlendirme girdilerini ayırır.
4. Niceleyici için tanık veya karşı örnek üyeyi gösterir.
5. Geçersiz bir argümana küçük ve açık bir karşı model üretir.
6. Birkaç modelde başarısız arama ile genel geçerlilik ispatını ayırır.
7. Bağıntı özelliklerini sıralı ikililer üzerinden gerekçelendirir.
8. Dört niceleyici kuralını özad ve yerine koyma kısıtlarıyla uygular.
9. Kimlik içeren karma bir doğal türetimi denetler ve onarır.
10. Aynı argüman için çeviri, semantik ve kanıt sonuçlarının neyi gösterdiğini
    ve neyi göstermediğini açıklar.

## Aşama çıkış görevi

Öğrenciye doğal dilde üç öncül ve bir sonuç içeren, iki yerli bağıntı,
niceleyici sırası ve kimlik kullanan yeni bir argüman verilir. Öğrenci:

1. Alanı ve aritesi açık FOL anahtarını kurar.
2. Argümanı sembolleştirip her formülü geri okur.
3. En az iki yorumda öncül ve sonucu yapılandırılmış doğruluk iziyle sınar.
4. Argüman geçersizse tüm öncülleri doğru, sonucu yanlış yapan karşı model
   verir; bulamazsa bunun henüz geçerlilik ispatı olmadığını yazar.
5. Argüman kanıtlanabiliyorsa `∀`, `∃` ve gerekirse `=` kurallarını içeren
   kapsamı doğru Fitch kanıtı kurar.
6. Her özadın neden taze olduğunu veya hangi satıra bağımlı olduğunu açıklar.
7. Model sonucu ile kanıt sonucunu karşılaştırır; olası bir çatışmayı gizlemez.
8. Biçimselleştirmenin doğal dilde kaybettiği en az iki özelliği raporlar.

Çıkış görevi yalnız çoktan seçmeli soruyla veya yazılımın “doğru” etiketiyle
geçilemez.

## Aday motor sözleşmesi

1. Semantik motor `core/logic_fol_semantics.py` içinde sözdizim motorundan ve
   canlı derslerden ayrı tutulur.
2. Model verisi alan, ad gönderimleri ve her yüklem için ariteye uygun uzantı
   taşır; eksik/fazla sembol ve alan dışı üyeyi reddeder.
3. Değerlendirme `FOLFormula` ağacını kullanır; metni düzenli ifadelerle
   yorumlamaz.
4. Açık formül için bütün serbest değişken atamaları istenir; kapalı cümlede
   başlangıç ataması sonucu değiştiremez.
5. Niceleyici değerlendirmesi her alan üyesini kaydeder ve ilk tanık veya
   karşı örneği raporlayabilir.
6. Karşı model araması yalnız verilen model bankasında çalışır ve hiçbir
   zaman `valid` etiketi üretmez.
7. Bağıntı özellikleri tanım başına ayrı karşı örnek tuple'ı döndürür.
8. FOL kanıt motoru `core/logic_fol_fitch.py` içinde TFL motorunun davranışını
   değiştirmeden geliştirilir.
9. Kanıt formülleri aynı FOL imzasıyla ayrıştırılır; öncül, hedef ve bütün
   satırlar kapalı cümle olmalıdır. Yalnız kural şeması işlemlerinde geçici
   açık formül kullanılır.
10. Özad kısıtları salt harf aramasıyla değil, ayrıştırılmış terim oluşumları
    ve açık kapsam bağımlılıklarıyla denetlenir.
11. Semantik ve kanıt motoru bağımsız çalışır; F41 çapraz denetleyicisi iki
    sonucu sonradan karşılaştırır.
12. Aday veri ve motorlar öğrenci rotasına, ilerleme modeline veya canlı ders
    URL'lerine bütün yayın kapıları geçilmeden bağlanmaz.

## Ders üretim kaydı

| Ders | Sözleşme | Aday veri | Otomatik motor/sınır testi | Yetkili önizleme |
| --- | --- | --- | --- | --- |
| F35 Yorum, Gönderim ve Doğruluk | Hazır | Hazır | Hazır | Bekliyor |
| F36 Model ve Karşı Model | Hazır | Hazır | Hazır | Bekliyor |
| F37 Bağıntı Özellikleri | Hazır | Hazır | Hazır | Bekliyor |
| F38 Niceleyici Kurallarına Giriş | Hazır | Bekliyor | Bekliyor | Bekliyor |
| F39 Özad Disiplini ve Kanıt Stratejisi | Hazır | Bekliyor | Bekliyor | Bekliyor |
| F40 Kimlik İçeren Kanıtlar | Hazır | Bekliyor | Bekliyor | Bekliyor |
| F41 Çeviri-Model-Kanıt Projesi | Hazır | Bekliyor | Bekliyor | Bekliyor |

## Aday geliştirme kapıları

- [x] Faz E dil/sözdizimi ile Faz F semantik/kanıt sınırı sabitlendi.
- [x] Yorum, atama, doğruluk, karşı model ve bağıntı özellikleri tanımlandı.
- [x] Sonlu model aramasının epistemik sınırı açıkça yazıldı.
- [x] Dört niceleyici ve iki kimlik kuralının yerine koyma/özad kısıtları
  sabitlendi.
- [x] Her dersin önkoşulu, yetkinliği ve ustalık kanıtı tanımlandı.
- [x] Aday semantik motoru ve sınır testleri yazıldı.
- [ ] Aday FOL kanıt motoru ve sınır testleri yazıldı.
- [ ] F35-F41 aday ders verisi yazıldı.
- [ ] Aday önkoşul grafiği ve kaynak sözleşmesi otomatik test edildi.
- [ ] Aday içerik yalıtılmış, salt okunur yetkili önizlemede doğrulandı.
- [ ] Mevcut öğrenci rotası ve ilerleme verisinin değişmediği regresyonla
  kanıtlandı.

## Canlıya alma kapıları

- [ ] En az bir mantık öğretmeni bütün model anahtarlarını, kanıtları ve hata
  açıklamalarını inceledi.
- [ ] Gerçek başlangıç öğrencileri F35-F41'i gözetimli pilotta tamamladı.
- [ ] Tanık/karşı örnek, model sınırı ve özad kısıtı yardımları pilot verisiyle
  düzeltildi.
- [ ] Semantik ve kanıt motorlarının kararları bağımsız referans örneklerle
  karşılaştırıldı.
- [ ] Klavye, ekran okuyucu, küçük ekran, uzun formül ve büyük model düzeni
  test edildi.
- [ ] Eski ilerleme kayıtları için geçiş ve geri alma planı onaylandı.
- [ ] Canlı görünürlük ayrıca ve bilinçli olarak etkinleştirildi.
