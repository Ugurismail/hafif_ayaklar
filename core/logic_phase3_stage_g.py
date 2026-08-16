"""Release-candidate philosophy bridge for the logic course.

Stage G connects the isolated formal curriculum to close reading in Frege,
Russell, and Wittgenstein. It never mutates the learner-facing 45-lesson
course. Reading fixtures keep source locations, required distinctions, and
interpretive limits machine-auditable without pretending to automate
philosophical interpretation.
"""

from .logic_phase3_stage_a import (
    _lesson,
    _practice,
    _production_task,
    _section,
    _worked,
)


STAGE_G_SOURCE_REFERENCES = {
    "sep-frege-logic": {
        "title": "Stanford Encyclopedia of Philosophy - Frege's Logic",
        "url": "https://plato.stanford.edu/archives/spr2024/entries/frege-logic/",
    },
    "sep-propositional-function": {
        "title": "Stanford Encyclopedia of Philosophy - Propositional Function",
        "url": "https://plato.stanford.edu/entries/propositional-function/",
    },
    "sep-frege": {
        "title": "Stanford Encyclopedia of Philosophy - Gottlob Frege",
        "url": "https://plato.stanford.edu/entries/frege/",
    },
    "sep-descriptions": {
        "title": "Stanford Encyclopedia of Philosophy - Descriptions",
        "url": "https://plato.stanford.edu/entries/descriptions/",
    },
    "sep-logical-atomism": {
        "title": "Stanford Encyclopedia of Philosophy - Logical Atomism",
        "url": "https://plato.stanford.edu/entries/logical-atomism/",
    },
    "sep-wittgenstein": {
        "title": "Stanford Encyclopedia of Philosophy - Ludwig Wittgenstein",
        "url": "https://plato.stanford.edu/archives/spr2022/entries/wittgenstein/",
    },
    "wittgenstein-tractatus": {
        "title": "Ludwig Wittgenstein Project - Tractatus Logico-Philosophicus",
        "url": "https://www.wittgensteinproject.org/w/index.php?title=Tractatus_Logico-Philosophicus_%28English%29",
    },
    "wittgenstein-investigations": {
        "title": "Ludwig Wittgenstein Project - Philosophische Untersuchungen",
        "url": "https://www.wittgensteinproject.org/w/index.php/Philosophische_Untersuchungen",
    },
    "sep-rule-following": {
        "title": "Stanford Encyclopedia of Philosophy - Rule-Following and Intentionality",
        "url": "https://plato.stanford.edu/entries/rule-following/",
    },
    "sep-private-language": {
        "title": "Stanford Encyclopedia of Philosophy - Private Language",
        "url": "https://plato.stanford.edu/entries/private-language/",
    },
    "oxford-logic-language": {
        "title": "Oxford Faculty of Philosophy - The Philosophy of Logic and Language",
        "url": "https://www.philosophy.ox.ac.uk/node/98441",
    },
}


def _reading_fixture(
    fixture_id,
    source_id,
    locator,
    focus,
    required_distinctions,
    prohibited_shortcuts,
    task,
    boundary,
):
    return {
        "id": fixture_id,
        "source_id": source_id,
        "locator": locator,
        "focus": focus,
        "required_distinctions": list(required_distinctions),
        "prohibited_shortcuts": list(prohibited_shortcuts),
        "task": task,
        "boundary": boundary,
    }


def _comparison_fixture(fixture_id, left, right, shared_problem, differences, task):
    return {
        "id": fixture_id,
        "left": left,
        "right": right,
        "shared_problem": shared_problem,
        "differences": list(differences),
        "task": task,
    }


def _stage_g_lesson(*args, **kwargs):
    lesson = _lesson(*args, **kwargs)
    lesson.update(
        {
            "reading_fixtures": [],
            "comparison_fixtures": [],
            "primary_text_locators": [],
        }
    )
    return lesson


