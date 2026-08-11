"""Release-candidate content for Phase 3, Stage B of the logic course.

Stage B is being built one lesson at a time. Candidate lessons stay outside
the learner-facing course until the complete stage and its migration plan pass
the release gates documented in ``docs/logic_phase3_stage_b_spec.md``.
"""

from .logic_phase3_stage_a import (
    _lesson,
    _practice,
    _production_task,
    _section,
    _worked,
)


STAGE_B_SOURCE_REFERENCES = {
    "forallx-first-symbolization": {
        "title": "forall x: Calgary - First symbolization",
        "url": "https://forallx.openlogicproject.org/html/Ch4.html",
    },
    "forallx-connectives": {
        "title": "forall x: Calgary - Connectives",
        "url": "https://forallx.openlogicproject.org/html/Ch5.html",
    },
    "forallx-tfl-sentences": {
        "title": "forall x: Calgary - Sentences of TFL",
        "url": "https://forallx.openlogicproject.org/html/Ch6.html",
    },
    "forallx-ambiguity": {
        "title": "forall x: Calgary - Ambiguity",
        "url": "https://forallx.openlogicproject.org/html/Ch7.html",
    },
    "mit-logic-sequence": {
        "title": "MIT OpenCourseWare Logic I - Calendar",
        "url": "https://ocw.mit.edu/courses/24-241-logic-i-fall-2009/pages/calendar",
    },
    "mit-logic-study-guide": {
        "title": "MIT OpenCourseWare Logic I - Final exam study guide",
        "url": "https://www.ocw.mit.edu/courses/24-241-logic-i-fall-2009/56f43731bfb2513d7b46afa10236e072_MIT24_241F09_final_study_guide.pdf",
    },
}


def _candidate_b7():
    lesson = _lesson(
        "B7",
        "ders-17-sembollestirmeye-giris",
        "Atomik TFL Cümleleri ve Sembol Anahtarı",
        "Bir cümle harfini kişi veya sözcük kısaltması olarak değil, belirli bir çalışma anahtarındaki tam atomik bildirim için kullanır.",
        "TFL dili ve sembol anahtarı",
        30,
        [
            "ders-1-onerme-nedir",
            "ders-9-karsi-ornek-sema-ve-curutme-teknikleri",
            "ders-kullanim-anma-ve-dil-duzeyleri",
        ],
        [
            "tfl.atomic_identify",
            "tfl.key_construct",
            "tfl.abstraction_explain",
        ],
        [
            "TFL açısından atomik bırakılacak tam bildirimleri kişi adlarından, tek sözcüklerden ve cümle parçalarından ayırmak.",
            "Her cümle harfine tek bir tam bildirim bağlayan, kendi çalışma bağlamı içinde tutarlı bir sembol anahtarı kurmak.",
            "Cümle harfinin doğal dildeki iç yapıyı görünmez kıldığını ve anahtarın başka bir problemde yeniden kurulabileceğini açıklamak.",
        ],
        [
            (
                "TFL",
                "Doğal dil bildiriminin yalnız doğruluk işlevsel yapısını izlemek için kullanılan önermeler mantığı dili.",
            ),
            (
                "Atomik TFL cümlesi",
                "TFL'nin bu aşamada izleyeceği cümleler arası yapı bakımından daha fazla ayrıştırılmadan bırakılan temel cümle.",
            ),
            (
                "Cümle harfi",
                "Belirli bir sembol anahtarında tam bir atomik bildirimin yerini tutan büyük harf.",
            ),
            (
                "Sembol anahtarı",
                "Cümle harfleri ile onların bu problemde temsil ettiği tam bildirimleri eşleyen geçici liste.",
            ),
            (
                "Soyutlama",
                "İncelenen mantıksal yapıyı koruyup o aşamada izlenmeyen dilsel ayrıntıları dışarıda bırakma işlemi.",
            ),
        ],
        [
            _section(
                "TFL neyi görünür kılar?",
                "TFL bir cümlenin konusunu veya bütün anlam inceliklerini kopyalamaz; bu aşamada bildirimin cümleler arası doğruluk işlevsel yapıda oynadığı rolü izler.",
                "Doğal dilden biçimsel dile geçerken hangi ayrıntının korunup hangisinin geçici olarak dışarıda kaldığını belirlerken.",
                "Önce tam bildirimleri bul; sonra yalnız bu problem için harflerle eşle.",
                "Aynı cümle harfi, içeriği ne kadar zengin olursa olsun bir atomik TFL cümlesi olarak davranır; doğal dildeki özne, yüklem, zaman ve ilişki yapısı harfin içinde görünmez olur.",
                "Soyutlamayı kusursuz çeviri sanma. Bir harf verdiğinde doğal dil cümlesinin iç yapısının bir kısmını bilinçli olarak kaybedersin.",
                [
                    (
                        "A: Deniz Ankara'dadır.",
                        "Sağ taraf tek başına doğru ya da yanlış olabilen tam bildirimdir; özne-yüklem yapısı TFL harfinin içinde görünmez kalır.",
                    ),
                    (
                        "B: Atölye bugün açıktır.",
                        "Zaman ve konu içeriği anahtarda korunur; harfin kendisi bu içeriği çözümlemez.",
                    ),
                ],
                (
                    "TFL'nin izlediği yapı için yeterli atomik bildirimleri ayrı harflerle göstermek.",
                    "Bir cümlenin bütün doğal dil anlamının harfin içinde eksiksiz korunduğunu varsaymak.",
                    "Cümle harfi bir ses kaydı değil, belirli bir mantıksal çözümleme amacı için kullanılan soyutlamadır.",
                ),
            ),
            _section(
                "Atomiklik doğal dilde mutlak basitlik değildir",
                "Bir bildirim, doğal dilde sözcüklerden ve ilişkilerden oluşsa da TFL'nin izleyeceği cümleler arası yapı bakımından atomik bırakılabilir.",
                "Yüzeyde görülen her 've' sözcüğünün iki tam bildirimi birleştirip birleştirmediğini sınarken.",
                "Bölme testi: İfadenin iki yanında tek başına doğru ya da yanlış olabilen iki tam bildirim var mı?",
                "'Deniz ve Ece kardeştir' tek bir ilişki bildirir. Buna karşılık 'Deniz geldi ve Ece kaldı' iki ayrı tam bildirim içerir.",
                "Sözcük sayısını veya yalnız yüzeydeki 've'yi ölçüt yapma; tam bildirim sınırını ve amaçlanan çözümleme düzeyini gerekçelendir.",
                [
                    (
                        "C: Deniz ve Ece kardeştir.",
                        "Yüzeyde 've' bulunsa da iki tam cümle bağlanmaz; TFL açısından tek atomik bildirim olarak bırakılır.",
                    ),
                    (
                        "Deniz geldi ve Ece kaldı.",
                        "'Deniz geldi' ve 'Ece kaldı' ayrı ayrı değerlendirilebilir iki tam bildirimdir; anahtarda ayrı harfler almalıdır.",
                    ),
                    (
                        "Deniz ve Ece geldi.",
                        "Bağlamda 'Deniz geldi; Ece geldi' diye açılabiliyorsa iki atomik bileşen gerekir. Yüzey benzerliği tek başına karar verdirmez.",
                    ),
                ],
                (
                    "Tam bildirim sınırını yeniden ifade ederek atomik bileşenleri bulmak.",
                    "İçinde 've' geçen her ifadeyi mekanik olarak ikiye bölmek.",
                    "'Ve' kişi adlarını, yüklemleri veya iki tam bildirimi bağlayabilir; yalnız son durumda TFL'nin cümleler arası yapısı açılır.",
                ),
            ),
            _section(
                "Sembol anahtarı yerel ve tutarlı bir sözleşmedir",
                "Bir sembol anahtarı, harflerin yalnız o problemde hangi tam bildirimleri temsil ettiğini söyler. Aynı harf başka bir problemde yeni bir anlam alabilir.",
                "Bir metindeki atomik bildirimleri kaydetmeden, geri okumadan ve çözümü denetlemeden önce.",
                "Bir anahtar içinde: bir harf, bir tam bildirim; aynı bildirim, tutarlı tek harf.",
                "Anahtar sağdan sola da okunabilmelidir: harfi gören kişi hangi tam bildirime dönmesi gerektiğini tereddütsüz bulmalıdır.",
                "Harfi kişi adının baş harfi sanma; aynı harfi aynı anahtar içinde iki anlama verme ve gereksiz yere iki harfle aynı bildirimi tekrar etme.",
                [
                    (
                        "Birinci problemde A: Atölye açıktır.",
                        "A harfinin anlamı bu anahtarın sözleşmesidir.",
                    ),
                    (
                        "İkinci problemde A: Müze kapalıdır.",
                        "Yeni ve ayrı bir anahtarda A yeniden kullanılabilir; önceki problemdeki anlamını kalıcı olarak taşımaz.",
                    ),
                    (
                        "D: Deniz",
                        "Geçersiz anahtardır; sağ taraf kişi adı, tam bildirim değildir.",
                    ),
                    (
                        "G: geldi",
                        "Geçersiz anahtardır; kimin geldiğini bildirmeyen bir cümle parçasıdır.",
                    ),
                ],
                (
                    "Anahtarın her satırını tam bildirim ve tek anlam bakımından geri okumak.",
                    "Harfleri bütün ders boyunca değişmeyen evrensel kısaltmalar gibi kullanmak.",
                    "Sembol anahtarı geçici ve bağlama bağlıdır; tutarlılık aynı problem içinde aranır.",
                ),
            ),
        ],
        [
            _worked(
                "A: Atölye bugün açıktır.",
                "Anahtarın sağ tarafı tek başına doğru ya da yanlış olabilen tam bildirimdir.",
                "Geçerli anahtar",
            ),
            _worked(
                "D: Deniz",
                "Kişi adı tam bildirim değildir; cümle harfi nesnenin veya kişinin adı yerine kullanılamaz.",
                "Kategori hatası",
                "bad",
            ),
            _worked(
                "G: geldi",
                "Yüklem parçası, kimin geldiğini söylemediği için tek başına değerlendirilemez.",
                "Eksik bildirim",
                "bad",
            ),
            _worked(
                "C: Deniz ve Ece kardeştir.",
                "Yüzeydeki 've' iki tam bildirimi değil, ilişki içindeki iki kişiyi bağlar; cümle TFL açısından atomik bırakılabilir.",
                "Sınır örneği",
            ),
            _worked(
                "Deniz geldi ve Ece kaldı.",
                "Cümle, ayrı ayrı doğru ya da yanlış olabilen iki tam bildirime ayrılır; her biri anahtarda ayrı harf alır.",
                "İki bileşen",
            ),
            _worked(
                "A harfi yeni bir problemde başka bir tam bildirimi temsil edebilir.",
                "Harflerin anlamı sembol anahtarıyla geçici olarak belirlenir.",
                "Yerel anahtar",
            ),
        ],
        [
            "Cümle harfini kişi, nesne, kavram veya tek sözcük adı gibi kullanmak.",
            "Bağlaçlı bütün bir metni tek harfle kapatıp izlenmesi gereken iç yapıyı silmek.",
            "Yüzeydeki her 've' sözcüğünü iki atomik TFL cümlesinin sınırı sanmak.",
            "Aynı sembol anahtarı içinde bir harfe iki farklı tam bildirim vermek.",
            "Bir harfin başka problemler için de kalıcı ve değişmez bir anlam taşıdığını varsaymak.",
        ],
        _practice(
            [
                (
                    "Hangisi sembol anahtarında bir cümle harfinin karşısına yazılabilir?",
                    ["Deniz", "geldi", "Deniz geldi.", "mavi"],
                    "Deniz geldi.",
                    "Yalnız bu seçenek tek başına doğru ya da yanlış olabilen tam bildirimdir.",
                    "Temel",
                ),
                (
                    "'A: Ankara' satırındaki temel sorun nedir?",
                    [
                        "A harfi büyük yazılmıştır",
                        "Sağ taraf kişi ya da yer adı olup tam bildirim değildir",
                        "Ankara hakkında konuşulamaz",
                        "Her anahtarda en az iki harf gerekir",
                    ],
                    "Sağ taraf kişi ya da yer adı olup tam bildirim değildir",
                    "Bir cümle harfi tek bir terimi değil, doğru ya da yanlış olabilen tam bildirimi temsil eder.",
                    "Temel",
                ),
                (
                    "'Deniz ve Ece kardeştir' ifadesi neden TFL açısından atomik bırakılabilir?",
                    [
                        "Çünkü bütün kısa cümleler atomiktir",
                        "Çünkü iki tam bildirimi değil, tek bir kardeşlik ilişkisini ileri sürer",
                        "Çünkü 've' mantıkta hiç kullanılmaz",
                        "Çünkü kişi adları her zaman tek harf alır",
                    ],
                    "Çünkü iki tam bildirimi değil, tek bir kardeşlik ilişkisini ileri sürer",
                    "Yüzeydeki 've', burada iki tam cümle arasında sınır kurmaz.",
                    "Orta",
                ),
                (
                    "'Deniz geldi ve Ece kaldı' ifadesi için en dikkatli ilk işlem hangisidir?",
                    [
                        "Bütün cümleye tek harf vermek",
                        "Deniz ve Ece adlarına harf vermek",
                        "İki tam bildirimi ayırıp anahtarda ayrı satırlar açmak",
                        "Yalnız 'geldi' sözcüğünü anahtara almak",
                    ],
                    "İki tam bildirimi ayırıp anahtarda ayrı satırlar açmak",
                    "Her iki parça tek başına doğruluk değerlendirmesine açıktır.",
                    "Orta",
                ),
                (
                    "Birinci problemde 'A: Atölye açıktır' kullanıldı. İkinci problemde A harfi kullanılabilir mi?",
                    [
                        "Hayır, A sonsuza kadar atölye anlamına gelir",
                        "Evet, yeni sembol anahtarı A için yeni bir tam bildirim belirleyebilir",
                        "Yalnız kişi adı için kullanılabilir",
                        "Yalnız ilk problem silinirse kullanılabilir",
                    ],
                    "Evet, yeni sembol anahtarı A için yeni bir tam bildirim belirleyebilir",
                    "Harflerin anlamı yerel ve geçici sembol anahtarıyla belirlenir.",
                    "Orta",
                ),
                (
                    "Aynı anahtar içinde 'A: Atölye açıktır' ve 'A: Atölye sessizdir' yazmak neden hatalıdır?",
                    [
                        "İki cümle de atölye hakkındadır",
                        "Aynı harfe iki farklı tam bildirim verildiği için geri okuma belirsizleşir",
                        "Sessizlik hakkında cümle kurulamaz",
                        "A harfi yalnız olumsuz cümlelere ayrılır",
                    ],
                    "Aynı harfe iki farklı tam bildirim verildiği için geri okuma belirsizleşir",
                    "Bir anahtar içinde bir harf tek bir anlam taşımalıdır.",
                    "İleri",
                ),
                (
                    "Bir doğal dil cümlesini tek cümle harfiyle gösterdiğimizde ne kaybolabilir?",
                    [
                        "Harfin büyük yazılması",
                        "Cümlenin özne, yüklem, zaman ve ilişki gibi iç yapısı",
                        "Cümlenin doğru ya da yanlış olabilmesi",
                        "Sembol anahtarının varlığı",
                    ],
                    "Cümlenin özne, yüklem, zaman ve ilişki gibi iç yapısı",
                    "Cümle harfi bu ayrıntıları çözümlemez; yalnız seçilen mantıksal düzeyde yer tutar.",
                    "İleri",
                ),
                (
                    "'Deniz ve Ece geldi' ifadesiyle karşılaşınca en güvenilir yaklaşım hangisidir?",
                    [
                        "Yüzeyde 've' olduğu için her durumda tek atom saymak",
                        "Sözcük sayısı uzun olduğu için ikiye bölmek",
                        "İfadenin 'Deniz geldi; Ece geldi' diye iki tam bildirime açılıp açılmadığını sınamak",
                        "Kişi adlarını anahtarın sağ tarafına tek başına yazmak",
                    ],
                    "İfadenin 'Deniz geldi; Ece geldi' diye iki tam bildirime açılıp açılmadığını sınamak",
                    "Karar, yüzey sözcüğünden değil tam bildirim sınırından ve amaçlanan çözümleme düzeyinden gelir.",
                    "Zor",
                ),
            ],
        ),
        {
            "prompt": "Atölye duyurusundaki atomik TFL cümleleri için sembol anahtarını tamamla.",
            "starter": "A: Atölye bugün açıktır.\nB: Atölye ve galeri aynı binadadır.",
            "checks": [
                "Anahtarın her sağ tarafı tek başına doğru ya da yanlış olabilen tam bildirimdir",
                "Atölye ile galerinin aynı binada olması tek ilişki bildirimi olarak atomik bırakılmıştır",
                "Son cümledeki iki tam bildirim ayrı anahtar satırlarına alınmıştır",
                "Bir harf yalnız bir anlam taşır",
            ],
            "solution": "C: Galeri sessizdir.\nD: Giriş ücretsizdir. Böylece 'Galeri sessizdir ve giriş ücretsizdir' ifadesindeki iki tam bildirim ayrı kaydedilir; bu derste henüz aralarındaki yapı için bir formül kurulmaz.",
        },
        [
            _production_task(
                "Müze duyurusundaki bütün atomik TFL bileşenlerini çıkar ve yalnız bir sembol anahtarı kur. Her satırın neden tam bildirim olduğunu açıkla; henüz bileşik formül yazma.",
                [
                    "Her anahtar satırının sağ tarafını tek başına doğruluk değerlendirmesine açıklık bakımından denetle.",
                    "'Deniz ve Ece kardeştir' cümlesinin neden tek atomik bildirim olarak bırakıldığını gerekçelendir.",
                    "Dördüncü duyurudaki iki tam bildirimi ayrı anahtar satırlarına al.",
                    "Beşinci duyurunun içindeki iki atomik bildirimi çıkar; aralarındaki yapıyı bu derste formülleştirme.",
                    "Aynı harfleri başka anlamlarla kullanan iki satırlı, ayrı bir ikinci sembol anahtarı yazarak anahtarın geçici olduğunu göster.",
                ],
                "Kişi adı ile tam bildirim ayrımını, yüzeydeki 've' sınırını ve soyutlamada kaybolan iç yapıyı açıkça göster.",
                "Müze duyurusu",
                [
                    "Müze pazartesi kapalıdır.",
                    "Salı günü giriş ücretsizdir.",
                    "Deniz ve Ece kardeştir.",
                    "Biletler çevrim içi satılır ve gişede nakit kabul edilmez.",
                    "Müze açılırsa kafeterya hizmet verir.",
                ],
                "Son cümledeki ilişki daha sonraki derste kurulacaktır; burada yalnız içerdiği atomik tam bildirimleri anahtara geçir.",
            ),
        ],
        [
            "Sembol anahtarındaki her sağ taraf tek başına doğru ya da yanlış olabilen tam bildirimdir.",
            "Aynı anahtar içinde her harf tek anlam taşır ve geri okuma belirsiz değildir.",
            "En az bir yüzey 've'si, iki tam bildirimi bağlamadığı gerekçesiyle atomik cümlenin içinde bırakılır.",
            "Bağlaçlı bir duyurudaki ayrı tam bildirimler, iç yapı silinmeden farklı harflere bağlanır.",
            "Öğrenci TFL atomikliğinin doğal dilde mutlak basitlik olmadığını ve cümle harfinin hangi iç yapıyı görünmez kıldığını açıklar.",
            "Aynı harfin ayrı bir problemde yeni bir geçici anahtarla yeniden kullanılabileceğini gösterir.",
        ],
        [
            "Bir cümle harfi neden kişi, nesne veya tek sözcük adı değildir?",
            "Bir doğal dil bildirimini atomik TFL cümlesi olarak bıraktığımızda hangi iç yapı görünmez olur?",
            "Yüzeydeki 've' sözcüğü hangi durumda iki ayrı anahtar satırı gerektirir?",
        ],
        "Sonraki derste bu atomik TFL cümlelerinin olumsuzlama ve birleşim içindeki kapsamını kuracağız.",
        ["forallx-first-symbolization", "mit-logic-sequence"],
        "Atomiklik doğal dilde mutlak sözdizimsel basitlik iddiası değildir; TFL'nin bu aşamada izlediği doğruluk işlevsel cümle yapısına göre belirlenen çözümleme sınırıdır.",
        ["ders-17-sembollestirmeye-giris"],
    )

    lesson["reading_note"] = (
        "Bir harf seçmeden önce sağ tarafa yazacağın ifadenin kişi adı veya cümle parçası değil, tam bildirim olduğunu sesli geri oku."
    )
    lesson["symbol_set"] = ["A", "B", "C", "A₁"]
    lesson["proof_tools"] = [
        "Atomik bileşen ayırma",
        "Sembol anahtarı kurma",
        "Geri okuma denetimi",
    ]
    return lesson


