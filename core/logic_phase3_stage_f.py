"""Release-candidate content for Phase 3, Stage F of the logic course.

Stage F remains isolated from the learner-facing course. Semantic fixtures are
checked by ``logic_fol_semantics``; proof fixtures are added only after the FOL
Fitch auditor has passed its own boundary tests.
"""

from .logic_phase3_stage_a import (
    _lesson,
    _practice,
    _production_task,
    _section,
    _worked,
)


STAGE_F_SOURCE_REFERENCES = {
    "forallx-interpretations": {
        "title": "forall x: Calgary - Extensionality and interpretations",
        "url": "https://forallx.openlogicproject.org/html/Ch30.html",
    },
    "forallx-truth-fol": {
        "title": "forall x: Calgary - Truth in FOL",
        "url": "https://forallx.openlogicproject.org/html/Ch31.html",
    },
    "forallx-semantic-concepts": {
        "title": "forall x: Calgary - Semantic concepts",
        "url": "https://forallx.openlogicproject.org/html/Ch32.html",
    },
    "forallx-using-interpretations": {
        "title": "forall x: Calgary - Using interpretations",
        "url": "https://forallx.openlogicproject.org/html/Ch33.html",
    },
    "forallx-reasoning-interpretations": {
        "title": "forall x: Calgary - Reasoning about interpretations",
        "url": "https://forallx.openlogicproject.org/html/Ch34.html",
    },
    "forallx-relation-properties": {
        "title": "forall x: Calgary - Properties of relations",
        "url": "https://forallx.openlogicproject.org/html/Ch35.html",
    },
    "forallx-fol-rules": {
        "title": "forall x: Calgary - Basic rules for FOL",
        "url": "https://forallx.openlogicproject.org/html/Ch36.html",
    },
    "forallx-quantifier-proofs": {
        "title": "forall x: Calgary - Proofs with quantifiers",
        "url": "https://forallx.openlogicproject.org/html/Ch37.html",
    },
    "forallx-identity-rules": {
        "title": "forall x: Calgary - Rules for identity",
        "url": "https://forallx.openlogicproject.org/html/Ch39.html",
    },
    "forallx-proofs-semantics": {
        "title": "forall x: Calgary - Proofs and semantics",
        "url": "https://forallx.openlogicproject.org/html/Ch41.html",
    },
    "mit-fol-semantics": {
        "title": "MIT OpenCourseWare Logic I - Predicate logic sequence",
        "url": "https://ocw.mit.edu/courses/24-241-logic-i-fall-2009/pages/calendar/",
    },
}


F35_SIGNATURE = {
    "domain": "atölyedeki insanlar",
    "names": {"a": "Ada", "b": "Bora", "c": "Ada'nın diğer adı"},
    "variables": ["x", "y", "z"],
    "predicates": {
        "F": {"arity": 1, "reading": "x araştırmacı"},
        "G": {"arity": 1, "reading": "x zamanında geldi"},
        "R": {
            "arity": 2,
            "reading": "x, y'ye güveniyor",
            "roles": ["güvenen", "güvenilen"],
        },
    },
}


F35_MODEL = {
    "label": "Atölye yorumu M",
    "domain": ["ada", "bora", "cem"],
    "names": {"a": "ada", "b": "bora", "c": "ada"},
    "predicates": {
        "F": ["ada", "cem"],
        "G": ["ada", "bora", "cem"],
        "R": [["ada", "bora"], ["bora", "cem"], ["cem", "cem"]],
    },
}


F37_SIGNATURE = {
    "domain": "üç düğümlü bir ağ",
    "names": {"a": "birinci düğüm", "b": "ikinci düğüm"},
    "variables": ["x", "y", "z"],
    "predicates": {
        "R": {
            "arity": 2,
            "reading": "x, y ile R bağıntısında",
            "roles": ["başlangıç", "bitiş"],
        },
        "F": {"arity": 1, "reading": "x işaretli düğüm"},
    },
}


FOL_PROOF_SIGNATURE = {
    "domain": "kanıtta konu edilen nesneler",
    "names": {"a": "Ada", "b": "Bora", "c": "keyfi/taze nesne", "d": "dördüncü nesne"},
    "variables": ["x", "y", "z"],
    "predicates": {
        "F": {"arity": 1, "reading": "x araştırmacı"},
        "G": {"arity": 1, "reading": "x dikkatli"},
        "H": {"arity": 1, "reading": "x rapor verdi"},
        "K": {"arity": 1, "reading": "x koordinatör"},
        "R": {"arity": 2, "reading": "x, y'ye danıştı", "roles": ["danışan", "danışılan"]},
    },
}


def _stage_f_lesson(*args, **kwargs):
    lesson = _lesson(*args, **kwargs)
    lesson.update(
        {
            "fol_signature": {},
            "model_fixtures": [],
            "semantic_fixtures": [],
            "countermodel_fixtures": [],
            "relation_fixtures": [],
            "proof_fixtures": [],
            "semantic_cross_checks": [],
            "capstone_fixtures": [],
        }
    )
    return lesson


def _proof_line(line_id, formula, rule, citations=(), *, depth=0, opens=None, closes=()):
    return {
        "id": line_id,
        "formula": formula,
        "rule": rule,
        "citations": list(citations),
        "depth": depth,
        "opens": opens,
        "closes": list(closes),
    }


def _cite(line_id):
    return {"kind": "line", "id": line_id}


def _cite_subproof(start, end):
    return {"kind": "subproof", "start": start, "end": end}


def _proof_fixture(fixture_id, kind, premises, target, lines, expected_codes=()):
    return {
        "id": fixture_id,
        "kind": kind,
        "proof": {"premises": premises, "target": target, "lines": lines},
        "expected_codes": list(expected_codes),
    }


def _candidate_f35():
    lesson = _stage_f_lesson(
        "F35",
        "ders-35-yorum-gonderim-ve-dogruluk",
        "Yorum, Gönderim ve Doğruluk",
        "FOL işaretlerini bir alan, ad gönderimleri, yüklem uzantıları ve değişken ataması içinde değerlendirir; cümle doğruluğunu doğal dil sezgisinden değil açık yorum verisinden çıkarır.",
        "Bir yorumda doğruluk",
        40,
        ["ders-fol-belirsizlik-sembollestirme-atolyesi"],
        [
            "fol_semantics.interpretation_read",
            "fol_semantics.term_denotation",
            "fol_semantics.atomic_evaluate",
            "fol_semantics.assignment_use",
            "fol_semantics.quantifier_trace",
        ],
        [
            "Alan, ad gönderimi ve yüklem uzantısını birbirinden ayırmak.",
            "Bir ve çok yerli atomik formülleri uzantı üyeliğiyle değerlendirmek.",
            "Kimliğin sabit yorumunu adların yazılışından ayırmak.",
            "Açık formül için atama gerektiğini, cümlede dış atamanın sonucu değiştirmediğini göstermek.",
            "Niceleyicinin her alan üyesi üzerindeki dallarını tanık veya karşı örnekle açıklamak.",
        ],
        [
            ("Yorum", "Bir FOL imzasına alan, ad gönderimleri ve yüklem uzantıları veren yapı."),
            ("Alan", "Niceleyicilerin üzerinde dolaştığı boş olmayan nesneler kümesi."),
            ("Gönderim", "Bir ad sembolünü yorumun alanındaki tam bir nesneye bağlayan eşleme."),
            ("Uzantı", "Bir yüklemin yorumda doğru olduğu nesne veya sıralı tuple'lar kümesi."),
            ("Değişken ataması", "Değişkenleri alan üyelerine geçici olarak gönderen eşleme."),
            ("Doyurma", "Bir nesne atamasının açık formülü doğru kılması."),
            ("Tanık", "Varoluşsal formülün gövdesini doğru yapan alan üyesi."),
            ("Karşı örnek üye", "Tümel formülün gövdesini yanlış yapan alan üyesi."),
        ],
        [
            _section(
                "Yorumun dört işi",
                "Yorum, sembollerin gündelik anlamını tahmin etmez; alanı, her adı ve her yüklemin doğru olduğu tuple'ları açıkça belirler. Kimlik işareti ayrıca yorumlanmaz.",
                "Bir model çizimini veya veri tablosunu FOL cümleleriyle eşleştirirken.",
                "M = ⟨D, ad gönderimleri, yüklem uzantıları⟩",
                "Aynı formül farklı yorumlarda farklı doğruluk değeri alabilir; değişen sözdizim değil yorumdur.",
                "Alan ile F yükleminin uzantısını aynı liste sanma: alan bütün aday nesneleri, F yalnız F olanları içerir.",
                [
                    ("D={ada,bora,cem}; F={ada,cem}", "Bora alanın üyesidir ama F'nin uzantısında değildir."),
                    ("a↦ada, c↦ada", "İki ayrı ad aynı nesneye gönderilebilir."),
                ],
                (
                    "Her sembol bileşenini yorum tablosunda ayrı okumak.",
                    "Doğal dilde araştırmacı olmayanı alan dışına çıkarmak.",
                    "Yüklem kısıtı alanı değil uzantıyı belirler.",
                ),
            ),
            _section(
                "Ad gönderimi ve kimlik",
                "Bir adın değeri, yorumun ona gönderdiği alan üyesidir. `a=c`, iki işaret aynı nesneye gidiyorsa doğrudur; harflerin farklı olması kimliksizliği garanti etmez.",
                "Ad içeren atomları ve `=`/`≠` cümlelerini değerlendirirken.",
                "⟦a⟧ᴹ = ada; a=c doğru iff ⟦a⟧ᴹ=⟦c⟧ᴹ",
                "Kimlik, yorumdan yoruma uzantısı seçilen sıradan bir ikili yüklem değildir.",
                "Benzeyen nesneleri özdeş sayma; burada ölçüt aynı alan üyesi olmalarıdır.",
                [
                    ("a=c", "M'de iki ad da ada'ya gittiği için doğrudur."),
                    ("a≠b", "ada ve bora farklı alan üyeleri olduğu için doğrudur."),
                ],
                (
                    "Önce iki terimin gönderimini bulup karşılaştırmak.",
                    "a ve c farklı harfler, öyleyse a≠c demek.",
                    "Sözdizimsel ayrılık semantik ayrılık değildir.",
                ),
            ),
            _section(
                "Atomik doğruluk ve sıralı tuple",
                "Bir yüklem uygulaması, terimlerin değerlerinden oluşan sıralı tuple yüklemin uzantısındaysa doğrudur.",
                "Tek ve çok yerli atomları değerlendirirken.",
                "R(t₁,t₂) doğru iff (⟦t₁⟧,⟦t₂⟧) ∈ Rᴹ",
                "İki yerli uzantıda sıra, E29'daki argüman rollerini semantik olarak korur.",
                "(ada,bora) uzantıda diye (bora,ada)yı sessizce ekleme; simetri ayrı bir iddiadır.",
                [
                    ("F(a)", "ada, F uzantısında olduğu için doğru."),
                    ("R(a,b)", "(ada,bora) uzantıda olduğu için doğru."),
                    ("R(b,a)", "(bora,ada) uzantıda olmadığı için yanlış."),
                ],
                (
                    "Terimleri yorumlayıp doğru sırayla tuple kurmak.",
                    "İlişkinin gündelik anlamından eksik çiftleri tahmin etmek.",
                    "Model yalnız açıkça verilen uzantıyı içerir.",
                ),
            ),
            _section(
                "Açık formül ve atama",
                "`F(x)` tek başına yorumda doğru veya yanlış bir cümle değildir; `x` için bir atama verildiğinde doyurulur ya da doyurulmaz.",
                "Serbest değişken içeren formülleri sınarken.",
                "M,g ⊨ F(x) iff g(x) ∈ Fᴹ",
                "Niceleyici, atamayı kendi değişkeni için geçici değiştirir; başka değişken değerlerini korur.",
                "Değişkeni bilinmeyen bir ad gibi okuma veya açık formüle atamasız doğruluk değeri verme.",
                [
                    ("g(x)=cem altında F(x)", "cem F uzantısında: doğru."),
                    ("g(x)=bora altında F(x)", "bora F uzantısında değil: yanlış."),
                ],
                (
                    "Önce serbest oluşumları bulup atamayı tamamlamak.",
                    "F(x) açıkken yalnız M vererek yanlış demek.",
                    "Eksik g girdisi bir yanlışlık değil, değerlendirme eksikliğidir.",
                ),
            ),
            _section(
                "Bağlaçlarda içten dışa değerlendirme",
                "Atomlar yorumda değerlendirildikten sonra TFL bağlaçlarının doğruluk koşulları değişmeden uygulanır.",
                "Karmaşık FOL cümlesinin ana işlemini hesaplarken.",
                "M ⊨ (𝒜→ℬ) iff M⊭𝒜 veya M⊨ℬ",
                "FOL ile gelen yenilik atom içi ve niceleyicidir; `¬`, `∧`, `∨`, `→`, `↔` Faz C'deki anlamını korur.",
                "Koşulun artbileşeni yanlış diye bütünü otomatik yanlış sayma; önbileşeni de denetle.",
                [
                    ("F(b)→G(b)", "Önbileşen yanlış olduğu için koşul doğrudur."),
                    ("F(a)∧G(a)", "İki atom da doğru olduğu için birleşim doğrudur."),
                ],
                (
                    "Alt formülleri değerlendirip en son ana bağlacı uygulamak.",
                    "Cümlenin doğal dilde makul oluşuna göre değer vermek.",
                    "Biçimsel sonuç yalnız yorum ve doğruluk koşulundan çıkar.",
                ),
            ),
            _section(
                "Niceleyici dalları, tanık ve karşı örnek",
                "Tümel niceleyici her alan üyesini sınar; varoluşsal niceleyici en az bir doğru dal arar. Alanın adı olmayan üyeleri de mutlaka sınanır.",
                "`∀` ve `∃` ile başlayan cümleleri değerlendirirken.",
                "∀x𝒜: bütün d∈D; ∃x𝒜: en az bir d∈D",
                "Niceleyici adlar üzerinde değil alan üyeleri üzerinde dolaşır. Adı olmayan cem de dallara girer.",
                "Yalnız a,b,c adlarını tarayıp alanı tükettiğini sanma; adlar ortak gönderime de sahip olabilir.",
                [
                    ("∀xG(x)", "ada, bora ve cem G'yi doyurur: doğru."),
                    ("∀xF(x)", "bora karşı örnektir: yanlış."),
                    ("∃xF(x)", "ada veya cem tanıktır: doğru."),
                ],
                (
                    "Alan listesini dal dal kaydedip belirleyici üyeyi göstermek.",
                    "Bir adı olmayan üyeyi niceleyici dışında bırakmak.",
                    "Niceleyicinin kapsamı alanın tüm üyelerini kapsar.",
                ),
            ),
        ],
        [
            _worked("M'nin alanı {ada,bora,cem}, F uzantısı {ada,cem}dir.", "Bora alan dışı değil; yalnız F olmayan bir alan üyesidir.", "Doğru ayrım"),
            _worked("a ve c aynı nesneye gönderildiği için a=c doğrudur.", "Farklı adların farklı nesne varsayımı yoktur.", "Doğru"),
            _worked("R(a,b) doğru, R(b,a) yanlıştır.", "Sıralı ikililer yönü korur.", "Doğru"),
            _worked("F(x), g(x)=cem altında doğrudur.", "Açık formül yorum ve atamayla değerlendirilmiştir.", "Doğru"),
            _worked("∀xF(x) yanlıştır; karşı örnek bora'dır.", "Tek yanlış dal tümeli yanlış yapar.", "Karşı örnek"),
            _worked("∃xF(x) doğrudur; ada tanıktır.", "Tek doğru dal varoluşu doğrular.", "Tanık"),
            _worked("∀x∃yR(x,y) doğrudur.", "ada için bora, bora için cem, cem için cem ayrı tanıklardır.", "Bağımlı tanık"),
            _worked("∃y∀xR(x,y) yanlıştır.", "Hiçbir tek y bütün x'lerden R oku almıyor.", "Ortak tanık yok"),
            _worked("Alan yalnız F uzantısıdır.", "Bu, F olmayan bora'yı niceleyici taramasından siler.", "Yanlış", "bad"),
            _worked("F(x) M'de yanlıştır.", "Atama verilmediği için henüz doğruluk değerlendirmesi yapılamaz.", "Eksik girdi", "bad"),
            _worked("a ve c farklı harf olduğu için a≠c.", "Ad yazımları değil gönderimler karşılaştırılır.", "Yanlış", "bad"),
            _worked("Bir modelde doğru olan cümle mantıksal olarak geçerlidir.", "Tek yorumdaki doğruluk bütün yorumlarda doğruluk değildir.", "Düzey hatası", "bad"),
        ],
        [
            "Alanı yüklem uzantısıyla özdeş saymak.",
            "Farklı adlara benzersiz ad varsayımı eklemek.",
            "İkili yüklem uzantısında sıralı ikili yönünü unutmak.",
            "Açık formüle atamasız doğru/yanlış demek.",
            "Niceleyiciyi yalnız adlandırılmış nesneler üzerinde dolaştırmak.",
            "Bir yorumdaki doğruluktan mantıksal geçerlilik çıkarmak.",
        ],
        _practice(
            [
                ("M'de bora hangi kümeye kesinlikle üyedir?", ["Yalnız F uzantısına", "Yalnız G uzantısına", "Alana ve G uzantısına", "Alan dışına"], "C", "Bora alan üyesi ve G uzantısındadır; F uzantısında değildir.", "Temel"),
                ("a ve c aynı nesneye gidiyorsa hangisi doğrudur?", ["a≠c", "a=c", "F(a)↔¬F(c)", "Hiçbiri belirlenemez"], "B", "Kimlik aynı gönderime göre değerlendirilir.", "Temel"),
                ("R(b,a) neden yanlıştır?", ["b alan dışı", "R simetrik değil", "(bora,ada) uzantıda yok", "a ve b aynıdır"], "C", "Atomik doğruluk tam sıralı tuple üyeliğine bağlıdır.", "Temel"),
                ("F(x) için hangi ek bilgi gerekir?", ["Yeni bir ad", "x'in atama değeri", "Yeni bir alan", "R uzantısı"], "B", "x serbest olduğu için atama gerekir.", "Temel"),
                ("∀xF(x)i yanlış yapan belirleyici üye hangisidir?", ["ada", "bora", "cem", "a adı"], "B", "Bora F uzantısında değildir.", "Orta"),
                ("∃xF(x)i doğrulamak için ne yeterlidir?", ["Her üyenin F olması", "Bir alan üyesinin F olması", "Bir adın bulunması", "F uzantısının alan olması"], "B", "Varoluşsal için tek tanık yeterlidir.", "Temel"),
                ("∀x∃yR(x,y) için y nasıl seçilebilir?", ["Her x için değişebilir", "Bütün x'ler için tek olmalı", "Yalnız adı olanlardan", "Alan dışından"], "A", "İç varoluşsal tanık dış tümel değişkene bağlı olabilir.", "Orta"),
                ("∃y∀xR(x,y) ne ister?", ["Her x için ayrı y", "Tek bir y'nin bütün x'lerce hedeflenmesini", "R'nin boş olmasını", "Yalnız R(a,b)yi"], "B", "Dış varoluşsal ortak tanık seçer.", "Orta"),
                ("Kimliğin uzantısını neden ayrıca yazmıyoruz?", ["Kimlik yasak", "Sabit olarak gerçek özdeşliktir", "Her zaman yanlış", "Yalnız adlarda kullanılır"], "B", "= yorumdan yoruma serbestçe değişmez.", "Orta"),
                ("Bir cümle M'de doğruysa ne kanıtlanmıştır?", ["FOL geçerliliği", "Yalnız M'deki doğruluğu", "Bütün modellerde doğruluğu", "Kanıtlanabilirliği"], "B", "Tek yorum sonucu genellenemez.", "Orta"),
                ("Adı olmayan cem niceleyici dallarına girer mi?", ["Hayır", "Yalnız ∃ altında", "Evet", "Yalnız F ise"], "C", "Niceleyici adları değil alan üyelerini dolaşır.", "Orta"),
                ("İç ∃x, dıştaki x atamasına ne yapar?", ["Kalıcı siler", "Kendi kapsamında geçici gölgeler", "Değiştirmez", "Formülü bozar"], "B", "İç bağlayıcı aynı harfin dış değerini kendi kapsamında gölgeler.", "İleri"),
            ]
        ),
        {
            "prompt": "M yorumunda ∀x(F(x)→G(x)) cümlesini alanın her üyesi için değerlendir.",
            "starter": "Önce x=ada, x=bora, x=cem dallarını aç; her dalda F ve G değerlerini ayrı yaz.",
            "checks": [
                "Her alan üyesi tam bir kez sınandı mı?",
                "F olmayan bora dalında koşulun neden doğru olduğu açıklandı mı?",
                "Son tümel değer ancak bütün dallardan sonra verildi mi?",
            ],
            "solution": "ada dalı T→T=T; bora dalı F→T=T; cem dalı T→T=T. Bütün dallar doğru olduğundan tümel cümle M'de doğrudur.",
        },
        [
            _production_task(
                "Üç nesneli yeni bir yorum kur ve altı cümleyi içten dışa değerlendir.",
                ["Alan boş değil", "Her ad tam bir üyeye gidiyor", "Uzantılar ariteye uygun", "Her niceleyici tanık/karşı örnek kaydı taşıyor"],
                "Örnek çözüm, doğal dil sezgisi yerine gönderim ve tuple üyeliğini gösterir.",
                "Değerlendirilecek cümleler",
                ["F(a)", "a=b", "R(a,b)", "∀x(F(x)→G(x))", "∃xF(x)", "∀x∃yR(x,y)"],
                "En az bir ad başka bir adla aynı nesneye gönderilsin ve en az bir alan üyesi adsız kalsın.",
            ),
            _production_task(
                "Bir açık formül ile bir cümlenin değerlendirme girdilerini karşılaştır.",
                ["Serbest oluşumlar işaretli", "Atama açık", "Niceleyici gölgelemesi doğru", "Cümle sonucunun dış atamadan bağımsızlığı gösterilmiş"],
                "Karşılaştırma, F(x) ile ∀xF(x)i aynı tür semantik nesne saymaz.",
                "Karşılaştırma çifti",
                ["F(x)", "∀xF(x)", "∃yR(x,y)", "∀x∃yR(x,y)"],
            ),
        ],
        [
            "Eksiksiz ve ariteye uygun yeni bir yorum tablosu.",
            "En az sekiz formül için terim gönderimi ve atom üyeliğini içeren doğruluk izi.",
            "Bir varoluş tanığı ve bir tümel karşı örnek üyenin açık gösterimi.",
            "Açık formül/cümle ayrımını atama üzerinden açıklayan kısa rapor.",
        ],
        [
            "Alan ile bir yerli yüklemin uzantısı arasındaki fark nedir?",
            "İki ayrı ad hangi koşulda kimlik cümlesini doğru yapar?",
            "Bir açık formülü değerlendirmek için yorumdan başka ne gerekir?",
            "∀x∃y ile ∃y∀x doğruluk dalları neden farklıdır?",
        ],
        "F36'da tek cümle doğruluğundan argüman düzeyine geçecek ve karşı model kuracaksın.",
        ["forallx-interpretations", "forallx-truth-fol", "mit-fol-semantics"],
        "Model, amaçlanan gerçek dünyanın eksiksiz resmi değildir. Bu derste yalnız verilen tek yorum altında doğruluk belirlenir; mantıksal sonuç tek modelden çıkarılmaz.",
        ["Yüklem Mantığında Semantik ve Modeller"],
    )
    lesson["fol_signature"] = F35_SIGNATURE
    lesson["model_fixtures"] = [F35_MODEL]
    lesson["semantic_fixtures"] = [
        {"id": "f35-atomic-true", "model": "Atölye yorumu M", "formula": "F(a)", "assignment": {}, "expected": True, "decisive_kind": "extension_member"},
        {"id": "f35-atomic-false", "model": "Atölye yorumu M", "formula": "R(b,a)", "assignment": {}, "expected": False, "decisive_kind": "extension_member"},
        {"id": "f35-co-reference", "model": "Atölye yorumu M", "formula": "a=c", "assignment": {}, "expected": True, "decisive_kind": "denotations"},
        {"id": "f35-open-true", "model": "Atölye yorumu M", "formula": "F(x)", "assignment": {"x": "cem"}, "expected": True, "decisive_kind": "extension_member"},
        {"id": "f35-conditional", "model": "Atölye yorumu M", "formula": "∀x(F(x) → G(x))", "assignment": {}, "expected": True, "decisive_kind": "counterexample"},
        {"id": "f35-universal-counterexample", "model": "Atölye yorumu M", "formula": "∀xF(x)", "assignment": {}, "expected": False, "decisive_kind": "counterexample", "decisive_value": "bora"},
        {"id": "f35-existential-witness", "model": "Atölye yorumu M", "formula": "∃xF(x)", "assignment": {}, "expected": True, "decisive_kind": "witness", "decisive_value": "ada"},
        {"id": "f35-dependent-witness", "model": "Atölye yorumu M", "formula": "∀x∃yR(x,y)", "assignment": {}, "expected": True, "decisive_kind": "counterexample"},
        {"id": "f35-shared-witness-fails", "model": "Atölye yorumu M", "formula": "∃y∀xR(x,y)", "assignment": {}, "expected": False, "decisive_kind": "witness"},
    ]
    return lesson