def _candidate_g42():
    lesson = _stage_g_lesson(
        "G42",
        "ders-42-frege-fonksiyon-arguman-kavram-nesne",
        "Frege: Fonksiyon, Argüman, Kavram ve Nesne",
        "Geleneksel özne-yüklem görünüşünden Frege'nin fonksiyon-argüman çözümlemesine geçer; kavram ile nesneyi dilbilgisel biçime değil mantıksal role göre ayırır.",
        "Fregeci çözümleme",
        42,
        ["ders-41-ceviri-model-kanit-asama-projesi"],
        [
            "frege.function_argument_analysis",
            "frege.unsaturated_function_explain",
            "frege.concept_object_distinguish",
            "frege.quantifier_level_read",
            "frege.modern_notation_limit",
        ],
        [
            "Özne-yüklem çözümlemesi ile fonksiyon-argüman çözümlemesini aynı cümlede karşılaştırmak.",
            "Bir ifadeden argüman çıkarıldığında kalan doymamış yapıyı göstermek.",
            "Kavramı nesnelerin doğruluk değerine gittiği birinci düzey fonksiyon olarak açıklamak.",
            "Birinci düzey kavram ile kavramlar hakkında olan ikinci düzey işlemi ayırmak.",
            "Modern FOL gösteriminin Frege'yi anlamaya yardım ettiği ve etmediği noktaları raporlamak.",
        ],
        [
            ("Fonksiyon", "Bir veya daha fazla argümanla tamamlandığında değer veren doymamış mantıksal yapı."),
            ("Argüman", "Bir fonksiyonun boş yerini doldurarak belirli bir değer elde edilmesini sağlayan öğe."),
            ("Doymamışlık", "Fonksiyon ifadesinin tamamlanmak için açık bir argüman yeri taşıması."),
            ("Kavram", "Frege'de nesneleri doğruluk değerlerine götüren birinci düzey fonksiyon."),
            ("Nesne", "Doymuş olan ve birinci düzey fonksiyonun argümanı olabilen mantıksal kategori."),
            ("Değer", "Fonksiyonun belirli argüman veya argümanlarda ürettiği sonuç."),
            ("Birinci düzey", "Argümanları nesneler olan fonksiyon veya kavram düzeyi."),
            ("İkinci düzey", "Argümanları birinci düzey fonksiyonlar olan mantıksal düzey; niceleyici çözümlemesinde belirgindir."),
        ],
        [
            _section(
                "Özne-yüklem kalıbının sınırı",
                "Geleneksel dilbilgisi `Ada araştırmacıdır` cümlesini özne ve yükleme ayırır. Fregeci çözümleme ise aynı yapıyı `x araştırmacıdır` fonksiyonu ile Ada argümanının birleşmesi olarak okur.",
                "Cümlenin dilbilgisel yüzeyi mantıksal bağımlılıkları gizlediğinde.",
                "araştırmacı(Ada) → doğru/yanlış",
                "Aynı fonksiyon farklı nesnelerle tamamlandığında sistematik olarak farklı doğruluk değerleri verebilir.",
                "Fonksiyon/argüman ayrımını yalnız cümlede önce ve sonra gelen sözcüklerin sırasına bağlama.",
                [("Ada araştırmacıdır", "Argüman Ada; doymamış yapı `x araştırmacıdır`."), ("Bora, Ada'ya güvenir", "İki argüman yeri ve bu yerlerin ayrı rolleri vardır.")],
                ("Boş yerleri ve rollerini işaretlemek.", "Her cümleyi tek özne ve tek yükleme zorlamak.", "Bağıntılar birden çok argüman yeri taşır."),
            ),
            _section(
                "Doymamış fonksiyon, doymuş değer",
                "`2 + 3` ifadesinde sayıları değiştirince aynı işlemsel örüntü korunur. Benzer biçimde bir yüklem ifadesi argüman yeri açıkken doymamış, argümanla tamamlandığında doğruluk değeri veren bütün hâle gelir.",
                "Bir ifadede değişebilen yer ile sabit yapıyı ayırırken.",
                "ξ araştırmacıdır; ξ=ada ⇒ doğru",
                "Fonksiyon bir nesne veya ad değildir; tamamlanma biçimidir. Argüman eklenmeden belirli bir doğruluk değeri elde edilmez.",
                "Doymamışlığı psikolojik eksiklik veya tamamlanmamış yazım hatası sanma.",
                [("x zamanında geldi", "x yeri doldurulmayı bekleyen yapıyı görünür kılar."), ("Ada zamanında geldi", "Belirli argümanla doymuş cümledir.")],
                ("Fonksiyonu boş yeriyle göstermek.", "Fonksiyonu cümledeki başka bir nesne saymak.", "Fonksiyon ve nesne farklı mantıksal kategorilerdir."),
            ),
            _section(
                "Kavram ve nesne kategori ayrımı",
                "Frege için kavram, nesneleri doğru veya yanlışa götüren fonksiyondur; nesne ise bu fonksiyonun argümanı olabilir. Ayrım sırf isim ile sıfat arasındaki dilbilgisel ayrıma eşit değildir.",
                "`F(a)` biçiminin felsefi rolünü açıklarken veya kategori hatasını teşhis ederken.",
                "F: nesne → doğruluk değeri; a: nesne",
                "Kavramın uzantısındaki nesneler ile kavramın kendisi aynı tür öğe değildir.",
                "`Araştırmacı kavramı da bir araştırmacıdır` gibi kavramı kendi nesnelerinden biriymiş gibi kullanma.",
                [("Ada, araştırmacı kavramının altına düşer", "Ada nesne, araştırmacı bir kavramdır."), ("Araştırmacıların kümesi", "Modern uzantısal temsil yararlıdır ama Fregeci kavramın kendisiyle özdeş değildir.")],
                ("Nesnenin kavram altına düştüğünü söylemek.", "Nesnenin kavramın parçası olduğunu söylemek.", "Altına düşme, parça-bütün ilişkisi değildir."),
            ),
            _section(
                "Niceleme ve düzeyler",
                "`Her araştırmacı dikkatli` cümlesinde niceleyici tek bir nesne adı değildir; birinci düzey kavramlar arasındaki genel bağlantıyı kuran daha yüksek düzeyli yapıdır.",
                "Niceleyiciyi görünmez bir çoğul ad gibi okuma hatasını önlerken.",
                "∀x(Fx → Gx)",
                "x, tek tek nesne konumunu açar; niceleme bu konumdaki bütün olası argümanları sistematik olarak kapsar.",
                "`Her araştırmacı` ifadesini belirli bir topluluk nesnesinin adı sayma.",
                [("∃xFx", "En az bir nesnenin F kavramının altına düştüğünü söyler."), ("∀x(Fx→Gx)", "F altında olan her nesnenin G altında da olduğunu söyler.")],
                ("Niceleyicinin değişken alanı üzerindeki işini açıklamak.", "∀ işaretini bütün nesnelerin ortak adı saymak.", "Niceleyici adlandırmaz; genellik kurar."),
            ),
            _section(
                "Bağıntı ve çoklu argüman",
                "Fregeci işlevsel çözümleme, `Ada Bora'ya güvenir` gibi bağıntılarda iki boş yerin sırasını korur. Bir argümanı sabitlemek, geriye tek yerli yeni bir fonksiyon bırakabilir.",
                "Bağıntı rolünü, yönünü ve kısmi uygulamayı okurken.",
                "R(ξ,ζ); R(ada,ζ)",
                "İlk boş yer güvenen, ikinci boş yer güvenilen rolündedir; aynı iki nesneyi ters çevirmek farklı değere yol açabilir.",
                "İki argümanı sırasız bir çift veya aynı dilbilgisel görev sayma.",
                [("R(ada,bora)", "Ada güvenen, Bora güvenilendir."), ("R(bora,ada)", "Roller değiştiği için ayrı uygulamadır.")],
                ("Her boş yere rol etiketi koymak.", "İsimleri alfabetik sıraya sokmak.", "Mantıksal sıra cümlenin bağıntı yapısını taşır."),
            ),
            _section(
                "Modern FOL ile dikkatli köprü",
                "Modern `F(a)` ve `∀x` gösterimi Frege'nin devrimini görünür kılar; fakat onun özgün iki boyutlu yazısı, doğruluk değerleri ve kavram kuramının tamamı modern ders notasyonuna indirgenemez.",
                "Tarihsel metni daha önce öğrenilen biçimsel araçlarla ilişkilendirirken.",
                "yardımcı yeniden yazım ≠ tarihsel özdeşlik",
                "Aynı problemi daha sonra standartlaşmış bir gösterimle ifade etmek, iki kuramın bütün ontoloji ve anlam görüşlerini eşitlemez.",
                "Frege modern FOL sembollerini aynen kullanmış gibi alıntı veya tarih yazma.",
                [("Fregeci genellik → ∀x", "Pedagojik yeniden yazımdır."), ("Frege'nin kavramı = modern küme", "Uzantısal benzerliği ontolojik özdeşlik sayan aşırı sadeleştirmedir.")],
                ("Yeniden yazımın kazancını ve kaybını birlikte belirtmek.", "Modern notasyonu tarihsel özgün metin diye sunmak.", "Köprü, farkı silmeden anlaşılabilirlik sağlamalıdır."),
            ),
        ],
        [
            _worked("Ada araştırmacıdır → F(a)", "Ada argüman, F açık argüman yeri taşıyan kavramdır.", "Çözümleme"),
            _worked("Araştırmacı Ada'dır → a=F", "Kavram ile nesneyi eşitliğin iki nesne terimi gibi yerleştirir.", "Kategori hatası", "bad"),
            _worked("Bora, Ada'ya güvenir → R(b,a)", "İki argüman yeri ve yön korunur.", "Bağıntı"),
            _worked("R(a,b) ile R(b,a) aynı uygulamadır", "Argüman sırası mantıksal rolü değiştirir.", "Sıra hatası", "bad"),
            _worked("`x dikkatli` doymamış bir yapıdır", "x bir nesne adı değil açık argüman yerini gösterir.", "Fonksiyon"),
            _worked("`Ada dikkatli` belirli bir doğruluk değeri alır", "Fonksiyon Ada argümanıyla tamamlanmıştır.", "Değer"),
            _worked("Ada, F kavramının altına düşer", "Nesne ile kavram arasındaki doğru kategori ilişkisini korur.", "Kavram/nesne"),
            _worked("Ada, F kavramının bir parçasıdır", "Altına düşmeyi mereolojik parça-bütün ilişkisine çevirir.", "Yanlış ilişki", "bad"),
            _worked("∃xF(x), bir nesnenin F olduğunu söyler", "Niceleyici belirli bir nesneyi adlandırmadan tanık gerektirir.", "Varoluş"),
            _worked("∀ bütün nesnelerin adıdır", "Niceleyiciyi nesne kategorisine sokar.", "Düzey hatası", "bad"),
            _worked("Modern F(a), Fregeci çözümlemeyi öğretmek için kullanılabilir", "İşlevsel yapıyı görünür kılan pedagojik köprüdür.", "Köprü"),
            _worked("Modern FOL, Frege'nin bütün kuramıyla aynıdır", "Gösterim yardımı tarihsel ve felsefi özdeşlik sağlamaz.", "Anakronizm", "bad"),
        ],
        [
            "Fonksiyon/argüman ayrımını sözcük sırasına indirgemek.",
            "Doymamışlığı psikolojik eksiklik saymak.",
            "Kavramı nesneler kümesiyle koşulsuz özdeşleştirmek.",
            "Niceleyiciyi çoğul bir özel ad gibi okumak.",
            "Bağıntı argümanlarının rol ve sırasını silmek.",
            "Modern FOL notasyonunu Frege'nin özgün sistemi diye sunmak.",
        ],
        _practice(
            [
                ("`Ada koşuyor` cümlesinde Fregeci argüman hangisidir?", ["Ada", "koşuyor", "doğru", "cümle"], "A", "Ada, `x koşuyor` fonksiyonunu tamamlayan nesnedir.", "Temel"),
                ("Doymamışlık neyi belirtir?", ["Yanlış cümleyi", "Açık argüman yerini", "Eksik yazımı", "Belirsiz duyguyu"], "B", "Fonksiyon tamamlanmak için argüman yeri taşır.", "Temel"),
                ("Fregeci kavram en iyi nasıl tanımlanır?", ["Bir nesne adı", "Bir kelime listesi", "Nesnelerden doğruluk değerlerine fonksiyon", "Herhangi bir küme"], "C", "Birinci düzey kavram nesneyi doğru/yanlışa götürür.", "Temel"),
                ("Hangisi kategori hatasıdır?", ["Ada F altına düşer", "F(a) doğrudur", "F kavramı Ada ile özdeştir", "a bir nesne terimidir"], "C", "Kavram nesne gibi kimlik terimi yapılmıştır.", "Orta"),
                ("`R(a,b)`de b neyi korur?", ["İkinci argüman rolünü", "Doğruluk tablosunu", "Niceleyiciyi", "Fonksiyonun adını"], "A", "İkili bağıntının ikinci rolündedir.", "Temel"),
                ("`R(a,b)` neden `R(b,a)`yı garanti etmez?", ["Harfler küçük", "Roller sıralıdır", "R kavram değildir", "a adı yoktur"], "B", "Argüman sırası bağıntı yönünü taşır.", "Orta"),
                ("`∃xF(x)` ne yapar?", ["x adlı nesneyi tanıtır", "En az bir nesnenin F olduğunu söyler", "F'yi nesne yapar", "Bütün nesneleri adlandırır"], "B", "Varoluş niceleyicisi belirli ad vermeden tanık ister.", "Temel"),
                ("İkinci düzey ayrım neyi önler?", ["Kavram hakkında olan işlemi nesne yüklemi sanmayı", "İsim yazmayı", "Doğruluk değeri vermeyi", "Bağıntı kurmayı"], "A", "Niceleme gibi yapıların kavram düzeyindeki rolünü ayırır.", "İleri"),
                ("Modern `F(a)` kullanımı için doğru not hangisidir?", ["Frege aynen bunu yazdı", "Yalnız pedagojik yeniden yazımdır", "Frege FOL'ü reddetti", "Tarihsel fark yoktur"], "B", "Modern notasyon işlevi gösterir ama tarihsel sistemi tüketmez.", "Orta"),
                ("Kavramın altına düşmek ne değildir?", ["Bir doğruluk koşulu", "Nesne-kavram ilişkisi", "Parça-bütün ilişkisi", "Fonksiyon uygulaması"], "C", "Mereolojik parça olmakla aynı değildir.", "Orta"),
                ("Bir argümanı sabitlenmiş ikili bağıntı ne bırakabilir?", ["Tek yerli fonksiyon", "Yeni niceleyici", "Kimlik", "Hiçbir şey"], "A", "R(a,ζ) tek açık yer taşıyabilir.", "İleri"),
                ("G42'nin temel tarihsel sınırı hangisidir?", ["Frege mantık yazmadı", "Modern FOL bütün Frege kuramına özdeştir", "Modern FOL yararlı ama eksik bir köprüdür", "Frege yalnız dilbilgisi yaptı"], "C", "Pedagojik eşleme tarihsel/felsefi özdeşlik değildir.", "İleri"),
            ]
        ),
        {
            "prompt": "`Her öğrenci bir kitap okudu` cümlesini özne-yüklem ve fonksiyon-argüman açısından karşılaştır.",
            "starter": "Önce `okudu` bağıntısının iki rolünü, sonra niceleyicilerin bu boş yerler üzerindeki sırasını göster.",
            "checks": ["İki argüman rolü ayrı", "Her/bir niceleyici düzeyi açık", "En az iki kapsam okuması ayrılmış", "Modern notasyonun tarihsel sınırı belirtilmiş"],
            "solution": "Özne-yüklem görünüşü `her öğrenci`yi tek özne gibi sunar. Fonksiyon-argüman çözümlemesi `R(x,y)`de x'i okuyan, y'yi okunan rolüne koyar. Bağlama göre ∀x(Sx→∃y(By∧Rxy)) doğal okumadır; tek ortak kitap iddiası ∃y(By∧∀x(Sx→Rxy)) ile ayrılır. Bu modern yazım Fregeci devrimi gösterir, özgün Begriffsschrift değildir.",
        },
        [
            _production_task(
                "Sekiz gündelik cümlede özne-yüklem görünüşü ile fonksiyon-argüman yapısını yan yana çıkar.",
                ["En az iki ikili bağıntı", "Her argüman rolü etiketli", "İki kategori hatası onarılmış", "Bir modern notasyon sınır notu"],
                "Cümlelerden biri görünür dilbilgisinde aynı, mantıksal yapıda farklı iki okuma taşısın.",
                "Çözümleme cümleleri",
                ["Ada Bora'ya yardım etti", "Her yazar bir kitap önerdi", "Yalnız bir kişi geldi", "Hiçbir araştırmacı geç kalmadı"],
            ),
            _production_task(
                "Fonksiyon, kavram ve nesne ayrımını konuya yeni başlayan birine bir sayfalık kavram haritasıyla öğret.",
                ["Doymamışlık açıklanmış", "Kavram/nesne kategori sınırı", "Birinci/ikinci düzey örneği", "Küme ile kavram özdeşleştirilmemiş"],
                "Her ok için ilişkinin adı yazılsın; yalnız kutu listesi olmasın.",
                "Zorunlu düğümler",
                ["fonksiyon", "argüman", "değer", "kavram", "nesne", "niceleme"],
            ),
        ],
        [
            "Yeni bir cümlenin fonksiyon ve argüman yerlerini doğru çıkarır.",
            "Kavram/nesne kategori hatasını gerekçesiyle onarır.",
            "Birinci ve ikinci düzeyi yeni niceleyici örneğinde ayırır.",
            "Modern FOL ile Frege arasındaki bir kazanç ve bir kaybı açıklar.",
        ],
        [
            "Doymamışlık neden eksik yazım demek değildir?",
            "Bir kavramın altına düşmek ile onun parçası olmak nasıl ayrılır?",
            "Modern `F(a)` gösterimi Frege okumasında ne kazandırır, neyi gizler?",
        ],
        "G43'te aynı gönderime sahip farklı ifadelerin neden farklı bilişsel değer taşıyabildiği anlam/gönderim ayrımıyla incelenecek.",
        ["sep-frege-logic", "sep-propositional-function", "sep-frege"],
        "Ders Fregeci kavramı modern küme veya açık formülle koşulsuz özdeşleştirmez. Standart FOL gösterimi tarihsel metni erişilebilir kılan kontrollü bir yeniden yazımdır.",
        ["Fonksiyon ve Kavram", "Kavram ve Nesne", "Begriffsschrift"],
    )
    lesson["reading_fixtures"] = [
        _reading_fixture(
            "g42-begriffsschrift",
            "sep-frege-logic",
            "Begriffsschrift (1879), §§1-12 ve SEP Frege's Logic §2",
            "Yargının içeriğini özne-yüklem kalıbından bağımsız çözümleme ihtiyacı.",
            ["dilbilgisel özne / mantıksal argüman", "içerik / yargı", "tekli yüklem / bağıntı"],
            ["Frege modern FOL yazıyordu", "özne-yüklem bütünüyle anlamsızdır"],
            "İki bağıntılı cümlede geleneksel ve işlevsel çözümlemeyi karşılaştır.",
            "Bu pasajlar tek başına Frege'nin sonraki anlam kuramını tamamlamaz.",
        ),
        _reading_fixture(
            "g42-function-concept",
            "sep-propositional-function",
            "Function and Concept (1891), açılış fonksiyon-argüman tartışması",
            "Fonksiyonun doymamışlığı ve argümandan kategori bakımından ayrılığı.",
            ["fonksiyon / argüman", "doymamış / doymuş", "ifade / gönderim"],
            ["doymamış = anlaşılmaz", "fonksiyon = nesneler listesi"],
            "Aritmetik örnek ile yüklem örneğinin ortak yapısını ve ayrıldığı noktayı yaz.",
            "Benzetme, aritmetik fonksiyon ile kavramın bütün özelliklerini eşitlemez.",
        ),
        _reading_fixture(
            "g42-concept-object",
            "sep-frege",
            "Concept and Object (1892), kavramın yüklemsel rolü tartışması",
            "Kavramdan nesne gibi söz etmenin dilsel baskısı ve kategori sorunu.",
            ["kavram / nesne", "altına düşme / eşitlik", "dilbilgisel ad / mantıksal kategori"],
            ["kavram sözcüğü geçiyorsa ifade kavramdır", "kategori ayrımı sırf sözcük türüdür"],
            "`At kavramı bir kavramdır` benzeri paradoksal görünüşün neden doğduğunu kendi örneğinle açıkla.",
            "Ders, tartışmanın bütün yorum sorunlarını tek çözüme bağlamaz.",
        ),
    ]
    lesson["comparison_fixtures"] = [
        _comparison_fixture(
            "g42-traditional-frege",
            "Geleneksel özne-yüklem çözümlemesi",
            "Fregeci fonksiyon-argüman çözümlemesi",
            "Bir cümlenin mantıksal bileşenlerini ve genellik yapısını görünür kılmak.",
            ["İkili bağıntılar Fregeci yapıda iki rolü açık tutar.", "Niceleme dilbilgisel özne yerine açık argüman yerleri üzerinde işler.", "İki çözümleme her basit cümlede farklı sonuç vermek zorunda değildir."],
            "Aynı doğal dil cümlesinin iki çözümlemede neyin görünür veya gizli kaldığını tabloyla göster.",
        ),
    ]
    lesson["primary_text_locators"] = [
        "Begriffsschrift (1879), §§1-12",
        "Function and Concept (1891), opening function/argument discussion",
        "Concept and Object (1892), concept/object discussion",
    ]
    return lesson


