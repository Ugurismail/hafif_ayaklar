from copy import deepcopy
from random import SystemRandom


def _question(qid, module_id, prompt, options, correct, explanation):
    return {
        "id": qid,
        "module_id": module_id,
        "prompt": prompt,
        "options": options,
        "correct": correct,
        "explanation": explanation,
    }


LOGIC_LEVEL_TEST_CONFIG = {
    "title": "Mantık Bitirme Testi",
    "subtitle": "Temel ayrımlardan sembolik mantık, aksiyomatik sistem ve metateoriye kadar kurduğun aparatı tek oturumda yoklar.",
    "duration": "70-90 dk",
    "pass_score": 80,
    "pass_correct": 40,
    "instructions": [
        "Test beş modülden oluşur ve her modülde rastgele seçilen sorular bulunur.",
        "Amaç yalnız tanım ezberi değil; sembolleştirme, çıkarım, niceleyici ve metateorik ayrımları birlikte kullanmaktır.",
        "Her modülü ayrı kontrol edebilirsin; en sonda genel başarı oranı hesaplanır.",
    ],
    "focus_points": [
        "Önerme, argüman, geçerlilik ve safsata ayrımlarını karıştırmamak.",
        "Önerme mantığı sembollerini ve kurallarını doğal dil kadar rahat kullanmak.",
        "Niceleyici, kapsam, kimlik ve çeviri sorunlarında formel disiplin göstermek.",
        "Aksiyom, theorem, derived rule ve metateoremi farklı katmanlar olarak görmek.",
    ],
    "modules": [
        {
            "id": "foundations",
            "title": "Temel Ayrımlar ve Argüman",
            "description": "Önerme, argüman, geçerlilik, zorunlu-yeterli koşul ve temel çözümleme becerileri.",
            "sample_size": 10,
        },
        {
            "id": "fallacies",
            "title": "Metin Analizi ve Safsatalar",
            "description": "Sav ayıklama, karşı örnek, açık varsayım, safsata türleri ve kavramsal çerçeve.",
            "sample_size": 10,
        },
        {
            "id": "propositional",
            "title": "Önerme Mantığı ve Türetim",
            "description": "Sembolleştirme, bağlaçlar, doğruluk tabloları, eşdeğerlikler ve çıkarım kuralları.",
            "sample_size": 10,
        },
        {
            "id": "predicate",
            "title": "Yüklem Mantığı ve Çeviri",
            "description": "Niceleyiciler, kapsam, kimlik, function symbols ve doğal dilden sembole geçiş.",
            "sample_size": 10,
        },
        {
            "id": "axiomatic",
            "title": "Aksiyomatik Sistem ve Metateori",
            "description": "Aksiyom şemaları, theorem üretimi, derived rules, soundness, completeness ve sınırlar.",
            "sample_size": 10,
        },
    ],
}