def _candidate_b8():
    lesson = _lesson(
        "B8",
        "ders-18-degil-ve-ve-baglaclari",
        "Olumsuzlama ve Birleşim",
        "Olumsuzlamanın hangi TFL cümlesini etkilediğini ve birleşimin hangi iki tam cümleyi bir araya getirdiğini parantez ve geri çeviriyle açıklar.",
        "Bağlaç kurma ve kapsam",
        35,
        ["ders-17-sembollestirmeye-giris"],
        [
            "tfl.negation_scope",
            "tfl.conjunction_build",
            "tfl.component_recover",
        ],
        [
            "Bir doğal dil bildirimini 'öyle değildir ki' biçiminde yeniden yazarak olumsuzlamanın kapsamını belirlemek.",
            "İki tam TFL cümlesini birleşim içinde kurmak ve her birleşeni sembol anahtarına geri çevirmek.",
            "Yalnız bir bileşenin olumsuzlanmasıyla bütün birleşimin olumsuzlanmasını parantez ve doğal dil okumasıyla ayırmak.",
            "'Ama', 'fakat', 'oysa' ve sıralı 've' kullanımlarında TFL'nin kaybettiği karşıtlık, vurgu ve zaman bilgisini belirtmek.",
        ],
        [
            (
                "Olumsuzlama",
                "Bir TFL cümlesinin başına gelerek 'bu cümlenin ileri sürdüğü durum söz konusu değildir' okuması kuran tekli bağlaç.",
            ),
            (
                "Birleşim",
                "İki TFL cümlesini, ikisinin de ileri sürüldüğü bileşik cümlede bir araya getiren ikili bağlaç.",
            ),
            (
                "Birleşen",
                "Bir birleşimin solunda veya sağında bulunan tam TFL cümlesi.",
            ),
            (
                "Kapsam",
                "Bir bağlacın etkilediği tam TFL cümlesi veya cümle parçası.",
            ),
            (
                "Geri çeviri",
                "Kurulan TFL cümlesini sembol anahtarıyla yeniden doğal dile okuyarak amaçlanan yapıyı denetleme işlemi.",
            ),
        ],
        [
            _section(
                "Olumsuzlama sözcük avı değildir",
                "Olumsuzlama, bir sözcüğün görünüşünden değil, bildirimin 'öyle değildir ki ...' biçiminde doğru yeniden yazılabilmesinden belirlenir.",
                "'Değil', '-me/-ma', 'yok' veya olumsuz anlamlı bir sözcük içeren cümlenin hangi atomik bildirimi reddettiğini saptarken.",
                "A: Ada geldi. Buna göre ¬A: Ada'nın geldiği doğru değildir.",
                "¬ işareti kendisinden sonra gelen tam TFL cümlesini etkiler. Önce olumlu atomik anahtarı kurmak, sonra reddedilen yapıyı göstermek geri okumayı güvenli kılar.",
                "'Mutsuz' sözcüğünü her bağlamda 'mutlu değildir' diye çözme. Bir kişi ne mutlu ne mutsuz olabilir; sözlük anlamı ile cümle olumsuzluğu aynı işlem değildir.",
                [
                    (
                        "A: Ada geldi. / ¬A: Ada gelmedi.",
                        "İkinci cümle, birincinin ileri sürdüğü durumu açıkça reddeder.",
                    ),
                    (
                        "H: Deniz mutludur. / M: Deniz mutsuzdur.",
                        "M cümlesini otomatik olarak ¬H saymak yerine ayrı atomik bildirim bırakmak daha dikkatli olabilir.",
                    ),
                    (
                        "¬¬A",
                        "Önce A olumsuzlanır; dıştaki işaret ortaya çıkan bütün olumsuz cümleyi yeniden olumsuzlar. Bu aşamada yalnız yapıyı geri okuruz.",
                    ),
                ],
                (
                    "Önce olumlu atomik bildirimi anahtara yazıp hangi tam cümlenin reddedildiğini göstermek.",
                    "Olumsuz anlam çağrıştıran her sözcüğü mekanik olarak ¬ ile göstermek.",
                    "Sözcüksel karşıtlık, dereceli anlam ve cümle olumsuzluğu her zaman çakışmaz.",
                ),
            ),
            _section(
                "Birleşimin iki tarafı da tam TFL cümlesidir",
                "Birleşim işareti kişi adlarını, sıfatları veya cümle parçalarını değil, ayrı ayrı geri okunabilen iki tam TFL cümlesini birleştirir.",
                "Doğal dilde ortak özne, ortak yüklem veya zamir yüzünden bileşenlerden biri eksik görünürken.",
                "A: Ada geldi. S: Ada sessizdir. Birleşim: (A ∧ S).",
                "Doğal dil tekrardan kaçınabilir. TFL anahtarı ise her birleşeni tam bildirim hâline getirir ve eksiltilmiş özne ya da yüklemi geri koyar.",
                "B7 sınırını unutma: 'Ada ve Bora kardeştir' tek ilişki bildirimi olabilir; 'Ada ve Bora geldi' ise 'Ada geldi' ve 'Bora geldi' diye iki tam bildirime açılabilir.",
                [
                    (
                        "Ada geldi ve sessizce oturdu.",
                        "A: Ada geldi. O: Ada sessizce oturdu. Ortak özne ikinci tam bildirimde geri konur; yapı (A ∧ O) olur.",
                    ),
                    (
                        "Ada ve Bora geldi.",
                        "A: Ada geldi. B: Bora geldi. Cümle, amaçlanan okumada (A ∧ B) biçiminde kurulabilir.",
                    ),
                    (
                        "Ada ve Bora kardeştir.",
                        "K: Ada ve Bora kardeştir. İki tam kardeşlik bildirimi olmadığı için K atomik bırakılır.",
                    ),
                ],
                (
                    "Her birleşeni sembol anahtarında tam bildirim olarak geri kurmak.",
                    "'A ∧ sessiz' gibi bir cümle harfiyle yalın sıfatı birleştirmek.",
                    "Birleşimin her iki tarafında da tek başına TFL cümlesi olarak okunabilen bir yapı bulunmalıdır.",
                ),
            ),
            _section(
                "Kapsamı parantez ve geri çeviri belirler",
                "Aynı harf ve işaretler, olumsuzlamanın yalnız ilk birleşeni mi yoksa bütün birleşimi mi etkilediğine göre farklı cümleler kurar.",
                "'İkisi de değil', 'ikisi birden değil' ve 'biri değil ama diğeri' gibi birbirine benzeyen Türkçe yapıları ayırırken.",
                "(¬A ∧ B): A değil, B. / ¬(A ∧ B): A ile B'nin birlikte ileri sürülmesi doğru değildir.",
                "Parantez, dıştaki olumsuzlamanın nerede başlayıp bittiğini görünür kılar. Geri çeviri ise parantezin amaçlanan Türkçe okumayı koruyup korumadığını sınar.",
                "¬(A ∧ B), tek başına hangi tarafın gerçekleşmediğini söylemez. Onu '(¬A ∧ ¬B)' diye okumak kapsamı ve iddia gücünü değiştirir.",
                [
                    (
                        "Ada gelmedi ama Bora geldi.",
                        "A: Ada geldi. B: Bora geldi. Yapı (¬A ∧ B) olur; yalnız A olumsuzlanır.",
                    ),
                    (
                        "Ada ile Bora'nın ikisinin de geldiği doğru değildir.",
                        "Bütün birleşim reddedilir: ¬(A ∧ B). Bu cümle ikisinin de gelmediğini tek başına ileri sürmez.",
                    ),
                    (
                        "Ne Ada geldi ne Bora geldi.",
                        "Her iki atomik bildirim ayrı ayrı reddedilir ve sonra birleştirilir: (¬A ∧ ¬B).",
                    ),
                ],
                (
                    "Formülü sembol anahtarıyla tam Türkçe cümleye geri okuyup kapsamı kontrol etmek.",
                    "(¬A ∧ B), ¬(A ∧ B) ve (¬A ∧ ¬B) yapılarını aynı saymak.",
                    "Olumsuzlamanın kapsamı değiştiğinde doğal dilde ileri sürülen içerik de değişir.",
                ),
            ),
            _section(
                "TFL karşıtlık ve zaman sırasını korumaz",
                "'Ve', 'ama', 'fakat', 'oysa', 'hem ... hem ...' gibi ifadeler iki bildirimi birlikte ileri sürebilir; buna rağmen vurgu, şaşırtıcılık veya olay sırası TFL birleşiminde görünmez kalabilir.",
                "Doğal dildeki iki cümleyi aynı birleşim yapısına dönüştürürken kaybedilen bilgiyi raporlamak için.",
                "A ∧ B yalnız iki TFL cümlesinin birlikte ileri sürüldüğünü gösterir; ek söylem ilişkisini ayrıca kodlamaz.",
                "'Ada çalışkandır ama dağınıktır' ile 'Ada çalışkandır ve dağınıktır' aynı atomik bileşenlere indirgenebilir; 'ama'nın karşıtlık beklentisi kaybolur.",
                "'Ayağa kalktı ve konuştu' ifadesindeki zaman sırasını görmezden gelme. TFL birleşimi yalnız seçilen sınırlı yapıyı koruduğu için kaybı açıkça not et.",
                [
                    (
                        "Ada gençtir ama deneyimlidir.",
                        "G: Ada gençtir. D: Ada deneyimlidir. (G ∧ D) iki bildirimi korur, 'ama'nın beklenti karşıtlığını korumaz.",
                    ),
                    (
                        "Deniz ayağa kalktı ve konuştu.",
                        "K: Deniz ayağa kalktı. O: Deniz konuştu. (K ∧ O) olayların ikisini izler; anlatılan sırayı tek başına göstermez.",
                    ),
                ],
                (
                    "Formülün koruduğu bileşenlerle kaybettiği vurgu veya sıra bilgisini ayrı ayrı yazmak.",
                    "TFL birleşimini doğal dil cümlesinin eksiksiz eş anlamlısı saymak.",
                    "Sembolleştirme amaçlı bir soyutlamadır; hangi bilginin dışarıda kaldığı çözümün parçasıdır.",
                ),
            ),
        ],
        [
            _worked(
                "A: Ada geldi. / ¬A: Ada gelmedi.",
                "Olumsuzlama, anahtardaki tam A cümlesini reddeder.",
                "Tekli kapsam",
            ),
            _worked(
                "H: Deniz mutludur. / M: Deniz mutsuzdur.",
                "Mutsuzluk her bağlamda mutluluğun yalın cümle olumsuzluğuyla aynı anlamı taşımaz; iki atom ayrı tutulabilir.",
                "Sözcüksel sınır",
            ),
            _worked(
                "A: Ada geldi. S: Ada sessizdir. / (A ∧ S)",
                "Doğal dilde ortak özne bir kez yazılsa da iki birleşen de anahtarda tam bildirimdir.",
                "Birleşim",
            ),
            _worked(
                "Ada gelmedi ama Bora geldi. / (¬A ∧ B)",
                "Yalnız A olumsuzlanır; 'ama'nın karşıtlık tonu formülde görünmez kalır.",
                "Dar kapsam",
            ),
            _worked(
                "Ada ile Bora'nın ikisinin de geldiği doğru değildir. / ¬(A ∧ B)",
                "Olumsuzlama parantez içindeki bütün birleşimi etkiler; hangi kişinin gelmediği ayrıca söylenmez.",
                "Geniş kapsam",
            ),
            _worked(
                "Ne Ada geldi ne Bora geldi. / (¬A ∧ ¬B)",
                "İki atomik bildirim de ayrı ayrı olumsuzlanır, ardından birleştirilir.",
                "İki olumsuz",
            ),
            _worked(
                "Deniz ayağa kalktı ve konuştu. / (K ∧ O)",
                "İki olay korunur; doğal dilde ima edilen zaman sırası TFL birleşiminde korunmaz.",
                "Bilgi kaybı",
            ),
        ],
        [
            "Olumsuz anlamlı her sözcüğü otomatik olarak bir başka atomik cümlenin ¬ biçimi saymak.",
            "¬A ∧ B ile ¬(A ∧ B) arasındaki kapsam farkını parantezsiz bırakmak.",
            "'İkisi birden değil' ifadesini 'ikisi de değil' diye okuyup ¬(A ∧ B) yerine (¬A ∧ ¬B) yazmak.",
            "Birleşimin bir tarafına tam TFL cümlesi yerine kişi adı, sıfat veya yüklem parçası koymak.",
            "'Ama' ve 'fakat' karşıtlığının ya da sıralı 've'nin zaman bilgisinin TFL'de eksiksiz korunduğunu varsaymak.",
        ],
        _practice(
            [
                (
                    "A: Ada geldi. 'Ada gelmedi' için hangi yapı uygundur?",
                    ["A", "¬A", "(A ∧ A)", "¬¬A"],
                    "¬A",
                    "Olumsuzlama, A'nın ileri sürdüğü tam bildirimi reddeder.",
                    "Temel",
                ),
                (
                    "A: Ada geldi. S: Ada sessizdir. 'Ada geldi ve sessizdir' hangi yapıdır?",
                    ["¬A", "(A ∧ S)", "¬(A ∧ S)", "(¬A ∧ S)"],
                    "(A ∧ S)",
                    "Ortak özne anahtardaki iki tam bildirimde geri kurulur ve iki cümle birleştirilir.",
                    "Temel",
                ),
                (
                    "H: Deniz mutludur. 'Deniz mutsuzdur' cümlesini otomatik olarak ¬H yazmak neden sakıncalı olabilir?",
                    [
                        "Çünkü H yalnız geçmiş zaman içindir",
                        "Çünkü mutsuzluk ile mutlu olmama her bağlamda aynı içeriği taşımayabilir",
                        "Çünkü olumsuzlama yalnız kişi adlarına gelir",
                        "Çünkü her cümlede iki harf gerekir",
                    ],
                    "Çünkü mutsuzluk ile mutlu olmama her bağlamda aynı içeriği taşımayabilir",
                    "Sözcüksel karşıtlık, cümle olumsuzluğundan daha güçlü veya farklı bir anlam taşıyabilir.",
                    "Orta",
                ),
                (
                    "A: Ada geldi. B: Bora geldi. (¬A ∧ B) nasıl geri okunur?",
                    [
                        "Ada ile Bora'nın ikisinin de geldiği doğru değildir",
                        "Ada gelmedi ve Bora geldi",
                        "Ne Ada ne Bora geldi",
                        "Ada geldi ve Bora gelmedi",
                    ],
                    "Ada gelmedi ve Bora geldi",
                    "Olumsuzlama yalnız ilk birleşenin kapsamındadır.",
                    "Orta",
                ),
                (
                    "¬(A ∧ B) cümlesi tek başına neyi söylemez?",
                    [
                        "A ile B'nin birlikte ileri sürülmesinin reddedildiğini",
                        "En azından birleşimin bütününün kabul edilmediğini",
                        "A'nın da B'nin de ayrı ayrı gerçekleşmediğini",
                        "Olumsuzlamanın parantez içindeki yapıyı etkilediğini",
                    ],
                    "A'nın da B'nin de ayrı ayrı gerçekleşmediğini",
                    "Bütün birleşimi reddetmek, her iki birleşeni ayrı ayrı reddetmekten daha zayıf bir iddiadır.",
                    "İleri",
                ),
                (
                    "'Ne Ada geldi ne Bora geldi' için hangi yapı amaçlanan okumayı korur?",
                    ["(¬A ∧ ¬B)", "¬(A ∧ B)", "(¬A ∧ B)", "(A ∧ ¬B)"],
                    "(¬A ∧ ¬B)",
                    "Her iki atomik bildirim ayrı ayrı reddedilir ve sonra birleştirilir.",
                    "Orta",
                ),
                (
                    "'Ada gençtir ama deneyimlidir' cümlesi (G ∧ D) olduğunda hangi bilgi görünmez kalır?",
                    [
                        "Ada'nın genç olduğu",
                        "Ada'nın deneyimli olduğu",
                        "'Ama'nın kurduğu beklenti karşıtlığı",
                        "İki tam bildirim bulunduğu",
                    ],
                    "'Ama'nın kurduğu beklenti karşıtlığı",
                    "Birleşim iki bildirimi korur, karşıtlık tonunu ayrıca kodlamaz.",
                    "İleri",
                ),
                (
                    "'Deniz ayağa kalktı ve konuştu' cümlesi (K ∧ O) olduğunda hangi uyarı eklenmelidir?",
                    [
                        "Kişi adları kullanılamaz",
                        "TFL birleşimi doğal dilde ima edilen zaman sırasını tek başına korumaz",
                        "Her iki olay da formülden silinir",
                        "Birleşim yalnız aynı anda olan olaylar içindir",
                    ],
                    "TFL birleşimi doğal dilde ima edilen zaman sırasını tek başına korumaz",
                    "TFL burada iki olayın birlikte ileri sürülmesini izler, anlatı sırasını değil.",
                    "İleri",
                ),
                (
                    "Hangisi iki tam TFL cümlesini birleştirmez?",
                    [
                        "(A ∧ B)",
                        "(¬A ∧ B)",
                        "(A ∧ sessiz)",
                        "(A ∧ ¬B)",
                    ],
                    "(A ∧ sessiz)",
                    "'Sessiz' tek başına tam bildirim veya TFL cümlesi değildir.",
                    "Zor",
                ),
                (
                    "Kapsam hatasını bulmanın en güvenilir son denetimi hangisidir?",
                    [
                        "Formüldeki harfleri alfabetik sıralamak",
                        "Formülü sembol anahtarıyla tam doğal dil cümlesine geri çevirmek",
                        "Parantezleri görünmez saymak",
                        "Yalnız 'değil' sözcüğünü aramak",
                    ],
                    "Formülü sembol anahtarıyla tam doğal dil cümlesine geri çevirmek",
                    "Geri çeviri, olumsuzlamanın ve birleşimin amaçlanan parçaları etkileyip etkilemediğini gösterir.",
                    "Zor",
                ),
            ],
        ),
        {
            "prompt": "Verilen anahtarla üç cümlenin yapısını tamamla ve her birini geri oku.",
            "starter": "A: Ada geldi.\nB: Bora geldi.\nS: Ada sessizdir.\n1. Ada gelmedi ama Bora geldi: (___ ∧ ___)",
            "checks": [
                "Birleşimin her iki tarafı da tam TFL cümlesidir",
                "Yalnız ilk cümlede olumsuzlama dar kapsamlıdır",
                "Bütün birleşimin reddedildiği cümlede parantez korunmuştur",
                "'Ne ... ne ...' cümlesinde iki atom da ayrı ayrı olumsuzlanmıştır",
                "Her formül sembol anahtarıyla eksiksiz geri çevrilmiştir",
            ],
            "solution": "1. (¬A ∧ B): Ada gelmedi ve Bora geldi.\n2. ¬(A ∧ S): Ada'nın hem geldiği hem sessiz olduğu doğru değildir.\n3. (¬A ∧ ¬S): Ne Ada geldi ne de Ada sessizdi. 'Ama' karşıtlığı ilk formülde görünmez kalır.",
        },
        [
            _production_task(
                "Aynı sembol anahtarıyla dört farklı kapsam yapısını kur, her birini doğal dile geri çevir ve önceki yapıdan farkını tek cümleyle açıkla.",
                [
                    "Anahtarda A ve B'nin karşısına tam bildirimler yaz.",
                    "(¬A ∧ B), (A ∧ ¬B), ¬(A ∧ B) ve (¬A ∧ ¬B) yapılarının dördünü de kullan.",
                    "Her yapı için yalnız hangi atomun veya hangi bütünün olumsuzlandığını belirt.",
                    "En az bir doğal dil cümlesinde 'ama' ya da 'fakat' kullanıp formülde kaybolan karşıtlık bilgisini yaz.",
                    "Bütün formülleri sembol anahtarıyla geri okuyarak kapsamı denetle.",
                ],
                "'İkisi birden değil' ile 'ikisi de değil' ayrımını ve doğal dildeki karşıtlık kaybını açıkça göster.",
                "Arşiv durumu",
                [
                    "Arşiv açık değildir ama salon sessizdir.",
                    "Arşiv açıktır fakat salon sessiz değildir.",
                    "Arşivin açık ve salonun sessiz olduğu doğru değildir.",
                    "Ne arşiv açıktır ne salon sessizdir.",
                ],
                "A: Arşiv açıktır. B: Salon sessizdir. Anahtarı önce doğrula, ardından dört farklı kapsamı kur.",
            ),
        ],
        [
            "Öğrenci doğal dilde olumsuzlanan tam bildirimi belirler ve sözcüksel karşıtlığı otomatik cümle olumsuzluğu saymaz.",
            "Birleşimin her iki tarafını sembol anahtarında tam TFL cümlesine geri bağlar.",
            "(¬A ∧ B), ¬(A ∧ B) ve (¬A ∧ ¬B) yapılarını parantez ve geri çeviriyle birbirinden ayırır.",
            "'İkisi birden değil' ile 'ikisi de değil' ifadelerini farklı kapsamlarla doğru eşler.",
            "En az bir 'ama/fakat' örneğinde karşıtlık vurgusunun ve bir sıralı 've' örneğinde zaman bilgisinin kaybolduğunu açıklar.",
            "Kurulan her formülü doğal dile geri çevirip sembol anahtarındaki anlamla karşılaştırır.",
        ],
        [
            "¬(A ∧ B) ile (¬A ∧ ¬B) neden aynı doğal dil iddiasını taşımaz?",
            "'Ada gençtir ama deneyimlidir' cümlesi birleşim olarak kurulduğunda hangi bilgi kaybolur?",
            "Birleşimin iki tarafının da tam TFL cümlesi olduğunu nasıl denetlersin?",
        ],
        "Sonraki derste kapsayıcı ve dışlayıcı 'veya' okumalarını, bu derste kurduğumuz kapsam disipliniyle ayıracağız.",
        ["forallx-connectives"],
        "Bu ders bağlaçların doğruluk koşullarını tabloyla öğretmez. Öğrenci yalnız yapı kurar, kapsamı parantezle görünür kılar, doğal dile geri çevirir ve TFL soyutlamasının kaybettiği bilgiyi raporlar.",
        ["ders-18-degil-ve-ve-baglaclari"],
    )

    lesson["reading_note"] = (
        "Her formülü iki kez oku: önce bağlaçların hangi tam cümleyi etkilediğini söyle, sonra sembol anahtarıyla doğal dile dön."
    )
    lesson["symbol_set"] = ["A", "B", "¬", "∧", "(", ")"]
    lesson["proof_tools"] = [
        "Olumlu atomu geri kurma",
        "Kapsam parantezleme",
        "Birleşenleri ayırma",
        "Geri çeviri denetimi",
        "Bilgi kaybı notu",
    ]
    return lesson