def _candidate_g43():
    lesson = _stage_g_lesson(
        "G43",
        "ders-43-frege-anlam-gonderim-dusunce",
        "Frege: Anlam, Gönderim ve Düşünce",
        "Özdeşlik cümlelerinin bilişsel değerinden hareketle anlam ile gönderimi ayırır; özel ad, cümle ve dolaylı bağlamlarda ayrımın nasıl çalıştığını ve nerede tartışmalı kaldığını inceler.",
        "İçerik ve gönderim",
        45,
        ["ders-42-frege-fonksiyon-arguman-kavram-nesne"],
        [
            "frege.identity_puzzle_reconstruct",
            "frege.sense_reference_distinguish",
            "frege.thought_truth_value_explain",
            "frege.indirect_context_diagnose",
            "frege.mental_image_reject",
        ],
        [
            "`a=a` ile `a=b` özdeşliklerinin aynı gönderime rağmen farklı bilişsel değerini açıklamak.",
            "Bir ifadenin anlamını gönderime ulaşma tarzı olarak, gönderiminden ayırmak.",
            "Cümlenin düşüncesi ile doğruluk değerini farklı semantik roller olarak göstermek.",
            "Dolaylı anlatımda olağan gönderimin neden yeterli olmadığını örnekle göstermek.",
            "Anlamı özel zihinsel imgeye veya yalnız sözlük tanımına indirgeyen okumayı onarmak.",
        ],
        [
            ("Anlam (Sinn)", "Bir gönderimin sunuluş tarzı; farklı ifadeler aynı gönderime farklı anlamlarla ulaşabilir."),
            ("Gönderim (Bedeutung)", "İfadenin dünyada veya Fregeci semantik düzende işaret ettiği nesne ya da değer."),
            ("Bilişsel değer", "Bir cümlenin bilgi taşıma, öğretici olma veya tanınma biçimi bakımından değeri."),
            ("Özdeşlik bilmecesi", "`a=a` ile doğru `a=b` cümlelerinin neden farklı bilgi değeri taşıdığı sorunu."),
            ("Düşünce", "Frege'de bildirici cümlenin nesnel, doğru ya da yanlış olabilen anlamı."),
            ("Doğruluk değeri", "Frege'nin bildirici cümlelerin gönderimi olarak ele aldığı Doğru veya Yanlış."),
            ("Dolaylı bağlam", "İnanç, söyleme gibi yapılarda ifadenin olağan gönderiminin yer değiştirdiği bağlam."),
            ("Zihinsel imge", "Kişiden kişiye değişebilen öznel tasarım; Fregeci anlamla özdeş değildir."),
        ],
        [
            _section(
                "Özdeşlik bilmecesi",
                "`Sabah Yıldızı Sabah Yıldızı'dır` ile `Sabah Yıldızı Akşam Yıldızı'dır` aynı göksel cisme dayanabilir; ikincisi yine de araştırmayla öğrenilen bilgi taşır.",
                "Aynı gönderime sahip iki ifadenin neden birbirinin basit kopyası olmadığını açıklarken.",
                "a=a ile a=b: aynı doğruluk, farklı sunuluş",
                "Yalnız gönderim eşitliği, özdeşlik cümlesinin bilişsel farkını açıklamaz; ifadelerin gönderimi sunma tarzı hesaba katılır.",
                "Farkı yalnız harflerin farklı yazılmasına veya konuşanın şaşırmasına bağlama.",
                [("Hesperus=Phosphorus", "Aynı gezegen, tarihsel olarak farklı tanıma yolları."), ("a=a", "Gönderim biliniyorsa genellikle tanımsal görünür.")],
                ("Aynı gönderim + farklı anlam olasılığını korumak.", "Gönderim aynıysa iki ifade her bakımdan aynıdır demek.", "Yerine koyma doğruluk değerini korusa da bilişsel yolu korumayabilir."),
            ),
            _section(
                "Anlam: gönderimin sunuluş tarzı",
                "Anlam, konuşanın özel resmi değil, gönderime belirli bir yoldan ulaşılmasını sağlayan paylaşılabilir içerik boyutudur.",
                "Eş gönderimli ifadelerin bilgi farkını ve anlaşılabilirliğini incelerken.",
                "ifade → anlam → gönderim",
                "Aynı gönderime birden çok anlamla ulaşılabilir; aynı anlamı kavrayan kişiler farklı özel imgeler taşıyabilir.",
                "Anlamı çağrışım, duygu veya kafadaki resimle özdeşleştirme.",
                [("Üçgenin ağırlık merkezi", "Bir nesneyi belirli geometrik sunuluşla verir."), ("Benim zihnimdeki sarı görüntü", "Paylaşılabilir anlamın ölçütü değildir.")],
                ("Kamusal olarak izlenebilir sunuluş tarzını açıklamak.", "Her kişinin çağrışımını ifadenin anlamı saymak.", "Öznel imge iletişimde ortak içerik sağlamaz."),
            ),
            _section(
                "Gönderim ve boş ad sorunu",
                "Bir ifade anlaşılır bir anlam sunarken gönderimden yoksun olabilir. Bu ihtimal, anlam ile gönderimin neden ayrı tutulduğunu gösterir; fakat boş adların tüm semantiği derste çözülmüş sayılmaz.",
                "Kurgu, hata veya başarısız betimleme içeren ifadeleri değerlendirirken.",
                "anlam var ⇏ gönderim var",
                "Bir ifadeyi anlayabilmek her zaman dünyada ona karşılık gelen nesne bulunduğunu kanıtlamaz.",
                "Anlaşılır her adın zorunlu olarak nesnesi olduğunu varsayma.",
                [("En uzak doğal sayı", "Sunuluş anlaşılır, fakat böyle bir sayı yoktur."), ("Venüs", "Bağlama göre belirli gezegene gönderir.")],
                ("Anlaşılabilirlik ve varlığı ayrı sınamak.", "Anlamlıysa vardır demek.", "Varlık iddiası ek bir semantik/olgusal yük taşır."),
            ),
            _section(
                "Cümle, düşünce ve doğruluk değeri",
                "Bildirici cümlenin anlamı bir düşünce, gönderimi ise Fregeci çerçevede doğruluk değeridir. Aynı düşünce farklı dillerde veya ifadelerde sunulabilir; doğru/yanlış olması düşüncenin içeriğinden ayrı bir semantik roldür.",
                "Cümle düzeyinde anlam ve gönderim ayrımını kurarken.",
                "cümle anlamı = düşünce; cümle gönderimi = Doğru/Yanlış",
                "Düşünce psikolojik düşünme edimi değildir; farklı kişilerin kavrayabileceği nesnel içeriktir.",
                "Bir cümlenin düşüncesini konuşanın o anki duygusu veya beynindeki olay sayma.",
                [("Kar yağıyor", "Bağlamı sabitlendiğinde bir düşünce ifade eder ve doğruluk değeri alır."), ("Ben buna inanıyorum", "İnanma edimi düşüncenin kendisi değildir.")],
                ("İçerik, kavrama edimi ve doğruluk değerini ayırmak.", "Düşünceyi zihinsel olayla özdeşleştirmek.", "Frege'nin nesnellik hedefi bu ayrımı gerektirir."),
            ),
            _section(
                "Dolaylı bağlam ve yerine koyma",
                "`Ada, Sabah Yıldızı'nın göründüğüne inanıyor` cümlesinde eş gönderimli `Akşam Yıldızı` ifadesini körlemesine koymak, Ada'nın inancını değiştirebilir. İnanç ve aktarma bağlamları olağan gönderim hesabını karmaşıklaştırır.",
                "İnanç, bilme, söyleme ve aktarma cümlelerinde eş gönderimli terimleri değiştirirken.",
                "a=b, fakat İnanıyor(k,Fa) ⇏ İnanıyor(k,Fb)",
                "Dış dünyadaki gönderim eşitliği, öznenin iki sunuluş tarzını aynı bildiğini garanti etmez.",
                "Kimlik yerine koyma kuralını bütün dil bağlamlarına koşulsuz taşımak.",
                [("Ali Venüs'ü gördü", "Olağan nesne bağlamında eş gönderim çoğunlukla korunur."), ("Ali Hesperus'un Phosphorus olduğunu bilmiyor", "Sunuluş tarzı bilişsel bağlamın içeriğidir.")],
                ("Bağlamın saydam mı dolaylı mı olduğunu sınamak.", "Eş gönderimi her yerde serbest yerine koymak.", "Dolaylı bağlamda bilişsel içerik değişebilir."),
            ),
            _section(
                "Kuramın işi ve açık sınırları",
                "Anlam/gönderim ayrımı özdeşlik ve dolaylı bağlam sorunlarını örgütler; fakat her adın tek, sabit bir anlam taşıdığı veya bütün bağlam problemlerinin çözüldüğü sonucu çıkarılmaz.",
                "Kuramı uygularken yorum tartışmasını ve bağlam bağımlılığını görünür tutmak için.",
                "açıklayıcı ayrım ≠ tartışmasız tam teori",
                "Bir kuramın belirli bilmecedeki başarısı, sonraki dil felsefesindeki bütün itirazları önceden cevaplamaz.",
                "Frege'nin ayrımını sözlükte iki kutuya yazıp her ifadeye mekanik olarak uygulamak.",
                [("Kimlik bilmecesi", "Ayrımın açık motivasyonudur."), ("İşaret ediciler ve bağlam", "Ek açıklama gerektiren sonraki sorunlardır.")],
                ("Kuramın çözdüğü soruyu ve açık bıraktığını birlikte yazmak.", "Tek ayrımı evrensel ve sorunsuz algoritma saymak.", "Felsefi okuma, başarı kadar kapsam sınırını da kaydeder."),
            ),
        ],
        [
            _worked("a=a ile doğru a=b aynı doğruluk değerine sahip olabilir", "Bilişsel değer yine de farklı olabilir.", "Özdeşlik"),
            _worked("Gönderim aynıysa anlam da zorunlu olarak aynıdır", "Ayrımın temel motivasyonunu inkâr eder.", "Özdeşleştirme", "bad"),
            _worked("Sabah Yıldızı ve Akşam Yıldızı aynı gezegene gönderir", "İki farklı sunuluş tarzı ortak gönderimde birleşir.", "Eş gönderim"),
            _worked("Anlam, kafamda beliren resimdir", "Öznel imgeyi paylaşılabilir semantik içerikle karıştırır.", "İmge hatası", "bad"),
            _worked("Anlamlı bir ifade gönderimsiz olabilir", "Anlaşılabilirlik tek başına nesne varlığını garanti etmez.", "Boş ad"),
            _worked("Gönderimsiz ifade hiçbir biçimde anlaşılamaz", "Anlam ile gönderimi yeniden tekleştirir.", "Varlık hatası", "bad"),
            _worked("Bildirici cümlenin anlamı düşüncedir", "Fregeci düşünce paylaşılabilir doğru/yanlış içeriktir.", "Düşünce"),
            _worked("Düşünce, konuşanın özel zihinsel olayıdır", "Kavrama edimi ile nesnel içeriği karıştırır.", "Psikolojizm", "bad"),
            _worked("Cümlenin gönderimi doğruluk değeridir", "Frege'nin cümle düzeyindeki sistematik hesabını verir.", "Cümle gönderimi"),
            _worked("İnanç bağlamında eş gönderimli adlar her zaman değiştirilebilir", "Özne sunuluş tarzlarının eşliğini bilmiyor olabilir.", "Dolaylı bağlam", "bad"),
            _worked("Kuram kimlik bilmecesini hedefler", "Ayrımın hangi açıklama yüküne cevap verdiğini belirler.", "Motivasyon"),
            _worked("Anlam/gönderim ayrımı bütün dil sorunlarını çözer", "Kuramın tarihsel kapsamını aşan kesinlik yükler.", "Aşırı sonuç", "bad"),
        ],
        [
            "Anlam ve gönderimi iki eşanlamlı sözcük saymak.",
            "Bilişsel değeri yalnız yazım farkına bağlamak.",
            "Fregeci anlamı özel zihinsel imgeye indirgemek.",
            "Anlaşılır her ifadenin gönderimi olduğunu varsaymak.",
            "Düşünceyi bireysel düşünme edimiyle karıştırmak.",
            "Dolaylı bağlamda eş gönderimli adları denetimsiz değiştirmek.",
        ],
        _practice(
            [
                ("Özdeşlik bilmecesinin çekirdeği nedir?", ["a=a her zaman yanlış", "Doğru a=b'nin bilgi taşıyabilmesi", "Adların gönderimsizliği", "Yüklemlerin aritesi"], "B", "Aynı gönderime rağmen bilişsel fark açıklanmalıdır.", "Temel"),
                ("Anlam en iyi nasıl tanımlanır?", ["Özel imge", "Gönderimin sunuluş tarzı", "Yalnız nesne", "Doğruluk tablosu"], "B", "Sinn, gönderime ulaşma biçimini taşır.", "Temel"),
                ("Gönderim neyi belirtir?", ["Her çağrışımı", "İfadenin işaret ettiği öğeyi", "Konuşma hızını", "Yalnız kelime türünü"], "B", "Gönderim, ifadenin semantik hedefidir.", "Temel"),
                ("Aynı gönderime ne eşlik edebilir?", ["Yalnız tek anlam", "Farklı anlamlar", "Daima boş ad", "Hiçbir düşünce"], "B", "Eş gönderimli ifadeler farklı sunuluş tarzları taşıyabilir.", "Temel"),
                ("Zihinsel imge neden anlamla özdeş değildir?", ["Hiç oluşmaz", "Kişiden kişiye değişebilir", "Daima yanlıştır", "Gönderimdir"], "B", "Paylaşılabilir içerik özel imgelerden ayrılır.", "Orta"),
                ("Anlamlı ama gönderimsiz ifade olasılığı neyi gösterir?", ["Anlam=gönderim", "Anlaşılabilirlik varlığı kanıtlamaz", "Her ad doğrudur", "Cümleler nesnedir"], "B", "Semantik rol ve varlık ayrı sınanır.", "Orta"),
                ("Frege'de bildirici cümlenin anlamı nedir?", ["Düşünce", "Nesne adı", "Yüklem", "Zihinsel imge"], "A", "Doğru ya da yanlış olabilen nesnel içeriktir.", "Temel"),
                ("Bildirici cümlenin gönderimi nedir?", ["Konuşan", "Doğruluk değeri", "Dil", "Kavram"], "B", "Fregeci sistemde Doğru veya Yanlış'tır.", "Orta"),
                ("Dolaylı bağlamda temel risk nedir?", ["Arite artar", "Eş gönderimli değişim inanç içeriğini değiştirebilir", "Hiç gönderim yoktur", "Niceleyici kaybolur"], "B", "Sunuluş tarzı bilişsel bağlamda rol oynar.", "Orta"),
                ("Hangisi doğru sınır notudur?", ["Kuram bütün bağlamları çözer", "Kuram yalnız yazımı açıklar", "Ayrım belirli sorunları çözer ama tartışmaları bitirmez", "Frege anlamı reddeder"], "C", "Açıklama başarısı evrensel tamlık değildir.", "İleri"),
                ("`Ali Hesperus'u biliyor`dan ne doğrudan çıkmaz?", ["Ali bir şeye inanıyor", "Ali Phosphorus sunuluşunu biliyor", "Hesperus'un gönderimi olabilir", "Cümle dolaylı bağlam içerir"], "B", "Eş gönderim bilişsel eşlik sağlamaz.", "İleri"),
                ("G43'te psikolojizm hatası hangisidir?", ["Düşünceyi paylaşılabilir içerik saymak", "Düşünceyi yalnız özel zihinsel olay saymak", "Doğruluk değeri ayırmak", "Gönderimi sınamak"], "B", "Fregeci düşünce bireysel edim değildir.", "İleri"),
            ]
        ),
        {
            "prompt": "Aynı kişiye gönderdiği söylenen `maskeli yazar` ve `ödüllü romancı` ifadeleriyle kurulan iki özdeşlik cümlesinin bilişsel değerini çözümle.",
            "starter": "Gönderim eşliğini varsay, sonra her ifadenin hangi tanıma yolunu sunduğunu ve bir öznenin bunlardan yalnız birini bilebileceğini göster.",
            "checks": ["Anlam/gönderim ayrı", "Bilişsel fark açıklanmış", "Zihinsel imgeye indirgenmemiş", "Dolaylı bağlam örneği var"],
            "solution": "İki ifade aynı kişiye gönderse bile biri görünüş, diğeri başarı üzerinden sunar. `Maskeli yazar ödüllü romancıdır` bu yolların birleştiğini öğretebilir. Bir okurun maskeli yazarı tanıyıp ödülü bilmemesi mümkündür; bu yüzden inanç bağlamında terimler körlemesine değiştirilemez. Ayrım, okurun özel yüz imgesine değil kamusal tanıma koşullarına dayanır.",
        },
        [
            _production_task(
                "Üç eş gönderimli ifade çifti kur ve her biri için kimlik, bilgi ve dolaylı bağlam cümlesi yaz.",
                ["Gönderim açık", "Farklı sunuluş tarzı", "Bilişsel değer gerekçesi", "Yerine koyma sınırı"],
                "En az bir örnek matematikten, biri gündelik kamusal bilgiden gelsin.",
                "Örnek alanları",
                ["coğrafya", "matematik", "takma ad", "kurumsal unvan"],
            ),
            _production_task(
                "Anlamı zihinsel imge sayan kısa bir paragrafı Fregeci ayrımları koruyacak biçimde yeniden yaz.",
                ["İmge/anlam ayrımı", "Paylaşılabilirlik", "Gönderim olasılığı", "Kuramın sınırı"],
                "Revizyon, özel imgelerin hiç var olmadığını iddia etmesin.",
                "Hatalı savlar",
                ["Herkes aynı kelimede aynı resmi görür", "Resim yoksa anlam yoktur", "Aynı nesne tek anlam demektir"],
            ),
        ],
        [
            "Yeni bir özdeşlik örneğinde bilişsel değer problemini kurar.",
            "Anlam, gönderim ve zihinsel imgeyi gerekçeli olarak ayırır.",
            "Cümle düzeyinde düşünce ve doğruluk değerinin rollerini açıklar.",
            "Dolaylı bağlamda geçersiz yerine koymayı yeni örnekle teşhis eder.",
        ],
        [
            "Doğru `a=b`, doğru `a=a`dan nasıl daha öğretici olabilir?",
            "Anlam neden zihinsel imge değildir?",
            "Eş gönderimli terimler hangi bağlamda neden serbestçe değiştirilemez?",
        ],
        "G44'te Russell, gönderiyor gibi görünen belirli betimlemeleri niceleyici, biriciklik ve kapsam yapısıyla çözümler.",
        ["sep-frege", "sep-frege-logic"],
        "Ders anlam/gönderim ayrımını tek ve tartışmasız çağdaş anlambilim olarak sunmaz. Fregeci düşünce psikolojik bir olay; anlam da kişisel çağrışım olarak öğretilmez.",
        ["Über Sinn und Bedeutung", "Der Gedanke"],
    )
    lesson["reading_fixtures"] = [
        _reading_fixture(
            "g43-identity-opening",
            "sep-frege",
            "On Sense and Reference (1892), açılıştaki a=a / a=b özdeşlik problemi",
            "Doğru özdeşliklerin neden farklı bilgi değeri taşıdığı.",
            ["doğruluk değeri / bilişsel değer", "işaret / anlam / gönderim", "a=a / a=b"],
            ["fark yalnız harflerin görünüşüdür", "aynı gönderim aynı anlamı zorunlu kılar"],
            "Özdeşlik problemini iki yeni kamusal örnekle yeniden kur.",
            "Örnek, Frege'nin bütün dil kuramını tek başına kanıtlamaz.",
        ),
        _reading_fixture(
            "g43-image-distinction",
            "sep-frege",
            "On Sense and Reference (1892), idea/image ile sense ayrımı",
            "Paylaşılabilir anlamın öznel tasarımdan ayrılması.",
            ["anlam / tasarım", "nesnel içerik / öznel yaşantı", "iletişim / çağrışım"],
            ["Frege imgeleri inkâr eder", "her zihinsel ortaklık anlam özdeşliğidir"],
            "Aynı adı anlayan iki kişinin farklı imgeler taşıyabildiği bir vaka çözümle.",
            "Ayrım, psikolojik imgelerin nedensel rolü hakkında tam teori vermez.",
        ),
        _reading_fixture(
            "g43-thought-context",
            "sep-frege",
            "On Sense and Reference (1892), cümlelerin anlamı/gönderimi ve dolaylı konuşma bölümleri",
            "Düşünce, doğruluk değeri ve dolaylı gönderim arasındaki ilişki.",
            ["cümle / düşünce", "düşünce / doğruluk değeri", "olağan / dolaylı bağlam"],
            ["düşünce konuşanın beyin olayıdır", "eş gönderimli değişim her bağlamda geçerlidir"],
            "Bir inanç raporunda iki eş gönderimli adı değiştir ve bilgi kaybını göster.",
            "Dolaylı bağlam çözümlemesinin çağdaş bütün itirazları kapattığı varsayılmaz.",
        ),
    ]
    lesson["comparison_fixtures"] = [
        _comparison_fixture(
            "g43-reference-only-sense-reference",
            "Yalnız gönderim hesabı",
            "Anlam ve gönderim ayrımı",
            "Özdeşlik cümlelerinin doğruluk ve bilgi değerini açıklamak.",
            ["Yalnız gönderim doğruluk eşliğini açıklar, öğrenme farkını açıklamaz.", "Anlam sunuluş tarzını ekler.", "Anlamın eklenmesi bütün bağlam sorunlarını otomatik çözmez."],
            "Bir özdeşlik vakasında her yaklaşımın açıkladığı ve açıklayamadığını yaz.",
        ),
    ]
    lesson["primary_text_locators"] = [
        "On Sense and Reference (1892), identity puzzle",
        "On Sense and Reference (1892), sense/reference and idea distinction",
        "On Sense and Reference (1892), sentence reference and indirect contexts",
    ]
    return lesson