def _candidate_f36():
    lesson = _stage_f_lesson(
        "F36",
        "ders-36-model-ve-karsi-model-kurma",
        "Model ve Karşı Model Kurma",
        "Bir argümanın semantik hedefini bütün öncüller doğru ve sonuç yanlış biçiminde kurar; tek karşı modelin kesin gücüyle sınırlı örneklemde karşı model bulamamanın sınırlı sonucunu ayırır.",
        "Semantik sonuç ve karşı model",
        40,
        ["ders-35-yorum-gonderim-ve-dogruluk"],
        [
            "fol_semantics.consequence_profile",
            "fol_semantics.countermodel_build",
            "fol_semantics.domain_minimize",
            "fol_semantics.sample_limit_explain",
            "fol_semantics.model_repair",
        ],
        [
            "Mantıksal sonuç tanımını yorumlar üzerindeki koşullu bir iddia olarak okumak.",
            "Karşı model hedefini bütün öncüller doğru, sonuç yanlış biçiminde kurmak.",
            "Alan, ad ve uzantıları en az taahhütle sistematik olarak seçmek.",
            "Niceleyici sırası, varoluşsal ithal ve kimlik hatalarına küçük karşı modeller üretmek.",
            "Sonlu örneklem aramasının başarısızlığından geçerlilik sonucu çıkarmamak.",
        ],
        [
            ("Model", "Belirli FOL cümlelerini doğru yapan yorum; bağlama göre yorumla eş anlamlı kullanılabilir."),
            ("Karşı model", "Bir argümanın bütün öncüllerini doğru, sonucunu yanlış yapan yorum."),
            ("Mantıksal sonuç", "Öncüllerin doğru olduğu her yorumda sonucun da doğru olması."),
            ("Geçersizlik", "En az bir karşı model bulunması."),
            ("Model profili", "Bir yorumda öncül ve sonucun doğru/yanlış değerlerinin sıralı kaydı."),
            ("Sınırlı arama", "Yalnız verilmiş veya belirli büyüklüğe kadar üretilmiş modelleri denetleyen, tam olmayan arama."),
        ],
        [
            _section(
                "Argüman düzeyinde semantik hedef",
                "Bir argüman tek bir cümle değildir. Geçersizlik için aynı yorumda bütün öncüller doğru ve sonuç yanlış olmalıdır.",
                "Bir FOL argümanına modelle karar vermeye başlarken.",
                "Karşı model profili: P₁=T, …, Pₙ=T, C=F",
                "Bir öncülü de yanlış yapan yorum argümana karşı örnek değildir; öncüllerin birlikte sonucu zorlamadığını göstermeliyiz.",
                "Sonucu yanlış yapan ilk yorumu kabul etme; bütün öncülleri tek tek denetle.",
                [("∃xF(x) ∴ ∀xF(x)", "Bir F ve bir F olmayan üyeli iki nesneli model karşı modeldir."), ("∀xF(x) ∴ F(a)", "Boş olmayan klasik alanda karşı model beklenmez; ama örnek arama tek başına ispat değildir.")],
                ("Önce hedef doğruluk profilini yazmak.", "Yalnız sonucu yanlış yapan yorum çizmek.", "Karşı model bütün öncülleri de doğru tutmalıdır."),
            ),
            _section(
                "Küçük model stratejisi",
                "Önce tek üyeli alanı dene; sonuç bir ayrım veya farklı tanık gerektiriyorsa ikinci üyeyi ekle. Her yeni üye ve tuple bir taahhüttür.",
                "Elle karşı model üretirken.",
                "En küçük alan → gerekli ad gönderimleri → gerekli doğru atomlar → sonucu yanlış tut",
                "Küçük model doğruluğu kolay denetlenir ve hangi yapının çıkarımı bozduğunu görünür kılar.",
                "Alan boyutunu küçültmeyi amaç uğruna zorlamayın; `a≠b` gibi öncül en az iki üye gerektirir.",
                [("∃xF(x) ∴ F(a)", "İki üye, a'yı F olmayan üyeye; bir adsız üyeyi F'ye gönder."), ("a≠b", "Tek üyeli model bu öncülü doğru yapamaz.")],
                ("Gerekli en küçük alanı gerekçelendirmek.", "Her zaman tek nesne kullanmak.", "Kimliksizlik ve ayrık tanıklar alan alt sınırı koyabilir."),
            ),
            _section(
                "Tümel ve varoluşsal öncülleri birlikte kurmak",
                "Tümel öncül, ilgili her üyeyi kısıtlar; varoluşsal öncül en az bir tanık ister. Aynı nesne birden çok varoluşsal role ancak kimliksizlik engeli yoksa hizmet edebilir.",
                "Karma niceleyici öncülleri doğru tutarken.",
                "Önce ∃ tanıklarını yerleştir, sonra ∀ koşullarını bütün alanda yay",
                "Tanık seçimi tümel koşullarla çelişirse uzantı veya alan tasarımı onarılır.",
                "Farklı varoluş niceleyicilerinin mutlaka farklı tanık istediğini varsayma.",
                [("∃xF(x), ∀x(F(x)→G(x))", "F tanığı G uzantısına da girmelidir."), ("∃xF(x), ∃xG(x)", "Kimliksizlik yoksa aynı üye iki tanık olabilir.")],
                ("Tanıklarla tümel yükümlülükleri çapraz denetlemek.", "Her ∃ için yeni nesne eklemek.", "FOL tanıkların farklılığını ayrıca söylemedikçe dayatmaz."),
            ),
            _section(
                "Niceleyici sırasına karşı model",
                "`∀x∃y` her x için farklı y'lere izin verir; `∃y∀x` tek ortak y ister. Ayrı tanıklar verip ortak tanığı engellemek standart karşı model stratejisidir.",
                "Çoklu genellik çıkarımlarını sınarken.",
                "∀x∃yR(x,y) doğru; ∃y∀xR(x,y) yanlış",
                "İki üyeli çapraz veya öz-ilmek modeli her üyenin bir hedefi olmasını sağlarken ortak hedef bırakmayabilir.",
                "Öncülü doğru yapmak için istemeden bütün okları aynı hedefe yöneltme.",
                [("D={u,v}; R={(u,u),(v,v)}", "Her x kendi y tanığıdır; ortak y yoktur."), ("R={(u,v),(v,v)}", "v ortak hedef olur ve sonuç yanlış tutulamaz.")],
                ("Ayrı tanıkları ve ortak tanık yokluğunu birlikte göstermek.", "Yalnız iki ok çizmenin yettiğini sanmak.", "Okların hedef sütunları ayrıca kontrol edilmelidir."),
            ),
            _section(
                "Bir karşı model kesin; başarısız arama sınırlı",
                "Tek gerçek karşı model evrensel sonuç iddiasını çürütür. Buna karşılık yüzlerce modelde karşı model bulamamak, geriye sınanmamış sonsuz sayıda yorum bırakabilir.",
                "Yazılım destekli model aramasının sonucunu raporlarken.",
                "Bulundu → geçersiz; bulunamadı → yalnız örneklemde bulunamadı",
                "FOL geçerliliği her yorum hakkındadır; sonlu deneme listesi genel ispat değildir.",
                "Arama düğmesinin yeşil sonucunu otomatik geçerlilik sertifikası sayma.",
                [("Karşı model bulundu", "Geçersizlik kesinleşir."), ("3 üyeye kadar bulunamadı", "Yalnız arama sınırı raporlanır; kanıt gerekir.")],
                ("Sonucu epistemik gücüne göre adlandırmak.", "Bulunamadı eşittir geçerli demek.", "Arama başarısızlığı ile evrensel semantik ispat farklıdır."),
            ),
            _section(
                "Modeli geri denetleme ve onarma",
                "Karşı model adayını tabloya çevir: her öncülün tanık/karşı örneğini, sonra sonucun yanlışlık nedenini kaydet. Başarısız satır hangi bileşenin onarılacağını gösterir.",
                "Karmaşık bir model çizimini teslim etmeden önce.",
                "Alan → gönderimler → atomlar → niceleyici dalları → profil",
                "Denetim sırası sözdizim ve semantik hatayı ayırır; yanlış formülü doğru modele uydurmaya çalışma riskini azaltır.",
                "Yalnız görsel sezgiyle 'oluyor' demek veya ad gönderimlerini kaydetmemek.",
                [("P₂ yanlış çıktı", "Uzantıyı onar veya bu modelin karşı model olamayacağını kabul et."), ("C de doğru çıktı", "Sonucun tanığını/evrensel dallarını bozacak kontrollü değişiklik yap.")],
                ("Her formülün değerini ayrı iz ile doğrulamak.", "Yalnız hedef sonucu kontrol etmek.", "Karşı model bir bütün doğruluk profilidir."),
            ),
        ],
        [
            _worked("∃xF(x) ∴ ∀xF(x) için D={u,v}, F={u} karşı modeldir.", "Öncül u tanığıyla doğru; sonuç v karşı örneğiyle yanlıştır.", "Karşı model"),
            _worked("∀xF(x) ∴ ∃xF(x) için tek üyeli model karşı model olamaz.", "Boş olmayan alanda tümel doğruysa o üye varoluşa tanık olur.", "Doğru sınır"),
            _worked("∀x∃yR(x,y) ∴ ∃y∀xR(x,y) için R={(u,u),(v,v)} karşı modeldir.", "Ayrı tanıklar vardır, ortak tanık yoktur.", "Karşı model"),
            _worked("∃xF(x) ∴ F(a) için adsız F tanığı ve F olmayan a gönderimi kullanılır.", "Adlar alanın bütün üyelerini tüketmek zorunda değildir.", "Karşı model"),
            _worked("a≠b ∴ ∃x∃y x≠y karşı modelsiz görünür.", "Öncül zaten iki farklı alan üyesi sağlar; sonuç aynı üyelerle doğrudur.", "Semantik gerekçe"),
            _worked("Sonucu yanlış yapan ama ilk öncülü de yanlış model.", "Bütün öncüller doğru olmadığı için karşı model değildir.", "Reddedildi", "bad"),
            _worked("İki ∃ cümlesi için zorunlu olarak iki nesne eklemek.", "Kimliksizlik yoksa tek üye iki cümleye de tanık olabilir.", "Gereksiz taahhüt", "bad"),
            _worked("100 modelde karşı örnek yok; demek ki geçerli.", "FOL'de yorumların tamamı sonlu örneklemle tüketilmez.", "Yanlış sonuç", "bad"),
            _worked("Karşı modelde bir adı alan dışı nesneye göndermek.", "Bu yorum değil, model sözleşmesi ihlalidir.", "Geçersiz model", "bad"),
            _worked("∀x(F(x)→G(x)) öncülünü F boş yaparak doğru tutmak.", "Başka öncül F varlığını istemiyorsa boş F uzantısı lisanslıdır.", "Boş uzantı"),
            _worked("∃xF(x) öncülü varken F'yi boş bırakmak.", "Varoluşsal tanık yoktur; profil başarısızdır.", "Onarım gerekli", "bad"),
            _worked("Model raporunda '2 üyeye kadar karşı model yok' yazmak.", "Sonuç sınırı dürüstçe korur ve geçerlilik iddia etmez.", "Doğru rapor"),
        ],
        [
            "Yalnız sonucu yanlış yapıp öncülleri kontrol etmemek.",
            "Her varoluşsal niceleyici için zorunlu ayrı nesne varsaymak.",
            "Kimliksizlik öncülüne rağmen tek üyeli alanda ısrar etmek.",
            "Niceleyici sırası karşı modelinde yanlışlıkla ortak tanık bırakmak.",
            "Sonlu örnek aramasını geçerlilik ispatı saymak.",
            "Model olmayan eksik/alan dışı veriyi karşı model diye sunmak.",
        ],
        _practice(
            [
                ("Karşı modelde hangi profil gerekir?", ["En az bir öncül F, sonuç F", "Bütün öncüller T, sonuç F", "Bütün cümleler T", "Bütün cümleler F"], "B", "Karşı model öncüllerin sonucu zorlamadığını gösterir.", "Temel"),
                ("∃xF(x) ∴ ∀xF(x) karşı modeli için en az kaç üye gerekir?", ["0", "1", "2", "3"], "C", "Bir F tanığı ve bir F olmayan karşı örnek gerekir.", "Temel"),
                ("∃xF(x), ∃xG(x) öncülleri neyi zorunlu kılmaz?", ["Boş olmayan alanı", "En az bir F'yi", "En az bir G'yi", "F ve G tanıklarının farklılığını"], "D", "İki tanık aynı nesne olabilir.", "Orta"),
                ("a≠b öncülü alan hakkında ne söyler?", ["En az iki üye", "Tam iki üye", "a ve b alan dışı", "Bütün adlar farklı"], "A", "Bu iki ad farklı alan üyelerine gitmelidir.", "Orta"),
                ("∀x∃yR(x,y)yi doğru tutmanın asgari şartı nedir?", ["Tek ortak y", "Her x için en az bir R-hedefi", "R'nin simetrisi", "Bütün tuple'lar"], "B", "Tanık x'e bağlı değişebilir.", "Orta"),
                ("∃y∀xR(x,y)yi yanlış tutmak için ne gerekir?", ["Hiç R oku olmaması zorunlu", "Her olası y için en az bir x'in ona bağlanmaması", "R'nin geçişli olması", "Tek üyeli alan"], "B", "Her ortak tanık adayının en az bir başarısız x'i olmalıdır.", "İleri"),
                ("Bir karşı model bulunursa hangi sonuç kesindir?", ["Argüman geçersiz", "Argüman geçerli", "Kanıt kısa", "Bütün öncüller yanlış"], "A", "Tek karşı model evrensel sonuç iddiasını çürütür.", "Temel"),
                ("Üç üyeye kadar karşı model bulunamadı. Ne denir?", ["Geçerli", "Tutarsız", "Bu örneklemde karşı model yok", "Kanıtlandı"], "C", "Arama sınırı genel geçerlilik değildir.", "Temel"),
                ("Bir öncül yanlışsa çizim neden karşı model değildir?", ["Sonuç doğru olur", "Karşı model tüm öncülleri doğru ister", "Alan büyüktür", "Adlar eksiktir"], "B", "Hedef profil birlikte sağlanmalıdır.", "Temel"),
                ("∀x(F(x)→G(x))i doğru tutmanın bir yolu hangisi?", ["F boş, G keyfi", "F dolu, G boş", "Her G'yi F yapmak", "Alanı boş yapmak"], "A", "Boş F uzantısında koşul her üyede vacuously doğrudur; alan boş olamaz.", "Orta"),
                ("Model onarımında önce ne sabitlenir?", ["Sonucun yazı tipi", "Hedef doğruluk profili", "En büyük alan", "Bütün yüklemler dolu"], "B", "Onarım hangi değerlerin korunacağını bilmelidir.", "Orta"),
                ("Bir kanıt bulunamadıysa bundan ne çıkar?", ["Geçersizlik", "Karşı model", "Tek başına hiçbir semantik sonuç", "Sonucun yanlışlığı"], "C", "Eksik arama veya strateji hatası olabilir; karşı model gerekir.", "İleri"),
            ]
        ),
        {
            "prompt": "∀x∃yR(x,y) ∴ ∃y∀xR(x,y) argümanına iki üyeli karşı model kur.",
            "starter": "D={u,v} seç. Her x'e en az bir hedef ver; sonra hiçbir hedefin iki x tarafından birden ortaklaşa seçilmemesini sağla.",
            "checks": ["Öncülün u ve v dallarında tanık var mı?", "u ortak tanık mı?", "v ortak tanık mı?", "Sonuç gerçekten yanlış mı?"],
            "solution": "R={(u,u),(v,v)} seç. Öncülde u için u, v için v tanıktır. Sonuçta y=u seçilirse x=v dalı; y=v seçilirse x=u dalı başarısız olur.",
        },
        [
            _production_task(
                "Dört geçersiz FOL argümanının her birine küçük karşı model kur.",
                ["Hedef profil yazılı", "Alan alt sınırı gerekçeli", "Ad gönderimleri eksiksiz", "Her öncül ve sonuç izi kayıtlı"],
                "Çözüm yalnız çizim değil, makinece denetlenebilir model tablosu ve doğruluk profili sunar.",
                "Argümanlar",
                ["∃xF(x) ∴ F(a)", "∃xF(x) ∴ ∀xF(x)", "∀x∃yR(x,y) ∴ ∃y∀xR(x,y)", "∀x(F(x)∨G(x)) ∴ (∀xF(x)∨∀xG(x))"],
            ),
            _production_task(
                "Karşı model bulamayan sınırlı bir arama raporunu akademik olarak düzelt.",
                ["Arama alanı açık", "Geçerlilik iddiası kaldırılmış", "Sonraki kanıt yöntemi önerilmiş", "Karşı model bulunursa sonuç ayrı belirtilmiş"],
                "Rapor, yazılım çıktısının kanıt gücünü abartmaz.",
                "Ham rapor",
                ["Alan boyutu 1-3 arasında 420 model denendi.", "Karşı model bulunamadı.", "Bu nedenle argüman geçerlidir."],
                "Son cümleyi düzelt ve hangi ek yöntemin gerektiğini yaz.",
            ),
        ],
        [
            "En az dört argüman için eksiksiz karşı model ve doğruluk profili.",
            "Her modelin neden daha küçük olamayacağını veya küçültülebileceğini açıklama.",
            "Bir başarısız model adayını ilk bozulan öncülü göstererek onarma.",
            "Sınırlı arama sonucu ile mantıksal geçerlilik arasındaki farkı doğru raporlama.",
        ],
        [
            "Karşı modelin dört doğruluk şartı nasıl yazılır?",
            "İki varoluşsal cümle neden iki farklı nesne gerektirmeyebilir?",
            "Tek karşı model neden kesin, karşı model bulamamak neden sınırlıdır?",
            "∀∃ ile ∃∀ arasındaki farkı hangi küçük model görünür kılar?",
        ],
        "F37'de model uzantılarını kullanarak bağıntıların yapısal özelliklerini ve karşı örnek tuple'larını okuyacaksın.",
        ["forallx-semantic-concepts", "forallx-using-interpretations", "forallx-reasoning-interpretations"],
        "FOL geçerliliği genel olarak sonlu sayıda model çizerek belirlenmez. Aday arama motoru karşı model bulduğunda geçersizlik verir; bulamadığında yalnız arama örnekleminin sınırını raporlar.",
        ["Yüklem Mantığında Semantik ve Modeller"],
    )
    lesson["fol_signature"] = F35_SIGNATURE
    lesson["countermodel_fixtures"] = [
        {
            "id": "f36-existential-to-name",
            "premises": ["∃xF(x)"],
            "conclusion": "F(a)",
            "models": [
                {"label": "karşı model", "domain": ["u", "v"], "names": {"a": "u", "b": "v", "c": "u"}, "predicates": {"F": ["v"], "G": [], "R": []}},
            ],
            "expected_status": "countermodel_found",
        },
        {
            "id": "f36-existential-to-universal",
            "premises": ["∃xF(x)"],
            "conclusion": "∀xF(x)",
            "models": [
                {"label": "karşı model", "domain": ["u", "v"], "names": {"a": "u", "b": "v", "c": "u"}, "predicates": {"F": ["u"], "G": [], "R": []}},
            ],
            "expected_status": "countermodel_found",
        },
        {
            "id": "f36-dependent-to-shared",
            "premises": ["∀x∃yR(x,y)"],
            "conclusion": "∃y∀xR(x,y)",
            "models": [
                {"label": "ayrı tanıklar", "domain": ["u", "v"], "names": {"a": "u", "b": "v", "c": "u"}, "predicates": {"F": [], "G": [], "R": [["u", "u"], ["v", "v"]]}},
            ],
            "expected_status": "countermodel_found",
        },
        {
            "id": "f36-no-claim-from-sample",
            "premises": ["∀xF(x)"],
            "conclusion": "F(a)",
            "models": [
                {"label": "destekleyen örnek", "domain": ["u"], "names": {"a": "u", "b": "u", "c": "u"}, "predicates": {"F": ["u"], "G": [], "R": []}},
            ],
            "expected_status": "no_countermodel_in_sample",
        },
    ]
    return lesson