def _candidate_b9():
    lesson = _lesson(
        "B9",
        "ders-19-veya-ve-ise",
        "Ayrık Bağlaç ve Dışlayıcı Okuma",
        "Doğal dildeki 'veya' kullanımının birlikte gerçekleşmeye izin verip vermediğini bağlamdan ayırır; kapsayıcı okumayı tek ayrık bağlaçla, dışlayıcı okumayı iki koşulu açıkça kurarak gösterir.",
        "Ayrık bağlaç ve okuma seçimi",
        30,
        ["ders-18-degil-ve-ve-baglaclari"],
        [
            "tfl.disjunction_build",
            "tfl.exclusive_or_construct",
            "tfl.neither_nor_scope",
        ],
        [
            "İki tam TFL cümlesinden kapsayıcı ayrık yapı kurmak ve onu 'en az biri' diye geri okumak.",
            "Doğal dil bağlamının dışlayıcılık gerektirip gerektirmediğini, yalnız 'ya ... ya ...' kalıbına güvenmeden gerekçelendirmek.",
            "Dışlayıcı okumayı 'en az biri' ve 'ikisi birlikte değil' bileşenlerini birleştirerek kurmak.",
            "'Ne ... ne ...' cümlesinde iki atomik bildirimi ayrı ayrı olumsuzlayıp kapsamı geri çeviriyle denetlemek.",
        ],
        [
            (
                "Ayrık bağlaç",
                "İki TFL cümlesinden en az birinin ileri sürüldüğü bileşik cümleyi kuran ikili bağlaç.",
            ),
            (
                "Ayrılan",
                "Bir ayrık yapının solunda veya sağında bulunan tam TFL cümlesi.",
            ),
            (
                "Kapsayıcı veya",
                "Seçeneklerden en az birinin gerçekleşmesini isteyen ve ikisinin birlikte gerçekleşmesine izin veren standart TFL okuması.",
            ),
            (
                "Dışlayıcı veya",
                "Seçeneklerden en az birinin, fakat ikisinin birlikte değil yalnız birinin gerçekleşmesini isteyen okuma.",
            ),
            (
                "Bağlam kanıtı",
                "Bir doğal dil kullanımının kapsayıcı mı dışlayıcı mı amaçlandığını destekleyen kural, açıklama veya durum bilgisi.",
            ),
        ],
        [
            _section(
                "TFL'de yalın veya kapsayıcıdır",
                "A ∨ B, A ile B'den en az birini ileri sürer ve tek başına ikisinin birlikte gerçekleşmesini dışlamaz.",
                "'Veya', 'ya ... ya ...', 'en az biri' ya da ortak yüklemli seçenekleri TFL'de kurarken.",
                "A ∨ B: A, B veya ikisi birlikte; en az biri.",
                "Ayrık bağlacın iki tarafı da B7'deki gibi tam TFL cümlesidir. Doğal dilde ortak özne veya yüklem yalnız bir kez yazılmışsa her ayrılan anahtarda tamamlanır.",
                "Gündelik 'veya'yı otomatik olarak 'tam olarak biri' diye okuma. TFL'de yalın ∨ kapsayıcıdır.",
                [
                    (
                        "Bildirim e-posta veya uygulama üzerinden gelir.",
                        "E: Bildirim e-posta üzerinden gelir. U: Bildirim uygulama üzerinden gelir. İki kanal da mümkünse yapı (E ∨ U) olur.",
                    ),
                    (
                        "Ada veya Bora sunum yapacak.",
                        "A: Ada sunum yapacak. B: Bora sunum yapacak. Bağlam ikisini yasaklamıyorsa (A ∨ B) en az birini söyler.",
                    ),
                ],
                (
                    "Önce iki tam ayrılanı anahtara yazıp sonra bağlamın birlikte gerçekleşmeye izin verip vermediğini sormak.",
                    "'Veya' görülen her yerde ikisinin birlikte olmasını otomatik olarak yasaklamak.",
                    "Dışlayıcılık yalın ayrık işaretin içinde gizli değildir; gerekiyorsa ayrıca kurulmalıdır.",
                ),
            ),
            _section(
                "Dışlayıcı okuma iki ayrı iddia kurar",
                "'Tam olarak biri' demek yalnız birlikte olmamayı değil, aynı zamanda seçeneklerden en az birinin gerçekleşmesini de gerektirir.",
                "Menü kuralı, tek kazanan, tek görevli veya seçeneklerden yalnız birine izin veren bağlamları biçimselleştirirken.",
                "((A ∨ B) ∧ ¬(A ∧ B)): en az A veya B; ayrıca A ile B birlikte değil.",
                "İlk parça iki seçeneğin de gerçekleşmediği durumu dışarıda bırakır. İkinci parça ikisinin birlikte gerçekleşmesini dışarıda bırakır. Dışlayıcılık ancak iki parça birlikteyken tamamlanır.",
                "Yalnız ¬(A ∧ B) yazma: bu yapı ikisinin birlikte olmasını reddeder ama ikisinin de olmaması ihtimalini tek başına dışlamaz.",
                [
                    (
                        "Ana yemekle ya çorba ya salata gelir; ikisi birden gelmez.",
                        "C: Çorba gelir. S: Salata gelir. Dışlayıcı yapı ((C ∨ S) ∧ ¬(C ∧ S)) olur.",
                    ),
                    (
                        "Ödülü Ada veya Bora alacak; tek kazanan var.",
                        "'Tek kazanan' bağlam kanıtıdır: en az biri kazanır ve ikisi birlikte kazanmaz.",
                    ),
                    (
                        "A ile B birlikte değil.",
                        "Yalnız birlikte olmamayı bildirir; en az birinin gerçekleştiğini ayrıca söylemediği için dışlayıcı veya değildir.",
                    ),
                ],
                (
                    "Dışlayıcı okumada hem en az biri hem birlikte olmama bileşenini açıkça göstermek.",
                    "Yalnız 'ikisi birlikte değil' parçasını dışlayıcı veya sanmak.",
                    "İki seçeneğin de gerçekleşmediği durum dışarıda bırakılmadıkça 'tam olarak biri' kurulmuş olmaz.",
                ),
            ),
            _section(
                "Ne ... ne ... iki reddi birlikte ileri sürer",
                "'Ne A ne B' okumasında A ve B ayrı ayrı olumsuzlanır, ardından bu iki olumsuz cümle birleştirilir.",
                "Türkçedeki 'ne ... ne ...', 'hiçbiri' ve 'ikisinden biri bile değil' ifadelerini açık kapsamla kurarken.",
                "(¬A ∧ ¬B): A değil ve B değil.",
                "Önce her atomik bildirim kendi olumsuzlamasıyla kurulur. Sonra iki tam olumsuz TFL cümlesi birleşim içine alınır.",
                "¬A ∨ ¬B yazma: bu yapı en az bir tarafın gerçekleşmediğini söyler; iki tarafın da gerçekleşmediğini söylemek için yetersizdir.",
                [
                    (
                        "Ne Ada ne Bora geldi.",
                        "A: Ada geldi. B: Bora geldi. Yapı (¬A ∧ ¬B) olur.",
                    ),
                    (
                        "Çorba da salata da gelmedi.",
                        "C: Çorba geldi. S: Salata geldi. Her iki bildirim reddedilir: (¬C ∧ ¬S).",
                    ),
                ],
                (
                    "Her iki atomu ayrı ayrı reddedip iki olumsuz cümleyi birleştirmek.",
                    "'Ne A ne B' ifadesini ¬A ∨ ¬B diye kurmak.",
                    "Yalın ayrık yapı yalnız en az bir tarafı gerektirir; 'ne ... ne ...' ise iki ayrı reddi birlikte ileri sürer.",
                ),
            ),
            _section(
                "Üç veya daha çok seçenek adım adım kurulur",
                "Birden çok ayrılan tek seferde parantezsiz yığılmaz; önce iki tam TFL cümlesi birleştirilir, sonra ortaya çıkan tam cümle yeni seçenekle birleştirilir.",
                "Üç kanal, üç aday veya birden fazla alternatif içeren cümlelerde yapıyı okunabilir tutarken.",
                "((A ∨ B) ∨ C): önce A ile B, sonra ortaya çıkan yapı ile C.",
                "Bu derste parantezler açık yazılır. Farklı parantezlemelerin biçimsel özellikleri daha sonra incelenecek; şimdilik kurucu adım görünür tutulur.",
                "A ∨ B ∨ C dizisini sessiz bir öncelik kuralıyla bırakma. Okuyucunun hangi iki cümlenin önce birleştiğini görmesini sağla.",
                [
                    (
                        "Başvuru e-posta, form veya gişe üzerinden yapılabilir.",
                        "E, F ve G tam bildirimleriyle yapı ((E ∨ F) ∨ G) olarak adım adım kurulabilir.",
                    ),
                    (
                        "Bu üç kanaldan tam olarak biri kullanılmalıdır.",
                        "Yalın üçlü ayrık yapı yalnız en az bir kanalı gösterir; dışlayıcılık için ek birlikte-olmama kısıtları gerekir ve bu daha ileri üretim olarak ayrıca yazılmalıdır.",
                    ),
                ],
                (
                    "Her kurucu adımda iki tam TFL cümlesini açık parantezle birleştirmek.",
                    "Üç ayrılanı parantezsiz bir sembol dizisi hâlinde bırakmak.",
                    "Açık kurucu adım, geri çeviride kapsam ve bileşen kaybını önler.",
                ),
            ),
        ],
        [
            _worked(
                "(A ∨ B)",
                "Standart okuma A, B veya ikisi birlikte olacak biçimde en az bir ayrılanı ileri sürer.",
                "Kapsayıcı",
            ),
            _worked(
                "Bildirim e-posta veya uygulama üzerinden gelir. / (E ∨ U)",
                "Bağlam iki kanalın birlikte kullanılmasına izin veriyorsa yalın kapsayıcı yapı yeterlidir.",
                "Bağlam",
            ),
            _worked(
                "Ana yemekle ya çorba ya salata gelir; ikisi birden gelmez. / ((C ∨ S) ∧ ¬(C ∧ S))",
                "İlk parça en az bir seçeneği, ikinci parça birlikte olmamayı kurar.",
                "Dışlayıcı",
            ),
            _worked(
                "¬(A ∧ B)",
                "Bu yapı yalnız ikisinin birlikte olmasını reddeder; tek başına en az birinin gerçekleştiğini söylemez.",
                "Eksik dışlayıcılık",
                "bad",
            ),
            _worked(
                "Ne Ada ne Bora geldi. / (¬A ∧ ¬B)",
                "Her iki atomik bildirim ayrı ayrı reddedilir ve olumsuz cümleler birleştirilir.",
                "Hiçbiri",
            ),
            _worked(
                "(¬A ∨ ¬B)",
                "En az bir tarafın gerçekleşmediğini söyler; 'ne A ne B' için iki reddi birlikte ileri sürmez.",
                "Kapsam hatası",
                "bad",
            ),
            _worked(
                "((A ∨ B) ∨ C)",
                "Üç seçenek, her adımda iki tam TFL cümlesi birleştirilerek açıkça kurulur.",
                "Üç seçenek",
            ),
        ],
        [
            "Yalın ∨ işaretini 'tam olarak biri' diye ezberleyip kapsayıcı okumayı unutmak.",
            "Dışlayıcı okuma için yalnız ¬(A ∧ B) yazıp en az bir seçeneğin gerçekleşmesi koşulunu kaybetmek.",
            "Yalnız (A ∨ B) yazıp bağlamın açıkça istediği birlikte-olmama koşulunu göstermemek.",
            "'Ne A ne B' ifadesini (¬A ∨ ¬B) biçiminde kurmak.",
            "Üç veya daha çok seçeneği kurucu adımı göstermeyen parantezsiz bir dizi hâlinde bırakmak.",
            "Dışlayıcı okumayı doğal dil bağlamıyla gerekçelendirmeden yalnız 'ya ... ya ...' kalıbından çıkarmak.",
        ],
        _practice(
            [
                (
                    "A ∨ B için standart geri okuma hangisidir?",
                    [
                        "Tam olarak A",
                        "Tam olarak B",
                        "A veya B; ikisi birlikte de olabilir",
                        "Ne A ne B",
                    ],
                    "A veya B; ikisi birlikte de olabilir",
                    "TFL'deki yalın ayrık bağlaç kapsayıcıdır ve en az bir ayrılanı ister.",
                    "Temel",
                ),
                (
                    "'Bildirim e-posta veya uygulama üzerinden gelir; iki kanal da kullanılabilir' hangi yapıyı destekler?",
                    ["(E ∨ U)", "(¬E ∧ ¬U)", "¬(E ∧ U)", "(E ∧ U)"],
                    "(E ∨ U)",
                    "Cümle en az bir kanalı ister ve birlikte kullanımı açıkça mümkün bırakır.",
                    "Temel",
                ),
                (
                    "Dışlayıcı 'A veya B' okumasında hangi iki parça birlikte gerekir?",
                    [
                        "A değil ve B değil",
                        "En az biri ve ikisi birlikte değil",
                        "Yalnız A ve yalnız B",
                        "A ile B birlikte ve en az biri değil",
                    ],
                    "En az biri ve ikisi birlikte değil",
                    "Tam olarak biri, iki seçeneğin de yokluğunu ve birlikte gerçekleşmesini ayrı ayrı dışarıda bırakır.",
                    "Orta",
                ),
                (
                    "Hangisi dışlayıcı A veya B okumasını tam kurar?",
                    [
                        "(A ∨ B)",
                        "¬(A ∧ B)",
                        "((A ∨ B) ∧ ¬(A ∧ B))",
                        "(¬A ∧ ¬B)",
                    ],
                    "((A ∨ B) ∧ ¬(A ∧ B))",
                    "Birinci birleşen en az birini, ikinci birleşen ikisinin birlikte olmamasını sağlar.",
                    "Orta",
                ),
                (
                    "¬(A ∧ B) neden tek başına dışlayıcı veya değildir?",
                    [
                        "Parantez içerdiği için",
                        "İki seçeneğin de gerçekleşmemesine izin verdiği için",
                        "A harfi büyük olduğu için",
                        "Yalnız A'yı zorunlu kıldığı için",
                    ],
                    "İki seçeneğin de gerçekleşmemesine izin verdiği için",
                    "Yapı birlikte olmayı reddeder ama en az bir seçeneğin gerçekleşmesini ileri sürmez.",
                    "İleri",
                ),
                (
                    "'Ne Ada ne Bora geldi' için hangi yapı uygundur?",
                    ["(¬A ∧ ¬B)", "(¬A ∨ ¬B)", "(A ∨ B)", "¬(A ∧ B)"],
                    "(¬A ∧ ¬B)",
                    "Her iki atom ayrı ayrı reddedilir ve iki olumsuz cümle birlikte ileri sürülür.",
                    "Orta",
                ),
                (
                    "(¬A ∨ ¬B) hangi nedenle 'ne A ne B'yi göstermez?",
                    [
                        "Hiç olumsuzlama içermediği için",
                        "Yalnız en az bir tarafın gerçekleşmediğini söylediği için",
                        "İki tarafı da zorunlu kıldığı için",
                        "Ayrık bağlaç kişi adlarını birleştirdiği için",
                    ],
                    "Yalnız en az bir tarafın gerçekleşmediğini söylediği için",
                    "'Ne A ne B' ise A'nın da B'nin de reddedilmesini ister.",
                    "İleri",
                ),
                (
                    "'Ödülü Ada veya Bora alacak; tek kazanan var' cümlesinde dışlayıcılık kanıtı nedir?",
                    [
                        "Kişi adlarının farklı olması",
                        "'Tek kazanan var' kuralı",
                        "Cümlenin gelecek zamanda olması",
                        "Ödül sözcüğünün kullanılması",
                    ],
                    "'Tek kazanan var' kuralı",
                    "Bu bağlam bilgisi iki kişinin birlikte kazanmasını açıkça dışlar.",
                    "Orta",
                ),
                (
                    "Üç seçenekli kapsayıcı yapıyı bu aşamada en açık nasıl yazarsın?",
                    ["A ∨ B ∨ C", "((A ∨ B) ∨ C)", "A B C", "(A ∧ B ∧ C)"],
                    "((A ∨ B) ∨ C)",
                    "Parantez, her adımda hangi iki tam TFL cümlesinin birleştirildiğini görünür kılar.",
                    "İleri",
                ),
                (
                    "Doğal dilde 'ya A ya B' gördüğünde ilk sorulması gereken nedir?",
                    [
                        "Hangi harf daha önce geliyor?",
                        "Bağlam ikisinin birlikte gerçekleşmesine izin veriyor mu?",
                        "Cümlede kaç sözcük var?",
                        "A ve B kişi adı mı?",
                    ],
                    "Bağlam ikisinin birlikte gerçekleşmesine izin veriyor mu?",
                    "Yüzey kalıbı tek başına kapsayıcı ve dışlayıcı okumayı her zaman belirlemez.",
                    "Zor",
                ),
            ],
        ),
        {
            "prompt": "Menü kurallarını aynı sembol anahtarıyla kapsayıcı, dışlayıcı ve hiçbir-seçenek okumalarına dönüştür.",
            "starter": "C: Çorba gelir.\nS: Salata gelir.\n1. Çorba veya salata alabilirsin; ikisini de alabilirsin: (C ∨ S)",
            "checks": [
                "Kapsayıcı okumada ikisinin birlikte gerçekleşmesi yasaklanmamıştır",
                "Dışlayıcı okumada hem en az biri hem birlikte olmama parçası vardır",
                "'Ne ... ne ...' okumasında C ve S ayrı ayrı olumsuzlanmıştır",
                "Her bağlam kanıtı formül kararının yanında belirtilmiştir",
                "Bütün formüller sembol anahtarıyla geri okunmuştur",
            ],
            "solution": "1. (C ∨ S): en az biri, ikisi de olabilir.\n2. ((C ∨ S) ∧ ¬(C ∧ S)): en az biri, fakat ikisi birlikte değil.\n3. (¬C ∧ ¬S): ne çorba ne salata gelir. İkinci okumanın dışlayıcılığı 'ikisi birden gelmez' kuralından gelir.",
        },
        [
            _production_task(
                "Aynı A, B ve C anahtarıyla dört farklı seçenek yapısı kur; her formülü geri çevir ve kapsayıcı ya da dışlayıcı kararını bağlam cümlesiyle gerekçelendir.",
                [
                    "A, B ve C'nin karşısına aynı konuya ait üç tam bildirim yaz.",
                    "A ile B için kapsayıcı en-az-biri yapısı kur.",
                    "A ile B için hem en az biri hem birlikte olmama bileşenlerini taşıyan dışlayıcı yapı kur.",
                    "A ile B'nin ikisinin de gerçekleşmediği yapıyı iki ayrı olumsuz cümleyle kur.",
                    "A, B ve C'den en az birini açık kurucu parantezlerle göster.",
                    "Her formül için onu kapsayıcı veya dışlayıcı yapan bağlam kanıtını ve doğal dil geri okumasını yaz.",
                ],
                "Yalın ∨ ile dışlayıcı yapıyı, 'ikisi birlikte değil' ile 'hiçbiri' okumalarını kesin biçimde ayır.",
                "Başvuru kanalları",
                [
                    "Başvuru e-posta veya çevrim içi form üzerinden yapılabilir; iki kanal da kabul edilir.",
                    "Doğrulama için ya e-posta ya telefon seçilmelidir; ikisi birden seçilemez.",
                    "Başvuru ne e-posta ne çevrim içi form üzerinden gönderildi.",
                    "Başvuru e-posta, çevrim içi form veya gişeden en az biriyle yapılabilir.",
                ],
                "E, F ve G gibi konuya uygun büyük cümle harfleri seçebilir; teslim boyunca aynı anahtarı koruyabilirsin.",
            ),
        ],
        [
            "Öğrenci yalın ∨ yapısını 'en az biri, ikisi de olabilir' diye doğru geri okur.",
            "Dışlayıcı okumayı hem (A ∨ B) hem ¬(A ∧ B) bileşenleriyle eksiksiz kurar.",
            "Dışlayıcılık kararını yüzey kalıbıyla değil, birlikte gerçekleşmeyi yasaklayan açık bağlam kanıtıyla gerekçelendirir.",
            "'Ne A ne B' ifadesini (¬A ∧ ¬B) yapısıyla kurar ve (¬A ∨ ¬B) hatasını açıklar.",
            "Üç seçenekli yapıyı her adımda iki tam TFL cümlesi kullanarak açık parantezle kurar.",
            "Her formülü sembol anahtarıyla doğal dile geri çevirip amaçlanan kapsayıcı veya dışlayıcı okumayla karşılaştırır.",
        ],
        [
            "A ∨ B, A ile B'nin birlikte gerçekleşmesini neden tek başına dışlamaz?",
            "Dışlayıcı 'A veya B' için neden yalnız ¬(A ∧ B) yeterli değildir?",
            "'Ne A ne B' ile 'A ve B birlikte değil' arasındaki iddia farkı nedir?",
        ],
        "Sonraki derste seçenek yapısından koşul yönüne geçecek; 'ise', 'yalnızca' ve '-medikçe' ifadelerini garanti ve gereklilik üzerinden kuracağız.",
        ["forallx-connectives"],
        "Kapsayıcı ve dışlayıcı ayrımı bu derste doğal dil okuması ve bileşik yapı üzerinden kurulur; değer ataması ve biçimsel eşdeğerlik kanıtı Faz C'ye bırakılır.",
        ["ders-19-veya-ve-ise"],
    )

    lesson["reading_note"] = (
        "'Veya' gördüğünde önce iki tam ayrılanı yaz; sonra bağlamın ikisinin birlikte gerçekleşmesini yasaklayıp yasaklamadığını ayrı bir cümleyle belirt."
    )
    lesson["symbol_set"] = ["A", "B", "C", "¬", "∧", "∨", "(", ")"]
    lesson["proof_tools"] = [
        "Ayrılanları tamamlama",
        "Kapsayıcı geri okuma",
        "Dışlayıcılığı iki parçaya ayırma",
        "Bağlam kanıtı yazma",
        "Kapsam parantezleme",
    ]
    return lesson


