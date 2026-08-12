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


E28_SIGNATURE = {
    "domain": "seminere katılan insanlar",
    "names": {
        "a": "Ada",
        "b": "Bora",
    },
    "variables": ["x", "y", "z"],
    "predicates": {
        "F": {
            "arity": 1,
            "reading": "x araştırmacı",
        },
        "G": {
            "arity": 1,
            "reading": "x meraklı",
        },
        "H": {
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


def _symbolization_fixture(
    fixture_id,
    prompt,
    accepted_readings,
    checks,
    *,
    teaching_point,
):
    """Build one auditable natural-language symbolization fixture."""

    return {
        "id": fixture_id,
        "prompt": prompt,
        "accepted_readings": [
            {
                "source": source,
                "context_condition": context_condition,
                "back_translation": back_translation,
            }
            for source, context_condition, back_translation in accepted_readings
        ],
        "checks": [
            {
                "source": source,
                "accepted": accepted,
                "expected_issue_code": issue_code,
                "explanation": explanation,
            }
            for source, accepted, issue_code, explanation in checks
        ],
        "teaching_point": teaching_point,
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
    lesson["symbolization_fixtures"] = []
    return lesson


def _candidate_e28():
    lesson = _lesson(
        "E28",
        "ders-fol-tek-niceleyicili-cumleler",
        "Tek Niceleyicili Cümleler",
        "Açık formülleri ∀ ve ∃ ile cümleye dönüştürür; tümel kısıtlamada koşulu, varoluşsal ortak özellikte birleşimi ve 'yalnız' ifadesinde doğru koşul yönünü korur.",
        "Tek niceleyici, kısıtlama ve geri okuma",
        40,
        [
            "ders-fol-alan-ad-yuklem-acik-formul",
            "ders-kosul-yalnizca-cift-yonluluk",
        ],
        [
            "fol.universal_restrict",
            "fol.existential_restrict",
            "fol.only_direction",
            "fol.empty_predicate_read",
            "fol.paraphrase_step",
        ],
        [
            "Her F, G'dir cümlesini ∀x(F(x)→G(x)) biçiminde kurup geri okumak.",
            "Bazı F'ler G'dir cümlesini ∃x(F(x)∧G(x)) biçiminde kurup bir tanık iddiası olarak açıklamak.",
            "Hiçbir F, G değildir; bazı F, G değildir ve bütün F'lerin G olduğu doğru değildir kalıplarını kapsamı koruyarak ayırmak.",
            "Yalnız F'ler G'dir cümlesini, her G'nin F olduğunu söyleyen ters yönlü koşul olarak yeniden yazmak.",
            "Tümel kısıtlamanın tek başına F olan bir nesnenin varlığını ileri sürmediğini belirtmek.",
            "Doğal dil cümlesini alan, kısıtlayıcı yüklem, ana yüklem ve niceleyici olarak kademeli çözümlemek.",
        ],
        [
            (
                "Tümel niceleyici (∀)",
                "Seçilen alandaki her nesne için kapsamındaki formülü ileri süren niceleyici.",
            ),
            (
                "Varoluşsal niceleyici (∃)",
                "Seçilen alanda kapsamındaki formülü sağlayan en az bir nesne bulunduğunu ileri süren niceleyici.",
            ),
            (
                "Kısıtlayıcı yüklem",
                "Nicelemenin doğal dilde hangi alt gruba yöneldiğini gösteren F gibi yüklem; söylem alanının kendisi değildir.",
            ),
            (
                "Tümel kısıtlama",
                "Her F için, o nesne F ise G olmasını isteyen ∀x(F(x)→G(x)) yapısı.",
            ),
            (
                "Varoluşsal ortak özellik",
                "Aynı tanığın hem F hem G olmasını isteyen ∃x(F(x)∧G(x)) yapısı.",
            ),
            (
                "Varoluşsal yük",
                "Bir cümlenin belirli türden en az bir nesnenin bulunduğunu da ileri sürmesi.",
            ),
            (
                "Geri çeviri",
                "Formülü sembol anahtarı ve alanla yeniden doğal dile okuyarak kapsam ile yönü denetleme adımı.",
            ),
        ],
        [
            _section(
                "Açık formülden cümleye",
                "F(x) açık formülü x'in hangi nesneler için ele alınacağını söylemez. ∀x ve ∃x, kapsamlarındaki x oluşumlarını bağlayarak serbest değişken bırakmayan FOL cümleleri kurar.",
                "Doğal dilde 'her', 'bütün', 'bazı', 'bir', 'en az bir' veya 'hiçbir' gibi nicelik ifadeleriyle karşılaştığında.",
                "F(x) · ∀xF(x) · ∃xF(x)",
                "Niceleyicinin hemen ardındaki değişken, kapsam içindeki aynı harfli uygun oluşumları bağlar. ∀xF(x) ve ∃xF(x) serbest değişken bırakmaz; ne var ki aynı iddiayı kurmazlar.",
                "∀ ve ∃'ü yalnızca 'güçlü' ve 'zayıf' sözcükler gibi değiştirme; niceleyicinin kapsamı dışında kalan x oluşumlarını bağlı sanma.",
                [
                    (
                        "F(x)",
                        "x serbesttir; sözdizimce formül olsa da henüz FOL cümlesi değildir.",
                    ),
                    (
                        "∀xF(x)",
                        "Alanın her üyesinin F olduğunu söyler ve x'i bağlar.",
                    ),
                    (
                        "∃xF(x)",
                        "Alanda F olan en az bir nesne bulunduğunu söyler ve x'i bağlar.",
                    ),
                ],
                (
                    "Niceleyicinin değişkenini ve kapsamını işaretleyip serbest oluşum kalmadığını denetlemek.",
                    "Formülün başında herhangi bir niceleyici varsa içindeki bütün değişkenleri bağlı saymak.",
                    "Bağlanma harf ve kapsam eşleşmesine bağlıdır; yalnızca niceleyicinin varlığına değil.",
                ),
            ),
            _section(
                "Her F, G'dir: koşul ile kısıtla",
                "Alan seminere katılan bütün insanlarsa 'Her araştırmacı meraklıdır' cümlesi herkesin araştırmacı olduğunu söylemez. Her alan üyesi için, araştırmacı olması durumunda meraklı olmasını ister.",
                "Tümel niceleme alanın yalnız bir alt grubuna yöneliyorsa.",
                "∀x(F(x)→G(x))",
                "Koşulun önbileşeni F, hangi nesnelerin iddiaya tabi olduğunu; artbileşeni G, bu nesneler hakkında ne ileri sürüldüğünü gösterir. F olmayan alan üyelerine G zorunluluğu yüklenmez.",
                "∀x(F(x)∧G(x)) yazma: bu formül alanın her üyesinin hem araştırmacı hem meraklı olduğunu söyleyerek kısıtlamayı kaybeder.",
                [
                    (
                        "Her araştırmacı meraklıdır.",
                        "∀x(F(x)→G(x)): araştırmacılık koşul, meraklılık sonuç yerindedir.",
                    ),
                    (
                        "Bütün geç kalanlar araştırmacıdır.",
                        "∀x(H(x)→F(x)): doğal dilde ilk grup önbileşen olur.",
                    ),
                    (
                        "∀xG(x)",
                        "Alan zaten araştırmacılar olarak seçilmişse 'Her araştırmacı meraklıdır' diye okunabilir; mevcut geniş alanda ise herkesin meraklı olduğunu söyler.",
                    ),
                ],
                (
                    "Önce alanı yazıp 'hangi nesneler için?' sorusunu F ile koşulun soluna yerleştirmek.",
                    "Doğal dilde iki yüklem yan yana geldiği için otomatik olarak birleşim kullanmak.",
                    "Tümel alt grup cümlesinde amaç aynı nesnede iki özellik saymak değil, F olanlara G koşulu getirmektir.",
                ),
            ),
            _section(
                "Bazı F'ler G'dir: aynı tanıkta birleştir",
                "'Bazı araştırmacılar meraklıdır' cümlesi, aynı nesnenin hem F hem G olmasını ister. ∃x(F(x)∧G(x)) bu ortak tanığı açıkça kurar.",
                "En az bir nesnenin iki veya daha fazla özelliği birlikte taşıdığı ileri sürülüyorsa.",
                "∃x(F(x)∧G(x))",
                "∃x bir tanık seçer; birleşim, seçilen aynı tanığın hem araştırmacı hem meraklı olmasını ister. 'Bazı' burada en az bir demektir; tam olarak bir veya çoğu demek değildir.",
                "∃x(F(x)→G(x)) kullanma: koşul yapısı, seçilen nesnenin F olmasını birlikte ileri sürmez ve hedeflenen tanık yapısını kaybeder.",
                [
                    (
                        "Bazı araştırmacılar meraklıdır.",
                        "∃x(F(x)∧G(x)): aynı x iki yüklemi birlikte taşır.",
                    ),
                    (
                        "En az bir meraklı insan geç kaldı.",
                        "∃x(G(x)∧H(x)): alan insanlardan oluştuğu için ayrı bir insan yüklemi gerekmez.",
                    ),
                    (
                        "Bazı araştırmacılar meraklı değildir.",
                        "∃x(F(x)∧¬G(x)): olumsuzluk yalnız G yüklemine uygulanır.",
                    ),
                ],
                (
                    "∃'ten sonra aynı tanığın taşıması gereken özellikleri birleşimle yazmak.",
                    "∃'ten sonra koşul kullanıp F tanığı bulunduğunu ileri sürdüğünü sanmak.",
                    "Varoluşsal örnekte iki yüklemin aynı nesne için birlikte ileri sürülmesi gerekir.",
                ),
            ),
            _section(
                "'Yalnız' koşul yönünü değiştirir",
                "'Yalnız araştırmacılar meraklıdır' cümlesi her araştırmacının meraklı olduğunu değil, meraklı olan herkesin araştırmacı olduğunu söyler.",
                "'Yalnız', 'ancak', 'sadece' veya '-den başkası ... değil' yapıları gruplar arasında gerekli koşul kuruyorsa.",
                "Yalnız F'ler G'dir ⇒ ∀x(G(x)→F(x))",
                "G olmak F olmayı gerektirir; bu nedenle G yeterli taraf olarak önbileşene, F gerekli taraf olarak artbileşene gelir. Cümle tek başına her F'nin G olduğunu ileri sürmez.",
                "Sözcük sırasını kopyalayıp ∀x(F(x)→G(x)) yazma; bu ters formül araştırmacı olmayan meraklıları dışlamaz.",
                [
                    (
                        "Yalnız araştırmacılar meraklıdır.",
                        "Açık yeniden yazım: Birisi meraklıysa araştırmacıdır; ∀x(G(x)→F(x)).",
                    ),
                    (
                        "Araştırmacılardan başkası meraklı değildir.",
                        "Meraklı olmak araştırmacı olmayı gerektirir; yine ∀x(G(x)→F(x)).",
                    ),
                    (
                        "Her araştırmacı meraklıdır ve yalnız araştırmacılar meraklıdır.",
                        "Bu iki ayrı yön birlikte gerekir; çift yönlülük tek 'yalnız' cümlesinden çıkmaz.",
                    ),
                ],
                (
                    "Cümleyi önce 'G olan herkes F'dir' diye açıp sonra koşul yönünü kurmak.",
                    "'Yalnız' sözcüğünün hemen ardındaki grubu otomatik önbileşen yapmak.",
                    "'Yalnız F' ifadesi F'yi gerekli koşul yapar; gerekli koşul artbileşene yerleşir.",
                ),
            ),
            _section(
                "Hiçbiri, bazısı değil ve hepsi değil",
                "Olumsuzluğun yeri nicelik iddiasını değiştirir. 'Hiçbir F, G değildir' her F'yi G dışında tutar; 'Bazı F, G değildir' bir karşı örnek tanığı ister; 'Bütün F'lerin G olduğu doğru değildir' bütün tümel iddiayı yadsır.",
                "Doğal dilde olumsuzluk niceleyiciye mi, ana yükleme mi uygulanıyor diye karar verirken.",
                "∀x(F(x)→¬G(x)) · ∃x(F(x)∧¬G(x)) · ¬∀x(F(x)→G(x))",
                "Bu üç formülün yüzeyinde aynı F ve G bulunsa da iddia güçleri farklıdır. E31'de niceleyici olumsuzlamalarının eşdeğer biçimleri gerekçelendirilecektir; burada yalnız doğru kapsam korunur.",
                "'Hepsi G değil' ile 'hepsi G olmayan' ifadelerini aynı sanma. Belirsiz bir doğal dil cümlesini doğrudan sembolleştirmek yerine açık yeniden yazım iste.",
                [
                    (
                        "Hiçbir araştırmacı meraklı değildir.",
                        "∀x(F(x)→¬G(x)): her araştırmacı için meraklılık reddedilir.",
                    ),
                    (
                        "Bazı araştırmacılar meraklı değildir.",
                        "∃x(F(x)∧¬G(x)): F olup G olmayan en az bir tanık vardır.",
                    ),
                    (
                        "Bütün araştırmacıların meraklı olduğu doğru değildir.",
                        "¬∀x(F(x)→G(x)): olumsuzluk tüm tümel cümleyi kapsar.",
                    ),
                ],
                (
                    "Olumsuz doğal dil cümlesini önce açık bir 'hiçbiri', 'bazısı ... değil' veya 'hepsi olduğu doğru değil' biçimine dönüştürmek.",
                    "Olumsuzluk işaretini formülün herhangi bir yerine koyup cümlenin aynı kaldığını varsaymak.",
                    "Olumsuzluğun kapsamı hangi nicelik iddiasının reddedildiğini belirler.",
                ),
            ),
            _section(
                "Tümel cümle varoluş eklemez",
                "∀x(F(x)→G(x)) her F için bir koşul koyar; F olan en az bir nesne bulunduğunu ayrıca ileri sürmez. Buna karşılık ∃x(F(x)∧G(x)) açık bir F tanığı ister.",
                "Tümel bir ifadeden belirli türden nesnelerin bulunduğu sonucunu çıkarıp çıkaramayacağını denetlerken.",
                "∀x(F(x)→G(x)) ⊬ ∃xF(x)",
                "Klasik FOL'nin standart kullanımında tümel kısıtlama varoluşsal yük taşımaz. Bu ders model hesabı yapmaz; yalnız formülün hangi iddiayı açıkça kurmadığını ayırır.",
                "Gündelik dilde konu edilen grubun var olduğu sezgisini formülün mantıksal içeriğine sessizce ekleme.",
                [
                    (
                        "Bütün tek boynuzlu atlar meraklıdır.",
                        "Tümel biçim tek başına tek boynuzlu at bulunduğunu ileri sürmez.",
                    ),
                    (
                        "Bazı tek boynuzlu atlar meraklıdır.",
                        "Varoluşsal biçim en az bir tek boynuzlu at tanığı ileri sürer.",
                    ),
                    (
                        "Her araştırmacı meraklıdır; demek ki bir araştırmacı vardır.",
                        "Sonuç için ayrı bir varoluş öncülü gerekir; tümel cümle tek başına yetmez.",
                    ),
                ],
                (
                    "Formülde bir tanık ileri süren ∃ bulunup bulunmadığını ayrıca denetlemek.",
                    "Doğal dilde grubun adı geçtiği için o gruptan en az bir nesnenin varlığını mantıksal olarak varsaymak.",
                    "Söz konusu olma ile varoluşsal tanık ileri sürme aynı işlem değildir.",
                ),
            ),
        ],
        [
            _worked(
                "Her araştırmacı meraklıdır.",
                "Alan seminere katılan bütün insanlardır; F alt grubunu koşulla kısıtlarız.",
                "∀x(F(x)→G(x))",
            ),
            _worked(
                "Bazı araştırmacılar meraklıdır.",
                "Aynı tanığın hem F hem G olması gerekir.",
                "∃x(F(x)∧G(x))",
            ),
            _worked(
                "Hiçbir araştırmacı meraklı değildir.",
                "Her F için G reddedilir; olumsuzluk ana yüklemdedir.",
                "∀x(F(x)→¬G(x))",
            ),
            _worked(
                "Bazı araştırmacılar meraklı değildir.",
                "F olan ve G olmayan en az bir ortak tanık istenir.",
                "∃x(F(x)∧¬G(x))",
            ),
            _worked(
                "Yalnız araştırmacılar meraklıdır.",
                "Meraklı olmak araştırmacı olmayı gerektirir; G'den F'ye gideriz.",
                "∀x(G(x)→F(x))",
            ),
            _worked(
                "Bütün araştırmacıların meraklı olduğu doğru değildir.",
                "Olumsuzluk yalnız G'ye değil, bütün tümel iddiaya uygulanır.",
                "¬∀x(F(x)→G(x))",
            ),
            _worked(
                "∀x(F(x)∧G(x))",
                "Bu, yalnız araştırmacıları değil alandaki herkesi hem F hem G yapar; tümel alt grup çevirisi değildir.",
                "Kısıtlama kaybı",
                "bad",
            ),
            _worked(
                "∃x(F(x)→G(x))",
                "Koşul, seçilen tanığın F olduğunu ortak özellik olarak ileri sürmez; 'bazı F, G'dir' yapısı kaybolur.",
                "Yanlış bağlaç",
                "bad",
            ),
            _worked(
                "∀x(F(x)→G(x))",
                "'Yalnız araştırmacılar meraklıdır' için bu yön tersidir; G olanların F olması gerekir.",
                "Yön hatası",
                "bad",
            ),
            _worked(
                "F(x)",
                "x serbest bırakıldığı için doğal dildeki kapalı cümleyi henüz sembolleştirmez.",
                "Serbest değişken",
                "bad",
            ),
        ],
        [
            "Tümel kısıtlamada koşul yerine birleşim kullanmak.",
            "Varoluşsal ortak tanıkta birleşim yerine koşul kullanmak.",
            "'Yalnız F'ler G'dir' cümlesini F'den G'ye koşul diye ters çevirmek.",
            "∃ niceleyicisini 'tam olarak bir' veya 'çoğu' diye okumak.",
            "Tümel cümleden sessizce F nesnelerinin varlığını çıkarmak.",
            "Söylem alanı ile doğal dildeki F kısıtlayıcısını aynı şey sanmak.",
            "'Hiçbiri G değil' ile 'hepsinin G olduğu doğru değil' kapsamlarını birleştirmek.",
            "Formülü geri okumadan yalnız sembol kalıbına bakarak onaylamak.",
        ],
        _practice(
            [
                (
                    "Alan seminere katılan insanlarsa 'Her araştırmacı meraklıdır' hangisidir?",
                    ["∀x(F(x)→G(x))", "∀x(F(x)∧G(x))", "∃x(F(x)∧G(x))", "∃x(F(x)→G(x))"],
                    "∀x(F(x)→G(x))",
                    "F olan alan üyeleri koşulla G'ye kısıtlanır.",
                    "Temel",
                ),
                (
                    "'Bazı araştırmacılar meraklıdır' için neden ∧ kullanılır?",
                    ["Aynı tanık hem F hem G olmalıdır", "Bütün nesneler F olmalıdır", "G, F için gerekli koşuldur", "∃ her zaman ∧ ile yazılır"],
                    "Aynı tanık hem F hem G olmalıdır",
                    "Birleşim niceleyiciden dolayı ezbere değil, ortak tanık yapısından dolayı seçilir.",
                    "Temel",
                ),
                (
                    "∀xF(x) formülünde x'in durumu nedir?",
                    ["Serbesttir", "∀x tarafından bağlıdır", "Bir addır", "Yüklemdir"],
                    "∀x tarafından bağlıdır",
                    "Niceleyici kapsamındaki aynı değişken oluşumunu bağlar.",
                    "Temel",
                ),
                (
                    "∃x(F(x)∧G(x)) için en dikkatli geri okuma hangisidir?",
                    ["Tam olarak bir araştırmacı meraklıdır", "En az bir araştırmacı meraklıdır", "Araştırmacıların çoğu meraklıdır", "Her araştırmacı meraklıdır"],
                    "En az bir araştırmacı meraklıdır",
                    "∃ en az bir tanık ileri sürer; sayıyı bire veya çoğunluğa sabitlemez.",
                    "Temel",
                ),
                (
                    "'Yalnız araştırmacılar meraklıdır' cümlesinin açık yeniden yazımı hangisidir?",
                    ["Birisi araştırmacıysa meraklıdır", "Birisi meraklıysa araştırmacıdır", "Birisi araştırmacıysa ve ancak o zaman meraklıdır", "Bazı meraklılar araştırmacıdır"],
                    "Birisi meraklıysa araştırmacıdır",
                    "Yalnız F ifadesi F'yi G olmanın gerekli koşulu yapar.",
                    "Orta",
                ),
                (
                    "Hiçbir araştırmacı meraklı değildir hangisidir?",
                    ["∀x(F(x)→¬G(x))", "¬∀x(F(x)→G(x))", "∃x(F(x)∧¬G(x))", "∀x(¬F(x)→G(x))"],
                    "∀x(F(x)→¬G(x))",
                    "Her F için G reddedilir; bu yalnızca tümel iddianın reddi değildir.",
                    "Orta",
                ),
                (
                    "'Bazı araştırmacılar meraklı değildir' hangisidir?",
                    ["∃x(F(x)∧¬G(x))", "∃x(F(x)→¬G(x))", "∀x(F(x)→¬G(x))", "¬∃x(F(x)∧G(x))"],
                    "∃x(F(x)∧¬G(x))",
                    "Aynı tanık F olmalı ve G olmamalıdır.",
                    "Orta",
                ),
                (
                    "∀x(F(x)∧G(x)) neden 'Her araştırmacı meraklıdır' değildir?",
                    ["x serbest kaldığı için", "Alandaki herkesi hem F hem G yaptığı için", "∧ yalnızca TFL'de kullanıldığı için", "∀ varoluş bildirdiği için"],
                    "Alandaki herkesi hem F hem G yaptığı için",
                    "Birleşim F olmayan alan üyelerini kısıtlama dışında bırakmaz.",
                    "Orta",
                ),
                (
                    "∀x(F(x)→G(x)) cümlesi tek başına hangisini ileri sürmez?",
                    ["F olanların G olması gerektiğini", "F olan en az bir nesne bulunduğunu", "x'in niceleyiciye bağlı olduğunu", "G'nin F için artbileşen olduğunu"],
                    "F olan en az bir nesne bulunduğunu",
                    "Tümel kısıtlama ayrı bir varoluş tanığı ileri sürmez.",
                    "Orta",
                ),
                (
                    "Alan yalnızca araştırmacılar olarak değiştirilirse ∀xG(x) nasıl okunabilir?",
                    ["Her araştırmacı meraklıdır", "Bazı araştırmacılar meraklıdır", "Yalnız araştırmacılar meraklıdır", "Hiçbir araştırmacı meraklı değildir"],
                    "Her araştırmacı meraklıdır",
                    "Alan daraltıldığında F kısıtı anahtara gömülür; aynı formül farklı alanla farklı geri okunur.",
                    "İleri",
                ),
                (
                    "'Bütün araştırmacıların meraklı olduğu doğru değildir' ile 'Hiçbir araştırmacı meraklı değildir' neden ayrıdır?",
                    ["Birincisi yalnızca tümel iddiayı reddeder, ikincisi her F için G'yi reddeder", "Birincisi ∃ kullanır, ikincisi hiç niceleyici kullanmaz", "Birincisi yalnızca adlara uygulanır", "Aralarında fark yoktur"],
                    "Birincisi yalnızca tümel iddiayı reddeder, ikincisi her F için G'yi reddeder",
                    "Olumsuzluğun tüm niceleyicili cümleyi mi, ana yüklemi mi kapsadığı iddia gücünü değiştirir.",
                    "İleri",
                ),
                (
                    "Bir sembolleştirmeyi son kez denetlemenin en güvenli yolu hangisidir?",
                    ["Sembol sayısını doğal dildeki sözcük sayısıyla eşleştirmek", "Formülü alan ve anahtarla geri okuyup aynı iddiayı verip vermediğine bakmak", "Her zaman ∀ ile başlamak", "Yüklemleri alfabetik sıralamak"],
                    "Formülü alan ve anahtarla geri okuyup aynı iddiayı verip vermediğine bakmak",
                    "Geri çeviri niceleyici, bağlaç, koşul yönü ve kapsam hatalarını görünür kılar.",
                    "İleri",
                ),
            ]
        ),
        {
            "prompt": "Sekiz doğal dil cümlesini önce açık yeniden yazıma, sonra FOL formülüne çevir; her biri için niceleyici, bağlaç, koşul yönü ve olumsuzluk kapsamını ayrı satırda gerekçelendir.",
            "starter": "Alanı sabitle; 'hangi nesneler?', 'ne ileri sürülüyor?', 'bir tanık mı herkes mi?' ve 'olumsuzluk tam olarak nereyi kapsıyor?' sorularını bu sırayla yanıtla.",
            "checks": [
                "Her F, G'dir için ∀ ve koşul kullanıldı",
                "Bazı F, G'dir için ∃ ve birleşim kullanıldı",
                "Yalnız F'ler G'dir, G'den F'ye açıkça yeniden yazıldı",
                "Hiçbiri, bazısı değil ve hepsi değil kapsamları ayrı tutuldu",
                "Her formülde serbest değişken kalmadı",
                "Her formül alan ve sembol anahtarıyla geri okundu",
                "Tümel cümleye varoluş iddiası eklenmedi",
            ],
            "solution": "Örnek anahtar: Her F G: ∀x(F(x)→G(x)); bazı F G: ∃x(F(x)∧G(x)); hiçbir F G değil: ∀x(F(x)→¬G(x)); bazı F G değil: ∃x(F(x)∧¬G(x)); yalnız F'ler G: ∀x(G(x)→F(x)); bütün F'lerin G olduğu doğru değil: ¬∀x(F(x)→G(x)).",
        },
        [
            _production_task(
                "Yeni bir alan ve üç bir yerli yüklem seçerek tek niceleyicili mini çeviri dosyası hazırla: her, bazı, hiçbiri, bazısı değil, hepsi olduğu doğru değil ve yalnız kalıplarını kullan; her formülü geri oku ve iki kasıtlı yanlışı onar.",
                [
                    "Söylem alanı ve üç yüklemin aritesi açıkça yazıldı.",
                    "Tümel alt grup cümlesi koşulla, varoluşsal ortak tanık birleşimle kuruldu.",
                    "Yalnız cümlesi açık yeniden yazımla doğru yöne çevrildi.",
                    "Üç farklı olumsuzluk kapsamı birbirine karıştırılmadı.",
                    "Her formül serbest değişken ve anahtar uyumu bakımından denetlendi.",
                    "Her formül doğal dile geri okunarak ilk cümleyle karşılaştırıldı.",
                    "Bir koşul/birleşim ve bir koşul yönü hatası ilk bozuk adımıyla açıklandı.",
                    "Tümel cümlelerin hangi varoluş iddiasını yapmadığı belirtildi.",
                ],
                "Değerlendirme yalnız son formüllere değil, yeniden yazımın koşul yönünü ve kapsamı nasıl koruduğuna bakar.",
                "Alan seçenekleri",
                [
                    "Bir kütüphanedeki kitaplar",
                    "Bir bahçedeki bitkiler",
                    "Bir konferanstaki katılımcılar",
                    "Bir koleksiyondaki filmler",
                    "Sınırlarını açık yazdığın başka bir alan",
                ],
                "Bu görevde iki yerli yüklem, kimlik, birden fazla niceleyici veya model/doğruluk hesabı kullanma.",
            ),
        ],
        [
            "Altı yaygın tek niceleyicili kalıbı yeni sembol anahtarıyla doğru kurma.",
            "Tümel kısıtlamada koşul ve varoluşsal ortak tanıkta birleşim seçimini gerekçelendirme.",
            "'Yalnız' cümlesini gerekli koşul diliyle açıp doğru yöne çevirme.",
            "Hiçbiri, bazısı değil ve hepsi olduğu doğru değil kapsamlarını ayrı formüllerle gösterme.",
            "Bir formülü alan ve anahtarla geri okuyup ilk yapı hatasını onarma.",
            "Tümel kısıtlamanın neden tek başına varoluşsal tanık ileri sürmediğini ifade etme.",
        ],
        [
            "Her F, G'dir cümlesinde neden ∧ değil → kullanılır?",
            "Bazı F, G'dir cümlesinde aynı tanık gereksinimi formülde nerede görünür?",
            "Yalnız F'ler G'dir cümlesinde hangi grup gerekli koşuldur?",
            "Hiçbir F, G değildir ile bütün F'lerin G olduğu doğru değildir arasındaki kapsam farkı nedir?",
            "∀x(F(x)→G(x)) neden tek başına ∃xF(x) iddiasını kurmaz?",
        ],
        "E29'da bir yerli yüklemlerden iki ve üç yerli bağıntılara geçecek; her argüman yerinin rolünü sabitleyip R(a,b) ile R(b,a) yönlerini ayıracağız.",
        [
            "forallx-one-quantifier",
            "forallx-fol-sentences",
            "mit-logic-sequence",
        ],
        "Ders standart klasik FOL gösterimini ve varoluşsal yük ayrımını kullanır; boş yüklem sınıfları için model doğruluğu hesabı yapmaz. Niceleyici olumsuzlamalarının eşdeğer dönüşümleri E31'e, resmi semantik gerekçeleri Faz F'ye ertelenir.",
        [
            "ders-26-niceleyicilere-giris",
            "ders-27-niceleyici-olumsuzlamalari",
            "ders-30-dogal-dilden-yuklem-mantigina-i",
        ],
    )
    lesson["fol_signature"] = E28_SIGNATURE
    lesson["syntax_scope"] = {
        "introduced": [
            "∀",
            "∃",
            "quantifier_scope",
            "universal_restriction",
            "existential_witness",
            "quantified_sentence",
        ],
        "review_only": ["unary_predicate", "open_formula", "¬", "∧", "→"],
        "locked_until_later": [
            "multi_place_predicate",
            "multiple_quantifier",
            "quantifier_negation_equivalence",
            "=",
            "substitution",
            "model_truth",
        ],
    }
    lesson["syntax_fixtures"] = [
        _syntax_fixture(
            "e28-universal-simple",
            "∀xF(x)",
            accepted=True,
            category="sentence",
            explanation="∀x, kapsamındaki F(x) oluşumunda x'i bağlar.",
        ),
        _syntax_fixture(
            "e28-existential-simple",
            "∃xG(x)",
            accepted=True,
            category="sentence",
            explanation="∃x en az bir G tanığı ileri süren kapalı cümledir.",
        ),
        _syntax_fixture(
            "e28-universal-restriction",
            "∀x(F(x) → G(x))",
            accepted=True,
            category="sentence",
            explanation="Tüm F nesnelerini G olmaya koşulla kısıtlar.",
        ),
        _syntax_fixture(
            "e28-existential-conjunction",
            "∃x(F(x) ∧ G(x))",
            accepted=True,
            category="sentence",
            explanation="Aynı x tanığı hem F hem G olarak bağlıdır.",
        ),
        _syntax_fixture(
            "e28-no-f-is-g",
            "∀x(F(x) → ¬G(x))",
            accepted=True,
            category="sentence",
            explanation="Her F için G kapsam içinde reddedilir.",
        ),
        _syntax_fixture(
            "e28-not-all",
            "¬∀x(F(x) → G(x))",
            accepted=True,
            category="sentence",
            explanation="Olumsuzluk bütün tümel cümleyi kapsar.",
        ),
        _syntax_fixture(
            "e28-free-variable",
            "(F(x) ∧ ∃yG(y))",
            accepted=True,
            category="open_formula",
            explanation="y bağlansa da soldaki x serbest kaldığı için formül açıktır.",
        ),
        _syntax_fixture(
            "e28-alpha-renamed",
            "∀y(F(y) → G(y))",
            accepted=True,
            category="sentence",
            explanation="Bağlı değişken y olarak tutarlı biçimde yeniden adlandırılmıştır.",
        ),
        _syntax_fixture(
            "e28-missing-variable",
            "∀(F(x) → G(x))",
            accepted=False,
            issue_code="quantifier.variable_expected",
            explanation="∀ işaretinden sonra tanımlı bir değişken bulunmalıdır.",
        ),
        _syntax_fixture(
            "e28-name-after-quantifier",
            "∀aF(a)",
            accepted=False,
            issue_code="quantifier.variable_expected",
            explanation="Niceleyici addan değil değişkenden sonra kullanılır.",
        ),
        _syntax_fixture(
            "e28-missing-body",
            "∃x",
            accepted=False,
            issue_code="formula.incomplete",
            explanation="Niceleyicinin kapsamında bir FOL formülü bulunmalıdır.",
        ),
        _syntax_fixture(
            "e28-unclosed-scope",
            "∀x(F(x) → G(x)",
            accepted=False,
            issue_code="parenthesis.unclosed",
            explanation="Niceleyicinin bileşik kapsamını açan parantez kapanmamıştır.",
        ),
    ]
    lesson["symbolization_fixtures"] = [
        _symbolization_fixture(
            "e28-every-f-g",
            "Her araştırmacı meraklıdır.",
            [
                (
                    "∀x(F(x) → G(x))",
                    "Alan seminere katılan bütün insanlardır.",
                    "Her alan üyesi için, araştırmacıysa meraklıdır.",
                ),
            ],
            [
                ("∀x(F(x) → G(x))", True, None, "Hedeflenen tümel kısıtlamadır."),
                ("∀y(F(y) → G(y))", True, None, "Bağlı değişkenin tutarlı yeniden adlandırılması aynı yapıdır."),
                ("∀x(F(x) ∧ G(x))", False, "translation.connective", "Birleşim alanın herkesi F yaparak kısıtlamayı bozar."),
                ("∀x(G(x) → F(x))", False, "translation.condition_direction", "Koşul yönü tersine dönmüştür."),
                ("∃x(F(x) ∧ G(x))", False, "translation.quantifier_kind", "Tümel iddia varoluşsal örneğe dönmüştürülmüştür."),
                ("(F(x) → G(x))", False, "translation.free_variable", "x'i bağlayan niceleyici eksiktir."),
            ],
            teaching_point="Tümel alt grup, koşulun önbileşeninde kısıtlanır.",
        ),
        _symbolization_fixture(
            "e28-some-f-g",
            "Bazı araştırmacılar meraklıdır.",
            [
                (
                    "∃x(F(x) ∧ G(x))",
                    "'Bazı' en az bir anlamında kullanılmıştır.",
                    "En az bir alan üyesi hem araştırmacı hem meraklıdır.",
                ),
            ],
            [
                ("∃x(F(x) ∧ G(x))", True, None, "Aynı tanıkta iki yüklem birleştirilir."),
                ("∃z(F(z) ∧ G(z))", True, None, "Bağlı z aynı yapıyı korur."),
                ("∃x(F(x) → G(x))", False, "translation.connective", "Koşul ortak F ve G tanığını kurmaz."),
                ("∀x(F(x) → G(x))", False, "translation.quantifier_kind", "En az bir iddiası her F iddiasına dönüştürülmüştür."),
            ],
            teaching_point="Varoluşsal örnekte aynı tanık F ve G'yi birlikte taşır.",
        ),
        _symbolization_fixture(
            "e28-only-f-g",
            "Yalnız araştırmacılar meraklıdır.",
            [
                (
                    "∀x(G(x) → F(x))",
                    "'Yalnız' araştırmacı olmayı meraklılığın gerekli koşulu yapar.",
                    "Meraklı olan herkes araştırmacıdır.",
                ),
            ],
            [
                ("∀x(G(x) → F(x))", True, None, "G olmak F olmayı gerektirir."),
                ("∀x(F(x) → G(x))", False, "translation.condition_direction", "Her F'nin G olduğunu söyleyen ters yöndür."),
                ("∀x(F(x) ↔ G(x))", False, "translation.connective", "Tek 'yalnız' ifadesi iki yönü birden vermez."),
            ],
            teaching_point="Yalnız F ifadesi F'yi gerekli koşul yapar; koşul G'den F'ye gider.",
        ),
        _symbolization_fixture(
            "e28-no-f-g",
            "Hiçbir araştırmacı meraklı değildir.",
            [
                (
                    "∀x(F(x) → ¬G(x))",
                    "'Hiçbir' her araştırmacı için meraklılığı reddeder.",
                    "Her araştırmacı meraklı olmayan biridir.",
                ),
            ],
            [
                ("∀x(F(x) → ¬G(x))", True, None, "Olumsuzluk ana yüklemdedir."),
                ("¬∀x(F(x) → G(x))", False, "translation.negation_scope", "Bu yalnızca bütün F'lerin G olduğunu reddeder."),
                ("∃x(F(x) ∧ ¬G(x))", False, "translation.quantifier_kind", "Bu yalnızca bazı F'lerin G olmadığını söyler."),
            ],
            teaching_point="Hiçbiri yapısında olumsuzluk her kısıtlanmış nesnenin ana yüklemine uygulanır.",
        ),
        _symbolization_fixture(
            "e28-some-f-not-g",
            "Bazı araştırmacılar meraklı değildir.",
            [
                (
                    "∃x(F(x) ∧ ¬G(x))",
                    "'Bazı' en az bir, olumsuzluk yalnız meraklılık yüklemindedir.",
                    "En az bir nesne araştırmacıdır ve meraklı değildir.",
                ),
            ],
            [
                ("∃x(F(x) ∧ ¬G(x))", True, None, "F ve G olmayan ortak tanık kurulur."),
                ("∃x(F(x) → ¬G(x))", False, "translation.connective", "Koşul ortak F tanığını garanti etmez."),
                ("∀x(F(x) → ¬G(x))", False, "translation.quantifier_kind", "Bazı yerine hiçbiri iddiası kurulmuştur."),
            ],
            teaching_point="Olumsuz varoluşsal örnekte tanık F ve ¬G'yi birlikte taşır.",
        ),
        _symbolization_fixture(
            "e28-not-every-f-g",
            "Bütün araştırmacıların meraklı olduğu doğru değildir.",
            [
                (
                    "¬∀x(F(x) → G(x))",
                    "Olumsuzluk açıkça bütün tümel iddiayı kapsar.",
                    "Her araştırmacının meraklı olduğu iddiası doğru değildir.",
                ),
            ],
            [
                ("¬∀x(F(x) → G(x))", True, None, "Tüm tümel cümle yadsınır."),
                ("∀x(F(x) → ¬G(x))", False, "translation.negation_scope", "Bu daha güçlü hiçbiri okumasıdır."),
                ("∃x(F(x) ∧ ¬G(x))", False, "translation.negation_scope", "Bu derste semantik eşdeğerlik henüz kabul anahtarı değildir; hedeflenen geniş kapsam korunmalıdır."),
            ],
            teaching_point="Sembolleştirme denetimi, E31'e kadar olumsuzluğun doğal dildeki geniş kapsamını aynen korur.",
        ),
    ]
    return lesson


STAGE_E_CANDIDATE_LESSONS = [
    _candidate_e27(),
    _candidate_e28(),
]

STAGE_E_CANDIDATE_MAP = {
    lesson["slug"]: lesson
    for lesson in STAGE_E_CANDIDATE_LESSONS
}