def _candidate_f37():
    lesson = _stage_f_lesson(
        "F37",
        "ders-37-baginti-ozelliklerini-modellerde-okuma",
        "Bağıntı Özelliklerini Modellerde Okuma",
        "İkili bir yüklemin uzantısından yansıma, simetri, asimetri, ters-simetri, geçişlilik ve serilik gibi özellikleri ayrı tanımlarla denetler; başarısız her özellik için belirleyici tuple verir.",
        "İkili bağıntıların yapısı",
        38,
        ["ders-36-model-ve-karsi-model-kurma"],
        [
            "relation.extension_read",
            "relation.reflexivity_check",
            "relation.symmetry_family_distinguish",
            "relation.transitivity_check",
            "relation.seriality_check",
            "relation.counterexample_tuple",
        ],
        [
            "İkili uzantıyı yönlü kenarlar veya sıralı ikililer olarak okumak.",
            "Yansımalı ile yansımasız, simetrik ile asimetrik ve ters-simetrik kavramlarını ayırmak.",
            "Geçişlilik için bütün iki-adımlı yolları denetlemek.",
            "Serilik için her başlangıç düğümünün en az bir çıkışını göstermek.",
            "Bir özelliğin başarısızlığını en küçük belirleyici üye, ikili veya üçlüyle raporlamak.",
        ],
        [
            ("Yansımalı", "Her alan üyesi x için (x,x) uzantıdadır."),
            ("Yansımasız", "Hiçbir alan üyesi x için (x,x) uzantıda değildir."),
            ("Simetrik", "(x,y) varsa (y,x) de vardır."),
            ("Asimetrik", "(x,y) varsa (y,x) yoktur; dolayısıyla öz-ilmek de olamaz."),
            ("Ters-simetrik", "(x,y) ve (y,x) birlikteyse x=y olmalıdır."),
            ("Geçişli", "(x,y) ve (y,z) varsa (x,z) de vardır."),
            ("Seri", "Her x için en az bir y vardır ve (x,y) uzantıdadır."),
            ("Karşı örnek tuple", "Bir bağıntı özelliğinin evrensel koşulunu bozan en küçük üye dizisi."),
        ],
        [
            _section(
                "Uzantıyı yönlü ağ olarak okumak",
                "Her (x,y) sıralı ikilisi x'ten y'ye yönlü bir ok; (x,x) ise öz-ilmektir. Çizim ile tuple listesi aynı veriyi taşır.",
                "Bir ilişki modelini özellikler bakımından denetlemeye başlarken.",
                "Rᴹ ⊆ D×D",
                "Ok yönü, E29'daki argüman sırasının model karşılığıdır.",
                "Çizgide ok başı görünmüyor diye ilişkiyi simetrik kabul etme; tuple listesi belirleyicidir.",
                [("(u,v)", "u'dan v'ye tek yönlü ok."), ("(u,u)", "u üzerindeki öz-ilmek.")],
                ("Her oku sıralı ikiliyle eşlemek.", "Bağlantıyı yönsüz çizgi sanmak.", "İkili yüklemin iki argüman rolü farklı olabilir."),
            ),
            _section(
                "Yansımalı ve yansımasız",
                "Yansımalı olma her düğümde öz-ilmek ister; yansımasız olma hiçbir düğümde öz-ilmek istemez. İkisi de bütün alanı tarar.",
                "Bir ilişkinin nesnelerin kendileriyle ilişkisini sınıflarken.",
                "Yansımalı: ∀xR(x,x); yansımasız: ∀x¬R(x,x)",
                "Tek eksik öz-ilmek yansımayı; tek mevcut öz-ilmek yansımasızlığı çürütür.",
                "Birçok öz-ilmek var diye yansımalı deme; alanın her üyesini denetle.",
                [("D={u,v}, R={(u,u),(v,v)}", "Yansımalı."), ("R={(u,v)}", "Yansımasız; ayrıca yansımalı değil.")],
                ("Alan listesinden kontrol tablosu yapmak.", "Yalnız uzantıda görünen düğümlere bakmak.", "İlişkisiz alan üyeleri de evrensel tanıma dahildir."),
            ),
            _section(
                "Simetri ailesini ayırmak",
                "Simetri ters okun varlığını; asimetri ters okun yokluğunu; ters-simetri ise iki yön birlikteyse uçların aynı olmasını ister.",
                "Karşılıklı ilişki yapılarını sınıflarken.",
                "Sim: Rxy→Ryx; Asim: Rxy→¬Ryx; Ters-sim: (Rxy∧Ryx)→x=y",
                "Asimetrik ilişki yansımasızdır. Ters-simetrik ilişki ise öz-ilmek taşıyabilir ve simetrik bir ilişkiden farklıdır.",
                "'Simetrik değil' ile 'asimetrik'i eş anlamlı kullanma; bazı çiftlerin tersi varken bazılarının yokluğu iki özelliği de bozabilir.",
                [("{(u,v),(v,u)}", "Simetrik; u≠v ise asimetrik ve ters-simetrik değil."), ("{(u,v)}", "Bu iki üyede asimetrik ve ters-simetrik; simetrik değil.")],
                ("Her tanımı ayrı evrensel koşulla sınamak.", "Bir özelliğin değili ile başka özelliği özdeşlemek.", "Kavramlar mantıksal karşıt değil, farklı koşullardır."),
            ),
            _section(
                "Geçişlilik ve iki-adımlı yollar",
                "Her x→y ve y→z zinciri için x→z kısayolu bulunmalıdır. Tek eksik kısayol geçişliliği çürütür.",
                "Bağıntının zincirleri koruyup korumadığını denetlerken.",
                "(x,y),(y,z)∈R ⇒ (x,z)∈R",
                "Aynı tuple birden çok zincirde rol alabilir; x,y,z'nin farklı olması gerekmez.",
                "Yalnız üç farklı düğümlü yolları denetleme; öz-ilmekli zincirler de tanıma dahildir.",
                [("(u,v),(v,w),(u,w)", "Bu zincir geçişlilik şartını sağlar."), ("(u,v),(v,w) var, (u,w) yok", "(u,v,w) karşı örnek üçlüsüdür.")],
                ("Bütün eşleşen orta uçları sistematik taramak.", "Grafiğe bakıp genel izlenimle karar vermek.", "Geçişlilik yerel iki-adımlı her yolu sınar."),
            ),
            _section(
                "Serilik ve çıkış tanıkları",
                "Seri ilişkide her alan üyesinin en az bir R-hedefi vardır. Hedef kendisi olabilir; ortak hedef zorunlu değildir.",
                "∀x∃yR(x,y) model koşulunu yapısal özellik olarak okurken.",
                "Her x için Out(x)≠∅",
                "Serilik, ∀∃ bağımlılığının ağ karşılığıdır; ∃∀ gibi ortak hedef istemez.",
                "Giriş oku olan düğümü çıkışı var sanma; yönler farklıdır.",
                [("R={(u,u),(v,u)}", "u ve v'nin çıkışı var: seri."), ("R={(u,v)} D={u,v}", "v'nin çıkışı yok: seri değil.")],
                ("Her başlangıç düğümü için bir çıkış tanığı yazmak.", "Her düğüme gelen bir ok aramak.", "Serilik kaynak rolünü evrensel niceleyiciyle tarar."),
            ),
            _section(
                "Özellik profili ve karşı örnek raporu",
                "Aynı ilişki bazı özellikleri taşıyıp bazılarını taşımayabilir. Her hayır kararı, tanımdaki evrensel koşulu bozan belirleyici veriyle desteklenir.",
                "Bir bağıntıyı tek etiket yerine tam profil olarak sunarken.",
                "özellik → holds + counterexample",
                "Karşı örnek yansıma için bir üye, simetri için ikili, geçişlilik için üçlü olabilir.",
                "'Geçişli değil' deyip eksik yolu göstermemek veya yanlış tür karşı örnek vermek.",
                [("simetrik: hayır, (u,v)", "(u,v) var; (v,u) yok."), ("geçişli: hayır, (u,v,w)", "İki adım var; kısayol yok.")],
                ("Her sonuç yanında tanıma uygun gerekçe taşımak.", "Yalnız evet/hayır tablosu vermek.", "Karşı örnek veri, kararın denetlenebilirliğini sağlar."),
            ),
        ],
        [
            _worked("Tam bağıntı D×D yansımalı, simetrik, geçişli ve seridir.", "Bütün sıralı ikililer bulunduğu için bu dört koşul otomatik sağlanır.", "Doğru profil"),
            _worked("Boş bağıntı boş olmayan alanda yansımasız, simetrik, asimetrik, ters-simetrik ve geçişlidir; seri değildir.", "Koşullu özellikler boş uzantıda vacuously doğru; her x için çıkış şartı başarısızdır.", "Sınır örneği"),
            _worked("{(u,v)} iki üyeli alanda asimetrik ve ters-simetriktir.", "Ters ok ve öz-ilmek yoktur.", "Doğru"),
            _worked("{(u,v),(v,u)} simetriktir ama u≠v ise ters-simetrik değildir.", "İki yönlü farklı uçlar ters-simetriyi bozar.", "Karşı örnek"),
            _worked("(u,v),(v,w) var, (u,w) yoksa geçişli değildir.", "(u,v,w) belirleyici karşı örnek üçlüsüdür.", "Karşı örnek"),
            _worked("Her düğümün bir çıkışı varsa ilişki seridir.", "Hedeflerin aynı olması gerekmez.", "Doğru"),
            _worked("Simetrik değil, o hâlde asimetrik.", "Bazı ters çiftler bulunup bazıları eksikse iki özellik de başarısız olabilir.", "Yanlış", "bad"),
            _worked("Ters-simetrik, o hâlde öz-ilmek yok.", "Ters-simetri aynı uçlu çiftlere izin verir.", "Yanlış", "bad"),
            _worked("Geçişlilik yalnız üç farklı düğümde sınanır.", "Tanım x,y,z'nin farklı olmasını istemez.", "Yanlış", "bad"),
            _worked("v'ye ok geliyor, demek ki v serilik şartını sağlıyor.", "Serilik v'den çıkan ok ister.", "Yön hatası", "bad"),
            _worked("Yansımalı değil kararına eksik öz-ilmek u karşı örneği eklenir.", "Tek üye evrensel koşulu çürütür.", "Denetlenebilir"),
            _worked("Bir ilişki hem simetrik hem ters-simetrik olabilir.", "Yalnız öz-ilmeklerden oluşan ilişki iki koşulu da taşıyabilir.", "Sınır örneği"),
        ],
        [
            "Bağıntıyı yönsüz bağlantı gibi okumak.",
            "Yansımalı değil ile yansımasızı özdeş saymak.",
            "Simetrik değil ile asimetriği özdeş saymak.",
            "Ters-simetriyi simetrinin karşıtı sanmak.",
            "Geçişlilikte yalnız farklı düğümlü yolları sınamak.",
            "Serilikte çıkan ok yerine gelen ok aramak.",
        ],
        _practice(
            [
                ("D={u,v}, R={(u,u),(v,v)} hangi özelliği taşır?", ["Yansımalı", "Yansımasız", "Asimetrik", "Seri değil"], "A", "Her düğümde öz-ilmek vardır; ilişki ayrıca simetrik, ters-simetrik, geçişli ve seridir.", "Temel"),
                ("Boş bağıntı boş olmayan alanda hangisini taşımaz?", ["Simetri", "Geçişlilik", "Yansımasızlık", "Serilik"], "D", "Hiçbir düğümün çıkış tanığı yoktur.", "Orta"),
                ("Simetri karşı örneği hangi biçimdedir?", ["(u,u) eksik", "(u,v) var, (v,u) yok", "u'nun çıkışı yok", "İki-adımlı yol"], "B", "Ters okun eksikliği simetriyi çürütür.", "Temel"),
                ("Asimetrik ilişki hangi özelliği zorunlu taşır?", ["Yansımalı", "Yansımasız", "Simetrik", "Seri"], "B", "Öz-ilmek kendi tersidir; asimetri onu yasaklar.", "Orta"),
                ("Ters-simetriyi ne çürütür?", ["Bir öz-ilmek", "Farklı u,v arasında iki yönün bulunması", "Tek yönlü ok", "Boş uzantı"], "B", "İki yön birlikteyken uçlar farklıysa koşul bozulur.", "Temel"),
                ("Geçişlilik karşı örneği hangisidir?", ["(u,v) var", "(u,v),(v,w) var ama (u,w) yok", "u'nun öz-ilmeği yok", "v'nin çıkışı yok"], "B", "İki adımlı yolun kısayolu eksiktir.", "Temel"),
                ("Serilik hangi FOL cümlesidir?", ["∀xR(x,x)", "∀x∃yR(x,y)", "∃y∀xR(x,y)", "∀x∀yR(x,y)"], "B", "Her kaynak için en az bir hedef gerekir.", "Orta"),
                ("Bir düğüme yalnız ok gelmesi neyi garanti eder?", ["O düğümün serilik tanığını", "O düğümden çıkış olduğunu", "Hiçbirini", "Yansımayı"], "C", "Serilik başlangıç rolündeki çıkışı sorar.", "Orta"),
                ("Bir ilişki hem simetrik hem ters-simetrik olabilir mi?", ["Asla", "Yalnız alan boşsa", "Evet, örneğin yalnız öz-ilmeklerde", "Yalnız seri değilse"], "C", "İki tanım farklı uçlu karşılıklı oklar olmadığında birlikte sağlanabilir.", "İleri"),
                ("Yansımalı değil ne demektir?", ["Mutlaka yansımasız", "En az bir eksik öz-ilmek", "Hiç ok yok", "Her öz-ilmek var"], "B", "Evrensel yansıma koşulunun tek başarısız üyesi yeterlidir; başka öz-ilmekler olabilir.", "Orta"),
                ("Geçişlilikte x,y,z farklı olmak zorunda mı?", ["Evet", "Yalnız x=z", "Hayır", "Yalnız seri ilişkide"], "C", "Tanım değişkenler arasında farklılık koşulu koymaz.", "Orta"),
                ("Özellik raporu neden karşı örnek taşır?", ["Grafiği süslemek", "Hayır kararını tanıma göre denetlenebilir kılmak", "Alanı büyütmek", "Yeni yüklem eklemek"], "B", "Karşı örnek evrensel koşulun tam nerede bozulduğunu gösterir.", "Temel"),
            ]
        ),
        {
            "prompt": "D={u,v,w}, R={(u,v),(v,u),(v,w)} bağıntısının tam özellik profilini çıkar.",
            "starter": "Öz-ilmek tablosu, ters-ok tablosu, iki-adımlı yollar ve çıkış listesi olmak üzere dört küçük denetim tablosu kur.",
            "checks": ["u,v,w'nin öz-ilmekleri kontrol edildi mi?", "Her okun tersi arandı mı?", "u→v→w yolu kaydedildi mi?", "w'nin çıkışı kontrol edildi mi?"],
            "solution": "Yansımalı değil (u karşı örnek), yansımasızdır; simetrik değil ((v,w)); asimetrik değil ((u,v) ve (v,u)); ters-simetrik değil ((u,v)); geçişli değil ((u,v,w)); seri değil (w).",
        },
        [
            _production_task(
                "Üç farklı ikili bağıntı tasarla ve her birinin yedi özellik profilini çıkar.",
                ["Alan açık", "Tuple listesi açık", "Her özellik ayrı tanımla sınanmış", "Her başarısızlık belirleyici karşı örnek taşıyor"],
                "Örneklerden biri boş bağıntı, biri yalnız öz-ilmekler, biri karışık yönlü ağ olabilir.",
                "Zorunlu profiller",
                ["Yansımalı ve simetrik", "Yansımasız ve asimetrik", "Simetrik değil ve asimetrik de değil"],
            ),
            _production_task(
                "Doğal dildeki bir bağıntı özelliğini FOL cümlesi ve model testiyle eşleştir.",
                ["Doğal dil iddiası açık", "FOL formülü doğru", "Uzantı testi formülle aynı rolleri kullanıyor", "Karşı örnek tuple doğru türde"],
                "Çözüm, gündelik ilişkinin gerçekte özelliği taşıdığını varsaymak yerine yalnız verilen modele karar verir.",
                "Özellikler",
                ["yansımalı", "simetrik", "ters-simetrik", "geçişli", "seri"],
            ),
        ],
        [
            "En az üç bağıntı için yedi maddelik, karşı örnekli özellik profili.",
            "Simetrik değil/asimetrik ve yansımalı değil/yansımasız ayrımlarını gösteren iki sınır model.",
            "Bir geçişlilik ve bir serilik hatasının tuple üzerinden onarımı.",
            "En az dört bağıntı özelliğinin doğal dil, FOL ve uzantı tanımını eşleyen tablo.",
        ],
        [
            "Yansımalı değil ile yansımasız arasındaki farkı tek modelle göster.",
            "Simetrik değil bir ilişki neden asimetrik olmak zorunda değildir?",
            "Geçişliliği bozan karşı örnek neden üç bileşen taşır?",
            "Serilik ile ortak hedef koşulu arasındaki niceleyici sırası farkı nedir?",
        ],
        "F38'de semantik olarak bildiğin genelleme ve tanık fikirlerini `∀E` ve `∃I` kanıt kurallarına dönüştüreceksin.",
        ["forallx-relation-properties", "forallx-truth-fol"],
        "Bu ders bir gündelik bağıntının gerçek dünyada hangi özelliği taşıdığını iddia etmez. Özellikler yalnız verilen alan ve uzantıya göre değerlendirilir.",
        ["Bağıntı Özellikleri"],
    )
    lesson["fol_signature"] = F37_SIGNATURE
    lesson["relation_fixtures"] = [
        {
            "id": "f37-complete",
            "model": {"label": "tam bağıntı", "domain": ["u", "v", "w"], "names": {"a": "u", "b": "v"}, "predicates": {"R": [[left, right] for left in ("u", "v", "w") for right in ("u", "v", "w")], "F": []}},
            "expected": {"reflexive": True, "irreflexive": False, "symmetric": True, "asymmetric": False, "antisymmetric": False, "transitive": True, "serial": True},
        },
        {
            "id": "f37-empty",
            "model": {"label": "boş bağıntı", "domain": ["u", "v", "w"], "names": {"a": "u", "b": "v"}, "predicates": {"R": [], "F": []}},
            "expected": {"reflexive": False, "irreflexive": True, "symmetric": True, "asymmetric": True, "antisymmetric": True, "transitive": True, "serial": False},
        },
        {
            "id": "f37-identity",
            "model": {"label": "yalnız öz-ilmekler", "domain": ["u", "v", "w"], "names": {"a": "u", "b": "v"}, "predicates": {"R": [["u", "u"], ["v", "v"], ["w", "w"]], "F": []}},
            "expected": {"reflexive": True, "irreflexive": False, "symmetric": True, "asymmetric": False, "antisymmetric": True, "transitive": True, "serial": True},
        },
        {
            "id": "f37-mixed",
            "model": {"label": "karışık ağ", "domain": ["u", "v", "w"], "names": {"a": "u", "b": "v"}, "predicates": {"R": [["u", "v"], ["v", "u"], ["v", "w"]], "F": []}},
            "expected": {"reflexive": False, "irreflexive": True, "symmetric": False, "asymmetric": False, "antisymmetric": False, "transitive": False, "serial": False},
        },
    ]
    return lesson


