# Mantık müfredatı Faz 3 denetimi

## Belgenin statüsü

Bu belge, gerçek öğrencilerle kullanılacak müfredatın yeniden kurulmasından önce yapılan içerik ve öğrenme tasarımı denetimidir. Bu adımda öğrenciye görünen ders sırası veya ders içeriği değiştirilmez.

Faz 3 uygulamasına ancak şu üç karar birlikte netleştiğinde başlanacaktır:

1. Her dersin kazandırdığı yetkinlik ve zorunlu önkoşulları.
2. Çekirdek, paralel atölye ve seçmeli içerik ayrımını.
3. Bir öğrencinin sonraki aşamaya hazır olduğunu gösterecek ölçütleri.

## Uzun vadeli hedef

Programın son hedefi yalnızca biçimsel işlem yaptırmak değildir. Öğrenci;

- doğal dilde bir argümanı yeniden kurabilmeli,
- önermeler ve yüklem mantığında sembolleştirme, semantik çözümleme ve kanıt üretebilmeli,
- biçimsel dil ile doğal dil arasındaki farkı açıklayabilmeli,
- Frege ve Russell'ın Wittgenstein için gerekli temel problemlerini tanıyabilmeli,
- `Tractatus Logico-Philosophicus` metnini kavramsal rehberle okuyabilmeli,
- erken ve geç Wittgenstein arasındaki yöntem değişimini izleyebilmeli,
- `Felsefi Soruşturmalar` içindeki anlam, kullanım, kural izleme ve özel dil tartışmalarını metin üzerinden çözümleyebilmelidir.

Bu nedenle ders sayısı korunacak bir hedef değildir. Ölçüt, gerekli bir yetkinliğin eksik kalmaması ve tek dersin öğrenciden aynı anda gereğinden fazla eşik aşmasını istememesidir.

## Mevcut envanter

### Yayın yapısı

- Veri dosyasında 47 ders tanımı vardır.
- Öğrenci rotasında 45 ders görünürdür.
- Eski 8 ve 11 numaralı iki toparlama dersi birleştirilmiş derslere yönlendirilir ve görünür rotada değildir.
- Testler görünür ders sayısını `45` olarak sabit kabul eder. Müfredat yeniden sıralanırken bu sabit sayı, yapısal sözleşmeye dönüştürülmelidir.
- Görünür rota 6 aşama ve toplam 2.410 dakika, yani yaklaşık 40 saat 10 dakika olarak tanımlanmıştır.

| Mevcut aşama | Ders | Tanımlı süre | Ders süresi aralığı |
| --- | ---: | ---: | ---: |
| Akıl Yürütmenin Temelleri | 9 | 332 dk | 30–45 dk |
| Argüman Çözümleme Atölyesi | 5 | 178 dk | 32–42 dk |
| Önermeler Mantığı | 7 | 316 dk | 40–48 dk |
| Kanıt ve Türetim | 5 | 314 dk | 50–74 dk |
| Yüklem Mantığı | 13 | 786 dk | 50–72 dk |
| İleri Mantık | 6 | 484 dk | 76–86 dk |

### Ders sözleşmesi

Mevcut içerik güçlü bir ortak biçime sahiptir:

- Her görünür derste öğrenme hedefi, iki açıklama bölümü, çalışılmış örnek, yaygın hata, kısa test ve üretim görevi vardır.
- 10 derste etkileşimli laboratuvar bulunur: 4 sembolleştirme, 2 doğruluk tablosu, 3 kanıt kurma ve 1 model kurma laboratuvarı.
- İlerleme ve laboratuvar durumu kalıcı olarak saklanır.

Ancak ortak biçim konu farklarından daha baskın hâle gelmiştir:

- Derslerin tamamı iki bölümden oluşur; konu gerçekten iki bölüme uygun mu diye ayrıştırılmamıştır.
- İleri derslerin çoğu 68–86 dakika sürer. Bu süre tek oturumda kavram öğrenme, örnek çözme ve bağımsız üretim için ağırdır.
- Derslerde makinece okunabilir `prerequisites` alanı yoktur. Arayüz, test ve öneri motoru öğrencinin hangi eksik yüzünden zorlandığını güvenilir biçimde bilemez.
- Laboratuvarlar güçlü bir başlangıçtır fakat 45 dersin yalnız 10'una dağılmıştır. Özellikle kanıt stratejisi ve yüklem mantığı semantiğinde daha fazla kademeli pratik gerekir.

