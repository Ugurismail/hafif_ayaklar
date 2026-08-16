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


E29_SIGNATURE = {
    "domain": "atölyedeki insanlar",
    "names": {
        "a": "Ada",
        "b": "Bora",
        "c": "Cem",
        "d": "Deniz",
    },
    "variables": ["x", "y", "z"],
    "predicates": {
        "F": {
            "arity": 1,
            "reading": "x editör",
            "roles": ["editör olan nesne"],
        },
        "T": {
            "arity": 2,
            "reading": "x, y'yi tanıyor",
            "roles": ["tanıyan", "tanınan"],
        },
        "L": {
            "arity": 2,
            "reading": "x, y'nin solunda oturuyor",
            "roles": ["solda oturan", "sağında oturulan"],
        },
        "I": {
            "arity": 3,
            "reading": "x, y'yi z ile tanıştırdı",
            "roles": ["tanıştıran", "tanıştırılan", "kendisiyle tanıştırılan"],
        },
    },
}


E30_SIGNATURE = {
    "domain": "atölyedeki insanlar",
    "names": {
        "a": "Ada",
        "b": "Bora",
        "c": "Cem",
        "d": "Deniz",
    },
    "variables": ["x", "y", "z"],
    "predicates": {
        "F": {
            "arity": 1,
            "reading": "x mentor",
            "roles": ["mentor olan"],
        },
        "G": {
            "arity": 1,
            "reading": "x katılımcı",
            "roles": ["katılımcı olan"],
        },
        "T": {
            "arity": 2,
            "reading": "x, y'yi tanıyor",
            "roles": ["tanıyan", "tanınan"],
        },
        "D": {
            "arity": 2,
            "reading": "x, y'ye danışıyor",
            "roles": ["danışan", "danışılan"],
        },
        "I": {
            "arity": 3,
            "reading": "x, y'yi z ile tanıştırıyor",
            "roles": ["tanıştıran", "tanıştırılan", "kendisiyle tanıştırılan"],
        },
    },
}


E31_SIGNATURE = {
    "domain": "seminere katılan insanlar",
    "names": {
        "a": "Ada",
        "b": "Bora",
        "c": "Cem",
    },
    "variables": ["x", "y", "z"],
    "predicates": {
        "F": {
            "arity": 1,
            "reading": "x araştırmacı",
            "roles": ["araştırmacı olan"],
        },
        "G": {
            "arity": 1,
            "reading": "x meraklı",
            "roles": ["meraklı olan"],
        },
        "H": {
            "arity": 1,
            "reading": "x geç kaldı",
            "roles": ["geç kalan"],
        },
        "T": {
            "arity": 2,
            "reading": "x, y'yi tanıyor",
            "roles": ["tanıyan", "tanınan"],
        },
    },
}