def _candidate_f38():
    lesson = _stage_f_lesson(
        "F38",
        "ders-38-tumel-acma-ve-varlik-genellemesi",
        "Tümeli Açma ve Varlık Genellemesi",
        "Semantikteki her-nesne ve en-az-bir-nesne fikirlerini `∀E` ile `∃I` kanıt adımlarına dönüştürür; yerine koyma örneğini yalnız harf değişimi değil, ayrıştırılmış formül yapısı üzerinden denetler.",
        "Kısıtsız niceleyici kuralları",
        42,
        ["ders-37-baginti-ozelliklerini-modellerde-okuma"],
        [
            "fol_proof.universal_elimination",
            "fol_proof.existential_introduction",
            "fol_proof.substitution_instance",
            "fol_proof.quantifier_propositional_mix",
            "fol_proof.direction_explain",
        ],
        [
            "Tümel bir cümleden belirli bir ad örneğini `∀E` ile çıkarmak.",
            "Bir ad örneğinden uygun varoluşsal cümleyi `∃I` ile kurmak.",
            "Bağlı değişkenin yalnız serbest oluşumlarını yakalamasız değiştirmek.",
            "Aynı adın yalnız seçili oluşumlarını genelleyen meşru `∃I` hedeflerini tanımak.",
            "Niceleyici adımlarını önerme mantığı kurallarıyla birleştirmek.",
        ],
        [
            ("Tümel eleme (∀E)", "`∀xA(x)`den, A'nın bir adla yakalamasız yerine koyma örneğini çıkaran kural."),
            ("Varoluşsal giriş (∃I)", "Bir A(c) örneğinden c'nin seçili oluşumlarını değişkene çeviren `∃xA(x)` sonucunu kuran kural."),
            ("Yerine koyma örneği", "Niceleyici gövdesindeki değişkenin serbest oluşumlarına aynı terimin yerleştirilmesiyle elde edilen formül."),
            ("Seçili genelleme", "Kaynak addaki bazı oluşumların hedef matrisinde değişkene çevrilmesi; hedef yine kaynakla gerçek bir yerine koyma ilişkisi taşır."),
            ("Kural yönü", "Bir çıkarım kuralının hangi biçimden hangi biçime geçmeye izin verdiği."),
        ],
        [
            _section(
                "Semantikten kanıt kuralına",
                "`∀xA(x)` her nesnede doğruysa seçilen adın gösterdiği nesnede de doğrudur; A(c) doğruysa en az bir A olan vardır. Bu iki güvenli geçiş sırasıyla `∀E` ve `∃I`dir.",
                "Niceleyicili bir öncülden somut bir ara satır çıkarırken veya somut satırı varoluşsal hedefe yükseltirken.",
                "∀xA(x) ⟹ A(c); A(c) ⟹ ∃xA(x)",
                "Kurallar semantik gerekçeye dayanır ama kanıtta yalnız formül ve atıf sözleşmesiyle uygulanır.",
                "Okları ters çevirme: A(c)den `∀xA(x)` veya `∃xA(x)`den A(c) bu dersin kuralları değildir.",
                [("∀xF(x) ⟹ F(a)", "Her nesne F ise Ada da F'dir."), ("G(b) ⟹ ∃xG(x)", "Bora bir G tanığıdır.")],
                ("Kuralı lisanslı yönde kullanmak.", "Niceleyici işaretini yalnız silmek veya eklemek.", "Kuralın yönü ve yerine koyma ilişkisi birlikte gerekir."),
            ),
            _section(
                "∀E ve tek biçimli yerine koyma",
                "Tümel gövdenin niceleyicinin bağladığı serbest x oluşumları aynı adla değiştirilir; içte yeniden bağlanan x oluşumları korunur.",
                "Bir tümel cümleden doğru örneği seçerken.",
                "∀xR(x,x) / R(a,a)",
                "Tek niceleyicinin iki oluşumu da bağladığı örnekte iki konum aynı adla doldurulur.",
                "`∀xR(x,x)`den R(a,b) çıkarma; bu iki farklı nesne seçer ve gövdenin örneği değildir.",
                [("∀x(F(x)→G(x))", "a için `(F(a)→G(a))` çıkar."), ("∀x∃yR(x,y)", "a için `∃yR(a,y)` çıkar; iç y bağlı kalır.")],
                ("AST'deki bağlı x oluşumlarını aynı terimle değiştirmek.", "Metindeki bütün x harflerini körlemesine değiştirmek.", "Bağlanma kapsamı harf görünümünden daha belirleyicidir."),
            ),
            _section(
                "∃I ve seçili oluşumlar",
                "Hedef matris, niceleyici değişkenine kaynak adı yerleştirildiğinde kaynak satırı vermelidir. Böylece R(a,a)den hem `∃xR(x,a)` hem `∃xR(a,x)` hem de `∃xR(x,x)` çıkabilir.",
                "Kaynakta aynı ad birden çok kez geçtiğinde neyin genellendiğini açık seçerken.",
                "R(a,a) ⟹ ∃xR(x,a) / ∃xR(a,x) / ∃xR(x,x)",
                "Hedef formül hangi oluşumların tanık tarafından doldurulduğunu açıkça kodlar.",
                "R(a,b)den `∃xR(x,x)` çıkarma; tek x hem a hem b olamaz.",
                [("R(a,a) ⟹ ∃xR(x,a)", "İlk oluşum genellenmiştir."), ("R(a,b) ⟹ ∃xR(x,b)", "a varoluş tanığıdır.")],
                ("Hedefi tekrar örnekleyip kaynağa dönüp dönmediğini sınamak.", "Her ad geçen yeri değişken yapmak zorunda sanmak.", "Seçili genelleme meşrudur; fakat hedef gerçek bir örnek ilişkisi taşımalıdır."),
            ),
            _section(
                "İç niceleyici ve yakalanmama",
                "Dış niceleyicinin değişkeni yerine ad koyarken iç niceleyicinin bağladığı değişkenler ve kapsam yapısı değişmez.",
                "İç içe niceleyici bulunan `∀E` veya `∃I` adımlarında.",
                "∀x(F(x)→∃yR(x,y)) ⟹ F(a)→∃yR(a,y)",
                "Adlar niceleyiciler tarafından bağlanmadığı için a iç y niceleyicisi altında serbest bir ad olarak kalır.",
                "İçteki y'yi de a yapmak veya niceleyiciyi düşürmek.",
                [("∀x∃xF(x)", "İç x dış x'i gölgeler; dış örnekleme iç gövdeyi değiştirmez."), ("∃x∀yR(x,y)", "R(a,y) matrisinde y hâlâ ∀ tarafından bağlıdır.")],
                ("Bağlanma ağacını korumak.", "Karakter bul-değiştir uygulamak.", "Yakalanmasız yerine koyma sözdizim ağacı işlemidir."),
            ),
            _section(
                "Önerme kurallarıyla zincir",
                "Niceleyiciyi açtıktan sonra elde edilen koşullu veya bağlaçlı cümlede Faz D kuralları uygulanır; sonuç sonra `∃I` ile yeniden niceleyicili olabilir.",
                "`∀x(F(x)→G(x)), F(a) ⊢ ∃xG(x)` türü karma kanıtlarda.",
                "∀E → →E → ∃I",
                "Her satır tek lisanslı dönüşüm yapar; iki kural tek etikette sıkıştırılmaz.",
                "Tümel öncülden doğrudan varoluşsal sonucu, aradaki örnek ve koşullu eleme olmadan yazmak.",
                [("∀x(F→G)", "Önce a örneği alınır."), ("G(a)", "Sonra a tanığıyla `∃xG(x)` kurulur.")],
                ("Ara satırları ve atıfları görünür tutmak.", "Birden çok kuralı tek satırda varsaymak.", "Denetlenebilir kanıt her geçişin gerekçesini ayırır."),
            ),
            _section(
                "Bu derste tazelik neden yok",
                "`∀E` mevcut tümel bilgiyi belirli örneğe indirir; `∃I` mevcut bir tanığı varoluşa yükseltir. Bu yönlerde seçilen adın yeni olması gerekmez.",
                "Yanlışlıkla F39'un özad koşullarını bu iki kurala taşımamak için.",
                "∀E/∃I: ad serbest; ∀I/∃E: özad koşulu var",
                "Kısıtların kural yönüne bağlı olması, ezberlenecek rastgele bir fark değildir.",
                "Her niceleyici kuralında taze ad istemek veya hiçbirinde istememek.",
                [("∀xF(x), F(a) / F(a) ∀E", "a öncülde zaten geçse de sorun yok."), ("F(a) / ∃xF(x) ∃I", "Tanık adı yeni olmak zorunda değildir.")],
                ("Kural başına koşul tablosu kullanmak.", "Niceleyici görünce tek genel tazelik sloganı uygulamak.", "F39'daki kurallar farklı semantik görevlere sahiptir."),
            ),
        ],
        [
            _worked("∀xF(x), öyleyse F(a).", "a'nın gönderimi alan üyesidir; tümel cümle o üyeyi de kapsar.", "∀E"),
            _worked("∀xR(x,x), öyleyse R(a,a).", "İki bağlı x oluşumu aynı adla örneklenir.", "Doğru örnek"),
            _worked("∀xR(x,x), öyleyse R(a,b).", "Gövde tek değişkenin aynı nesneye gönderildiği iki oluşumunu ister.", "Yerine koyma hatası", "bad"),
            _worked("∀x∃yR(x,y), öyleyse ∃yR(a,y).", "Dış x örneklenir; iç y bağlı kalır.", "İç kapsam"),
            _worked("F(a), öyleyse ∃xF(x).", "a varoluşsal tanıktır.", "∃I"),
            _worked("R(a,a), öyleyse ∃xR(x,a).", "Yalnız ilk oluşum genellenebilir.", "Seçili genelleme"),
            _worked("R(a,b), öyleyse ∃xR(x,x).", "Tek x iki farklı adı aynı anda geri üretemez.", "Örnek hatası", "bad"),
            _worked("∃xF(x), öyleyse F(a).", "Var olan F'nin a olduğu verilmemiştir; bu ∃E değildir.", "Yön hatası", "bad"),
            _worked("F(a), öyleyse ∀xF(x).", "Ada'dan bütün nesnelere genelleme lisanssızdır.", "Yön hatası", "bad"),
            _worked("∀x(F(x)→G(x)), F(a) ⊢ G(a)", "∀E ile koşullu örnek, sonra →E kullanılır.", "Karma zincir"),
            _worked("G(a) ⊢ ∃xG(x)", "Tanığın kim olduğu varoluş sonucunda saklanabilir.", "Tanık"),
            _worked("∀xF(x) ⊢ ∃xF(x)", "Boş olmayan alan semantiğinde bir ad örneği alınıp ∃I uygulanabilir.", "İki adım"),
        ],
        [
            "`∀E`yi niceleyici silme işlemi sanmak.",
            "`∃I` hedefinin kaynağa geri örneklenip örneklenmediğini denetlememek.",
            "İç niceleyicinin bağlı değişkenini de değiştirmek.",
            "R(a,b)den tek değişkenli R(x,x) matrisi üretmek.",
            "`∃xF(x)`den keyfî F(a) çıkarmak.",
            "Her niceleyici kuralına gereksiz tazelik şartı eklemek.",
        ],
        _practice([
            ("`∀xF(x)`den hangisi `∀E` ile çıkar?", ["F(a)", "∃xF(x)", "F(x)", "∀xG(x)"], "A", "a ile doğru örnek alınır.", "Temel"),
            ("`∀xR(x,x)`den hangisi çıkmaz?", ["R(a,a)", "R(b,b)", "R(a,b)", "R(c,c)"], "C", "İki x aynı adla doldurulmalıdır.", "Temel"),
            ("`R(a,a)`den hangisi `∃I` ile çıkar?", ["∃xR(x,a)", "∀xR(x,a)", "R(a,b)", "∃xR(x,b)"], "A", "İlk a oluşumu genellenir.", "Orta"),
            ("`R(a,b)` neden `∃xR(x,x)`i lisanslamaz?", ["x yasak", "Tek x iki farklı adı geri veremez", "R ikili", "a yeni değil"], "B", "Yerine koyma örneği şartı bozulur.", "Orta"),
            ("`∀x∃yR(x,y)`nin a örneği nedir?", ["∃yR(a,y)", "R(a,a)", "∀yR(a,y)", "∃xR(x,a)"], "A", "Yalnız dış x örneklenir.", "Orta"),
            ("`F(a)`den doğrudan hangisi çıkar?", ["∀xF(x)", "∃xF(x)", "F(b)", "¬F(a)"], "B", "a varoluş tanığıdır.", "Temel"),
            ("∀E için ad taze olmalı mı?", ["Her zaman", "Hayır", "Yalnız ikili yüklemde", "Yalnız a için"], "B", "Tazelik bu kural yönünde gerekmez.", "Temel"),
            ("∃I için ad taze olmalı mı?", ["Evet", "Hayır", "Yalnız sonuçta", "Yalnız öncülde"], "B", "Mevcut tanık adı kullanılabilir.", "Temel"),
            ("`∀x(F(x)→G(x))`den a örneği hangisi?", ["F(a)→G(a)", "F(x)→G(x)", "F(a)→G(b)", "∀xG(x)"], "A", "İki serbest x oluşumu aynı a ile değiştirilir.", "Orta"),
            ("Karma zincirin sırası hangisi?", ["∃I,∀E,→E", "∀E,→E,∃I", "→E,∀I,∃E", "∀I,=E,∃I"], "B", "Önce örnek, sonra önerme kuralı, sonra varoluş genellemesi.", "Orta"),
            ("Yakalanmasız yerine koyma neyi korur?", ["Yalnız harf sayısını", "Bağlanma kapsamını", "Satır numarasını", "Doğruluk tablosunu"], "B", "İç niceleyicilerin bağları değişmemelidir.", "İleri"),
            ("Bir ∃I hedefini nasıl denetlersin?", ["Niceleyiciyi sil", "Hedef matrisine tanık adı koyup kaynağı geri elde et", "Adı değiştir", "Model çiz"], "B", "Geri örnekleme yapısal denetimdir.", "İleri"),
        ]),
        {
            "prompt": "`∀x(F(x)→G(x)), F(a)` öncüllerinden `∃xG(x)` hedefini satır satır kur.",
            "starter": "Önce tümel koşullunun a örneğini yaz; sonra →E ve ∃I uygula.",
            "checks": ["∀E örneği doğru", "→E iki doğru satıra atıflı", "∃I hedefi kaynağa geri örnekleniyor"],
            "solution": "1 ∀x(F(x)→G(x)) PR; 2 F(a) PR; 3 F(a)→G(a) ∀E 1; 4 G(a) →E 3,2; 5 ∃xG(x) ∃I 4.",
        },
        [
            _production_task("Altı `∀E` ve altı `∃I` adımını örnek ilişkisiyle denetle.", ["Her kaynak/hedef ayrıştırılmış", "Seçili oluşumlar işaretli", "İç kapsam korunmuş", "Hatalar kural koduyla açıklanmış"], "En az iki hata aynı harfin farklı kapsamda kullanılmasını içersin.", "Denetlenecek çiftler", ["∀xR(x,x) / R(a,a)", "∀xR(x,x) / R(a,b)", "R(a,a) / ∃xR(x,a)", "R(a,b) / ∃xR(x,x)"]),
            _production_task("Bir `∀E → önerme kuralı → ∃I` kanıtı üret ve her adımın semantik gerekçesini yaz.", ["En az iki öncül", "En az bir koşullu", "Atıflar açık", "Sonuç varoluşsal"], "Kanıt denetleyicisi sıfır hata vermeli.", "Başlangıç şablonları", ["∀x(F(x)→G(x)), F(a)", "∀x(F(x)∧G(x))", "∀xR(x,a), F(b)"]),
        ],
        ["On iki yerine koyma çiftini doğru/yanlış gerekçesiyle sınıflandırır.", "En az iki seçili ∃I genellemesini geri örneklemeyle doğrular.", "İç niceleyiciyi koruyan üç ∀E adımı kurar.", "Önerme kurallarıyla birleşen eksiksiz bir kanıt üretir."],
        ["∀E neden varoluşsal eleme değildir?", "R(a,a)den kaç farklı meşru tek değişkenli varoluş sonucu kurulabilir?", "∃I hedefinin kaynakla ilişkisini nasıl mekanik olarak sınarsın?"],
        "F39'da ters yönlerdeki `∀I` ve `∃E` için özad tazeliği ve alt kanıt disiplini eklenecek.",
        ["forallx-fol-rules", "forallx-quantifier-proofs"],
        "Bu ders yalnız kısıtsız iki niceleyici kuralını açar. `F(a) ⊢ ∀xF(x)` ve `∃xF(x) ⊢ F(a)` özellikle geçersiz karşı biçimler olarak tutulur.",
        ["Niceleyici Kanıtları"],
    )
    lesson["fol_signature"] = FOL_PROOF_SIGNATURE
    lesson["proof_fixtures"] = [
        _proof_fixture("f38-universal-instance", "valid", ["∀x(F(x) → G(x))", "F(a)"], "∃xG(x)", [
            _proof_line("l1", "∀x(F(x) → G(x))", "PR"),
            _proof_line("l2", "F(a)", "PR"),
            _proof_line("l3", "(F(a) → G(a))", "∀E", [_cite("l1")]),
            _proof_line("l4", "G(a)", "→E", [_cite("l3"), _cite("l2")]),
            _proof_line("l5", "∃xG(x)", "∃I", [_cite("l4")]),
        ]),
        _proof_fixture("f38-selective-existential", "valid", ["R(a,a)"], "∃xR(x,a)", [
            _proof_line("l1", "R(a,a)", "PR"),
            _proof_line("l2", "∃xR(x,a)", "∃I", [_cite("l1")]),
        ]),
        _proof_fixture("f38-bad-universal-instance", "invalid", ["∀xR(x,x)"], "R(a,b)", [
            _proof_line("l1", "∀xR(x,x)", "PR"),
            _proof_line("l2", "R(a,b)", "∀E", [_cite("l1")]),
        ], ["rule.universal_elimination_substitution"]),
        _proof_fixture("f38-bad-existential-instance", "invalid", ["R(a,b)"], "∃xR(x,x)", [
            _proof_line("l1", "R(a,b)", "PR"),
            _proof_line("l2", "∃xR(x,x)", "∃I", [_cite("l1")]),
        ], ["rule.existential_introduction_substitution"]),
    ]
    return lesson