def _candidate_b10():
    lesson = _lesson(
        "B10",
        "ders-kosul-yalnizca-cift-yonluluk",
        "Koşul, Yalnızca, Çift Yönlülük ve “-medikçe”",
        "Koşul cümlesinin yönünü sözcük sırasından değil garanti ve gereklilik ilişkisinden kurar; tek yönlü koşulu, iki yönlü koşulu ve '-medikçe' okumalarını açık yeniden yazımla ayırır.",
        "Koşul yönü ve çift yönlülük",
        40,
        [
            "ders-5-zorunlu-ve-yeterli-kosul",
            "ders-19-veya-ve-ise",
        ],
        [
            "tfl.conditional_direction",
            "tfl.biconditional_construct",
            "tfl.unless_translate",
        ],
        [
            "'A ise B' ile 'A yalnızca B ise' cümlelerini garanti ve gereklilik testiyle doğru yönde koşul olarak kurmak.",
            "Yeterli koşulu önbileşene, onun gerekli koşulunu artbileşene yerleştirmek ve bu terimleri argüman rolleriyle karıştırmamak.",
            "Çift yönlü koşulu iki ayrı tek yönlü koşul olarak açmak ve iki yönün de metinde desteklendiğini denetlemek.",
            "'-medikçe' cümlesini önce açık bir 'eğer ... değilse ...' cümlesine dönüştürüp sonra sembolleştirmek.",
            "Koşul işaretinin nedensellik, zaman sırası, söz verme veya açıklama ilişkisini tek başına korumadığını belirtmek.",
        ],
        [
            (
                "Koşul",
                "Bir TFL cümlesinin gerçekleşmesini başka bir TFL cümlesinin gerçekleşmesi durumuna bağlayan tek yönlü yapı.",
            ),
            (
                "Önbileşen",
                "Koşul cümlesinde 'eğer' tarafında bulunan tam TFL cümlesi; argümanın öncülüyle aynı kavram değildir.",
            ),
            (
                "Artbileşen",
                "Koşul cümlesinde 'o hâlde' tarafında bulunan tam TFL cümlesi; argümanın sonucu olmak zorunda değildir.",
            ),
            (
                "Gerekli koşul",
                "Hedefin gerçekleşmesi için bulunması gereken koşul; hedef koşul yapısında bu gerekli koşula yönelir.",
            ),
            (
                "Yeterli koşul",
                "Verildiğinde hedefi garanti eden koşul; koşul yapısının önbileşeninde yer alır.",
            ),
            (
                "Çift yönlü koşul",
                "Her iki tarafın da diğeri için hem gerekli hem yeterli olduğunu ileri süren iki yönlü yapı.",
            ),
        ],
        [
            _section(
                "Koşul yönü garanti testiyle bulunur",
                "A → B yapısında A önbileşen, B artbileşendir: A'nın gerçekleşmesi B'yi garanti eden yön olarak yazılır.",
                "'İse', 'eğer ... o hâlde', 'olduğunda' veya devrik koşul cümlelerinde hangi tarafın oku başlattığını belirlerken.",
                "A → B: Eğer A ise B. A, B için yeterli; B, A için gereklidir.",
                "Sözcüklerin cümledeki sırası tek başına yönü belirlemez. A'yı varsay: metin B'yi garanti ediyor mu? Evetse yön A'dan B'yedir.",
                "Koşul cümlesinin önbileşenini argümanın öncülü, artbileşenini de otomatik olarak argümanın sonucu sanma; bunlar cümle içi yapısal rollerdir.",
                [
                    (
                        "Kart geçerliyse turnike açılır.",
                        "K: Kart geçerlidir. T: Turnike açılır. Kartın geçerli olması açılmayı garanti ettiği için K → T yazılır.",
                    ),
                    (
                        "Turnike, kart geçerliyse açılır.",
                        "Sözcük sırası değişse de açık yeniden yazım 'Eğer kart geçerliyse turnike açılır' olur; yön yine K → T'dir.",
                    ),
                    (
                        "Turnike açılırsa kart geçerlidir.",
                        "Bu ayrı iddia T → K yönündedir; önceki koşulun sözcüklerini taşıması iki yönü aynı yapmaz.",
                    ),
                ],
                (
                    "A'yı varsayıp metnin B'yi garanti edip etmediğini sorarak yönü kurmak.",
                    "Ok yönünü cümlede önce yazılan ada veya harfe göre seçmek.",
                    "Koşul yönü sözcük konumundan değil, ileri sürülen garanti ilişkisinden gelir.",
                ),
            ),
            _section(
                "'Yalnızca' ve gereklilik oku hedefe çevirir",
                "'A yalnızca B ise' cümlesi, A'nın gerçekleşmesinin B'yi gerektirdiğini söyler; bu nedenle A → B biçimindedir.",
                "'Yalnızca', 'ancak ... ise', 'için gereklidir' ve 'için yeterlidir' kalıplarında yön hatasını önlerken.",
                "A yalnızca B ise: A → B. / A, B için yeterliyse: A → B. / B, A için gerekliyse: A → B.",
                "Yalnızca'dan sonraki B, A'nın gerekli koşuludur. A gerçekleştiğinde B'nin bulunması gerekir; fakat B'nin tek başına A'yı garanti ettiği henüz söylenmez.",
                "Her 'ancak' sözcüğünü koşul işareti sanma. 'Rapor uzundu; ancak anlaşılırdı' cümlesindeki ancak karşıtlık kurar ve birleşim yapısındadır.",
                [
                    (
                        "Kullanıcı yalnızca kartı geçerliyse içeri girer.",
                        "G: Kullanıcı içeri girer. K: Kart geçerlidir. Giriş kartı gerektirdiği için G → K yazılır.",
                    ),
                    (
                        "Kartın geçerli olması giriş için yeterlidir.",
                        "K, G'yi garanti eden yeterli koşuldur: K → G.",
                    ),
                    (
                        "Kartın geçerli olması giriş için gereklidir.",
                        "Giriş gerçekleştiğinde kartın geçerli olması gerekir: G → K.",
                    ),
                    (
                        "Rapor uzundu; ancak anlaşılırdı.",
                        "U: Rapor uzundu. A: Rapor anlaşılırdı. 'Ancak' burada karşıtlık kurar; yapı (U ∧ A) olur ve karşıtlık tonu kaybolur.",
                    ),
                ],
                (
                    "Yeterli koşuldan garanti edilene; hedef durumdan onun gerekli koşuluna doğru oku çizmek.",
                    "'Yalnızca B ise A' cümlesini sözcük sırasına bakıp B → A yapmak.",
                    "'Yalnızca' B'yi A için gerekli kılar; B'nin A için yeterli olduğunu tek başına söylemez.",
                ),
            ),
            _section(
                "Çift yönlülük iki ayrı garantiyi birlikte ister",
                "A ↔ B, yalnız A → B'yi değil B → A'yı da ileri sürer; iki yönün metinde ayrı ayrı desteklenmesi gerekir.",
                "'Ancak ve ancak', 'tam olarak şu durumda', 'hem gerekli hem yeterli' gibi iki yönlü ifadeleri kurarken.",
                "A ↔ B, (A → B) ∧ (B → A) biçimindeki iki yönün kısa gösterimidir.",
                "Bir yön A'nın B için yeterli, B'nin A için gerekli olduğunu; diğer yön bunun tersini kurar. Birlikte her taraf diğerinin hem gerekli hem yeterli koşulu olur.",
                "Gündelik konuşmada kişi tek yönlü 'eğer' ile daha güçlü bir söz vermek isteyebilir; metin veya açık bağlam ikinci yönü desteklemiyorsa otomatik ↔ yazma.",
                [
                    (
                        "Kapı ancak ve ancak kart geçerliyse açılır.",
                        "T: Turnike açılır. K: Kart geçerlidir. Metin hem T → K hem K → T söylediği için T ↔ K yazılır.",
                    ),
                    (
                        "Şekil, tam olarak üç kenarı varsa üçgendir.",
                        "Ü: Şekil üçgendir. K: Şeklin tam üç kenarı vardır. Amaçlanan tanımsal okumada Ü ↔ K kurulabilir.",
                    ),
                    (
                        "Çalışırsan geçersin.",
                        "Ç: Çalışırsın. G: Geçersin. Cümle yalnız Ç → G yönünü verir; geçmenin çalışmayı garanti ettiği ikinci yönü söylemez.",
                    ),
                ],
                (
                    "↔ yazmadan önce A → B ve B → A cümlelerini doğal dilde ayrı ayrı doğrulamak.",
                    "Metindeki tek bir 'eğer' kullanımını bağlam kanıtı olmadan çift yönlü yapmak.",
                    "Çift yönlü koşul, tek yönlü koşuldan daha güçlü iki iddiayı birlikte taşır.",
                ),
            ),
            _section(
                "'-medikçe' önce açık koşula çevrilir",
                "'-medikçe' kalıbı doğrudan sembole atlanmadan, cümlenin amaçlanan okumasına göre 'eğer ... değilse ...' biçiminde yeniden yazılır.",
                "'Olmadıkça', '-meden', 'aksi hâlde' ve benzeri dolaylı koşul yapılarında olumsuzlamanın hangi tarafta olduğunu belirlerken.",
                "K olmadıkça T olmaz: Eğer K değilse T değil; ¬K → ¬T.",
                "Yeniden yazım, iki olumsuzlamayı ve yönü görünür kılar. Gündelik kullanım bazen bundan daha güçlü bir iki yönlülük ima edebilir; yalnız açıkça desteklenen okuma biçimselleştirilir.",
                "'-medikçe'yi tek bir sabit sembol şablonuna mekanik olarak bağlama. Önce özne, olumsuzluk ve garanti yönünü tam cümlelerle aç.",
                [
                    (
                        "Kart okutulmadıkça turnike açılmaz.",
                        "K: Kart okutulur. T: Turnike açılır. Açık okuma 'Eğer kart okutulmazsa turnike açılmaz' olur: ¬K → ¬T.",
                    ),
                    (
                        "Yağmur dinmedikçe maç başlamaz.",
                        "D: Yağmur diner. M: Maç başlar. Açık okuma ¬D → ¬M olur.",
                    ),
                    (
                        "Yağmur yağmadıkça koşarım.",
                        "Y: Yağmur yağar. K: Koşarım. Asgari koşullu okuma 'Eğer yağmur yağmazsa koşarım' biçimindedir: ¬Y → K.",
                    ),
                ],
                (
                    "Önce '-medikçe' cümlesini açık 'eğer ... değilse ...' yapısına dönüştürüp sonra harfleri yerleştirmek.",
                    "Olumsuzlukların yerini denetlemeden ezberlenmiş bir ok yönü çizmek.",
                    "Açık yeniden yazım, Türkçedeki olumsuzluk ve yön hatasını formülden önce görünür kılar.",
                ),
            ),
            _section(
                "Koşul işareti doğal dil ilişkisinin tamamı değildir",
                "TFL koşulu, seçilen tek yönlü yapıyı korur; nedensellik, açıklama, zaman, emir, söz verme veya olasılık derecesini ayrıca kodlamaz.",
                "Aynı koşul yapısına indirgenen doğal dil cümlelerinin neden yine de tam eş anlamlı olmadığını raporlarken.",
                "A → B yalnız 'A ise B' yönünü gösterir; A'nın B'ye neden olduğunu tek başına söylemez.",
                "'Düğmeye basarsan ışık yanar' nedensel okunabilir; 'Sayı dörde bölünüyorsa çifttir' kavramsal bir bağlantıdır. Aynı koşul yapısı ilişki türünü görünmez bırakır.",
                "Formülü doğal dil cümlesinin eksiksiz çevirisi diye sunma. Kayıp ilişkiyi çözümün yanında belirt.",
                [
                    (
                        "Düğmeye basarsan ışık yanar.",
                        "B → I yapısı yönü korur; fiziksel nedenselliği ayrıca göstermez.",
                    ),
                    (
                        "Sayı dörde bölünüyorsa çifttir.",
                        "D → Ç yine koşul yapısıdır; matematiksel ilişkinin niteliği ok işaretinde ayrıca görünmez.",
                    ),
                    (
                        "Ödevini bitirirsen parka gideriz.",
                        "Koşul biçimi kurulabilir; söz verme, izin veya konuşma edimi bilgisi TFL'de kaybolur.",
                    ),
                ],
                (
                    "Koşul yönünü kurduktan sonra kaybolan nedensellik, zaman veya konuşma edimi bilgisini yazmak.",
                    "Her A → B yapısını A'nın B'ye neden olduğu iddiası saymak.",
                    "TFL aynı yapısal örüntüyü izlerken doğal dil ilişkisinin türünü dışarıda bırakabilir.",
                ),
            ),
        ],
        [
            _worked(
                "Kart geçerliyse turnike açılır. / K → T",
                "K'nın gerçekleşmesi T'yi garanti eden yön olarak ileri sürülür.",
                "Koşul",
            ),
            _worked(
                "Kullanıcı yalnızca kartı geçerliyse içeri girer. / G → K",
                "Kartın geçerli olması giriş için gerekli koşuldur; girişten karta yöneliriz.",
                "Yalnızca",
            ),
            _worked(
                "Kartın geçerli olması giriş için yeterlidir. / K → G",
                "Yeterli koşul önbileşende, garanti edilen durum artbileşendedir.",
                "Yeterli",
            ),
            _worked(
                "Kartın geçerli olması giriş için gereklidir. / G → K",
                "Hedef durumdan onun gerekli koşuluna yöneliriz.",
                "Gerekli",
            ),
            _worked(
                "Kapı ancak ve ancak kart geçerliyse açılır. / T ↔ K",
                "Metin T → K ve K → T yönlerinin ikisini de ileri sürer.",
                "Çift yönlü",
            ),
            _worked(
                "Kart okutulmadıkça turnike açılmaz. / ¬K → ¬T",
                "Önce 'Kart okutulmazsa turnike açılmaz' diye açık koşula dönüştürülür.",
                "-medikçe",
            ),
            _worked(
                "Rapor uzundu; ancak anlaşılırdı. / (U ∧ A)",
                "'Ancak' burada gerekli koşul değil karşıtlık kurar; karşıtlık tonu birleşimde kaybolur.",
                "Koşul değil",
                "bad",
            ),
            _worked(
                "Düğmeye basarsan ışık yanar. / B → I",
                "Yön korunur; nedensel bağlantının türü koşul işaretinde görünmez.",
                "Bilgi kaybı",
            ),
        ],
        [
            "'A yalnızca B ise' cümlesini B → A yazarak gerekli ve yeterli yönünü ters çevirmek.",
            "Koşul cümlesinin önbileşenini argümanın öncülü, artbileşenini argümanın sonucu sanmak.",
            "Tek yönlü bir 'eğer' cümlesini bağlam kanıtı olmadan A ↔ B biçiminde güçlendirmek.",
            "A ↔ B yazıp A → B ile B → A yönlerinden birini doğal dilde doğrulamamak.",
            "'-medikçe' kalıbında olumsuzlukları ve yönü açık cümleye çevirmeden sembole atlamak.",
            "Karşıtlık anlamındaki 'ancak' sözcüğünü koşul belirteci sanmak.",
            "A → B yapısının nedensellik, zaman sırası veya söz verme bilgisini de eksiksiz taşıdığını varsaymak.",
        ],
        _practice(
            [
                (
                    "K: Kart geçerlidir. T: Turnike açılır. 'Kart geçerliyse turnike açılır' hangi yapıdır?",
                    ["K → T", "T → K", "K ↔ T", "(K ∧ T)"],
                    "K → T",
                    "Kartın geçerli olması turnikenin açılmasını garanti eden önbileşendir.",
                    "Temel",
                ),
                (
                    "G: Kullanıcı girer. K: Kart geçerlidir. 'Kullanıcı yalnızca kartı geçerliyse girer' hangi yapıdır?",
                    ["K → G", "G → K", "G ↔ K", "(G ∧ K)"],
                    "G → K",
                    "Giriş gerçekleştiğinde gerekli koşul olan geçerli kartın bulunması gerekir.",
                    "Temel",
                ),
                (
                    "'A, B için yeterlidir' hangi yönü verir?",
                    ["A → B", "B → A", "A ↔ B", "(A ∧ B)"],
                    "A → B",
                    "Yeterli koşul A verildiğinde hedef B garanti edilir.",
                    "Orta",
                ),
                (
                    "'B, A için gereklidir' hangi yönü verir?",
                    ["A → B", "B → A", "A ↔ B", "¬A → B"],
                    "A → B",
                    "A gerçekleştiğinde onun gerekli koşulu B bulunmalıdır.",
                    "Orta",
                ),
                (
                    "A → B yapısında A ve B'nin cümle içi adları hangileridir?",
                    [
                        "A öncül, B sonuç",
                        "A önbileşen, B artbileşen",
                        "A ayrılan, B birleşen",
                        "A tanım, B örnek",
                    ],
                    "A önbileşen, B artbileşen",
                    "Bunlar koşul cümlesinin yapısal parçalarıdır; argüman rolleriyle özdeş değildir.",
                    "Orta",
                ),
                (
                    "A ↔ B yazmak için hangi iki yönün de desteklenmesi gerekir?",
                    ["A → B ve B → A", "A → B ve ¬A", "A ∧ B ve ¬B", "A ∨ B ve ¬A"],
                    "A → B ve B → A",
                    "Çift yönlü koşul iki tek yönlü garantiyi birlikte ileri sürer.",
                    "Temel",
                ),
                (
                    "'Çalışırsan geçersin' cümlesi neden tek başına Ç ↔ G değildir?",
                    [
                        "Çünkü gelecek zaman kullanır",
                        "Çünkü yalnız Ç → G yönünü verir, G → Ç yönünü söylemez",
                        "Çünkü koşul cümleleri sembolleştirilemez",
                        "Çünkü iki kişi yoktur",
                    ],
                    "Çünkü yalnız Ç → G yönünü verir, G → Ç yönünü söylemez",
                    "İkinci yönü eklemek doğal dil cümlesini gerekçesiz biçimde güçlendirir.",
                    "İleri",
                ),
                (
                    "K: Kart okutulur. T: Turnike açılır. 'Kart okutulmadıkça turnike açılmaz' önce nasıl yeniden yazılır?",
                    [
                        "Kart okutulursa turnike açılmaz",
                        "Kart okutulmazsa turnike açılmaz",
                        "Turnike açılırsa kart okutulmaz",
                        "Kart okutulur ve turnike açılır",
                    ],
                    "Kart okutulmazsa turnike açılmaz",
                    "'-medikçe' yapısındaki olumsuzluklar ve yön, sembolden önce açık koşula çevrilir.",
                    "Orta",
                ),
                (
                    "'Kart okutulmadıkça turnike açılmaz' açık okuması hangi yapıdır?",
                    ["¬K → ¬T", "K → ¬T", "¬T → ¬K", "K ↔ T"],
                    "¬K → ¬T",
                    "Önbileşen kartın okutulmaması, artbileşen turnikenin açılmamasıdır.",
                    "İleri",
                ),
                (
                    "Hangi 'ancak' kullanımı koşul değil karşıtlık kurar?",
                    [
                        "Dosya ancak ödeme yapılırsa açılır",
                        "Rapor uzundu; ancak anlaşılırdı",
                        "Yalnızca kart varsa girilir",
                        "İzin gerekliyse kapı açılmaz",
                    ],
                    "Rapor uzundu; ancak anlaşılırdı",
                    "Buradaki 'ancak' iki bildirimi karşıtlık tonuyla birleştirir; gerekli koşul belirtmez.",
                    "İleri",
                ),
                (
                    "B → I formülü 'Düğmeye basarsan ışık yanar' için hangi bilgiyi tek başına taşımaz?",
                    [
                        "Basma ile yanma arasındaki yönü",
                        "B ve I'nin tam TFL cümleleri olduğunu",
                        "Basma olayının ışığın yanmasına fiziksel olarak neden olduğu bilgisini",
                        "Bir koşul yapısı bulunduğunu",
                    ],
                    "Basma olayının ışığın yanmasına fiziksel olarak neden olduğu bilgisini",
                    "Koşul işareti seçilen yapısal yönü korur, nedensellik türünü ayrıca kodlamaz.",
                    "Zor",
                ),
                (
                    "Koşul yönünü teslim etmeden önce en güvenilir denetim hangisidir?",
                    [
                        "Harflere alfabetik sıra vermek",
                        "Önbileşeni varsayıp metnin artbileşeni garanti edip etmediğini sormak ve geri çevirmek",
                        "Her koşulu çift yönlü yapmak",
                        "Yalnız ok işaretinin görünüşüne bakmak",
                    ],
                    "Önbileşeni varsayıp metnin artbileşeni garanti edip etmediğini sormak ve geri çevirmek",
                    "Garanti testi ve geri çeviri, sözcük sırasına dayalı yön hatasını görünür kılar.",
                    "Zor",
                ),
            ],
        ),
        {
            "prompt": "Kütüphane erişim kurallarını garanti yönünü açıklayarak tamamla.",
            "starter": "K: Kart geçerlidir.\nT: Turnike açılır.\nG: Kullanıcı girer.\nR: Rezervasyon vardır.\n1. Kart geçerliyse turnike açılır: K → T",
            "checks": [
                "Her koşulun önbileşeni ve artbileşeni tam TFL cümlesidir",
                "'Yalnızca' cümlesinde hedef durum gerekli koşula yönelmiştir",
                "Çift yönlü cümlede iki tek yön ayrı ayrı geri okunmuştur",
                "'-medikçe' cümlesi sembolden önce açık koşula çevrilmiştir",
                "Koşul işaretinde kaybolan ilişki türü en az bir örnekte belirtilmiştir",
            ],
            "solution": "1. K → T.\n2. 'Kullanıcı yalnızca kartı geçerliyse girer': G → K.\n3. 'Özel salona ancak ve ancak rezervasyonu varsa girer': G ↔ R; hem G → R hem R → G.\n4. 'Kart okutulmadıkça turnike açılmaz': ¬K → ¬T. Her formül anahtarla geri okunmalı; erişim politikasının hukuki veya nedensel niteliği ok işaretinde ayrıca görünmez.",
        },
        [
            _production_task(
                "Yayın politikasını sembolleştir; her koşul için garanti yönünü yaz, çift yönlü cümleyi iki yöne aç, '-medikçe' cümlesini önce açık Türkçeye çevir ve koşul olmayan 'ancak' kullanımını ayır.",
                [
                    "I, Y ve E harfleri için tam ve tutarlı bir sembol anahtarı kur.",
                    "Her tek yönlü koşulda önbileşeni varsayıp artbileşenin metin tarafından garanti edildiğini göster.",
                    "'Yalnızca' ve 'gereklidir' cümlelerini aynı yönü verip vermedikleri bakımından karşılaştır.",
                    "Çift yönlü koşulu iki ayrı tek yönlü koşul olarak geri oku.",
                    "'-medikçe' cümlesini sembolleştirmeden önce 'eğer ... değilse ...' biçiminde yaz.",
                    "Karşıtlık anlamındaki 'ancak' cümlesini koşul sayma; kaybolan karşıtlık tonunu not et.",
                    "En az bir koşulda nedensellik, zaman veya kurumsal kural bilgisinin formülde görünmediğini açıkla.",
                ],
                "Yeterli ve gerekli koşul yönlerini, tek ve çift yönlülüğü, olumsuz koşulu ve karşıtlık anlamındaki 'ancak'ı birbirinden ayır.",
                "Yayın politikası",
                [
                    "Dosya imzalanırsa yayımlanır.",
                    "Dosya yalnızca editör onaylarsa yayımlanır.",
                    "Editör onayı dosyanın yayımlanması için gereklidir.",
                    "Dosya, editör onayı için yeterli değildir.",
                    "Dosya ancak ve ancak editör onayı ve imza varsa yayımlanır.",
                    "İmza olmadıkça dosya yayımlanmaz.",
                    "Dosya uzundu; ancak anlaşılırdı.",
                ],
                "Dördüncü cümle bir koşulu reddeder; onu otomatik bir olumlu ok yapısına dönüştürmeden doğal dilde neyi dışladığını açıkla.",
            ),
        ],
        [
            "Öğrenci 'A ise B', 'A yalnızca B ise', 'A B için yeterlidir' ve 'B A için gereklidir' cümlelerinin yönünü garanti testiyle doğru kurar.",
            "Koşul cümlesinin önbileşen/artbileşen rollerini argümanın öncül/sonuç rollerinden ayırır.",
            "A ↔ B yapısını A → B ve B → A yönlerinin ikisini de doğal dilde geri okuyarak doğrular.",
            "'-medikçe' cümlesini açık olumsuz koşula dönüştürmeden sembolleştirmez ve iki olumsuzlamanın kapsamını korur.",
            "Karşıtlık anlamındaki 'ancak'ı koşul belirteci sanmaz.",
            "En az bir koşul örneğinde nedensellik, zaman sırası veya konuşma edimi bilgisinin TFL'de kaybolduğunu açıklar.",
        ],
        [
            "'A yalnızca B ise' neden B → A değil A → B biçimindedir?",
            "A ↔ B yazmadan önce hangi iki doğal dil cümlesini ayrı ayrı doğrulamalısın?",
            "'-medikçe' cümlesinde yönü bulmak için ilk yeniden yazım adımı nedir?",
        ],
        "Sonraki derste şimdiye kadar kullandığımız işaret dizilerinin hangi kurucu kurallarla TFL cümlesi olduğunu, ana bağlaç ve kapsam üzerinden kesinleştireceğiz.",
        ["forallx-connectives"],
        "Koşul bu derste sözdizimsel yön, geri çeviri ve doğal dil kaybı üzerinden kurulur. Maddi koşulun değer koşulları ve koşul paradoksları Faz C'de; çıkarım lisansları Faz D'de ele alınacaktır.",
        ["ders-19-veya-ve-ise"],
    )

    lesson["reading_note"] = (
        "Oku çizmeden önce cümleyi 'Eğer ... ise ...' biçiminde yeniden yaz; sonra ilk tarafın ikinciyi gerçekten garanti edip etmediğini sor."
    )
    lesson["symbol_set"] = [
        "A",
        "B",
        "¬",
        "∧",
        "∨",
        "→",
        "↔",
        "(",
        ")",
    ]
    lesson["proof_tools"] = [
        "Garanti yönü testi",
        "Gerekli-yeterli yeniden yazımı",
        "İki yönü ayrı doğrulama",
        "-medikçe açılımı",
        "Geri çeviri denetimi",
        "Bilgi kaybı notu",
    ]
    return lesson