def _candidate_g44():
    lesson = _stage_g_lesson(
        "G44",
        "ders-44-russell-belirli-betimlemeler",
        "Russell: Belirli Betimlemeler ve Mantıksal Biçim",
        "`F olan şey G'dir` görünüşündeki belirli betimlemeleri varlık, biriciklik ve yüklemleme koşullarına ayırır; olumsuzlamanın kapsamını yüzeysel sözcük sırasından bağımsız denetler.",
        "Betimleme ve kapsam",
        48,
        ["ders-43-frege-anlam-gonderim-dusunce"],
        [
            "russell.description_components_extract",
            "russell.logical_form_symbolize",
            "russell.negation_scope_distinguish",
            "russell.empty_description_evaluate",
            "russell.contextual_definition_limit",
        ],
        [
            "Belirli betimlemenin dilbilgisel özne gibi görünmesi ile mantıksal niceleme yapısını ayırmak.",
            "Varlık, biriciklik ve yüklemleme koşullarını ayrı ayrı yazmak ve sınamak.",
            "`F olan şey G'dir` biçimini kimlik kullanarak FOL'de çözümlemek.",
            "Olumsuzlamanın geniş ve dar kapsam okumalarını geri çeviriyle ayırmak.",
            "Betimleme kuramının çözümlediği problemi ve tartışmalı sınırlarını birlikte raporlamak.",
        ],
        [
            ("Belirli betimleme", "`F olan şey`, `tek F` veya `the F` görünüşünde biriciklik ima eden ifade."),
            ("Varlık koşulu", "En az bir nesnenin betimleyici F koşulunu sağlaması."),
            ("Biriciklik koşulu", "F koşulunu sağlayan her nesnenin aynı nesne olması."),
            ("Yüklemleme koşulu", "Varlığı ve biricikliği kurulan nesnenin ayrıca G olması."),
            ("Mantıksal biçim", "Cümlenin doğruluk koşullarını belirleyen, yüzeysel dilbilgisinden farklı olabilen yapı."),
            ("Geniş kapsam", "Bir işlecin cümlenin daha büyük bölümünü kapsamına alması."),
            ("Dar kapsam", "Bir işlecin betimleme çözümlemesinin içinde veya daha küçük bir bileşende çalışması."),
            ("Bağlamsal tanım", "Betimlemenin tek başına adlandırdığı nesneyi vermek yerine geçtiği bütün cümlenin kullanımını çözümlemek."),
        ],
        [
            _section(
                "Dilbilgisel özne, mantıksal ad olmayabilir",
                "`Mevcut Fransa kralı keldir` cümlesinde betimleme dilbilgisel özne yerindedir. Russellcı çözümleme onu gizli bir özel ad saymak yerine cümlenin niceleme yapısına dağıtır.",
                "Bir ifade nesne adı gibi görünmesine rağmen başarısız veya birden çok karşılığı olduğunda.",
                "the F is G → niceliksel çözümleme",
                "Cümlenin doğruluk koşulu, betimlemenin tek başına neye gönderdiğini bulmadan varlık ve biriciklik üzerinden verilebilir.",
                "Dilbilgisel özne olan her ifadeyi mantıksal ad sayma.",
                [("Mevcut Fransa kralı keldir", "Betimleme, niceleme ve kimlikle açılır."), ("Ada keldir", "`Ada` bağlama göre doğrudan ad rolü oynayabilir.")],
                ("İfadenin cümledeki bağlamsal işini çözümlemek.", "Önce hayali bir nesne uydurup ona özellik yüklemek.", "Boş betimleme için nesne varsaymak gerekmez."),
            ),
            _section(
                "Üç koşul: varlık, biriciklik, yüklemleme",
                "`F olan şey G'dir` cümlesi en az bir F bulunduğunu, en fazla bir F bulunduğunu ve o F'nin G olduğunu birlikte söyler.",
                "Bir betimlemenin hangi nedenle başarısız olduğunu teşhis ederken.",
                "∃x(Fx ∧ ∀y(Fy→y=x) ∧ Gx)",
                "İlk bileşen tanık ister; ikinci bütün F tanıklarını aynı nesneye bağlar; üçüncü seçilen nesneye G yükler.",
                "Yalnız `∃x(Fx∧Gx)` yazıp biricikliği sessizce bırakma.",
                [("Tek editör geldi", "Varlık ve biriciklik ikisi de gerekir."), ("Bir editör geldi", "Yalnız varlık bildirir; başka editörleri dışlamaz.")],
                ("Üç koşulu ayrı satırda geri okumak.", "`bir` ile `tek`i aynı niceleme saymak.", "Belirli betimlemenin ayırt edici yükü biricikliktir."),
            ),
            _section(
                "Biricikliği kimlikle kurmak",
                "`∀y(Fy→y=x)` bileşeni, F olan herhangi bir y'nin seçilen x ile özdeş olduğunu söyler. Böylece birden fazla F görünen model cümleyi yanlış yapar.",
                "Biriciklik iddiasını FOL'de açıkça kodlarken.",
                "unique F(x) := Fx ∧ ∀y(Fy→y=x)",
                "Kimlik, iki tanığın aslında aynı alan üyesi olmasını ifade eder; yalnız benzerlik veya aynı özellikleri taşıma yetmez.",
                "`∀y(Fy→Fx)` yazmak; bu yalnız x'in F olduğunu tekrarlar, y=x demez.",
                [("İki ayrı F var", "Herhangi biri x seçilse diğeri x'e özdeş olmadığı için biriciklik bozulur."), ("İki ad aynı nesneye gidiyor", "Ad sayısı değil alan üyesi sayısı önemlidir.")],
                ("Her F tanığını seçilen x'e kimlikle bağlamak.", "Aynı yüklemi paylaşmayı özdeşlik sanmak.", "İki nesne aynı özellikleri taşıyıp yine farklı olabilir."),
            ),
            _section(
                "Boş ve çoklu betimlemeler",
                "Hiç F yoksa varlık koşulu; birden çok F varsa biriciklik koşulu başarısızdır. Her iki durumda olumlu `F olan şey G'dir` çözümlemesi yanlıştır, fakat gerekçeler ayrıdır.",
                "Modelde betimlemenin neden gönderim kuramadığını incelerken.",
                "0 F → varlık başarısız; 2+ F → biriciklik başarısız",
                "Kuram başarısız betimlemeyi gizemli bir nesneye göndermek yerine bütün cümlenin doğruluk koşulunda ele alır.",
                "Boş betimleme ile çok anlamlı/birden çok nesneli betimlemeyi tek hata sayma.",
                [("Mevcut Fransa kralı", "Varlık koşulu başarısız."), ("Dünyadaki kıta", "Birden çok kıta varsa biriciklik başarısız.")],
                ("Varlık ve biriciklik testlerini sırayla çalıştırmak.", "Her başarısızlığı `nesne belirsiz` diye geçmek.", "İki başarısızlığın mantıksal tanıkları farklıdır."),
            ),
            _section(
                "Olumsuzlama ve kapsam",
                "`F olan şey G değildir` en az iki yapı taşıyabilir. Dar kapsam okumasında tek F vardır ve G değildir; geniş kapsam okumasında tek F'nin G olduğu bütün iddiası doğru değildir. İkinci okuma F hiç olmadığında da doğru olabilir.",
                "Olumsuz belirli betimlemeleri ve varlık yükünü çözümlerken.",
                "dar: ∃x(UFx ∧ ¬Gx); geniş: ¬∃x(UFx ∧ Gx)",
                "Olumsuzlamanın betimleme çözümlemesinin içinde veya dışında olması farklı doğruluk koşulları üretir.",
                "Sözcükte `değil`in hemen önündeki parçaya bakıp kapsamı otomatik seçme.",
                [("Tek müdür güler yüzlü değildir", "Tek müdürün varlığını koruyan dar kapsam okuması."), ("Tek müdürün güler yüzlü olduğu doğru değil", "Varlık/biriciklik dahil bütün iddiayı olumsuzlayabilir.")],
                ("İki formülü ayrı geri çeviriyle vermek.", "Olumsuzlamayı yer değiştirip eşdeğer saymak.", "Kapsam, varlık çıkarımını değiştirir."),
            ),
            _section(
                "Bağlamsal çözümleme ve kuram sınırı",
                "Russell betimlemeyi eksik sembol gibi ele alır: anlamlı katkısı, geçtiği cümlenin çözümlemesinde görünür. Bu güçlü araç, bütün doğal dil kullanımlarının tek ve tartışmasız hesabı olarak sunulmaz.",
                "Kuramın felsefi başarısı ile sonraki itirazları aynı anda değerlendirirken.",
                "betimleme tek başına değil, cümle içinde çözülür",
                "Yüzeysel ad görünüşünü niceleme yapısına çevirmek boş terim ve kapsam bilmecelerini örgütler.",
                "Her adın gizli betimleme olduğunu veya konuşur niyetinin hiç rolü olmadığını dersin sonucu sayma.",
                [("Bağlamsal tanım", "Bütün cümlenin doğruluk koşulunu verir."), ("Tek başına `the F`", "Kuramda bağımsız ad gibi nesne seçmek zorunda değildir.")],
                ("Çözülen problemi ve açık tartışmayı ayırmak.", "Başarıyı evrensel son teori diye genellemek.", "Ders tarihsel çözümlemeyi öğretir, çağdaş tartışmayı kapatmaz."),
            ),
        ],
        [
            _worked("Tek F, G'dir → ∃x(Fx∧∀y(Fy→y=x)∧Gx)", "Varlık, biriciklik ve yüklemleme birlikte kodlanır.", "Tam çözümleme"),
            _worked("Tek F, G'dir → ∃x(Fx∧Gx)", "Birden fazla F olasılığını dışlamaz.", "Biriciklik eksik", "bad"),
            _worked("Hiç F yoksa olumlu betimleme yanlıştır", "Varlık bileşeni için tanık bulunamaz.", "Boş betimleme"),
            _worked("İki ayrı F varsa olumlu betimleme yanlıştır", "Biriciklik bileşeni başarısızdır.", "Çoklu betimleme"),
            _worked("İki farklı ad aynı nesneye gidiyorsa iki F vardır", "Ad sayısı alan üyesi sayısı değildir.", "Ad/nesne hatası", "bad"),
            _worked("∀y(Fy→y=x) biricikliği kurar", "Her F adayı seçilen x ile özdeş olmak zorundadır.", "Kimlik"),
            _worked("∀y(Fy→Fx) biricikliği kurar", "y=x koşulu yoktur; yalnız Fx tekrar edilir.", "Yanlış formül", "bad"),
            _worked("Dar kapsam olumsuzlama tek F'nin varlığını koruyabilir", "Olumsuzluk yalnız G yüklemine uygulanır.", "Dar kapsam"),
            _worked("Geniş kapsam olumsuzlama varlık başarısızlığında doğru olabilir", "Bütün olumlu çözümleme olumsuzlanır.", "Geniş kapsam"),
            _worked("Olumsuz iki okuma her modelde eşdeğerdir", "F bulunmayan veya biricik olmayan modeller okumaları ayırır.", "Kapsam hatası", "bad"),
            _worked("Betimleme cümle içinde bağlamsal olarak çözülür", "Bağımsız gizemli nesne varsaymadan doğruluk koşulu verir.", "Bağlamsal tanım"),
            _worked("Russell her özel adı kesin olarak betimleme saymıştır ve tartışma bitmiştir", "Kuramın kapsamını ve tarihsel nüansını aşar.", "Aşırı genelleme", "bad"),
        ],
        [
            "Dilbilgisel özneyi otomatik mantıksal ad saymak.",
            "Biriciklik bileşenini varoluşsal çözümlemeden düşürmek.",
            "Aynı özellikleri taşıyan nesneleri özdeş saymak.",
            "Boş ve çoklu betimlemeyi aynı başarısızlık gerekçesiyle açıklamak.",
            "Olumsuzlamanın dar ve geniş kapsamını tek okuma saymak.",
            "Bağlamsal çözümlemeyi bütün adların tartışmasız son kuramına çevirmek.",
        ],
        _practice(
            [
                ("Belirli betimlemenin üç koşulu hangisidir?", ["Varlık-biriciklik-yüklemleme", "Ad-fiil-sıfat", "Doğru-yanlış-belirsiz", "Anlam-imge-duygu"], "A", "Russellcı açılım üç ayrı doğruluk yükü taşır.", "Temel"),
                ("`∃x(Fx∧Gx)` neden yetersizdir?", ["Varlık yok", "Biriciklik yok", "G yok", "Niceleyici yok"], "B", "Birden fazla F'yi dışlamaz.", "Temel"),
                ("Biriciklik hangi bileşenle kurulur?", ["∀y(Fy→y=x)", "∀y(Fy→Fx)", "Gx", "¬Fx"], "A", "Her F tanığı x ile özdeşlenir.", "Orta"),
                ("Hiç F yoksa hangi koşul bozulur?", ["Yüklemleme", "Varlık", "Biriciklik yalnız", "Kimlik"], "B", "Tanık bulunamaz.", "Temel"),
                ("İki ayrı F varsa hangi koşul bozulur?", ["Varlık", "Biriciklik", "Her zaman G", "Olumsuzlama"], "B", "Tek F olma koşulu karşı örnek alır.", "Temel"),
                ("Farklı iki ad aynı nesneye gidiyorsa kaç nesne vardır?", ["Zorunlu iki", "Adlardan belirlenemez; bir olabilir", "Sıfır", "Sonsuz"], "B", "Ad ayrılığı nesne ayrılığı değildir.", "Orta"),
                ("Dar kapsam olumsuzlama genellikle neyi korur?", ["Tek F'nin varlığını", "Hiç F olmadığını", "Bütün cümlenin doğruluğunu", "Adın anlamını"], "A", "Olumsuzluk G yüklemine daralabilir.", "Orta"),
                ("Geniş kapsam olumsuzlama neyi kapsar?", ["Yalnız G'yi", "Bütün olumlu betimleme iddiasını", "Yalnız F'yi", "Yalnız x'i"], "B", "Varlık ve biriciklik dahil çözümleme olumsuzlanır.", "Orta"),
                ("Mantıksal biçim neye karşıt olabilir?", ["Doğruluğa", "Yüzeysel dilbilgisel görünüme", "Her anlama", "Kaynağa"], "B", "Cümle özne gibi görünse de niceleme yapısı taşıyabilir.", "Temel"),
                ("Bağlamsal tanım ne yapar?", ["Betimlemeye gizli nesne uydurur", "Geçtiği bütün cümlenin kullanımını çözümler", "Her adı siler", "Kapsamı yok eder"], "B", "Betimlemenin katkısı cümle çözümlemesinde verilir.", "İleri"),
                ("Boş betimlemede doğru yöntem hangisidir?", ["Hayali nesne seçmek", "Varlık koşulunun başarısızlığını göstermek", "Cümleyi anlamsız ilan etmek zorunda olmak", "Biricikliği varsaymak"], "B", "Niceleyici çözümlemesi başarısızlığı açıklar.", "Orta"),
                ("Kuram sınırı için doğru ifade hangisidir?", ["Bütün tekil terimler sorunu bitmiştir", "Kuram belirli bilmeceleri çözer, kapsamı tartışmalıdır", "Russell nicelemeyi reddeder", "Yüzeysel dilbilgisi her zaman yeterlidir"], "B", "Başarı ile evrensel tamlık ayrılır.", "İleri"),
            ]
        ),
        {
            "prompt": "`Kütüphanenin müdürü bugün gelmedi` cümlesinin iki olumsuz kapsam okumasını kur ve üç modelde ayır.",
            "starter": "Önce müdür olma koşulunu M, gelmeyi G ile yaz; tek M var, hiç M yok ve iki M var modellerini ayrı sın.",
            "checks": ["Varlık açık", "Biriciklik açık", "Dar/geniş kapsam ayrı", "Her model için geri çeviri"],
            "solution": "Dar okuma ∃x(Mx∧∀y(My→y=x)∧¬Gx), tek müdürün varlığını ve gelmediğini söyler. Geniş okuma ¬∃x(Mx∧∀y(My→y=x)∧Gx), tek ve gelen bir müdür bulunduğunu reddeder. Hiç müdür olmayan modelde dar yanlış, geniş doğru; tek gelmeyen müdürde ikisi doğru; iki müdürde dar yanlış, geniş doğru olabilir.",
        },
        [
            _production_task(
                "Altı belirli betimlemeyi varlık, biriciklik ve yüklemleme tablosuna çöz.",
                ["Her bileşen ayrı", "Tam FOL formülü", "Geri çeviri", "Başarısızlık tanığı"],
                "İki örnek boş, iki örnek çoklu, iki örnek gerçekten biricik olsun.",
                "Betimleme adayları",
                ["sınıfın temsilcisi", "şehrin belediye başkanı", "en büyük doğal sayı", "masadaki kitap"],
            ),
            _production_task(
                "Dört olumsuz betimleme için dar ve geniş kapsam çiftleri üret.",
                ["İki ayrı formül", "İki ayrı doğal dil geri okuma", "Ayırıcı model", "Varlık çıkarımı karşılaştırması"],
                "En az bir örnekte iki okumanın aynı, birinde farklı doğruluk değeri aldığı model ver.",
                "Kapsam kalıpları",
                ["tek F, G değil", "tek F'nin G olduğu doğru değil", "herkes tek F'yi görmedi", "tek F bulunmadı"],
            ),
        ],
        [
            "Yeni betimlemenin üç doğruluk koşulunu eksiksiz çıkarır.",
            "Biricikliği kimlikle doğru sembolleştirir.",
            "Dar ve geniş olumsuzlamayı ayırıcı modelle gösterir.",
            "Kuramın çözüm gücü ve kapsam sınırını birlikte açıklar.",
        ],
        [
            "Dilbilgisel özne neden mantıksal ad olmak zorunda değildir?",
            "Biriciklik koşulu yalnız varoluşsal niceleyiciyle neden kurulamaz?",
            "Olumsuzlamanın kapsamı betimlemenin varlık yükünü nasıl değiştirir?",
        ],
        "G45'te mantıksal çözümleme, atomik olgu ve atomik önerme kavramlarıyla Russell ve erken Wittgenstein arasındaki köprü kurulacak.",
        ["sep-descriptions", "sep-logical-atomism", "oxford-logic-language"],
        "Standart Russell çözümlemesi tarihsel işleviyle öğretilir; her doğal dil betimlemesinin bağlamdan bağımsız tek çözümü veya bütün özel adların tartışmasız teorisi sayılmaz.",
        ["On Denoting", "The Philosophy of Logical Atomism"],
    )
    lesson["reading_fixtures"] = [
        _reading_fixture(
            "g44-on-denoting-form",
            "sep-descriptions",
            "Russell, On Denoting (1905), belirli betimleme çözümlemesi",
            "Dilbilgisel özne görünüşünün varlık, biriciklik ve yüklemleme yapısına açılması.",
            ["gramatik biçim / mantıksal biçim", "varlık / biriciklik", "ad / bağlamsal betimleme"],
            ["the F gizli özel addır", "varlık tek başına yeterlidir"],
            "Yeni bir betimlemenin üç bileşenini ve tam FOL biçimini çıkar.",
            "Standart formül, doğal dildeki bütün kullanım ve ima farklarını tüketmez.",
        ),
        _reading_fixture(
            "g44-negative-description",
            "sep-descriptions",
            "Descriptions, Russell's Theory bölümü: olumsuz betimleme ve kapsam örnekleri",
            "Olumsuzlamanın betimleme içinde ve dışında farklı doğruluk koşulları üretmesi.",
            ["dar / geniş kapsam", "birincil / ikincil oluş", "varlık çıkarımı / varlık reddi"],
            ["değil tek bir sabit yerde çalışır", "iki okuma her modelde eşdeğerdir"],
            "İki kapsam okumasını ayıran en küçük modeli kur.",
            "Kapsam belirsizliği her kullanımda fiilen bulunmak zorunda değildir; bağlam bir okumayı seçebilir.",
        ),
        _reading_fixture(
            "g44-incomplete-symbol",
            "sep-logical-atomism",
            "Russell's logical atomism: analysis and incomplete symbols",
            "Betimlemenin bağımsız nesne adı yerine geçtiği önerme içinde çözümlenmesi.",
            ["tek başına ifade / cümlede katkı", "görünür bileşen / çözümleme", "kuramsal araç / ontolojik nesne"],
            ["eksik sembol anlamsız semboldür", "çözümleme yeni hayali nesne ekler"],
            "Bir betimleme cümlesinin çözümlemeden önce ve sonraki ontolojik yükünü karşılaştır.",
            "Eksik sembol öğretisi Russell'ın bütün dönemlerinde değişmez tek formül gibi sunulmaz.",
        ),
    ]
    lesson["comparison_fixtures"] = [
        _comparison_fixture(
            "g44-name-description",
            "Mantıksal ad gibi okuma",
            "Russellcı belirli betimleme çözümlemesi",
            "Gönderim başarısız olduğunda cümlenin doğruluk koşulunu açıklamak.",
            ["Ad okuması önce bir nesne arar.", "Betimleme çözümlemesi varlık ve biricikliği cümlenin iddiasına katar.", "Hangi ifadelerin gerçek mantıksal ad olduğu ayrıca tartışmalıdır."],
            "Boş bir betimleme cümlesinde iki yaklaşımın ontolojik ve semantik maliyetini yaz.",
        ),
    ]
    lesson["primary_text_locators"] = [
        "On Denoting (1905), definite descriptions analysis",
        "The Philosophy of Logical Atomism (1918), analysis and incomplete symbols",
    ]
    return lesson