def _candidate_f39():
    lesson = _stage_f_lesson(
        "F39",
        "ders-39-ozad-disiplini-tumel-ve-varlik-elemesi",
        "Özad Disiplini: Tümel Giriş ve Varlık Elemesi",
        "`∀I`de keyfî nesne ile `∃E`de geçici tanığı birbirinden ayırır; adın hangi açık öncül, varsayım ve sonuçta geçmesinin kuralı bozduğunu bağımlılık ağacıyla denetler.",
        "Taze ad ve alt kanıt",
        48,
        ["ders-38-tumel-acma-ve-varlik-genellemesi"],
        ["fol_proof.universal_introduction", "fol_proof.existential_elimination", "fol_proof.eigenname_check", "fol_proof.dependency_trace", "fol_proof.subproof_discharge"],
        ["Keyfî bir ad örneğinden `∀I` ile güvenli genelleme yapmak.", "Varoluş tanığını kapalı alt kanıtta kullanıp `∃E` ile tanıktan bağımsız sonuç çıkarmak.", "Ad tazeliğini bütün kanıtta değil, ilgili açık bağımlılıklarda denetlemek.", "Tanık adının varoluşsal öncüle veya sonuca sızmasını teşhis etmek.", "Başarısız kanıt girişiminin geçersizlik kanıtı olmadığını açıklamak."],
        [("Taze özad", "İlgili kuralın yasakladığı açık bağımlılık ve sonuçlarda geçmeyen geçici ad."), ("Keyfî nesne", "Özel bir bilgiye bağlanmadan seçilen ve bu nedenle genellenebilen nesne."), ("Tanık varsayımı", "∃E alt kanıtında varoluşsal gövdenin taze ad örneği olarak geçici kabul edilen cümle."), ("Açık bağımlılık", "Bir satırın doğruluğu için hâlâ dayanılan, boşaltılmamış öncül veya varsayım."), ("Boşaltma", "Alt kanıt varsayımını sonuç satırının dışına çıkarırken bağımlılıktan kaldırma işlemi."), ("Özad sızıntısı", "Geçici adın sonuçta veya yasaklı dış bağımlılıkta kalması." )],
        [
            _section("∀I'nin semantik fikri", "A(c) yalnız c hakkında özel bir varsayıma dayanmadan gösterildiyse c keyfî nesneyi temsil edebilir ve `∀xA(x)` çıkarılır.", "Bir kanıtı tümel hedefle bitirirken.", "A(c) / ∀xA(x), c açık bağımlılıklarda yok", "Kural c'nin dünyadaki kimliğini bilmediğimiz için değil, kanıtın c'ye özgü bilgi kullanmaması nedeniyle güvenlidir.", "F(c) öncülünden ∀xF(x) çıkarmak; c öncülde geçer.", [("∀x(F→G),∀xF ⊢ ∀xG", "c yalnız tümel öncüllerin örneklenmesinde kullanılır."), ("F(c) ⊢ ∀xF(x)", "c'ye özgü öncül nedeniyle yasaktır.")], ("Kaynak satırın bağımlılıklarını izlemek.", "Ad yalnız sonuçta görünmüyor diye taze saymak.", "Tazelik sözcük taraması değil bağımlılık koşuludur.")),
            _section("∀I için ad seçimi", "Kanıtın başında bir ad seçmek tek başına yeterli değildir; o ad sonradan açık bir varsayımda kullanılırsa genelleme engellenir.", "Genellemeden hemen önce özad denetimi yaparken.", "blocked(c)=adlar(açık bağımlılıklar)", "Kapanmış alt kanıt varsayımları doğru biçimde boşaltılmışsa artık engel değildir.", "Kanıtta herhangi bir yerde görünmüş adı sonsuza dek yasak saymak.", [("c yalnız ara örneklerde", "Tümel öncüllerden geliyorsa genellenebilir."), ("c açık AS satırında", "O varsayım boşaltılmadan genellenemez.")], ("Satırın gerçek bağımlılık kümesini kullanmak.", "Tüm geçmiş satırların metnini taramak.", "Kullanılmamış veya boşaltılmış satırlar genellemeyi gereksizce engellememelidir.")),
            _section("∃E'nin alt kanıtı", "`∃xA(x)`den doğrudan A(c) çıkarılmaz. Bunun yerine A(c) taze tanık varsayımıyla bir alt kanıt açılır; tanıktan bağımsız B elde edilip kapsam kapatılır.", "Varoluşsal öncüden tanığın kimliğine bağlı olmayan sonuç çıkarırken.", "∃xA(x), [A(c) ... B] / B", "Alt kanıt, hangi nesnenin A olduğunu bilmeden her olası tanığın aynı B'yi sağladığını temsil eder.", "A(c)yi kök satıra taşımak veya alt kanıtı kapatmadan B yazmak.", [("∃xF(x),∀x(F→G) ⊢ ∃xG(x)", "F(c) varsayımından G(c), sonra ∃xG(x)."), ("∃xF(x) ⊢ F(c)", "Tanığın c olduğu garanti edilmez.")], ("Tanık varsayımını kapsam içine hapsetmek.", "Varoluşsal cümleyi bir adlandırma cümlesi sanmak.", "∃ varlığı garanti eder, kimliği değil.")),
            _section("∃E tazelik üçlüsü", "Tanık adı varoluşsal öncülde, alt kanıt sonucunda veya alt kanıt dışındaki açık bağımlılıklarda geçemez.", "Bir ∃E uygulamasını kabul etmeden önce.", "c ∉ names(∃xA), names(B), names(dış bağımlılıklar)", "Üç yasak birlikte, sonucun geçici tanığın kimliğine dayanmadığını garanti eder.", "Yalnız sonuçta görünmemeyi kontrol edip dış öncüldeki c'yi kaçırmak.", [("Sonuç ∃xG(x)", "c görünmez; uygun olabilir."), ("Sonuç G(c)", "Tanık sızmıştır; yasak.")], ("Üç ayrı tazelik kutusunu işaretlemek.", "Tek 'ad yeni mi?' sorusuyla yetinmek.", "Aynı ad farklı yerlerde farklı bağımlılık riski yaratır.")),
            _section("Bağımlılık ağacı", "Her PR satırı bir öncüle, her AS satırı açtığı kapsama bağımlıdır. Atıflar bağımlılıkları birleştirir; →I, ¬I ve ∃E ilgili alt kanıt varsayımını boşaltır.", "Karma kanıtta adın gerçekten hangi varsayıma bağlı olduğunu bulurken.", "deps(sonuç)=⋃deps(atıflar)−boşaltılan kapsam", "Tazelik kontrolü bu yapılandırılmış kümeye uygulanır.", "Bir satırın yalnız hemen önceki satıra bağlı olduğunu varsaymak.", [("R ile tekrar", "Kaynağın bütün bağımlılıklarını taşır."), ("→I", "Alt kanıt başlangıç varsayımını sonuç bağımlılığından çıkarır.")], ("Atıflardan bağımlılık hesaplamak.", "Görsel yakınlığı bağımlılık sanmak.", "Fitch çizgileri kapsamı, atıflar ise gerçek gerekçeyi kodlar.")),
            _section("Kanıt bulunamaması ne göstermez", "Bir özad ihlali yalnız o kanıt girişimini bozar. Başka bir kanıt olabilir; geçersizlik için karşı model gerekir.", "Denetleyici hata verdiğinde epistemik sonucu doğru sınırlarken.", "invalid proof ≠ invalid argument", "F36 semantiği ile kanıt denetimi birbirini tamamlar ama aynı karar yöntemi değildir.", "Kırmızı kanıt satırından argüman geçersiz sonucuna atlamak.", [("Özad hatası", "Kanıtı onar veya başka strateji dene."), ("Karşı model", "Tüm öncüller doğru, sonuç yanlışsa geçersizlik gösterir.")], ("Biçim hatasını argüman statüsünden ayırmak.", "Denetleyiciyi karar verici sanmak.", "Eksik/yanlış türetim semantik karşı örnek değildir.")),
        ],
        [
            _worked("∀x(F(x)→G(x)), ∀xF(x) ⊢ ∀xG(x)", "c yalnız tümel öncüllerin örneklerinde kullanıldığı için ∀I güvenlidir.", "Geçerli ∀I"),
            _worked("F(c) ⊢ ∀xF(x)", "c açık öncülde geçtiği için keyfî değildir.", "Özad ihlali", "bad"),
            _worked("[F(c)] ... G(c), sonra ∀xG(x)", "F(c) varsayımı açıkken c'ye özgü bağımlılık sürer.", "Açık varsayım", "bad"),
            _worked("∃xF(x), [F(c) ... ∃xF(x)] ⊢ ∃xF(x)", "Sonuç c içermediği ve tanık tazeyse biçimsel olarak güvenlidir.", "Geçerli ∃E"),
            _worked("∃xF(x), [F(c) ... G(c)] ⊢ G(c)", "Geçici tanık sonuçta sızar.", "Sonuç sızıntısı", "bad"),
            _worked("∃xR(x,c), [R(c,c)...B]", "c varoluşsal öncülde zaten geçtiği için tanık olamaz.", "Kaynak sızıntısı", "bad"),
            _worked("K(c), ∃xF(x), [F(c)...B]", "B, K(c) dış öncülüne dayanıyorsa c taze değildir.", "Dış bağımlılık", "bad"),
            _worked("∃xF(x), ∀x(F(x)→G(x)) ⊢ ∃xG(x)", "F(c) alt kanıtında G(c), sonra tanıktan bağımsız varoluş sonucu elde edilir.", "Geçerli ∃E"),
            _worked("∃xF(x) ⊢ F(a)", "a'nın tanık olduğu verilmez.", "Doğrudan örnekleme", "bad"),
            _worked("Kapanmış AS bağımlılığı ∀I'yi her zaman engeller.", "Yalnız kaynak satır hâlâ o kapsama bağımlıysa engeller.", "Yanlış genelleme", "bad"),
            _worked("Bir kanıtta c geçti, artık kullanılamaz.", "Tazelik bütün geçmiş metne değil ilgili bağımlılıklara göre ölçülür.", "Aşırı kısıt", "bad"),
            _worked("Kanıt denetleyicisi reddetti, argüman geçersiz.", "Reddedilen yalnız bu türetimdir; karşı model gerekir.", "Epistemik sınır", "bad"),
        ],
        ["∀I'yi öncülde geçen adla uygulamak.", "∃E'yi doğrudan örnek seçme kuralı sanmak.", "Tanık adını sonuçta bırakmak.", "Tanık adının varoluşsal öncülde geçtiğini kaçırmak.", "Dış açık bağımlılıkları denetlememek.", "Kanıt hatasını geçersizlik göstergesi saymak."],
        _practice([
            ("∀I için c neyi temsil etmeli?", ["Ada'yı", "Keyfî nesneyi", "Tek tanığı", "Boş alanı"], "B", "c özel bilgiye bağlı olmamalıdır.", "Temel"),
            ("F(c) öncülünden ∀xF(x) neden çıkmaz?", ["F yasak", "c öncülde açık bağımlılık", "∀ yok", "Alan sonlu"], "B", "c keyfî değildir.", "Temel"),
            ("∃E alt kanıtı neyle başlar?", ["A(c) taze tanık varsayımı", "B sonucu", "¬A(c)", "∀xA(x)"], "A", "Varoluşsal matrisin taze ad örneği varsayılır.", "Temel"),
            ("Tanık adı nerede geçemez?", ["Yalnız satır numarasında", "Varoluşsal öncül, sonuç ve dış bağımlılıkta", "Alt kanıt varsayımında", "Kural etiketinde"], "B", "Üç tazelik bölgesi vardır.", "Orta"),
            ("∃xF(x)den doğrudan F(a) çıkar mı?", ["Evet", "Hayır", "Yalnız a tazeyse", "Yalnız iki nesnede"], "B", "Varoluş tanığın kimliğini vermez.", "Temel"),
            ("∃E sonucu G(c) olabilir mi?", ["Her zaman", "Tanık c ise", "Hayır, c sonuçta sızar", "Yalnız G tekli"], "C", "Sonuç tanık adından bağımsız olmalıdır.", "Orta"),
            ("Bağımlılık neyle taşınır?", ["Yalnız satır sırasıyla", "Atıflarla", "Fontla", "Model alanıyla"], "B", "Atıf yapılan satırların bağımlılıkları birleşir.", "Temel"),
            ("Alt kanıt varsayımı ne zaman boşaltılır?", ["Açılırken", "Uygun kuralla kapatıldığında", "Her R adımında", "Model çizilince"], "B", "Kapsam kullanan kural varsayımı bağımlılıktan çıkarır.", "Orta"),
            ("Kanıt hatası neyi gösterir?", ["Argüman kesin geçersiz", "Bu kanıt girişimi lisanssız", "Karşı model bulundu", "Öncüller yanlış"], "B", "Başka kanıt olabilir.", "Temel"),
            ("Geçersizliği ne gösterir?", ["Özad hatası", "Tek karşı model", "Uzun kanıt", "Taze ad"], "B", "Tüm öncülleri doğru, sonucu yanlış yapan model yeterlidir.", "Temel"),
            ("c yalnız kapanmış ve boşaltılmış varsayımda geçtiyse ∀I otomatik yasak mı?", ["Evet", "Hayır, kaynak bağımlılığına bakılır", "Yalnız c için", "Yalnız kimlikte"], "B", "Gerçek bağımlılık belirleyicidir.", "İleri"),
            ("∃E'de dış bağımlılık denetimi neden var?", ["Satırları azaltmak", "Sonucun tanığın kimliğine gizlice dayanmasını önlemek", "Adları alfabetik yapmak", "Modeli büyütmek"], "B", "Dış c bilgisi tanığı özel kılar.", "İleri"),
        ]),
        {"prompt": "`∃xF(x), ∀x(F(x)→G(x))` öncüllerinden `∃xG(x)` için taze c ile alt kanıt kur.", "starter": "F(c) varsayımı aç; tümel koşulu c için örnekle; G(c)den varoluş sonucu çıkar ve kapsamı kapat.", "checks": ["c öncüllerde yok", "c sonuçta yok", "Alt kanıt son satırı ∃xG(x)", "∃E kapsam kapandıktan sonra"], "solution": "1 ∃xF(x) PR; 2 ∀x(F(x)→G(x)) PR; 3 [F(c) AS; 4 F(c)→G(c) ∀E 2; 5 G(c) →E 4,3; 6 ∃xG(x) ∃I 5]; 7 ∃xG(x) ∃E 1,3-6."},
        [
            _production_task("Dört ∀I girişimini bağımlılık kümeleriyle denetle ve hatalı olanları onar.", ["PR/AS bağımlılıkları işaretli", "Boşaltılan kapsam çıkarılmış", "Genellenen ad belirlenmiş", "Hata kodu doğru"], "En az biri kullanılmayan eski c satırı içersin.", "Kanıt iskeletleri", ["F(c) / ∀xF(x)", "∀xF(x) / F(c) / ∀xF(x)", "[F(c)...G(c)] / ∀xG(x)"]),
            _production_task("İki geçerli ve üç hatalı ∃E kanıtı tasarla.", ["Tanık varsayımı doğru örnek", "Kapsam kapalı", "Sonuç tanıktan bağımsız", "Dış bağımlılıklar denetlenmiş"], "Üç hata sırasıyla kaynak, sonuç ve dış bağımlılık sızıntısı olsun.", "Zorunlu hata türleri", ["source name leak", "conclusion name leak", "external dependency leak"]),
        ],
        ["Geçerli bir ∀I kanıtında genellenen adın bağımlılık raporunu çıkarır.", "Üç ayrı ∃E özad ihlalini doğru hata koduyla ayırır.", "Kapsamı doğru kapanan karma ∃E kanıtı üretir.", "Kanıt hatası ile karşı modelin epistemik farkını açıklar."],
        ["∀I için adın bütün kanıtta hiç geçmemesi neden fazla güçlü bir koşuldur?", "∃E'nin üç tazelik bölgesi hangileridir?", "Bir alt kanıt varsayımı bağımlılıktan nasıl boşaltılır?"],
        "F40'ta bu özad disiplini kimlik yerine koyması ve daha uzun karma kanıtlarla birleştirilecek.",
        ["forallx-fol-rules", "forallx-quantifier-proofs"],
        "Özad denetimi ham metin aramasıyla değil ayrıştırılmış ad oluşumları ve satır bağımlılıklarıyla yapılır. Reddedilen kanıt argüman geçersizliği olarak etiketlenmez.",
        ["Özad ve Niceleyici Stratejisi"],
    )
    lesson["fol_signature"] = FOL_PROOF_SIGNATURE
    lesson["proof_fixtures"] = [
        _proof_fixture("f39-valid-universal", "valid", ["∀x(F(x) → G(x))", "∀xF(x)"], "∀xG(x)", [
            _proof_line("l1", "∀x(F(x) → G(x))", "PR"), _proof_line("l2", "∀xF(x)", "PR"),
            _proof_line("l3", "(F(c) → G(c))", "∀E", [_cite("l1")]), _proof_line("l4", "F(c)", "∀E", [_cite("l2")]),
            _proof_line("l5", "G(c)", "→E", [_cite("l3"), _cite("l4")]), _proof_line("l6", "∀xG(x)", "∀I", [_cite("l5")]),
        ]),
        _proof_fixture("f39-invalid-universal-name", "invalid", ["F(c)"], "∀xF(x)", [
            _proof_line("l1", "F(c)", "PR"), _proof_line("l2", "∀xF(x)", "∀I", [_cite("l1")]),
        ], ["rule.universal_introduction_name_not_fresh"]),
        _proof_fixture("f39-valid-existential", "valid", ["∃xF(x)", "∀x(F(x) → G(x))"], "∃xG(x)", [
            _proof_line("l1", "∃xF(x)", "PR"), _proof_line("l2", "∀x(F(x) → G(x))", "PR"),
            _proof_line("l3", "F(c)", "AS", depth=1, opens="w"), _proof_line("l4", "(F(c) → G(c))", "∀E", [_cite("l2")], depth=1),
            _proof_line("l5", "G(c)", "→E", [_cite("l4"), _cite("l3")], depth=1), _proof_line("l6", "∃xG(x)", "∃I", [_cite("l5")], depth=1),
            _proof_line("l7", "∃xG(x)", "∃E", [_cite("l1"), _cite_subproof("l3", "l6")], closes=["w"]),
        ]),
        _proof_fixture("f39-invalid-existential-leak", "invalid", ["∃xF(x)"], "F(c)", [
            _proof_line("l1", "∃xF(x)", "PR"), _proof_line("l2", "F(c)", "AS", depth=1, opens="w"),
            _proof_line("l3", "F(c)", "R", [_cite("l2")], depth=1), _proof_line("l4", "F(c)", "∃E", [_cite("l1"), _cite_subproof("l2", "l3")], closes=["w"]),
        ], ["rule.existential_elimination_name_not_fresh"]),
    ]
    return lesson