## Akademik sıra karşılaştırması

`forall x: Calgary`, biçimsel mantığı şu omurgayla kurar: temel kavramlar; doğruluk-fonksiyonlu dil; doğruluk tabloları; önermeler mantığında doğal türetim; birinci derece mantığın dili; yorumlar; birinci derece mantıkta doğal türetim; ardından modal mantık ve metateori.

Mevcut program bu omurganın büyük bölümünü kapsar, fakat sıra açısından şu sorunlar vardır:

1. Beş safsata dersi, biçimsel mantık çekirdeğine zorunlu bir blok olarak yerleşmiştir. Safsata teşhisi yararlıdır; fakat sembolik mantığın önkoşulu değildir ve etiket ezberine dönüşme riski taşır.
2. Çıkarım kuralları ile doğal türetim iki ayrı başlangıç gibi sunulur. Öğrenci aynı kanıt sistemine ikinci kez başlıyormuş hissine kapılabilir.
3. Yüklem mantığında zor doğal dil çevirileri, biçimsel sözdizim ve serbest/bağlı değişkenler açıkça kurulmadan önce gelir.
4. Doğruluk ağacı, doğal türetim ve metateori tek derste birleşir. Bunlar farklı öğrenme hedefleri ve farklı hata türleri taşır.
5. Fonksiyon sembolleri, önek normal biçim ve aksiyomatik sistemler, Wittgenstein okumak için zorunlu çekirdekmiş gibi görünür. Bunlar değerli ileri içeriklerdir, fakat çekirdeği gereksiz uzatabilir.
6. Wittgenstein hazırlığı 78 dakikalık tek bir köprü dersine bırakılmıştır. Oxford'un Wittgenstein rotası bile erken dönemi Frege ve Russell bağlamında; geç dönemi anlam, kullanım, kural izleme, özel dil ve kesinlik eksenlerinde ayrı ele alır.

## Wittgenstein hazırlık boşlukları

### Faz 4'e geçmeden önce gerekli biçimsel yetkinlikler

- Nesne dili ile üst dili ayırmak.
- Kullanım ile anmayı ayırmak.
- Yüzeysel dilbilgisi ile mantıksal biçim arasındaki farkı göstermek.
- Sözdizim, semantik ve kanıt kuramının farklı sorulara cevap verdiğini açıklamak.
- Doğruluk fonksiyonu, totoloji, çelişki ve mantıksal sonucu örnekle göstermek.
- Niceleme, kapsam, bağıntı ve kimlik içeren cümleleri okuyabilmek.
- Model ve karşı modelin neyi kanıtlayıp neyi kanıtlamadığını bilmek.
- Biçimselleştirmenin kazandırdıkları ile kaybettirdiklerini ayırt etmek.

### Faz 4'te ayrıca kurulacak felsefi köprü

- Frege'de fonksiyon/argüman, kavram/nesne ve anlam/gönderim.
- Russell'da belirli betimlemeler, mantıksal biçim ve görünür dilbilgisinin çözümlemesi.
- Mantıksal atomculuk, adlandırma, önerme ve dünya ilişkisi.
- Mantık yasalarının statüsü ve mantıksal zorunluluk.

Bu köprü tamamlanmadan `Tractatus` doğrudan ders metni hâline getirilmemelidir.

## Öğrenme tasarımı ilkeleri

### Ders boyutu

- Hedef süre çoğu ders için 20–35 dakikadır.
- Bir ders tek bir büyük kavramsal eşik taşır.
- 40 dakikayı aşan ders ancak okuma atölyesi veya bütünleştirici uygulama ise korunur.
- Uzun dersler içerik silinerek değil, önkoşulları ve uygulamaları ayrılarak bölünür.

### Öğrenme döngüsü

Her çekirdek derste şu sıra aranır:

1. Ön bilgiyi hatırlatan kısa geri çağırma.
2. Tek bir yeni kavram veya yöntem.
3. Tam çözümlü örnek.
4. Bazı adımları öğrenciye bırakılmış örnek.
5. Bağımsız üretim.
6. Hata türüne göre açıklayıcı geri bildirim.
7. Sonraki derste kısa gecikmeli geri çağırma.