def _candidate_b11():
    lesson = _lesson(
        "B11",
        "ders-tfl-cumlesi-ana-baglac-ve-kapsam",
        "TFL Cümlesi, Ana Bağlaç ve Kapsam",
        "Bir işaret dizisinin TFL cümlesi olup olmadığını kurucu tanımla kanıtlar; oluşum ağacından ana bağlacı, doğrudan alt cümleleri ve kapsamı çıkarır.",
        "Biçimsel sözdizimi ve çözümleme",
        40,
        [
            "ders-kullanim-anma-ve-dil-duzeyleri",
            "ders-kosul-yalnizca-cift-yonluluk",
        ],
        [
            "tfl.wff_verify",
            "tfl.main_connective",
            "tfl.scope_parse",
            "metalanguage.metavariable_use",
        ],
        [
            "TFL ifadesi ile kurucu kurallara göre oluşmuş TFL cümlesini birbirinden ayırmak.",
            "TFL cümlelerinin temel, kurucu ve kapanış maddelerinden oluşan tümevarımsal tanımını hem kurma hem çözme yönünde uygulamak.",
            "Karmaşık bir TFL cümlesinin ana bağlacını, doğrudan alt cümlelerini ve bütün bağlaç kapsamlarını oluşum ağacıyla bulmak.",
            "Nesne dilindeki A cümle harfiyle üst dilde herhangi bir TFL cümlesi için kullanılan 𝒜 üst değişkenini ayırmak.",
            "Katı parantez kuralıyla yalnız en dış parantezi düşürme uzlaşımını birbirine karıştırmamak.",
        ],
        [
            (
                "TFL ifadesi",
                "TFL alfabesindeki cümle harfi, bağlaç ve parantez sembollerinin herhangi bir sonlu dizisi; iyi kurulmuş olmak zorunda değildir.",
            ),
            (
                "TFL cümlesi",
                "TFL'nin kurucu tanımıyla atomik cümlelerden sonlu sayıda adımda üretilmiş iyi kurulmuş ifade.",
            ),
            (
                "Tümevarımsal tanım",
                "Temel öğeleri, onlardan yeni öğe üretme kurallarını ve bunların dışında hiçbir öğenin kabul edilmediğini belirleyen tanım.",
            ),
            (
                "Alt cümle",
                "Bir TFL cümlesinin kurucu geçmişinde yer alan ve kendisi de TFL cümlesi olan parça.",
            ),
            (
                "Ana bağlaç",
                "Karmaşık TFL cümlesini kuran son adımda eklenen bağlaç.",
            ),
            (
                "Kapsam",
                "Belirli bir bağlacın ana bağlaç olduğu en kısa alt cümle.",
            ),
            (
                "Üst değişken",
                "Nesne dilinin bir cümlesi olmayan, üst dilde herhangi bir TFL cümlesinin yerini tutan 𝒜 veya ℬ gibi işaret.",
            ),
        ],
        [
            _section(
                "Her ifade cümle değildir",
                "TFL alfabesindeki sembollerin herhangi bir dizisi TFL ifadesidir; ancak yalnız kurucu tanıma göre oluşan diziler TFL cümlesidir.",
                "Bir diziyi yalnız 'mantıksal göründüğü' veya parantezleri dengeli olduğu için kabul etmeden önce.",
                "Alfabe: A, B, C, ... ve alt indisli cümle harfleri; ¬, ∧, ∨, →, ↔; ( ve ).",
                "A atomik TFL cümlesidir. Buna karşılık ¬∧A, yalnız TFL sembollerinden oluşsa bile hiçbir kurucu adımla üretilemez.",
                "Dengeli parantez sayısını cümle olmanın yeterli koşulu sanma. (A) dengelidir ama tek bir cümleyi yalnız paranteze alma kuralı yoktur.",
                [
                    (
                        "A",
                        "Bir cümle harfi olduğu için doğrudan atomik TFL cümlesidir.",
                    ),
                    (
                        "¬∧A",
                        "TFL ifadesidir; fakat ¬ işaretinden sonra gelen ∧A bir TFL cümlesi olmadığı için kurucu tanımda tıkanır.",
                    ),
                    (
                        "(A)",
                        "TFL ifadesidir; fakat yalnız parantez ekleyerek yeni cümle üretme kuralı bulunmadığı için katı anlamda cümle değildir.",
                    ),
                    (
                        "𝒜",
                        "TFL alfabesinin bir cümle harfi değildir; nesne dilinde ifade değil, üst dilde kullanılan üst değişkendir.",
                    ),
                ],
                (
                    "Her diziyi hangi kurucu maddeyle üretildiğini göstererek kabul etmek.",
                    "Yalnız TFL'ye benzeyen semboller ve dengeli parantez gördüğünde diziyi cümle saymak.",
                    "İyi kurulmuşluk, görünüş değil kurucu geçmiş özelliğidir.",
                ),
            ),
            _section(
                "Kurucu tanım bütün ve yalnız TFL cümlelerini üretir",
                "Tanım atomik cümlelerle başlar, önceki TFL cümlelerine bağlaç uygulayarak yeni cümleler üretir ve bunların dışında hiçbir diziyi kabul etmez.",
                "Bir cümleyi adım adım kurarken veya karmaşık bir diziyi atomik yapraklara kadar çözerken.",
                "1. Her cümle harfi cümledir. 2. 𝒜 cümleyse ¬𝒜 cümledir. 3. 𝒜 ve ℬ cümleyse (𝒜 ∧ ℬ), (𝒜 ∨ ℬ), (𝒜 → ℬ) ve (𝒜 ↔ ℬ) cümledir. 4. Bunların dışında hiçbir dizi TFL cümlesi değildir.",
                "Tanım iki yönde çalışır: atomlardan karmaşık cümle kurar; karmaşık cümleyi de onu üreten son kurala ve daha küçük cümlelere geri çözer.",
                "'Başka hiçbir şey' kapanış maddesini atlama. Bu madde olmadan hatalı dizilerin neden dışarıda kaldığını açıklayamazsın.",
                [
                    (
                        "A, B, (A ∧ B), ¬(A ∧ B)",
                        "A ve B temel maddeyle; birleşim ikili kuralla; son cümle olumsuzlama kuralıyla sırasıyla üretilir.",
                    ),
                    (
                        "C, ¬C, (B → ¬C), (A ∨ (B → ¬C))",
                        "Her adımda yalnız daha önce cümle olduğu gösterilmiş tam parçalar kullanılır.",
                    ),
                ],
                (
                    "Her karmaşık cümlenin doğrudan alt cümlelerini daha önce doğrulanmış kurucu adımlara bağlamak.",
                    "Bağlaçları ve harfleri doğru sayıda içerdiği için bir diziyi kanıtsız kabul etmek.",
                    "Kurucu tanım, hangi dizilerin cümle olduğunu üretilebilirlik üzerinden kesin biçimde sınırlar.",
                ),
            ),
            _section(
                "A nesne dilinde, 𝒜 üst dildedir",
                "A belirli bir atomik TFL cümlesidir; 𝒜 ise TFL'nin içinde bulunmayan ve üst dilde herhangi bir TFL cümlesinden söz etmek için kullanılan üst değişkendir.",
                "Kurucu tanımı tek tek bütün cümleler için yeniden yazmadan genel kural ifade ederken.",
                "'A' belirli bir TFL cümlesini anar. '𝒜' herhangi bir TFL cümlesi için üst dilde yer tutar.",
                "'𝒜 cümleyse ¬𝒜 cümledir' kuralında 𝒜 yerine A, ¬A veya (A ∧ B) gibi herhangi bir TFL cümlesi getirilebilir; 𝒜'nın kendisi formülün içine yazılmaz.",
                "𝒜'yı sembol anahtarına yeni bir atomik bildirim olarak ekleme ve öğrenci çözümünde (𝒜 ∧ B) yazma. Bu, nesne diliyle üst dili karıştırır.",
                [
                    (
                        "A",
                        "TFL nesne dilinin belirli atomik cümlesidir ve bir sembol anahtarında doğal dil bildirimiyle eşlenebilir.",
                    ),
                    (
                        "𝒜",
                        "Üst dilde genel cümle değişkenidir; TFL sembol anahtarına girmez.",
                    ),
                    (
                        "𝒜 yerine (A ∨ ¬B) koymak",
                        "Kurucu kuralın genel şemasını belirli bir TFL cümlesine uygulamaktır; ortaya çıkan nesne dili cümlesi ¬(A ∨ ¬B) olur.",
                    ),
                ],
                (
                    "Belirli nesne dili cümlesiyle herhangi bir cümleyi anan üst değişkeni yazı tipi ve görev bakımından ayırmak.",
                    "𝒜 ve ℬ'yi A ve B gibi yeni atomik TFL cümleleri sanmak.",
                    "Üst değişkenler TFL hakkında genel kural kurmamızı sağlar; TFL cümlelerinin parçaları değildir.",
                ),
            ),
            _section(
                "Ana bağlaç son kurucu adımı gösterir",
                "Karmaşık bir TFL cümlesinin ana bağlacı soldan görülen ilk işaret değil, bütün cümleyi kuran son adımda eklenen bağlaçtır.",
                "Bir cümlenin en üst yapısını, doğrudan alt cümlelerini ve oluşum ağacının ilk dallanmasını bulurken.",
                "((A ∨ B) → ¬C) cümlesinde son adım koşuldur; ana bağlaç →, doğrudan alt cümleler (A ∨ B) ve ¬C'dir.",
                "Oluşum ağacını kökten yapraklara doğru çöz: ana bağlacı kaldırınca geriye bir tekli veya iki tam doğrudan alt cümle kalmalıdır.",
                "En soldaki bağlacı ana bağlaç sanma. ¬A ∧ B rahat yazımında ilk işaret ¬ olsa da katı yapı (¬A ∧ B), ana bağlaç ∧'dir.",
                [
                    (
                        "¬(A ∧ B)",
                        "Son adım bütün birleşimi olumsuzlamaktır; ana bağlaç en soldaki ¬, doğrudan alt cümle (A ∧ B)'dir.",
                    ),
                    (
                        "(¬A ∧ B)",
                        "Son adım ¬A ile B'yi birleştirmektir; ana bağlaç ∧, doğrudan alt cümleler ¬A ve B'dir.",
                    ),
                    (
                        "((A ∨ B) → ¬C)",
                        "Ana bağlaç →; sol doğrudan alt cümle (A ∨ B), sağ doğrudan alt cümle ¬C'dir.",
                    ),
                ],
                (
                    "Cümleyi üreten son kurucu adımı bulup doğrudan alt cümlelere ayırmak.",
                    "Soldan sağa tararken karşılaşılan ilk bağlacı ana bağlaç seçmek.",
                    "Ana bağlaç görsel konum değil oluşum ağacındaki kök görevidir.",
                ),
            ),
            _section(
                "Parantez uzlaşımı iç yapıyı silme izni değildir",
                "Katı tanımda ikili bağlaçla kurulan her cümlenin dış parantezi vardır; okunabilirlik için yalnız bütün cümlenin en dış parantez çifti düşürülebilir.",
                "Daha önce rahat yazılmış formülleri katı biçime geri döndürürken ve karmaşık cümleyi başka bir cümleye gömerken.",
                "Katı: (A ∧ B). Rahat: A ∧ B. Gömülü kullanım: ¬(A ∧ B); iç parantez geri gelmelidir.",
                "A → B → C gibi bir dizi, öncelik uzlaşımı olmadan hangi koşulun önce kurulduğunu göstermez. Bu program sessiz bağlaç önceliği kullanmaz; (A → (B → C)) ile ((A → B) → C) ayrı yazılır.",
                "Dış parantezi düşürme iznini bütün iç parantezleri kaldırma izni sanma. Kapsamı değiştiren hiçbir parantez düşürülemez.",
                [
                    (
                        "A ∧ B",
                        "Katı tanımda yalnız ifadedir; programın açık rahat yazım uzlaşımıyla bütün cümlenin dış parantezi düşürülmüş kabul edilir.",
                    ),
                    (
                        "¬A ∧ B",
                        "Rahat yazımın katı biçimi (¬A ∧ B)'dir; olumsuzlama yalnız A'yı kapsar.",
                    ),
                    (
                        "¬(A ∧ B)",
                        "İç parantez zorunludur; kaldırılırsa olumsuzlamanın kapsamı değişir.",
                    ),
                    (
                        "A → B → C",
                        "Sessiz öncelik kullanılmadığından kabul edilmez; amaçlanan kurucu yapı parantezle seçilmelidir.",
                    ),
                ],
                (
                    "Rahat yazımı çözümlemeden önce tam katı parantezli biçime geri getirmek.",
                    "Dış parantez uzlaşımını kullanarak iç kapsam parantezlerini de silmek.",
                    "Parantez, cümlenin kurucu tarihini ve bağlaç kapsamını taşır.",
                ),
            ),
            _section(
                "Kapsam oluşum ağacındaki alt cümledir",
                "Bir bağlacın kapsamı, o bağlacın ana bağlaç olduğu en kısa alt cümledir; aynı işaret türünün farklı örnekleri ayrı kapsamlara sahip olabilir.",
                "Bir cümledeki her bağlacın tam olarak hangi parçayı kurduğunu işaretlerken.",
                "((A ∨ B) → ¬C): → kapsamı bütün cümle; ∨ kapsamı (A ∨ B); ¬ kapsamı ¬C.",
                "Önce oluşum ağacını kur, sonra her bağlacı kendi düğümüne bağla. Böylece kapsam yalnız çizgisel yakınlığa göre tahmin edilmez.",
                "Olumsuzlamanın yalnız sonraki harfi mi yoksa parantezli bütün yapıyı mı etkilediğini görsel mesafeyle değil alt cümle sınırıyla belirle.",
                [
                    (
                        "¬(A ∨ (B ∧ C))",
                        "Dış ¬ kapsamı bütün cümle; ∨ kapsamı (A ∨ (B ∧ C)); ∧ kapsamı (B ∧ C)'dir.",
                    ),
                    (
                        "((¬A ∨ B) ↔ C)",
                        "↔ kapsamı bütün cümle; ∨ kapsamı (¬A ∨ B); ¬ kapsamı ¬A'dır.",
                    ),
                ],
                (
                    "Her bağlaç örneğini ana bağlaç olduğu en kısa alt cümleyle eşlemek.",
                    "Aynı sembol türündeki bütün bağlaçların kapsamını tek ve ortak sanmak.",
                    "Kapsam bağlaç türüne değil, o bağlaç örneğinin oluşum ağacındaki yerine bağlıdır.",
                ),
            ),
        ],
        [
            _worked(
                "A",
                "Temel madde gereği her cümle harfi atomik TFL cümlesidir.",
                "Atomik cümle",
            ),
            _worked(
                "¬∧A",
                "Yalnız TFL sembollerinden oluşan bir ifadedir; ¬ sonrasında tam TFL cümlesi bulunmadığı için cümle değildir.",
                "Yalnız ifade",
                "bad",
            ),
            _worked(
                "(A)",
                "Parantezleri dengeli olsa da tek cümleyi paranteze alma kurucu kuralı yoktur.",
                "Kuralsız",
                "bad",
            ),
            _worked(
                "A, B, (A ∧ B), ¬(A ∧ B)",
                "Dizi atomik maddelerden başlayıp ikili ve tekli kurallarla adım adım kurulur.",
                "Oluşum kanıtı",
            ),
            _worked(
                "((A ∨ B) → ¬C)",
                "Son kurucu adım → olduğu için ana bağlaç koşuldur; iki doğrudan alt cümle (A ∨ B) ile ¬C'dir.",
                "Ana bağlaç",
            ),
            _worked(
                "¬(A ∧ B) / (¬A ∧ B)",
                "İlk cümlenin ana bağlacı ¬, ikincinin ∧'dir; aynı semboller farklı oluşum ağacı kurar.",
                "Kapsam karşılaştırması",
            ),
            _worked(
                "A → B → C",
                "Bu program sessiz öncelik uzlaşımı kullanmaz; kurucu yapı parantezlenmediği için kabul edilmez.",
                "Belirsiz dizi",
                "bad",
            ),
            _worked(
                "A / 𝒜",
                "A nesne dilinde belirli atomik cümle, 𝒜 üst dilde herhangi bir TFL cümlesi için üst değişkendir.",
                "Dil düzeyi",
            ),
        ],
        [
            "TFL alfabesindeki sembollerden oluşan her ifadeyi TFL cümlesi saymak.",
            "Dengeli parantezi iyi kurulmuşluk için yeterli görmek.",
            "Kurucu tanımın 'bunların dışında hiçbir şey' kapanış maddesini atlamak.",
            "Ana bağlacı soldan görülen ilk bağlaç sanmak.",
            "Yalnız en dış parantezi düşürme iznini iç parantezleri de silme izni saymak.",
            "A → B → C gibi dizileri açıklanmamış bağlaç önceliğiyle kabul etmek.",
            "𝒜 ve ℬ üst değişkenlerini TFL nesne dilinin atomik cümleleri sanmak.",
            "Kapsamı oluşum ağacı yerine sembollerin görsel yakınlığıyla tahmin etmek.",
        ],
        _practice(
            [
                (
                    "Hangisi atomik bir TFL cümlesidir?",
                    ["A", "𝒜", "(A)", "¬"],
                    "A",
                    "A nesne dilinin cümle harfidir; diğerleri atomik TFL cümlesi değildir.",
                    "Temel",
                ),
                (
                    "¬∧A dizisi neden TFL cümlesi değildir?",
                    [
                        "Hiç TFL sembolü içermediği için",
                        "¬ işaretinden sonra tam TFL cümlesi gelmediği için",
                        "A harfi küçük olmadığı için",
                        "Parantezi dengeli olduğu için",
                    ],
                    "¬ işaretinden sonra tam TFL cümlesi gelmediği için",
                    "Olumsuzlama kuralı yalnız daha önce cümle olduğu gösterilmiş bir yapıya uygulanabilir.",
                    "Temel",
                ),
                (
                    "(A) neden katı anlamda TFL cümlesi değildir?",
                    [
                        "A cümle harfi olmadığı için",
                        "Tek bir cümleyi yalnız paranteze alarak yeni cümle üretme kuralı olmadığı için",
                        "Parantezler eşleşmediği için",
                        "Her cümlede bağlaç bulunması gerektiği için",
                    ],
                    "Tek bir cümleyi yalnız paranteze alarak yeni cümle üretme kuralı olmadığı için",
                    "Dengeli parantez kurucu tanımda bulunmayan bir üretim adımını meşrulaştırmaz.",
                    "Orta",
                ),
                (
                    "Kurucu tanımın kapanış maddesi ne söyler?",
                    [
                        "Her TFL ifadesi cümledir",
                        "Yalnız atomik cümleler vardır",
                        "Temel ve kurucu maddelerle üretilmeyen hiçbir dizi TFL cümlesi değildir",
                        "Parantezler isteğe bağlıdır",
                    ],
                    "Temel ve kurucu maddelerle üretilmeyen hiçbir dizi TFL cümlesi değildir",
                    "Bu madde tanımın yalnız izin verilen üretimleri kabul etmesini sağlar.",
                    "Orta",
                ),
                (
                    "¬(A ∧ B) cümlesinin ana bağlacı hangisidir?",
                    ["İlk A", "¬", "∧", "B"],
                    "¬",
                    "Bütün cümleyi kuran son adım, (A ∧ B) alt cümlesinin olumsuzlanmasıdır.",
                    "Temel",
                ),
                (
                    "(¬A ∧ B) cümlesinin ana bağlacı hangisidir?",
                    ["¬", "∧", "A", "B"],
                    "∧",
                    "Son adım ¬A ile B tam cümlelerini birleşim içinde bir araya getirir.",
                    "Orta",
                ),
                (
                    "((A ∨ B) → ¬C) cümlesinin doğrudan alt cümleleri hangileridir?",
                    [
                        "A ve B",
                        "(A ∨ B) ve ¬C",
                        "A ve ¬C",
                        "B ve C",
                    ],
                    "(A ∨ B) ve ¬C",
                    "Ana bağlaç → kaldırıldığında iki tam doğrudan alt cümle kalır.",
                    "Orta",
                ),
                (
                    "A → B rahat yazımı katı biçimde nasıl yazılır?",
                    ["(A → B)", "A(→B)", "((A) → (B))", "¬(A → B)"],
                    "(A → B)",
                    "Rahat uzlaşım yalnız bütün cümlenin en dış parantez çiftini düşürür.",
                    "Temel",
                ),
                (
                    "A → B → C dizisi bu programda neden kabul edilmez?",
                    [
                        "Üç cümle harfi içerdiği için",
                        "Koşul işareti kullanılamadığı için",
                        "Hangi iki cümlenin önce birleştiğini gösteren parantez bulunmadığı ve sessiz öncelik kullanılmadığı için",
                        "C harfi yalnız niceleyicilerde kullanıldığı için",
                    ],
                    "Hangi iki cümlenin önce birleştiğini gösteren parantez bulunmadığı ve sessiz öncelik kullanılmadığı için",
                    "(A → (B → C)) ile ((A → B) → C) ayrı kurucu yapılardır.",
                    "İleri",
                ),
                (
                    "A ile 𝒜 arasındaki görev farkı hangisidir?",
                    [
                        "İkisi de aynı atomik TFL cümlesidir",
                        "A nesne dilinde belirli cümle harfi, 𝒜 üst dilde herhangi bir TFL cümlesi için üst değişkendir",
                        "A bağlaç, 𝒜 parantezdir",
                        "A yalnız yanlış, 𝒜 yalnız doğru cümleleri gösterir",
                    ],
                    "A nesne dilinde belirli cümle harfi, 𝒜 üst dilde herhangi bir TFL cümlesi için üst değişkendir",
                    "Üst değişken kurucu kuralları genel yazmak için kullanılır ve TFL alfabesine ait değildir.",
                    "İleri",
                ),
                (
                    "¬(A ∨ (B ∧ C)) içinde ∧ bağlacının kapsamı hangisidir?",
                    ["B", "C", "(B ∧ C)", "¬(A ∨ (B ∧ C))"],
                    "(B ∧ C)",
                    "Bu ∧ örneği, (B ∧ C) alt cümlesinin ana bağlacıdır.",
                    "İleri",
                ),
                (
                    "Bir cümlenin ana bağlacını bulmanın kavramsal olarak en güvenilir yolu hangisidir?",
                    [
                        "Soldan ilk bağlacı seçmek",
                        "En çok tekrarlanan bağlacı seçmek",
                        "Cümleyi kuran son adımı ve oluşum ağacının kökünü bulmak",
                        "Parantezleri kaldırmak",
                    ],
                    "Cümleyi kuran son adımı ve oluşum ağacının kökünü bulmak",
                    "Ana bağlaç çizgisel konum değil kurucu görevdir.",
                    "Zor",
                ),
            ],
        ),
        {
            "prompt": "((A ∨ B) → ¬C) cümlesinin oluşum ağacını tamamla; ana bağlacı, doğrudan alt cümleleri ve her bağlacın kapsamını yaz.",
            "starter": "Yapraklar: A, B, C.\nİlk kurucu adım: A ve B'den (A ∨ B).\nİkinci kurucu adım: C'den ¬C.",
            "checks": [
                "Her yaprak bir atomik cümle harfidir",
                "Her iç düğüm kurucu tanımın tekli veya ikili maddelerinden biriyle oluşturulmuştur",
                "Ana bağlaç son kurucu adımdaki → olarak gösterilmiştir",
                "Doğrudan alt cümleler (A ∨ B) ve ¬C olarak ayrılmıştır",
                "∨, ¬ ve → örneklerinin kapsamları ayrı ayrı yazılmıştır",
                "𝒜 veya ℬ nesne dili cümlesinin parçası yapılmamıştır",
            ],
            "solution": "A ve B, (A ∨ B)'yi; C, ¬C'yi kurar. Son adım bu iki tam cümleyi ((A ∨ B) → ¬C) içinde birleştirir. Ana bağlaç →'dir. → kapsamı bütün cümle, ∨ kapsamı (A ∨ B), ¬ kapsamı ¬C'dir.",
        },
        [
            _production_task(
                "Sekiz diziyi katı TFL cümlesi, yalnız dış-parantez uzlaşımıyla kabul edilen cümle veya TFL ifadesi fakat cümle değil diye sınıflandır. Her kararı kurucu maddeyle ya da tıkanan adımla gerekçelendir; iki geçerli karmaşık cümlenin oluşum ağacını ve kapsamlarını çıkar.",
                [
                    "Her kabul kararında temel veya kurucu maddeyi numarası ve kullandığı tam alt cümlelerle belirt.",
                    "Her ret kararında ilk hangi parçada kurucu tanımın uygulanamadığını göster.",
                    "Rahat yazımları çözümlemeden önce katı dış parantezli biçime geri getir.",
                    "Seçtiğin iki karmaşık cümleyi atomik yapraklara kadar oluşum ağacında çöz.",
                    "Her iki ağaçta ana bağlacı, doğrudan alt cümleleri ve bütün bağlaç kapsamlarını işaretle.",
                    "A nesne dili harfiyle 𝒜 üst değişkeninin farkını görevin sonunda iki cümleyle açıkla.",
                ],
                "Yalnız parantez dengesi veya görsel benzerlik değil, üretilebilirlik ve dil düzeyi üzerinden gerekçe ver.",
                "Sınıflandırılacak diziler",
                [
                    "A",
                    "¬¬A",
                    "(A ∧ ¬B)",
                    "A ∧ ¬B",
                    "((A ∨ B) → ¬C)",
                    "A → B → C",
                    "¬∧A",
                    "(A)",
                ],
                "İlk beş diziden hangilerinin katı, hangilerinin yalnız rahat uzlaşımla kabul edildiğini açıkça ayır; son üç dizide tıkanan kurucu adımı göster.",
            ),
        ],
        [
            "Öğrenci TFL ifadesi ile TFL cümlesini yalnız görünüşe veya parantez sayısına başvurmadan kurucu tanımla ayırır.",
            "Kurucu tanımın temel, tekli, ikili ve 'bunların dışında hiçbir şey' kapanış maddelerini eksiksiz uygular.",
            "En az iki karmaşık TFL cümlesini atomik yapraklara kadar doğru oluşum ağacına ayırır.",
            "Ana bağlacı soldaki ilk bağlaçtan en az bir örnekte doğru ayırır ve doğrudan alt cümleleri belirtir.",
            "Her bağlaç örneğini ana bağlaç olduğu en kısa alt cümleyle doğru kapsam olarak eşler.",
            "Yalnız en dış parantezi düşürme uzlaşımını iç parantezleri silmeden uygular ve rahat biçimi katı biçime geri döndürür.",
            "A ve 𝒜 işaretlerini nesne dili/üst dil görevleri bakımından açıkça ayırır; 𝒜'yı sembol anahtarına yazmaz.",
        ],
        [
            "TFL sembollerinden oluşan her ifade neden TFL cümlesi değildir?",
            "Ana bağlaç cümlenin hangi kurucu adımını gösterir?",
            "A ile 𝒜 hangi iki dil düzeyinde hangi görevleri üstlenir?",
            "Dış parantezi düşürme uzlaşımı hangi parantezleri kaldırmana izin vermez?",
        ],
        "Sonraki derste doğal dilde birden fazla okuma taşıyan cümleleri önce açık Türkçe okumalara, sonra bu kesin TFL yapılarından ayrı ayrı uygun olanlara dönüştüreceğiz.",
        ["forallx-tfl-sentences"],
        "Bu ders yalnız sözdizimi öğretir. Tümevarımsal yapı daha sonra semantik ve kanıt yöntemlerinin altyapısı olacaktır; burada bir cümlenin değerini hesaplamak veya çıkarım lisansı vermek için kullanılmaz.",
        [
            "ders-kullanim-anma-ve-dil-duzeyleri",
            "ders-20-dogruluk-tablolari-i",
        ],
    )

    lesson["reading_note"] = (
        "Bir diziyi çözmeden önce rahat yazımı katı parantezli biçime getir; sonra son kurucu adımı bulup her dalı atomik harfe kadar izle."
    )
    lesson["symbol_set"] = [
        "A",
        "A₁",
        "¬",
        "∧",
        "∨",
        "→",
        "↔",
        "(",
        ")",
    ]
    lesson["proof_tools"] = [
        "Kurucu tanım denetimi",
        "Katı paranteze geri döndürme",
        "Oluşum ağacı",
        "Ana bağlaç ayırma",
        "Kapsam eşleme",
        "Nesne dili-üst dil denetimi",
    ]
    return lesson