def _candidate_f40():
    lesson = _stage_f_lesson(
        "F40",
        "ders-40-kimlik-ve-karma-fol-kanitlari",
        "Kimlik ve Karma FOL Kanıtları",
        "Kimliğin özdeşlik ve seçili yerine koyma kurallarını niceleyici, bağlaç ve özad kurallarıyla birleştirir; uzun kanıtı hedeften geriye ve öncüllerden ileri iki yönlü planlar.",
        "Kimlik ve kanıt stratejisi",
        50,
        ["ders-39-ozad-disiplini-tumel-ve-varlik-elemesi"],
        ["fol_proof.identity_introduction", "fol_proof.identity_elimination", "fol_proof.selected_identity_substitution", "fol_proof.mixed_strategy", "fol_proof.audit_repair"],
        ["Atıfsız `=I` ile her ad için özdeşlik satırı kurmak.", "`=E` ile eş adların seçili serbest oluşumlarını iki yönde değiştirmek.", "Kimlik yerine koymasını bağıntı argüman sırası ve niceleyici kapsamıyla uyumlu uygulamak.", "Tümel/varoluşsal ve önerme kurallarını kimlikle birleştirmek.", "Hatalı uzun kanıtı ilk lisanssız satırdan başlayarak onarmak."],
        [("Kimlik giriş (=I)", "Her ad c için c=c sonucunu atıfsız veren kural."), ("Kimlik eleme (=E)", "a=b ve a içeren bir formülden seçili a oluşumlarını b ile değiştiren kural."), ("Seçili yerine koyma", "Eş adın bütün oluşumlarını değil, bir veya daha fazlasını değiştirmeye izin veren yapı koruyucu işlem."), ("Kimliğin simetrisi", "a=b ise b=a; =E iki yöndeki yerine koymayı lisanslayabilir."), ("İleri planlama", "Öncüllerin ana bağlaç/niceleyicilerinin açtığı satırları üretmek."), ("Geri planlama", "Hedefin son kuralını ve o kuralın gerektirdiği alt hedefleri belirlemek." )],
        [
            _section("=I: özdeşliğin başlangıç satırı", "`c=c` için öncül veya atıf gerekmez. Bu, c'nin hangi nesneye gönderildiğinden bağımsız olarak aynı nesnenin kendisiyle özdeş olmasına dayanır.", "Bir kanıtta refleksif kimlik gerektiğinde.", "— / c=c =I", "Kimlik işareti sıradan R yüklemi olmadığı için modelden ayrıca uzantı okunmaz.", "a=b'yi =I ile yazmak; iki farklı ad aynı nesneye gidebilir ama bu kanıtta verilmiş değildir.", [("a=a", "=I ile doğrudan."), ("a=b", "Yalnız =I ile çıkmaz.")], ("Yalnız aynı terimin iki yanını yazmak.", "Farklı adların olası ortak gönderimini varsaymak.", "Olasılık kanıt satırı değildir.")),
            _section("=E: eşleri yerine koymak", "a=b ve A(a) satırlarından A(b) elde edilebilir. Kaynak kimlik ile değiştirilecek formül ayrı atıflardır.", "Bir nesne hakkında bir adla verilen bilgiyi eş adına taşırken.", "a=b, A(a) / A(b)", "Eş adlar aynı gönderime sahip olduğundan yüklem üyeliği ve bağıntı rolü korunur.", "a=b ve F(a)dan G(b) çıkarmak; yüklem de değiştirilmiştir.", [("a=b, F(a) / F(b)", "Meşru."), ("a=b, R(a,c) / R(b,c)", "İlk argüman değiştirilir.")], ("Yalnız ad oluşumunu değiştirmek.", "Kimlik bahanesiyle yüklem, bağlaç veya başka adı değiştirmek.", "=E formül iskeletini korur.")),
            _section("Seçili oluşum ve yön", "R(a,a) gibi bir satırda tek veya iki a oluşumu b ile değiştirilebilir: R(b,a), R(a,b), R(b,b). Ayrıca a=b kimliği ters yönde de kullanılabilir.", "Aynı ad birden çok rolde geçtiğinde.", "a=b, R(a,a) / R(b,a) veya R(a,b) veya R(b,b)", "Her hedef, kaynakta en az bir eş ad oluşumunu değiştirir; diğer yapı aynıdır.", "Aynı adın sıfır oluşumunu değiştirip =E etiketi kullanmak veya c'yi d yapmak.", [("R(a,a)→R(b,a)", "İlk oluşum seçildi."), ("R(a,c)→R(b,d)", "c→d kimlikle lisanslı değil.")], ("Değişen terim konumlarını tek tek işaretlemek.", "Bütün formülü eşdeğer sanmak.", "Kimlik yerine koyması yerel ve izlenebilir olmalıdır.")),
            _section("Kimlik ve niceleyici kapsam", "Kimlik satırı bir niceleyicinin gövdesindeki ad oluşumunu değiştirebilir; bağlı değişkenler ve niceleyici kapsamı korunur.", "`a=b, ∀xR(x,a) ⊢ ∀xR(x,b)` gibi adımlarda.", "a=b, ∀xR(x,a) / ∀xR(x,b)", "Değiştirilen a addır; bağlı x oluşumları etkilenmez.", "x değişkenini a=b üzerinden değiştirmek veya niceleyici harfini yeniden adlandırmayı =E saymak.", [("∃xR(a,x)→∃xR(b,x)", "Serbest ad oluşumu değişir."), ("∀xR(x,a)→∀xR(b,a)", "Bağlı x, a=b ile b yapılamaz.")], ("Ad ve bağlı değişken türünü ayırmak.", "Aynı küçük harf görünümünden hareket etmek.", "İmza adlarla değişkenleri ayrık tutar.")),
            _section("İleri ve geri planı buluşturmak", "Öncüllerden ∀E/=E ile kullanılabilir örnekler üret; hedeften son kuralı belirle. İki cephe ortak bir ara formülde buluşur.", "Beşten uzun karma kanıtlarda.", "ileri: aç/taşı; geri: hedefin ana işareti", "Varoluşsal hedef çoğu kez son `∃I`; tümel hedef çoğu kez son `∀I`; koşullu hedef çoğu kez `→I` ister.", "Rastgele bütün öncülleri açmak veya hedef biçimini görmeden satır üretmek.", [("Hedef ∃xG(x)", "Bir G(c) ara satırı ara."), ("Hedef ∀x(c=x→F(x))", "Keyfî ad ve →I alt kanıtı planla.")], ("Son kural ve ara hedef yazmak.", "Yalnız ileri zincirle kör arama yapmak.", "Strateji arama alanını küçültür.")),
            _section("İlk hatada dur ve onar", "Uzun kanıtta sonraki satırlar ilk lisanssız satıra dayanabilir. Önce en erken hata düzeltilir, sonra bağımlı satırlar yeniden denetlenir.", "Denetleyici birden çok hata verdiğinde.", "ilk hata → onarım → yeniden denetim", "Hata kodları biçim, kapsam, atıf, yerine koyma ve tazelik sorunlarını ayırır.", "Son satırı hedefe benzetip ara hataları bırakmak.", [("=E substitution", "Yanlış ad/yüklem değişimini düzelt."), ("∀I name_not_fresh", "Keyfî ad seçimini veya bağımlılığı yeniden kur.")], ("Kök nedeni sırayla onarmak.", "Bütün kırmızı satırları bağımsız sanmak.", "Bağımlı kanıtta erken hata zincirleme etki yaratır.")),
        ],
        [
            _worked("a=a =I", "Aynı adın gönderimi kendisiyle özdeştir; atıf gerekmez.", "=I"),
            _worked("a=b =I", "Farklı adların özdeşliği öncülsüz kurulamaz.", "Yanlış =I", "bad"),
            _worked("a=b, F(a) ⊢ F(b)", "F yüklemi korunur, eş ad değiştirilir.", "=E"),
            _worked("a=b, R(a,a) ⊢ R(b,a)", "Seçili ilk oluşum değiştirilebilir.", "Seçili =E"),
            _worked("a=b, R(a,a) ⊢ R(b,b)", "İki a oluşumu da b ile değiştirilebilir.", "Tam =E"),
            _worked("a=b, R(a,c) ⊢ R(b,d)", "c→d değişimi kimlikçe lisanslı değildir.", "Fazla değişim", "bad"),
            _worked("a=b, F(b) ⊢ F(a)", "Kimlik iki yönde yerine koymaya izin verir.", "Ters yön"),
            _worked("a=b, ∀xR(x,a) ⊢ ∀xR(x,b)", "Yalnız serbest ad oluşumu değişir.", "Kapsam korunur"),
            _worked("a=b, ∀xR(x,a) ⊢ ∀xR(b,a)", "Bağlı x oluşumunu adla değiştirmek =E değildir.", "Bağlanma hatası", "bad"),
            _worked("a=b,F(a),∀x(F(x)→G(x)) ⊢ ∃xG(x)", "=E, ∀E, →E ve ∃I sıralı kullanılabilir.", "Karma kanıt"),
            _worked("F(a) ⊢ ∀x(x=a→F(x))", "Keyfî c için c=a varsayımından =E ile F(c), sonra →I ve ∀I.", "Kimlikli tümel"),
            _worked("Denetleyici =E hatası verdi, argüman geçersiz.", "Yalnız türetim hatalıdır; semantik karar için karşı model gerekir.", "Sınır", "bad"),
        ],
        ["=I ile farklı adların özdeşliğini varsaymak.", "=E sırasında yüklemi veya ilişkisiz adı değiştirmek.", "Seçili oluşum yerine bütün satırı yeniden yazmak.", "Bağlı değişkeni kimlik üzerinden adla değiştirmek.", "Kimlikten sonra özad kısıtlarını unutmak.", "Uzun kanıtta ilk hata yerine yalnız son satırı düzeltmek."],
        _practice([
            ("=I hangisini lisanslar?", ["a=a", "a=b", "F(a)", "∀xF(x)"], "A", "Özdeşlik refleksif biçimidir.", "Temel"),
            ("a=b,F(a)den ne çıkar?", ["G(b)", "F(b)", "a=a yalnız", "∀xF(x)"], "B", "Eş ad aynı yüklem konumuna taşınır.", "Temel"),
            ("a=b,R(a,a)den hangisi çıkar?", ["R(b,a)", "R(c,a)", "G(b)", "R(a,c)"], "A", "İlk a seçilerek b yapılır.", "Orta"),
            ("a=b,R(a,c)den R(b,d) neden çıkmaz?", ["R ikili", "c→d lisanssız", "b taze", "a=b yanlış"], "B", "Kimlik yalnız a/b değişimini lisanslar.", "Temel"),
            ("=E yönü hangisidir?", ["Yalnız a→b", "Yalnız b→a", "Kimliğin iki yönü", "Hiçbiri"], "C", "Eşlik simetriktir.", "Temel"),
            ("∀xR(x,a)de a=b ile ne değişebilir?", ["Bağlı x", "Serbest a", "∀ işareti", "R yüklemi"], "B", "a addır; x niceleyiciye bağlıdır.", "Orta"),
            ("Varoluşsal hedefte tipik son kural?", ["∃I", "∀E", "=I", "PR"], "A", "Bir tanık ara satırı genellenir.", "Temel"),
            ("Tümel hedefte tipik son kural?", ["∃E", "∀I", "=E", "∨I"], "B", "Keyfî örnek genellenir.", "Temel"),
            ("Koşullu hedefte tipik plan?", ["→I alt kanıtı", "∃I", "=I", "DS"], "A", "Ön bileşen varsayılıp art bileşen türetilir.", "Orta"),
            ("İlk hata yaklaşımı neden kullanılır?", ["Fontu düzeltmek", "Sonraki satırlar erken hataya bağımlı olabilir", "Modeli küçültmek", "Adları silmek"], "B", "Kök hata zincirleme sorun yaratır.", "Orta"),
            ("Kimlikli tümel kanıtta ∀I öncesi ne denetlenir?", ["Adın açık bağımlılıklarda geçmemesi", "Yalnız satır sayısı", "Model alanı", "Kaynak yılı"], "A", "Kimlik özad şartını kaldırmaz.", "İleri"),
            ("Hatalı =E kanıtı argüman hakkında ne gösterir?", ["Geçersizlik", "Yalnız bu adımın lisanssızlığı", "Karşı model", "Öncül yanlışlığı"], "B", "Semantik statü ayrı sınanır.", "İleri"),
        ]),
        {"prompt": "`a=b, F(a), ∀x(F(x)→G(x))` öncüllerinden `∃xG(x)` hedefini kur.", "starter": "Önce F(a)yı eş ad b'ye taşı; tümel koşulu b için aç; G(b)yi varoluşa yükselt.", "checks": ["=E yalnız adı değiştirdi", "∀E b örneği doğru", "→E atıfları doğru", "∃I hedefi geri örnekleniyor"], "solution": "1 a=b PR; 2 F(a) PR; 3 ∀x(F(x)→G(x)) PR; 4 F(b) =E 1,2; 5 F(b)→G(b) ∀E 3; 6 G(b) →E 5,4; 7 ∃xG(x) ∃I 6."},
        [
            _production_task("Sekiz =E adayını seçili oluşum tablosuyla denetle.", ["Kimlik yönü yazılı", "Değişen konumlar işaretli", "Formül iskeleti korunmuş", "En az bir değişim var"], "İkisi niceleyici kapsamı, ikisi ikili bağıntı içersin.", "Kimlik çiftleri", ["a=b / R(a,a)", "a=b / ∀xR(x,a)", "a=b / ∃xR(a,x)", "a=b / F(c)"]),
            _production_task("En az sekiz satırlı kimlik ve niceleyici kanıtı üret, sonra kasıtlı üç hata ekleyip onar.", ["=E", "En az iki niceleyici kuralı", "Bir alt kanıt", "Hata kodlarına göre onarım"], "Hatalar yerine koyma, kapsam ve özad türlerinden olsun.", "Hedef seçenekleri", ["∀x(x=a→F(x))", "∃xG(x)", "∀x∃yR(x,y)"]),
        ],
        ["=I ve =E'yi doğru atıf sayısıyla uygular.", "Seçili kimlik değiştirmesini en az altı yapısal örnekte denetler.", "Kimlik, niceleyici ve önerme kurallı eksiksiz kanıt üretir.", "Uzun kanıtta ilk lisanssız satırı bulup bağımlı zinciri onarır."],
        ["=E neden bütün eşdeğer formüller arasında serbest geçiş değildir?", "Bağlı değişken ile ad oluşumunu nasıl ayırırsın?", "Hedefin ana işareti son kuralı nasıl önerir?"],
        "F41'de çeviri, model araması ve kanıt aynı argüman üzerinde bağımsız çalıştırılıp çapraz denetlenecek.",
        ["forallx-identity-rules", "forallx-quantifier-proofs"],
        "Kimlik yerine koyması yalnız ayrıştırılmış serbest ad oluşumlarında çalışır. Kimlik kuralları özad kısıtlarını veya kapsam disiplinini askıya almaz.",
        ["Kimlik Kanıtları"],
    )
    lesson["fol_signature"] = FOL_PROOF_SIGNATURE
    lesson["proof_fixtures"] = [
        _proof_fixture("f40-identity-introduction", "valid", [], "a=a", [_proof_line("l1", "a=a", "=I")]),
        _proof_fixture("f40-selected-substitution", "valid", ["a=b", "R(a,a)"], "R(b,a)", [
            _proof_line("l1", "a=b", "PR"), _proof_line("l2", "R(a,a)", "PR"), _proof_line("l3", "R(b,a)", "=E", [_cite("l1"), _cite("l2")]),
        ]),
        _proof_fixture("f40-mixed", "valid", ["a=b", "F(a)", "∀x(F(x) → G(x))"], "∃xG(x)", [
            _proof_line("l1", "a=b", "PR"), _proof_line("l2", "F(a)", "PR"), _proof_line("l3", "∀x(F(x) → G(x))", "PR"),
            _proof_line("l4", "F(b)", "=E", [_cite("l1"), _cite("l2")]), _proof_line("l5", "(F(b) → G(b))", "∀E", [_cite("l3")]),
            _proof_line("l6", "G(b)", "→E", [_cite("l5"), _cite("l4")]), _proof_line("l7", "∃xG(x)", "∃I", [_cite("l6")]),
        ]),
        _proof_fixture("f40-bad-substitution", "invalid", ["a=b", "R(a,c)"], "R(b,d)", [
            _proof_line("l1", "a=b", "PR"), _proof_line("l2", "R(a,c)", "PR"), _proof_line("l3", "R(b,d)", "=E", [_cite("l1"), _cite("l2")]),
        ], ["rule.identity_elimination_substitution"]),
    ]
    return lesson