def _candidate_g45():
    lesson = _stage_g_lesson(
        "G45",
        "ders-45-cozumleme-ve-mantiksal-atomculuk",
        "Çözümleme ve Mantıksal Atomculuk",
        "Mantıksal çözümlemenin yüzeyden yapıya geçişini; atomik olgu, atomik önerme ve doğruluk-fonksiyonlu birleşimi Russell ile erken Wittgenstein'ın ortak sorunları ve ayrılıkları üzerinden kurar.",
        "Russell-Erken Wittgenstein köprüsü",
        50,
        ["ders-44-russell-belirli-betimlemeler"],
        [
            "atomism.analysis_method_explain",
            "atomism.fact_thing_distinguish",
            "atomism.atomic_molecular_map",
            "atomism.physical_atom_error_reject",
            "atomism.russell_wittgenstein_compare",
        ],
        [
            "Mantıksal çözümlemeyi yalnız cümleyi kısaltma veya sözcük tanımlama işleminden ayırmak.",
            "Olgu ile nesne; atomik önerme ile atomik olgu rollerini ayrı tutmak.",
            "Moleküler önermenin atomik önermelerden doğruluk işlemleriyle kuruluşunu göstermek.",
            "Mantıksal atomu fiziksel parçacık anlamında okuyan yanılgıyı onarmak.",
            "Russell ile erken Wittgenstein'ın ortak problem alanını tarihsel ve doktrinel özdeşliğe çevirmeden karşılaştırmak.",
        ],
        [
            ("Mantıksal çözümleme", "Bir önermenin yüzeysel dilbilgisinin altında doğruluk koşullarını taşıyan yapıyı açığa çıkarma yöntemi."),
            ("Olgu", "Bir önermeyi doğru ya da yanlış kılan, nesnelerin belirli biçimde bir araya gelmesi veya gelmemesi."),
            ("Nesne", "Bir olgunun bileşeni olabilen öğe; olgunun kendisiyle aynı kategori değildir."),
            ("Atomik önerme", "Analizde daha basit doğruluk-fonksiyonlu önermelere ayrılmayan temel önerme."),
            ("Atomik olgu", "Atomik önermenin doğru olması hâlinde onunla ilişkili temel durum veya olgu."),
            ("Moleküler önerme", "Atomik önermelerden doğruluk işlemleriyle kurulan bileşik önerme."),
            ("Mantıksal atomculuk", "Dünya ve önermelerin çözümlemesinde bağımsız temel bileşenler arayan görüşler ailesi."),
            ("Yapısal eşlik", "Önerme ile temsil ettiği durum arasında bileşen ve birleşme düzeni bakımından kurulan ilişki."),
        ],
        [
            _section(
                "Çözümleme bir yöntemdir",
                "Russell ve erken Wittgenstein bağlamında çözümleme, cümlenin gündelik görünüşünü doğruluk koşullarını taşıyan daha açık yapıya dönüştürür. Betimleme kuramı bunun örneklerinden biridir.",
                "Yüzeyde ad gibi görünen, kapsamı veya bağıntı yapısı gizli ifadelerde.",
                "yüzeysel biçim → mantıksal biçim",
                "Başarılı çözümleme, aynı cümleyi yalnız daha kısa söylemez; hangi durumlarda doğru olacağını açıklaştırır.",
                "Çözümlemeyi sözcükleri sözlükte tanımlamak veya metni özetlemek sanma.",
                [("Tek F, G'dir", "Niceleme ve kimlik yapısına açılır."), ("Cümleyi daha kısa yazmak", "Mantıksal çözümleme garantisi vermez.")],
                ("Doğruluk koşulundaki gizli yapıyı göstermek.", "Yalnız eşanlamlı sözcüklerle yeniden yazmak.", "Yöntemin hedefi yapısal açıklıktır."),
            ),
            _section(
                "Dünya şeylerin değil olguların toplamı mı?",
                "Erken Wittgenstein'ın açılış ayrımı, yalnız hangi nesnelerin bulunduğuna değil onların nasıl bir araya geldiğine odaklanır. Aynı nesneler farklı düzenlenince farklı dünya durumları oluşabilir.",
                "Bir önermeyi doğru yapanın yalnız nesne listesi olmadığını gösterirken.",
                "nesneler + düzenleniş → durum/olgu",
                "Ada ve kitap nesnelerinin bulunması, Ada'nın kitabı okuduğu olgusunu tek başına vermez; ilişki ve rol gerekir.",
                "Olgu ile nesneyi veya olgu ile doğru cümleyi özdeşleştirme.",
                [("Ada kitabı okuyor", "Nesneler belirli bağıntıda düzenlenmiştir."), ("Ada, kitap", "Yalnız envanter; okuma olgusunu vermez.")],
                ("Bileşenlerle birleşme biçimini birlikte belirtmek.", "Nesne listesini dünya betimi saymak.", "Olgu, öğelerin belirli düzenlenişini içerir."),
            ),
            _section(
                "Atomik önerme ve atomik olgu",
                "Atomik önerme temel bir durumun varlığını temsil eder; doğruysa ilgili olgu vardır, yanlışsa temsil edilen durum gerçekleşmemiştir. `Atomik` burada analizin rolüdür, cümlenin kısa olması değildir.",
                "Bileşik önermeyi temel doğruluk taşıyıcılarına ayırırken.",
                "p ↔ bir temel durumun varlığı/yokluğu",
                "Bir önermenin atomik sayılması dilde kaç kelime taşıdığına değil çözümlemede daha basit doğruluk-fonksiyonlu bileşene ayrılıp ayrılmadığına bağlıdır.",
                "Kısa her cümleyi atomik; uzun her cümleyi moleküler sayma.",
                [("F(a)", "Ders notasyonunda atomik yapı örneği."), ("¬F(a)", "Atomik önerme üzerine doğruluk işlemi içerir.")],
                ("Ana mantıksal işleci sınamak.", "Kelime sayısını ölçmek.", "Atomiklik sözdizimsel ve analitik roldür."),
            ),
            _section(
                "Moleküler önerme ve doğruluk işlemi",
                "`p∧q`, `¬p` ve benzeri önermelerin değeri bileşenlerinin değerlerinden hesaplanır. Bu teknik zemin, `Tractatus`ta önermelerin doğruluk işlemleri olarak ele alınmasına hazırlık sağlar.",
                "Bileşik önermenin atomik tabanla ilişkisini kurarken.",
                "p, q ⇒ ¬p, p∧q, p∨q, p→q",
                "Doğruluk-fonksiyonlu bileşim, bileşik önermenin ek gizli olgu adı taşımasını gerektirmez.",
                "Her bağlacın dünyada ayrı bir nesneye gönderdiğini varsayma.",
                [("p∧q", "İki bileşen de doğruysa doğru."), ("Bağlaç nesnesi", "Doğruluk işlevini nesneye çevirmek gereksizdir.")],
                ("Bileşik değeri atomik değerlerden izlemek.", "`ve` için dünyada üçüncü nesne aramak.", "Bağlaçlar doğruluk işlemi rolünde okunur."),
            ),
            _section(
                "Mantıksal atom fiziksel parçacık değildir",
                "Mantıksal atomculuğun `atom`u, çözümlemede bağımsız temel rolü anlatır. Bunun elektron, atom veya en küçük fiziksel parça olması gerekmez; Russell ve Wittgenstein'da atomların statüsü ayrıca tartışmalıdır.",
                "Mantıksal ve bilimsel açıklama düzeylerini ayırırken.",
                "analiz temeli ≠ fiziksel küçüklük",
                "Mantıksal basitlik, mikroskopla ölçülen boyut değil bir temsil/çözümleme ilişkisidir.",
                "Mantıksal atomculuğu maddenin atomlardan oluştuğu fizik teorisi diye tanımlama.",
                [("Basit nesne", "Analizin temel bileşeni olarak düşünülür."), ("Elektron", "Fiziksel teoriye ait olması onu otomatik mantıksal atom yapmaz.")],
                ("Hangi çözümlemede temel olduğunu açıklamak.", "En küçük fiziksel parçayı seçmek.", "Felsefi `atom` yöntemsel ve mantıksal bir roldür."),
            ),
            _section(
                "Russell ile erken Wittgenstein: ortaklık ve ayrılık",
                "Her ikisi de görünür dilbilgisinin yanıltıcılığı, çözümleme ve temel olgu/önerme yapısıyla ilgilenir. Fakat epistemoloji, tanışıklık, mantıksal biçimin söylenebilirliği ve çözümlemenin sonucu konusunda aynı doktrini paylaşmazlar.",
                "`Tractatus`a geçerken tarihsel etkiyi özdeşliğe dönüştürmemek için.",
                "ortak problem ≠ aynı kuram",
                "Russell'ın mantıksal atomculuğu kendi dönemleri içinde değişir; Wittgenstein'ın sistemi de Russell'ın basit devamı değildir.",
                "İki filozofu tek bir `analitik felsefe görüşü` içinde ayrıntısız birleştirme.",
                [("Ortaklık", "Mantıksal biçim ve çözümleme merkezi sorundur."), ("Ayrılık", "Wittgenstein mantıksal biçimin temsil edilemeyip gösterildiği yönünde özgül bir sınır geliştirir.")],
                ("Her benzerliğe en az bir ayrılık eşlemek.", "Etkilenmeyi doktrinel kopya saymak.", "Köprü ancak farklar korunursa okuma sağlar."),
            ),
        ],
        [
            _worked("Mantıksal çözümleme doğruluk koşulunu açar", "Yalnız üslup düzeltmesi veya özet değildir.", "Yöntem"),
            _worked("Bir cümleyi kısaltmak onu mantıksal olarak çözümlemektir", "Yapı ve doğruluk koşulu açılmamış olabilir.", "Özet hatası", "bad"),
            _worked("Nesnelerin varlığı, aralarındaki her olguyu garanti etmez", "Düzenleniş ve bağıntı ayrıca gerekir.", "Olgu"),
            _worked("Olgu yalnız bir nesnedir", "Olgu, öğelerin belirli biçimde bulunmasını içerir.", "Kategori hatası", "bad"),
            _worked("F(a) atomik önerme örneğidir", "Ana doğruluk-fonksiyonlu bağlaç taşımayan temel ders biçimidir.", "Atomik"),
            _worked("¬F(a) aynı anlamda atomiktir", "Olumsuzlama bir doğruluk işlemi ekler.", "İşlem var", "bad"),
            _worked("p∧q değeri p ve q değerlerinden belirlenir", "Bileşik önerme doğruluk-fonksiyonludur.", "Moleküler"),
            _worked("`ve` dünyadaki üçüncü bir nesnenin adıdır", "Mantıksal işleci ontolojik nesneye çevirir.", "Bağlaç hatası", "bad"),
            _worked("Mantıksal atom, çözümlemenin temelidir", "Fiziksel boyut değil analitik rol belirtilir.", "Atom"),
            _worked("Mantıksal atomculuk, antik atom fiziğinin aynısıdır", "Mantıksal ve fiziksel açıklama düzeylerini karıştırır.", "Fizikçilik", "bad"),
            _worked("Russell ve Wittgenstein çözümleme sorununu paylaşır", "Ortak tarihsel problem alanını doğru belirler.", "Ortaklık"),
            _worked("Russell ile Wittgenstein aynı kuramı savunur", "Mantıksal biçim, epistemoloji ve yöntem ayrımlarını siler.", "Özdeşleştirme", "bad"),
        ],
        [
            "Çözümlemeyi özetleme veya sözlük tanımı sanmak.",
            "Olgu ile nesne listesini aynı saymak.",
            "Atomikliği cümlenin kelime sayısıyla ölçmek.",
            "Bağlaçları dünyadaki ayrı nesneler gibi yorumlamak.",
            "Mantıksal atomu fiziksel parçacığa indirgemek.",
            "Russell ve erken Wittgenstein'ın ortak problemlerini tek kuram saymak.",
        ],
        _practice(
            [
                ("Mantıksal çözümlemenin hedefi nedir?", ["Cümleyi kısaltmak", "Doğruluk koşulu taşıyan yapıyı açmak", "Yazarı özetlemek", "Sözcükleri sıralamak"], "B", "Yüzeyden mantıksal biçime geçer.", "Temel"),
                ("Olgu nesneden nasıl ayrılır?", ["Daima daha küçüktür", "Nesnelerin belirli düzenlenişini içerir", "Yalnız sözcüktür", "Doğruluk değeridir"], "B", "Olgu bileşenlerin nasıl bulunduğunu taşır.", "Temel"),
                ("Aynı nesneler ne zaman farklı durum oluşturabilir?", ["Asla", "Farklı bağıntı ve düzende", "Adları değişince yalnız", "Renkleri aynıysa"], "B", "Düzenleniş dünya durumunu değiştirir.", "Orta"),
                ("Atomik önerme neyle belirlenir?", ["Kelime sayısıyla", "Analizde temel doğruluk taşıyıcı rolüyle", "Yazı boyuyla", "Fiziksel konuyla"], "B", "Atomiklik analitik/sözdizimsel roldür.", "Temel"),
                ("¬p neden moleküler yapı sayılır?", ["p uzundur", "Doğruluk işlemi içerir", "p yanlıştır", "Negasyon nesnedir"], "B", "Olumsuzlama atomik değere işlem uygular.", "Temel"),
                ("p∧q nasıl değerlendirilir?", ["Üçüncü nesneyle", "p ve q doğruluk değerleriyle", "Sözcük sırasıyla", "Konuşanın duygusuyla"], "B", "Doğruluk-fonksiyonlu bileşimdir.", "Temel"),
                ("Mantıksal atom ne değildir?", ["Analiz temeli", "Zorunlu olarak fiziksel parçacık", "Temel rol", "Felsefi kavram"], "B", "Fiziksel küçüklük zorunlu değildir.", "Orta"),
                ("Russell ve erken Wittgenstein'ın ortak sorunu nedir?", ["Yalnız etik", "Mantıksal biçim ve çözümleme", "Yalnız psikoloji", "Deneysel fizik"], "B", "Yüzeyin altındaki temsil yapısı merkezidir.", "Temel"),
                ("Ortak sorun neden aynı kuram demek değildir?", ["Farklı dilde yazdıkları için", "Epistemoloji ve mantıksal biçim görüşleri ayrılabilir", "Biri mantık bilmediği için", "Tarihleri aynı olmadığı için"], "B", "Benzer hedef, doktrinel özdeşlik sağlamaz.", "İleri"),
                ("Betimleme kuramı hangi yönteme örnektir?", ["Fizik deneyi", "Mantıksal çözümleme", "Özel dil", "Davranışçılık"], "B", "Yüzeysel ad görünüşünü niceliksel yapıya açar.", "Orta"),
                ("`Dünya şeylerin listesidir` okumasının eksiği nedir?", ["Nesne yoktur", "Düzenleniş ve olguları siler", "Liste kısa kalır", "Adları artırır"], "B", "Aynı öğelerin farklı birleşimi farklı durumdur.", "İleri"),
                ("G45'in temel sınır ilkesi hangisidir?", ["Etkilenme = özdeş kuram", "Ortak problem ile doktrin ayrılır", "Atom = elektron", "Çözümleme = özet"], "B", "Tarihsel köprü farkları korur.", "İleri"),
            ]
        ),
        {
            "prompt": "`Ada masadaki tek kitabı okuyor ve Bora okumuyor` cümlesini mantıksal çözümleme, atomik taban ve moleküler birleşim katmanlarına ayır.",
            "starter": "Önce betimlemenin varlık/biriciklik yapısını, sonra Ada ve Bora için okuma atomlarını, en son bağlaç ve olumsuzlamayı göster.",
            "checks": ["Betimleme çözülmüş", "Atomik önermeler ayrı", "Bağlaç/olumsuzlama işlemleri açık", "Olgu/nesne ayrımı korunmuş"],
            "solution": "Tek kitap için ∃x(Kx∧Mx∧∀y((Ky∧My)→y=x)∧R(a,x)∧¬R(b,x)) yazılabilir. Kx, Mx, R(a,x), R(b,x) atomik yapı örnekleridir; ∧ ve ¬ bunları bileştirir. Ada, Bora ve kitap nesne adaylarıdır; okuma bağıntısındaki düzenleniş olgusal yapıyı verir. Modern FOL çözümlemesi tarihsel atomculuk kuramının tamamı değildir.",
        },
        [
            _production_task(
                "Dört karmaşık cümleyi yüzey, mantıksal çözümleme, atomik taban ve doğruluk işlemleri katmanlarında haritala.",
                ["Her katman ayrı", "En az bir betimleme", "Olgu/nesne ayrımı", "Kayıp raporu"],
                "Bir cümlede aynı nesnelerle iki farklı olası durum karşılaştırılsın.",
                "Cümle türleri",
                ["betimleme", "olumsuz bağıntı", "koşullu", "iki farklı kapsam"],
            ),
            _production_task(
                "Russell ve erken Wittgenstein için ortaklık-ayrılık matrisi üret.",
                ["En az üç ortak problem", "En az üç ayrılık", "Her satırda kaynak konumu", "Fiziksel atom yanılgısı dışlanmış"],
                "`İkisi de mantıksal atomcudur` cümlesinin neden yetersiz olduğunu sonuç paragrafında açıkla.",
                "Karşılaştırma eksenleri",
                ["çözümleme", "olgu", "önerme", "mantıksal biçim", "epistemoloji", "söyleme/gösterme"],
            ),
        ],
        [
            "Yeni bir cümlenin yüzey ve mantıksal çözümleme katmanlarını ayırır.",
            "Olgu, nesne, atomik önerme ve moleküler önermeyi doğru kategorilerde kullanır.",
            "Mantıksal atomu fiziksel parçacığa indirgeyen açıklamayı onarır.",
            "Russell-erken Wittgenstein karşılaştırmasında ortaklık ve ayrılığı kaynaklı savunur.",
        ],
        [
            "Mantıksal çözümleme, sıradan özetten nasıl ayrılır?",
            "Olgu neden yalnız nesneler listesi değildir?",
            "Russell ile erken Wittgenstein'ın ortak problemi neden aynı kuramı paylaştıklarını göstermez?",
        ],
        "G46'da `Tractatus`un 1-4 numaralı ana dalları dünya, olgu, resim, düşünce ve önerme ilişkisi içinde yakın okunacak.",
        ["sep-logical-atomism", "sep-wittgenstein", "wittgenstein-tractatus"],
        "Mantıksal atomculuk fizik teorisi olarak sunulmaz. Russell ve Wittgenstein'ın aynı terimleri kullanması aynı epistemoloji, ontoloji veya yöntem sonucuna bağlanmaz.",
        ["The Philosophy of Logical Atomism", "Tractatus Logico-Philosophicus 1-4"],
    )
    lesson["reading_fixtures"] = [
        _reading_fixture(
            "g45-russell-analysis",
            "sep-logical-atomism",
            "Russell, The Philosophy of Logical Atomism (1918), lectures I-II",
            "Çözümlemenin karmaşık görünüşten temel önerme ve olgulara ilerleyen yöntemsel rolü.",
            ["çözümleme / özet", "olgu / nesne", "atomik / fiziksel"],
            ["mantıksal atom elektrondur", "çözümleme yalnız daha kısa cümledir"],
            "Bir betimleme çözümlemesini atomculuğun yöntem hedefleriyle ilişkilendir.",
            "Russell'ın 1918 dersleri bütün dönemlerindeki değişimleri tek biçime indirgemez.",
        ),
        _reading_fixture(
            "g45-tlp-world-fact",
            "wittgenstein-tractatus",
            "Tractatus 1-2.063",
            "Dünya, olgu, durum ve nesne arasındaki numaralı bağımlılık.",
            ["dünya / nesne toplamı", "olgu / durum", "nesne / birleşme"],
            ["dünya fiziksel eşya listesidir", "olgu doğru cümlenin başka adıdır"],
            "1, 1.1, 2 ve 2.01 önermelerini ebeveyn-alt önerme ağacı olarak haritala.",
            "Açılış önermeleri tek başına kitabın etik ve yöntemsel sonunu açıklamaz.",
        ),
        _reading_fixture(
            "g45-atomic-comparison",
            "sep-logical-atomism",
            "Logical Atomism, Russell/Wittgenstein karşılaştırma bölümleri",
            "Ortak terminoloji altında farklı mantıksal ve epistemolojik taahhütler.",
            ["etki / özdeşlik", "ortak problem / ortak doktrin", "atomik önerme / atomik olgu"],
            ["iki yazarın kuramı aynıdır", "tek fark kullandıkları sembollerdir"],
            "Üç ortaklık ve üç ayrılığı aynı problem eksenlerinde eşleştir.",
            "Karşılaştırma, her iki düşünürün iç dönemsel değişimlerini tüketmez.",
        ),
    ]
    lesson["comparison_fixtures"] = [
        _comparison_fixture(
            "g45-russell-wittgenstein",
            "Russell'ın mantıksal atomculuğu",
            "Erken Wittgenstein'ın Tractatus projesi",
            "Dilsel yüzeyin altında önerme, olgu ve mantıksal biçim ilişkisini açıklamak.",
            ["Russell'da tanışıklık ve epistemik çözümleme belirgin bir rol taşır.", "Wittgenstein mantıksal biçimin söylenmesinden çok gösterilmesi sınırını geliştirir.", "Her ikisinde de ortak sözcüklerin işlevi bağlama göre ayrıca okunmalıdır."],
            "Ortak terimleri satır, doktrinel farkları sütun yapan kanıtlı bir matris kur.",
        ),
    ]
    lesson["primary_text_locators"] = [
        "The Philosophy of Logical Atomism (1918), lectures I-II",
        "Tractatus Logico-Philosophicus 1-2.063",
    ]
    return lesson


STAGE_G_CANDIDATE_LESSONS = [
    _candidate_g42(),
    _candidate_g43(),
    _candidate_g44(),
    _candidate_g45(),
]

STAGE_G_CANDIDATE_MAP = {
    lesson["slug"]: lesson for lesson in STAGE_G_CANDIDATE_LESSONS
}