LOGIC_LEVEL_TEST_BANK = [
    _question("logic-foundations-001", "foundations", "Hangisi önerme değildir?", ["Ankara Türkiye'nin başkentidir.", "Lütfen kapıyı kapat.", "2 asal sayıdır.", "Kar yağmaktadır."], "Lütfen kapıyı kapat.", "Emir cümlesi doğruluk değeri taşımaz; bu yüzden önerme değildir."),
    _question("logic-foundations-002", "foundations", "Bir argümanda öncülün temel işi nedir?", ["Sonucu desteklemek", "Soruyu tekrarlamak", "Metni uzatmak", "Sadece örnek vermek"], "Sonucu desteklemek", "Öncül, sonucun lehine gerekçe üreten cümledir."),
    _question("logic-foundations-003", "foundations", "Geçerli ama sağlam olmayan argüman için en doğru ifade hangisidir?", ["Biçim iyi, en az bir öncül sorunlu", "Biçim bozuk, sonuç doğru", "Bütün öncüller doğru, sonuç yanlış", "Sadece sembolik olarak okunabilir"], "Biçim iyi, en az bir öncül sorunlu", "Sağlamlık için hem geçerlilik hem de doğru öncüller gerekir."),
    _question("logic-foundations-004", "foundations", "'Yalnızca çalışırsan geçersin' ifadesi mantıksal olarak en iyi nasıl okunur?", ["Geçmek çalışmak için yeterlidir", "Çalışmak geçmek için zorunludur", "Çalışmak geçmek için yeterlidir", "Geçmek ile çalışmak eşdeğerdir"], "Çalışmak geçmek için zorunludur", "'Only if' yönü zorunlu koşul kurar; geçmek varsa çalışma da vardır."),
    _question("logic-foundations-005", "foundations", "Aşağıdakilerden hangisi zorunlu koşul örneğidir?", ["Oksijen varsa ateş vardır", "Ateş için oksijen gerekir", "Oksijen ateş için yeterlidir", "Ateş ve oksijen eşdeğerdir"], "Ateş için oksijen gerekir", "'Gerekir' dili zorunlu koşulu işaret eder."),
    _question("logic-foundations-006", "foundations", "Bir metinde sonuç cümlesini bulurken en güvenilir ölçüt hangisidir?", ["En uzun cümle olması", "Desteklenmek istenen ana iddia olması", "Son cümle olması", "Örnek içermesi"], "Desteklenmek istenen ana iddia olması", "Sonuç, metnin savunmak istediği ana iddiadır; konumu tek başına yeterli ölçüt değildir."),
    _question("logic-foundations-007", "foundations", "Karşı örnek neyi göstermeye yarar?", ["Argümanın sesini güzelleştirmeyi", "Genel iddianın her durumda işlemediğini", "Sonucun her zaman doğru olduğunu", "Aksiyomatik sistem kurmayı"], "Genel iddianın her durumda işlemediğini", "Tek bir uygun karşı örnek evrensel iddiayı yıkabilir."),
    _question("logic-foundations-008", "foundations", "'Bütün insanlar ölümlüdür. Sokrates insandır. O hâlde Sokrates ölümlüdür.' bu argümanın sonucu hangisidir?", ["Bütün insanlar ölümlüdür", "Sokrates insandır", "Sokrates ölümlüdür", "İnsan olmak ölümlü olmaktır"], "Sokrates ölümlüdür", "İlk iki cümle destek, son cümle sonuçtur."),
    _question("logic-foundations-009", "foundations", "'Bu yanlıştır.' ifadesi neden problemli olabilir?", ["Çünkü çok kısadır", "Çünkü bağlam olmadan neye gönderdiği belirsizdir", "Çünkü soru cümlesidir", "Çünkü daima doğrudur"], "Çünkü bağlam olmadan neye gönderdiği belirsizdir", "Gösterici ve anaforik ifadeler bağlamdan kopunca mantıksal nesnesini yitirir."),
    _question("logic-foundations-010", "foundations", "Geçerlilik hangi şeyi yasaklar?", ["Öncüller yanlış, sonuç doğru satırını", "Öncüller doğru, sonuç yanlış durumunu", "Sonucun doğru olduğu her satırı", "Bütün çelişkileri"], "Öncüller doğru, sonuç yanlış durumunu", "Geçerlilik tam olarak bu tür karşı durumu yasaklar."),
    _question("logic-foundations-011", "foundations", "Bir argümanın 'sağlam' olması için ne gerekir?", ["Sadece sonuç doğru olsun", "Sadece öncüller çok olsun", "Geçerli olması ve öncüllerinin doğru olması", "Doğal dilde yazılmış olması"], "Geçerli olması ve öncüllerinin doğru olması", "Sağlamlık geçerlilik + doğru öncüller birleşimidir."),
    _question("logic-foundations-012", "foundations", "Aşağıdakilerden hangisi açık varsayım yerine geçmez?", ["Metinde hiç yazılmamış ama akışı taşıyan kabul", "Argümanın işlemesi için sessizce kullanılan ilke", "Sonuç cümlesinin kendisi", "Bağlamdan devralınan ama savunulmamış ön kabul"], "Sonuç cümlesinin kendisi", "Açık varsayım, sonucu taşıyan ama açıkça savunulmayan arka kabulün adıdır."),

    _question("logic-fallacies-001", "fallacies", "Ad hominem safsatasının çekirdeği nedir?", ["Kişinin iddiasını değil karakterini hedef almak", "Örnek vermek", "Koşul kurmak", "Tümel niceleyici kullanmak"], "Kişinin iddiasını değil karakterini hedef almak", "Argümanın kendisi yerine kişiye saldırmak konu kaydırır."),
    _question("logic-fallacies-002", "fallacies", "Yanlış ikilem ne yapar?", ["Gereksiz uzun konuşur", "Sadece iki seçenek varmış gibi sunar", "Kanıtı gizler", "Doğruluk tablosu çizer"], "Sadece iki seçenek varmış gibi sunar", "Ara seçenekler veya alternatifler bastırılır."),
    _question("logic-fallacies-003", "fallacies", "Kaygan zemin safsatasında tipik hata nedir?", ["Her adımı bağımsız kanıtlamak", "Zayıf ilk adımdan zincirleme felaket çıkarmak", "Tanım yapmak", "Örneği sonuç sanmak"], "Zayıf ilk adımdan zincirleme felaket çıkarmak", "Aradaki geçişler gerekçelendirilmeden büyüyen korku zinciri kurulur."),
    _question("logic-fallacies-004", "fallacies", "Saman adam safsatası hangi durumda oluşur?", ["Rakibin tezini güçlendirince", "Rakibin tezini karikatürleştirip onu çürütünce", "Sonucu açık yazınca", "Karşı örnek verince"], "Rakibin tezini karikatürleştirip onu çürütünce", "Gerçek tez değil, zayıflatılmış kopya hedef alınır."),
    _question("logic-fallacies-005", "fallacies", "Döngüsel gerekçe neyi bozar?", ["Yazım düzenini", "Sonucu öncüllerde gizleyerek bağımsız destek üretme işini", "Sembolleştirmeyi", "Çeviri kurallarını"], "Sonucu öncüllerde gizleyerek bağımsız destek üretme işini", "Sonuç, gerçekten desteklenmek yerine öncüllerde yeniden paketlenir."),
    _question("logic-fallacies-006", "fallacies", "Otoriteye başvuru ne zaman safsataya dönüşür?", ["Her uzman adı geçtiğinde", "Uzmanlık alanı ilgisizken veya otorite tek kanıt yerine konduğunda", "Kaynak verildiğinde", "Bir kitap adı anıldığında"], "Uzmanlık alanı ilgisizken veya otorite tek kanıt yerine konduğunda", "Uzmanlık ilişkisizse yahut argüman yerine ikame ediliyorsa sorun doğar."),
    _question("logic-fallacies-007", "fallacies", "Neden-sonuç karışıklığında tipik hata hangisidir?", ["Sırf birlikte göründüler diye biri ötekine neden sanmak", "Aksiyom kurmak", "Negasyon eklemek", "Tanımı daraltmak"], "Sırf birlikte göründüler diye biri ötekine neden sanmak", "Korelasyon nedensellik değildir."),
    _question("logic-fallacies-008", "fallacies", "Bir paragrafta örnek cümleyi sonuçtan ayırmanın iyi yolu nedir?", ["Örneklerin genelde tek başına savunulmak istenmemesi", "Örneklerin her zaman ilk cümle olması", "Sonucun mutlaka italik yazılması", "Örneklerin niceleyici içermesi"], "Örneklerin genelde tek başına savunulmak istenmemesi", "Örnek, savı göstermek içindir; savın kendisi değildir."),
    _question("logic-fallacies-009", "fallacies", "Açık varsayım neden önemlidir?", ["Çünkü metni kısaltır", "Çünkü görünmez destek ayağını açığa çıkarır", "Çünkü tüm safsataları çözer", "Çünkü her zaman doğrudur"], "Çünkü görünmez destek ayağını açığa çıkarır", "Metin çoğu zaman argümanı sessiz kabuller üstünden yürütür."),
    _question("logic-fallacies-010", "fallacies", "Kavramsal çerçeve sorunu hangi durumda ortaya çıkar?", ["Terimler kaydırılarak tartışma başka bir şeye çevrilince", "Bir sayı yanlış yazılınca", "Doğruluk tablosu eksik olunca", "Bir örnek verildiğinde"], "Terimler kaydırılarak tartışma başka bir şeye çevrilince", "Aynı sözcükle farklı kavramlar işlendiğinde tartışma kayar."),
    _question("logic-fallacies-011", "fallacies", "Karşı örnek kurmanın en güçlü etkisi nedir?", ["Metni uzatması", "Evrensel bir iddiayı tek vakayla sarsabilmesi", "Aksiyom üretmesi", "Sembolleştirmeyi kaldırması"], "Evrensel bir iddiayı tek vakayla sarsabilmesi", "'Her zaman' türü tezler tek uygun karşı örnekle düşebilir."),
    _question("logic-fallacies-012", "fallacies", "Yanlış ikilem ile kaygan zemin arasındaki fark nedir?", ["Biri seçenekleri daraltır, öteki zayıf zincir büyütür", "İkisi tamamen aynıdır", "Biri sembolik, diğeri doğal dildir", "Biri theorem, diğeri aksiyomdur"], "Biri seçenekleri daraltır, öteki zayıf zincir büyütür", "Yanlış ikilem alternatifleri bastırır; kaygan zemin ardışık felaket üretir."),

    _question("logic-propositional-001", "propositional", "'Eğer yağmur yağarsa yol ıslanır' cümlesinin en iyi sembolleştirmesi hangisidir?", ["p ∧ q", "p → q", "p ↔ q", "¬p ∨ q ∨ r"], "p → q", "Koşullu yapı standart olarak p → q ile gösterilir."),
    _question("logic-propositional-002", "propositional", "¬(p ∧ q) ile eşdeğer ifade hangisidir?", ["¬p ∧ ¬q", "¬p ∨ ¬q", "p ∨ q", "p → q"], "¬p ∨ ¬q", "De Morgan kuralına göre birleşimin inkârı ayrık inkâra açılır."),
    _question("logic-propositional-003", "propositional", "İki atomik önerme için doğruluk tablosu kaç satırdır?", ["2", "3", "4", "8"], "4", "n atomik önermede satır sayısı 2^n olur; burada 2² = 4."),
    _question("logic-propositional-004", "propositional", "Modus ponens kalıbı hangisidir?", ["p→q, p ⟹ q", "p→q, q ⟹ p", "p∨q, ¬p ⟹ ¬q", "p∧q ⟹ ¬p"], "p→q, p ⟹ q", "Koşul ve ön bileşenin doğrulanması son bileşeni verir."),
    _question("logic-propositional-005", "propositional", "Disjunctive syllogism hangi kalıptır?", ["p∨q, ¬p ⟹ q", "p→q, ¬q ⟹ ¬p", "p∧q ⟹ p", "p↔q ⟹ p∨q"], "p∨q, ¬p ⟹ q", "Bir disjunkt elenince öteki kalır."),
    _question("logic-propositional-006", "propositional", "'p only if q' nasıl okunur?", ["p → q", "q → p", "p ∧ q", "p ↔ q"], "p → q", "'only if' yönü sonuç tarafına q'yu yerleştirir."),
    _question("logic-propositional-007", "propositional", "Tautology için en iyi tanım hangisidir?", ["Her satırda yanlış olan formül", "En az bir satırda doğru olan formül", "Her satırda doğru olan formül", "Yalnız iki satırlı formül"], "Her satırda doğru olan formül", "Tautology bütün yorumlarda doğrudur."),
    _question("logic-propositional-008", "propositional", "Contradiction nedir?", ["Her yorumda doğru formül", "Bazı yorumlarda doğru formül", "Her yorumda yanlış formül", "Koşullu her formül"], "Her yorumda yanlış formül", "Çelişki hiçbir yorumda doğrulanmaz."),
    _question("logic-propositional-009", "propositional", "p ↔ q genellikle nasıl açılır?", ["(p→q) ∧ (q→p)", "p∨q", "¬p→¬q", "p∧¬q"], "(p→q) ∧ (q→p)", "Çift yönlülük iki koşulun birleşimi olarak analiz edilir."),
    _question("logic-propositional-010", "propositional", "Ana bağlacı bulmak niçin önemlidir?", ["Formülü kısaltmak için", "Son değerlendirmenin hangi işleç altında yapılacağını belirlemek için", "Niceleyiciyi silmek için", "Sadece estetik için"], "Son değerlendirmenin hangi işleç altında yapılacağını belirlemek için", "Doğruluk tablosu ve dönüşüm stratejisi ana bağlaçtan başlar."),
    _question("logic-propositional-011", "propositional", "Aşağıdakilerden hangisi geçerli bir eşdeğerliktir?", ["p→q ≡ q→p", "¬¬p ≡ p", "p∨q ≡ p∧q", "p↔q ≡ p→q"], "¬¬p ≡ p", "Çift olumsuzluk kuralı geçerlidir; ötekiler genel olarak yanlıştır."),
    _question("logic-propositional-012", "propositional", "Bir argümanın truth-table ile geçersizliği nasıl gösterilir?", ["Her satırda sonuç doğru çıkarsa", "Öncüller doğruyken sonuç yanlış olan en az bir satır bulunursa", "İki satır aynıysa", "Çelişki çıkarsa"], "Öncüller doğruyken sonuç yanlış olan en az bir satır bulunursa", "Tek bir karşı-satır geçersizliği göstermeye yeter."),

    _question("logic-predicate-001", "predicate", "'Bütün filozoflar ölümlüdür' cümlesinin en iyi çevirisi hangisidir?", ["∀x(Fx → Ox)", "∃x(Fx ∧ Ox)", "∀x(Fx ∧ Ox)", "∃x(Fx → Ox)"], "∀x(Fx → Ox)", "Sınıf cümlelerinde standart çözüm koşullu tümeldir."),
    _question("logic-predicate-002", "predicate", "'Bazı öğrenciler çalışkandır' için en uygun çeviri hangisidir?", ["∀x(Sx → Cx)", "∃x(Sx ∧ Cx)", "∃x(Sx → Cx)", "∀x(Sx ∧ Cx)"], "∃x(Sx ∧ Cx)", "Varlık + özellik birleşimi existential conjunction ile kurulur."),
    _question("logic-predicate-003", "predicate", "¬∀xFx hangi ifadeye denktir?", ["∀x¬Fx", "∃x¬Fx", "¬∃xFx", "∃xFx"], "∃x¬Fx", "Tümelin inkârı, karşı örnek varlığına döner."),
    _question("logic-predicate-004", "predicate", "¬∃xFx hangi ifadeye denktir?", ["∃x¬Fx", "¬∀xFx", "∀x¬Fx", "∀xFx"], "∀x¬Fx", "Varoluşun inkârı tümel inkâra çevrilir."),
    _question("logic-predicate-005", "predicate", "'Her doktor bir hastayı muayene eder' cümlesinde en kritik sorun nedir?", ["Çevirilemez olması", "Niceleyici kapsamının belirsiz olabilmesi", "Yalnız iki sembol gerektirmesi", "Kimlik zorunlu olması"], "Niceleyici kapsamının belirsiz olabilmesi", "Her doktor aynı hastayı mı, kendi hastasını mı muayene ediyor sorusu kapsam farkıdır."),
    _question("logic-predicate-006", "predicate", "Identity için temel simge hangisidir?", ["≡", "=", "⊨", "↔"], "=", "Kimlik/eşitlik formel dilde '=' ile gösterilir."),
    _question("logic-predicate-007", "predicate", "'Sokrates, Platon değildir' en iyi nasıl yazılır?", ["s = p", "¬(s = p)", "s ↔ p", "¬s = p"], "¬(s = p)", "Kimlik önermesinin inkârı parantezli yazılır."),
    _question("logic-predicate-008", "predicate", "Function symbol neyi temsil eder?", ["Doğruluk değerini", "Bir terim üretici bağıntıyı", "Yalnız niceleyiciyi", "Bir theorem listesini"], "Bir terim üretici bağıntıyı", "Function symbol nesne değil, nesne üreten terim yapısıdır."),
    _question("logic-predicate-009", "predicate", "Prenex normal form'ta ne olur?", ["Bütün niceleyiciler başa toplanır", "Bütün bağlaçlar silinir", "Kimlik yasaklanır", "Tüm terimler eşitlenir"], "Bütün niceleyiciler başa toplanır", "Prenex dönüşüm niceleyici bloğunu formülün önüne taşır."),
    _question("logic-predicate-010", "predicate", "Serbest değişken sorunu neden önemlidir?", ["Yazımı güzelleştirmek için", "Genelleme ve bağlanma hatalarını önlemek için", "Tabloyu kısaltmak için", "Aksiyom saymak için"], "Genelleme ve bağlanma hatalarını önlemek için", "Serbest değişkenler yanlış tümelleştirme ve hatalı okuma üretir."),
    _question("logic-predicate-011", "predicate", "'Yalnız bir kral vardır' gibi ifade hangi sorunu açar?", ["Definite description ve tekillik yükü", "Modus tollens", "Truth-tree kapanışı", "Double negation"], "Definite description ve tekillik yükü", "'The' yapıları varlık ve tekillik yükü taşır."),
    _question("logic-predicate-012", "predicate", "Universal instantiation kabaca ne yapar?", ["Bir örnekten tümel üretir", "Tümel önermeden tekil örnek çıkarır", "Kimliği siler", "Ayrık bağlaç kurar"], "Tümel önermeden tekil örnek çıkarır", "∀ ile başlayan ifade uygun terim için örneklenir."),

    _question("logic-axiomatic-001", "axiomatic", "Aksiyom ile theorem arasındaki temel fark nedir?", ["Aksiyom başlangıç, theorem türetilmiş formüldür", "Theorem daha kısadır", "Aksiyom daha doğrudur", "Aralarında fark yoktur"], "Aksiyom başlangıç, theorem türetilmiş formüldür", "Aksiyomlar başlangıç noktası; theorem'ler sistem içinde kanıtlanmış formüllerdir."),
    _question("logic-axiomatic-002", "axiomatic", "Derived rule neyi ifade eder?", ["Keyfî kestirme", "Temel kurallardan kanıtlanabildiği için kısaltma olarak kullanılan kural", "Yeni aksiyom", "Yalnız doğal dil kuralı"], "Temel kurallardan kanıtlanabildiği için kısaltma olarak kullanılan kural", "Derived rule'un meşruiyeti temel düzeyde türetilebilir olmasından gelir."),
    _question("logic-axiomatic-003", "axiomatic", "Soundness neyi garanti eder?", ["Sistem her doğruyu bulur", "Sistem yanlış semantik sonucu türetmez", "Bütün ispatlar kısadır", "Her theorem aksiyomdur"], "Sistem yanlış semantik sonucu türetmez", "Soundness güvenirlik yönüdür: Γ ⊢ φ ise Γ ⊨ φ."),
    _question("logic-axiomatic-004", "axiomatic", "Completeness neyi söyler?", ["Sistem semantik sonucu sentaktik olarak da yakalayabilir", "Sistem daima hızlı çalışır", "Sistem yalnız truth-tree kullanır", "Her aksiyom bağımsızdır"], "Sistem semantik sonucu sentaktik olarak da yakalayabilir", "Γ ⊨ φ ise Γ ⊢ φ yönü completeness'tır."),
    _question("logic-axiomatic-005", "axiomatic", "Compactness hangi fikri taşır?", ["Bütün formüller kısa olur", "Doyurulamazlık sonlu altkümeyle de gösterilebilir", "Her theorem aksiyomdur", "Only if yönü tersine döner"], "Doyurulamazlık sonlu altkümeyle de gösterilebilir", "Compactness, sonsuz küme davranışını sonlu tanıklık fikrine bağlar."),
    _question("logic-axiomatic-006", "axiomatic", "Bağımsızlık neyi tartışır?", ["Bir aksiyomun ötekilerden türetilememesini", "Her aksiyomun theorem olmasını", "Tüm sistemlerin tamamlanamazlığını", "Truth-table sayısını"], "Bir aksiyomun ötekilerden türetilememesini", "Independence, aksiyom kümesinin iç yapısına dair bir metateoremdir."),
    _question("logic-axiomatic-007", "axiomatic", "Aksiyomatik sistemde modus ponens'in yeri nedir?", ["Sıradan örnek", "Merkezi temel çıkarım mekanizması", "Yalnız derived rule", "Niceleyici eşleniği"], "Merkezi temel çıkarım mekanizması", "Hilbert tarzı sistemler çoğu yükü aksiyom şemaları ve MP üstüne kurar."),
    _question("logic-axiomatic-008", "axiomatic", "'p→p' neden pedagojik olarak önemlidir?", ["Çünkü süslüdür", "Basit bir theorem üretiminin nasıl çalıştığını gösterir", "Çünkü predicate logic'tir", "Çünkü asla kanıtlanamaz"], "Basit bir theorem üretiminin nasıl çalıştığını gösterir", "Kısa theorem'ler sistemin üretim mantığını görünür kılar."),
    _question("logic-axiomatic-009", "axiomatic", "Metateori hangi düzeyde konuşur?", ["Tek tek formüllerin içeriği düzeyinde", "Sistemlerin gücü, sınırı ve güvenirliği düzeyinde", "Yalnız yazım düzeyinde", "Yalnız Türkçe çeviri düzeyinde"], "Sistemlerin gücü, sınırı ve güvenirliği düzeyinde", "Metateori formül değil, sistem düzeyi analiz yapar."),
    _question("logic-axiomatic-010", "axiomatic", "Natural deduction ile aksiyomatik sistem arasındaki farkın iyi özeti hangisidir?", ["Biri sentaktik, öteki anlamsal", "Biri kural adımı merkezli, öteki aksiyom şeması + MP merkezli", "Aralarında fark yoktur", "Biri yalnız predicate logic içindir"], "Biri kural adımı merkezli, öteki aksiyom şeması + MP merkezli", "İkisi de biçimsel sistemdir; mimarileri farklıdır."),
    _question("logic-axiomatic-011", "axiomatic", "Theorem library neden önemlidir?", ["Yalnız tarih tutmak için", "Tekrar kullanılan kanıt kalıplarını ekonomik biçimde çağırmak için", "Aksiyomları iptal etmek için", "Semantiği yok etmek için"], "Tekrar kullanılan kanıt kalıplarını ekonomik biçimde çağırmak için", "İleri çalışma theorem ve lemma kütüphanesi üstüne kurulur."),
    _question("logic-axiomatic-012", "axiomatic", "Karar verilebilirlik neyi sorar?", ["Bir karar prosedürü var mı?", "Formül güzel mi?", "Aksiyom bağımsız mı?", "Kimlik sembolü var mı?"], "Bir karar prosedürü var mı?", "Decidability mekanik karar imkânına dair metateorik sorudur."),
]