F41_VALID_ARGUMENT = {
    "premises": [
        "∀x(F(x) → ∃y(K(y) ∧ R(x,y)))",
        "F(a)",
        "a=b",
    ],
    "conclusion": "∃y(K(y) ∧ R(b,y))",
}


F41_INVALID_ARGUMENT = {
    "premises": [
        "∀x(F(x) → ∃y(K(y) ∧ R(x,y)))",
        "F(a)",
        "a=b",
    ],
    "conclusion": "∃y(K(y) ∧ ∀x(F(x) → R(x,y)))",
}


def _f41_translation_tasks(argument):
    tasks = [
        {
            "id": f"p{index + 1}",
            "label": f"{index + 1}. öncül",
            "role": "premise",
            "position": index,
            "candidate": formula,
            "accepted_sources": [formula],
        }
        for index, formula in enumerate(argument["premises"])
    ]
    tasks.append(
        {
            "id": "c",
            "label": "Sonuç",
            "role": "conclusion",
            "candidate": argument["conclusion"],
            "accepted_sources": [argument["conclusion"]],
        }
    )
    return tasks


def _candidate_f41():
    lesson = _stage_f_lesson(
        "F41",
        "ders-41-ceviri-model-kanit-asama-projesi",
        "Çeviri, Model ve Kanıt Aşama Projesi",
        "Aynı doğal dil argümanını sembolleştirme, sonlu model ve Fitch kanıtı kanallarında bağımsız denetler; karşı model ile doğrulanmış kanıt çatışmasını gizlemek yerine yayın engeli olarak raporlar.",
        "Üç kanallı mantık denetimi",
        65,
        ["ders-40-kimlik-ve-karma-fol-kanitlari"],
        [
            "fol_capstone.argument_freeze",
            "fol_capstone.translation_audit",
            "fol_capstone.model_audit",
            "fol_capstone.proof_audit",
            "fol_capstone.conflict_reconciliation",
            "fol_capstone.formalization_limits",
        ],
        [
            "Doğal dil argümanı ile FOL anahtarını denetim boyunca sabit tutmak.",
            "Her öncül ve sonucu kabul edilen çeviri yapısıyla ayrı karşılaştırmak.",
            "Aynı formülleri en az iki yorumda doğruluk iziyle değerlendirmek.",
            "Karşı model aramasının olumlu ve olumsuz sonuçlarını epistemik olarak ayırmak.",
            "Kanıtın gerçekten aynı öncül ve hedefi kullandığını denetlemek.",
            "Çeviri, semantik ve kanıt sonuçlarını tek etikete ezmeden uzlaştırmak.",
        ],
        [
            ("Argüman dondurma", "Üç denetim kanalının aynı öncül ve sonuç formüllerini kullanmasını sağlayan sözleşme."),
            ("Bağımsız kanal", "Başka kanalın sonucunu varsaymadan kendi motoru ve hata diliyle çalışan denetim."),
            ("Çeviri anahtarı", "Doğal dil yapısını koruduğu önceden onaylanmış bir veya daha fazla FOL cümlesi."),
            ("Model raporu", "Her yorumda öncül ve sonucun değeriyle tanık/karşı örnek izlerini birlikte gösteren kayıt."),
            ("Kanıt doğrulaması", "Satır, kapsam, atıf, yerine koyma ve özad denetimlerinden hatasız geçen türetim."),
            ("Güvenirlik çatışması", "Aynı argüman için doğrulanmış kanıt ile gerçek karşı modelin birlikte raporlanması."),
            ("Belirsiz sonuç", "Örneklemde karşı model bulunmamasına rağmen kanıt da verilmediğinde korunması gereken durum."),
        ],
        [
            _section(
                "Önce argümanı dondur",
                "Doğal dildeki üç öncül ve sonuç için alan, adlar, yüklemler ve ariteler bir kez yazılır. Çeviri, model ve kanıt kanalları bundan sonra aynı ayrıştırılmış formülleri kullanır.",
                "Bir projenin farklı araçlarında farkında olmadan başka argümanlar sınanmasını önlemek için.",
                "A = ⟨Γ, C, imza⟩",
                "Aynı görünen metinler bile niceleyici sırası veya bağıntı argüman yönü değişince başka argüman olabilir.",
                "Kanıtta sonucu kolaylaştırmak için ∀x∃y sırasını ∃y∀x yapmak.",
                [("Her araştırmacı bir koordinatöre danıştı", "∀x(F(x)→∃y(K(y)∧R(x,y)))"), ("Bir koordinatör bütün araştırmacılara danışıldı", "∃y(K(y)∧∀x(F(x)→R(x,y)))")],
                ("Her kanala aynı formül kimliğini vermek.", "Metni kanala göre yeniden sembolleştirmek.", "Çapraz denetim ancak nesnesi aynıysa anlamlıdır."),
            ),
            _section(
                "Çeviri kanalı",
                "Her cümle doğal dil rolü, kabul edilen yapılar ve öğrencinin adayıyla değerlendirilir. Hata, doğruluk değerinden önce niceleyici, kapsam, yön veya kimlik yapısında aranır.",
                "Model kurmadan önce yanlış formülün kusursuz değerlendirilmesini engellemek için.",
                "doğal dil → kabul edilen yapı ↔ aday",
                "Çeviri denetimi genel mantıksal eşdeğerlik değil, istenen dil yapısının korunmasıdır.",
                "Bir modelde aynı değeri aldı diye yanlış niceleyici sırasını kabul etmek.",
                [("Ada araştırmacıdır", "F(a)"), ("Ada ile Bora aynı kişidir", "a=b")],
                ("Her öncül ve sonucu ayrı raporlamak.", "Bütün argümana tek doğru/yanlış etiketi vermek.", "Yerel çeviri hatası hangi formülün düzeltilmesi gerektiğini gösterir."),
            ),
            _section(
                "Model kanalı",
                "Aynı kanonik formüller açık alan ve uzantılarda değerlendirilir. Her niceleyicinin tanığı veya karşı örneği izde görünür; tüm öncülleri doğru, sonucu yanlış yapan yorum karşı modeldir.",
                "Argümanın geçersizliğini göstermek veya formüllerin semantik davranışını sınamak için.",
                "M ⊨ Γ ve M ⊭ C ⇒ karşı model",
                "Tek karşı model geçersizliği kanıtlar; sınırlı bankada karşı model bulamamak geçerliliği kanıtlamaz.",
                "İki başarılı örneği bütün yorumların kanıtı saymak.",
                [("Ortak koordinatör modeli", "Geçerli proje argümanında bütün öncül ve sonuç doğru."), ("Farklı koordinatörler modeli", "∀x∃y doğruyken ∃y∀x yanlış olabilir.")],
                ("Model bankasının sınırını sonuçta yazmak.", "Arama başarısızlığını 'geçerli' diye sunmak.", "Sonlu örneklem evrensel semantik nicelemenin yerini tutmaz."),
            ),
            _section(
                "Kanıt kanalı",
                "Kanıt önce öncül ve hedef kümesinin dondurulmuş argümanla eşleşmesi bakımından, sonra Fitch kuralları bakımından denetlenir.",
                "Geçerliliği doğal türetim yoluyla göstermek ve her geçişi yeniden oynatmak için.",
                "aynı Γ, aynı C; sonra satır/kapsam/kural denetimi",
                "Başka hedefe ait kusursuz bir kanıt bu projenin argümanını kanıtlamaz.",
                "Kanıt öncüllerine gizlice yardımcı bir cümle eklemek.",
                [("a=b ile danışma bilgisini a'dan b'ye taşı", "=E yalnız ad oluşumunu değiştirir."), ("∀E sonra →E", "Tümel kural ile önerme kuralı ayrı satırlarda kalır.")],
                ("Argüman eşleşmesini kural denetiminden önce yapmak.", "Son satır hedefe benziyor diye kabul etmek.", "Doğru kanıt yalnız doğru sonuca değil doğru öncüllere de bağlıdır."),
            ),
            _section(
                "Sonuçları uzlaştır",
                "Üç kanal tek bir puanda eritilmez. Çeviri revizyonu, bulunan karşı model, doğrulanmış kanıt, eksik kanıt ve motor çatışması ayrı durumlar olarak korunur.",
                "Öğrenciye ne bildiğimizi ve sıradaki işlemi açık söylemek için.",
                "blocked > countermodel > translation revision > verified proof > undetermined",
                "Doğrulanmış kanıt ve karşı model birlikteyse pedagojik sonuç değil, veri veya motor hatası vardır; yayın durur.",
                "Çatışmada güçlü görünen kanalı seçip diğerini saklamak.",
                [("Kanıt var, karşı model yok", "Kanıt doğrulandı; örneklem ayrıca raporlanır."), ("Kanıt yok, karşı model yok", "Durum belirsiz kalır.")],
                ("Her kanalın ham raporunu saklamak.", "Tek yeşil/kırmızı durum göstermek.", "İzlenebilirlik hatanın hangi temsil düzeyinde olduğunu korur."),
            ),
            _section(
                "Biçimselleştirme kayıp raporu",
                "Proje, başarılı biçimselleştirmenin dahi doğal dildeki zaman, kiplik, bağlam, ima veya söylem etkilerini dışarıda bırakabileceğini açıkça kaydeder.",
                "Formel başarının doğal dilin eksiksiz açıklaması sanılmasını önlemek için.",
                "formel başarı ≠ anlamsal tüketme",
                "FOL argümanın seçilmiş yapısını görünür kılar; bütün kullanım bağlamını temsil etmez.",
                "Kanıt bulunduğu için doğal dil yorumunun tek mümkün okuma olduğunu söylemek.",
                [("'Danıştı' geçmiş zaman", "Mevcut imza zamanı kodlamıyor."), ("'Bir koordinatör' bağlamsal belirginlik", "Varoluş niceleyicisi bunu tek başına taşımaz.")],
                ("En az iki kaybı somut cümleye bağlamak.", "Genel 'bağlam kaybolur' sloganıyla yetinmek.", "Kayıp raporu hangi ayrımın dışarıda kaldığını göstermelidir."),
            ),
        ],
        [
            _worked("∀x(F(x)→∃y(K(y)∧R(x,y)))", "Her araştırmacının tanığı kendine göre değişebilir; niceleyici sırası korunur.", "Çeviri"),
            _worked("∃y(K(y)∧∀x(F(x)→R(x,y)))", "Tek bir ortak koordinatör ister; önceki cümleyle aynı değildir.", "Sıra farkı", "bad"),
            _worked("F(a), a=b ⊢ F(b)", "Kimlik bilgiyi eş ada taşır.", "Kimlik"),
            _worked("İki modelde sonuç doğru; demek argüman geçerli.", "Sonlu başarılı örneklem genel geçerlilik ispatı değildir.", "Aşırı sonuç", "bad"),
            _worked("Bir modelde bütün öncüller doğru, sonuç yanlış.", "Bu tek yorum karşı model olarak geçersizliği gösterir.", "Karşı model"),
            _worked("Kanıtın hedefi başka formül.", "Kurallar doğru olsa bile başka argüman denetlenmiştir.", "Argüman uyuşmazlığı", "bad"),
            _worked("Kanıt doğrulandı, örneklemde karşı model yok.", "Geçerlilik iddiasının dayanağı kanıttır; örneklem yalnız ek kontroldür.", "Kanıt"),
            _worked("Kanıt yok, örneklemde karşı model yok.", "Ne geçerlilik ne geçersizlik kurulmuştur; sonuç belirsizdir.", "Belirsiz"),
            _worked("Kanıt doğrulandı ve karşı model bulundu.", "Seslik beklentisi bozulmuştur; yayın engellenip veri/motor incelenir.", "Çatışma", "bad"),
            _worked("Bir çeviri hatalı ama kanıt doğru.", "Öğrencinin çeviri kanalı yine revizyon ister; kanıt sonucu hatayı silmez.", "Bağımsızlık", "bad"),
            _worked("'Danıştı' zaman bilgisini R ile kodlamak", "R yüklemi geçmiş zamanı ayrıca temsil etmiyorsa bu bilgi kayıp raporuna yazılır.", "Kayıp"),
            _worked("Tüm kanal raporlarını saklamak", "Düzeltme ve akademik inceleme hangi adımın değiştiğini yeniden kurabilir.", "İzlenebilirlik"),
        ],
        [
            "Model kurarken çeviri formülünü farkında olmadan değiştirmek.",
            "Aynı modelde eşit değer alan farklı çevirileri özdeş saymak.",
            "Karşı model bulunamadı sonucunu geçerlilik etiketi yapmak.",
            "Kanıta dondurulmuş argümanda olmayan ek öncül koymak.",
            "Hatalı kanıtı argümanın geçersizliği sanmak.",
            "Doğrulanmış kanıt ile karşı model çatışmasını sessizce bastırmak.",
            "Biçimselleştirmenin dışarıda bıraktığı doğal dil özelliklerini raporlamamak.",
        ],
        _practice([
            ("Üç kanalın aynı argümanı sınadığını ne garanti eder?", ["Aynı renk", "Dondurulmuş imza, öncüller ve sonuç", "Aynı model", "Aynı satır sayısı"], "B", "Formül kimliği kanallar arası sözleşmedir.", "Temel"),
            ("∀x∃y ile ∃y∀x arasındaki temel fark?", ["Yüklem", "Tanığın x'e göre değişebilmesi", "Ad sayısı", "Bağlaç"], "B", "İlk biçimde farklı x'lerin farklı tanıkları olabilir.", "Orta"),
            ("Tek karşı model ne gösterir?", ["Geçerlilik", "Geçersizlik", "Çeviri doğruluğu", "Kanıt eksikliği"], "B", "Bütün öncüller doğru ve sonuç yanlışsa argüman geçersizdir.", "Temel"),
            ("On modelde karşı model bulunmaması ne gösterir?", ["Kesin geçerlilik", "Yalnız bu örneklemde bulunmadığını", "Kesin yanlışlık", "Çeviri eşdeğerliği"], "B", "Sonlu arama genel sonucu kapatmaz.", "Temel"),
            ("Kanıt denetiminden önce ne eşleştirilir?", ["Font", "Öncül kümesi ve hedef", "Model etiketi", "Süre"], "B", "Başka argümanın kanıtı kabul edilmemelidir.", "Temel"),
            ("Kanıt hatası neyi tek başına göstermez?", ["Bu adım lisanssız", "Argüman geçersiz", "Atıf bozuk", "Kapsam hatası"], "B", "Başka bir kanıt bulunabilir.", "Orta"),
            ("Doğrulanmış kanıtla karşı model birlikteyse?", ["Kanıtı seç", "Modeli sil", "Yayın engeli ve inceleme", "Ortalama al"], "C", "Seslik çatışması gizlenemez.", "İleri"),
            ("Çeviri yanlış, kanıt doğruysa genel durum?", ["Tamamlandı", "Çeviri revizyonu", "Karşı model", "Model hatası"], "B", "Kanallar birbirini aklamaz.", "Orta"),
            ("Kanıt yok ve karşı model bulunmadıysa?", ["Geçerli", "Geçersiz", "Belirsiz", "Çelişik"], "C", "Her iki genel statü de kurulmamıştır.", "Temel"),
            ("Model izinde niceleyici için ne aranır?", ["Yalnız son değer", "Tanık veya karşı örnek", "Satır numarası", "Kaynak yılı"], "B", "İz semantik gerekçeyi görünür kılar.", "Orta"),
            ("a=b neden projede önemlidir?", ["İki adın aynı gönderimini kanıt kanalında taşıtır", "Alanı boşaltır", "R'yi simetrik yapar", "Niceleyiciyi siler"], "A", "=E eş adlar arasında seçili yerine koymayı lisanslar.", "İleri"),
            ("Kayıp raporunun amacı?", ["Kanıtı geçersiz kılmak", "FOL'un temsil etmediği doğal dil ayrımlarını belirtmek", "Modeli büyütmek", "Yeni öncül eklemek"], "B", "Formel başarı doğal dilin tamamını tüketmez.", "İleri"),
        ]),
        {
            "prompt": "Verilen üç öncül ve sonucu değiştirmeden çeviri, iki model ve Fitch kanıtı kanallarında denetle; sonra tek bir çapraz rapor yaz.",
            "starter": "Önce imza ile dört formülü dondur; her kanalın girdisini bu listeyle eşleştir.",
            "checks": ["Dört çeviri görevi kapsandı", "İki modelde bütün değerler izlendi", "Kanıt aynı Γ ve C'yi kullanıyor", "Örneklem sınırı yazıldı", "En az iki doğal dil kaybı belirtildi"],
            "solution": "Geçerli ana örnekte ∀E ile a örneği alınır, →E ile Ada'nın danıştığı koordinatörün varlığı çıkarılır, a=b üzerinden =E ile sonuç Bora adına taşınır. İki model raporu genel geçerlilik iddiası yapmaz; bunu doğrulanmış kanıt sağlar.",
        },
        [
            _production_task(
                "Ana geçerli argümanın üç kanal raporunu sıfırdan yeniden üret.",
                ["İmza ve ariteler açık", "Dört çeviri ayrı", "En az iki model izi", "Kanıtın her atfı görünür", "Çatışma alanı raporda var"],
                "Rapor sonucu tek rozet değil, üç bağımsız bölüm içermeli.",
                "Ana argüman",
                ["Her araştırmacı bir koordinatöre danıştı.", "Ada araştırmacıdır.", "Ada ile Bora aynı kişidir.", "Öyleyse Bora bir koordinatöre danıştı."],
            ),
            _production_task(
                "Tanıkların kişiye göre değiştiği karşı modeli kur ve ortak tanık sonucunu çürüt.",
                ["En az iki araştırmacı", "En az iki koordinatör", "Her araştırmacının bir danıştığı var", "Hiçbir koordinatör herkese ortak değil", "Öncül/sonuç değerleri açık"],
                "∀x∃y ile ∃y∀x farkı yorum verisinde görünmeli.",
                "Karşı model hedefi",
                ["∀x(F(x)→∃y(K(y)∧R(x,y)))", "F(a)", "a=b", "∃y(K(y)∧∀x(F(x)→R(x,y)))"],
            ),
        ],
        [
            "Dört doğal dil cümlesini aynı imzada yapısal olarak doğru sembolleştirir.",
            "En az iki modelde öncül ve sonuç izlerini eksiksiz yeniden üretir.",
            "Geçerli ana argümanın kimlikli Fitch kanıtını sıfır hata ile kurar.",
            "Geçersiz varyant için açık ve küçük karşı model verir.",
            "Çatışma ve belirsizlik durumlarını geçerlilikten doğru ayırır.",
            "Biçimselleştirmenin dışarıda bıraktığı en az iki ayrımı somutlaştırır.",
        ],
        [
            "Üç kanal neden tek bir doğru/yanlış puanına indirgenmemelidir?",
            "Sonlu model araması ile Fitch kanıtının epistemik rolleri nasıl ayrılır?",
            "Aynı argüman sözleşmesi hangi gizli değişiklikleri engeller?",
            "Formel başarının doğal dili tüketmediğini bu örnek üzerinde nasıl gösterirsin?",
        ],
        "G42'de bu teknik beceriler Frege'nin işlev-argüman çözümlemesi ve mantıksal biçim fikrine bağlanacak.",
        ["forallx-proofs-semantics", "forallx-semantic-concepts", "forallx-using-interpretations", "mit-fol-semantics"],
        "Çapraz denetleyici yeni bir karar yöntemi değildir. Çeviri, model ve kanıt motorlarının aynı argüman üzerindeki sonuçlarını ayrı tutar; kanıt/karşı model çatışmasını güvenilirlik arızası olarak engeller.",
        ["FOL Aşama Projesi"],
    )
    lesson["fol_signature"] = FOL_PROOF_SIGNATURE
    valid_models = [
        {
            "label": "Ortak koordinatör",
            "domain": ["ada", "deniz", "koor"],
            "names": {"a": "ada", "b": "ada", "c": "deniz", "d": "koor"},
            "predicates": {
                "F": ["ada", "deniz"],
                "G": [],
                "H": [],
                "K": ["koor"],
                "R": [["ada", "koor"], ["deniz", "koor"]],
            },
        },
        {
            "label": "Tek araştırmacı",
            "domain": ["ada", "koor"],
            "names": {"a": "ada", "b": "ada", "c": "koor", "d": "koor"},
            "predicates": {
                "F": ["ada"],
                "G": [],
                "H": [],
                "K": ["koor"],
                "R": [["ada", "koor"]],
            },
        },
    ]
    valid_proof = {
        "premises": F41_VALID_ARGUMENT["premises"],
        "target": F41_VALID_ARGUMENT["conclusion"],
        "lines": [
            _proof_line("l1", F41_VALID_ARGUMENT["premises"][0], "PR"),
            _proof_line("l2", "F(a)", "PR"),
            _proof_line("l3", "a=b", "PR"),
            _proof_line("l4", "F(a) → ∃y(K(y) ∧ R(a,y))", "∀E", [_cite("l1")]),
            _proof_line("l5", "∃y(K(y) ∧ R(a,y))", "→E", [_cite("l4"), _cite("l2")]),
            _proof_line("l6", "∃y(K(y) ∧ R(b,y))", "=E", [_cite("l3"), _cite("l5")]),
        ],
    }
    countermodel = {
        "label": "Farklı koordinatörler",
        "domain": ["ada", "deniz", "k1", "k2"],
        "names": {"a": "ada", "b": "ada", "c": "k1", "d": "k2"},
        "predicates": {
            "F": ["ada", "deniz"],
            "G": [],
            "H": [],
            "K": ["k1", "k2"],
            "R": [["ada", "k1"], ["deniz", "k2"]],
        },
    }
    lesson["capstone_fixtures"] = [
        {
            "id": "f41-valid-identity-argument",
            "signature": FOL_PROOF_SIGNATURE,
            "argument": F41_VALID_ARGUMENT,
            "translation_tasks": _f41_translation_tasks(F41_VALID_ARGUMENT),
            "models": valid_models,
            "proof": valid_proof,
            "expected_status": "proof_verified",
        },
        {
            "id": "f41-invalid-shared-witness",
            "signature": FOL_PROOF_SIGNATURE,
            "argument": F41_INVALID_ARGUMENT,
            "translation_tasks": _f41_translation_tasks(F41_INVALID_ARGUMENT),
            "models": [countermodel],
            "proof": None,
            "expected_status": "countermodel_found",
        },
    ]
    lesson["semantic_cross_checks"] = [
        {
            "fixture_id": fixture["id"],
            "expected_status": fixture["expected_status"],
        }
        for fixture in lesson["capstone_fixtures"]
    ]
    return lesson


STAGE_F_CANDIDATE_LESSONS = [
    _candidate_f35(),
    _candidate_f36(),
    _candidate_f37(),
    _candidate_f38(),
    _candidate_f39(),
    _candidate_f40(),
    _candidate_f41(),
]


STAGE_F_CANDIDATE_MAP = {
    lesson["slug"]: lesson
    for lesson in STAGE_F_CANDIDATE_LESSONS
}