E32_SIGNATURE = {
    "domain": "araştırma ekibindeki insanlar",
    "names": {
        "a": "Ada",
        "b": "Bora",
        "c": "Cem",
    },
    "variables": ["w", "x", "y", "z"],
    "predicates": {
        "F": {
            "arity": 1,
            "reading": "x araştırmacı",
            "roles": ["araştırmacı olan"],
        },
        "G": {
            "arity": 1,
            "reading": "x görevlendirildi",
            "roles": ["görevlendirilen"],
        },
        "T": {
            "arity": 2,
            "reading": "x, y'yi tanıyor",
            "roles": ["tanıyan", "tanınan"],
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


def _candidate_e29():
    lesson = _lesson(
        "E29",
        "ders-fol-baginti-arite-yon",
        "Çok Yerli Yüklemler ve Bağıntı Yönü",
        "Bir, iki ve üç yerli yüklemlerin aritesini sabitler; her argüman yerini doğal dildeki rolüyle eşleyerek etken, edilgen ve dönüşlü cümlelerde bağıntı yönünü korur.",
        "Arite, argüman rolleri ve yön disiplini",
        35,
        ["ders-fol-tek-niceleyicili-cumleler"],
        [
            "fol.arity_validate",
            "fol.argument_order",
            "fol.relation_key",
            "fol.active_passive_normalize",
        ],
        [
            "Bir, iki ve üç yerli yüklemleri istedikleri terim sayısına göre ayırmak.",
            "Bağıntı anahtarında her argüman yerinin rolünü ve sırasını açık yazmak.",
            "T(a,b), T(b,a) ve T(a,a) atomlarını anahtara göre doğru geri okumak.",
            "Etken ve edilgen yüzey yapılarını aynı rol sırasına normalleştirmek.",
            "Arite, argüman sırası ve yanlış terim hatalarını ayrı ayrı tanımak.",
            "Simetri veya nesne farklılığını atomik yazıma sessizce eklememek.",
        ],
        [
            ("Arite", "Bir yüklemin atomik formül kurmak için istediği sabit terim sayısı."),
            ("Bir yerli yüklem", "F(x) gibi tek nesne yeri bulunan özellik yüklemi."),
            ("İki yerli yüklem", "T(x,y) gibi iki sıralı rolü birbirine bağlayan bağıntı."),
            ("Üç yerli yüklem", "I(x,y,z) gibi üç rolü aynı atomda birleştiren bağıntı."),
            ("Argüman yeri", "Anahtarda belirli bir doğal dil rolüne ayrılmış sıralı terim konumu."),
            ("Bağıntı yönü", "Hangi nesnenin hangi rolü doldurduğunu belirleyen argüman sırası."),
            ("Dönüşlü atom", "T(a,a) gibi aynı terimin birden fazla rolü doldurduğu atom."),
            ("Simetrik bağıntı", "R(a,b) doğruysa R(b,a)'nın da doğru olmasını gerektiren ek bağıntı özelliği."),
        ],
        [
            _section(
                "Arite yüklemin sabit sözleşmesidir",
                "F(x), T(x,y) ve I(x,y,z) sırasıyla bir, iki ve üç terim ister. Arite, formül kurulurken ihtiyaca göre değiştirilmez.",
                "Yeni bir yüklem anahtarı kurarken veya eksik/fazla terimi denetlerken.",
                "F: 1 yer · T: 2 yer · I: 3 yer",
                "Doğal dilde mantıksal olarak izlenecek nesne rolleri anahtarda ilan edilir; her atom tam bu sayıda terimle tamamlanır.",
                "Aynı T sembolünü bir cümlede bir, başka cümlede iki yerli kullanma; tekrar eden aynı nesne rol sayısını azaltmaz.",
                [
                    ("F(a)", "F bir yerli olduğu için tek terimle tamamlanır."),
                    ("T(a,b)", "Tanıyan ve tanınan rolleri ayrı terimlerle doldurulur."),
                    ("I(a,b,c)", "Üç ayrı rol üç sıralı terimle doldurulur."),
                ],
                (
                    "Ariteyi ve rol sayısını atom yazmadan önce sabitlemek.",
                    "Terim sayısını her cümlede yeniden seçmek.",
                    "Aynı sembolün aritesi alıştırma boyunca değişmez.",
                ),
            ),
            _section(
                "Argüman yerleri rol taşır",
                "T(x,y): x, y'yi tanıyor anahtarında ilk yer tanıyanı, ikinci yer tanınanı gösterir. Yer sırası bağıntının yönüdür.",
                "Aynı iki nesne arasındaki ters yönlü iddiaları ayırırken.",
                "T(a,b): Ada Bora'yı tanıyor · T(b,a): Bora Ada'yı tanıyor",
                "Aynı adlar ve aynı yüklem bulunsa da yerler değişince roller değişir. Simetri ayrıca verilmedikçe atomlar birbirinin yerine geçmez.",
                "Cümlede adı önce geçen kişiyi otomatik ilk argüman yapma; önce rolünü belirle.",
                [
                    ("T(a,b)", "a tanıyan, b tanınandır."),
                    ("T(b,a)", "b tanıyan, a tanınandır."),
                    ("L(a,b)", "Ada, Bora'nın solunda oturur."),
                ],
                (
                    "Her terimi anahtardaki rol etiketiyle eşlemek.",
                    "Aynı iki ad bulunduğu için sırayı önemsiz saymak.",
                    "Sıralı yerler iddianın yönünü belirler.",
                ),
            ),
            _section(
                "Etken ve edilgen aynı rolleri korur",
                "'Ada Bora'yı tanıyor' ve 'Bora Ada tarafından tanınıyor' farklı öğeyle başlar; ikisinde de tanıyan Ada, tanınan Bora'dır.",
                "Edilgen çatı nesneyi doğal dilde öne çıkardığında.",
                "Ada Bora'yı tanıyor = Bora Ada tarafından tanınıyor = T(a,b)",
                "Sembolleştirme sözcük sırasını değil anahtardaki rolleri korur. Edilgen cümleyi önce rolü açık etken cümleye dönüştürmek yön hatasını azaltır.",
                "Dilbilgisel özne ilk geldi diye onu bağıntının ilk rolü sanma; 'tarafından' öbeğindeki faili izle.",
                [
                    ("Bora Ada tarafından tanınıyor.", "Ada tanıyan, Bora tanınandır: T(a,b)."),
                    ("Bora'nın sağında Ada oturuyor.", "Bora Ada'nın solundadır: L(b,a)."),
                    ("Cem, Bora ile Ada tarafından tanıştırıldı.", "Ada faili, Cem ikinci, Bora üçüncü roldür: I(a,c,b)."),
                ],
                (
                    "Cümleyi rol etiketli etken ara cümleye dönüştürmek.",
                    "Adları doğal dilde göründükleri sırayla kopyalamak.",
                    "Dilbilgisel yer değişebilir; mantıksal roller aynı kalır.",
                ),
            ),
            _section(
                "Aynı terim birden fazla rolü doldurabilir",
                "T(a,a), Ada'nın hem tanıyan hem tanınan rolünde olduğunu söyler. Bu arite hatası değil, dönüşlü atomik bir iddiadır.",
                "'Kendini', 'kendisinin' veya 'kendi kendine' yapıları bulunduğunda.",
                "T(a,a): Ada kendini tanıyor",
                "Argüman yerleri ayrı roller olsa da bu rolleri dolduran nesnelerin farklı olması gerekmez. Farklılık gerekiyorsa E32'de kimliksizlik ile yazılır.",
                "Aynı ad iki kez geçti diye bir terimi silme; rol sayısı ile farklı nesne sayısını karıştırma.",
                [
                    ("T(a,a)", "Ada iki rolü de doldurur."),
                    ("L(a,a)", "Sözdizimce düzenli, fakat sıra dışı bir iddiadır."),
                    ("I(a,b,b)", "Üç rol doludur; son iki rol aynı nesneye verilmiştir."),
                ],
                (
                    "Her rolü yazıp aynı nesneyse aynı adı tekrarlamak.",
                    "Ayrı yerlerin zorunlu olarak ayrı nesne istediğini varsaymak.",
                    "Arite rol sayısıdır, farklı nesne sayısı değildir.",
                ),
            ),
            _section(
                "Üç yerli yüklemde rol tablosu kullan",
                "I(x,y,z): x, y'yi z ile tanıştırdı yüklemi üç kişiyi tek atomda izler. Bir terimin yerini değiştirmek doğal dil rollerini değiştirir.",
                "Vermek, göndermek veya tanıştırmak gibi ikiden fazla rol gerektiren bağıntılarda.",
                "I: 1 tanıştıran · 2 tanıştırılan · 3 kendisiyle tanıştırılan",
                "Anahtar her konumun rolünü numaralı olarak sabitler; geri okuma bu tablodan yapılır.",
                "İkinci ve üçüncü rolü cümlede yan yana göründükleri için birbirinin yerine koyma.",
                [
                    ("I(a,b,c)", "Ada Bora'yı Cem ile tanıştırdı."),
                    ("I(a,c,b)", "Ada Cem'i Bora ile tanıştırdı."),
                    ("I(c,a,b)", "Cem Ada'yı Bora ile tanıştırdı."),
                ],
                (
                    "Her nesnenin rolünü numaralandırıp atomu o sırayla kurmak.",
                    "Üç adı yüzeyde göründükleri sırada yazmak.",
                    "Yüzey sıra değişebilir; anahtardaki rol sırası sabittir.",
                ),
            ),
            _section(
                "Simetriyi sembol biçiminden çıkarma",
                "T ve L ikisi de iki yerli yazılır; fakat R(a,b)'den R(b,a)'ya geçmek için bağıntının simetrik olduğuna dair ayrıca gerekçe gerekir.",
                "Bir atomdan ters yönlü atoma geçmenin haklı olup olmadığını değerlendirirken.",
                "R(a,b) tek başına R(b,a)'yı vermez",
                "Anahtar okuma ve rol sırası verir. Simetri ise E30 sonrasında ayrıca niceleyicili bir cümleyle ifade edilecek bağıntı özelliğidir.",
                "'Arkadaşıdır' gibi gündelikte karşılıklı düşünülen ilişkilerde bile simetriyi sırf iki yerlilikten çıkarma.",
                [
                    ("Ada Bora'yı tanıyor.", "Bora'nın Ada'yı tanıdığını tek başına söylemez."),
                    ("Ada Bora'nın solunda.", "Ters atom aynı iddiayı vermez."),
                    ("Ada Bora ile aynı yaşta.", "Simetrik olabilir; bunu arite değil bağıntının özelliği destekler."),
                ],
                (
                    "Ters atomu ayrı geri okuyup ek bilgi olmadan onaylamamak.",
                    "Aynı iki terim kullanıldığı için atomları özdeş saymak.",
                    "Argüman sırası korunur; simetri ayrı bir genellemedir.",
                ),
            ),
        ],
        [
            _worked("F(a)", "F bir yerli; Ada tek özelliği doldurur.", "Ada editördür"),
            _worked("T(a,b)", "İlk yer tanıyan, ikinci yer tanınandır.", "Ada Bora'yı tanıyor"),
            _worked("T(b,a)", "Aynı adlar ters rollerdedir.", "Bora Ada'yı tanıyor"),
            _worked("T(a,a)", "Ada iki rolü de doldurur.", "Ada kendini tanıyor"),
            _worked("L(a,b)", "a solda oturan, b sağında oturulandır.", "Ada Bora'nın solunda"),
            _worked("I(a,b,c)", "Üç rol anahtardaki sıradadır.", "Ada Bora'yı Cem ile tanıştırdı"),
            _worked("I(a,c,b)", "İkinci ve üçüncü roller değişmiştir.", "Ada Cem'i Bora ile tanıştırdı"),
            _worked("T(a)", "T iki terim ister; ikinci rol eksiktir.", "Eksik arite", "bad"),
            _worked("T(a,b,c)", "T iki yerli; üçüncü terim fazladır.", "Fazla arite", "bad"),
            _worked("I(b,a,c)", "Hedef cümleye göre ilk iki rol ters yazılmıştır.", "Argüman sırası hatası", "bad"),
        ],
        [
            "İki yerli yüklemi tek terimle tamamlamak.",
            "Doğal dilde ilk görünen adı otomatik ilk argümana koymak.",
            "Etken ve edilgen cümleleri ayrı rol yapıları sanmak.",
            "Simetrik olmayan bağıntıda terim sırasını sessizce ters çevirmek.",
            "Aynı terimin iki rolde kullanılmasını arite eksikliği sanmak.",
            "Ayrı yerlerin zorunlu olarak ayrı nesneler istediğini varsaymak.",
            "Üç yerli anahtarda ikinci ve üçüncü rolü açıkça etiketlememek.",
            "Bağıntının simetrisini aritesinden çıkarmak.",
        ],
        _practice(
            [
                ("T(x,y): x, y'yi tanıyor yükleminin aritesi kaçtır?", ["1", "2", "3", "Değişir"], "2", "Tanıyan ve tanınan iki sıralı roldür.", "Temel"),
                ("T(a,b) hangisidir?", ["Ada Bora'yı tanıyor", "Bora Ada'yı tanıyor", "Ada kendini tanıyor", "Ada ve Bora editördür"], "Ada Bora'yı tanıyor", "a tanıyan, b tanınandır.", "Temel"),
                ("T(a,a) için hangisi doğrudur?", ["Arite hatasıdır", "Ada kendini tanıyor", "İki farklı Ada vardır", "T bir yerli olur"], "Ada kendini tanıyor", "Aynı terim iki rolü doldurabilir.", "Temel"),
                ("I(x,y,z) kaç yerlidir?", ["1", "2", "3", "4"], "3", "Üç rol ayrı izlenir.", "Temel"),
                ("Bora Ada tarafından tanınıyor hangisidir?", ["T(a,b)", "T(b,a)", "T(a,a)", "T(b,b)"], "T(a,b)", "Tanıyan Ada, tanınan Bora'dır.", "Orta"),
                ("Bora'nın sağında Ada oturuyor hangisidir?", ["L(a,b)", "L(b,a)", "L(a,a)", "T(a,b)"], "L(b,a)", "Bora Ada'nın solundadır.", "Orta"),
                ("T(a) için ilk hata nedir?", ["Yanlış yön", "Eksik arite", "Serbest değişken", "Niceleyici"], "Eksik arite", "T iki terim ister.", "Orta"),
                ("Ada Bora'yı Cem ile tanıştırdı hangisidir?", ["I(a,b,c)", "I(a,c,b)", "I(b,a,c)", "I(c,b,a)"], "I(a,b,c)", "Roller anahtar sırasındadır.", "Orta"),
                ("Cem, Bora ile Ada tarafından tanıştırıldı hangisidir?", ["I(a,c,b)", "I(c,b,a)", "I(b,c,a)", "I(a,b,c)"], "I(a,c,b)", "Ada fail, Cem ikinci, Bora üçüncü roldür.", "Orta"),
                ("R(a,b)'den R(b,a)'ya geçmek için ne gerekir?", ["İki yerlilik yeter", "Ad olmaları yeter", "Simetriye dair ek bilgi", "Her zaman geçilir"], "Simetriye dair ek bilgi", "Simetri ariteden ayrı bir özelliktir.", "İleri"),
                ("I(a,b,b) için hangisi doğrudur?", ["Arite hatasıdır", "Üç rol dolduğu için sözdizimce düzenlidir", "I iki yerli olur", "b değişkendir"], "Üç rol dolduğu için sözdizimce düzenlidir", "Aynı nesne birden fazla rolü doldurabilir.", "İleri"),
                ("Edilgen cümlede en güvenli ara adım nedir?", ["Adları soldan sağa kopyalamak", "Rol etiketli etken cümleye dönüştürmek", "Yüklemi bir yerli yapmak", "Sırayı otomatik ters çevirmek"], "Rol etiketli etken cümleye dönüştürmek", "Yüzey sıra yerine rolleri korur.", "İleri"),
            ]
        ),
        {
            "prompt": "On atomik cümleyi rol tablosuyla sembolleştir ve geri oku; iki arite, iki yön ve bir edilgen çatı hatasını ayrı sınıflarla onar.",
            "starter": "Önce her yüklemin aritesini ve numaralı rollerini yaz; nesnelerin rollerini belirlemeden formül kurma.",
            "checks": [
                "Bir, iki ve üç yerli yüklemlerin ariteleri sabitlendi",
                "Her argüman yerinin rolü yazıldı",
                "Etken ve edilgen eş cümleler aynı atomla gösterildi",
                "T(a,b), T(b,a) ve T(a,a) ayrı geri okundu",
                "Arite ile argüman sırası hatası ayrıldı",
                "Üç yerli örneklerde rol sırası korundu",
                "Simetri veya nesne farklılığı sessizce eklenmedi",
            ],
            "solution": "Kontrol örnekleri: T(a,b) Ada Bora'yı tanıyor; T(b,a) Bora Ada'yı tanıyor; T(a,a) Ada kendini tanıyor; I(a,b,c) Ada Bora'yı Cem ile tanıştırdı.",
        },
        [
            _production_task(
                "Kendi bağlamında bir bir yerli, iki iki yerli ve bir üç yerli yüklem kur; etken, edilgen, ters yönlü ve dönüşlü on atomu sembolleştirip geri oku.",
                [
                    "Her yüklemin aritesi ve numaralı rolleri yazıldı.",
                    "Aynı sembol her örnekte aynı arite ve rolle kullanıldı.",
                    "İki etken/edilgen çift aynı atomla gösterildi.",
                    "İki ters yönlü atom ayrı geri okundu.",
                    "Bir dönüşlü atomda aynı terim iki rolü doldurdu.",
                    "Üç yerli yüklemde terim rolleri tabloyla doğrulandı.",
                    "Bir arite ve bir sıra hatası onarıldı.",
                    "Simetri ve farklılık varsayımı eklenmedi.",
                ],
                "Değerlendirme yüzey sözcük sırasına değil, anahtardaki rol sırasının korunmasına bakar.",
                "Bağlam",
                ["Editöryal ekip", "Öğrenci topluluğu", "Kargo ağı", "Aile arşivi", "Rolleri açık başka bir bağlam"],
                "Niceleyici, kimlik, model doğruluğu veya simetri aksiyomu ekleme.",
            ),
        ],
        [
            "Üç yerli bir yüklem için rol etiketli anahtar kurma.",
            "Etken, edilgen, ters ve dönüşlü sekiz atomu doğru geri çevirme.",
            "Arite ile yanlış argüman sırasını ayrı hata sayma.",
            "Edilgen cümleyi rolü açık etken cümleye normalleştirme.",
            "Simetrinin atomik yazımdan çıkmadığını açıklama.",
        ],
        [
            "T(a,b) ile T(b,a) farkını hangi veri belirler?",
            "Edilgen cümlede ilk ad neden otomatik ilk argüman değildir?",
            "T(a,a) neden ariteyi bire düşürmez?",
            "Üç yerli anahtarda rol numaraları neden gerekir?",
            "R(a,b)'den R(b,a)'ya geçmek neden iki yerlilikle haklı çıkmaz?",
        ],
        "E30'da sabit argüman yerlerini birden fazla niceleyiciyle bağlayacak; ∀x∃y ile ∃y∀x arasındaki tanık bağımlılığını yönü bozmadan okuyacağız.",
        ["forallx-multiple-generality", "forallx-fol-sentences", "mit-logic-sequence"],
        "Ders yalnız arite ve argüman sırasını kurar. Simetri, dönüşlülük ve geçişlilik gibi model özellikleri atomik yazımdan çıkarılmaz; resmi model semantiği Faz F'ye ertelenir.",
        ["ders-28-coklu-niceleyici-ve-kapsam", "ders-29-kimlik-yuklemler-ve-alan", "ders-31-dogal-dilden-yuklem-mantigina-ii"],
    )
    lesson["fol_signature"] = E29_SIGNATURE
    lesson["syntax_scope"] = {
        "introduced": [
            "predicate_arity",
            "binary_predicate",
            "ternary_predicate",
            "argument_role",
            "argument_order",
            "reflexive_atom",
        ],
        "review_only": ["name", "variable", "atomic_formula", "sentence", "open_formula"],
        "locked_until_later": [
            "multiple_quantifier",
            "relation_property_semantics",
            "=",
            "distinctness",
            "substitution",
        ],
    }
    lesson["syntax_fixtures"] = [
        _syntax_fixture("e29-unary", "F(a)", accepted=True, category="sentence", explanation="F bir yerli ve tek terimle tamamlanmıştır."),
        _syntax_fixture("e29-binary-forward", "T(a,b)", accepted=True, category="sentence", explanation="Tanıyan ve tanınan rolleri doludur."),
        _syntax_fixture("e29-binary-reverse", "T(b,a)", accepted=True, category="sentence", explanation="Aynı adlar ters rolde düzenli atom kurar."),
        _syntax_fixture("e29-reflexive", "T(a,a)", accepted=True, category="sentence", explanation="Aynı ad iki rolü doldurabilir."),
        _syntax_fixture("e29-ternary", "I(a,b,c)", accepted=True, category="sentence", explanation="I'nin üç rolü doludur."),
        _syntax_fixture("e29-binary-open", "T(x,b)", accepted=True, category="open_formula", explanation="İlk roldeki x serbesttir."),
        _syntax_fixture("e29-ternary-open", "I(a,y,c)", accepted=True, category="open_formula", explanation="İkinci roldeki y serbesttir."),
        _syntax_fixture("e29-binary-too-few", "T(a)", accepted=False, issue_code="predicate.arity_mismatch", explanation="T iki terim ister."),
        _syntax_fixture("e29-binary-too-many", "T(a,b,c)", accepted=False, issue_code="predicate.arity_mismatch", explanation="T yalnız iki terim ister."),
        _syntax_fixture("e29-ternary-too-few", "I(a,b)", accepted=False, issue_code="predicate.arity_mismatch", explanation="I üç terim ister."),
        _syntax_fixture("e29-ternary-too-many", "I(a,b,c,d)", accepted=False, issue_code="predicate.arity_mismatch", explanation="I yalnız üç terim ister."),
        _syntax_fixture("e29-unknown-relation", "R(a,b)", accepted=False, issue_code="predicate.unknown", explanation="R anahtarda tanımlı değildir."),
    ]
    lesson["symbolization_fixtures"] = [
        _symbolization_fixture(
            "e29-ada-knows-bora",
            "Ada Bora'yı tanıyor.",
            [("T(a,b)", "İlk rol tanıyan, ikinci rol tanınandır.", "Ada Bora'yı tanıyor.")],
            [
                ("T(a,b)", True, None, "a tanıyan, b tanınandır."),
                ("T(b,a)", False, "translation.argument_order", "Roller ters yazılmıştır."),
                ("L(a,b)", False, "translation.predicate", "Yanlış bağıntı kullanılmıştır."),
            ],
            teaching_point="Sıra tanıyan/tanınan rollerini izler.",
        ),
        _symbolization_fixture(
            "e29-passive-knowing",
            "Bora Ada tarafından tanınıyor.",
            [("T(a,b)", "Edilgen cümlede Ada fail, Bora tanınandır.", "Ada Bora'yı tanıyor.")],
            [
                ("T(a,b)", True, None, "Edilgen yüzey rolleri değiştirmez."),
                ("T(b,a)", False, "translation.argument_order", "Yüzeydeki ilk ad yanlış role konmuştur."),
            ],
            teaching_point="Edilgen cümleyi rolü açık etken cümleye dönüştür.",
        ),
        _symbolization_fixture(
            "e29-left-of",
            "Ada Bora'nın solunda oturuyor.",
            [("L(a,b)", "İlk rol solda oturandır.", "Ada Bora'nın solundadır.")],
            [
                ("L(a,b)", True, None, "a solda, b sağında oturulandır."),
                ("L(b,a)", False, "translation.argument_order", "Mekânsal yön terstir."),
            ],
            teaching_point="Ters atom ters mekânsal iddiadır.",
        ),
        _symbolization_fixture(
            "e29-right-surface",
            "Bora'nın sağında Ada oturuyor.",
            [("L(b,a)", "Bora Ada'nın solundadır.", "Bora Ada'nın solunda oturuyor.")],
            [
                ("L(b,a)", True, None, "Sağında yapısı solda olma anahtarına çevrilmiştir."),
                ("L(a,b)", False, "translation.argument_order", "Sağ/sol yönü ters okunmuştur."),
            ],
            teaching_point="Sağında cümlesini solda olma anahtarına göre yeniden yaz.",
        ),
        _symbolization_fixture(
            "e29-self-knowing",
            "Ada kendini tanıyor.",
            [("T(a,a)", "Aynı Ada iki rolü doldurur.", "Ada kendini tanıyor.")],
            [
                ("T(a,a)", True, None, "Aynı terim iki roldedir."),
                ("T(a,b)", False, "translation.term", "Kendini yerine Bora kullanılmıştır."),
            ],
            teaching_point="Rol sayısı iki, farklı nesne sayısı bir olabilir.",
        ),
        _symbolization_fixture(
            "e29-introduced",
            "Ada Bora'yı Cem ile tanıştırdı.",
            [("I(a,b,c)", "Sıra tanıştıran, tanıştırılan, kendisiyle tanıştırılandır.", "Ada Bora'yı Cem ile tanıştırdı.")],
            [
                ("I(a,b,c)", True, None, "Üç rol doğru sıradadır."),
                ("I(b,a,c)", False, "translation.argument_order", "İlk iki rol terstir."),
                ("I(a,c,b)", False, "translation.argument_order", "Son iki rol terstir."),
            ],
            teaching_point="Her terimi numaralı rol tablosuna yerleştir.",
        ),
        _symbolization_fixture(
            "e29-passive-introduced",
            "Cem, Bora ile Ada tarafından tanıştırıldı.",
            [("I(a,c,b)", "Ada tanıştıran, Cem ikinci, Bora üçüncü roldür.", "Ada Cem'i Bora ile tanıştırdı.")],
            [
                ("I(a,c,b)", True, None, "Edilgen cümle rollere normalleştirilmiştir."),
                ("I(c,b,a)", False, "translation.argument_order", "Adlar yüzey sırasıyla kopyalanmıştır."),
            ],
            teaching_point="Faili ve iki hedef rolünü ayrı belirle.",
        ),
    ]
    return lesson


def _candidate_e30():
    lesson = _lesson(
        "E30",
        "ders-fol-coklu-niceleyici-bagimlilik",
        "Çoklu Niceleyici, Sıra ve Bağımlılık",
        "Bir bağıntının yerlerini birden fazla niceleyiciyle bağlar; ∀∃ ile ∃∀ arasındaki farkı ayrı tanık ve ortak tanık okumaları üzerinden görünür kılar.",
        "Niceleyici sırası, tanık bağımlılığı ve değişken planı",
        45,
        ["ders-fol-baginti-arite-yon"],
        [
            "fol.quantifier_order",
            "fol.dependency_read",
            "fol.multiple_generalize",
            "fol.variable_plan",
        ],
        [
            "İki niceleyicinin hangi değişken oluşumlarını ve bağıntı yerlerini bağladığını göstermek.",
            "∀x∃y ile ∃y∀x yapılarını ayrı tanık ve ortak tanık okumalarıyla ayırmak.",
            "Aynı tür ve farklı tür niceleyicilerin yer değiştirmesini birbirine karıştırmamak.",
            "Doğal dil sözcük sırası yerine bağımlılık ve bağıntı rollerinden hareketle formül kurmak.",
            "Değişken gölgelemesini önleyen açık bir değişken planı kullanmak.",
            "Üç niceleyicili bir cümleyi rol tablosu ve ara yeniden ifadelerle sembolleştirmek.",
        ],
        [
            ("Çoklu niceleme", "Tek formül içinde iki veya daha fazla niceleyicinin farklı değişken oluşumlarını bağlaması."),
            ("Niceleyici sırası", "Bir niceleyicinin diğerinin kapsamında bulunmasını belirleyen dıştan içe düzen."),
            ("Bağımlı tanık", "Seçimi dıştaki tümel değişkenin değerine göre değişebilen varoluşsal örnek."),
            ("Ortak tanık", "Dıştaki varoluşsal niceleyici tarafından bir kez seçilip içteki bütün durumlar için kullanılan örnek."),
            ("Bağımlılık", "İçteki bir seçimin dıştaki değişkenin değerine göre değişebilmesi ilişkisi."),
            ("Niceleyici kaydırma", "Gerekçe olmadan niceleyicilerin sırasını veya kapsamını değiştirerek daha güçlü ya da farklı bir iddiaya geçme."),
            ("Değişken planı", "Her doğal dil rolüne ayrı değişken ayıran ve niceleyici sırasını formülden önce belirleyen taslak."),
            ("Gölgeleme", "İçteki bir niceleyicinin aynı değişken harfini yeniden bağlayıp dış bağlayıcının görünürlüğünü kapatması."),
        ],
        [
            _section(
                "Her niceleyici bir rolü bağlar",
                "T(x,y): x, y'yi tanıyor anahtarında x tanıyan, y tanınandır. ∀x∃yT(x,y) formülünde iki niceleyici aynı bağıntının farklı yerlerini bağlar.",
                "Bir doğal dil cümlesinde birden fazla kişi veya nesne rolü genellendiğinde.",
                "rol 1: x = tanıyan · rol 2: y = tanınan",
                "Önce bağıntının yerlerini doldur, sonra her değişkenin nicelik türünü ve hangi sırada seçildiğini belirle.",
                "Niceleyicileri yazıp değişkenlerin hangi role gittiğini sonradan tahmin etme.",
                [
                    ("∀x∃yT(x,y)", "Her x için en az bir y vardır ve x, y'yi tanır."),
                    ("∀x∃yT(y,x)", "Her x için en az bir y vardır ve y, x'i tanır."),
                    ("∃x∀yT(x,y)", "Bir x vardır ve x herkesi tanır."),
                ],
                (
                    "Bağıntı rol tablosunu, değişkenleri ve bağlayıcıları ayrı satırlarda planlamak.",
                    "Aynı x ve y harfleri geçtiği için formülleri aynı saymak.",
                    "Niceleyici türü, sıra ve bağıntı yeri birlikte okunur.",
                ),
            ),
            _section(
                "∀∃ ayrı tanıklara izin verir",
                "∀x∃yT(x,y), her kişi için tanıdığı en az bir kişi bulunduğunu söyler. y'nin seçimi x değiştikçe değişebilir; tek ortak kişi ileri sürülmez.",
                "'Herkes birini ...' ve 'her ... için bir ...' yapılarını okurken.",
                "her x → ona uygun en az bir y",
                "Dıştaki ∀ önce hangi durumun ele alındığını belirler; içteki ∃ o duruma göre bir tanık seçebilir.",
                "y'yi bütün x'ler için aynı kişiymiş gibi sabitleme.",
                [
                    ("∀x∃yT(x,y)", "Ada Bora'yı, Bora Cem'i, Cem Ada'yı tanıyor olabilir."),
                    ("∀x∃yD(x,y)", "Her katılımcının danıştığı kişi farklı olabilir."),
                    ("∀x∃y∃zI(x,y,z)", "Her tanıştıran için y ve z ayrı ayrı seçilebilir."),
                ],
                (
                    "Her dıştaki durum için içteki tanığın yeniden seçilebileceğini sormak.",
                    "Varoluşsal tanığı formülün tamamı için tek kişi yapmak.",
                    "İçteki varoluşsal seçim dıştaki tümel seçime bağımlı olabilir.",
                ),
            ),
            _section(
                "∃∀ ortak bir tanık ileri sürer",
                "∃y∀xT(x,y), önce tek bir y seçer; sonra bütün x'lerin o aynı y'yi tanıdığını söyler. Bu, ∀x∃yT(x,y)'den daha güçlü bir ortaklık iddiasıdır.",
                "'Birisi var ki herkes onu ...' veya 'herkesin aynı ...' ifadelerinde.",
                "tek y → bütün x'ler için korunur",
                "Dıştaki ∃ tanığı içteki ∀ başlamadan sabitler. x değişse de y aynı kalır.",
                "Cümlede 'birisi' sözcüğü geçti diye onu otomatik dışa alma; ortaklık anlamını bağlamdan doğrula.",
                [
                    ("∃y∀xT(x,y)", "Herkesin tanıdığı en az bir ortak kişi vardır."),
                    ("∃y∀xD(x,y)", "Herkesin danıştığı aynı kişi vardır."),
                    ("∃x∀yT(x,y)", "Bir kişi herkesi tanır; roller farklıdır."),
                ],
                (
                    "Tanığın bütün tümel örneklerde aynı kalıp kalmadığını sınamak.",
                    "∃∀ ile ∀∃ arasındaki farkı yalnız sembol sırası diye ezberlemek.",
                    "Dıştaki varoluşsal niceleyici ortak tanığı sabitler.",
                ),
            ),
            _section(
                "Aynı tür niceleyiciler ile karışık türleri ayır",
                "Klasik FOL'de ardışık iki tümel ya da iki varoluşsal niceleyici yer değiştirebilir; ∀∃ ile ∃∀ ise genel olarak aynı şeyi söylemez.",
                "Niceleyici sırasının anlamı değiştirip değiştirmediğini değerlendirirken.",
                "∀x∀y𝒜 ≡ ∀y∀x𝒜 · ∃x∃y𝒜 ≡ ∃y∃x𝒜 · ∀x∃y𝒜 ≢ ∃y∀x𝒜",
                "Aynı tür niceleyiciler aynı alan üzerinde aynı birleşik taramayı yapar. Karışık türlerde tanığın ne zaman seçildiği değişir.",
                "İlk iki eşdeğerlikten bütün niceleyicilerin serbestçe kaydırılabileceği sonucunu çıkarma.",
                [
                    ("∀x∀yT(x,y)", "Herkes herkesi tanıyor."),
                    ("∀y∀xT(x,y)", "Aynı tümel çift, aynı matrisi tarar."),
                    ("∃x∃yT(x,y)", "Bir tanıyan ve bir tanınan vardır; seçim sırası ortak varoluş iddiasını değiştirmez."),
                ],
                (
                    "Niceleyici türlerini ve içteki matrisin rollerini birlikte karşılaştırmak.",
                    "Her yer değişimini ya da hiçbir yer değişimini otomatik geçerli saymak.",
                    "Aynı türler yer değiştirebilir; karışık türler ayrıca sınanır.",
                ),
            ),
            _section(
                "Değişken planı gölgelemeyi önler",
                "Her bağımsız rol için ayrı değişken seçmek, ∀x∃xT(x,x) gibi içteki niceleyicinin dıştaki x'i gölgelemesini önler.",
                "İki veya daha fazla nicelik sözcüğünü tek formülde birleştirirken.",
                "tanıyan: x · tanınan: y · üçüncü rol: z",
                "Önce rol-değişken tablosu kurulur; her niceleyici yalnız kendi rolünün değişkenini bağlar. Harfler anlam taşımaz, fakat aynı kapsamda görevleri karıştırmamalıdır.",
                "Yeni bir nicelik gördükçe aynı x harfini yeniden kullanma.",
                [
                    ("∀x∃yT(x,y)", "İki rol iki ayrı değişkenle görünürdür."),
                    ("∀x∃xT(x,x)", "Sözdizimce cümledir; içteki ∃x dıştaki ∀x'i gölgeler ve hedef okumayı kaybeder."),
                    ("∀x∃y∃zI(x,y,z)", "Üç rol üç değişkenle izlenir."),
                ],
                (
                    "Her rol için ayrı harf ayırıp bağlayıcıyı dıştan içe yazmak.",
                    "Değişken harfini doğal dildeki kişinin kalıcı adı sanmak.",
                    "Değişkenler yer tutucudur; plan, bağlanma ilişkisini okunur tutar.",
                ),
            ),
            _section(
                "Üç niceleyicide katman katman ilerle",
                "Üç yerli I(x,y,z) bağıntısında her niceleyici yeni bir seçim katmanı açar. ∀x∃y∃zI(x,y,z), her x için uygun bir y ve z çifti bulunmasını ister.",
                "Vermek, tanıştırmak veya göndermek gibi üç rolün birden genellendiği cümlelerde.",
                "1. rol tablosu · 2. niceleme sırası · 3. matris · 4. geri okuma",
                "Cümle önce rolü açık ara ifadeye çevrilir; sonra dıştan içe seçim sırası yazılır ve en son atom eklenir.",
                "Üç niceleyiciyi doğal dilde göründükleri sırayla yığıp bağıntı yerlerini kontrol etmeden bırakma.",
                [
                    ("∀x∃y∃zI(x,y,z)", "Her kişi birini başka biriyle tanıştırır; y ve z, x'e göre değişebilir."),
                    ("∃z∀x∃yI(x,y,z)", "Tek bir z vardır; herkes bir y'yi o z ile tanıştırır."),
                    ("∃y∃z∀xI(x,y,z)", "Aynı y ve z çifti bütün x'ler için sabittir."),
                ],
                (
                    "Her niceleyiciden sonra hangi seçimlerin sabit, hangilerinin değişebilir olduğunu not etmek.",
                    "Üç niceliği tek adımda çevirip bağımlılıkları görünmez kılmak.",
                    "Dıştan içe her katman sonraki seçimlerin bağımlılık alanını belirler.",
                ),
            ),
            _section(
                "Niceleyici kaydırmayı karşı senaryoyla sın",
                "∀x∃yT(x,y)'den ∃y∀xT(x,y)'ye geçmek geçerli değildir. Herkes farklı birini tanıyor olabilir; ortak tanınan kişi bulunmayabilir.",
                "Bir çıkarımda niceleyicilerin yalnızca sırası değiştirilmiş görünüyorsa.",
                "ayrı tanıklar ortak tanığı garanti etmez",
                "Küçük bir senaryoda her x için bir y verilir; sonra bütün x'lere uyan tek y bulunup bulunmadığı sorulur. Bulunamıyorsa kaydırma bozuk görünür.",
                "Karşı senaryoyu resmi model semantiğinin tamamı sanma; burada yalnız anlam farkını görünür kılan hazırlık aracıdır.",
                [
                    ("Ada Bora'yı, Bora Cem'i, Cem Ada'yı tanıyor.", "Herkes birini tanır; herkesin tanıdığı ortak biri olmak zorunda değildir."),
                    ("Herkes Deniz'i tanıyor.", "Hem ∃y∀xT(x,y) hem ∀x∃yT(x,y) sağlanabilir."),
                    ("Kimse kimseyi tanımıyor.", "İki yapı da başarısız olur; bu durum aralarındaki farkı göstermez."),
                ],
                (
                    "Öncülü sağlayıp sonucu bozan küçük bir karşı senaryo aramak.",
                    "Daha güçlü ortak tanık iddiasını sırf semboller aynı diye çıkarmak.",
                    "Ayrı tanıkların varlığı tek ortak tanığın varlığını gerektirmez.",
                ),
            ),
        ],
        [
            _worked("∀x∃yT(x,y)", "Her x için y yeniden seçilebilir.", "Herkes birini tanıyor"),
            _worked("∃y∀xT(x,y)", "Önce tek y seçilir ve bütün x'ler onu tanır.", "Herkesin tanıdığı biri var"),
            _worked("∀x∃yT(y,x)", "Her x için onu tanıyan bir y bulunur.", "Herkes birisi tarafından tanınıyor"),
            _worked("∃x∀yT(x,y)", "Tek x bütün y'leri tanır.", "Herkesi tanıyan biri var"),
            _worked("∀x∀yT(x,y)", "İki tümel değişken bütün sıralı çiftleri tarar.", "Herkes herkesi tanıyor"),
            _worked("∃x∃yT(x,y)", "En az bir tanıyan-tanınan çifti vardır.", "Birisi birini tanıyor"),
            _worked("∀x(F(x) → ∃y(G(y) ∧ T(x,y)))", "Her mentor için katılımcı tanık ayrı seçilebilir.", "Her mentor bir katılımcıyı tanıyor"),
            _worked("∃y(G(y) ∧ ∀x(F(x) → T(x,y)))", "Aynı katılımcı bütün mentorlar tarafından tanınır.", "Bütün mentorların tanıdığı bir katılımcı var"),
            _worked("∀x∃y∃zI(x,y,z)", "y ve z, dıştaki x'e göre değişebilir.", "Herkes birini başka biriyle tanıştırıyor"),
            _worked("∃z∀x∃yI(x,y,z)", "z bütün x'ler için ortak, y ise x'e göre değişebilir.", "Biri var; herkes birini onunla tanıştırıyor"),
            _worked("∃y∀xT(x,y)", "Hedef ∀x∃y ise ortak tanık iddiası gereksizce güçlendirilmiştir.", "Niceleyici sırası hatası", "bad"),
            _worked("∀x∃xT(x,x)", "İçteki ∃x dıştaki ∀x'i gölgeler; iki rolün bağımlılığı kaybolur.", "Değişken gölgelemesi", "bad"),
        ],
        [
            "∀∃ içindeki varoluşsal tanığı bütün tümel örneklerde aynı kişi sanmak.",
            "∃∀ ortak tanık iddiasını ∀∃ ile eşdeğer saymak.",
            "Doğal dilde ilk görünen nicelik sözcüğünü düşünmeden en dış niceleyici yapmak.",
            "Bağıntı yönünü korumadan yalnız niceleyici sırasına odaklanmak.",
            "Aynı tür niceleyicilerin yer değiştirebilmesinden karışık türlerin de değişebileceğini çıkarmak.",
            "İki farklı rol için aynı değişkeni iç içe yeniden bağlayarak gölgeleme üretmek.",
            "Üç niceleyicili cümleyi rol ve bağımlılık tablosu olmadan tek adımda yazmak.",
            "Ayrı tanıklardan tek ortak tanığa gerekçesiz niceleyici kaydırmak.",
            "Küçük doğal dil senaryosunu resmi FOL model semantiğinin tamamı sanmak.",
        ],
        _practice(
            [
                ("∀x∃yT(x,y) en iyi nasıl okunur?", ["Herkes birini tanıyor", "Birini herkes tanıyor", "Herkes herkesi tanıyor", "Kimse kimseyi tanımıyor"], "Herkes birini tanıyor", "y her x için yeniden seçilebilir.", "Temel"),
                ("∃y∀xT(x,y) neyi ekler?", ["Ortak bir tanınan kişi", "Her x için farklı y", "Kimsenin tanınmaması", "Yalnız iki kişi"], "Ortak bir tanınan kişi", "Dıştaki ∃ tek y'yi sabitler.", "Temel"),
                ("Herkes birisi tarafından tanınıyor hangisidir?", ["∀x∃yT(y,x)", "∀x∃yT(x,y)", "∃y∀xT(x,y)", "∀x∀yT(x,y)"], "∀x∃yT(y,x)", "x tanınan, y tanıyandır.", "Temel"),
                ("Herkesi tanıyan biri var hangisidir?", ["∃x∀yT(x,y)", "∀x∃yT(x,y)", "∃y∀xT(x,y)", "∀x∀yT(y,x)"], "∃x∀yT(x,y)", "Tek x bütün y'leri tanır.", "Temel"),
                ("∀x∃y yapısında y için hangisi doğrudur?", ["x'e göre değişebilir", "Her zaman aynı kalır", "Serbesttir", "Bir addır"], "x'e göre değişebilir", "İçteki tanık dıştaki seçime bağımlı olabilir.", "Orta"),
                ("Hangi çift genel olarak eşdeğer değildir?", ["∀x∃y𝒜 ve ∃y∀x𝒜", "∀x∀y𝒜 ve ∀y∀x𝒜", "∃x∃y𝒜 ve ∃y∃x𝒜", "∀x∀y𝒜 ve ∀x∀y𝒜"], "∀x∃y𝒜 ve ∃y∀x𝒜", "Karışık niceleyici sırası tanık bağımlılığını değiştirir.", "Orta"),
                ("∀x∃xT(x,x) için öğretimsel sorun nedir?", ["Gölgeleme", "Arite eksikliği", "Bilinmeyen yüklem", "Eksik parantez"], "Gölgeleme", "İçteki ∃x dıştaki ∀x bağını kapatır.", "Orta"),
                ("∀x∃y∃zI(x,y,z) içinde hangileri x'e göre değişebilir?", ["y ve z", "Yalnız x", "Hiçbiri", "Yalnız z sabittir"], "y ve z", "İki varoluşsal seçim dıştaki x'in kapsamındadır.", "Orta"),
                ("∃z∀x∃yI(x,y,z) içinde hangi değişken ortaktır?", ["z", "x", "y", "Hiçbiri"], "z", "z bütün x seçimlerinden önce sabitlenir.", "Orta"),
                ("∀x∃yT(x,y)'den ∃y∀xT(x,y) neden çıkmaz?", ["Ayrı tanıklar ortak tanığı garanti etmez", "T iki yerli değildir", "x ve y addır", "İki formül sözdizimce hatalıdır"], "Ayrı tanıklar ortak tanığı garanti etmez", "Her x farklı bir y tanıyor olabilir.", "İleri"),
                ("Çoklu niceleyicide ilk güvenli adım nedir?", ["Rol-değişken tablosu kurmak", "Bütün niceleyicileri ∀ yapmak", "Sözcükleri soldan sağa kopyalamak", "Parantezleri kaldırmak"], "Rol-değişken tablosu kurmak", "Bağıntı yerleri ve seçim sırası önce görünür kılınır.", "İleri"),
                ("Herkesin danıştığı aynı kişi var hangisidir?", ["∃y∀xD(x,y)", "∀x∃yD(x,y)", "∃x∀yD(y,x)", "∀x∀yD(x,y)"], "∃y∀xD(x,y)", "Danışılan y dışta seçilip bütün x'ler için sabit kalır.", "İleri"),
            ]
        ),
        {
            "prompt": "Altı doğal dil cümlesini önce rol-değişken tablosuna, sonra FOL'e çevir; her ∀∃/∃∀ çiftini küçük bir senaryoyla geri oku ve bir niceleyici kaydırma hatasını onar.",
            "starter": "Her cümlede bağıntı yerlerini yaz, ortak kalması gereken rolü işaretle ve niceleyicileri ancak bundan sonra dıştan içe sırala.",
            "checks": [
                "Her değişken ayrı bir bağıntı rolüne bağlandı",
                "∀∃ ayrı tanık, ∃∀ ortak tanık olarak geri okundu",
                "Bağıntı yönü niceleyici sırası değişirken korundu",
                "Aynı tür ve karışık tür niceleyici değişimleri ayrıldı",
                "Değişken gölgelemesi üretilmedi",
                "Üç niceleyicili örnek katman katman kuruldu",
                "Niceleyici kaydırmasına karşı senaryo verildi",
            ],
            "solution": "Kontrol çifti: ∀x∃yT(x,y) herkes birini tanıyor; ∃y∀xT(x,y) herkesin tanıdığı ortak biri var. Ada Bora'yı, Bora Cem'i, Cem Ada'yı tanıyorsa ilk cümle sağlanabilirken ikinci sağlanmayabilir.",
        },
        [
            _production_task(
                "Kendi bağlamında iki ayrı-tanık, iki ortak-tanık ve bir üç-niceleyicili cümle kur; her formülü rol tablosu, bağımlılık notu, geri okuma ve karşı senaryoyla gerekçelendir.",
                [
                    "Alan ile aritesi ve rolleri açık bağıntı anahtarı yazıldı.",
                    "Her rol için ayrı değişken kullanıldı.",
                    "İki ∀∃ formunda iç tanığın neye bağlı olduğu açıklandı.",
                    "İki ∃∀ formunda ortak tanığın neden sabit kaldığı açıklandı.",
                    "En az bir bağıntı ters yönü ayrıca geri okundu.",
                    "Üç niceleyicili form katmanlara ayrıldı.",
                    "Bir geçersiz niceleyici kaydırmasına karşı senaryo kuruldu.",
                    "Formüllerde kimlik, model doğruluğu veya kanıt kuralı kullanılmadı.",
                ],
                "Değerlendirme yalnız sembol dizisine değil, seçim sırasının ve bağıntı rollerinin doğal dilde doğru gerekçelendirilmesine bakar.",
                "Bağlam",
                ["Mentorluk ağı", "Sağlık ekibi", "Kütüphane danışmanlığı", "Araştırma ortaklığı", "Rolleri açık başka bir ağ"],
                "En az bir örnekte herkesin farklı bir tanığı olabildiği, bir örnekte ise tek ortak tanığın gerektiği açık olsun.",
            ),
        ],
        [
            "∀∃ ile ∃∀ yapılarını ayrı ve ortak tanık okumalarıyla ayırma.",
            "Her değişkeni doğru bağıntı yerine ve bağlayıcıya eşleme.",
            "Bağıntı yönünü niceleyici sırasından bağımsız olarak koruma.",
            "Üç niceleyicili cümleyi ara basamaklarla sembolleştirme.",
            "Değişken gölgelemesini teşhis edip ayrı harflerle onarma.",
            "Niceleyici kaydırmasına somut karşı senaryo üretme.",
        ],
        [
            "∀x∃y içinde y neden bütün x'ler için aynı olmak zorunda değildir?",
            "∃y∀x yapısında hangi seçim önce sabitlenir?",
            "Aynı tür niceleyiciler ile karışık türlerin yer değiştirmesi neden ayrılmalıdır?",
            "Bağıntı yönü doğru, niceleyici sırası yanlış bir örnek nasıl görünür?",
            "Üç niceleyicili bir cümlede bağımlılık tablosu neyi görünür kılar?",
        ],
        "E31'de bu çoklu yapılara olumsuzlama ekleyecek; 'hepsi değil', 'hiçbiri' ve geniş/dar kapsam okumalarını niceleyici türünü doğru değiştirerek ayıracağız.",
        ["forallx-multiple-generality", "forallx-fol-sentences", "mit-logic-sequence"],
        "Ders çoklu niceleyicinin dilsel seçim sırasını öğretir. Küçük senaryolar anlam farkını görünür kılar; resmi yorum, atama ve model doğruluğu Faz F'ye, niceleyici olumsuzlamaları E31'e ertelenir.",
        ["ders-28-coklu-niceleyici-ve-kapsam", "ders-31-dogal-dilden-yuklem-mantigina-ii"],
    )
    lesson["fol_signature"] = E30_SIGNATURE
    lesson["syntax_scope"] = {
        "introduced": [
            "multiple_quantifier",
            "quantifier_order",
            "witness_dependency",
            "variable_plan",
            "quantifier_shadowing_warning",
        ],
        "review_only": [
            "universal_quantifier",
            "existential_quantifier",
            "predicate_arity",
            "argument_order",
            "sentence",
            "open_formula",
        ],
        "locked_until_later": [
            "quantifier_negation",
            "formal_model_truth",
            "variable_assignment",
            "=",
            "distinctness",
            "substitution",
        ],
    }
    lesson["syntax_fixtures"] = [
        _syntax_fixture("e30-forall-exists", "∀x∃yT(x,y)", accepted=True, category="sentence", explanation="Her iki değişken de ayrı niceleyicilerce bağlanır."),
        _syntax_fixture("e30-exists-forall", "∃y∀xT(x,y)", accepted=True, category="sentence", explanation="Ortak y dışta, bütün x'ler içte bağlanır."),
        _syntax_fixture("e30-all-pairs", "∀x∀yT(x,y)", accepted=True, category="sentence", explanation="İki tümel niceleyici bütün sıralı çiftleri kapsar."),
        _syntax_fixture("e30-some-pair", "∃x∃yT(x,y)", accepted=True, category="sentence", explanation="Bir tanıyan-tanınan çifti ileri sürülür."),
        _syntax_fixture("e30-reverse-role", "∀x∃yT(y,x)", accepted=True, category="sentence", explanation="Bağıntı yönü ters olsa da düzenli bir FOL cümlesidir."),
        _syntax_fixture("e30-three-quantifiers", "∀x∃y∃zI(x,y,z)", accepted=True, category="sentence", explanation="Üç rol üç niceleyiciyle bağlanmıştır."),
        _syntax_fixture("e30-shared-third", "∃z∀x∃yI(x,y,z)", accepted=True, category="sentence", explanation="z ortak, y ise x'e göre seçilebilir."),
        _syntax_fixture("e30-shadowing", "∀x∃xT(x,x)", accepted=True, category="sentence", explanation="Sözdizimce cümledir; gölgeleme ayrıca öğretimsel uyarıdır."),
        _syntax_fixture("e30-free-third", "∀x∃yT(y,z)", accepted=True, category="open_formula", explanation="z hiçbir niceleyici tarafından bağlanmamıştır."),
        _syntax_fixture("e30-too-few", "∀x∃yT(x)", accepted=False, issue_code="predicate.arity_mismatch", explanation="T iki terim ister."),
        _syntax_fixture("e30-unknown-predicate", "∀x∃yR(x,y)", accepted=False, issue_code="predicate.unknown", explanation="R sembol anahtarında yoktur."),
        _syntax_fixture("e30-unknown-variable", "∀q∃yT(q,y)", accepted=False, issue_code="quantifier.variable_expected", explanation="q aday değişken kümesinde değildir."),
    ]
    lesson["symbolization_fixtures"] = [
        _symbolization_fixture(
            "e30-everyone-knows-someone",
            "Herkes birini tanıyor.",
            [("∀x∃yT(x,y)", "Tanınılan kişi, tanıyan kişiye göre değişebilir.", "Herkes en az bir kişiyi tanıyor.")],
            [
                ("∀x∃yT(x,y)", True, None, "Ayrı tanıklara izin veren sıra doğrudur."),
                ("∃y∀xT(x,y)", False, "translation.quantifier_order", "Tek ortak tanınan kişi gereksizce ileri sürülmüştür."),
                ("∀x∃yT(y,x)", False, "translation.argument_order", "Tanıyan ve tanınan rolleri ters yazılmıştır."),
            ],
            teaching_point="Önce her kişi, sonra ona göre seçilebilen bir tanınan kişi gelir.",
        ),
        _symbolization_fixture(
            "e30-someone-everyone-knows",
            "Herkesin tanıdığı biri var.",
            [("∃y∀xT(x,y)", "Aynı y bütün x'ler için tanınandır.", "Bir kişi vardır ve herkes onu tanır.")],
            [
                ("∃y∀xT(x,y)", True, None, "Ortak tanık dışta seçilmiştir."),
                ("∀x∃yT(x,y)", False, "translation.quantifier_order", "Her kişi için ayrı tanık ortak kişiyi garanti etmez."),
                ("∃y∀xT(y,x)", False, "translation.argument_order", "Ortak kişinin rolü tanıyana çevrilmiştir."),
            ],
            teaching_point="Ortak kişi bütün tümel örneklerden önce sabitlenir.",
        ),
        _symbolization_fixture(
            "e30-everyone-known",
            "Herkes birisi tarafından tanınıyor.",
            [("∀x∃yT(y,x)", "Tanıyan y, tanınan x'e göre değişebilir.", "Her kişi için onu tanıyan en az bir kişi vardır.")],
            [
                ("∀x∃yT(y,x)", True, None, "Roller ve ayrı tanık sırası korunmuştur."),
                ("∀x∃yT(x,y)", False, "translation.argument_order", "Tanıyan ve tanınan yerleri ters çevrilmiştir."),
                ("∃y∀xT(y,x)", False, "translation.quantifier_order", "Herkesi tanıyan tek kişi gereksizce eklenmiştir."),
            ],
            teaching_point="Niceleyici sırası kadar bağıntı yönü de denetlenir.",
        ),
        _symbolization_fixture(
            "e30-someone-knows-everyone",
            "Herkesi tanıyan biri var.",
            [("∃x∀yT(x,y)", "Aynı x bütün y'leri tanır.", "Bir kişi vardır ve o kişi herkesi tanır.")],
            [
                ("∃x∀yT(x,y)", True, None, "Tanıyan ortak kişi dışta seçilmiştir."),
                ("∀y∃xT(x,y)", False, "translation.quantifier_order", "Her tanınan için farklı tanıyan yeterli sayılmıştır."),
                ("∃x∀yT(y,x)", False, "translation.argument_order", "Ortak kişi tanınan rolüne konmuştur."),
            ],
            teaching_point="Ortak tanığın hangi bağıntı yerinde olduğu ayrıca korunur.",
        ),
        _symbolization_fixture(
            "e30-every-mentor-knows-participant",
            "Her mentor bir katılımcıyı tanıyor.",
            [("∀x(F(x) → ∃y(G(y) ∧ T(x,y)))", "Katılımcı her mentora göre ayrı seçilebilir.", "Her mentorun tanıdığı en az bir katılımcı vardır.")],
            [
                ("∀x(F(x) → ∃y(G(y) ∧ T(x,y)))", True, None, "Tümel kısıtlama ve içteki varoluşsal tanık doğrudur."),
                ("∀x(F(x) ∧ ∃y(G(y) ∧ T(x,y)))", False, "translation.connective", "Alan içindeki herkesi mentor yapan birleşim kullanılmıştır."),
                ("∀x(F(x) → ∃y(G(y) ∧ T(y,x)))", False, "translation.argument_order", "Mentor tanınan role geçirilmiştir."),
            ],
            teaching_point="Kısıtlı tümel dışta koşul, ona bağlı tanık sonuç tarafında kurulur.",
        ),
        _symbolization_fixture(
            "e30-shared-participant",
            "Bütün mentorların tanıdığı bir katılımcı var.",
            [("∃y(G(y) ∧ ∀x(F(x) → T(x,y)))", "Aynı katılımcı bütün mentorlar için sabittir.", "Bir katılımcı vardır ve bütün mentorlar onu tanır.")],
            [
                ("∃y(G(y) ∧ ∀x(F(x) → T(x,y)))", True, None, "Katılımcı dışta ortak tanık olarak seçilmiştir."),
                ("∃y(G(y) ∧ ∀x(F(x) ∧ T(x,y)))", False, "translation.connective", "Tümel mentor kısıtlaması birleşime çevrilmiştir."),
                ("∃y(G(y) ∧ ∀x(F(x) → T(y,x)))", False, "translation.argument_order", "Ortak katılımcı tanıyan role geçirilmiştir."),
            ],
            teaching_point="Ortak tanık varoluşsal koşulla birlikte dışta tutulur.",
        ),
        _symbolization_fixture(
            "e30-everyone-introduces-pair",
            "Herkes birini başka biriyle tanıştırıyor.",
            [("∀x∃y∃zI(x,y,z)", "y ve z, tanıştıran x'e göre değişebilir.", "Her kişi için tanıştırdığı bir kişi ve onunla tanıştırdığı başka bir rol vardır.")],
            [
                ("∀x∃y∃zI(x,y,z)", True, None, "Üç rolün seçim sırası korunmuştur."),
                ("∃y∃z∀xI(x,y,z)", False, "translation.quantifier_order", "Aynı y-z çifti herkes için ortaklaştırılmıştır."),
                ("∀x∃y∃zI(y,x,z)", False, "translation.argument_order", "Tanıştıran ve tanıştırılan rolleri ters yazılmıştır."),
            ],
            teaching_point="Üç rol önce değişken tablosunda, sonra dıştan içe niceleyicilerde izlenir.",
        ),
        _symbolization_fixture(
            "e30-everyone-knows-everyone",
            "Herkes herkesi tanıyor.",
            [
                ("∀x∀yT(x,y)", "İki tümel niceleyici aynı alanın bütün sıralı çiftlerini tarar.", "Her kişi her kişiyi tanır."),
                ("∀y∀xT(x,y)", "Aynı tür niceleyiciler yer değiştirmiştir; bağıntı rolleri korunur.", "Her kişi her kişiyi tanır."),
            ],
            [
                ("∀x∀yT(x,y)", True, None, "Bütün sıralı çiftler kapsanır."),
                ("∀y∀xT(x,y)", True, None, "Aynı tür niceleyicilerin sırası bu okumayı değiştirmez."),
                ("∀x∃yT(x,y)", False, "translation.quantifier_kind", "İkinci tümel niceleyici varoluşsala çevrilmiştir."),
            ],
            teaching_point="Aynı tür niceleyicilerin değişimi ile karışık türlerin değişimini ayır.",
        ),
    ]
    return lesson


def _candidate_e31():
    lesson = _lesson(
        "E31",
        "ders-fol-kapsam-niceleyici-olumsuzlama",
        "Kapsam ve Niceleyici Olumsuzlaması",
        "Olumsuzluğun niceleyiciye, kısıtlayıcı yükleme veya ana yükleme uygulanmasını ayırır; 'hepsi değil' ile 'hiçbiri'ni geniş ve dar kapsam üzerinden çözümler.",
        "Olumsuzluk kapsamı ve niceleyici dönüşümü",
        40,
        [
            "ders-fol-coklu-niceleyici-bagimlilik",
            "ders-mantiksal-esdegerlik-ve-tutarlilik",
        ],
        [
            "fol.scope_mark",
            "fol.quantifier_negate",
            "fol.not_all_distinguish",
            "fol.wide_narrow_read",
        ],
        [
            "¬∀x𝒜, ∀x¬𝒜, ¬∃x𝒜 ve ∃x¬𝒜 yapılarını ayrı geri okumak.",
            "Niceleyici olumsuzlamasında olumsuzluğu içeri taşırken niceleyici türünü değiştirmek.",
            "'Hepsi değil' ile 'hiçbiri' ve 'bazısı değil' okumalarını ayırmak.",
            "Kısıtlı niceleme içinde olumsuzluğun koşulun hangi tarafına uygulandığını göstermek.",
            "Çoklu niceleyicide geniş ve dar kapsam olumsuzluklarını bağımlılık farkıyla karşılaştırmak.",
            "Belirsiz Türkçe cümleleri bağlam koşullarıyla birden fazla açık formüle ayırmak.",
        ],
        [
            ("Geniş kapsam", "Bir işlecin daha büyük formül parçasını, özellikle bütün niceleyicili cümleyi kapsaması."),
            ("Dar kapsam", "Bir işlecin yalnız içteki yüklem veya daha küçük formül parçasına uygulanması."),
            ("Niceleyici olumsuzlaması", "¬∀x𝒜 ile ∃x¬𝒜; ¬∃x𝒜 ile ∀x¬𝒜 arasındaki standart eşdeğer yeniden yazım."),
            ("Hepsi değil", "Tümel iddianın yanlış olduğunu, dolayısıyla en az bir karşı örnek bulunduğunu söyleyen okuma."),
            ("Hiçbiri", "Alan içindeki hiçbir nesnenin hedef özelliği taşımadığını söyleyen daha güçlü okuma."),
            ("Kapsam belirsizliği", "Yüzey cümlesinin olumsuzluk ile niceliğin sırasını tek başına belirlemediği durum."),
            ("Kısıtlayıcı yüklem", "Alan içinden ilgilenilen alt sınıfı koşulun solunda belirleyen yüklem."),
            ("Karşı örnek tanığı", "Tümel iddianın yanlışlığını gösteren ve ∃x¬𝒜 biçiminde görünür olan nesne."),
        ],
        [
            _section(
                "Olumsuzluğun kapsamını parantezle görünür kıl",
                "¬∀xG(x), bütün tümel iddiayı yadsır. ∀x¬G(x) ise her nesne için G'nin yanlış olduğunu söyler. Semboller aynı olsa da kapsam farklıdır.",
                "Olumsuzluk ile niceleyici aynı cümlede bulunduğunda.",
                "¬[∀x G(x)] ≠ ∀x[¬G(x)]",
                "Önce yadsınan tam cümle paranteze alınır; sonra olumsuzluk işareti bu parçanın önüne yerleştirilir.",
                "Türkçedeki 'değil' sözcüğünü en yakın yüklemin önüne otomatik taşıma.",
                [
                    ("¬∀xG(x)", "Herkesin meraklı olduğu doğru değildir."),
                    ("∀x¬G(x)", "Hiç kimse meraklı değildir."),
                    ("∃x¬G(x)", "En az bir kişi meraklı değildir."),
                ],
                (
                    "Olumsuzluğun yadsıdığı en büyük formül parçasını işaretlemek.",
                    "Aynı semboller bulunduğu için kapsamları özdeş saymak.",
                    "İşleç sırası, yadsınan iddianın gücünü belirler.",
                ),
            ),
            _section(
                "Tümeli yadsımak karşı örnek ister",
                "¬∀x𝒜, 'her x için 𝒜' iddiasının başarısız olduğunu söyler ve standart olarak ∃x¬𝒜 biçiminde yeniden yazılır.",
                "'Hepsi değil', 'herkesin ... olduğu doğru değil' veya tümel iddiaya itiraz ifadelerinde.",
                "¬∀x𝒜 ≡ ∃x¬𝒜",
                "Olumsuzluk niceleyicinin içinden geçerken ∀, ∃'ye dönüşür ve matris yadsınır.",
                "Olumsuzluğu içeri taşıyıp ∀ işaretini aynı bırakma.",
                [
                    ("¬∀xG(x)", "Herkes meraklı değildir okumasının geniş kapsam biçimi."),
                    ("∃x¬G(x)", "Meraklı olmayan en az bir kişi vardır."),
                    ("¬∀x(F(x) → G(x))", "Bütün araştırmacıların meraklı olduğu doğru değildir."),
                ],
                (
                    "Tümel iddiayı bozan en az bir tanığı aramak.",
                    "Tümel yadsımayı herkes için olumsuz özellik diye güçlendirmek.",
                    "Tümelin yanlışlığı tek bir karşı örnekle gösterilebilir.",
                ),
            ),
            _section(
                "Varoluşu yadsımak hiçbir örnek bırakmaz",
                "¬∃x𝒜, 𝒜 olan hiçbir x bulunmadığını söyler ve standart olarak ∀x¬𝒜 biçiminde yeniden yazılır.",
                "'Hiç kimse', 'hiçbir ...' veya '... olan biri yok' ifadelerinde.",
                "¬∃x𝒜 ≡ ∀x¬𝒜",
                "Olumsuzluk ∃ üzerinden içeri taşınırken niceleyici ∀ olur; her olası tanığın 𝒜'yı sağlamadığı belirtilir.",
                "¬∃x𝒜'yı ∃x¬𝒜 ile karıştırma; ikincisi yalnız bir olumsuz örnek ister.",
                [
                    ("¬∃xG(x)", "Meraklı hiç kimse yoktur."),
                    ("∀x¬G(x)", "Herkes için meraklı olmak yanlıştır."),
                    ("¬∃x(F(x) ∧ G(x))", "Hem araştırmacı hem meraklı olan hiç kimse yoktur."),
                ],
                (
                    "Bir olumlu tanığın bulunmasının tüm cümleyi bozup bozmadığını sormak.",
                    "Hiçbiri iddiasını bazısı değil düzeyine zayıflatmak.",
                    "Varoluşun yadsınması bütün olası örnekleri dışlar.",
                ),
            ),
            _section(
                "Kısıtlı tümelde hepsi değil ile hiçbiri ayrılır",
                "'Her F, G'dir' cümlesinin yadsınması ¬∀x(F(x)→G(x)) olur. 'Hiçbir F, G değildir' ise ∀x(F(x)→¬G(x)) biçimindedir.",
                "Alt sınıf hakkında olumsuz nicelik cümleleri kurulurken.",
                "hepsi değil: ∃x(F(x)∧¬G(x)) · hiçbiri: ¬∃x(F(x)∧G(x))",
                "İlk form bir F karşı örneği ister; ikinci form F ve G'nin ortak örneğini bütünüyle dışlar.",
                "'Her F, G değildir' yüzeyini bağlam sormadan iki okumadan birine zorlamamak.",
                [
                    ("¬∀x(F(x) → G(x))", "Bütün araştırmacılar meraklı değildir: en az bir karşı örnek vardır."),
                    ("∀x(F(x) → ¬G(x))", "Hiçbir araştırmacı meraklı değildir."),
                    ("∃x(F(x) ∧ ¬G(x))", "Araştırmacı olup meraklı olmayan biri vardır."),
                ],
                (
                    "Önce cümlenin bir karşı örnek mi yoksa sıfır ortak örnek mi istediğini belirlemek.",
                    "Hepsi değil ile hiçbiri arasında güç farkını yok saymak.",
                    "Karşı örnek varlığı, bütün ortak örneklerin yokluğu değildir.",
                ),
            ),
            _section(
                "Olumsuzluğun koşuldaki yerini koru",
                "∀x(F(x)→¬G(x)) ana yüklemi yadsır. ∀x(¬F(x)→G(x)) ise araştırmacı olmayanları kısıtlayıcı sınıf yapar ve bambaşka bir iddia kurar.",
                "Kısıtlayıcı ve ana yüklemin ikisi de olumsuzlanabilir göründüğünde.",
                "kısıt: F(x) · hedef: G(x)",
                "Doğal dilde 'hangi nesneler hakkında?' sorusu koşulun solunu, 'onlar hakkında ne söyleniyor?' sorusu sağını belirler.",
                "Olumsuzluk işaretini koşulun bir tarafından diğerine eşdeğerlik varmış gibi taşıma.",
                [
                    ("∀x(F(x) → ¬G(x))", "Her araştırmacı meraklı değildir; hiçbiri okuması."),
                    ("∀x(¬F(x) → G(x))", "Araştırmacı olmayan herkes meraklıdır."),
                    ("¬∀x(F(x) → G(x))", "Tüm araştırmacı-meraklı genellemesi yadsınır."),
                ],
                (
                    "Kısıtlayıcı sınıfı ve o sınıfa yüklenen özelliği ayrı yazmak.",
                    "Olumsuzluğu koşulun içinde serbestçe dolaştırmak.",
                    "Koşulun iki tarafı farklı doğal dil rolleridir.",
                ),
            ),
            _section(
                "Çoklu niceleyicide geniş ve dar kapsam",
                "¬∀x∃yT(x,y), herkesin birini tanıdığı iddiasını yadsır. ∀x¬∃yT(x,y) ise hiç kimsenin kimseyi tanımadığını söyler ve çok daha güçlüdür.",
                "Olumsuzluk bir ∀∃ veya ∃∀ zinciriyle birlikte bulunduğunda.",
                "¬[∀x∃yT(x,y)] ≡ ∃x∀y¬T(x,y)",
                "Olumsuzluğu her niceleyicinin üzerinden geçirirken türünü sırayla değiştir; bağıntı yönünü ve değişken rollerini koru.",
                "Olumsuzluğu yalnız en içteki atoma taşıyıp niceleyicileri değiştirmeden bırakma.",
                [
                    ("¬∀x∃yT(x,y)", "En az bir kişi hiç kimseyi tanımıyor."),
                    ("∀x¬∃yT(x,y)", "Hiç kimse kimseyi tanımıyor."),
                    ("∃y¬∀xT(x,y)", "Herkes tarafından tanınmayan en az bir kişi var."),
                ],
                (
                    "Olumsuzluğu bir katman taşırken niceleyici türünü de değiştirmek.",
                    "Dış ve iç niceleyiciyi aynı anda atlayıp bağımlılığı kaybetmek.",
                    "Her kapsam katmanı ayrı dönüştürülür.",
                ),
            ),
            _section(
                "Belirsizliği tek cevaba zorlamadan kaydet",
                "'Herkes gelmedi' gündelik Türkçede bağlama göre 'bazıları gelmedi' veya 'hiç kimse gelmedi' diye kullanılabilir. Biçimselleştirme önce bağlam koşulunu açıklar.",
                "Yüzey cümlesi nicelik ile olumsuzluğun kapsamını tek başına sabitlemediğinde.",
                "okuma 1: ¬∀xG(x) · okuma 2: ∀x¬G(x)",
                "Her savunulabilir okuma ayrı formül, geri çeviri ve onu destekleyen bağlamla yazılır. Belirsizlik formülde gizlenmez.",
                "Bağlam vermeden bir formülü tek resmi doğru cevap ilan etme.",
                [
                    ("Toplantıda üç kişiden biri eksik.", "¬∀xG(x) okumasını destekler."),
                    ("Salon tamamen boş.", "∀x¬G(x) okumasını destekler."),
                    ("Bağlam verilmedi.", "İki okuma da aday olarak tutulur."),
                ],
                (
                    "Yüzey cümlesi, olası okumalar ve bağlam kanıtını üç ayrı sütunda yazmak.",
                    "Mantıksal gösterimin doğal dil belirsizliğini kendiliğinden çözmesini beklemek.",
                    "Formül seçimi bağlamsal bir çözümleme kararıdır.",
                ),
            ),
        ],
        [
            _worked("¬∀xG(x)", "Olumsuzluk bütün tümel iddiayı kapsar.", "Herkesin meraklı olduğu doğru değil"),
            _worked("∃x¬G(x)", "Tümel iddianın karşı örnek tanığı görünürdür.", "Meraklı olmayan biri var"),
            _worked("¬∃xG(x)", "Meraklı bir tanığın varlığı bütünüyle yadsınır.", "Meraklı hiç kimse yok"),
            _worked("∀x¬G(x)", "Her nesne için G yanlış denir.", "Hiç kimse meraklı değil"),
            _worked("¬∀x(F(x) → G(x))", "En az bir F, G değildir.", "Bütün araştırmacıların meraklı olduğu doğru değil"),
            _worked("∃x(F(x) ∧ ¬G(x))", "Araştırmacı ve meraklı olmayan ortak tanık kurulur.", "Meraklı olmayan bir araştırmacı var"),
            _worked("∀x(F(x) → ¬G(x))", "F olanların tamamında G yadsınır.", "Hiçbir araştırmacı meraklı değil"),
            _worked("¬∃x(F(x) ∧ G(x))", "F ve G ortak tanığı dışlanır.", "Araştırmacı ve meraklı olan hiç kimse yok"),
            _worked("¬∀x∃yT(x,y)", "Dıştaki tümel iddia geniş kapsamda yadsınır.", "Herkesin birini tanıdığı doğru değil"),
            _worked("∀x¬∃yT(x,y)", "Her kişi için herhangi bir tanıma ilişkisi yadsınır.", "Hiç kimse kimseyi tanımıyor"),
            _worked("∀x¬G(x)", "Hedef 'hepsi değil' ise bu form hiçbiri diye gereksizce güçlendirilmiştir.", "Olumsuzluk kapsamı hatası", "bad"),
            _worked("¬∀x(F(x) → ¬G(x))", "Olumsuzluk hem dışta hem hedefte bırakılmış; hedef iddia tersine dönmüştür.", "Çifte kapsam hatası", "bad"),
        ],
        [
            "¬∀x𝒜'yı ∀x¬𝒜 ile özdeş saymak.",
            "¬∃x𝒜'yı ∃x¬𝒜 ile karıştırmak.",
            "Olumsuzluğu içeri taşırken niceleyici türünü değiştirmemek.",
            "Hepsi değil okumasını hiçbiri düzeyine güçlendirmek.",
            "Kısıtlayıcı yüklem ile ana yüklemdeki olumsuzluğu yer değiştirmek.",
            "Koşulun sağındaki olumsuzluğu bütün koşulun olumsuzluğu sanmak.",
            "Çoklu niceleyicide yalnız en içteki atomu yadsıyıp dış niceleyicileri olduğu gibi bırakmak.",
            "Bağıntı yönünü niceleyici olumsuzlaması sırasında ters çevirmek.",
            "Belirsiz Türkçe cümleye bağlam vermeden tek formül dayatmak.",
        ],
        _practice(
            [
                ("¬∀xG(x) en iyi nasıl okunur?", ["Herkes G değildir / hepsi değil", "Hiç kimse G değildir", "Bazı herkes G'dir", "G olan biri yoktur"], "Herkes G değildir / hepsi değil", "Tümel iddia geniş kapsamda yadsınır.", "Temel"),
                ("∀x¬G(x) ne söyler?", ["Hiç kimse G değildir", "Bazı kişi G değildir", "Herkes G'dir", "G olan biri vardır"], "Hiç kimse G değildir", "Her nesne için G yadsınır.", "Temel"),
                ("¬∃xG(x) hangisine eşdeğerdir?", ["∀x¬G(x)", "∃x¬G(x)", "¬∀xG(x)", "∀xG(x)"], "∀x¬G(x)", "Varoluş yadsınırken ∃, ∀ olur.", "Temel"),
                ("¬∀xG(x) hangisine eşdeğerdir?", ["∃x¬G(x)", "∀x¬G(x)", "¬∃xG(x)", "∃xG(x)"], "∃x¬G(x)", "Tümel yadsımaya bir karşı örnek yeter.", "Temel"),
                ("'Bütün F'ler G değildir' yalnız hepsi değil anlamındaysa hangisidir?", ["¬∀x(F(x) → G(x))", "∀x(F(x) → ¬G(x))", "¬∃x(F(x) ∧ G(x))", "∀x(F(x) ∧ ¬G(x))"], "¬∀x(F(x) → G(x))", "En az bir F karşı örneği istenir.", "Orta"),
                ("'Hiçbir F, G değildir' hangisidir?", ["∀x(F(x) → ¬G(x))", "¬∀x(F(x) → G(x))", "∃x(F(x) ∧ ¬G(x))", "∀x(¬F(x) → G(x))"], "∀x(F(x) → ¬G(x))", "Her F için G yadsınır.", "Orta"),
                ("∀x(¬F(x) → G(x)) hangi sınıfı kısıtlar?", ["F olmayanları", "F olanları", "G olmayanları", "Herkesi F yapar"], "F olmayanları", "Koşulun solu kısıtlayıcı sınıftır.", "Orta"),
                ("¬∀x∃yT(x,y) neyi garanti eder?", ["En az bir kişi hiç kimseyi tanımıyor", "Hiç kimse kimseyi tanımıyor", "Herkes aynı kişiyi tanıyor", "Birisi herkesi tanıyor"], "En az bir kişi hiç kimseyi tanımıyor", "¬∀, ∃¬ olur; içteki ∃ de yadsınır.", "Orta"),
                ("∀x¬∃yT(x,y) hangisidir?", ["Hiç kimse kimseyi tanımıyor", "Bazı kişi kimseyi tanımıyor", "Herkes birini tanıyor", "Birini herkes tanıyor"], "Hiç kimse kimseyi tanımıyor", "Her x için herhangi bir y ile T bağı yadsınır.", "Orta"),
                ("Olumsuzluk bir niceleyicinin içinden geçirilirken ne olur?", ["Niceleyici türü değişir", "Bağıntı yönü değişir", "Değişken ad olur", "Arite azalır"], "Niceleyici türü değişir", "∀ ile ∃ birbirine dönüşür ve iç formül yadsınır.", "İleri"),
                ("'Herkes gelmedi' bağlamsızsa en güvenli yaklaşım nedir?", ["İki olası okumayı bağlam koşullarıyla yazmak", "Her zaman hiçbiri saymak", "Her zaman hepsi değil saymak", "Niceleyiciyi kaldırmak"], "İki olası okumayı bağlam koşullarıyla yazmak", "Yüzey cümlesi kapsamı tek başına sabitlemeyebilir.", "İleri"),
                ("Hepsi değil ile hiçbiri arasındaki temel fark nedir?", ["Bir karşı örnek ile bütün örneklerin dışlanması", "Yüklem aritesi", "Değişken harfi", "Alan büyüklüğü"], "Bir karşı örnek ile bütün örneklerin dışlanması", "Hepsi değil en az bir karşı örnek; hiçbiri sıfır olumlu örnek ister.", "İleri"),
            ]
        ),
        {
            "prompt": "Sekiz olumsuz nicelik cümlesinde yadsınan parçayı işaretle, geniş/dar kapsam formüllerini yaz, eşdeğer yeniden ifadeyi ver ve iki belirsiz cümleyi bağlam koşullarıyla dallandır.",
            "starter": "Önce olumsuzluk olmadan ileri sürülen cümleyi yaz; sonra yadsınan tam parçayı köşeli paranteze al.",
            "checks": [
                "Her olumsuzluğun kapsamı açıkça işaretlendi",
                "¬∀ ile ∃¬; ¬∃ ile ∀¬ dönüşümleri doğru yapıldı",
                "Hepsi değil ve hiçbiri ayrı geri okundu",
                "Kısıtlayıcı ve ana yüklem olumsuzlukları karıştırılmadı",
                "Çoklu niceleyicide her katman sırayla dönüştürüldü",
                "Bağıntı yönü dönüşüm boyunca korundu",
                "Belirsiz okumalar bağlam koşullarıyla ayrı formüllere ayrıldı",
            ],
            "solution": "Temel kontrol: ¬∀xG(x) ≡ ∃x¬G(x), fakat ∀x¬G(x) ≡ ¬∃xG(x). İlki hepsi değil, ikincisi hiçbiri okumasıdır.",
        },
        [
            _production_task(
                "Kendi bağlamından hepsi değil, hiçbiri, bazısı değil ve iki çoklu niceleyici olumsuzluğu üret; her biri için kapsam ağacı, eşdeğer yeniden yazım ve geri çeviri ver.",
                [
                    "Alan ve sembol anahtarı açık yazıldı.",
                    "Her formülde yadsınan tam parça işaretlendi.",
                    "En az bir ¬∀/∃¬ ve bir ¬∃/∀¬ çifti doğru kuruldu.",
                    "Hepsi değil ile hiçbiri aynı örnekte karşılaştırıldı.",
                    "Kısıtlayıcı yüklem ile ana yüklemdeki olumsuzluk ayrıldı.",
                    "Bir ∀∃ zincirinde olumsuzluk katman katman taşındı.",
                    "İki belirsiz yüzey cümlesi bağlam koşullarıyla dallandırıldı.",
                    "Resmi semantik ispatı veya model doğruluğu iddiası eklenmedi.",
                ],
                "Değerlendirme formül benzerliğine değil, kapsamın doğal dilde doğru geri okunmasına ve bağlam kararının açık olmasına bakar.",
                "Bağlam",
                ["Seminer katılımı", "Araştırma ekibi", "Sosyal ağ", "Kütüphane üyeliği", "Olumsuz nicelik içeren başka bir bağlam"],
                "En az bir cümle bağlam verilmeden iki savunulabilir okumaya sahip olsun.",
            ),
        ],
        [
            "Dört temel olumsuz niceleme yapısını ayrı geri okuma.",
            "Niceleyici olumsuzlamasını tür değiştirerek doğru uygulama.",
            "Hepsi değil ve hiçbiri için güç farkını karşı örnekle açıklama.",
            "Kısıtlayıcı ve ana yüklem olumsuzluklarını ayırma.",
            "Çoklu niceleyicide geniş ve dar kapsam biçimlerini kurma.",
            "Belirsiz Türkçe cümleye bağlam koşullu iki savunulabilir form verme.",
        ],
        [
            "¬∀x𝒜 ile ∀x¬𝒜 arasında hangi güç farkı vardır?",
            "¬∃x𝒜 neden ∃x¬𝒜 değildir?",
            "Kısıtlı tümelde olumsuzluğun koşulun sağında olması neyi söyler?",
            "¬∀x∃yT(x,y) ile ∀x¬∃yT(x,y) nasıl ayrılır?",
            "Belirsiz bir yüzey cümlesinde formül seçimini ne gerekçelendirir?",
        ],
        "E32'de olumsuzluğun yanına kimlik ekleyecek; 'başka', 'yalnız', en az, en çok ve tam olarak sayı ifadelerini farklılık koşullarıyla kuracağız.",
        ["forallx-one-quantifier", "forallx-multiple-generality", "forallx-fol-ambiguity", "mit-logic-sequence"],
        "Ders standart klasik niceleyici olumsuzlamalarını çeviri ve geri okuma aracı olarak kullanır. Eşdeğerliklerin resmi model kuramsal gerekçesi Faz F'ye; kimlik ve sayı kalıpları E32'ye ertelenir.",
        ["ders-27-niceleyici-olumsuzlamalari", "ders-28-coklu-niceleyici-ve-kapsam", "ders-31-dogal-dilden-yuklem-mantigina-ii"],
    )
    lesson["fol_signature"] = E31_SIGNATURE
    lesson["syntax_scope"] = {
        "introduced": [
            "quantifier_negation",
            "wide_scope_negation",
            "narrow_scope_negation",
            "not_all_pattern",
            "none_pattern",
        ],
        "review_only": [
            "universal_quantifier",
            "existential_quantifier",
            "multiple_quantifier",
            "conditional_restriction",
            "argument_order",
        ],
        "locked_until_later": [
            "formal_equivalence_proof",
            "formal_model_truth",
            "=",
            "distinctness",
            "substitution",
        ],
    }
    lesson["syntax_fixtures"] = [
        _syntax_fixture("e31-not-all", "¬∀xG(x)", accepted=True, category="sentence", explanation="Olumsuzluk bütün tümel cümleyi kapsar."),
        _syntax_fixture("e31-some-not", "∃x¬G(x)", accepted=True, category="sentence", explanation="Meraklı olmayan bir tanık vardır."),
        _syntax_fixture("e31-none-wide", "¬∃xG(x)", accepted=True, category="sentence", explanation="G olan bir tanığın varlığı yadsınır."),
        _syntax_fixture("e31-none-narrow", "∀x¬G(x)", accepted=True, category="sentence", explanation="Her nesne için G yadsınır."),
        _syntax_fixture("e31-restricted-not-all", "¬∀x(F(x) → G(x))", accepted=True, category="sentence", explanation="Bütün F'lerin G olduğu iddiası yadsınır."),
        _syntax_fixture("e31-restricted-none", "∀x(F(x) → ¬G(x))", accepted=True, category="sentence", explanation="Her F için G yadsınır."),
        _syntax_fixture("e31-no-overlap", "¬∃x(F(x) ∧ G(x))", accepted=True, category="sentence", explanation="F ve G ortak tanığı dışlanır."),
        _syntax_fixture("e31-multiple-wide", "¬∀x∃yT(x,y)", accepted=True, category="sentence", explanation="Bütün ∀∃ iddiası yadsınır."),
        _syntax_fixture("e31-multiple-narrow", "∀x¬∃yT(x,y)", accepted=True, category="sentence", explanation="Her x için tanıdığı bir y bulunması yadsınır."),
        _syntax_fixture("e31-open-negation", "¬G(x)", accepted=True, category="open_formula", explanation="x serbest kaldığı için ifade cümle değildir."),
        _syntax_fixture("e31-missing-body", "¬∀x", accepted=False, issue_code="formula.incomplete", explanation="Niceleyicinin gövdesi eksiktir."),
        _syntax_fixture("e31-bad-arity", "¬∃xT(x)", accepted=False, issue_code="predicate.arity_mismatch", explanation="T iki terim ister."),
    ]
    lesson["symbolization_fixtures"] = [
        _symbolization_fixture(
            "e31-not-everyone-curious",
            "Herkesin meraklı olduğu doğru değildir.",
            [
                ("¬∀xG(x)", "Olumsuzluk tümel iddiayı geniş kapsamda yadsır.", "Herkes meraklı değildir; hepsi değil."),
                ("∃x¬G(x)", "Standart niceleyici olumsuzlamasıyla karşı örnek görünürdür.", "Meraklı olmayan biri vardır."),
            ],
            [
                ("¬∀xG(x)", True, None, "Geniş kapsam korunmuştur."),
                ("∃x¬G(x)", True, None, "Eşdeğer karşı örnek formudur."),
                ("∀x¬G(x)", False, "translation.negation_scope", "Hepsi değil, hiçbiri diye güçlendirilmiştir."),
            ],
            teaching_point="Tümel iddianın yadsınması tek karşı örnek ister.",
        ),
        _symbolization_fixture(
            "e31-nobody-curious",
            "Hiç kimse meraklı değildir.",
            [
                ("¬∃xG(x)", "Meraklı bir tanığın varlığı yadsınır.", "Meraklı hiç kimse yoktur."),
                ("∀x¬G(x)", "Her kişi için meraklılık yadsınır.", "Hiç kimse meraklı değildir."),
            ],
            [
                ("¬∃xG(x)", True, None, "Varoluşun geniş kapsam yadsımasıdır."),
                ("∀x¬G(x)", True, None, "Eşdeğer dar kapsam formudur."),
                ("∃x¬G(x)", False, "translation.negation_scope", "Yalnız bir olumsuz örnek hiçbiri için yetmez."),
            ],
            teaching_point="Hiçbiri, olumlu tanıkların tamamını dışlar.",
        ),
        _symbolization_fixture(
            "e31-not-all-researchers",
            "Bütün araştırmacıların meraklı olduğu doğru değildir.",
            [
                ("¬∀x(F(x) → G(x))", "Tüm araştırmacı-meraklı genellemesi yadsınır.", "Bütün araştırmacılar meraklı değildir; hepsi değil."),
                ("∃x(F(x) ∧ ¬G(x))", "Karşı örnek araştırmacı açıkça kurulur.", "Meraklı olmayan bir araştırmacı vardır."),
            ],
            [
                ("¬∀x(F(x) → G(x))", True, None, "Kısıtlı tümel geniş kapsamda yadsınır."),
                ("∃x(F(x) ∧ ¬G(x))", True, None, "Eşdeğer karşı örnek formudur."),
                ("∀x(F(x) → ¬G(x))", False, "translation.negation_scope", "Hepsi değil, hiçbir araştırmacı diye güçlendirilmiştir."),
            ],
            teaching_point="Kısıtlı tümelin yadsınması F ve ¬G ortak tanığını gerektirir.",
        ),
        _symbolization_fixture(
            "e31-no-researcher-curious",
            "Hiçbir araştırmacı meraklı değildir.",
            [
                ("∀x(F(x) → ¬G(x))", "Her araştırmacı için meraklılık yadsınır.", "Hiçbir araştırmacı meraklı değildir."),
                ("¬∃x(F(x) ∧ G(x))", "Araştırmacı ve meraklı ortak tanığı dışlanır.", "Hem araştırmacı hem meraklı biri yoktur."),
            ],
            [
                ("∀x(F(x) → ¬G(x))", True, None, "Kısıtlı hiçbiri kalıbıdır."),
                ("¬∃x(F(x) ∧ G(x))", True, None, "Eşdeğer ortak-tanık yadsımasıdır."),
                ("¬∀x(F(x) → G(x))", False, "translation.negation_scope", "Yalnız bir karşı örnek hiçbiri için yetmez."),
            ],
            teaching_point="Hiçbiri, F ve G kesişimini bütünüyle dışlar.",
        ),
        _symbolization_fixture(
            "e31-not-everyone-knows-someone",
            "Herkesin birini tanıdığı doğru değildir.",
            [
                ("¬∀x∃yT(x,y)", "Olumsuzluk bütün ∀∃ iddiasını kapsar.", "En az bir kişi hiç kimseyi tanımıyor."),
                ("∃x¬∃yT(x,y)", "Tümel yadsıma karşı örnek kişiyi görünür kılar.", "Hiç kimseyi tanımayan en az bir kişi var."),
            ],
            [
                ("¬∀x∃yT(x,y)", True, None, "Geniş kapsam doğru kurulmuştur."),
                ("∃x¬∃yT(x,y)", True, None, "Eşdeğer karşı örnek yapısıdır."),
                ("∀x¬∃yT(x,y)", False, "translation.negation_scope", "En az bir kişi yerine hiç kimse kimseyi tanımıyor denmiştir."),
            ],
            teaching_point="Dıştaki tümelin yadsınması bir x karşı örneği bulur.",
        ),
        _symbolization_fixture(
            "e31-someone-not-known-by-all",
            "Herkes tarafından tanınmayan en az bir kişi vardır.",
            [
                ("∃y¬∀xT(x,y)", "Bir y seçilir ve bütün x'lerin onu tanıdığı iddiası yadsınır.", "En az bir kişi vardır; onu tanımayan biri bulunur."),
                ("∃y∃x¬T(x,y)", "Niceleyici olumsuzlaması tanımayan x tanığını görünür kılar.", "Bir kişi ve onu tanımayan bir kişi vardır."),
            ],
            [
                ("∃y¬∀xT(x,y)", True, None, "Ortak y için tümel tanınma yadsınmıştır."),
                ("∃y∃x¬T(x,y)", True, None, "Eşdeğer tanımayan çift formudur."),
                ("∃y∀x¬T(x,y)", False, "translation.negation_scope", "Bir kişi hiç kimse tarafından tanınmıyor diye güçlendirilmiştir."),
            ],
            teaching_point="Herkes tarafından tanınmamak, hiç kimse tarafından tanınmamak değildir.",
        ),
        _symbolization_fixture(
            "e31-ambiguous-everyone-did-not-arrive",
            "Herkes geç kalmadı.",
            [
                ("¬∀xH(x)", "Cümle 'hepsi geç kalmadı' anlamında kullanılıyorsa.", "Geç kalmayan en az bir kişi vardır."),
                ("∀x¬H(x)", "Cümle 'hiç kimse geç kalmadı' anlamında kullanılıyorsa.", "Hiç kimse geç kalmadı."),
            ],
            [
                ("¬∀xH(x)", True, None, "Hepsi değil okuması açıkça temsil edilir."),
                ("∀x¬H(x)", True, None, "Hiçbiri okuması açıkça temsil edilir."),
                ("¬∃x¬H(x)", False, "translation.negation_scope", "Bu, herkesin geç kaldığını söyleyen farklı bir yapıdır."),
            ],
            teaching_point="Bağlam verilmezse iki okuma da koşuluyla birlikte tutulur.",
        ),
    ]
    return lesson


def _candidate_e32():
    lesson = _lesson(
        "E32",
        "ders-fol-kimlik-sayisal-ifadeler",
        "Kimlik ve Sayısal İfadeler",
        "Kimliği benzerlikten ayırır; 'başka', 'yalnız', 'hariç', en az, en çok ve tam olarak ifadelerini açık varlık ve farklılık koşullarıyla kurar.",
        "Kimlik, farklılık ve nicelik sayma kalıpları",
        45,
        ["ders-fol-kapsam-niceleyici-olumsuzlama"],
        [
            "fol.identity_read",
            "fol.distinctness_construct",
            "fol.cardinality_at_least",
            "fol.cardinality_at_most",
            "fol.cardinality_exactly",
        ],
        [
            "a=b ifadesini iki adın aynı nesneyi gösterdiği iddiası olarak okumak.",
            "x≠y ile iki tanığın farklı olmasını açıkça zorunlu kılmak.",
            "'Başka', 'kendisi dışında', 'yalnız' ve 'hariç' kalıplarının kimlik koşullarını ayırmak.",
            "En az iki ve en az üç için bütün gerekli ikili farklılıkları yazmak.",
            "En çok bir ve en çok iki kalıplarını koşullu kimlikle kurmak.",
            "Tam olarak n ifadesini varlık ile üst sınırın birlikte sağlanması olarak açıklamak.",
        ],
        [
            ("Kimlik", "İki terimin aynı alan nesnesini gösterdiğini söyleyen = bağıntısı."),
            ("Farklılık", "İki terimin farklı nesneleri gösterdiğini söyleyen x≠y, yani ¬(x=y), koşulu."),
            ("Eş gönderim", "Farklı adların aynı nesneyi göstermesi; a=b bunun mantıksal iddiasıdır."),
            ("Ayrık tanık", "Başka bir tanıkla özdeş olmadığı açık bir ≠ koşuluyla belirtilen nesne."),
            ("Alt sınır", "En az n farklı nesnenin hedef özelliği taşıdığını söyleyen koşul."),
            ("Üst sınır", "n'den fazla farklı hedef nesne bulunmasını dışlayan koşul."),
            ("Tam sayı koşulu", "Aynı özellik için alt ve üst sınırın birlikte kurulması."),
            ("Varlık önkabulu", "Gündelik 'yalnız' veya 'hariç' ifadesinin hedef nesnenin gerçekten varlığını ayrıca gerektirip gerektirmediği."),
        ],
        [
            _section(
                "Kimlik benzerlik değil, aynı nesnedir",
                "a=b, Ada ve Bora adlarının benzer kişileri değil aynı alan nesnesini gösterdiğini söyler. = mantıksal bir işarettir; sembol anahtarında yeni bir yüklem değildir.",
                "İki adın veya değişkenin aynı nesneyi gösterip göstermediği ifade edilirken.",
                "a=b · x=y · x≠y kısaltması: ¬(x=y)",
                "Önce iki terimin gönderimini sor; aynı gönderim iddia ediliyorsa =, farklı gönderim zorunluysa ≠ kullan.",
                "a=b'yi Ada ile Bora'nın aynı özelliklere sahip olması diye okumak.",
                [
                    ("a=b", "Ada adı ile Bora adı aynı kişiyi gösterir."),
                    ("a≠b", "Ada ile Bora farklı kişilerdir."),
                    ("F(a) ∧ F(b)", "İki adın da araştırmacı olması onların aynı kişi olduğunu göstermez."),
                ],
                (
                    "Terimlerin özelliklerini değil gönderimlerini karşılaştırmak.",
                    "Aynı özellikleri taşıyan nesneleri özdeş saymak.",
                    "Kimlik, nitel benzerlikten daha güçlüdür.",
                ),
            ),
            _section(
                "İki niceleyici iki farklı tanık garanti etmez",
                "∃x∃y(F(x)∧F(y)) ifadesinde x ile y aynı kişiyi seçebilir. En az iki araştırmacı için x≠y ayrıca yazılmalıdır.",
                "'İki', 'başka biri' veya 'farklı kişiler' denildiğinde.",
                "∃x∃y((F(x) ∧ F(y)) ∧ x≠y)",
                "Her yeni tanık için hedef özellikleri yaz; sonra ayrı olması gereken tanık çiftlerini ≠ ile bağla.",
                "Değişken harfleri farklı olduğu için nesnelerin de kendiliğinden farklı olduğunu sanmak.",
                [
                    ("∃x∃y(F(x) ∧ F(y))", "Bir araştırmacı bile bu formülü doğru yapabilir."),
                    ("∃x∃y((F(x) ∧ F(y)) ∧ x≠y)", "En az iki farklı araştırmacı vardır."),
                    ("∀x∃y(x≠y ∧ T(x,y))", "Herkes kendisi dışında en az birini tanır."),
                ],
                (
                    "Değişken adı ile seçilen nesneyi ayrı tutmak.",
                    "x ve y harflerini farklılık kanıtı saymak.",
                    "Farklılık nesnelere ilişkin ek bir iddiadır.",
                ),
            ),
            _section(
                "En az n: tanıkları kur ve bütün çiftleri ayır",
                "En az iki için bir, en az üç için üç ikili farklılık gerekir. Üç tanıkta x≠y ve y≠z yazmak x ile z'nin aynı olmasını hâlâ mümkün bırakır.",
                "Bir özelliği taşıyan en az iki veya üç nesne sayılırken.",
                "en az 3: F(x), F(y), F(z), x≠y, x≠z, y≠z",
                "n tanığı yaz; her tanığa yüklemi uygula; sonra n(n−1)/2 farklı tanık çiftinin tamamını denetle.",
                "Zincir biçiminde iki farklılık yazarak bütün üçlünün ayrık olduğunu sanmak.",
                [
                    ("∃xF(x)", "En az bir araştırmacı vardır."),
                    ("∃x∃y((F(x) ∧ F(y)) ∧ x≠y)", "En az iki farklı araştırmacı vardır."),
                    ("x≠y, x≠z, y≠z", "Üç tanığın bütün ikili farklılık listesi."),
                ],
                (
                    "Tanıkları düğüm, ≠ koşullarını bütün çiftleri birleştiren kenar olarak kontrol etmek.",
                    "Üç tanıkta yalnız komşu harfleri ayırmak.",
                    "Her tanık çifti ayrı ayrı farklılaştırılır.",
                ),
            ),
            _section(
                "En çok n: fazla tanıkların çakışmasını zorunlu kıl",
                "En çok bir F, herhangi iki F tanığının aynı olmasını ister. En çok iki F ise üç F tanığından en az ikisinin aynı olmasını zorunlu kılar.",
                "Bir sınıfın üst sınırı belirtilirken ve varlık iddiası eklenmek istenmezken.",
                "en çok 1: ∀x∀y((F(x)∧F(y))→x=y)",
                "n+1 keyfi hedef tanığı varsay; bunlardan en az ikisinin özdeş olması gerektiğini sonuçta yaz.",
                "En çok bir cümlesine gereksizce ∃xF(x) ekleyip hiç F bulunmaması olasılığını dışlamak.",
                [
                    ("∀x∀y((F(x) ∧ F(y)) → x=y)", "Araştırmacı sayısı sıfır veya birdir."),
                    ("¬∃x∃y((F(x) ∧ F(y)) ∧ x≠y)", "İki farklı araştırmacı bulunamaz."),
                    ("∀x∀y∀z(((F(x) ∧ F(y)) ∧ F(z)) → ((x=y ∨ x=z) ∨ y=z))", "Üç araştırmacı adayı arasında en az bir eşit çift vardır."),
                ],
                (
                    "Üst sınırın varlık değil fazla ayrık tanık yasağı olduğunu görmek.",
                    "En çok biri tam olarak bir diye okumak.",
                    "Üst sınır tek başına alt sınır kurmaz.",
                ),
            ),
            _section(
                "Tam olarak n: alt ve üst sınırı birlikte kur",
                "Tam olarak bir, en az bir ve en çok bir koşullarını; tam olarak iki ise iki farklı tanık ve bütün hedef nesnelerin bu ikisinden biri olması koşulunu birlikte gerektirir.",
                "Sayı hem eksik hem fazla olamayacak biçimde sabitlenirken.",
                "tam 2: ∃x∃y(Fx ∧ Fy ∧ x≠y ∧ ∀z(Fz→(z=x∨z=y)))",
                "Önce gerekli farklı tanıkları kur; sonra keyfi bir hedef nesnenin seçilmiş tanıklardan birine eşit olduğunu söyle.",
                "Yalnız varlığı yazarak fazladan örnekleri veya yalnız üst sınırı yazarak sıfır örneği açık bırakmak.",
                [
                    ("∃x(F(x) ∧ ∀y(F(y) → y=x))", "Tam olarak bir araştırmacı vardır."),
                    ("∃x∃y(((F(x) ∧ F(y)) ∧ x≠y) ∧ ∀z(F(z) → (z=x ∨ z=y)))", "Tam olarak iki araştırmacı vardır."),
                    ("∃x∃y((F(x) ∧ F(y)) ∧ x≠y)", "Yalnız en az iki; üçüncü araştırmacıyı dışlamaz."),
                ],
                (
                    "Formülü alt sınır ve üst sınır diye iki renkte denetlemek.",
                    "Tam sayıyı yalnız bir yarısıyla ifade etmek.",
                    "Tamlık iki bağımsız sınırın birleşimidir.",
                ),
            ),
            _section(
                "Yalnız ve hariç: varlık iddiasını açıklaştır",
                "'Yalnız Ada araştırmacıdır' hem F(a)'yı hem bütün araştırmacıların Ada olduğunu söyler. 'Ada hariç herkes görevlendirildi' ise tek başına Ada'nın görevlendirilmediğini söylemeyebilir.",
                "Doğal dil bir kişiyi tek örnek veya istisna olarak sunduğunda.",
                "yalnız Ada F: F(a) ∧ ∀x(F(x)→x=a)",
                "Önce hedef kişinin özelliği taşıdığını ayrıca ileri sürüp sürmediğini; sonra diğer nesnelerin nasıl kısıtlandığını yaz.",
                "'Yalnız Ada F' için sadece ∀x(F(x)→x=a) yazıp Ada'nın F olmasını garanti ettiğini sanmak.",
                [
                    ("(F(a) ∧ ∀x(F(x) → x=a))", "Ada araştırmacıdır ve başka araştırmacı yoktur."),
                    ("∀x(x≠a → G(x))", "Ada dışındaki herkes görevlendirildi; Ada'nın durumu açık bırakılır."),
                    ("(¬G(a) ∧ ∀x(x≠a → G(x)))", "Ada görevlendirilmedi, diğer herkes görevlendirildi."),
                ],
                (
                    "Varlık, teklik ve istisna iddialarını ayrı satırlarda yazmak.",
                    "Gündelik vurguya gizlenmiş varlık koşulunu otomatik varsaymak veya unutmak.",
                    "Doğal dil önkabulleri formülde açık karara dönüşür.",
                ),
            ),
            _section(
                "Kimlik kalıplarını geri çeviriyle denetle",
                "Kimlik içeren uzun formüllerde yalnız sembol dizisine bakmak hata üretir. Her = ve ≠ koşulu doğal dilde ayrı okunmalı, sonra bütün formülün sayı iddiası yeniden kurulmalıdır.",
                "En az/en çok/tam olarak formülü tamamlandıktan sonra.",
                "tanıklar → farklılıklar → kapsama sınırı → geri çeviri",
                "Seçilen tanıkları listele, her farklılık çiftini oku, en içteki üst sınırı açıklayıp tam cümleye dön.",
                "Doğru şablona benzediği için eksik bir farklılık veya varlık koşulunu gözden kaçırmak.",
                [
                    ("x=y", "x ile y aynı nesnedir."),
                    ("x≠y", "x ile y farklı nesnelerdir."),
                    ("∀z(F(z) → (z=x ∨ z=y))", "Her araştırmacı x veya y'den biridir."),
                ],
                (
                    "Her atomik kimlik iddiasını sesli geri okumak.",
                    "Kalıbı anlamadan ezberden kopyalamak.",
                    "Geri çeviri eksik sınırı görünür kılar.",
                ),
            ),
        ],
        [
            _worked("a=b", "İki adın aynı alan nesnesini gösterdiği ileri sürülür.", "Ada, Bora ile aynı kişidir"),
            _worked("a≠b", "≠, ¬(a=b) kısaltmasıdır.", "Ada ile Bora farklı kişilerdir"),
            _worked("∀x∃y(x≠y ∧ T(x,y))", "Her x için ondan farklı bir y tanığı seçilir.", "Herkes kendisi dışında birini tanır"),
            _worked("∃x∃y((F(x) ∧ F(y)) ∧ x≠y)", "İki F tanığı açık farklılıkla ayrılır.", "En az iki araştırmacı var"),
            _worked("∃x∃y∃z((((F(x) ∧ F(y)) ∧ F(z)) ∧ x≠y) ∧ (x≠z ∧ y≠z))", "Üç F tanığı ve üç ikili farklılık birlikte kurulur.", "En az üç araştırmacı var"),
            _worked("∀x∀y((F(x) ∧ F(y)) → x=y)", "Her iki F tanığı çakışmak zorundadır.", "En çok bir araştırmacı var"),
            _worked("∀x∀y∀z(((F(x) ∧ F(y)) ∧ F(z)) → ((x=y ∨ x=z) ∨ y=z))", "Üç F adayı arasında eşit bir çift bulunmalıdır.", "En çok iki araştırmacı var"),
            _worked("∃x(F(x) ∧ ∀y(F(y) → y=x))", "Bir F vardır ve bütün F'ler odur.", "Tam olarak bir araştırmacı var"),
            _worked("∃x∃y(((F(x) ∧ F(y)) ∧ x≠y) ∧ ∀z(F(z) → (z=x ∨ z=y)))", "İki farklı F vardır ve başka F yoktur.", "Tam olarak iki araştırmacı var"),
            _worked("(F(a) ∧ ∀x(F(x) → x=a))", "Ada'nın F oluşu ile teklik koşulu birlikte yazılır.", "Yalnız Ada araştırmacıdır"),
            _worked("∃x∃y(F(x) ∧ F(y))", "x ve y aynı kişiyi seçebildiği için iki farklı araştırmacı çıkmaz.", "Eksik farklılık", "bad"),
            _worked("∀x∀y((F(x) ∧ F(y)) → x≠y)", "İki F varsa farklı olmasını istemek sayıyı üstten sınırlamaz; hatta tek F aynı değişkenle çelişki üretir.", "Yanlış üst sınır", "bad"),
        ],
        [
            "='yi aynı özelliklere sahip olma veya benzerlik diye okumak.",
            "Farklı değişkenlerin kendiliğinden farklı nesneler seçtiğini sanmak.",
            "En az iki formülünde x≠y koşulunu unutmak.",
            "En az üçte x≠z gibi bir ikili farklılığı atlamak.",
            "En çok bir formülünü varoluş iddiası sanmak.",
            "En çok iki için üç hedef tanığı değil yalnız iki tanığı karşılaştırmak.",
            "Tam olarak birde varlık veya teklik yarısından yalnız birini yazmak.",
            "Tam olarak ikide seçilen iki tanık dışındaki hedefleri dışlamamak.",
            "'Yalnız Ada' cümlesinde F(a) varlık koşulunu unutmak.",
            "'Ada hariç' ifadesinin Ada hakkında olumsuz iddia taşıyıp taşımadığını açıklamamak.",
        ],
        _practice(
            [
                ("a=b ne söyler?", ["a ve b aynı nesneyi gösterir", "a ile b benzerdir", "a ve b aynı yüklemdir", "a, b'yi tanır"], "a ve b aynı nesneyi gösterir", "Kimlik gönderimlerin aynılığıdır.", "Temel"),
                ("x≠y hangi yapının kısaltmasıdır?", ["¬(x=y)", "F(x)∧F(y)", "x=y", "¬F(x)"], "¬(x=y)", "Farklılık kimliğin yadsınmasıdır.", "Temel"),
                ("∃x∃y(F(x)∧F(y)) neden en az iki F demez?", ["x ve y aynı nesneyi seçebilir", "İki ∃ yasaktır", "F tek yerli değildir", "Alan boş olmalıdır"], "x ve y aynı nesneyi seçebilir", "Niceleyiciler ayrık tanık garantilemez.", "Temel"),
                ("En az iki F için eksik olmayan koşul hangisidir?", ["∃x∃y((F(x)∧F(y))∧x≠y)", "∃x∃y(F(x)∧F(y))", "∀xF(x)", "∃xF(x)"], "∃x∃y((F(x)∧F(y))∧x≠y)", "İki F tanığı açıkça ayrılır.", "Orta"),
                ("Üç tanık için kaç ikili farklılık gerekir?", ["3", "2", "1", "6"], "3", "x≠y, x≠z ve y≠z gerekir.", "Orta"),
                ("En çok bir F formülü F'nin varlığını garanti eder mi?", ["Hayır", "Evet", "Yalnız alan doluysa", "Yalnız iki ad varsa"], "Hayır", "Sıfır F de üst sınırı sağlar.", "Orta"),
                ("∀x∀y((F(x)∧F(y))→x=y) ne söyler?", ["En çok bir F vardır", "En az iki F vardır", "Tam iki F vardır", "Her şey F'dir"], "En çok bir F vardır", "Her iki F tanığı aynı olmak zorundadır.", "Orta"),
                ("Tam olarak bir F için hangi iki parça gerekir?", ["Varlık ve en çok bir", "İki varlık", "Yalnız en çok bir", "Yalnız en az iki"], "Varlık ve en çok bir", "Tamlık alt ve üst sınırı birleştirir.", "Orta"),
                ("En çok iki F kontrolünde neden üç değişken kullanılır?", ["Üç F adayı arasında ikisini eşitlemek için", "Arite üç olduğu için", "Alan üç kişi olduğu için", "Bir değişken serbest kalsın diye"], "Üç F adayı arasında ikisini eşitlemek için", "Üç farklı F olasılığı dışlanır.", "İleri"),
                ("'Yalnız Ada F'dir' için F(a) neden ayrıca gerekir?", ["Ada'nın gerçekten F olduğunu garanti etmek için", "a'yı değişken yapmak için", "Alanı doldurmak için", "Kimliği kaldırmak için"], "Ada'nın gerçekten F olduğunu garanti etmek için", "∀x(F(x)→x=a) tek başına hiç F yokken de doğrudur.", "İleri"),
                ("∀x(x≠a→G(x)) Ada hakkında ne söyler?", ["G olup olmadığını açık bırakır", "Kesinlikle G değildir", "Kesinlikle G'dir", "Ada yoktur"], "G olup olmadığını açık bırakır", "Koşul yalnız a'dan farklı nesnelere uygulanır.", "İleri"),
                ("Tam olarak iki F formülünün üst sınır parçası hangisidir?", ["∀z(F(z)→(z=x∨z=y))", "x≠y", "F(x)∧F(y)", "∃x∃y"], "∀z(F(z)→(z=x∨z=y))", "Her F seçilen iki tanıktan biri olmak zorundadır.", "İleri"),
            ]
        ),
        {
            "prompt": "Bir özellik için en az bir, en az iki, en az üç, en çok bir, en çok iki, tam bir ve tam iki formüllerini aynı anahtar altında kur; her birini tanık, farklılık ve sınır tablosuyla geri oku.",
            "starter": "Önce gerekli tanık sayısını ve bütün farklı tanık çiftlerini listele; üst sınır gerekiyorsa bir fazla keyfi tanığı denetle.",
            "checks": [
                "Kimlik benzerlik değil aynı gönderim olarak okundu",
                "En az iki için x≠y açıkça yazıldı",
                "En az üç için üç ikili farklılık tamamlandı",
                "En çok kalıpları gereksiz varlık iddiası eklemedi",
                "Tam sayı kalıpları alt ve üst sınırı birlikte kurdu",
                "Yalnız ve hariç cümlelerinde varlık önkabulleri açıklandı",
                "Her uzun formül doğal dile geri çevrildi",
            ],
            "solution": "Kontrol örneği: tam iki F, iki farklı F tanığı ve her F'nin bu iki tanıktan biri olması koşuludur.",
        },
        [
            _production_task(
                "Kendi bağlamında bir kimlik vakası, bir 'başka', bir 'yalnız/hariç' ve en az/en çok/tam olarak sayı cümleleri üret; her formülü tanık-farklılık-sınır tablosuyla denetle.",
                [
                    "Alan, adlar ve yüklemler açık anahtarla verildi.",
                    "Kimlik ile nitel benzerlik ayrıldı.",
                    "Başka/kendisi dışında cümlesinde ≠ koşulu doğru bağlandı.",
                    "En az üçte bütün ikili farklılıklar yazıldı.",
                    "En çok bir ve en çok iki varlık iddiasından ayrıldı.",
                    "Tam bir ve tam iki alt-üst sınır bileşimiyle kuruldu.",
                    "Yalnız/hariç ifadesinin varlık önkabulu açıklandı.",
                    "Her formül geri çeviriyle denetlendi.",
                ],
                "Değerlendirme şablon ezberinden çok her =/≠ koşulunun işlevini ve sayı sınırlarının eksiksizliğini ölçer.",
                "Bağlam",
                ["Araştırma ekibi", "Kütüphane koleksiyonu", "Turnuva katılımcıları", "Aile ilişkileri", "Kendi sayı bağlamın"],
                "En az bir örnekte gündelik 'yalnız' ifadesinin varlık önkabulünü tartış.",
            ),
        ],
        [
            "Kimliği aynı özelliklere sahip olmaktan ayırma.",
            "İki tanığın farklılığı için açık ≠ koşulu kurma.",
            "En az üçte bütün ikili farklılıkları eksiksiz yazma.",
            "En çok bir ve en çok iki kalıplarını varlık iddiasından ayırma.",
            "Tam olarak bir ve ikiyi alt-üst sınır bileşimiyle kurma.",
            "Yalnız ve hariç cümlelerinde varlık önkabullerini açıklama.",
        ],
        [
            "a=b neden a ile b'nin benzer olduğu anlamına gelmez?",
            "İki varoluş niceleyicisi neden iki farklı nesne garanti etmez?",
            "En az üçte hangi farklılık çiftleri gerekir?",
            "En çok bir neden tam olarak bir değildir?",
            "Tam olarak iki formülünde üst sınır hangi parçada kurulur?",
            "Yalnız ve hariç ifadelerinde hangi varlık iddiaları ayrıca kararlaştırılır?",
        ],
        "E33'te bu uzun formülleri oluşturan terim ve formül kurallarını tümevarımsal olarak kesinleştirecek; serbest/bağlı oluşum ile güvenli yerine koymayı öğreneceğiz.",
        ["forallx-identity", "forallx-multiple-generality", "forallx-fol-sentences", "mit-logic-sequence"],
        "Ders standart özdeşlikli birinci-derece mantığı kullanır. Sayı ifadeleri sonlu sayı şemalarıdır; betimlemeler kuramı, fonksiyon sembolleri ve kimliğin kanıt kuralları bu aşamada açılmaz.",
        ["ders-29-kimlik-yuklemler-ve-alan"],
    )
    lesson["fol_signature"] = E32_SIGNATURE
    lesson["syntax_scope"] = {
        "introduced": [
            "identity",
            "distinctness",
            "at_least_n",
            "at_most_n",
            "exactly_n",
            "only_except_patterns",
        ],
        "review_only": [
            "multiple_quantifier",
            "quantifier_negation",
            "conditional_restriction",
            "argument_order",
        ],
        "locked_until_later": [
            "identity_proof_rules",
            "definite_descriptions",
            "function_symbols",
            "formal_model_truth",
            "substitution",
        ],
    }
    lesson["syntax_fixtures"] = [
        _syntax_fixture("e32-name-identity", "a=b", accepted=True, category="sentence", explanation="İki ad arasındaki kimlik kapalı cümledir."),
        _syntax_fixture("e32-name-distinct", "a≠b", accepted=True, category="sentence", explanation="≠, kimliğin yadsınması olarak ayrıştırılır."),
        _syntax_fixture("e32-variable-identity", "x=y", accepted=True, category="open_formula", explanation="İki değişken de serbesttir."),
        _syntax_fixture("e32-bound-identity", "∀x∃y(x=y ∨ F(y))", accepted=True, category="sentence", explanation="Kimlik atomu niceleyicilerin kapsamındadır."),
        _syntax_fixture("e32-other", "∀x∃y(x≠y ∧ T(x,y))", accepted=True, category="sentence", explanation="Her kişi için farklı bir tanık bağlanır."),
        _syntax_fixture("e32-at-least-two", "∃x∃y((F(x) ∧ F(y)) ∧ x≠y)", accepted=True, category="sentence", explanation="İki farklı F tanığı vardır."),
        _syntax_fixture("e32-at-most-one", "∀x∀y((F(x) ∧ F(y)) → x=y)", accepted=True, category="sentence", explanation="Her iki F tanığı özdeş olmak zorundadır."),
        _syntax_fixture("e32-exactly-one", "∃x(F(x) ∧ ∀y(F(y) → y=x))", accepted=True, category="sentence", explanation="Varlık ve teklik birlikte kurulur."),
        _syntax_fixture("e32-exactly-two", "∃x∃y(((F(x) ∧ F(y)) ∧ x≠y) ∧ ∀z(F(z) → (z=x ∨ z=y)))", accepted=True, category="sentence", explanation="İki farklı tanık ve üst sınır vardır."),
        _syntax_fixture("e32-identity-right-missing", "a=", accepted=False, issue_code="identity.right_term_missing", explanation="Kimliğin sağ terimi eksiktir."),
        _syntax_fixture("e32-distinct-right-missing", "x≠", accepted=False, issue_code="identity.right_term_missing", explanation="Farklılığın sağ terimi eksiktir."),
        _syntax_fixture("e32-unknown-term", "a=q", accepted=False, issue_code="term.unknown", explanation="q anahtarda terim değildir."),
        _syntax_fixture("e32-bare-term", "a", accepted=True, category="name", explanation="Ad bir terimdir; sınıflandırılır fakat tek başına formül değildir."),
        _syntax_fixture("e32-bad-equality-target", "a=F(a)", accepted=False, issue_code="term.expected", explanation="Kimliğin sağında formül değil terim gerekir."),
    ]
    lesson["symbolization_fixtures"] = [
        _symbolization_fixture(
            "e32-same-person",
            "Ada, Bora ile aynı kişidir.",
            [("a=b", "İki adın gönderimi özdeşleştirilir.", "Ada ve Bora adları aynı kişiyi gösterir.")],
            [
                ("a=b", True, None, "Kimlik doğrudan kurulmuştur."),
                ("b=a", True, None, "Kimlik simetriktir."),
                ("(F(a) ∧ F(b))", False, "translation.identity_missing", "Ortak özellik aynı kişi olmayı göstermez."),
            ],
            teaching_point="Kimlik, ortak yüklemden değil aynı gönderimden söz eder.",
        ),
        _symbolization_fixture(
            "e32-different-people",
            "Ada ile Bora farklı kişilerdir.",
            [("a≠b", "İki ad arasındaki kimlik yadsınır.", "Ada, Bora değildir.")],
            [
                ("a≠b", True, None, "Farklılık açıkça kurulmuştur."),
                ("b≠a", True, None, "Farklılık simetriktir."),
                ("a=b", False, "translation.distinctness_missing", "Kimlik, hedef farklılığın tersidir."),
            ],
            teaching_point="≠, ayrı değişken harflerinden bağımsız bir nesne iddiasıdır.",
        ),
        _symbolization_fixture(
            "e32-knows-other",
            "Herkes kendisi dışında en az birini tanır.",
            [("∀x∃y(x≠y ∧ T(x,y))", "Tanıdığı kişi x'ten farklı olmak zorundadır.", "Her kişi için ondan farklı, tanıdığı bir kişi vardır.")],
            [
                ("∀x∃y(x≠y ∧ T(x,y))", True, None, "Farklı tanık ve bağıntı aynı y üzerinde birleşir."),
                ("∀x∃yT(x,y)", False, "translation.distinctness_missing", "Kişinin kendisini seçmesi engellenmemiştir."),
                ("∀x∃y(x≠y ∧ T(y,x))", False, "translation.argument_order", "Tanıyan ve tanınan rolleri ters çevrilmiştir."),
            ],
            teaching_point="'Başka' sözcüğü tanığın farklılığını formüle ekler.",
        ),
        _symbolization_fixture(
            "e32-at-least-two",
            "En az iki araştırmacı vardır.",
            [("∃x∃y((F(x) ∧ F(y)) ∧ x≠y)", "İki F tanığı açıkça ayrılır.", "Birbirinden farklı en az iki araştırmacı vardır.")],
            [
                ("∃x∃y((F(x) ∧ F(y)) ∧ x≠y)", True, None, "İki farklı F tanığı kurulmuştur."),
                ("∃x∃y(F(x) ∧ F(y))", False, "translation.distinctness_missing", "İki değişken aynı araştırmacıyı seçebilir."),
                ("∀x∀y((F(x) ∧ F(y)) → x≠y)", False, "translation.quantifier_kind", "Alt sınır yerine hatalı tümel koşul kurulmuştur."),
            ],
            teaching_point="Tanık sayısını değişken sayısı değil ≠ koşulu garanti eder.",
        ),
        _symbolization_fixture(
            "e32-at-most-one",
            "En çok bir araştırmacı vardır.",
            [
                ("∀x∀y((F(x) ∧ F(y)) → x=y)", "Her iki F tanığı çakışır.", "İki araştırmacı adayı varsa aynı kişidir."),
                ("¬∃x∃y((F(x) ∧ F(y)) ∧ x≠y)", "İki farklı F tanığı dışlanır.", "İki farklı araştırmacı yoktur."),
            ],
            [
                ("∀x∀y((F(x) ∧ F(y)) → x=y)", True, None, "Koşullu kimlik üst sınırı kurar."),
                ("¬∃x∃y((F(x) ∧ F(y)) ∧ x≠y)", True, None, "İki farklı tanık yadsınmıştır."),
                ("∃xF(x)", False, "translation.identity_missing", "Varlık teklik sağlamaz."),
            ],
            teaching_point="En çok bir, hiç örnek bulunmaması olasılığıyla uyumludur.",
        ),
        _symbolization_fixture(
            "e32-exactly-one",
            "Tam olarak bir araştırmacı vardır.",
            [("∃x(F(x) ∧ ∀y(F(y) → y=x))", "Bir F tanığı vardır ve bütün F'ler ona eşittir.", "Bir araştırmacı vardır ve başka araştırmacı yoktur.")],
            [
                ("∃x(F(x) ∧ ∀y(F(y) → y=x))", True, None, "Alt ve üst sınır birleşmiştir."),
                ("∃xF(x)", False, "translation.identity_missing", "Yalnız varlık vardır; fazladan araştırmacılar dışlanmaz."),
                ("∀x∀y((F(x) ∧ F(y)) → x=y)", False, "translation.quantifier_kind", "Yalnız üst sınır vardır; araştırmacı bulunmayabilir."),
            ],
            teaching_point="Tam bir, varlık ile teklik koşulunun ikisini de ister.",
        ),
        _symbolization_fixture(
            "e32-exactly-two",
            "Tam olarak iki araştırmacı vardır.",
            [("∃x∃y(((F(x) ∧ F(y)) ∧ x≠y) ∧ ∀z(F(z) → (z=x ∨ z=y)))", "İki farklı F vardır ve bütün F'ler bu ikisinden biridir.", "Tam iki farklı araştırmacı vardır.")],
            [
                ("∃x∃y(((F(x) ∧ F(y)) ∧ x≠y) ∧ ∀z(F(z) → (z=x ∨ z=y)))", True, None, "Alt ve üst sınır eksiksizdir."),
                ("∃x∃y((F(x) ∧ F(y)) ∧ x≠y)", False, "translation.identity_missing", "En az iki vardır; üçüncü tanık dışlanmamıştır."),
                ("∃x∃y((F(x) ∧ F(y)) ∧ ∀z(F(z) → (z=x ∨ z=y)))", False, "translation.distinctness_missing", "Seçilen iki tanığın farklılığı garanti edilmemiştir."),
            ],
            teaching_point="Tam iki formülünde farklılık ve kapsama üst sınırı bağımsız denetlenir.",
        ),
        _symbolization_fixture(
            "e32-only-ada",
            "Yalnız Ada araştırmacıdır.",
            [("(F(a) ∧ ∀x(F(x) → x=a))", "Ada F'dir ve her F Ada'dır.", "Ada araştırmacıdır; ondan başka araştırmacı yoktur.")],
            [
                ("(F(a) ∧ ∀x(F(x) → x=a))", True, None, "Varlık ve yalnızlık birlikte kurulmuştur."),
                ("∀x(F(x) → x=a)", False, "translation.quantifier_scope", "Ada'nın araştırmacı olması garanti edilmemiştir."),
                ("F(a)", False, "translation.identity_missing", "Başka araştırmacılar dışlanmamıştır."),
            ],
            teaching_point="'Yalnız Ada' hem Ada'nın özelliğini hem tekliğini ileri sürer.",
        ),
        _symbolization_fixture(
            "e32-except-ada",
            "Ada hariç herkes görevlendirildi; Ada'nın durumu belirtilmiyor.",
            [("∀x(x≠a → G(x))", "a'dan farklı bütün nesneler G'dir.", "Ada dışındaki herkes görevlendirildi.")],
            [
                ("∀x(x≠a → G(x))", True, None, "İstisna koşulu Ada'nın durumunu açık bırakır."),
                ("(¬G(a) ∧ ∀x(x≠a → G(x)))", False, "translation.quantifier_scope", "Ada hakkında istenmeyen ek olumsuz iddia vardır."),
                ("∀xG(x)", False, "translation.distinctness_missing", "Ada da görevlendirilmiş sayılmıştır."),
            ],
            teaching_point="Hariç kalıbında istisna kişinin kendi özelliği ayrıca kararlaştırılır.",
        ),
    ]
    return lesson


STAGE_E_CANDIDATE_LESSONS = [
    _candidate_e27(),
    _candidate_e28(),
    _candidate_e29(),
    _candidate_e30(),
    _candidate_e31(),
    _candidate_e32(),
]

STAGE_E_CANDIDATE_MAP = {
    lesson["slug"]: lesson
    for lesson in STAGE_E_CANDIDATE_LESSONS
}