def _build_assessment_question(item, rng):
    prepared = deepcopy(item)
    options = list(prepared["options"])
    correct = prepared["correct"]
    rng.shuffle(options)
    prepared["options"] = options
    prepared["correct_index"] = options.index(correct)
    return prepared


def get_logic_level_test_bank_size():
    return len(LOGIC_LEVEL_TEST_BANK)


def build_logic_level_test():
    rng = SystemRandom()
    bank = LOGIC_LEVEL_TEST_BANK
    if not bank:
        return None

    exercises = []
    total_questions = 0
    for module in LOGIC_LEVEL_TEST_CONFIG["modules"]:
        pool = [item for item in bank if item["module_id"] == module["id"]]
        sample_size = min(module["sample_size"], len(pool))
        selected = rng.sample(pool, sample_size)
        questions = [_build_assessment_question(item, rng) for item in selected]
        rng.shuffle(questions)
        total_questions += len(questions)
        exercises.append(
            {
                "id": f'logic-level-test-{module["id"]}',
                "type": "single_choice",
                "title": module["title"],
                "description": module["description"],
                "questions": questions,
            }
        )

    return {
        "slug": "mantik-bitirme-testi",
        "title": LOGIC_LEVEL_TEST_CONFIG["title"],
        "subtitle": LOGIC_LEVEL_TEST_CONFIG["subtitle"],
        "duration": LOGIC_LEVEL_TEST_CONFIG["duration"],
        "question_bank_size": len(bank),
        "sample_size": total_questions,
        "pass_score": LOGIC_LEVEL_TEST_CONFIG["pass_score"],
        "pass_correct": LOGIC_LEVEL_TEST_CONFIG["pass_correct"],
        "module_count": len(exercises),
        "instructions": LOGIC_LEVEL_TEST_CONFIG["instructions"],
        "focus_points": LOGIC_LEVEL_TEST_CONFIG["focus_points"],
        "exercises": exercises,
    }