Yalnız yeniden okuma yerine geri çağırma pratiği kullanılması, sınıf araştırmalarında farklı eğitim düzeyleri ve içerik alanlarında olumlu sonuçlarla ilişkilidir. Ustalık testleri de genel olarak olumlu etki gösterir; ancak öğretim süresini artırabilir. Bu nedenle hız değil, düzeltme rotasının kalitesi esas alınacaktır.

### Ustalık

- Çoktan seçmeli puan tek başına ustalık sayılmaz.
- Her aşama en az bir çeviri, tablo, model, kanıt veya metin çözümleme üretimi ister.
- Yanlış yanıt yalnız işaretlenmez; hata sınıfı ve dönülmesi gereken önkoşul gösterilir.
- Öğrenci sonraki içeriği inceleyebilir; fakat aşama ustalığı açık ölçüt karşılanmadan verilmez.
- Mevcut yüzde 70 eşiği uygulama öncesinde yeniden değerlendirilecektir. Eşik, düzeltme ve yeniden deneme akışından bağımsız kararlaştırılmayacaktır.

## Faz 3 için taslak çekirdek rota

Bu liste uygulama emri değil, ayrıntılı ders sözleşmelerini yazmak için aday omurgadır. Ders sayısı yalnız içerik denetiminden sonra kesinleşecektir.

### A. Akıl yürütme ve mantıksal ayrımlar

1. İddia, cümle, önerme ve bağlam.
2. Argüman, öncül, ara sonuç ve ana sonuç.
3. Doğruluk, geçerlilik, sağlamlık ve mantıksal sonuç.
4. Biçim, karşı örnek ve geçersizliği gösteren karşı durum fikri.
5. Zorunlu/yeterli koşul ve yön hataları.
6. Nesne dili, üst dil, kullanım ve anma.

### B. Önermeler mantığının dili

7. Atomik TFL cümleleri ve sembol anahtarı.
8. Olumsuzlama ve birleşim.
9. Ayrık bağlaç ve dışlayıcı okuma.
10. Maddi koşul, yalnızca, çift yönlülük ve “-medikçe”.
11. İyi kurulmuş formül, ana bağlaç ve kapsam.
12. Belirsizlik ve birden fazla savunulabilir biçimselleştirme.
13. Kademeli sembolleştirme atölyesi.

### C. Önermeler mantığının semantiği

14. Değerlemeler ve doğruluk fonksiyonları.
15. Tam doğruluk tablosu kurma.
16. Totoloji, çelişki ve olumsallık.
17. Mantıksal eşdeğerlik ve tutarlılık.
18. Geçerlilik ve karşı değerleme.
19. Kısa/eksik tablolar ve önermeler mantığının ifade sınırları.

### D. Önermeler mantığında doğal türetim

20. Kanıt fikri, satır bağımlılığı ve hedef okuma.
21. Birleşim ve koşul kuralları.
22. Olumsuzlama, alt kanıt ve çelişkiye indirgeme.
23. Ayrık bağlaç ve çift yönlülük kuralları.
24. Geriye doğru planlama ve kanıt stratejisi.
25. Türetilmiş kurallar ve eşdeğerliklerin lisansı.
26. Kanıt ile semantik geçerlilik arasındaki ilişki.

### E. Birinci derece mantığın dili

27. Alan, adlar, yüklemler ve açık cümleler.
28. Tek niceleyicili cümleler.
29. Çoklu genellik ve niceleyici sırası.
30. Kapsam ve niceleyici olumsuzlaması.
31. İkili bağıntılar ve bağıntı yönü.
32. Kimlik.
33. Serbest/bağlı değişken, yerine koyma ve iyi kurulmuş formül.
34. Birinci derece mantıkta belirsizlik ve sembolleştirme atölyesi.

### F. Birinci derece mantığın semantiği ve kanıtı

35. Yorum, gönderim ve doğruluk koşulları.
36. Model ve karşı model kurma.
37. Bağıntı özelliklerini modellerde okuma.
38. Niceleyici kurallarının lisansı.
39. Niceleyicilerle kanıt stratejisi.
40. Kimlik içeren kanıtlar.
41. Sözdizim, semantik ve kanıtı birleştiren aşama projesi.

## Paralel ve seçmeli rotalar

### Paralel argüman çözümleme atölyesi

