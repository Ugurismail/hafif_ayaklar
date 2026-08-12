"""Release-candidate content for Phase 3, Stage E of the logic course.

Stage E is developed one lesson at a time. Candidate lessons and strict FOL
fixtures remain isolated from the learner-facing course until the complete
stage passes the gates in ``docs/logic_phase3_stage_e_spec.md``.
"""

from .logic_phase3_stage_a import (
    _lesson,
    _practice,
    _production_task,
    _section,
    _worked,
)


STAGE_E_SOURCE_REFERENCES = {
    "forallx-fol-building-blocks": {
        "title": "forall x: Calgary - Building blocks of FOL",
        "url": "https://forallx.openlogicproject.org/html/Ch23.html",
    },
    "forallx-one-quantifier": {
        "title": "forall x: Calgary - Sentences with one quantifier",
        "url": "https://forallx.openlogicproject.org/html/Ch24.html",
    },
    "forallx-multiple-generality": {
        "title": "forall x: Calgary - Multiple generality",
        "url": "https://forallx.openlogicproject.org/html/Ch25.html",
    },
    "forallx-identity": {
        "title": "forall x: Calgary - Identity",
        "url": "https://forallx.openlogicproject.org/html/Ch26.html",
    },
    "forallx-fol-sentences": {
        "title": "forall x: Calgary - Sentences of FOL",
        "url": "https://forallx.openlogicproject.org/html/Ch27.html",
    },
    "forallx-fol-ambiguity": {
        "title": "forall x: Calgary - Ambiguity",
        "url": "https://forallx.openlogicproject.org/html/Ch29.html",
    },
    "mit-logic-sequence": {
        "title": "MIT OpenCourseWare Logic I - Calendar",
        "url": "https://ocw.mit.edu/courses/24-241-logic-i-fall-2009/pages/calendar/",
    },
}


E27_SIGNATURE = {
    "domain": "atölyedeki insanlar",
    "names": {
        "a": "Ada",
        "b": "Bora",
    },
    "variables": ["x", "y", "z"],
    "predicates": {
        "F": {
            "arity": 1,
            "reading": "x filozof",
        },
        "G": {
            "arity": 1,
            "reading": "x geç kaldı",
        },
    },
}


def _syntax_fixture(
    fixture_id,
    source,
    *,
    accepted,
    category=None,
    issue_code=None,
    explanation,
):
    return {
        "id": fixture_id,
        "source": source,
        "accepted": accepted,
        "expected_category": category,
        "expected_issue_code": issue_code,
        "explanation": explanation,
    }