def _candidate_b12():
    lesson = _lesson(
        "B12",
        "ders-belirsizlik-bulaniklik-savunulabilir-okumalar",
        "Belirsizlik, Bulanıklık ve Savunulabilir Okumalar",
        "Doğal dildeki birden fazla savunulabilir okumayı tek formüle zorlamadan açık ara cümleler, sembol anahtarları ve ayrı TFL cümleleriyle gösterir.",
        "Doğal dil belirsizliği ve TFL'nin açıklık sınırı",
        35,
        ["ders-tfl-cumlesi-ana-baglac-ve-kapsam"],
        [
            "language.ambiguity_detect",
            "language.reading_disambiguate",
            "tfl.multiple_symbolizations",
            "language.vagueness_distinguish",
        ],
        [
            "Sözcüksel, yapısal ve kapsam belirsizliğini doğal Türkçe örneklerde birbirinden ayırmak.",
            "Her savunulabilir okumayı sembolleştirmeden önce tek anlamlı bir Türkçe ara cümleyle açıklaştırmak.",
            "Aynı yüzey cümlesinin farklı okumalarını gerektiğinde farklı sembol anahtarları ve ayrı TFL cümleleriyle göstermek.",
            "Bağlamın bir okumayı desteklemesi ile başka bir okumanın dilbilgisel olarak imkânsız olması arasındaki farkı açıklamak.",
            "Belirsizliği, sınır vakaları bulunan bulanık yüklemlerden ayırmak ve TFL'deki bilgi kaybını belirtmek.",
        ],
        [
            (
                "Belirsizlik",
                "Tek bir doğal dil ifadesinin aynı bağlam açıklığa kavuşmadan önce birden fazla belirli ve savunulabilir okuma taşıması.",
            ),
            (
                "Sözcüksel belirsizlik",
                "Bir sözcük veya biçimin birden fazla anlamı nedeniyle cümlenin farklı bildirimler ifade edebilmesi.",
            ),
            (
                "Yapısal belirsizlik",
                "Sözcüklerin farklı dilbilgisel gruplara bağlanabilmesi nedeniyle birden fazla okuma oluşması.",
            ),
            (
                "Kapsam belirsizliği",
                "Olumsuzlama veya bağlacın hangi cümle parçasını kapsadığının yüzey biçiminden tek olarak belirlenememesi.",
            ),
            (
                "Bulanıklık",
                "Bir ifadenin tek bir genel anlamı olsa bile hangi sınır vakalarına uygulanacağının keskin olmaması.",
            ),
            (
                "Açık ara okuma",
                "Yüzey cümlesinin tek bir amaçlanan anlamını belirsizliği kaldıracak biçimde yeniden yazan doğal dil cümlesi.",
            ),
            (
                "Bağlam desteği",
                "Konuşma durumu, önceki cümleler veya vurgu nedeniyle bir okumanın diğerlerinden daha olası hale gelmesi; mantıksal zorunluluk değildir.",
            ),
        ],
        [
            _section(
                "Belirsizlik tek cevabı bilmemek değildir",
                "Belirsiz bir cümle, eksik bilgi yüzünden cevabı bilinmeyen cümle değildir; aynı yüzey biçimi birden fazla belirli bildirim ifade edebilir.",
                "Bir cümle için iki farklı sembolleştirme önerisi ortaya çıktığında önce bunların hata mı, yoksa iki ayrı okuma mı olduğunu sınarken.",
                "Yüzey cümlesi → açık okuma 1 / açık okuma 2 → ayrı anahtar ve TFL cümlesi",
                "Her okuma önce belirsiz olmayan Türkçe bir ara cümlede yazılır. Formel gösterim, seçilen okumayı kesinleştirir; hangi okumanın gerçekten amaçlandığını kendi başına keşfetmez.",
                "En alışıldık okumayı tek dilbilgisel olarak mümkün okuma sayma. Olasılık, tekillik değildir.",
                [
                    (
                        "Film uzun ve sıkıcı değil.",
                        "'Film hem uzun hem sıkıcı değildir' ile 'Film uzun değildir ve sıkıcıdır' ayrı belirli okumalardır.",
                    ),
                    (
                        "Bağlamda film üç saat sürüyor denmesi",
                        "Bu bilgi bir okumayı zayıflatabilir; cümlenin diğer okumasını geriye dönük olarak dilbilgisi dışı yapmaz.",
                    ),
                ],
                (
                    "Her formülün önüne onu karşılayan açık Türkçe okumayı yazmak.",
                    "Formülü doğrudan yüzey cümlesine bağlayıp hangi okumayı temsil ettiğini söylememek.",
                    "Bir sembolleştirmenin doğruluğu yalnız işaret dizisine değil, açık okuma ile formülün uyumuna bağlıdır.",
                ),
            ),
            _section(
                "Sözcüksel ve yapısal belirsizliği Türkçede sınamak",
                "Türkçede aynı ses veya yazı biçimi farklı sözcükleri karşılayabilir; ayrıca ad öbekleri ve örtük özneler farklı yapılara izin verebilir.",
                "Formüllerden önce sembol anahtarının bile değişmesi gerekip gerekmediğini belirlerken.",
                "Önce her okumayı tam cümleyle yaz; aynı atomik bildirim değilse ayrı anahtar satırı kullan.",
                "'Kazı gördüm' cümlesinde kazı, bir kazı çalışması veya belirli bir kaz olabilir. 'Çocuk kitabı aldı' ise çocuğun belirli kitabı alması ya da örtük bir öznenin çocuk kitabı alması biçiminde çözümlenebilir.",
                "İngilizcedeki bir çok anlamlılık örneğini Türkçede aynıymış gibi kullanma. Belirsizlik hedef dilin gerçek biçiminden doğmalıdır.",
                [
                    (
                        "Kazı gördüm. — Okuma 1: Bir kazı çalışması gördüm.",
                        "A: Konuşan kişi bir kazı çalışması gördü. Bu okuma atomik A ile gösterilebilir.",
                    ),
                    (
                        "Kazı gördüm. — Okuma 2: Belirli bir kazı gördüm.",
                        "B: Konuşan kişi belirli bir kaz gördü. Aynı yüzey biçimi başka bir atomik bildirim gerektirir.",
                    ),
                    (
                        "Çocuk kitabı aldı.",
                        "'Çocuk belirli kitabı aldı' ve 'Örtük özne bir çocuk kitabı aldı' farklı dilbilgisel gruplamalardır.",
                    ),
                ],
                (
                    "Her okumanın özne, nesne ve sözcük anlamını açık ara cümlede görünür kılmak.",
                    "Aynı harfi iki farklı atomik bildirime verip belirsizliği anahtarın içine taşımak.",
                    "Sembol anahtarı belirsizliği yeniden üretmemeli; her satır tek belirli bildirimi karşılamalıdır.",
                ),
            ),
            _section(
                "Kapsam belirsizliğini parantezle görünür kılmak",
                "Olumsuzlama, birleşim ve ayrık bağlaç doğal dilde parantezsiz göründüğünde aynı sözcük dizisi farklı oluşum ağaçlarına izin verebilir.",
                "İki okumanın aynı atomik anahtarı paylaşıp farklı ana bağlaç veya kapsam gerektirdiği durumlarda.",
                "Açık okuma → ana bağlaç → doğrudan alt cümleler → katı parantezli TFL cümlesi",
                "L: Film uzundur; S: Film sıkıcıdır. 'İkisinin birden doğru olduğu söylenemez' okuması ¬(L ∧ S), 'uzun değil ama sıkıcı' okuması (¬L ∧ S) olur.",
                "Sembolleri aynı sırada tutup yalnız sezgiye güvenme. Farklı okumalar, oluşum ağacında gerçekten farklı bir ana bağlaç veya kapsam göstermelidir.",
                [
                    (
                        "Film hem uzun hem sıkıcı değildir.",
                        "¬(L ∧ S): ana bağlaç ¬; bütün birleşim olumsuzlamanın kapsamındadır.",
                    ),
                    (
                        "Film uzun değildir ve sıkıcıdır.",
                        "(¬L ∧ S): ana bağlaç ∧; olumsuzlama yalnız L'yi kapsar.",
                    ),
                    (
                        "Ada ve Bora veya Cem sunum yapacak.",
                        "((A ∧ B) ∨ C) ile (A ∧ (B ∨ C)) iki ayrı gruplamadır; açık ara okumalar yazılmadan yalnız formüller yeterli değildir.",
                    ),
                    (
                        "Ada ve Bora gelmedi.",
                        "¬(A ∧ B) 'ikisi birden gelmedi'; (¬A ∧ ¬B) 'ikisi de gelmedi' okumasını taşır.",
                    ),
                ],
                (
                    "Her parantezlemenin doğal dildeki açık karşılığını ve ana bağlacını birlikte vermek.",
                    "Aynı Türkçe ara cümleyi iki farklı formülün açıklaması olarak tekrar etmek.",
                    "Farklı formüller, gerçekten farklı belirli okumaları temsil ettikleri ölçüde birlikte savunulabilir.",
                ),
            ),
            _section(
                "Bulanıklık parantez sorunu değildir",
                "'Uzun', 'genç' ve 'kalabalık' gibi yüklemler tek bir genel anlam taşısa da bağlam belirlendikten sonra bile sınır vakaları bırakabilir.",
                "Bir cümleye iki formül üretme isteğinin gerçek belirsizlikten mi, yoksa keskin olmayan uygulama sınırından mı kaynaklandığını sınarken.",
                "E: Ece uzundur. Atomik TFL cümlesi sınır ölçütünü görünür kılmaz.",
                "Kişiler için karşılaştırma sınıfı verilse bile tam hangi santimetreden itibaren 'uzun' deneceği keskin olmayabilir. Yeni parantezler bu eşiği belirlemez.",
                "Bulanık cümleye yapay iki okuma uydurma. Sorun cümlenin iki belirli anlamı değil, tek yüklemin sınır vakalarıdır.",
                [
                    (
                        "Ece uzundur.",
                        "Bağlam 'profesyonel basketbolcular arasında' diye daraltılabilir; yine de sınırda kalan boylar olabilir.",
                    ),
                    (
                        "Salon kalabalıktır.",
                        "Salon kapasitesi ve amaç eşik hakkında bilgi verir, fakat 'kalabalık' yükleminin bütün vakalarını otomatik keskinleştirmez.",
                    ),
                    (
                        "E / ¬E",
                        "Klasik TFL atomik cümleyi iki seçenekli kullanır; doğal dildeki sınır derecelerini harfin içinde göstermez.",
                    ),
                ],
                (
                    "Bulanık yüklemin karşılaştırma sınıfını ve kaybolan sınır bilgisini ayrıca raporlamak.",
                    "Sorunu (E ∧ ...) veya ¬(E ∧ ...) gibi yeni parantezlerle çözmeye çalışmak.",
                    "Parantez kapsamı belirler; bulanık yüklemin uygulama eşiğini belirlemez.",
                ),
            ),
            _section(
                "Bağlam okumayı destekler, kanıtlamaz",
                "Önceki konuşma, ortak bilgi, noktalama ve vurgu bir okumayı daha makul kılabilir; fakat sembolleştirme yazarın zihinsel niyetine doğrudan erişim sağlamaz.",
                "Alternatif okumalar arasında seçim yaparken ve gerekçenin gücünü doğru ifade ederken.",
                "Dilbilgisel olanak + bağlam kanıtı → tercih edilen okuma; bağlam desteği ≠ mantıksal zorunluluk",
                "Bir okuma ancak cümlenin dil yapısıyla uyumluysa adaydır. Bağlam adaylar arasında ağırlık verir; açık yeniden yazım ise seçilen adayı görünür hale getirir.",
                "'Yazar kesin bunu kastetti' diye formülden niyet sonucu çıkarma. Yalnız hangi okumanın hangi kanıtla daha iyi desteklendiğini söyle.",
                [
                    (
                        "Programda yalnız Cem'in tek başına sunabileceği yazıyorsa",
                        "((A ∧ B) ∨ C) okuması desteklenir; bu ek bilgi yüzey cümlesinin öteki yapısını dilbilgisi dışı yapmaz.",
                    ),
                    (
                        "Konuşmacı 'ikisi de gelmedi' diye düzeltiyorsa",
                        "Ada ve Bora gelmedi cümlesi için (¬A ∧ ¬B) okuması açıkça seçilmiş olur.",
                    ),
                ],
                (
                    "Bağlam kanıtını alıntılayıp hangi okumanın neden öne çıktığını olasılık diliyle açıklamak.",
                    "Bağlamın desteklediği okumayı tek mantıksal olarak mümkün okuma ilan etmek.",
                    "İyi çözüm, dilbilgisel olanak ile bağlamsal tercih arasındaki kanıt düzeyini korur.",
                ),
            ),
        ],
        [
            _worked(
                "Kazı gördüm: 'Bir kazı çalışması gördüm' / 'Belirli bir kazı gördüm'.",
                "Aynı yazı biçimi iki farklı sözcüksel çözümlemeye açılır; okumalar ayrı tam bildirim ve anahtar satırları gerektirir.",
                "Sözcüksel belirsizlik",
            ),
            _worked(
                "Çocuk kitabı aldı: 'Çocuk belirli kitabı aldı' / 'Bir kişi çocuk kitabı aldı'.",
                "Özne ve ad öbeğinin farklı gruplanması iki yapısal okuma üretir.",
                "Yapısal belirsizlik",
            ),
            _worked(
                "Film hem uzun hem sıkıcı değildir → ¬(L ∧ S).",
                "Olumsuzlama bütün birleşimi kapsar; filmde iki özelliğin birlikte bulunması reddedilir.",
                "Geniş kapsam",
            ),
            _worked(
                "Film uzun değildir ve sıkıcıdır → (¬L ∧ S).",
                "Olumsuzlama yalnız L'yi kapsar; ana bağlaç birleşimdir.",
                "Dar kapsam",
            ),
            _worked(
                "Ya Ada ile Bora birlikte sunacak ya da Cem sunacak → ((A ∧ B) ∨ C).",
                "Birinci açık okuma Ada-Bora çiftini tek ayrık seçenek olarak gruplayarak ana bağlacı ∨ yapar.",
                "Birinci gruplama",
            ),
            _worked(
                "Ada sunacak; ona Bora veya Cem eşlik edecek → (A ∧ (B ∨ C)).",
                "İkinci açık okuma A'yı zorunlu tutup B-C ayrıklığını sağ alt cümlede kurar.",
                "İkinci gruplama",
            ),
            _worked(
                "Ada ve Bora gelmedi → ¬(A ∧ B) / (¬A ∧ ¬B).",
                "'İkisi birden değil' ile 'ikisi de değil' aynı iddia değildir; açık ara okuma formül seçimini belirler.",
                "Kapsam karşılaştırması",
            ),
            _worked(
                "Ece uzundur.",
                "Tek bir genel yüklem vardır; sorun iki okuma değil, karşılaştırma sınıfı içinde kalabilen sınır vakalarıdır.",
                "Bulanıklık",
            ),
            _worked(
                "Ada gelmedi ve Bora kaldı → (¬A ∧ B).",
                "Açık bağlaç ve yerel olumsuzlama tek doğal oluşum ağacı verir; bu bir kontrol örneğidir.",
                "Belirsiz olmayan kontrol",
            ),
        ],
        [
            "En alışıldık okumayı tek mantıksal olarak mümkün okuma saymak.",
            "İki formül yazıp bu formüllere karşılık gelen açık Türkçe ara okumaları vermemek.",
            "Aynı sembol anahtarında bir harfi iki farklı atomik bildirime bağlamak.",
            "Sözcüksel belirsizliği yalnız yeni parantez ekleyerek çözmeye çalışmak.",
            "Bulanık 'uzun', 'genç' veya 'kalabalık' yüklemini kapsam belirsizliği sanmak.",
            "Bağlamın bir okumayı desteklemesini öteki okumanın dilbilgisel imkânsızlığı gibi sunmak.",
            "TFL cümlesinin konuşmacının gerçek niyetini kanıtladığını varsaymak.",
            "Her cümlede zorla belirsizlik arayıp açık kontrol cümlelerine gereksiz alternatifler üretmek.",
        ],
        _practice(
            [
                (
                    "Belirsiz bir cümleyi en iyi tanımlayan seçenek hangisidir?",
                    [
                        "Doğruluğu henüz bilinmeyen cümle",
                        "Birden fazla belirli ve savunulabilir okuma taşıyan cümle",
                        "Yalnız yanlış yazılmış cümle",
                        "İçinde her zaman bulanık sıfat bulunan cümle",
                    ],
                    "Birden fazla belirli ve savunulabilir okuma taşıyan cümle",
                    "Belirsizlik bilgi eksikliğinden değil, aynı yüzey biçiminin birden fazla belirli okuma taşımasından doğar.",
                    "Temel",
                ),
                (
                    "'Kazı gördüm' örneğindeki iki okuma hangi belirsizlik türünü gösterir?",
                    [
                        "Sözcüksel belirsizlik",
                        "Yalnız kapsam belirsizliği",
                        "Bulanıklık",
                        "Geçerlilik sorunu",
                    ],
                    "Sözcüksel belirsizlik",
                    "Kazı çalışması ile belirli kaz, aynı yüzey biçiminde iki farklı sözcüksel çözümlemedir.",
                    "Temel",
                ),
                (
                    "'Çocuk kitabı aldı' cümlesindeki temel ayrım hangisidir?",
                    [
                        "Çocuğun belirli kitabı alması ile örtük öznenin çocuk kitabı alması",
                        "Kitabın doğru veya yanlış olması",
                        "Çocuğun uzun veya kısa olması",
                        "Aynı formülün iki kez yazılması",
                    ],
                    "Çocuğun belirli kitabı alması ile örtük öznenin çocuk kitabı alması",
                    "Özne ve ad öbeği farklı gruplandığı için yapısal belirsizlik oluşur.",
                    "Orta",
                ),
                (
                    "L: Film uzundur; S: Film sıkıcıdır. 'Film hem uzun hem sıkıcı değildir' hangi formülle gösterilir?",
                    ["¬(L ∧ S)", "(¬L ∧ S)", "(L ∧ ¬S)", "(¬L ∧ ¬S)"],
                    "¬(L ∧ S)",
                    "Olumsuzlama, iki özelliğin birlikte bulunduğu bütün birleşimi kapsar.",
                    "Orta",
                ),
                (
                    "Aynı anahtarla 'Film uzun değildir ve sıkıcıdır' hangi formülle gösterilir?",
                    ["¬(L ∧ S)", "(¬L ∧ S)", "(L ∧ ¬S)", "¬S"],
                    "(¬L ∧ S)",
                    "Olumsuzlama yalnız L'yi kapsar; ana bağlaç ∧'dir.",
                    "Orta",
                ),
                (
                    "A, B ve C ilgili kişilerin sunum yapacağını göstersin. 'Ya Ada ile Bora birlikte sunacak ya da Cem sunacak' hangi yapıdır?",
                    ["((A ∧ B) ∨ C)", "(A ∧ (B ∨ C))", "¬(A ∧ B)", "(A ↔ C)"],
                    "((A ∧ B) ∨ C)",
                    "Ada-Bora birleşimi ayrık bağlacın sol doğrudan alt cümlesidir.",
                    "İleri",
                ),
                (
                    "'Ada sunacak; ona Bora veya Cem eşlik edecek' hangi yapıdır?",
                    ["((A ∧ B) ∨ C)", "(A ∧ (B ∨ C))", "((A ∨ B) ∧ C)", "¬(A ∨ C)"],
                    "(A ∧ (B ∨ C))",
                    "Ada'nın sunması dış birleşimde sabit, Bora-Cem seçeneği iç ayrık cümlededir.",
                    "İleri",
                ),
                (
                    "'Ece uzundur' cümlesindeki sınır vakası neden yeni parantezle çözülemez?",
                    [
                        "Parantez bağlaç kapsamını gösterir, 'uzun' yükleminin uygulama eşiğini belirlemez",
                        "Ece hakkında hiçbir önerme kurulamaz",
                        "Her atomik cümle belirsizdir",
                        "Uzun sözcüğü bir bağlaçtır",
                    ],
                    "Parantez bağlaç kapsamını gösterir, 'uzun' yükleminin uygulama eşiğini belirlemez",
                    "Bulanıklık, oluşum ağacı değil yüklemin sınır uygulaması sorunudur.",
                    "Orta",
                ),
                (
                    "Bağlam bir okumayı güçlü biçimde destekliyorsa hangi sonuç savunulabilir?",
                    [
                        "Bu okuma tercih edilebilir, fakat diğer dilbilgisel okumalar sırf bu yüzden imkânsız olmaz",
                        "Diğer bütün okumalar mantıksal çelişki olur",
                        "Sembol anahtarına gerek kalmaz",
                        "Konuşmacının niyeti kesin olarak kanıtlanır",
                    ],
                    "Bu okuma tercih edilebilir, fakat diğer dilbilgisel okumalar sırf bu yüzden imkânsız olmaz",
                    "Bağlam kanıtı olasılık ağırlığı verir; dilbilgisel olanak ile mantıksal zorunluluk aynı değildir.",
                    "İleri",
                ),
                (
                    "İki farklı formülün aynı yüzey cümlesi için birlikte savunulabilir olmasının gerekli koşulu nedir?",
                    [
                        "Her formülün farklı ve dilbilgisel olarak mümkün açık bir okumayla uyumlu olması",
                        "İki formülün aynı işaret dizisi olması",
                        "Formüllerin anahtarsız yazılması",
                        "En uzun formülün seçilmesi",
                    ],
                    "Her formülün farklı ve dilbilgisel olarak mümkün açık bir okumayla uyumlu olması",
                    "Alternatif çözüm, açık okuma-formül uyumuyla gerekçelendirilir.",
                    "İleri",
                ),
                (
                    "Sözcüksel belirsizlikte sembol anahtarı için en güvenli tutum hangisidir?",
                    [
                        "Her belirli atomik okuma için ayrı ve tek anlamlı bir anahtar satırı kurmak",
                        "Aynı harfe iki anlam vermek",
                        "Anahtarı tamamen kaldırmak",
                        "Her sözcüğe ayrı cümle harfi vermek",
                    ],
                    "Her belirli atomik okuma için ayrı ve tek anlamlı bir anahtar satırı kurmak",
                    "Anahtar belirsizliği saklamamalı, seçilen bildirimi açıklaştırmalıdır.",
                    "Orta",
                ),
                (
                    "'Ada gelmedi ve Bora kaldı' neden iyi bir kontrol örneğidir?",
                    [
                        "Yerel olumsuzlama ile açık birleşim tek bir amaçlanan oluşum ağacını görünür kıldığı için",
                        "Her zaman iki sözcüksel anlam taşıdığı için",
                        "'Kaldı' bulanık bir sıfat olduğu için",
                        "Hiç TFL cümlesi kurulamadığı için",
                    ],
                    "Yerel olumsuzlama ile açık birleşim tek bir amaçlanan oluşum ağacını görünür kıldığı için",
                    "Belirsizlik çözümlemesi, açık cümleleri de doğru biçimde açık olarak sınıflandırabilmelidir.",
                    "Zor",
                ),
            ],
        ),
        {
            "prompt": "'Ada ve Bora veya Cem sunum yapacak' ile 'Ada ve Bora sunum yapmadı' cümlelerinin ikişer savunulabilir okumasını açık Türkçeyle yaz ve her okumayı katı parantezli TFL cümlesine dönüştür.",
            "starter": "Anahtar: A: Ada sunum yapacak. B: Bora sunum yapacak. C: Cem sunum yapacak. İkinci cümlede A ve B aynı kişilerin sunum yapmasını göstersin.",
            "checks": [
                "İlk yüzey cümlesi için ((A ∧ B) ∨ C) ve (A ∧ (B ∨ C)) yapılarını karşılayan iki farklı açık Türkçe okuma yazılmıştır",
                "İkinci yüzey cümlesi için ¬(A ∧ B) ile (¬A ∧ ¬B) arasındaki 'ikisi birden değil/ikisi de değil' ayrımı açıkça yazılmıştır",
                "Her formülün ana bağlacı ve doğrudan alt cümleleri doğru belirtilmiştir",
                "Formüller rahat önceliğe bırakılmadan katı parantezlenmiştir",
                "Bir okumanın daha olası görülmesi, diğerinin dilbilgisel imkânsızlığı diye sunulmamıştır",
            ],
            "solution": "Birinci cümle: 'Ya Ada ile Bora birlikte sunum yapacak ya da Cem yapacak' → ((A ∧ B) ∨ C); 'Ada sunum yapacak ve ona Bora veya Cem eşlik edecek' → (A ∧ (B ∨ C)). İkinci cümle: 'Ada ile Bora'nın ikisinin birden sunum yaptığı doğru değil' → ¬(A ∧ B); 'Ada sunum yapmadı ve Bora sunum yapmadı' → (¬A ∧ ¬B).",
        },
        [
            _production_task(
                "Altı yüzey cümlesini önce belirsizlik türü, bulanıklık veya belirsiz olmayan kontrol diye sınıflandır. En az üç belirsiz cümle için bütün savunulabilir okumaları açık Türkçeyle yaz, tek anlamlı sembol anahtarı kur ve ayrı TFL cümleleri üret. Bulanık örneğin neden aynı yöntemle çözülemeyeceğini ve ek bağlamın hangi okumayı neden desteklediğini ayrıca açıkla.",
                [
                    "Her cümleyi sözcüksel, yapısal, kapsam, bulanık veya belirsiz olmayan kontrol olarak gerekçeli sınıflandır.",
                    "Belirsiz her örnekte formülden önce tek anlamlı açık Türkçe ara okumaları yaz.",
                    "Sözcüksel okumalar farklı atomik bildirimlerse aynı harfe iki anlam vermeden ayrı anahtar satırları kur.",
                    "Yapısal ve kapsam okumalarını katı parantezli ayrı TFL cümleleriyle göster.",
                    "Bulanık örnekte karşılaştırma sınıfını ve TFL'de kaybolan sınır bilgisini belirt; yapay parantez üretme.",
                    "Kontrol cümlesine gereksiz ikinci okuma uydurma.",
                    "Seçtiğin bir örneğe bağlam ekle; bu bağlamın bir okumayı desteklediğini fakat konuşmacı niyetini mantıksal olarak kanıtlamadığını yaz.",
                ],
                "Değerlendirme tek bir cevap dizisini değil, sınıflandırma, açık okuma, sembol anahtarı ve formül arasındaki tutarlılığı arar.",
                "İncelenecek cümleler",
                [
                    "Kazı gördüm.",
                    "Çocuk kitabı aldı.",
                    "Film uzun ve sıkıcı değil.",
                    "Ada ve Bora veya Cem sunum yapacak.",
                    "Ece uzundur.",
                    "Ada gelmedi ve Bora kaldı.",
                ],
                "İlk iki cümlede Türkçenin gerçek sözcük ve öbek yapısını, sonraki iki cümlede bağlaç kapsamını, beşinci cümlede sınır vakasını ve son cümlede kontrol yapısını incele.",
            ),
        ],
        [
            "Öğrenci en az bir sözcüksel, bir yapısal ve iki kapsam belirsizliğini doğru türde sınıflandırır.",
            "En az iki yapısal veya kapsam belirsizliği için farklı ve doğru katı TFL cümleleri üretir.",
            "Her alternatif formülün karşılığı olan tek anlamlı açık Türkçe ara okumayı verir.",
            "Sembol anahtarındaki her harfi yalnız tek bir tam ve belirli bildirime bağlar.",
            "Bulanıklığı çok anlamlılık veya kapsam sorunu sanmadan karşılaştırma sınıfı ve sınır vakası üzerinden açıklar.",
            "Bağlam desteğini mantıksal zorunluluk ya da konuşmacı niyetinin kanıtı gibi sunmaz.",
            "Belirsiz olmayan kontrol cümlesine yapay alternatif okuma üretmez.",
        ],
        [
            "Biçimsel dil belirsizliği hangi aşamada giderir, hangi aşamada gidermez?",
            "Bulanık bir yüklem neden yalnız yeni parantez ekleyerek keskinleştirilemez?",
            "Bağlamın bir okumayı desteklemesi ile diğer okumayı dilbilgisi dışı yapması arasında ne fark vardır?",
        ],
        "Sonraki atölyede anahtarı hazır verilmeyen kısa metinleri baştan sona çözümleyecek, sembolleştirecek, geri okuyacak ve kayıp bilgi raporu yazacağız.",
        ["forallx-ambiguity"],
        "Formel dil, seçilmiş bir okumayı yapısal olarak açık kılar; doğal dil cümlesinin amaçlanan okumasını kendiliğinden seçmez. Bulanıklık ise çoklu oluşum ağacından değil, yüklemin sınır vakalarından doğar ve klasik TFL bu derece bilgisini atomik harfin içinde korumaz.",
        [],
    )

    lesson["reading_note"] = (
        "Önce yüzey cümlesini sınıflandır; sonra her savunulabilir okumayı tek anlamlı Türkçe ara cümlede yaz. Formülü ancak bu okumadan sonra kur ve bağlam kanıtını zorunluluk dili kullanmadan belirt."
    )
    lesson["symbol_set"] = [
        "A",
        "B",
        "C",
        "¬",
        "∧",
        "∨",
        "→",
        "↔",
        "(",
        ")",
    ]
    lesson["proof_tools"] = [
        "Belirsizlik türü sınıflandırması",
        "Açık Türkçe ara okuma",
        "Tek anlamlı sembol anahtarı",
        "Alternatif formül çifti",
        "Ana bağlaç ve kapsam denetimi",
        "Bağlam kanıtı derecelendirmesi",
        "Bulanıklık ve kayıp bilgi notu",
    ]
    return lesson