Bu rota A aşamasından sonra açılabilir; biçimsel çekirdeğin ilerlemesini engellemez.

1. Tanım, belirsizlik ve yardımsever yeniden kurma.
2. İlgililik hataları, kişiye saldırı ve otorite kullanımı.
3. Yanlış ikilem, saman adam ve döngüsel gerekçe.
4. Nedensellik, korelasyon ve alternatif açıklama.
5. Gerçek bir metni teşhis edip yeniden yazma atölyesi.

### Seçmeli ileri mantık

- Doğruluk ağaçları.
- Fonksiyon sembolleri ve karmaşık terimler.
- Normal biçimler.
- Alternatif kanıt sistemleri ve aksiyomatik sistemler.
- Güvenirlik, tamlık ve kompaktlığa giriş.
- Karar verilebilirlik ve biçimsel sistemlerin sınırları.

Belirli betimlemeler yalnız teknik seçmeli olarak bırakılmayacaktır; Russell ve erken Wittgenstein köprüsünde felsefi işleviyle yeniden ele alınacaktır.

## Yetkinlik matrisi

| Yetkinlik | İlk kurulum | Kademeli pratik | Aşama kanıtı |
| --- | --- | --- | --- |
| Argüman yapısı | A2 | A3–A5 | Gerçek paragrafın şeması ve revizyonu |
| Nesne dili/üst dil | A6 | B11, C16–C18 | Kullanım-anma hatasını açıklama |
| Önermeler mantığında çeviri | B7–B12 | B13, C | Yeni metnin gerekçeli çevirisi |
| Doğruluk tablosu | C14–C17 | C18–C19 | Karşı değerleme ile geçerlilik kararı |
| Doğal türetim | D20–D25 | D26 | Hedefe yönelik bağımsız kanıt |
| Niceleme ve kapsam | E27–E33 | E34 | İki farklı kapsam okumasını modelleme |
| Model/karşı model | F35–F37 | F41 | Geçersizliğe karşı model üretme |
| Yüklem mantığında kanıt | F38–F40 | F41 | Niceleyici ve kimlik içeren kanıt |
| Biçimselleştirmenin sınırları | A6, C19 | F41 | Aynı cümlenin biçimsel ve dilsel kaybını tartışma |

## Doğrulama protokolü

Faz 3'te aday müfredatı üretmek ile öğrenciye açmak iki ayrı süreçtir. Bir fazın aday içeriğinin hazırlanmış olması, o fazın onaylandığı veya canlı müfredata alınabileceği anlamına gelmez.

### Aday geliştirme kapısı

Bir sonraki aday faza geçmeden önce mevcut faz şu kontrollerden geçer:

1. **Akademik denetim:** Tanım, sembol, cevap anahtarı, çıkarım yönü ve kaynak kontrolü.
2. **Sözleşme testleri:** Önkoşul grafiği, aday ders sırası, yönlendirmeler ve cevapların veri sözleşmesine uygunluğu.
3. **Yalıtılmış önizleme:** Aday içerik öğrenci gezinmesine, ilerleme kaydına ve canlı ders verisine bağlanmadan incelenebilir olmalı.
4. **Teknik regresyon:** Aday modülün mevcut mantık akışını ve mantık dışındaki temel kullanıcı akışlarını değiştirmediği doğrulanmalı.

Bu dört kontrol geçilmeden sonraki aday fazın ders metinleri yazılmaz. İnsan incelemesi bekleyen bir aday faz ise açıkça “yayına kapalı” kalır; bu durum sonraki fazın kaynak araştırmasını ve aday sözleşmesini hazırlamaya engel değildir.

### Canlıya alma kapısı

A-F aday fazlarının ve felsefi köprülerin tamamı hazırlandıktan sonra rota A1'den başlayarak gerçek insanlarla tek tek yeniden yürütülür:

