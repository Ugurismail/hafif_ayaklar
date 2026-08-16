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
        }
    )
    return lesson


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


STAGE_F_CANDIDATE_LESSONS = [
    _candidate_f35(),
    _candidate_f36(),
    _candidate_f37(),
]


STAGE_F_CANDIDATE_MAP = {
    lesson["slug"]: lesson
    for lesson in STAGE_F_CANDIDATE_LESSONS
}