def _candidate_b13():
    lesson = _lesson(
        "B13",
        "ders-kademeli-sembollestirme-atolyesi",
        "Kademeli Sembolleştirme Atölyesi",
        "Hazır anahtar veya seçenek olmadan yeni bir doğal dil metnini analiz eder, sembolleştirir, kurucu yapıyla denetler, geri okur ve bilgi kaybını raporlar.",
        "Faz B aşama çıkış performansı",
        50,
        [
            "ders-17-sembollestirmeye-giris",
            "ders-18-degil-ve-ve-baglaclari",
            "ders-19-veya-ve-ise",
            "ders-kosul-yalnizca-cift-yonluluk",
            "ders-tfl-cumlesi-ana-baglac-ve-kapsam",
            "ders-belirsizlik-bulaniklik-savunulabilir-okumalar",
        ],
        [
            "tfl.translation_plan",
            "tfl.translation_produce",
            "tfl.translation_audit",
            "tfl.loss_explain",
        ],
        [
            "Bağlamı belirleme, atomik bildirimleri çıkarma ve tek anlamlı sembol anahtarı kurma adımlarını hazır ipucu olmadan yürütmek.",
            "Belirsiz doğal dil cümlelerini açık ara okumalara ayırıp karmaşık yapıyı ana bağlaçtan başlayarak dıştan içe çözmek.",
            "Her açık okuma için katı parantezli TFL cümlesi üretmek ve oluşum ağacıyla iyi kurulmuşluğu denetlemek.",
            "Koşul yönü, dışlayıcılık ve kapsam kararlarını metinsel kanıtla gerekçelendirmek.",
            "Formülü doğal dile geri çevirip korunan mantıksal yapı ile kaybolan zaman, vurgu, nedensellik, karşıtlık veya bulanıklık bilgisini raporlamak.",
        ],
        [
            (
                "Çözüm günlüğü",
                "Sembolleştirme kararlarını bağlamdan kayıp bilgi notuna kadar görünür kılan yedi adımlı çalışma kaydı.",
            ),
            (
                "Atom envanteri",
                "Metinde izlenecek, tek başına değerlendirilebilen ve anahtarda bir kez tanımlanan temel bildirimlerin listesi.",
            ),
            (
                "Dıştan içe çözümleme",
                "Karmaşık cümlenin önce ana bağlacını ve doğrudan alt cümlelerini, sonra her alt cümlenin iç yapısını bulma yöntemi.",
            ),
            (
                "Sözdizimi denetimi",
                "Üretilen dizinin atomik yapraklardan kurucu kurallarla üretilebildiğini ve kapsam parantezlerinin korunduğunu gösterme.",
            ),
            (
                "Geri çeviri",
                "TFL cümlesini yalnız sembol anahtarını kullanarak açık doğal dil okumasına yeniden dönüştürme.",
            ),
            (
                "Kayıp bilgi raporu",
                "TFL'nin korumadığı doğal dil ayrıntılarını ve bu kaybın yorum üzerindeki etkisini açıkça belirtme.",
            ),
            (
                "Aşama çıkış görevi",
                "Yeni bir metinde Faz B yetkinliklerinin ipucusuz ve bütünleşik biçimde gösterildiği bağımsız performans.",
            ),
        ],
        [
            _section(
                "Yedi adım sembolden önce başlar",
                "Güvenilir çözüm, yüzeydeki bağlaçları işaretlerle değiştirmekten önce bağlamı, atomları ve amaçlanan okumayı açıklaştırır.",
                "Hazır anahtarı bulunmayan yeni bir cümle veya kısa politika metniyle karşılaştığında.",
                "1 bağlam · 2 atomlar/anahtar · 3 açık okuma · 4 dıştan içe yapı · 5 formül · 6 sözdizimi · 7 geri çeviri/kayıp",
                "Adımlar birbirini denetler: erken kurulmuş iyi bir anahtar, sonraki formülü geri okumayı mümkün kılar; açık okuma ise hangi kapsam ve yönün amaçlandığını sabitler.",
                "Birinci adımda sembol yazma. Metni sözcük sözcük çevirmek, aynı bildirime iki harf verme ve belirsizliği anahtara taşıma riskini artırır.",
                [
                    (
                        "Bağlam: Müze erişim politikası",
                        "'Kart', 'kayıt' ve 'izin' sözcüklerinin teknik bağlamdaki görevini önce sabitler.",
                    ),
                    (
                        "Atom envanteri: K, R, P...",
                        "Her harfin karşısına yalnız tek bir tam bildirim yazılır; kişi veya tek sözcük yazılmaz.",
                    ),
                    (
                        "Açık okuma: Kart çalışıyorsa kayıt etkindir.",
                        "'Yalnızca' yüzey cümlesi işaretlere geçmeden garanti yönüyle yeniden yazılır.",
                    ),
                ],
                (
                    "İlk üç adımı tamamlamadan bağlaç seçmemek.",
                    "Cümleyi soldan sağa her sözcüğün altına bir sembol koyarak çevirmek.",
                    "Sembolleştirme sözcük ikamesi değil, belirli bir okumanın yapısal çözümlemesidir.",
                ),
            ),
            _section(
                "Ana bağlaçtan dıştan içe ilerlemek",
                "Açık ara cümle, önce bütün yapıyı kuran ana bağlaca ve doğrudan alt cümlelere; sonra daha küçük bileşenlere ayrılır.",
                "Birden fazla bağlaç, olumsuzlama veya koşul içeren cümlede parantez yapısını kurarken.",
                "Açık okuma → ana bağlaç → doğrudan alt cümleler → atomik yapraklar",
                "'Kapı açılırsa alarm susar ve bildirim gider' cümlesinde ana bağlaç →; sol alt cümle P, sağ alt cümle (A ∧ B)'dir. Formül (P → (A ∧ B)) olur.",
                "İlk görülen bağlacı ana bağlaç sanma. Sağdaki birleşim, bütün cümlenin değil koşulun artbileşeninin iç yapısıdır.",
                [
                    (
                        "Kart yalnızca kayıt etkinse çalışır.",
                        "Açık okuma 'Kart çalışıyorsa kayıt etkindir'; yapı (K → R)'dir.",
                    ),
                    (
                        "Kapı açılırsa alarm susar ve bildirim gider.",
                        "Dış koşul (P → ...), iç birleşim (A ∧ B) olarak katmanlanır.",
                    ),
                    (
                        "Misafir iki yoldan tam birini kullanır.",
                        "Önce en az biri (M ∨ I), sonra birlikte olmama ¬(M ∧ I), en sonda iki koşulu birleştiren ∧ kurulur.",
                    ),
                ],
                (
                    "Her katmanda yalnız tam TFL cümlelerini birleştirip dış parantezi korumak.",
                    "P → A ∧ B gibi sessiz önceliğe bırakan bir dizi teslim etmek.",
                    "Katı parantezleme çözümün kurucu tarihini ve ana bağlacını görünür tutar.",
                ),
            ),
            _section(
                "Anahtar ve sözdizimi iki ayrı denetimdir",
                "Bir formül iyi kurulmuş olsa bile yanlış anahtarla yanlış okumayı temsil edebilir; doğru anahtar da kuralsız bir işaret dizisini kurtaramaz.",
                "İlk taslaktan sonra çözümü teslim edilebilir hale getirirken.",
                "Anlam denetimi: anahtar + açık okuma. Yapı denetimi: kurucu adımlar + parantez + kapsam.",
                "Önce her harfin tek tam bildirime bağlı olduğunu kontrol et. Sonra formülü atomik yapraklardan başlayarak tekli ve ikili kurallarla yeniden kur; ana bağlaç ve doğrudan alt cümleleri işaretle.",
                "Yalnız formülün göze tanıdık gelmesine güvenme. Tutarsız harf kullanımı ile hatalı koşul yönü sözdizimsel olarak kusursuz görünebilir.",
                [
                    (
                        "K: Kart çalışır; sonra aynı metinde K: Kayıt etkindir.",
                        "Formül iyi kurulsa bile anahtar tutarsızdır; ikinci bildirim R gibi ayrı harf almalıdır.",
                    ),
                    (
                        "(P → (A ∧ B))",
                        "P, A ve B atomik yaprak; (A ∧ B) ara cümle; bütün koşul son kurucu adımdır.",
                    ),
                    (
                        "(K → R) yerine (R → K)",
                        "Her iki dizi de TFL cümlesidir; hata sözdiziminde değil 'yalnızca' yönünün açık okumayla uyuşmamasındadır.",
                    ),
                ],
                (
                    "Anahtar doğruluğunu ve iyi kurulmuşluğu ayrı onay kutularıyla denetlemek.",
                    "Formül TFL cümlesiyse doğal dil çevirisinin de otomatik doğru olduğunu varsaymak.",
                    "Biçimsel doğruluk ile çeviri doğruluğu farklı kanıt ister.",
                ),
            ),
            _section(
                "Alternatif okumalar rubrikle karşılaştırılır",
                "Bir yüzey cümlesi iki savunulabilir okuma taşıyorsa çözüm anahtarı tek formülü zorlamaz; her okumanın dilbilgisi, bağlam ve formülle uyumu değerlendirilir.",
                "Belirsiz bir cümlede iki öğrencinin farklı ama gerekçeli çözümlerini değerlendirirken.",
                "Açık okuma + tek anlamlı anahtar + uyumlu formül + bağlam kanıtı",
                "'Selin ve Mert veya Duru kontrol yapacak' cümlesi ((S ∧ M) ∨ D) veya (S ∧ (M ∨ D)) olabilir. Hangi formülün amaçlandığı, açık ara okuma ve bağlamla gösterilir.",
                "Cevap anahtarındaki işaret dizisini tek ölçüt yapma. Fakat dilbilgisel olmayan veya formülle uyuşmayan her alternatif de kabul edilemez.",
                [
                    (
                        "Ya Selin ile Mert birlikte kontrol yapacak ya da Duru yapacak.",
                        "((S ∧ M) ∨ D) için açık ve savunulabilir okumadır.",
                    ),
                    (
                        "Selin kontrol yapacak; ona Mert veya Duru eşlik edecek.",
                        "(S ∧ (M ∨ D)) için açık ve savunulabilir okumadır.",
                    ),
                    (
                        "Bağlamda Selin'in her ekipte bulunması şartı",
                        "İkinci okumayı destekler; ilk yapının dilbilgisel olarak kurulabilmesini tek başına ortadan kaldırmaz.",
                    ),
                ],
                (
                    "Alternatif çözümü okuma-formül uyumu ve bağlam kanıtı üzerinden puanlamak.",
                    "Farklı görünen her formülü eşit derecede doğru saymak veya tek anahtarı ezberletmek.",
                    "Çoğul cevap kabulü ölçütsüzlük değil, açık gerekçe ve yapısal uyum gerektirir.",
                ),
            ),
            _section(
                "Geri çeviri ve kayıp raporu son denetimdir",
                "Formül anahtarla geri okunduğunda açık ara okumayı vermeli; ardından TFL'de görünmeyen doğal dil bilgisinin adı konmalıdır.",
                "Teslimden hemen önce kapsam, koşul yönü ve soyutlama kaybını yakalamak için.",
                "Formül → anahtarla geri okuma → hedef açık okumayla karşılaştırma → kayıp bilgi listesi",
                "(K → R) geri okuması 'Kart çalışıyorsa kayıt etkindir' olmalıdır. Yüzeydeki 'yalnızca' sözcüğünün vurgu etkisi, politikanın amacı veya nedensel açıklaması formülde görünmez.",
                "Geri çeviriyi yüzey cümlesini hafızadan tekrar ederek yapma. Yalnız anahtar ve formülü kullan; aksi halde formüldeki yön hatasını fark etmeyebilirsin.",
                [
                    (
                        "(P → (A ∧ B))",
                        "Geri okuma: Kapı açılırsa alarm susar ve bildirim gider. Koşul yönü ile iç kapsam korunur.",
                    ),
                    (
                        "((M ∨ I) ∧ ¬(M ∧ I))",
                        "Geri okuma: Misafir iki yöntemden en az birini ve ikisini birlikte olmaksızın kullanır.",
                    ),
                    (
                        "'Fakat' sözcüğü",
                        "Birleşim yapısı korunabilir; beklenti karşıtlığı ve söylem tonu TFL'de kaybolur.",
                    ),
                    (
                        "'Önce' ve 'ardından'",
                        "İki atomik bildirim korunabilir; zaman sırası yalnız ∧ ile temsil edilmez.",
                    ),
                ],
                (
                    "En az iki somut kaybı adlandırıp çözümün amaçlanan soyutlama düzeyini belirtmek.",
                    "'Hiçbir bilgi kaybolmadı' demek veya formülden nedensellik ve zaman sırası okumak.",
                    "TFL mantıksal bağlaç yapısını seçerek korur; bütün doğal dil anlamını kopyalamaz.",
                ),
            ),
        ],
        [
            _worked(
                "Kart yalnızca kayıt etkinse çalışır.",
                "Açık okuma 'Kart çalışıyorsa kayıt etkindir'; K: Kart çalışır, R: Kayıt etkindir anahtarıyla (K → R) kurulur.",
                "Yalnızca yönü",
            ),
            _worked(
                "Kapı açılırsa alarm susar ve bildirim gider.",
                "Ana bağlaç →; artbileşen (A ∧ B) olduğundan katı biçim (P → (A ∧ B))'dir.",
                "Dıştan içe",
            ),
            _worked(
                "Misafir ya danışmanla girer ya geçici izin kullanır; iki yol birlikte kullanılamaz.",
                "M ve I için kapsayıcı en-az-biri ile birlikte-olmama koşulu birleştirilir: ((M ∨ I) ∧ ¬(M ∧ I)).",
                "Dışlayıcı yapı",
            ),
            _worked(
                "K harfini iki farklı bildirime vermek",
                "İyi kurulmuş bir formülün anlamını kararsız bırakır; anahtar denetiminde yakalanmalıdır.",
                "Anahtar hatası",
                "bad",
            ),
            _worked(
                "(R → K) yazmak",
                "TFL cümlesidir fakat 'Kart yalnızca kayıt etkinse çalışır' açık okumasındaki garanti yönünü tersine çevirir.",
                "Çeviri hatası",
                "bad",
            ),
            _worked(
                "P → A ∧ B yazmak",
                "Sessiz öncelik kullanır; bu programda amaçlanan kurucu yapı (P → (A ∧ B)) olarak açık parantezlenmelidir.",
                "Parantez hatası",
                "bad",
            ),
            _worked(
                "((S ∧ M) ∨ D)",
                "'Ya Selin ile Mert birlikte ya da Duru' açık okumasıyla uyumludur.",
                "Alternatif okuma 1",
            ),
            _worked(
                "(S ∧ (M ∨ D))",
                "'Selin ve ona eşlik edecek Mert veya Duru' açık okumasıyla uyumludur.",
                "Alternatif okuma 2",
            ),
            _worked(
                "Formülü anahtarla geri okumak",
                "Hedef ara okumayla uyuşmayan yön veya kapsam hatasını yüzey cümlesine bakmadan yakalar.",
                "Geri denetim",
            ),
            _worked(
                "'Fakat' karşıtlığı ile 'önce' zaman sırası",
                "TFL birleşimi ortak doğruluk işlevsel iskeleti koruyabilir; karşıtlık ve sıralama bilgisini ayrıca kayıp raporuna taşır.",
                "Bilgi kaybı",
            ),
            _worked(
                "Oda yeterince serindir → O",
                "Atomik TFL cümlesi kurulabilir; 'yeterince serin' eşiğinin bulanıklığı harfin içinde görünmez.",
                "Bulanıklık kaybı",
            ),
        ],
        [
            "Sembol anahtarı yazmadan harfleri kullanmaya başlamak.",
            "Aynı atomik bildirime metnin farklı yerlerinde farklı harfler vermek.",
            "Cümleyi soldan sağa sözcük sözcük çevirip ana bağlacı hiç belirlememek.",
            "'Yalnızca', gerekli koşul ve yeterli koşul ifadelerinde garanti yönünü açık ara cümleyle sınamamak.",
            "Dışlayıcı 'ya...ya' okumasını yalnız (A ∨ B) ile bırakmak.",
            "Katı parantezi atıp bağlaç önceliğini okuyucuya bırakmak.",
            "Alternatif savunulabilir okumayı tek cevap dizisine uymadığı için otomatik reddetmek.",
            "Formülü anahtarla geri okumadan teslim etmek.",
            "TFL'nin zaman, nedensellik, vurgu, karşıtlık ve bulanıklık ayrıntılarını eksiksiz koruduğunu varsaymak.",
        ],
        _practice(
            [
                (
                    "Yeni bir metinde ilk yapılacak işlem hangisidir?",
                    [
                        "Bağlamı ve çözümleme amacını belirlemek",
                        "Bütün bağlaçları işaretlerle değiştirmek",
                        "En uzun formülü seçmek",
                        "Parantezleri kaldırmak",
                    ],
                    "Bağlamı ve çözümleme amacını belirlemek",
                    "Sembol anahtarı ve açık okumalar, hangi bağlamdaki bildirimi izlediğimiz sabitlenmeden güvenle kurulamaz.",
                    "Temel",
                ),
                (
                    "Atom envanterine hangi tür ifade girer?",
                    [
                        "Tek başına değerlendirilebilen tam bildirim",
                        "Kişi adı",
                        "Bağlaç sözcüğü",
                        "Eksik yüklem parçası",
                    ],
                    "Tek başına değerlendirilebilen tam bildirim",
                    "Cümle harfi yalnız tam atomik bildirimin yerini tutar.",
                    "Temel",
                ),
                (
                    "'Kart yalnızca kayıt etkinse çalışır' için K: Kart çalışır, R: Kayıt etkindir. Doğru formül hangisidir?",
                    ["(K → R)", "(R → K)", "(K ↔ R)", "(K ∧ R)"],
                    "(K → R)",
                    "Kartın çalışması kayıt etkinliğini garanti eder; kayıt gerekli koşuldur.",
                    "Orta",
                ),
                (
                    "P: Kapı açılır; A: Alarm susar; B: Bildirim gider. 'Kapı açılırsa alarm susar ve bildirim gider' hangisidir?",
                    ["(P → (A ∧ B))", "((P → A) ∧ B)", "((P ∧ A) → B)", "(P ↔ (A ∧ B))"],
                    "(P → (A ∧ B))",
                    "Ana bağlaç koşul, artbileşenin iç yapısı birleşimdir.",
                    "Orta",
                ),
                (
                    "M ve I iki izin yolunu göstersin. Tam olarak bir yol kullanılacaksa hangi yapı gerekir?",
                    [
                        "((M ∨ I) ∧ ¬(M ∧ I))",
                        "(M ∨ I)",
                        "¬(M ∧ I)",
                        "(M ∧ I)",
                    ],
                    "((M ∨ I) ∧ ¬(M ∧ I))",
                    "Tam olarak bir, hem en az bir yolun hem de iki yolun birlikte olmamasının sağlanmasını ister.",
                    "İleri",
                ),
                (
                    "Bir formül iyi kurulmuş fakat yanlış koşul yönündeyse hangi denetim başarısızdır?",
                    [
                        "Açık okuma ve çeviri uyumu denetimi",
                        "Yalnız alfabe denetimi",
                        "Yalnız parantez dengesi",
                        "Yazı boyutu denetimi",
                    ],
                    "Açık okuma ve çeviri uyumu denetimi",
                    "Sözdizimsel iyi kurulmuşluk, doğal dil okumasıyla anlam uyumunu garanti etmez.",
                    "Orta",
                ),
                (
                    "((A ∨ B) → ¬C) için ana bağlaç hangisidir?",
                    ["→", "∨", "¬", "A"],
                    "→",
                    "Bütün cümleyi kuran son adım iki doğrudan alt cümleyi koşulla birleştirir.",
                    "Temel",
                ),
                (
                    "Geri çeviri hangi malzemeyle yapılmalıdır?",
                    [
                        "Yalnız formül ve sembol anahtarıyla",
                        "Yüzey cümlesini ezberden tekrarlayarak",
                        "Bağlaçları görmezden gelerek",
                        "Anahtardaki tam bildirimleri kısaltarak",
                    ],
                    "Yalnız formül ve sembol anahtarıyla",
                    "Bu yöntem formülde gerçekten yazılan yön ve kapsamın hedef okumaya dönüp dönmediğini sınar.",
                    "Orta",
                ),
                (
                    "İki öğrenci aynı belirsiz cümle için farklı formüller verdiğinde ilk karşılaştırılacak şey nedir?",
                    [
                        "Her formülün açık Türkçe okumasıyla uyumu",
                        "Hangi formülün daha uzun olduğu",
                        "Kimin önce teslim ettiği",
                        "Harflerin alfabetik sırası",
                    ],
                    "Her formülün açık Türkçe okumasıyla uyumu",
                    "Alternatif cevap ancak belirli ve dilbilgisel bir okumayı tutarlı anahtar ve yapıyla temsil ediyorsa savunulabilir.",
                    "İleri",
                ),
                (
                    "Bağlam Selin'in her kontrol ekibinde bulunacağını söylüyorsa hangi okuma desteklenir?",
                    ["(S ∧ (M ∨ D))", "((S ∧ M) ∨ D)", "¬S", "(M ↔ D)"],
                    "(S ∧ (M ∨ D))",
                    "Bu yapı S'yi her durumda dış birleşimin zorunlu bileşeni yapar.",
                    "İleri",
                ),
                (
                    "Aşağıdakilerden hangisi tipik bir kayıp bilgi notudur?",
                    [
                        "'Fakat'ın beklenti karşıtlığı ∧ içinde görünmez",
                        "A harfi kesinlikle doğrudur",
                        "Her koşul nedenseldir",
                        "Parantezler gereksizdir",
                    ],
                    "'Fakat'ın beklenti karşıtlığı ∧ içinde görünmez",
                    "TFL birleşim yapısını korur; söylemsel karşıtlığı ayrıca temsil etmez.",
                    "Orta",
                ),
                (
                    "'Oda yeterince serindir' cümlesini O ile atomik göstermek hangi bilgiyi kaybedebilir?",
                    [
                        "'Yeterince serin' için kullanılan eşik ve sınır vakaları",
                        "O harfinin büyük olması",
                        "Cümlenin noktayla bitmesi",
                        "Herhangi bir bağlaç önceliği",
                    ],
                    "'Yeterince serin' için kullanılan eşik ve sınır vakaları",
                    "Atomik harf, bulanık yüklemin derece ve karşılaştırma sınıfını açmaz.",
                    "İleri",
                ),
                (
                    "Bir çözüm günlüğünün son adımı hangisidir?",
                    [
                        "Formülü geri çevirip kayıp bilgiyi raporlamak",
                        "Yeni atomlar eklemek",
                        "Anahtarı silmek",
                        "İlk bağlacı ana bağlaç ilan etmek",
                    ],
                    "Formülü geri çevirip kayıp bilgiyi raporlamak",
                    "Son denetim hedef okuma uyumunu ve soyutlama sınırını görünür kılar.",
                    "Temel",
                ),
                (
                    "Yedi adımlı akışta sözdizimi denetimi neyi göstermelidir?",
                    [
                        "Formülün atomik yapraklardan kurucu kurallarla üretilebildiğini",
                        "Konuşmacının zihnindeki tek niyeti",
                        "Bulanık yüklemin kesin eşiğini",
                        "Cümlenin gündelik hayatta doğru olduğunu",
                    ],
                    "Formülün atomik yapraklardan kurucu kurallarla üretilebildiğini",
                    "Sözdizimi denetimi iyi kurulmuşluğu gösterir; gerçek dünya doğruluğunu veya niyeti değil.",
                    "Zor",
                ),
            ],
        ),
        {
            "prompt": "Üç cümlelik müze erişim politikasını yedi adımlı çözüm günlüğüyle sembolleştir: kart-yetki koşulu, kapı-alarm-bildirim koşulu ve iki izin yolundan tam birini kullanma kuralı.",
            "starter": "Bağlam: Müze erişimi. Aday atomlar: K: Kart çalışır. R: Kayıt etkindir. P: Kapı açılır. A: Alarm susar. B: Bildirim gider. M: Misafir danışmanla girer. I: Misafir geçici izin kullanır.",
            "checks": [
                "Her anahtar satırı tek ve tam atomik bildirimdir",
                "'Kart yalnızca kayıt etkinse çalışır' açık okuması K → R yönünü gerekçelendirir",
                "Kapı kuralında ana bağlaç →, artbileşen (A ∧ B) olarak dıştan içe ayrılır",
                "İzin kuralı en az bir ile birlikte-olmama koşullarını ((M ∨ I) ∧ ¬(M ∧ I)) içinde birlikte taşır",
                "Her formül atomik yapraklardan kurucu adımlarla yeniden kurulmuştur",
                "Geri çeviriler yüzey cümlesini ezberden değil anahtar ve formülden üretir",
                "En az iki kayıp bilgi, örneğin politika amacı, nedensellik, zaman veya söylem vurgusu olarak adlandırılır",
            ],
            "solution": "Açık okumalar ve formüller: 'Kart çalışıyorsa kayıt etkindir' → (K → R). 'Kapı açılırsa hem alarm susar hem bildirim gider' → (P → (A ∧ B)). 'Misafir en az bir izin yolunu kullanır ve iki yolu birlikte kullanmaz' → ((M ∨ I) ∧ ¬(M ∧ I)). Her formül anahtarla aynı cümleye geri dönmeli; politikanın nedeni, zamanlaması ve vurgu bilgisi ayrıca kayıp raporuna yazılmalıdır.",
        },
        [
            _production_task(
                "Arşiv erişim metni için hazır anahtar veya seçenek kullanmadan tam bir aşama çıkış dosyası üret. Altı cümleyi yedi adımlı çözüm günlüğünden geçir; belirsiz cümleyi iki savunulabilir okumayla, bulanık cümleyi ise kayıp sınır bilgisiyle raporla.",
                [
                    "Bağlamı ve sembolleştirme amacını iki cümlede sınırla.",
                    "Bütün tekrar eden atomik bildirimleri çıkar; her birine tek harf veren tutarlı bir sembol anahtarı kur.",
                    "Her yüzey cümlesini belirsiz olmayan açık Türkçe ara okumaya dönüştür; dördüncü cümle için iki ayrı okuma yaz.",
                    "Her açık okumada ana bağlacı ve doğrudan alt cümleleri dıştan içe göster.",
                    "Bütün formülleri katı parantezle yaz; gerekli koşul yönünü ve dışlayıcı yapıyı metinsel kanıtla gerekçelendir.",
                    "Her formülü atomik yapraklardan kurucu adımlarla denetle; açıklanmamış öncelik bırakma.",
                    "Formülleri yalnız anahtarla geri çevir; hedef okumayla karşılaştır.",
                    "En az iki genel kayıp bilgi ile 'yeterince serin' yükleminin bulanıklık kaybını ayrı ayrı raporla.",
                    "Dördüncü cümlede iki çözümü dilbilgisi, açık okuma, formül uyumu ve bağlam kanıtı rubriğiyle karşılaştır.",
                ],
                "Rubrik yalnız son işaret dizilerini değil, çözüm günlüğündeki her kararın metinle ve sonraki adımla tutarlılığını puanlar.",
                "Arşiv erişim metni",
                [
                    "Arşiv yalnızca sorumlu görevli buradaysa açılır.",
                    "Nem yükselirse alarm çalar ve havalandırma çalışır.",
                    "Araştırmacı ya dijital kopyayı kullanır ya da özgün belgeyi gözetim altında inceler; iki yöntem aynı oturumda birlikte kullanılamaz.",
                    "Selin ve Mert veya Duru kapanış kontrolünü yapacak.",
                    "Oda yeterince serindir.",
                    "Işık açık değildir ve kayıt sistemi çalışır.",
                ],
                "Dördüncü cümle iki gruplamaya izin verir. Beşinci cümle atomik bırakılabilir ama 'yeterince' eşiği TFL'de görünmez. Diğer cümlelerde koşul yönü, dışlayıcılık ve yerel olumsuzlama denetlenir.",
            ),
        ],
        [
            "Öğrenci yedi adımlı çözüm günlüğünü hazır anahtar veya çoktan seçmeli seçenek olmadan eksiksiz yürütür.",
            "Sembol anahtarı tutarlı tam bildirimlerden oluşur; aynı atom gereksiz yere çoğaltılmaz ve bir harfe iki anlam verilmez.",
            "Bütün karmaşık formüller katı parantezli TFL cümlesidir ve atomik yapraklardan kurucu kurallarla yeniden üretilebilir.",
            "Koşul yönü, kapsam ve dışlayıcılık kararları yüzey sözcükleri yerine açık ara okuma ve metinsel kanıtla gerekçelendirilir.",
            "En az bir belirsiz cümle iki farklı, savunulabilir ve formülle uyumlu açık okumayla gösterilir.",
            "Her formül yalnız anahtarla geri çevrildiğinde öğrencinin hedeflediği açık okumayı verir.",
            "En az iki doğal dil kaybı ve bir bulanıklık kaybı doğru adlandırılır; formülde bulunmayan nedensellik veya zaman bilgisi geri eklenmez.",
            "Alternatif çözümler tek cevap ezberiyle değil, açık rubrik ölçütleriyle değerlendirilir.",
        ],
        [
            "Bir sembolleştirme çözümünü teslim etmeden önce hangi yedi denetimi yaparsın?",
            "İki farklı formül hangi koşulda aynı doğal dil cümlesi için birlikte savunulabilir olabilir?",
            "İyi kurulmuş bir TFL cümlesi neden yine de yanlış çeviri olabilir?",
            "Geri çeviri ile kayıp bilgi raporu hangi iki farklı hatayı yakalar?",
        ],
        "Bir sonraki aşamada aynı TFL cümlelerinin hangi koşullarda doğru veya yanlış olduğunu sistematik olarak inceleyeceğiz; Faz B'de kurulan hiçbir semantik sonucu peşinen varsaymayacağız.",
        [
            "forallx-first-symbolization",
            "forallx-connectives",
            "forallx-tfl-sentences",
            "forallx-ambiguity",
            "mit-logic-sequence",
            "mit-logic-study-guide",
        ],
        "Atölye yeni bir bağlaç veya değerlendirme yöntemi öğretmez. Değerlendirme nesnesi yalnız son formül değil; bağlam varsayımı, atom envanteri, açık okuma, anahtar, kurucu denetim, geri çeviri ve kayıp bilgi raporunun birlikte oluşturduğu gerekçeli çözüm zinciridir.",
        [
            "ders-17-sembollestirmeye-giris",
            "ders-18-degil-ve-ve-baglaclari",
            "ders-19-veya-ve-ise",
            "ders-20-dogruluk-tablolari-i",
        ],
    )

    lesson["reading_note"] = (
        "Son formülü hemen yazma. Yedi adımlı çözüm günlüğünde her kararın bir önceki adımdan çıktığını ve geri çeviride aynı açık okumaya döndüğünü göster."
    )
    lesson["symbol_set"] = [
        "A",
        "B",
        "C",
        "A₁",
        "¬",
        "∧",
        "∨",
        "→",
        "↔",
        "(",
        ")",
    ]
    lesson["proof_tools"] = [
        "Yedi adımlı çözüm günlüğü",
        "Atom envanteri",
        "Tek anlamlı sembol anahtarı",
        "Açık Türkçe ara okuma",
        "Dıştan içe oluşum ağacı",
        "Anahtar ve sözdizimi çift denetimi",
        "Geri çeviri",
        "Kayıp bilgi raporu",
        "Alternatif okuma rubriği",
    ]
    return lesson


STAGE_B_CANDIDATE_LESSONS = [
    _candidate_b7(),
    _candidate_b8(),
    _candidate_b9(),
    _candidate_b10(),
    _candidate_b11(),
    _candidate_b12(),
    _candidate_b13(),
]

STAGE_B_CANDIDATE_MAP = {
    lesson["slug"]: lesson
    for lesson in STAGE_B_CANDIDATE_LESSONS
}