def _candidate_e27():
    lesson = _lesson(
        "E27",
        "ders-fol-alan-ad-yuklem-acik-formul",
        "Alan, Adlar, Yüklemler ve Açık Formüller",
        "TFL'de tek atom olarak bırakılan bildirimin içini açar; alanı, adları, değişkenleri ve yüklem yerlerini ayırarak atomik FOL cümlesi ile açık formülü birbirine karıştırmadan okur.",
        "FOL'nin yapı taşları ve kategori disiplini",
        35,
        [
            "ders-17-sembollestirmeye-giris",
            "ders-kanit-ve-semantik-gecerlilik-koprusu",
        ],
        [
            "fol.domain_choose",
            "fol.name_distinguish",
            "fol.predicate_key",
            "fol.open_formula_read",
            "fol.tfl_limit_explain",
        ],
        [
            "TFL'nin nesne-yüklem iç yapısını neden koruyamadığını bir argüman üzerinden göstermek.",
            "Söylem alanı, ad, değişken, bir yerli yüklem, terim ve atomik formül kategorilerini ayırmak.",
            "Bir yüklem anahtarını boşluk ve argüman yeri açık olacak biçimde kurmak.",
            "F(a) cümlesiyle F(x) açık formülünü, x'i bilinmeyen bir ad gibi okumadan ayırmak.",
            "Ayrı adların aynı nesneyi gösterebileceğini ve alandaki her nesnenin adlandırılmış olmak zorunda olmadığını açıklamak.",
        ],
        [
            (
                "Söylem alanı",
                "Niceleyicilerin dolaşacağı ve adlar ile yüklemlerin yorumlanacağı, çalışma bağlamında açıkça seçilmiş boş olmayan nesneler kümesi.",
            ),
            (
                "Ad (birey sabiti)",
                "Sembol anahtarında alanın tam bir üyesini gösteren a-r aralığındaki terim.",
            ),
            (
                "Değişken",
                "Tek başına belirli bir nesnenin adı olmayan; sonraki derslerde niceleyici veya atamayla ele alınacak s-z aralığındaki terim.",
            ),
            (
                "Yüklem",
                "Bir veya daha fazla terim yeri bulunan ve bu yerler dolduğunda atomik formül oluşturan ifade şeması.",
            ),
            (
                "Terim",
                "Bu çekirdek dilde bir ad veya değişken olan, yüklemin argüman yerini doldurabilen ifade.",
            ),
            (
                "Atomik formül",
                "Bir yüklemin aritesine uygun terimlerle tamamlanmış en küçük FOL formülü; örneğin F(a) veya F(x).",
            ),
            (
                "Açık formül",
                "En az bir serbest değişken oluşumu taşıdığı için henüz doğru veya yanlış bir FOL cümlesi olmayan formül.",
            ),
            (
                "FOL cümlesi",
                "Serbest değişken oluşumu bulunmayan FOL formülü.",
            ),
        ],
        [
            _section(
                "TFL atomunu neden açıyoruz?",
                "TFL tam cümleler arasındaki doğruluk işlevsel yapıyı korur, fakat cümlenin içindeki nesne-yüklem ortaklığını görünmez bırakır. FOL aynı yüklemin farklı nesnelere uygulanmasını açıkça izler.",
                "Doğal dilde açıkça geçerli görünen bir argüman TFL'de ilgisiz üç cümle harfine dönüşüp yapısını kaybettiğinde.",
                "TFL: A, B ⊢ C · FOL iskeleti: F(a), ∀x(F(x)→G(x)) ⊢ G(a)",
                "TFL sembolleştirmesi kendi çözümleme düzeyinde yanlış değildir; kullandığı atomlar gereken iç yapıyı göstermeye yetmez. FOL, ad ile yüklemi ayırarak ortak F ve G yapısını görünür kılar.",
                "FOL'yi daha süslü bir TFL yazımı sanma. Cümle harfi tam bildirimin yerini tutarken ad yalnız nesneyi, yüklem ise açık bir özellik yerini temsil eder.",
                [
                    (
                        "Ada filozoftur; bütün filozoflar meraklıdır; öyleyse Ada meraklıdır.",
                        "TFL üç ayrı atom görür; FOL Ada'nın aynı iki yüklem altında izlenmesini mümkün kılar.",
                    ),
                    (
                        "A: Ada filozoftur.",
                        "A bir TFL cümlesidir; Ada'nın adı değildir ve içindeki filozofluk yapısını ayrıca göstermez.",
                    ),
                    (
                        "a: Ada · F(x): x filozoftur",
                        "a bir ad, F ise bir yerli yüklemdir; F(a) birlikte atomik cümle oluşturur.",
                    ),
                ],
                (
                    "TFL'nin kaybettiği iç yapıyı ad ve yüklem kategorileriyle açmak.",
                    "TFL örneği geçersiz gösterdi diye doğal dil argümanını da geçersiz saymak.",
                    "Sorun argümanda değil, o argüman için fazla kaba kalan temsil dilindedir.",
                ),
            ),
            _section(
                "Alan çözümlemenin sınırını belirler",
                "Alan, bu problemde niceleyicilerin hangi nesneler üzerinde dolaşacağını ve adların ne tür nesneleri göstereceğini açıklar. Yüklemin kendisi veya yüklemi sağlayan nesneler listesi değildir.",
                "'Herkes', 'bir şey' veya aynı yüklemin farklı türden nesnelere uygulanması ileride formüle dökülmeden önce.",
                "alan: atölyedeki insanlar",
                "Aynı FOL biçimi farklı alan anahtarlarında farklı doğal dil genişliğine sahip olur. Alanı açık yazmak, kısıtlayıcı yüklemi ve bağlamsal varsayımı birbirine karıştırmayı önler.",
                "Alanı yalnız hakkında olumlu yüklem kurulan nesnelerden oluşturma; bir kişinin filozof olmaması onu insanlar alanının dışına çıkarmaz.",
                [
                    (
                        "Alan: atölyedeki insanlar",
                        "Ada, Bora ve adı verilmeyen başka katılımcılar alanın üyeleri olabilir.",
                    ),
                    (
                        "Alan: filozoflar",
                        "Bu seçim mümkündür, fakat 'filozof olma' yüklemini ayrıca kullanma ihtiyacını ve cümlelerin geri okumasını değiştirir.",
                    ),
                    (
                        "Alan: F olanlar",
                        "F yüklemi henüz tanımlanmadan veya bağlam gerekçesi verilmeden yapılan döngüsel bir alan tarifidir.",
                    ),
                ],
                (
                    "Çevrilecek bütün cümleleri kapsayan, açık ve bağlamca gerekçeli bir alan seçmek.",
                    "Alanı yalnız cümlede adı geçen nesneler listesi sanmak.",
                    "Adlandırılmamış alan üyeleri olabilir; alan ile ad envanteri aynı şey değildir.",
                ),
            ),
            _section(
                "Ad bir cümle değildir",
                "a gibi bir ad alanın tek bir üyesini gösterir; doğru veya yanlış olmaz. F(a) gibi bir atomik formülde yüklemin açık yerini doldurduğunda bir cümleye katkı verir.",
                "TFL cümle harfi ile FOL birey sabitini ayırırken ve sembol anahtarı kurarken.",
                "a: Ada · b: Bora · F(a): Ada filozoftur",
                "Adın gönderimde bulunması ile cümlenin doğruluk değeri taşıması farklı kategorilerdir. Ayrıca a ve b'nin farklı yazılması, tek başına farklı kişileri göstermelerini garanti etmez.",
                "a'yı 'Ada filozoftur' tam cümlesinin kısaltması yapma; farklı adlardan otomatik kimliksizlik sonucu çıkarma.",
                [
                    (
                        "a",
                        "Ada'yı gösteren terimdir; tek başına FOL formülü veya doğruluk iddiası değildir.",
                    ),
                    (
                        "F(a)",
                        "F yükleminin tek yeri a ile dolduğu için atomik FOL cümlesidir.",
                    ),
                    (
                        "a: Sabah Yıldızı · b: Akşam Yıldızı",
                        "İki farklı adın aynı gökcismini göstermesi sözdizimce mümkündür; kimlik E32'de açıkça ifade edilir.",
                    ),
                ],
                (
                    "Adı nesne terimi, cümleyi yüklem uygulanmış formül olarak sınıflandırmak.",
                    "Küçük harfi TFL cümle harfinin küçültülmüş sürümü saymak.",
                    "TFL harfi tam cümle; FOL adı ise yüklem yerini dolduran terim kategorisindedir.",
                ),
            ),
            _section(
                "Yüklem açık bir yer taşır",
                "F yüklemi tek başına 'filozoftur' sözcüğü değil, x filozoftur biçiminde hangi argüman yerinin doldurulacağını gösteren bir şemadır.",
                "Doğal dilde ortak özelliği ayırıp farklı terimlere tutarlı biçimde uygularken.",
                "F(x): x filozoftur · F(a) · F(b)",
                "Yüklem anahtarındaki x, belirli bir kişinin adı değil argüman yerini görünür yapan işarettir. Yüklem ancak ilan edilen sayıda terimle tamamlandığında atomik formül üretir.",
                "F'yi tek başına cümle sanma; anahtarda yalnız 'filozof' diye isim verip argüman yerini gizleme; bir yerli F'ye iki terim verme.",
                [
                    (
                        "F(x): x filozoftur",
                        "Bir boşluklu doğal dil yüklemi ve bir yerli FOL yüklemi açıkça eşlenmiştir.",
                    ),
                    (
                        "G(x): x geç kaldı",
                        "G(a), Ada'nın; G(b), Bora'nın geç kaldığını söyler.",
                    ),
                    (
                        "F(a,b)",
                        "F bir yerli ilan edildiği için fazladan terim arite hatasıdır; yanlış ama anlamlı bir cümle değildir.",
                    ),
                ],
                (
                    "Anahtarda her yüklemin argüman yerini ve aritesini açık tutmak.",
                    "Yüklemin kaç terim istediğini kullanım sırasında tahmin etmek.",
                    "Arite sembol anahtarının sabit sözleşmesidir; her formülde yeniden seçilmez.",
                ),
            ),
            _section(
                "Açık formül ile cümleyi ayır",
                "F(a) içindeki a belirli bir alan üyesini gösterdiği için cümledir. F(x) ise x serbest kaldığında hangi nesne hakkında konuşulduğunu sabitlemez; bir yüklemin açık formülüdür.",
                "Değişken içeren bir ifadeye doğruluk değeri vermeden veya onu doğal dil cümlesi diye geri okumadan önce.",
                "F(a): cümle · F(x): açık formül",
                "Değişken 'adı bilinmeyen ama belirli biri' değildir. E28'de niceleyici, E33'te bağlanma kuralları bu açık oluşumun nasıl cümleye dönüştüğünü kesinleştirecektir.",
                "x'i gizemli bir kişinin adı gibi okuyup F(x)'e doğrudan doğru/yanlış deme; açık formülü sözdizimce bozuk sanma.",
                [
                    (
                        "F(a)",
                        "Serbest değişken yoktur; anahtarla 'Ada filozoftur' diye geri okunur.",
                    ),
                    (
                        "F(x)",
                        "Sözdizimce doğru atomik formüldür, fakat x serbest olduğu için cümle değildir.",
                    ),
                    (
                        "(F(x) ∧ G(a))",
                        "Bileşimin bir tarafı kapalı olsa da x serbest kalır; bütün formül açıktır.",
                    ),
                ],
                (
                    "Formülün bütün değişken oluşumlarını denetleyip serbest oluşum varsa açık formül demek.",
                    "İçinde bir ad bulunduğu için bütün formülü otomatik cümle saymak.",
                    "Cümle olma koşulu bazı terimlerin ad olması değil, hiçbir serbest değişken oluşumunun kalmamasıdır.",
                ),
            ),
        ],
        [
            _worked(
                "a",
                "Sembol anahtarında Ada'yı gösteren addır; tek başına formül değildir.",
                "Ad",
            ),
            _worked(
                "x",
                "Belirli bir nesnenin adı değildir; bu aşamada serbest kullanılabilen değişken terimdir.",
                "Değişken",
            ),
            _worked(
                "F",
                "Bir yerli yüklem sembolüdür; argüman yeri doldurulmadan cümle olmaz.",
                "Yüklem",
            ),
            _worked(
                "F(a)",
                "Tanımlı bir yerli yüklem, tanımlı bir adla tamamlanmıştır ve serbest değişken içermez.",
                "FOL cümlesi",
            ),
            _worked(
                "F(x)",
                "Sözdizimce doğru atomik formüldür; x serbest olduğu için açık formüldür.",
                "Açık formül",
            ),
            _worked(
                "F(a,b)",
                "F bir yerli tanımlanmıştır; iki terim verilmesi arite uyuşmazlığıdır.",
                "Arite hatası",
                "bad",
            ),
            _worked(
                "H(a)",
                "H yüklemi anahtarda tanımlı değildir; formüle anlam sonradan tahmin edilemez.",
                "Bilinmeyen yüklem",
                "bad",
            ),
            _worked(
                "F(q)",
                "q aday anahtarda ne ad ne değişken olarak tanımlıdır; bilinmeyen terimdir.",
                "Bilinmeyen terim",
                "bad",
            ),
            _worked(
                "(F(x) ∧ G(a))",
                "G(a) cümle olsa da x serbest kaldığı için bütün birleşim açık formüldür.",
                "Bileşik açık formül",
            ),
        ],
        [
            "TFL cümle harfi ile FOL birey adını aynı kategori sanmak.",
            "Yüklemi tek başına doğru veya yanlış bir cümle diye sınıflandırmak.",
            "Değişkeni adı henüz bilinmeyen belirli bir nesne olarak okumak.",
            "Alanı yalnız adı verilen veya yüklemi sağlayan nesnelerden ibaret sanmak.",
            "Farklı adların zorunlu olarak farklı nesneleri gösterdiğini varsaymak.",
            "Yüklemin aritesini anahtar yerine her kullanımda yeniden belirlemek.",
            "Açık formülü sözdizimsel hata, cümleyi ise yalnız noktalama farkı sanmak.",
        ],
        _practice(
            [
                (
                    "TFL'nin 'A: Ada filozoftur' anahtarında A neyi temsil eder?",
                    ["Ada kişisini", "Filozofluk yüklemini", "Tam bir atomik bildirimi", "Söylem alanını"],
                    "Tam bir atomik bildirimi",
                    "TFL cümle harfi bir kişi veya yüklem değil, bu çözümlemede atomik bırakılan tam cümledir.",
                    "Temel",
                ),
                (
                    "FOL anahtarında 'a: Ada' satırındaki a hangi kategoridedir?",
                    ["Cümle", "Ad/terim", "Yüklem", "Niceleyici"],
                    "Ad/terim",
                    "a alanın belirli bir üyesini gösterir; tek başına doğruluk iddiası değildir.",
                    "Temel",
                ),
                (
                    "'F(x): x filozoftur' anahtarı neyi açıkça gösterir?",
                    ["F'nin tek başına cümle olduğunu", "F'nin bir argüman yeri olan yüklem olduğunu", "x'in Ada'nın başka adı olduğunu", "Alanı yalnız filozofların oluşturduğunu"],
                    "F'nin bir argüman yeri olan yüklem olduğunu",
                    "x boşluğu hangi terim yerinin doldurulacağını görünür kılar.",
                    "Temel",
                ),
                (
                    "F bir yerli ve a tanımlı bir ad ise F(a) nedir?",
                    ["Yalnız terim", "Yalnız yüklem", "Atomik FOL cümlesi", "Sözdizim hatası"],
                    "Atomik FOL cümlesi",
                    "Yüklemin tek yeri tanımlı bir adla dolmuştur ve serbest değişken yoktur.",
                    "Temel",
                ),
                (
                    "F(x) neden bu aşamada cümle değildir?",
                    ["F büyük yazıldığı için", "x serbest değişken olduğu için", "Parantez kullanıldığı için", "Yüklem tek yerli olduğu için"],
                    "x serbest değişken olduğu için",
                    "İfade formüldür, fakat x'i ele alan bir niceleyici henüz yoktur.",
                    "Temel",
                ),
                (
                    "Hangisi alan ile ad envanteri arasındaki doğru ilişkidir?",
                    ["Alan yalnız adı olan nesnelerden oluşur", "Her ad farklı alan üyesi gösterir", "Alanda adı verilmeyen üyeler olabilir", "Alan bir yüklem sembolüdür"],
                    "Alanda adı verilmeyen üyeler olabilir",
                    "FOL adları her nesneyi adlandırmak zorunda değildir.",
                    "Orta",
                ),
                (
                    "a ve b iki farklı ad olduğunda hangisi sözdizimce mümkündür?",
                    ["Mutlaka farklı nesneleri gösterirler", "Aynı nesneyi gösterebilirler", "b değişken olmak zorundadır", "a=b yazılamaz"],
                    "Aynı nesneyi gösterebilirler",
                    "Farklı sembol kullanımı tek başına kimliksizlik garantisi vermez.",
                    "Orta",
                ),
                (
                    "F bir yerli yüklemse F(a,b) için ilk hata sınıfı nedir?",
                    ["Alan hatası", "Arite uyuşmazlığı", "Niceleyici sırası", "Kimlik hatası"],
                    "Arite uyuşmazlığı",
                    "F anahtara göre bir terim ister, iki terim verilmiştir.",
                    "Orta",
                ),
                (
                    "(F(x) ∧ G(a)) formülünün kategorisi nedir?",
                    ["Cümle", "Açık formül", "Yalnız terim", "Yüklem anahtarı"],
                    "Açık formül",
                    "G(a) kapalı olsa da F(x) içindeki x serbest kalır.",
                    "Orta",
                ),
                (
                    "H(a) neden otomatik kabul edilemez?",
                    ["H büyük olduğu için", "a küçük olduğu için", "H'nin aritesi ve okuması sembol anahtarında tanımlı olmadığı için", "Her formül F ile başlamalı olduğu için"],
                    "H'nin aritesi ve okuması sembol anahtarında tanımlı olmadığı için",
                    "Yüklem sözleşmesi formül kullanılırken tahmin edilmez.",
                    "Orta",
                ),
                (
                    "'Alan: atölyedeki insanlar' seçildiğinde F(x): x filozof için hangisi doğrudur?",
                    ["Filozof olmayanlar alan dışındadır", "F alanın kendisidir", "F bazı alan üyelerinin sağlayabileceği bir yüklemdir", "Bütün alan üyeleri F'dir"],
                    "F bazı alan üyelerinin sağlayabileceği bir yüklemdir",
                    "Alan hangi nesnelerden konuşulduğunu, F ise hangi özelliğin ileri sürüldüğünü ayırır.",
                    "İleri",
                ),
                (
                    "FOL'ye geçişte kazanılan temel yapı hangisidir?",
                    ["Her doğal dil ayrıntısının eksiksiz kopyası", "Nesne, yüklem ve ortak argüman yerlerinin görünürlüğü", "Doğruluk tablosunun gereksizleşmesi", "Bütün argümanların otomatik kanıtı"],
                    "Nesne, yüklem ve ortak argüman yerlerinin görünürlüğü",
                    "FOL TFL atomlarının içindeki tekrar eden nesne-yüklem yapısını açar; bütün doğal dil anlamını tüketmez.",
                    "İleri",
                ),
            ]
        ),
        {
            "prompt": "Aşağıdaki altı ifadeyi ad, değişken, yüklem, FOL cümlesi, açık formül veya hatalı dizi olarak sınıflandır; her kararda anahtardaki kategori ya da arite kuralını yaz.",
            "starter": "Önce tek sembolleri kategori olarak ayır. Formüllerde yüklemin aritesini ve bütün değişken oluşumlarını denetle.",
            "checks": [
                "a, ad/terim olarak sınıflandırıldı",
                "x, değişken/terim olarak sınıflandırıldı",
                "F, bir yerli yüklem olarak sınıflandırıldı",
                "F(a), serbest değişkensiz atomik cümle olarak sınıflandırıldı",
                "F(x), serbest x nedeniyle açık formül olarak sınıflandırıldı",
                "F(a,b), F'nin aritesiyle uyuşmadığı için reddedildi",
            ],
            "solution": "a: ad; x: değişken; F: yüklem; F(a): FOL cümlesi; F(x): açık formül; F(a,b): arite uyuşmazlığı nedeniyle hatalı dizi.",
        },
        [
            _production_task(
                "Yeni bağlam için FOL yapı taşı dosyası hazırla: alanı seç, üç ad ve üç bir yerli yüklem tanımla; her kategoriyi örnekleyen cümle/açık formül çiftleri üret ve TFL ile FOL çözümlemelerini karşılaştır.",
                [
                    "Alan çevrilecek bütün cümleleri kapsıyor ve bağlamla gerekçelendirildi.",
                    "Üç adın sağ tarafında nesne, üç yüklemin sağ tarafında açık x yeri bulunuyor.",
                    "Her yüklem için bir adla atomik cümle ve x ile açık formül yazıldı.",
                    "En az bir örnekte iki farklı adın farklı nesneleri göstermesinin neden otomatik olmadığı açıklandı.",
                    "En az bir adlandırılmamış alan üyesi olasılığı belirtildi.",
                    "Bir doğal dil bildiriminin TFL harfi ve FOL atomu karşılaştırılarak kazanılan/kaybedilen yapı yazıldı.",
                    "Bütün örnekler anahtara göre kategori ve arite denetiminden geçirildi.",
                ],
                "Değerlendirme formül sayısına değil, kategori ayrımlarının doğruluğuna, anahtarın geri okunabilirliğine ve TFL/FOL soyutlama farkının açıklanmasına bakar.",
                "Çalışma bağlamı",
                [
                    "Bir araştırma ekibi",
                    "Bir müze sergisi",
                    "Bir şehir meclisi toplantısı",
                    "Bir müzik topluluğu",
                    "Kendi seçtiğin, sınırları açık başka bir bağlam",
                ],
                "Bu görevde niceleyici kullanma; amaç alan, ad, yüklem ve açık formül kategorilerini temiz kurmaktır.",
            ),
        ],
        [
            "Savunulabilir bir alan seçip kapsamını bir cümleyle gerekçelendirme.",
            "En az üç ad ve iki bir yerli yüklemi kategori ve arite bakımından doğru anahtarlama.",
            "Ad, değişken, yüklem, atomik cümle ve açık formülü yeni örneklerde ayırma.",
            "Bir arite ve bir bilinmeyen sembol hatasını ilk hata koduyla onarma.",
            "TFL ile FOL temsilinde korunan ve kaybedilen iç yapıyı açıklama.",
        ],
        [
            "TFL cümle harfi ile FOL adı arasındaki kategori farkı nedir?",
            "F(x) neden sözdizimce doğru olduğu hâlde henüz cümle değildir?",
            "Alan neden yalnız adı verilen veya F yüklemini sağlayan nesneler listesi değildir?",
            "Farklı iki adın farklı nesneleri göstermesi neden otomatik değildir?",
        ],
        "E28'de açık değişken yerlerini ∀ ve ∃ niceleyicileriyle bağlayacak; tümel kısıtlamada koşul, varoluşsal örnekte birleşim kullanımını ayıracağız.",
        [
            "forallx-fol-building-blocks",
            "forallx-fol-sentences",
            "mit-logic-sequence",
        ],
        "Bu derste F(x) açık formülünün modelde ne zaman sağlandığı veya niceleyicilerin doğruluk koşulları öğretilmez. Amaç yalnız dil kategorilerini kurmaktır. Aday gösterim F(a) parantezini zorunlu tutar ve eski canlı Fa kısaltmasına sessizce karışmaz.",
        [
            "ders-26-niceleyicilere-giris",
            "ders-29-kimlik-yuklemler-ve-alan",
            "ders-32-formel-sözdizim-serbest-bagli-degiskenler",
        ],
    )
    lesson["fol_signature"] = E27_SIGNATURE
    lesson["syntax_scope"] = {
        "introduced": [
            "domain",
            "name",
            "variable",
            "unary_predicate",
            "atomic_formula",
            "open_formula",
            "sentence",
        ],
        "review_only": ["¬", "∧", "∨", "→", "↔"],
        "locked_until_later": ["∀", "∃", "=", "multi_place_predicate"],
    }
    lesson["syntax_fixtures"] = [
        _syntax_fixture(
            "e27-name",
            "a",
            accepted=True,
            category="name",
            explanation="a anahtarda Ada'yı gösteren addır.",
        ),
        _syntax_fixture(
            "e27-variable",
            "x",
            accepted=True,
            category="variable",
            explanation="x değişken terimdir; tek başına cümle değildir.",
        ),
        _syntax_fixture(
            "e27-predicate",
            "F",
            accepted=True,
            category="predicate",
            explanation="F anahtarda bir yerli yüklem sembolüdür.",
        ),
        _syntax_fixture(
            "e27-atomic-sentence",
            "F(a)",
            accepted=True,
            category="sentence",
            explanation="Tanımlı bir ad, bir yerli F yükleminin tek yerini doldurur.",
        ),
        _syntax_fixture(
            "e27-open-formula",
            "F(x)",
            accepted=True,
            category="open_formula",
            explanation="x serbest kaldığı için formül cümle değildir.",
        ),
        _syntax_fixture(
            "e27-negated-sentence",
            "¬G(b)",
            accepted=True,
            category="sentence",
            explanation="Bora'nın geç kalmadığını bildiren kapalı cümledir.",
        ),
        _syntax_fixture(
            "e27-compound-open-formula",
            "(F(x) ∧ G(a))",
            accepted=True,
            category="open_formula",
            explanation="G(a) kapalı olsa da F(x) içindeki x serbesttir.",
        ),
        _syntax_fixture(
            "e27-too-many-terms",
            "F(a,b)",
            accepted=False,
            issue_code="predicate.arity_mismatch",
            explanation="F bir yerli olduğu için iki terim kabul etmez.",
        ),
        _syntax_fixture(
            "e27-no-term",
            "F()",
            accepted=False,
            issue_code="predicate.arity_mismatch",
            explanation="F yükleminin tek argüman yeri boş bırakılamaz.",
        ),
        _syntax_fixture(
            "e27-unknown-predicate",
            "H(a)",
            accepted=False,
            issue_code="predicate.unknown",
            explanation="H sembolü anahtarda yüklem olarak tanımlı değildir.",
        ),
        _syntax_fixture(
            "e27-unknown-term",
            "F(q)",
            accepted=False,
            issue_code="term.unknown",
            explanation="q anahtarda ad veya değişken değildir.",
        ),
        _syntax_fixture(
            "e27-term-is-not-formula",
            "a ∧ F(a)",
            accepted=False,
            issue_code="formula.term_without_identity",
            explanation="a terimi tek başına ikili bağlacın cümle bileşeni olamaz.",
        ),
    ]
    return lesson


STAGE_E_CANDIDATE_LESSONS = [
    _candidate_e27(),
]

STAGE_E_CANDIDATE_MAP = {
    lesson["slug"]: lesson
    for lesson in STAGE_E_CANDIDATE_LESSONS
}