1. **Uzman yürüyüşü:** Bir mantık/felsefe okuyucusu her dersi hedef, örnek, kaynak ve üretim görevi açısından baştan sona inceler.
2. **Acemi sesli düşünme testi:** Konuyu bilmeyen bir kullanıcı ne düşündüğünü sesli anlatarak dersi tamamlar; açıklama gerektiren her durak kaydedilir.
3. **Küçük grup testi:** Farklı ön bilgi düzeylerinden birkaç gerçek öğrenci aşamayı tamamlar. Tekrarlanan kavram yanılgıları içerik sorunu kabul edilir.
4. **Süre pilotu:** Tahmini süreler gerçek çalışma oturumlarıyla ölçülür; hız uğruna içerik veya üretim görevi çıkarılmaz.
5. **Erişilebilirlik ve cihaz kontrolü:** Klavye, ekran okuyucuya anlamlı etiketler, renk dışı geri bildirim, masaüstü ve mobil doğrulanır.
6. **Uçtan uca öğrenme denetimi:** Öğrenci A1'den son aşama projesine kadar ilerler; unutulan önkoşullar, gereksiz tekrarlar ve ani zorluk sıçramaları kaydedilir.
7. **Son regresyon ve geçiş denetimi:** Eski bağlantılar, mevcut ilerleme kayıtları ve mantık dışındaki temel kullanıcı akışları yeniden doğrulanır.

Bir ders insan testinde kritik bir sorun çıkarırsa yalnız o ekran düzeltilmiş sayılmaz; değişikliğin önkoşul ve sonraki derslere etkisi de yeniden sınanır. Bütün kapılar geçmeden hiçbir aday faz canlı müfredata bağlanmaz.

## Uygulama sırası

1. Ders veri sözleşmesine `prerequisites`, `competencies`, `estimated_minutes`, `mastery_evidence` ve `review_prompts` alanlarını eklemek.
2. A aşamasını yeni sözleşmeyle yeniden yazmak ve aday geliştirme kapısından geçirmek.
3. B–F aşamalarını sırayla araştırmak, sözleşmelerini yazmak ve her birini aday geliştirme kapısından geçirmek.
4. Paralel atölye ile Frege, Russell, erken Wittgenstein ve geç Wittgenstein köprülerini çekirdekten açıkça ayırarak hazırlamak.
5. Tüm aday rota hazır olduğunda A1'den başlayarak uzman, acemi, küçük grup, süre, erişilebilirlik ve uçtan uca öğrenme testlerini yürütmek.
6. Kritik bulguları giderip etkilenen önkoşul zincirlerini yeniden test etmek.
7. Eski ilerleme kayıtlarının geçiş planı ve son regresyon tamamlanınca onaylanan rotayı canlıya almak.

## Yayın kapıları

Faz 3 için “tamamlandı” denebilmesi adına:

- Her dersin açık önkoşulu ve ölçülebilir yetkinliği olmalı.
- Hiçbir çekirdek ders bir önceki derste kurulmamış gösterimi varsaymamalı.
- Her aşamada tanıma sorusundan bağımsız üretim kanıtı bulunmalı.
- Kritik yanlış örneklerin neden yanlış olduğu açıklanmalı.
- Laboratuvarlar klavye ve mobilde tamamlanabilmeli.
- Eski ders bağlantıları veri kaybetmeden yeni karşılıklarına yönlenmeli.
- İlerleme kaydı yeniden sıralamada yanlış derse taşınmamalı.
- Gerçek kullanıcı testinde tekrarlanan kritik belirsizlikler kapatılmalı.
- Bütün proje testleri ve mantık dışı temel kullanıcı akışları geçmeli.

## Kaynaklar

- [forall x: Calgary, güncel HTML içindekiler](https://forallx.openlogicproject.org/html/)
- [Oxford: The Philosophy of Logic and Language](https://www.philosophy.ox.ac.uk/node/98441)
- [Oxford: The Philosophy of Wittgenstein](https://www.philosophy.ox.ac.uk/node/98441)
- [Stanford Encyclopedia of Philosophy: Ludwig Wittgenstein](https://plato.stanford.edu/archives/spr2022/entries/wittgenstein/)
- [Ludwig Wittgenstein Project: Tractatus](https://www.wittgensteinproject.org/w/index.php/Tractatus_Logico-Philosophicus_%28English%29)
- [Ludwig Wittgenstein Project: Philosophische Untersuchungen](https://www.wittgensteinproject.org/w/index.php/Philosophische_Untersuchungen)
- [Retrieval Practice Consistently Benefits Student Learning: systematic review](https://eric.ed.gov/?id=EJ1319572)
- [Mastery Testing and Student Learning: A Meta-Analysis](https://journals.sagepub.com/doi/abs/10.2190/FG7X-7Q9V-JX8M-RDJP)
