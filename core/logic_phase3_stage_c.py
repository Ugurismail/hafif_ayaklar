"""Release-candidate content for Phase 3, Stage C of the logic course.

Stage C is developed one lesson at a time. Candidate lessons and their
machine-checkable semantic fixtures remain isolated from the learner-facing
course until the complete stage passes the gates documented in
``docs/logic_phase3_stage_c_spec.md``.
"""

from .logic_phase3_stage_a import (
    _lesson,
    _practice,
    _production_task,
    _section,
    _worked,
)


STAGE_C_SOURCE_REFERENCES = {
    "forallx-use-mention": {
        "title": "forall x: Calgary - Use and mention",
        "url": "https://forallx.openlogicproject.org/html/Ch8.html",
    },
    "forallx-characteristic-tables": {
        "title": "forall x: Calgary - Characteristic truth tables",
        "url": "https://forallx.openlogicproject.org/html/Ch9.html",
    },
    "forallx-truth-functionality": {
        "title": "forall x: Calgary - Truth-functionality",
        "url": "https://forallx.openlogicproject.org/html/Ch10.html",
    },
    "forallx-valuations": {
        "title": "forall x: Calgary - Valuations",
        "url": "https://forallx.openlogicproject.org/html/Ch11.html",
    },
    "forallx-logical-concepts": {
        "title": "forall x: Calgary - Logical concepts",
        "url": "https://forallx.openlogicproject.org/html/Ch12.html",
    },
    "forallx-expressiveness": {
        "title": "forall x: Calgary - Expressive limitations of TFL",
        "url": "https://forallx.openlogicproject.org/html/Ch13.html",
    },
    "forallx-table-shortcuts": {
        "title": "forall x: Calgary - Shortcuts in truth tables",
        "url": "https://forallx.openlogicproject.org/html/Ch14.html",
    },
    "forallx-partial-tables": {
        "title": "forall x: Calgary - Partial truth tables",
        "url": "https://forallx.openlogicproject.org/html/Ch15.html",
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


def _candidate_c14():
    lesson = _lesson(
        "C14",
        "ders-degerlemeler-ve-dogruluk-islevleri",
        "Değerlemeler ve Doğruluk İşlevleri",
        "Bir TFL cümlesinin doğruluk değerini, verilen tek bir değerleme altında beş bağlacın karakteristik koşullarını içten dışa uygulayarak hesaplar.",
        "Tek değerleme altında semantik hesap",
        40,
        [
            "ders-kullanim-anma-ve-dil-duzeyleri",
            "ders-kosul-yalnizca-cift-yonluluk",
            "ders-tfl-cumlesi-ana-baglac-ve-kapsam",
            "ders-kademeli-sembollestirme-atolyesi",
        ],
        [
            "tfl.valuation_read",
            "tfl.truth_function_apply",
            "tfl.semantic_trace",
            "tfl.material_conditional_evaluate",
        ],
        [
            "Değerlemeyi, TFL cümle harflerine Doğru (T) veya Yanlış (F) atayan bir üst dil aracı olarak okumak ve gerçek dünyayı araştıran yöntemden ayırmak.",
            "¬, ∧, ∨, → ve ↔ bağlaçlarının karakteristik doğruluk koşullarını verilen tek bir değerleme altında doğru uygulamak.",
            "Karmaşık bir TFL cümlesini oluşum ağacına uygun biçimde en iç alt cümlelerden ana bağlaca doğru değerlendirmek.",
            "Maddi koşulun ve öteki TFL bağlaçlarının doğruluk işlevsel tanımıyla doğal dildeki bütün anlam inceliklerinin aynı şey olmadığını açıklamak.",
        ],
        [
            (
                "Değerleme",
                "TFL cümle harflerinin her birine Doğru (T) veya Yanlış (F) doğruluk değeri atayan üst dil aracı.",
            ),
            (
                "Doğruluk değeri",
                "Klasik iki değerli TFL'de bir cümlenin aldığı Doğru (T) veya Yanlış (F) değeri.",
            ),
            (
                "Doğruluk işlevi",
                "Bileşik cümlenin değerini yalnız doğrudan alt cümlelerinin doğruluk değerlerinden belirleyen işlem.",
            ),
            (
                "Karakteristik doğruluk koşulu",
                "Bir bağlacın, alt cümlelerinin her olası doğruluk değeri birleşiminde hangi sonucu verdiğini belirleyen kural.",
            ),
            (
                "Maddi koşul",
                "A → B cümlesini yalnız A doğru ve B yanlışken yanlış, diğer üç değer birleşiminde doğru yapan TFL bağlacı.",
            ),
            (
                "Semantik iz",
                "Bir bileşik cümlede atomlardan başlayıp her alt cümlenin değerini ana bağlaca kadar görünür biçimde kaydetme sırası.",
            ),
        ],
        [
            _section(
                "Değerleme ne söyler, ne söylemez?",
                "v(A)=T yazımı, yalnız v adı verilen değerlemenin A'ya Doğru değerini atadığını söyler. T ve F bu cümleden söz ettiğimiz üst dilin kısaltmalarıdır; TFL cümle harfi değildir.",
                "Bir alıştırmada atomik cümlelerin değerleri hazır verildiğinde ve hesap boyunca hangi atamanın sabit tutulacağını belirlerken.",
                "v(A)=T; v(B)=F",
                "Değerleme bir senaryo satırı gibidir: o çalışma boyunca aynı harf aynı değeri korur. Bir cümlenin bu tek değerlemede doğru çıkması, onun bütün değerlemelerde nasıl davrandığını henüz göstermez.",
                "v(A)=T ifadesini 'A gerçek dünyada kanıtlanmıştır' diye okuma. Değerleme, semantik hesabın girdisidir; gözlem veya kanıt yöntemi değildir.",
                [
                    (
                        "v(A)=T ve v(B)=F",
                        "Bu hesapta A doğru, B yanlıştır; T ile F ayrıca değerlendirilecek TFL atomları değildir.",
                    ),
                    (
                        "Başka bir w değerlemesinde w(A)=F olabilir.",
                        "Cümle harfinin değeri bütün olası değerlemelerde sabit olmak zorunda değildir.",
                    ),
                    (
                        "A: Arşiv açıktır.",
                        "A'nın bugün fiilen doğru olup olmadığını araştırmak sembol anahtarının ve değerlemenin yaptığı iş değildir.",
                    ),
                ],
                (
                    "v'nin verdiği atomik değerleri hesap girdisi olarak sabit tutmak.",
                    "Tek bir değerlemeyi gerçek dünyanın eksiksiz betimi veya bütün değerlemeler hakkında sonuç sanmak.",
                    "Değerleme olası bir doğruluk atamasıdır; tek satırlık hesap, cümlenin tüm olası atamalardaki statüsünü belirlemez.",
                ),
            ),
            _section(
                "Beş bağlacın karakteristik koşulları",
                "Her TFL bağlacı, doğrudan alt cümlelerinin değerlerinden bileşik cümlenin değerini belirleyen sabit bir doğruluk işlevi verir.",
                "Bir alt cümlenin değerleri bilindiğinde bir üst düğümün değerini hesaplarken.",
                "¬T=F; T∧T=T; F∨T=T; T→F=F; T↔T=T ve F↔F=T",
                "¬ değeri tersine çevirir. ∧ yalnız iki taraf da doğruysa doğrudur. ∨ en az bir taraf doğruysa doğrudur ve kapsayıcıdır. → yalnız T/F birleşiminde yanlıştır. ↔ iki taraf aynı değerdeyse doğrudur.",
                "Doğal dil sezgisini bağlacın resmi koşulunun yerine koyma. Özellikle 'veya'nın iki doğru tarafı dışladığını ya da çift yönlü koşulun iki yanlış tarafında yanlış olduğunu varsayma.",
                [
                    (
                        "v(A)=T altında v(¬A)=F",
                        "Olumsuzlama doğrudan alt cümlenin değerini tersine çevirir.",
                    ),
                    (
                        "v(A)=T ve v(B)=T altında v(A∨B)=T",
                        "TFL'deki ∨ kapsayıcıdır; iki ayrılanın birlikte doğru olmasına izin verir.",
                    ),
                    (
                        "v(A)=F ve v(B)=F altında v(A↔B)=T",
                        "Çift yönlü koşul, tarafların aynı doğruluk değerini taşımasına bakar; ikisinin de doğru olmasını şart koşmaz.",
                    ),
                ],
                (
                    "Bağlacın karakteristik koşulunu alt cümle değerlerine mekanik ve gerekçeli biçimde uygulamak.",
                    "Bağlacın günlük dilde çağrıştırdığı ilişkiyi resmi doğruluk koşuluna eklemek.",
                    "TFL bağlaçları doğruluk işlevseldir; nedensellik, zaman, vurgu ve karşıolgusallık gibi ek ilişkiler bu hesapta yer almaz.",
                ),
            ),
            _section(
                "İçten dışa semantik iz",
                "Karmaşık cümlede ana bağlacın değeri doğrudan tahmin edilmez. Önce atomlar, sonra en iç alt cümleler, en son ana bağlaç hesaplanır.",
                "Birden fazla bağlaç ve parantez içeren TFL cümlesinde ara değerleri kaybetmeden ilerlerken.",
                "atomlar → en iç alt cümleler → doğrudan alt cümleler → ana bağlaç",
                "Sözdizimsel oluşum ağacı hesap sırasını belirler. Aynı atom tekrar ederse değerlemede aldığı değer her geçtiği yerde aynıdır; fakat her farklı alt cümle kendi bağlacına göre hesaplanır.",
                "Soldan sağa okuma sırasını hesap sırası sanma ve ana bağlacı, onun doğrudan alt cümleleri hazır olmadan değerlendirme.",
                [
                    (
                        "v(A)=T, v(B)=F altında ¬(A∧B)→B",
                        "Önce A∧B=F, sonra ¬(A∧B)=T, son olarak T→F=F bulunur.",
                    ),
                    (
                        "v(A)=F, v(B)=T, v(C)=F altında (A∨B)↔¬C",
                        "A∨B=T ve ¬C=T hesaplandıktan sonra T↔T=T bulunur.",
                    ),
                    (
                        "A iki kez geçse de v(A) değişmez.",
                        "(A→B)∧(B→A) içinde her A görünümü aynı atomik atamayı kullanır.",
                    ),
                ],
                (
                    "Her ara alt cümleyi formülüyle ve T/F değeriyle kaydetmek.",
                    "Yalnız nihai değeri yazıp hangi bağlaç koşulunun uygulandığını görünmez bırakmak.",
                    "Semantik iz, doğru cevabın tesadüf mü yoksa yeniden üretilebilir bir hesap mı olduğunu gösterir.",
                ),
            ),
            _section(
                "Maddi koşulun tek yanlış durumu",
                "A → B maddi koşulu yalnız önbileşen doğru ve artbileşen yanlışken yanlıştır. Önbileşen yanlışsa koşul, artbileşenin değerinden bağımsız olarak doğrudur.",
                "Koşul cümlesinin değerini hesaplarken ve gündelik 'eğer' sezgisinin resmi koşula fazladan bilgi eklediğini fark ederken.",
                "T→T=T; T→F=F; F→T=T; F→F=T",
                "Maddi koşul, 'A olup B olmaması' durumunu dışlar. B10'daki yön bilgisi korunur; fakat nedensel bağ, zaman sırası, açıklama ve konuşma edimi bu doğruluk işlevine eklenmez.",
                "Önbileşeni yanlış olan satırlarda 'ilişki bilinmiyor' deyip boş bırakma veya koşulu otomatik yanlış yapma.",
                [
                    (
                        "v(A)=T, v(B)=F: v(A→B)=F",
                        "Koşulun yasakladığı tek birleşim gerçekleşmiştir: A var, B yoktur.",
                    ),
                    (
                        "v(A)=F, v(B)=F: v(A→B)=T",
                        "A'nın gerçekleşip B'nin gerçekleşmediği bir ihlal yoktur.",
                    ),
                    (
                        "Eğer taş düşseydi cam kırılırdı.",
                        "Karşıolgusal ve nedensel içerik, yalnız iki atomun mevcut T/F değerleriyle tüketilemeyebilir.",
                    ),
                ],
                (
                    "Önce A ile B'nin değer çiftini yazıp yalnız T/F çiftinde F sonucu vermek.",
                    "Doğal dilde makul veya şaşırtıcı görünmesine göre A→B'nin değerini değiştirmek.",
                    "Bu ders maddi koşulun resmi hesabını öğretir; doğal dil koşullarının eksiksiz teorisini değil.",
                ),
            ),
            _section(
                "Doğruluk işlevselliğinin sınırı",
                "Bir ifade doğruluk işlevselse bileşiğin değeri, bileşenlerin yalnız T/F değerleriyle belirlenir. Doğal dildeki her kurucu bu özelliği taşımaz.",
                "TFL sembolleştirmesinin hangi bilgiyi koruduğunu ve hangi anlam katmanını dışarıda bıraktığını raporlarken.",
                "Aynı alt cümle değerleri + aynı doğruluk işlevi = aynı bileşik değer",
                "'Değil', doğruluk işlevsel olumsuzlama için uygundur. Buna karşılık 'zorunlu olarak', 'çünkü', 'önce', 'inanıyor ki' veya zengin karşıolgusal kullanımlar yalnız alt cümlelerin mevcut doğruluk değerleriyle belirlenmeyebilir.",
                "TFL'nin ifade edemediği ayrıntıyı önemsiz sayma; biçimsel modelin sınırını çözümün parçası olarak açıkça yaz.",
                [
                    (
                        "A ve B",
                        "TFL'de ∧, A ile B'nin yalnız doğruluk değerlerinden bileşiğin değerini belirler.",
                    ),
                    (
                        "A çünkü B",
                        "A ile B doğru olsa bile 'çünkü' ile ileri sürülen açıklama ilişkisi ayrıca yanlış olabilir.",
                    ),
                    (
                        "Zorunlu olarak A",
                        "A'nın fiilen doğru olması, onun zorunlu olduğunu tek başına belirlemez.",
                    ),
                ],
                (
                    "TFL hesabını doğru yürütüp kaybolan doğal dil bilgisini ayrıca raporlamak.",
                    "TFL'de gösterilemeyen her ayrıntının anlamsız veya mantıksal bakımdan değersiz olduğunu söylemek.",
                    "Biçimselleştirme seçici bir modellemedir; kapsamı kadar sınırı da gerekçelendirilmelidir.",
                ),
            ),
        ],
        [
            _worked(
                "v(A)=T altında ¬A=F",
                "Olumsuzlama, doğrudan alt cümlenin doğruluk değerini tersine çevirir.",
                "Olumsuzlama",
            ),
            _worked(
                "v(A)=T, v(B)=F altında A∧B=F",
                "Birleşim yalnız iki taraf da doğruysa doğrudur.",
                "Birleşim",
            ),
            _worked(
                "v(A)=T, v(B)=T altında A∨B=T",
                "Kapsayıcı ayrık bağlaçta en az bir doğru taraf yeterlidir; iki tarafın birlikte doğru olması sonucu bozmaz.",
                "Kapsayıcı veya",
            ),
            _worked(
                "v(A)=T, v(B)=F altında A→B=F",
                "Maddi koşulun tek yanlış birleşimi T/F'dir.",
                "Maddi koşul",
            ),
            _worked(
                "v(A)=F, v(B)=F altında A↔B=T",
                "Çift yönlü koşul iki taraf aynı değerde olduğunda doğrudur.",
                "Çift yönlü",
            ),
            _worked(
                "v(A)=T, v(B)=F altında ¬(A∧B)→B=F",
                "A∧B=F, ¬(A∧B)=T ve son adım T→F=F sırasıyla hesaplanır.",
                "İçten dışa",
            ),
            _worked(
                "v(A)=F, v(B)=T, v(C)=F altında (A∨B)↔¬C=T",
                "İki doğrudan alt cümle de T olduğundan ana bağlaç T↔T sonucu verir.",
                "Semantik iz",
            ),
            _worked(
                "'A çünkü B' ifadesini yalnız A∧B ile tüketmek",
                "A ve B'nin doğruluğu, B'nin A'yı açıkladığını garanti etmez; açıklama ilişkisi TFL birleşiminde kaybolur.",
                "Model sınırı",
                "bad",
            ),
        ],
        [
            "T ve F işaretlerini, değerlemeyi oluşturan TFL cümle harfleri sanmak.",
            "v(A)=T yazımını A'nın gerçek dünyada gözlemle kanıtlandığı iddiası diye okumak.",
            "Tek bir değerlemede doğru çıkan cümlenin bütün değerlemelerde doğru olduğunu varsaymak.",
            "A∨B'yi varsayılan olarak dışlayıcı okuyup T/T birleşiminde yanlış yapmak.",
            "A→B'yi önbileşen yanlışken otomatik yanlış saymak veya değersiz bırakmak.",
            "A↔B'yi yalnız iki taraf da doğru olduğunda doğru sanmak.",
            "Ana bağlacın değerini, doğrudan alt cümleleri hesaplamadan tahmin etmek.",
            "Maddi koşulun nedensellik, zaman ve karşıolgusallık bilgisini eksiksiz taşıdığını varsaymak.",
        ],
        _practice(
            [
                (
                    "v(A)=F ifadesi tam olarak ne söyler?",
                    [
                        "A her koşulda yanlıştır",
                        "v değerlemesi A'ya Yanlış (F) değerini atar",
                        "F, A'nın yerine geçen yeni bir TFL atomudur",
                        "A gerçek dünyada çürütülmüştür",
                    ],
                    "v değerlemesi A'ya Yanlış (F) değerini atar",
                    "Değerleme belirli bir semantik atamayı bildirir; bütün değerlemeler veya fiili dünya hakkında tek başına sonuç vermez.",
                    "Temel",
                ),
                (
                    "T ile F bu derste hangi dil düzeyindedir?",
                    [
                        "TFL'nin atomik cümleleri",
                        "Doğruluk değerlerini gösteren üst dil kısaltmaları",
                        "Doğal dilde özel adlar",
                        "Çıkarım kuralları",
                    ],
                    "Doğruluk değerlerini gösteren üst dil kısaltmaları",
                    "T ve F, TFL cümlelerinden söz ederken kullandığımız üst dil işaretleridir.",
                    "Temel",
                ),
                (
                    "v(A)=T ise v(¬A) kaçtır?",
                    ["T", "F", "Hem T hem F", "Belirlenemez"],
                    "F",
                    "Olumsuzlama alt cümlenin değerini tersine çevirir.",
                    "Temel",
                ),
                (
                    "v(A)=T ve v(B)=F ise v(A∧B) kaçtır?",
                    ["T", "F", "A", "Belirlenemez"],
                    "F",
                    "Birleşim yalnız iki taraf da doğruysa doğrudur.",
                    "Temel",
                ),
                (
                    "v(A)=T ve v(B)=T ise v(A∨B) kaçtır?",
                    ["T", "F", "Yalnız bağlama göre", "Tanımsız"],
                    "T",
                    "TFL'deki ∨ kapsayıcıdır; iki ayrılan birlikte doğru olabilir.",
                    "Orta",
                ),
                (
                    "Maddi koşul A→B hangi değer çiftinde yanlıştır?",
                    ["T/T", "T/F", "F/T", "F/F"],
                    "T/F",
                    "A'nın doğru olup B'nin yanlış olması koşulun dışladığı tek durumdur.",
                    "Temel",
                ),
                (
                    "v(A)=F ve v(B)=F ise v(A→B) kaçtır?",
                    ["T", "F", "Belirsiz", "Bağlama göre"],
                    "T",
                    "Önbileşen yanlış olduğunda T/F ihlali oluşmaz; maddi koşul doğrudur.",
                    "Orta",
                ),
                (
                    "v(A)=F ve v(B)=F ise v(A↔B) kaçtır?",
                    ["T", "F", "A", "Belirlenemez"],
                    "T",
                    "Çift yönlü koşul iki taraf aynı doğruluk değerindeyse doğrudur.",
                    "Orta",
                ),
                (
                    "v(A)=T, v(B)=F altında ¬(A∧B)→B için doğru hesap sırası hangisidir?",
                    [
                        "Önce →, sonra ¬, sonra ∧",
                        "Önce A∧B, sonra ¬(A∧B), sonra →",
                        "Yalnız soldan sağa sembolleri saymak",
                        "Önce B'nin gerçek dünyadaki doğruluğunu araştırmak",
                    ],
                    "Önce A∧B, sonra ¬(A∧B), sonra →",
                    "Oluşum ağacı en iç alt cümlelerden ana bağlaca doğru ilerlemeyi gerektirir.",
                    "Orta",
                ),
                (
                    "v(A)=F, v(B)=T, v(C)=F altında (A∨B)↔¬C kaçtır?",
                    ["T", "F", "Belirsiz", "C"],
                    "T",
                    "A∨B=T ve ¬C=T; aynı değerli iki taraf T↔T sonucunu verir.",
                    "İleri",
                ),
                (
                    "Hangisi yalnız bileşenlerinin mevcut doğruluk değerleriyle her zaman belirlenmeyebilir?",
                    ["A ve B", "A veya B", "A çünkü B", "A değil"],
                    "A çünkü B",
                    "A ile B'nin doğruluğu, aralarındaki açıklama ilişkisinin doğruluğunu tek başına belirlemez.",
                    "İleri",
                ),
                (
                    "Bir cümle bu tek değerlemede T çıktı. Bundan hangisi çıkar?",
                    [
                        "Yalnız bu değerleme altında doğrudur",
                        "Bütün değerlemelerde doğrudur",
                        "Doğal dilde zorunlu bir doğrudur",
                        "Kanıt kurallarıyla türetilmiştir",
                    ],
                    "Yalnız bu değerleme altında doğrudur",
                    "Bütün değerlemelerdeki statü, tek bir atamadan belirlenemez ve sonraki derslerin konusudur.",
                    "Zor",
                ),
            ]
        ),
        {
            "prompt": "v(A)=T, v(B)=F ve v(C)=T altında ((A∨B)∧¬C)→B cümlesini içten dışa değerlendir.",
            "starter": "1. Atomları kaydet: A=T, B=F, C=T.\n2. En iç iki alt cümleyi bul: (A∨B) ve ¬C.",
            "checks": [
                "A∨B için kapsayıcı ayrık bağlacın koşulu uygulanmıştır",
                "¬C, C'nin değeri tersine çevrilerek hesaplanmıştır",
                "(A∨B)∧¬C, maddi koşuldan önce tamamlanmıştır",
                "Ana bağlacın önbileşen/artbileşen değer çifti açıkça yazılmıştır",
                "Sonuç yalnız nihai harfle değil uygulanan karakteristik koşulla gerekçelendirilmiştir",
            ],
            "solution": "A∨B=T; ¬C=F; (A∨B)∧¬C=F. Ana bağlaçta önbileşen F, artbileşen B=F olur. Maddi koşul yalnız T/F birleşiminde yanlış olduğu için F→F=T. Bu sonuç yalnız verilen v değerlemesi içindir.",
        },
        [
            _production_task(
                "Üç ayrı değerleme-formül çiftini semantik iz halinde çöz. Her satırda atomik atamaları, iç alt cümleleri, ana bağlacı ve nihai değeri yaz; ardından doğal dil sınırı sorusunu yanıtla.",
                [
                    "Her değerlemede A, B ve C için verilen T/F atamalarını değiştirmeden kaydet.",
                    "Formülün ana bağlacını ve iki doğrudan alt cümlesini hesap başlamadan işaretle.",
                    "Her iç alt cümleyi ana bağlaçtan önce formülü ve değeriyle yaz.",
                    "¬, ∧, ∨, → ve ↔ koşullarının her birini çalışmanın bütününde en az bir kez açıkça gerekçelendir.",
                    "Nihai T/F sonucunun yalnız o değerleme altında geçerli olduğunu belirt.",
                    "Karşıolgusal doğal dil koşulunda maddi koşulun koruyamadığı en az iki bilgi türünü adlandır.",
                ],
                "Doğru nihai değerden önce yeniden üretilebilir hesap sırası ve model sınırı açıklaması üret.",
                "Tek değerleme çalışma kartları",
                [
                    "v₁(A)=T, v₁(B)=F, v₁(C)=T: ¬(A∧B)→C",
                    "v₂(A)=F, v₂(B)=F, v₂(C)=T: (A↔B)∧¬C",
                    "v₃(A)=T, v₃(B)=T, v₃(C)=F: (A∨C)↔(B∧¬C)",
                    "Sınır sorusu: 'Geçmişte farklı bir karar verseydim bugün burada olmazdım' cümlesindeki hangi bilgiler yalnız → ile görünmez kalır?",
                ],
                "Beklenen nihai değerler sırasıyla T, F ve T'dir. Bu anahtar yalnız son kontrol içindir; ara semantik iz ve sınır açıklaması olmadan görev tamamlanmış sayılmaz.",
            ),
        ],
        [
            "Öğrenci v(A)=T yazımını bir üst dil ataması olarak okur; T/F'yi TFL atomu veya gerçek dünya kanıtı saymaz.",
            "Beş bağlacın karakteristik doğruluk koşulunu en az bir örnekte doğru uygular.",
            "Karmaşık formüllerde atomlardan ana bağlaca uzanan semantik izi eksiksiz ve doğru sırada üretir.",
            "Maddi koşulun yalnız T/F değer çiftinde yanlış olduğunu hem temel hem karmaşık örnekte kullanır.",
            "Tek değerleme altındaki sonucu bütün değerlemeler hakkındaki bir statü iddiasından ayırır.",
            "TFL hesabının dışarıda bıraktığı en az bir nedensel, zamansal, açıklayıcı veya karşıolgusal ilişkiyi doğru adlandırır.",
        ],
        [
            "v(A)=T yazımı A hakkında ne söyler ve neyi henüz söylemez?",
            "A→B hangi tek değer çiftinde yanlıştır; neden?",
            "A↔B'nin iki taraf da yanlışken doğru olması hangi karakteristik koşuldan gelir?",
            "Karmaşık bir cümlenin semantik hesap sırasını hangi sözdizimsel yapı belirler?",
        ],
        "Sonraki derste tek bir değerlemeyi hesaplamakla yetinmeyip ilgili atomların bütün olası değerlemelerini eksiksiz ve tekrarsız düzenlemeyi öğreneceğiz.",
        [
            "forallx-use-mention",
            "forallx-characteristic-tables",
            "forallx-truth-functionality",
            "forallx-valuations",
            "mit-logic-sequence",
            "mit-logic-study-guide",
        ],
        "Bu ders yalnız verilen tek bir değerleme altında hesap yapar. Karakteristik bağlaç koşulları tam doğruluk tablosu değildir; bütün değerlemeleri üretme, cümle statüsü, semantik sonuç ve kanıt kuralları sonraki derslerin ayrı öğrenme eşikleridir.",
        [
            "ders-19-veya-ve-ise",
            "ders-20-dogruluk-tablolari-i",
        ],
    )

    lesson["reading_note"] = (
        "Önce değerlemeyi kopyala, sonra oluşum ağacının en iç düğümlerinden ana bağlaca ilerle. Her ara değerin yanına kullandığın bağlaç koşulunu yaz."
    )
    lesson["symbol_set"] = [
        "A",
        "B",
        "C",
        "T",
        "F",
        "v",
        "w",
        "¬",
        "∧",
        "∨",
        "→",
        "↔",
        "(",
        ")",
    ]
    lesson["proof_tools"] = [
        "Değerleme kartı",
        "Karakteristik doğruluk koşulları",
        "Ana bağlaç işaretleme",
        "İçten dışa semantik iz",
        "Maddi koşul T/F denetimi",
        "Doğruluk işlevselliği sınır notu",
    ]
    lesson["semantic_checks"] = [
        {
            "id": "negation",
            "formula": "¬A",
            "valuation": {"A": "T"},
            "expected": "F",
        },
        {
            "id": "conjunction",
            "formula": "A ∧ B",
            "valuation": {"A": "T", "B": "F"},
            "expected": "F",
        },
        {
            "id": "inclusive-disjunction",
            "formula": "A ∨ B",
            "valuation": {"A": "T", "B": "T"},
            "expected": "T",
        },
        {
            "id": "material-conditional-false",
            "formula": "A → B",
            "valuation": {"A": "T", "B": "F"},
            "expected": "F",
        },
        {
            "id": "material-conditional-false-antecedent",
            "formula": "A → B",
            "valuation": {"A": "F", "B": "F"},
            "expected": "T",
        },
        {
            "id": "biconditional-both-false",
            "formula": "A ↔ B",
            "valuation": {"A": "F", "B": "F"},
            "expected": "T",
        },
        {
            "id": "worked-complex",
            "formula": "¬(A ∧ B) → B",
            "valuation": {"A": "T", "B": "F"},
            "expected": "F",
        },
        {
            "id": "guided-complex",
            "formula": "((A ∨ B) ∧ ¬C) → B",
            "valuation": {"A": "T", "B": "F", "C": "T"},
            "expected": "T",
        },
        {
            "id": "production-one",
            "formula": "¬(A ∧ B) → C",
            "valuation": {"A": "T", "B": "F", "C": "T"},
            "expected": "T",
        },
        {
            "id": "production-two",
            "formula": "(A ↔ B) ∧ ¬C",
            "valuation": {"A": "F", "B": "F", "C": "T"},
            "expected": "F",
        },
        {
            "id": "production-three",
            "formula": "(A ∨ C) ↔ (B ∧ ¬C)",
            "valuation": {"A": "T", "B": "T", "C": "F"},
            "expected": "T",
        },
    ]
    return lesson


def _candidate_c15():
    lesson = _lesson(
        "C15",
        "ders-tam-dogruluk-tablosu-kurma",
        "Tam Doğruluk Tablosu Kurma",
        "Bir TFL cümlesindeki farklı atomları sayar, bütün değerlemeleri sistematik T/F örüntüsüyle üretir ve alt cümle sütunlarını ana bağlaca kadar eksiksiz doldurur.",
        "Bütün değerlemeleri eksiksiz tabloya dönüştürme",
        45,
        [
            "ders-degerlemeler-ve-dogruluk-islevleri",
            "ders-tfl-cumlesi-ana-baglac-ve-kapsam",
        ],
        [
            "tfl.table_rows_generate",
            "tfl.table_dependencies_order",
            "tfl.table_complete",
            "tfl.main_column_identify",
        ],
        [
            "Bir formüldeki farklı cümle harfi sayısından gerekli 2^n satır sayısını bulmak ve harf tekrarlarını ayrı atom sanmamak.",
            "Bütün değerlemeleri standart T/F blok örüntüsüyle eksiksiz, tekrarsız ve denetlenebilir sırada üretmek.",
            "Alt cümle sütunlarını oluşum ağacının bağımlılık sırasına göre atomlardan ana bağlaca doğru hesaplamak.",
            "Bütün formülün değerini veren ana bağlaç sütununu renk dışında başlık ve metin etiketiyle de ayırt etmek.",
            "Tabloyu satır kapsamı, sütun bağımlılığı ve bağımsız yeniden hesaplama denetimleriyle doğrulamak.",
        ],
        [
            (
                "Tam doğruluk tablosu",
                "Bir formüldeki farklı atomlar üzerindeki bütün olası değerlemeleri ve formülün her değerlemedeki hesabını gösteren tablo.",
            ),
            (
                "Değerleme satırı",
                "Atomların her birine bir kez T veya F atayan tek bir olası atama.",
            ),
            (
                "Atom sütunu",
                "Farklı bir TFL cümle harfinin bütün satırlardaki T/F örüntüsünü gösteren temel sütun.",
            ),
            (
                "Alt cümle sütunu",
                "Bir bileşik alt cümlenin, daha önce hesaplanmış doğrudan parçalarına dayanarak her satırda aldığı değeri gösteren sütun.",
            ),
            (
                "Ana sütun",
                "Bütün formülün ana bağlacında aldığı değerleri gösteren ve tablonun hedef sonucunu taşıyan sütun.",
            ),
            (
                "Blok örüntüsü",
                "İlk atomdan son atoma doğru T ve F bloklarını yarıya indirerek bütün değerlemeleri düzenli üretme yöntemi.",
            ),
            (
                "Tablo denetimi",
                "Satır sayısını, benzersiz atamaları, sütun bağımlılıklarını ve seçilen satırların yeniden hesabını kontrol etme işlemi.",
            ),
        ],
        [
            _section(
                "Tek değerlemeden bütün değerlemelere",
                "C14'te verilen tek bir değerleme hesaplandı. Tam tablo ise formülde geçen farklı atomlar üzerindeki bütün T/F atamalarını listeler; n farklı atom için 2^n satır gerekir.",
                "Bir formülün kaç ayrı değerleme altında hesaplanması gerektiğini belirlerken.",
                "farklı atom sayısı = n; tam satır sayısı = 2^n",
                "Her atom için iki seçenek vardır. Bağımsız n atomun T/F seçenekleri çarpıldığında 2×2×...×2 = 2^n farklı atama elde edilir. Aynı harfin formülde yeniden görünmesi yeni seçenek yaratmaz.",
                "Sembol sayısını, bağlaç sayısını veya atomun tekrar sayısını n sanma. Önce farklı cümle harflerinden oluşan kümeyi yaz.",
                [
                    (
                        "A∧B içinde farklı atomlar: A, B",
                        "n=2 olduğu için dört değerleme gerekir.",
                    ),
                    (
                        "(A↔A)∨¬A içinde farklı atomlar: yalnız A",
                        "A üç kez görünse de n=1 ve yalnız iki değerleme vardır.",
                    ),
                    (
                        "(A∧B)→¬C içinde farklı atomlar: A, B, C",
                        "n=3 olduğu için sekiz değerleme gerekir.",
                    ),
                ],
                (
                    "Formülü tarayıp farklı atomları bir kez listelemek ve 2^n hesabını bu listeye dayandırmak.",
                    "Formüldeki her harf görünümünü yeni atom sayıp gereğinden fazla satır üretmek.",
                    "Değerleme harf görünümüne değil cümle harfinin kendisine değer atar; aynı atom her geçtiği yerde aynı değeri taşır.",
                ),
            ),
            _section(
                "T/F bloklarıyla eksiksiz satır üretimi",
                "Standart sıra, ilk atomda en uzun bloklarla başlar; her sonraki atom T/F değişimini iki kat hızlandırır. Böylece hiçbir atama atlanmaz veya tekrarlanmaz.",
                "İki, üç veya daha çok atom için satırları sezgisel ve dağınık yazmak yerine sistematik olarak üretirken.",
                "A: TTTT/FFFF; B: TT/FF/TT/FF; C: T/F/T/F/T/F/T/F",
                "Üç atomlu standart sırada satırlar TTT, TTF, TFT, TFF, FTT, FTF, FFT, FFF olur. Bu sıra tek mümkün sıra değildir; fakat düzenli blok yöntemi tamlık denetimini kolaylaştırır.",
                "Satırları gelişigüzel sıralayıp sonra yalnız sayısını kontrol etme. Sekiz satır bulunması, bir satırın tekrarlanıp başka birinin atlanmadığını tek başına garanti etmez.",
                [
                    (
                        "İki atom: TT, TF, FT, FF",
                        "Dört olası atamanın her biri tam bir kez görünür.",
                    ),
                    (
                        "Üç atomda A sütunu TTTTFFFF",
                        "İlk atom dört T ve dört F ile en uzun blokları taşır.",
                    ),
                    (
                        "Üç atomda C sütunu TFTFTFTF",
                        "Son atom her satırda değer değiştirir.",
                    ),
                ],
                (
                    "Atomları alfabetik sıraya koyup T/F blok uzunluğunu her sütunda yarıya indirmek.",
                    "Rastgele satırlar yazıp eksik ve tekrarları gözle yakalamaya çalışmak.",
                    "Blok örüntüsü, bütün ikili seçim birleşimlerini görünür ve denetlenebilir kılar.",
                ),
            ),
            _section(
                "Alt cümle sütunları bağımlılık sırasını izler",
                "Atom sütunlarından sonra her bileşik alt cümle, doğrudan parçaları hazır olduğunda hesaplanır. Oluşum ağacında daha içte olan sütun daha önce gelir.",
                "Karmaşık formül için hangi ara sütunların gerektiğini ve hangi sırada doldurulacağını belirlerken.",
                "atomlar → en iç bileşikler → dış bileşikler → bütün formül",
                "(A∧B)→¬C için önce A, B, C; sonra A∧B ve ¬C; son olarak (A∧B)→¬C sütunu gerekir. Aynı alt cümle iki kez geçiyorsa tek hesap sütunu yeniden kullanılabilir.",
                "Formülde solda göründüğü için bir dış bağlacı önce hesaplama. Sütun sırasını yazı yönü değil sözdizimsel bağımlılık belirler.",
                [
                    (
                        "(A∧B)→¬C",
                        "A∧B ve ¬C ana koşuldan önce hazırlanmalıdır.",
                    ),
                    (
                        "¬(A∨B)↔(¬A∧¬B)",
                        "A∨B, ¬(A∨B), ¬A, ¬B ve ¬A∧¬B sütunları ana ↔ sütunundan önce gelir.",
                    ),
                    (
                        "(A∧B)↔(A∧B)",
                        "A∧B aynı yapısal alt cümle olduğu için bir sütunda hesaplanıp iki tarafta kullanılabilir.",
                    ),
                ],
                (
                    "Her sütunun doğrudan hangi hazır sütunlardan hesaplandığını oluşum ağacına göre yazmak.",
                    "Ana bağlaç sütununu ara değerler hazır değilken tahminle doldurmak.",
                    "Bağımlılık sırası hem hesap hatasını azaltır hem de yanlış parantezlemenin ürettiği farklı formülü görünür kılar.",
                ),
            ),
            _section(
                "Ana sütunu erişilebilir biçimde işaretleme",
                "Tablonun hedef sütunu, bütün formülün ana bağlacını temsil eder. Renk kullanılsa bile sütun başlığında 'Ana sütun' etiketi, kalın ayırıcı veya metinsel işaret bulunmalıdır.",
                "Bir tablodaki ara sütunlarla bütün formülün sonuç sütununu ayırırken ve tabloyu renk algısına bağlı olmadan okunabilir kılarken.",
                "Ana sütun: bütün formülün yeniden parantezlenmiş açık başlığı",
                "Ana sütun her zaman en sağdaki rastgele sütun değildir; tasarımda en sona yerleştirilse bile kimliği ana bağlaç çözümlemesinden gelir. Başlık formülün kapsamını korumalıdır.",
                "Yalnız hücre arka plan rengine güvenme, bağlacın son yazılan sembol olduğunu sanma veya alt cümle başlığındaki parantezleri düşürme.",
                [
                    (
                        "Ana sütun — ((A∧B)→¬C)",
                        "Metin etiketi ve tam parantez, hedef sütunu renk olmadan da tanımlar.",
                    ),
                    (
                        "Ara sütun — (A∧B)",
                        "Bu sütun gerekli olsa da bütün formülün sonucu değildir.",
                    ),
                    (
                        "¬C en sağda yazıldı diye ana sütun olmaz.",
                        "Ana bağlaç → olduğundan hedef sütun bütün koşul cümlesidir.",
                    ),
                ],
                (
                    "Ana bağlacı önce bulup tam formülü sütun başlığı ve 'Ana sütun' etiketiyle işaretlemek.",
                    "Ana sütunu yalnız renk veya fiziksel konumla belirtmek.",
                    "Renk dışı işaret, ekran okuyucu ve renk görme farklılıkları için tablo sonucunu erişilebilir kılar.",
                ),
            ),
            _section(
                "Tamlık ve yeniden hesaplama denetimi",
                "Bir tablo, doğru görünen son sütunla değil; satır kapsamı, benzersizlik, sütun bağımlılığı ve seçilmiş satırların bağımsız hesabıyla doğrulanır.",
                "Tabloyu teslim etmeden veya başka bir semantik iddiada kullanmadan önce.",
                "n atom → 2^n benzersiz satır; her sütun hazır girdilerden; en az iki satır yeniden hesaplanmış",
                "Önce atom listesini ve satır sayısını karşılaştır. Sonra her değerleme ikilisinin tek kez geçtiğini denetle. En son biri ana sütunun değer değiştirdiği sınır satırı olmak üzere en az iki satırı karakteristik koşullarla yeniden hesapla.",
                "Nihai sütun düzenli görünüyor diye tabloyu doğru kabul etme. Aynı yanlış ara sütun bütün ana sütunu tutarlı fakat hatalı gösterebilir.",
                [
                    (
                        "Üç atom, sekiz benzersiz satır",
                        "Satır kapsamının ilk zorunlu denetimidir.",
                    ),
                    (
                        "TTF ve FFF satırlarını baştan hesaplamak",
                        "Farklı bağlaç koşullarını kullanan iki bağımsız örnek sağlar.",
                    ),
                    (
                        "Ana sütun etiketi ile ana bağlacın uyuşması",
                        "Doğru hesaplanmış ara sütunun sonuç diye yanlış seçilmesini önler.",
                    ),
                ],
                (
                    "Tabloyu satır, sütun ve yeniden hesaplama olmak üzere üç ayrı düzeyde denetlemek.",
                    "Yalnız son sütundaki örüntüye bakıp tablonun tamamını onaylamak.",
                    "Tam tablo sonraki semantik sınıflandırmaların verisidir; yanlış tablo üzerine doğru kavram uygulanamaz.",
                ),
            ),
        ],
        [
            _worked(
                "A ve B için n=2; 2^2=4 satır",
                "Farklı iki atomun her biri iki değer alabildiği için dört benzersiz atama vardır.",
                "Satır sayısı",
            ),
            _worked(
                "A, B ve C için n=3; 2^3=8 satır",
                "Üç bağımsız ikili seçim sekiz değerleme üretir.",
                "Üç atom",
            ),
            _worked(
                "(A↔A)∨¬A için n=1; iki satır",
                "A'nın üç görünümü yeni atom değildir; aynı atama bütün görünümlerde korunur.",
                "Tekrarlı atom",
            ),
            _worked(
                "Üç atomun sırası: TTT, TTF, TFT, TFF, FTT, FTF, FFT, FFF",
                "Blok örüntüsü bütün atamaları bir kez üretir.",
                "Eksiksiz sıra",
            ),
            _worked(
                "(A∧B)→¬C sütun sırası: A, B, C, A∧B, ¬C, ana koşul",
                "Her bileşik sütun, doğrudan girdileri hazır olduktan sonra hesaplanır.",
                "Bağımlılık",
            ),
            _worked(
                "(A∧B)→¬C ana sütunu: F, T, T, T, T, T, T, T",
                "Standart sekiz satırda yalnız A=T, B=T, C=T iken önbileşen T ve ¬C=F olur.",
                "Tam örnek",
            ),
            _worked(
                "¬(A∨B)↔(¬A∧¬B) için ana sütun başlığını tam formülle yazmak",
                "↔ ana bağlaçtır; iki tarafın ara sütunları önce hesaplanır ve ana sütun renk dışında metinle de işaretlenir.",
                "Ana sütun",
            ),
            _worked(
                "Sekiz satır yazıp TTF satırını iki kez tekrarlamak",
                "Satır sayısı doğru olsa bile bir değerleme tekrarlanmışsa başka bir değerleme eksiktir; tablo tam değildir.",
                "Tamlık hatası",
                "bad",
            ),
        ],
        [
            "Formüldeki her harf görünümünü ayrı atom sayıp 2^n satır sayısını şişirmek.",
            "Üç atom için altı veya yedi satırın yeterli olduğunu sanmak.",
            "Doğru sayıda satır yazıp bir değerlemeyi tekrarlarken başka bir değerlemeyi atlamak.",
            "T/F bloklarını düzensiz değiştirip satır kapsamını gözle denetlenemez hâle getirmek.",
            "Dış alt cümleyi, doğrudan parçalarının sütunları hazır olmadan hesaplamak.",
            "En sağdaki veya son yazılan sembolün sütununu otomatik olarak ana sütun sanmak.",
            "Ana sütunu yalnız renkle işaretleyip metinsel başlık ve kapsam bilgisini vermemek.",
            "İki satırı bağımsız yeniden hesaplamadan yalnız düzenli görünen sonuç örüntüsüne güvenmek.",
        ],
        _practice(
            [
                (
                    "(A∧B)→A formülünde kaç farklı atom vardır?",
                    ["1", "2", "3", "4"],
                    "2",
                    "A iki kez görünse de farklı atom kümesi yalnız A ve B'dir.",
                    "Temel",
                ),
                (
                    "Üç farklı atom içeren bir tam tablo kaç satırdır?",
                    ["4", "6", "8", "9"],
                    "8",
                    "Her atom iki değer aldığı için 2^3=8 benzersiz değerleme vardır.",
                    "Temel",
                ),
                (
                    "(A↔A)∨¬A formülü için kaç satır gerekir?",
                    ["2", "4", "6", "8"],
                    "2",
                    "Formülde yalnız bir farklı atom vardır; tekrarlar satır sayısını artırmaz.",
                    "Orta",
                ),
                (
                    "İki atom için standart tam sıra hangisidir?",
                    [
                        "TT, TF, FT, FF",
                        "TT, FF, TT, FF",
                        "TF, TF, TF, TF",
                        "TT, TF, TT, FF",
                    ],
                    "TT, TF, FT, FF",
                    "A sütunu TTFF, B sütunu TFTF örüntüsüyle dört atamayı bir kez üretir.",
                    "Temel",
                ),
                (
                    "Üç atomlu standart sırada ilk atomun sütunu hangisidir?",
                    ["TFTFTFTF", "TTFFTTFF", "TTTTFFFF", "FFFFFFFF"],
                    "TTTTFFFF",
                    "İlk atom en uzun T ve F bloklarını kullanır.",
                    "Orta",
                ),
                (
                    "Üç atomlu standart sırada son atomun sütunu hangisidir?",
                    ["TFTFTFTF", "TTFFTTFF", "TTTTFFFF", "TTTTTTTT"],
                    "TFTFTFTF",
                    "Son atom her satırda T ile F arasında değişir.",
                    "Orta",
                ),
                (
                    "(A∧B)→¬C için atomlardan sonra ilk hangi iki ara sütun hazırlanmalıdır?",
                    [
                        "A→C ve B→C",
                        "A∧B ve ¬C",
                        "A∨B ve C∧A",
                        "Yalnız ana → sütunu",
                    ],
                    "A∧B ve ¬C",
                    "Ana koşulun doğrudan iki alt cümlesi bu ara sütunlara dayanır.",
                    "Orta",
                ),
                (
                    "¬(A∨B)↔(¬A∧¬B) formülünün ana bağlacı hangisidir?",
                    ["İlk ¬", "∨", "∧", "↔"],
                    "↔",
                    "Formülün son kurucu adımı iki büyük alt cümleyi ↔ ile birleştirir.",
                    "Orta",
                ),
                (
                    "Ana sütunu belirtmenin erişilebilir yolu hangisidir?",
                    [
                        "Yalnız yeşil arka plan kullanmak",
                        "Yalnız en sağa koymak",
                        "Tam formül başlığına 'Ana sütun' metin etiketi ve ayırıcı eklemek",
                        "Başlığı kaldırıp yalnız sonuçları göstermek",
                    ],
                    "Tam formül başlığına 'Ana sütun' metin etiketi ve ayırıcı eklemek",
                    "Metin ve yapısal işaret, sonucu renk algısından bağımsız kılar.",
                    "İleri",
                ),
                (
                    "Üç atomlu tabloda sekiz satır var; fakat TTF iki kez yazılmış. Ne çıkar?",
                    [
                        "Tablo yine tamdır",
                        "Başka bir değerleme eksiktir ve tablo tam değildir",
                        "Yalnız satır sırası değişmiştir",
                        "Atom sayısı dörde çıkmıştır",
                    ],
                    "Başka bir değerleme eksiktir ve tablo tam değildir",
                    "Doğru satır sayısı benzersizliği garanti etmez; her atama tam bir kez görünmelidir.",
                    "İleri",
                ),
                (
                    "Bir dış sütunu hesaplamadan önce ne hazır olmalıdır?",
                    [
                        "Yalnız ilk atom",
                        "Onun doğrudan alt cümle sütunları",
                        "Sonraki dersin kavram etiketleri",
                        "Formülün doğal dilde doğru olup olmadığı",
                    ],
                    "Onun doğrudan alt cümle sütunları",
                    "Sütun bağımlılığı oluşum ağacını izler; dış işlem hazır girdilerden hesaplanır.",
                    "Temel",
                ),
                (
                    "Tablo tesliminden önce en güçlü son denetim hangisidir?",
                    [
                        "Yalnız hücre renklerine bakmak",
                        "Satır kapsamını, sütun bağımlılığını ve iki bağımsız satır hesabını birlikte kontrol etmek",
                        "Ana sütunu ezberlenen örüntüyle değiştirmek",
                        "Parantezleri silip formülü kısaltmak",
                    ],
                    "Satır kapsamını, sütun bağımlılığını ve iki bağımsız satır hesabını birlikte kontrol etmek",
                    "Üç düzeyli denetim hem eksik değerlemeyi hem ara sütun hem de ana sütun hatasını yakalar.",
                    "Zor",
                ),
            ]
        ),
        {
            "prompt": "¬(A∨B)↔(¬A∧¬B) için yarı tamamlanmış dört satırlı tabloyu onar ve ana sütunu renk kullanmadan işaretle.",
            "starter": "Satırlar: TT, TF, FT, FF.\nSütun taslağı: A | B | A∨B | ¬(A∨B) | ¬A | ¬B | ¬A∧¬B | ana ↔.\nHata: Taslakta TF satırı iki kez, FT satırı hiç yazılmamış.",
            "checks": [
                "Dört değerlemenin her biri tam bir kez bulunur",
                "A∨B sütunu dış olumsuzlamadan önce hesaplanır",
                "¬A ile ¬B, onların birleşiminden önce hesaplanır",
                "Ana ↔ sütunu iki büyük alt cümlenin hazır değerlerinden bulunur",
                "Ana sütun tam formül başlığı ve metin etiketiyle belirtilir",
                "En az TT ve FF satırları karakteristik koşullarla yeniden hesaplanır",
            ],
            "solution": "Düzeltilmiş sıra TT, TF, FT, FF'dir. A∨B: T,T,T,F; ¬(A∨B): F,F,F,T; ¬A: F,F,T,T; ¬B: F,T,F,T; ¬A∧¬B: F,F,F,T. 'Ana sütun — ¬(A∨B)↔(¬A∧¬B)' değerleri T,T,T,T olur. Bu derste yalnız tablo tamamlanır; bu örüntüye verilecek semantik sınıf etiketi C16'ya bırakılır.",
        },
        [
            _production_task(
                "(A∨B)→(C∧¬A) formülü için sıfırdan tam doğruluk tablosu kur ve üç düzeyli denetim raporu ekle.",
                [
                    "Farklı atomları alfabetik sırada bir kez listele ve n ile 2^n hesabını yaz.",
                    "Sekiz değerlemeyi standart T/F blok örüntüsüyle eksiksiz ve tekrarsız üret.",
                    "A∨B, ¬A ve C∧¬A ara sütunlarını bağımlılık sırasına göre hesapla.",
                    "Bütün koşul cümlesini tam başlıkla 'Ana sütun' olarak metinsel biçimde işaretle.",
                    "Ana sütun değerlerini yalnız hazır doğrudan alt cümle sütunlarından üret.",
                    "TTT ve FTF satırlarını tablodan bağımsız olarak yeniden hesaplayıp karşılaştır.",
                    "Henüz cümleye sonraki derse ait bir semantik sınıf etiketi verme; yalnız tam ve doğrulanmış tabloyu teslim et.",
                ],
                "Satır üretimi, sütun bağımlılığı ve ana sütun denetimini birbirinden ayrı görünür kanıtlarla tamamla.",
                "Bağımsız tam tablo görevi",
                [
                    "Hedef formül: (A∨B)→(C∧¬A)",
                    "Farklı atomlar: öğrenci tarafından çıkarılacak",
                    "Satır sayısı: n belirlendikten sonra hesaplanacak",
                    "Zorunlu renk dışı işaret: 'Ana sütun' metin etiketi",
                ],
                "Kontrol anahtarında standart sıra için ana sütun F, F, F, F, T, F, T, T'dir. Bu dizi tek başına teslim sayılmaz; ara sütunlar ve denetim raporu zorunludur.",
            ),
        ],
        [
            "Öğrenci farklı n atomdan 2^n satır gerektiğini açıklar ve harf tekrarlarını ayrı atom saymaz.",
            "Bütün değerlemeleri standart T/F blok örüntüsüyle eksiksiz ve tekrarsız üretir.",
            "Alt cümle sütunlarını oluşum ağacına uygun bağımlılık sırasıyla hesaplar.",
            "Bütün formülün ana sütununu doğru seçer ve renk dışında metin etiketiyle de gösterir.",
            "En az iki satırı karakteristik bağlaç koşullarıyla bağımsız yeniden hesaplar.",
            "Tam tabloyu sonraki dersin cümle statüsü etiketini peşinen kullanmadan teslim eder.",
        ],
        [
            "Aynı cümle harfinin beş kez geçmesi satır sayısını neden değiştirmez?",
            "Üç atom için standart T/F bloklarının uzunlukları nasıl ilerler?",
            "Ana bağlaç sütunundan önce hangi alt cümle sütunları hazır olmalıdır?",
            "Sekiz satır bulunması neden tek başına tablonun tam olduğunu kanıtlamaz?",
        ],
        "Sonraki derste doğru kurulmuş ana sütunun bütün değerlemelerdeki örüntüsünü kullanarak tek bir TFL cümlesinin semantik statüsünü sınıflandıracağız.",
        [
            "forallx-characteristic-tables",
            "forallx-truth-functionality",
            "forallx-valuations",
            "mit-logic-sequence",
            "mit-logic-study-guide",
        ],
        "Bu ders yalnız tam tablo üretiminin mekanik ve denetlenebilir doğruluğunu ölçer. Ana sütun örüntüsünü totoloji, çelişki veya olumsallık olarak sınıflandırmak C16'nın ayrı öğrenme eşiğidir; semantik sonuç, geçerlilik, kısmi tablo ve kanıt kuralları daha sonraki derslere aittir.",
        ["ders-20-dogruluk-tablolari-i"],
    )

    lesson["reading_note"] = (
        "Önce farklı atomları ve 2^n satırı doğrula; sonra T/F bloklarını kur. Her bileşik sütunu yalnız doğrudan alt cümle sütunları hazır olduğunda hesapla."
    )
    lesson["symbol_set"] = [
        "A",
        "B",
        "C",
        "T",
        "F",
        "n",
        "2^n",
        "¬",
        "∧",
        "∨",
        "→",
        "↔",
        "(",
        ")",
    ]
    lesson["proof_tools"] = [
        "Farklı atom envanteri",
        "2^n satır hesabı",
        "T/F blok örüntüsü",
        "Alt cümle bağımlılık sırası",
        "Renk dışı ana sütun etiketi",
        "Benzersiz satır denetimi",
        "İki satırlık bağımsız yeniden hesaplama",
    ]
    lesson["table_checks"] = [
        {
            "id": "complete-three-atom-example",
            "formula": "(A ∧ B) → ¬C",
            "expected_atoms": ["A", "B", "C"],
            "expected_row_count": 8,
            "expected_compound_columns": [
                "(A ∧ B)",
                "¬C",
                "((A ∧ B) → ¬C)",
            ],
            "expected_main_values": ["F", "T", "T", "T", "T", "T", "T", "T"],
        },
        {
            "id": "repeated-atom-example",
            "formula": "(A ↔ A) ∨ ¬A",
            "expected_atoms": ["A"],
            "expected_row_count": 2,
            "expected_compound_columns": [
                "(A ↔ A)",
                "¬A",
                "((A ↔ A) ∨ ¬A)",
            ],
            "expected_main_values": ["T", "T"],
        },
        {
            "id": "guided-de-morgan-table",
            "formula": "¬(A ∨ B) ↔ (¬A ∧ ¬B)",
            "expected_atoms": ["A", "B"],
            "expected_row_count": 4,
            "expected_compound_columns": [
                "(A ∨ B)",
                "¬(A ∨ B)",
                "¬A",
                "¬B",
                "(¬A ∧ ¬B)",
                "(¬(A ∨ B) ↔ (¬A ∧ ¬B))",
            ],
            "expected_main_values": ["T", "T", "T", "T"],
        },
        {
            "id": "independent-production-table",
            "formula": "(A ∨ B) → (C ∧ ¬A)",
            "expected_atoms": ["A", "B", "C"],
            "expected_row_count": 8,
            "expected_compound_columns": [
                "(A ∨ B)",
                "¬A",
                "(C ∧ ¬A)",
                "((A ∨ B) → (C ∧ ¬A))",
            ],
            "expected_main_values": ["F", "F", "F", "F", "T", "F", "T", "T"],
        },
    ]
    return lesson


def _candidate_c16():
    lesson = _lesson(
        "C16",
        "ders-totoloji-celiski-ve-olumsallik",
        "Totoloji, Çelişki ve Olumsallık",
        "Bir TFL cümlesinin tek bir değerlemedeki doğruluk değerini bütün değerlemelerdeki davranışından ayırır; doğrulanmış ana sütunu totoloji, çelişki veya olumsallık olarak sınıflandırır.",
        "Tek TFL cümlesinin semantik statüsü",
        35,
        [
            "ders-3-gecerlilik-ve-dogruluk",
            "ders-kullanim-anma-ve-dil-duzeyleri",
            "ders-tam-dogruluk-tablosu-kurma",
        ],
        [
            "tfl.status_classify",
            "tfl.status_justify",
            "tfl.truth_vs_tautology_distinguish",
            "metalanguage.formula_status_state",
        ],
        [
            "Totoloji, çelişki ve olumsallığı ana sütunun bütün satırlarını nicelikli ifadelerle tarayarak tanımlamak.",
            "Tek bir değerlemede doğru veya yanlış çıkmayı, bir cümlenin bütün değerlemelerdeki semantik statüsünden ayırmak.",
            "Olumsallığı en az bir doğru ve en az bir yanlış satırı açıkça göstererek gerekçelendirmek.",
            "'Doğru cümle' ile 'totoloji', 'yanlış cümle' ile 'çelişki' arasındaki tür farkını açıklamak.",
            "TFL'deki statünün yalnız sembolleştirilen doğruluk işlevsel yapıyı sınadığını ve doğal dildeki her zorunluluğu yakalamadığını belirtmek.",
        ],
        [
            (
                "Semantik statü",
                "Tek bir TFL cümlesinin bütün olası değerlemelerde aldığı doğruluk değerlerinin oluşturduğu sınıf.",
            ),
            (
                "Totoloji (tautology)",
                "Her değerlemede Doğru (T) olan TFL cümlesi.",
            ),
            (
                "Çelişki",
                "Her değerlemede Yanlış (F) olan tek TFL cümlesi.",
            ),
            (
                "Olumsal cümle",
                "En az bir değerlemede Doğru (T) ve en az bir değerlemede Yanlış (F) olan TFL cümlesi.",
            ),
            (
                "Ana sütun örüntüsü",
                "Tam tabloda bütün formülün her değerlemede aldığı T/F değerlerinin sıralı dizisi.",
            ),
            (
                "Doğru tanığı",
                "Olumsal bir cümlenin Doğru (T) çıktığını gösteren açık bir değerleme satırı.",
            ),
            (
                "Yanlış tanığı",
                "Olumsal bir cümlenin Yanlış (F) çıktığını gösteren açık bir değerleme satırı.",
            ),
        ],
        [
            _section(
                "Bir satırdaki değer ile bütün tablodaki statü",
                "v(𝒜)=T, 𝒜 cümlesinin yalnız v değerlemesinde doğru olduğunu söyler. Totoloji, çelişki ve olumsallık ise aynı cümlenin bütün değerlemelerdeki davranışını sınıflandırır.",
                "Bir tablo satırından elde edilen sonucu cümlenin genel statüsüyle karıştırmamak için.",
                "tek satır: v(𝒜)=T veya F; statü: ana sütunun bütün satırları",
                "Doğruluk değeri bir değerlemeye görelidir. Semantik statü ise tam değerleme uzayına bakılarak belirlenir. Bu yüzden tek doğru satır totolojiyi, tek yanlış satır çelişkiyi kanıtlamaz.",
                "'Bu satırda doğru' cümlesinden 'totolojidir' sonucuna atlama. Önce tablonun tam ve ana sütunun doğrulanmış olması gerekir.",
                [
                    (
                        "A→B, A=F ve B=F iken T'dir.",
                        "Bu yalnız bir satır sonucudur; aynı formül A=T ve B=F iken F olur.",
                    ),
                    (
                        "A∨¬A, A=T iken T ve A=F iken T'dir.",
                        "Tek atomun iki değerlemesi de tarandığı için genel statü çıkarılabilir.",
                    ),
                    (
                        "A∧¬A, A=T iken F ve A=F iken F'dir.",
                        "Bütün satırlar F olduğunda tek cümle çelişki olarak sınıflandırılır.",
                    ),
                ],
                (
                    "Önce tek satırın değerini, sonra bütün ana sütunun statüsünü ayrı cümlelerle belirtmek.",
                    "Bir satırdaki T veya F değerini doğrudan genel statü etiketi yapmak.",
                    "Değerleme niceleyicisi değişir: satır iddiası 'bu değerlemede', statü iddiası 'bütün değerlemelerde' veya 'en az bir değerlemede' der.",
                ),
            ),
            _section(
                "Üç statüyü niceliklerle tanımlama",
                "Totoloji için her satır T, çelişki için her satır F, olumsallık içinse en az bir T ve en az bir F gerekir.",
                "Ana sütun örüntüsünü ezberlenmiş biçimlere değil tanımlara göre sınıflandırırken.",
                "her T → totoloji; her F → çelişki; en az bir T ve en az bir F → olumsal",
                "Üç sınıf klasik iki değerli TFL'de birbirini dışlar ve bütün tek-cümle ana sütun örüntülerini kapsar. T oranı değil, gerekli nicelik koşulunun karşılanması belirleyicidir.",
                "'Çoğu satır T'yi totoloji, 'çoğu satır F'yi çelişki sanma. Tek karşı örnek bile ilk iki evrensel iddiayı bozar ve iki değerin de bulunduğu örüntüyü olumsal yapar.",
                [
                    (
                        "T,T,T,T",
                        "Dört satırın her biri T olduğu için totolojidir.",
                    ),
                    (
                        "F,F,F,F",
                        "Dört satırın her biri F olduğu için çelişkidir.",
                    ),
                    (
                        "T,F,T,T",
                        "Hem T hem F bulunduğu için olumsaldır; üç doğru satır totoloji için yeterli değildir.",
                    ),
                ],
                (
                    "Statü gerekçesinde 'her', 'hiçbir' veya iki ayrı 'en az bir' niceliğini açıkça kullanmak.",
                    "T ve F hücrelerini sayıp çoğunluğa göre statü seçmek.",
                    "Totoloji ve çelişki evrensel koşullardır; olumsallık iki farklı türde tanık gerektiren karma koşuldur.",
                ),
            ),
            _section(
                "Ana sütundan güvenli sınıflandırma akışı",
                "Statü kararı, yalnız tamlığı ve hesabı denetlenmiş ana sütundan verilir: önce F var mı, sonra T var mı diye bakılır ve tanık satırlar kaydedilir.",
                "Tam tabloyu bir semantik statü iddiasına dönüştürürken.",
                "tamlık → ana sütun → F ara → T ara → statü ve tanık",
                "Ana sütunda hiç F yoksa totoloji; hiç T yoksa çelişki; ikisi de varsa olumsallık bulunur. Olumsal sonuçta bir doğru ve bir yanlış değerleme açıkça yazılır. Evrensel statülerde bütün satır kapsamı denetlenir.",
                "Ara sütunu ana sütun sanma veya eksik tabloda görünmeyen satırları yok sayma. Statü, doğru kurulmamış tablonun düzenli görünen son sütunundan güvenle çıkmaz.",
                [
                    (
                        "(A∧B)→A ana sütunu T,T,T,T",
                        "Hiç F yoktur; tam dört satır doğrulandığında formül totolojidir.",
                    ),
                    (
                        "(A∨B)∧¬(A∨B) ana sütunu F,F,F,F",
                        "Hiç T yoktur; formül çelişkidir.",
                    ),
                    (
                        "A→B ana sütunu T,F,T,T",
                        "TT doğru tanığı, TF yanlış tanığı olabilir; formül olumsaldır.",
                    ),
                ],
                (
                    "Statüden önce C15 denetimlerini tamamlamak ve olumsallıkta iki karşıt tanığı açıkça göstermek.",
                    "Formülün görünüşüne bakıp tablo kurmadan etiketi tahmin etmek.",
                    "Statü, sözdizimsel benzerlikten değil bütün değerlemelerde hesaplanan ana sütundan gelir.",
                ),
            ),
            _section(
                "Fiili doğruluk, zorunlu doğruluk ve TFL yapısı",
                "Bir doğal dil cümlesi fiilen veya başka bir kuramda zorunlu doğru olabilir; fakat TFL'de yapısız bir atom olarak temsil edilirse hem T hem F değerlemesi alır ve olumsal görünür.",
                "'Bu açıkça doğrudur, öyleyse totolojidir' türündeki doğal dil itirazlarını değerlendirirken.",
                "Doğal dil içeriği → sembolleştirme seçimi → TFL'nin görebildiği doğruluk işlevsel yapı",
                "TFL tablosu aritmetik, tanımsal, modal veya kavramsal zorunluluğu içeriden çözümlemez. `2+2=4` cümlesi A atomu olarak bırakılırsa A için T ve F satırları üretir; bu, aritmetiğin yanlış olabileceğini değil temsilin o yapıyı kodlamadığını gösterir.",
                "TFL'deki olumsal etiketini doğal dil cümlesinin metafizik statüsü hakkında eksiksiz hüküm sanma. Sonuç sembol anahtarına ve korunan yapıya bağlıdır.",
                [
                    (
                        "A: 2+2=4",
                        "A atomik bırakıldığında TFL tablosu A'yı T ve F değerlemeleri altında tarar; formül TFL bakımından olumsaldır.",
                    ),
                    (
                        "A∨¬A",
                        "Totoloji, A'nın içeriğinden değil açık doğruluk işlevsel biçimden doğar.",
                    ),
                    (
                        "A: Ankara Türkiye'nin başkentidir.",
                        "Fiilen doğru olması, yalnız A biçiminin her değerlemede doğru olmasını sağlamaz.",
                    ),
                ],
                (
                    "Statüyü 'bu sembolleştirmede, TFL bakımından' kaydıyla ifade etmek.",
                    "Doğal dilde doğru görünen her atomu totoloji ilan etmek.",
                    "Doğruluk tablosu yalnız formülde temsil edilen doğruluk işlevsel yapıya duyarlıdır.",
                ),
            ),
            _section(
                "Cümlenin kendisi ile statü iddiasını ayırma",
                "A∨¬A bir TFL cümlesidir; 'A∨¬A bir totolojidir' ise o cümleden söz eden üst dil iddiasıdır. Statü etiketi formülün içine yeni bir bağlaç gibi yazılmaz.",
                "Çözümde nesne dili formülünü, tablo verisini ve sonuç cümlesini açık katmanlarda sunarken.",
                "formül | tam tablo | üst dilde statü ve gerekçe",
                "TFL cümlesi her satırda T veya F alır. Onun statüsünü söyleyen açıklama ise bütün satırları niceliklendiren üst dil cümlesidir. 'Totoloji' tek cümlenin, 'geçerli' ise argümanın değerlendirme türüdür.",
                "Statü sözcüğünü formülün parçası sanma veya tek cümleye 'geçerli argüman' etiketi verme. Kullanılan ifade türünü koru.",
                [
                    (
                        "Formül: A∨¬A",
                        "Bu satır nesne dilindeki hedef TFL cümlesini gösterir.",
                    ),
                    (
                        "Sonuç: 'A∨¬A' her değerlemede T olduğu için totolojidir.",
                        "Tırnaklı formülden söz eden üst dil cümlesi statüyü ve gerekçeyi verir.",
                    ),
                    (
                        "A→B olumsaldır.",
                        "İddia tek cümlenin statüsüdür; bir argümanın sonucunu değerlendirmez.",
                    ),
                ],
                (
                    "Formülü, tablosunu ve formülden söz eden statü cümlesini ayrı göstermek.",
                    "'Totoloji'yi nesne diline eklenmiş bir operatör ya da argüman etiketi gibi kullanmak.",
                    "Kullanım/anma ayrımı, tablo hücresinin değeriyle formül hakkındaki genel iddiayı aynı satıra sıkıştırmayı önler.",
                ),
            ),
        ],
        [
            _worked(
                "A∨¬A: T,T; totoloji",
                "A'nın bütün değerlemelerinde ana sütun T'dir.",
                "Her satır T",
            ),
            _worked(
                "A∧¬A: F,F; çelişki",
                "A'nın bütün değerlemelerinde ana sütun F'dir.",
                "Her satır F",
            ),
            _worked(
                "A→B: T,F,T,T; olumsal",
                "En az bir doğru ve en az bir yanlış değerleme vardır.",
                "İki tanık",
            ),
            _worked(
                "(A∧B)→A: T,T,T,T; totoloji",
                "Önbileşenin doğru olduğu her durumda A zaten doğrudur; öteki satırlarda maddi koşul doğrudur.",
                "Yapısal örnek",
            ),
            _worked(
                "A↔¬A: F,F; çelişki",
                "A ile ¬A hiçbir değerlemede aynı doğruluk değerini taşımaz.",
                "Çift yönlü",
            ),
            _worked(
                "A atomu: T,F; olumsal",
                "Atomun fiili içeriği tabloya ek bir kısıt getirmez; iki değerleme de taranır.",
                "Atomik örnek",
            ),
            _worked(
                "A→B üç satırda T olduğu için totolojidir.",
                "Bir F satırı evrensel doğruluk koşulunu bozar; doğru statü olumsaldır.",
                "Çoğunluk hatası",
                "bad",
            ),
            _worked(
                "2+2=4 doğrudur; A olarak yazıldığı için A totolojidir.",
                "Fiili veya aritmetik doğruluk, atomik TFL biçiminin bütün değerlemelerde T olmasını sağlamaz.",
                "Temsil hatası",
                "bad",
            ),
        ],
        [
            "Tek doğru satırı totoloji için yeterli saymak.",
            "Tek yanlış satırı çelişki için yeterli saymak.",
            "Dört satırın üçünün doğru olmasını çoğunlukla totoloji ilan etmek.",
            "Olumsallık gerekçesinde yalnız doğru ya da yalnız yanlış tanığı göstermek.",
            "Tamlığı denetlenmemiş veya bir değerlemesi eksik tabloya statü vermek.",
            "Ara sütunun T/F örüntüsünü bütün formülün ana sütunu sanmak.",
            "Fiilen doğru atomik bir doğal dil cümlesini TFL totolojisi saymak.",
            "Tek TFL cümlesine 'geçerli', bir argümana 'totoloji' etiketi vermek.",
            "Cümlenin kendisi ile o cümlenin statüsünü bildiren üst dil ifadesini karıştırmak.",
        ],
        _practice(
            [
                (
                    "Ana sütunu T,T,T,T olan bir TFL cümlesinin statüsü nedir?",
                    ["Totoloji", "Çelişki", "Olumsal", "Geçerli argüman"],
                    "Totoloji",
                    "Bütün değerlemelerde T olan tek cümle totolojidir.",
                    "Temel",
                ),
                (
                    "Ana sütunu F,F,F,F olan tek TFL cümlesinin statüsü nedir?",
                    ["Totoloji", "Çelişki", "Olumsal", "Sağlam"],
                    "Çelişki",
                    "Bütün değerlemelerde F olan tek cümle çelişkidir.",
                    "Temel",
                ),
                (
                    "Ana sütunu T,F,T,T olan bir cümlenin statüsü nedir?",
                    ["Totoloji", "Çelişki", "Olumsal", "Belirsiz"],
                    "Olumsal",
                    "En az bir T ve en az bir F satırı bulunduğu için cümle olumsaldır.",
                    "Temel",
                ),
                (
                    "A→B formülü A=F, B=F satırında T çıktı. Bundan tek başına ne çıkar?",
                    [
                        "A→B bir totolojidir",
                        "A→B yalnız bu değerlemede doğrudur",
                        "A→B bir çelişkidir",
                        "Bütün tablo tamamlanmıştır",
                    ],
                    "A→B yalnız bu değerlemede doğrudur",
                    "Tek satır sonucu, bütün değerlemeler üzerindeki statüyü belirlemez.",
                    "Temel",
                ),
                (
                    "Bir totolojiyi yanlışlamak için kaç yanlış satır bulmak yeterlidir?",
                    ["Hiçbiri", "Bir", "Yarıdan fazlası", "Bütün satırlar"],
                    "Bir",
                    "Totoloji her değerlemede T olmalıdır; tek F satırı evrensel koşulu bozar.",
                    "Orta",
                ),
                (
                    "Olumsallığı göstermek için en az hangi kanıt çifti gerekir?",
                    [
                        "İki doğru satır",
                        "İki yanlış satır",
                        "Bir doğru ve bir yanlış değerleme",
                        "Yalnız formülün görünüşü",
                    ],
                    "Bir doğru ve bir yanlış değerleme",
                    "Olumsallık iki doğruluk değerinin de en az bir kez gerçekleşmesini gerektirir.",
                    "Orta",
                ),
                (
                    "A atomunun tam ana sütunu T,F ise TFL bakımından statüsü nedir?",
                    ["Totoloji", "Çelişki", "Olumsal", "Geçerli"],
                    "Olumsal",
                    "Atomun bir T ve bir F değerlemesi vardır; doğal dildeki fiili doğruluk tablo düzenini değiştirmez.",
                    "Orta",
                ),
                (
                    "'2+2=4' cümlesi A atomuyla gösterildiğinde A neden TFL totolojisi çıkmaz?",
                    [
                        "Aritmetik yanlıştır",
                        "A atomik biçimi aritmetik iç yapıyı temsil etmez",
                        "Totoloji yalnız iki atomla kurulur",
                        "TFL'de T değeri yoktur",
                    ],
                    "A atomik biçimi aritmetik iç yapıyı temsil etmez",
                    "TFL yalnız açıkça sembolleştirilen doğruluk işlevsel yapıyı sınar.",
                    "İleri",
                ),
                (
                    "Statü kararından hemen önce hangi veri zorunludur?",
                    [
                        "Formülün günlük dilde ikna edici olması",
                        "Tamlığı ve hesabı denetlenmiş ana sütun",
                        "Yalnız ilk tablo satırı",
                        "Yazarın niyeti",
                    ],
                    "Tamlığı ve hesabı denetlenmiş ana sütun",
                    "Statü bütün değerlemelerdeki ana formül değerlerine dayanır.",
                    "Orta",
                ),
                (
                    "'A∨¬A bir totolojidir' ifadesi hangi düzeydedir?",
                    [
                        "A∨¬A formülünün içine eklenmiş yeni bağlaç",
                        "TFL cümlesinden söz eden üst dil iddiası",
                        "Yalnız bir değerleme satırı",
                        "Bir argümanın sonucu",
                    ],
                    "TFL cümlesinden söz eden üst dil iddiası",
                    "Statü cümlesi hedef formülün bütün değerlemelerdeki davranışından söz eder.",
                    "İleri",
                ),
                (
                    "Bir formül sekiz satırın yedisinde F, birinde T ise hangisi doğrudur?",
                    [
                        "Çelişkidir çünkü çoğu satır F'dir",
                        "Olumsaldır çünkü hem T hem F vardır",
                        "Totolojidir çünkü bir T vardır",
                        "Statüsü yoktur",
                    ],
                    "Olumsaldır çünkü hem T hem F vardır",
                    "Çoğunluk kullanılmaz; iki farklı değerin bulunması olumsallık için yeterlidir.",
                    "İleri",
                ),
                (
                    "Tek TFL cümlesinin semantik statüsü için uygun etiket hangisidir?",
                    ["Totoloji", "Geçerli argüman", "Sağlam argüman", "Güçlü tümevarım"],
                    "Totoloji",
                    "Totoloji tek cümlenin bütün değerlemelerdeki statüsüdür; öteki seçenekler argüman değerlendirmeleridir.",
                    "Zor",
                ),
            ]
        ),
        {
            "prompt": "Ana sütunları verilen üç tam tabloyu sınıflandır; her statüyü tanımındaki nicelikle gerekçelendir ve hatalı çoğunluk yorumunu onar.",
            "starter": "Tablo I: T,T,T,T\nTablo II: F,F,F,F\nTablo III: T,F,T,T\nHatalı yorum: Tablo III dört satırın üçünde doğru olduğundan totolojidir.",
            "checks": [
                "Tablo I için bütün satırların T olduğu açıkça belirtilir",
                "Tablo II için bütün satırların F olduğu açıkça belirtilir",
                "Tablo III için en az bir T ve en az bir F satırı gösterilir",
                "Çoğunluğun statü ölçütü olmadığı açıklanır",
                "Her etiket tek TFL cümlesinin ana sütununa bağlanır",
                "Tek satır doğruluğu ile genel statü ayrı cümlelerle yazılır",
            ],
            "solution": "Tablo I totolojidir; her değerlemede T'dir. Tablo II çelişkidir; her değerlemede F'dir. Tablo III olumsaldır; ilk satır doğru tanığı, ikinci satır yanlış tanığıdır. Üç T hücresi çoğunluk sağlar ama totoloji için gereken her satırda T koşulunu sağlamaz.",
        },
        [
            _production_task(
                "Bir totoloji, bir çelişki ve bir olumsal TFL cümlesi üret; her biri için tam tablo, ana sütun etiketi ve nicelikli statü gerekçesi ver.",
                [
                    "Üç formülün her biri en az bir TFL bağlacı içerir ve iyi biçimlenmiştir.",
                    "Her formül için farklı atomlar, 2^n satır ve eksiksiz değerlemeler gösterilir.",
                    "Alt cümle sütunları bağımlılık sırasıyla hesaplanır ve ana sütun metinle işaretlenir.",
                    "Totoloji gerekçesi bütün satırların T olduğunu söyler.",
                    "Çelişki gerekçesi bütün satırların F olduğunu söyler.",
                    "Olumsallık gerekçesi bir doğru ve bir yanlış değerlemeyi açıkça yazar.",
                    "Fiilen doğru olabilecek bir doğal dil cümlesi ayrıca atomik sembolleştirilir ve TFL bakımından neden olumsal çıktığı açıklanır.",
                ],
                "Sonuç etiketinden önce tablo tamlığını; etiketten sonra doğru niceliği ve gerekiyorsa iki karşıt tanığı görünür kıl.",
                "Üretim koşulları",
                [
                    "Totoloji: en az iki atom içersin",
                    "Çelişki: yalnız A∧¬A örneğini kopyalama",
                    "Olumsal: bir doğru ve bir yanlış satırını adlandır",
                    "Doğal dil örneği: fiilen doğru olabilir fakat TFL'de atom olarak bırakılır",
                ],
                "Örnek cevap ailesi: (A∧B)→A; (A∨B)∧¬(A∨B); ¬(A↔B). Öğrenci aynı üç formülü kopyalamak yerine kendi örneklerini kurmalıdır.",
            ),
        ],
        [
            "Üç statüyü sırasıyla her T, her F ve hem en az bir T hem en az bir F nicelikleriyle tanımlar.",
            "Sınıflandırmayı tamlığı ve hesabı denetlenmiş ana sütunun bütün satırlarına dayandırır.",
            "Olumsal cümle için bir doğru ve bir yanlış değerlemeyi açık tanık olarak gösterir.",
            "Tek değerlemedeki doğruluk değeri ile bütün değerlemelerdeki semantik statüyü ayrı ifadelerle açıklar.",
            "Fiili doğruluk ile TFL totolojisini en az bir atomik sembolleştirme örneğiyle ayırır.",
            "Formül, tablo ve formülden söz eden üst dil statü cümlesini ayrı katmanlarda sunar.",
        ],
        [
            "Bir cümle üç satırda doğru, bir satırda yanlışsa hangi statüdedir ve neden?",
            "Olumsal bir cümle için gereken iki tanık türü nedir?",
            "Zorunlu doğru bir doğal dil cümlesi atomik bırakıldığında neden TFL totolojisi çıkmayabilir?",
            "Tek satırda v(𝒜)=T yazmak ile 𝒜'nın totoloji olduğunu söylemek arasındaki fark nedir?",
        ],
        "Sonraki derste tek cümlenin statüsünden iki cümlenin bütün satırlardaki ilişkisine ve bir cümle kümesinin ortak doğruluk imkânına geçeceğiz.",
        [
            "forallx-use-mention",
            "forallx-truth-functionality",
            "forallx-valuations",
            "forallx-logical-concepts",
            "mit-logic-sequence",
            "mit-logic-study-guide",
        ],
        "Bu ders yalnız tek bir TFL cümlesinin bütün değerlemelerdeki statüsünü ölçer. Eşdeğerlik ve cümle kümeleri C17'ye, argüman değerlendirmesi C18'e, kısmi tablo ve kanıt yöntemleri daha sonraki aşamalara bırakılır. TFL totolojisi, seçilen sembolleştirmenin doğruluk işlevsel yapısına göredir; doğal dildeki bütün zorunluluk türlerinin eksiksiz çözümlemesi değildir.",
        ["ders-21-dogruluk-tablolari-ii-ve-gecerlilik"],
    )

    lesson["reading_note"] = (
        "Önce tablonun tamlığını ve ana sütunu doğrula. Sonra T ve F dağılımını 'her', 'hiçbir' ve iki ayrı 'en az bir' koşuluyla sınıflandır."
    )
    lesson["symbol_set"] = [
        "A",
        "B",
        "C",
        "𝒜",
        "v",
        "T",
        "F",
        "¬",
        "∧",
        "∨",
        "→",
        "↔",
        "(",
        ")",
    ]
    lesson["proof_tools"] = [
        "Tam tablo denetimi",
        "Ana sütun örüntüsü",
        "Bütün-satırlar T denetimi",
        "Bütün-satırlar F denetimi",
        "Doğru ve yanlış tanık çifti",
        "Kullanım/anma katman ayrımı",
        "Sembolleştirme sınırı notu",
    ]
    lesson["status_checks"] = [
        {
            "id": "excluded-middle",
            "formula": "A ∨ ¬A",
            "expected_status": "tautology",
            "expected_main_values": ["T", "T"],
            "expected_true_count": 2,
            "expected_false_count": 0,
        },
        {
            "id": "direct-contradiction",
            "formula": "A ∧ ¬A",
            "expected_status": "contradiction",
            "expected_main_values": ["F", "F"],
            "expected_true_count": 0,
            "expected_false_count": 2,
        },
        {
            "id": "material-conditional-contingent",
            "formula": "A → B",
            "expected_status": "contingency",
            "expected_main_values": ["T", "F", "T", "T"],
            "expected_true_count": 3,
            "expected_false_count": 1,
        },
        {
            "id": "conjunction-elimination-shape",
            "formula": "(A ∧ B) → A",
            "expected_status": "tautology",
            "expected_main_values": ["T", "T", "T", "T"],
            "expected_true_count": 4,
            "expected_false_count": 0,
        },
        {
            "id": "compound-contradiction",
            "formula": "(A ∨ B) ∧ ¬(A ∨ B)",
            "expected_status": "contradiction",
            "expected_main_values": ["F", "F", "F", "F"],
            "expected_true_count": 0,
            "expected_false_count": 4,
        },
        {
            "id": "atomic-contingency",
            "formula": "A",
            "expected_status": "contingency",
            "expected_main_values": ["T", "F"],
            "expected_true_count": 1,
            "expected_false_count": 1,
        },
        {
            "id": "opposite-biconditional",
            "formula": "A ↔ ¬A",
            "expected_status": "contradiction",
            "expected_main_values": ["F", "F"],
            "expected_true_count": 0,
            "expected_false_count": 2,
        },
        {
            "id": "sparse-contingency",
            "formula": "(A ∨ B) ∧ ¬A",
            "expected_status": "contingency",
            "expected_main_values": ["F", "F", "T", "F"],
            "expected_true_count": 1,
            "expected_false_count": 3,
        },
        {
            "id": "conditional-cover",
            "formula": "(A → B) ∨ (B → A)",
            "expected_status": "tautology",
            "expected_main_values": ["T", "T", "T", "T"],
            "expected_true_count": 4,
            "expected_false_count": 0,
        },
        {
            "id": "incompatible-conditional-conjunction",
            "formula": "(A → B) ∧ (A ∧ ¬B)",
            "expected_status": "contradiction",
            "expected_main_values": ["F", "F", "F", "F"],
            "expected_true_count": 0,
            "expected_false_count": 4,
        },
        {
            "id": "independent-production-contingency",
            "formula": "¬(A ↔ B)",
            "expected_status": "contingency",
            "expected_main_values": ["F", "T", "T", "F"],
            "expected_true_count": 2,
            "expected_false_count": 2,
        },
    ]
    return lesson


def _candidate_c17():
    lesson = _lesson(
        "C17",
        "ders-mantiksal-esdegerlik-ve-tutarlilik",
        "Mantıksal Eşdeğerlik ve Tutarlılık",
        "İki TFL cümlesini ortak değerleme uzayındaki bütün satırlarda karşılaştırır; bir cümle kümesinin üyelerini aynı anda doğru yapan ortak bir değerleme bulunup bulunmadığını sınar.",
        "Cümle ilişkileri ve cümle kümelerinin ortak doğruluğu",
        45,
        [
            "ders-totoloji-celiski-ve-olumsallik",
            "ders-tfl-cumlesi-ana-baglac-ve-kapsam",
        ],
        [
            "tfl.equivalence_test",
            "tfl.satisfiability_test",
            "tfl.semantic_relation_witness",
            "tfl.single_vs_set_property_distinguish",
        ],
        [
            "İki TFL cümlesinin ortak atom uzayındaki bütün değerlemelerde aynı doğruluk değerini alıp almadığını sınamak.",
            "Eşdeğer olmayan iki cümle için doğruluk değerlerini ayıran en az bir açık değerleme göstermek.",
            "Bir cümle kümesinin bütün üyelerini aynı anda doğru yapan ortak değerleme bulunup bulunmadığını belirlemek.",
            "Birlikte doyurulabilirliği tek ortak doğru satırla, birlikte doyurulamazlığı bütün satırların elenmesiyle gerekçelendirmek.",
            "Tek cümlenin statüsü, iki cümlenin eşdeğerliği ve cümle kümesinin tutarlılığı için doğru semantik türü ve dil düzeyini korumak.",
        ],
        [
            (
                "Mantıksal eşdeğerlik",
                "İki TFL cümlesinin ortak atomları üzerindeki her değerlemede aynı doğruluk değerini alması.",
            ),
            (
                "Ortak değerleme uzayı",
                "Karşılaştırılan bütün cümlelerde geçen farklı atomların birleşimi üzerinde üretilen tam değerleme kümesi.",
            ),
            (
                "Ayırıcı değerleme",
                "İki cümleden birini doğru, diğerini yanlış yaparak eşdeğer olmadıklarını gösteren değerleme.",
            ),
            (
                "Cümle kümesi",
                "Aynı değerleme altında birlikte incelenen bir veya daha çok TFL cümlesi.",
            ),
            (
                "Birlikte doyurulabilir",
                "Kümenin bütün üyelerini aynı anda doğru yapan en az bir ortak değerlemesi bulunan cümle kümesi.",
            ),
            (
                "Birlikte doyurulamaz",
                "Kümenin bütün üyelerini aynı anda doğru yapan hiçbir değerlemesi bulunmayan cümle kümesi.",
            ),
            (
                "Semantik tutarlılık",
                "Bu derste birlikte doyurulabilir cümle kümesi için kullanılan açıklayıcı eş anlamlı terim.",
            ),
            (
                "Ortak doğru tanığı",
                "Doyurulabilir bir kümenin bütün cümlelerini aynı satırda doğru yapan açık değerleme.",
            ),
        ],
        [
            _section(
                "Eşdeğerlik bütün satırlarda sütun eşleşmesidir",
                "İki TFL cümlesi, ortak atom uzayındaki her değerlemede aynı T/F değerini alıyorsa mantıksal olarak eşdeğerdir.",
                "Farklı görünen iki formülün aynı doğruluk koşullarını taşıyıp taşımadığını sınarken.",
                "her değerlemede v(𝒜)=v(ℬ) → 𝒜 ile ℬ mantıksal olarak eşdeğer",
                "Önce iki formülde geçen bütün farklı atomlar birleştirilir. Sonra her değerlemede iki ana sütun yan yana karşılaştırılır. Tek satırdaki eşleşme değil, bütün satırlardaki eşleşme gerekir.",
                "Formüllerin yalnız ortak görünen atomlarını tabloya alma veya birkaç örnek satır eşleşti diye eşdeğerlik ilan etme.",
                [
                    (
                        "¬(A∨B): F,F,F,T; ¬A∧¬B: F,F,F,T",
                        "Dört ortak satırın tamamında değerler aynı olduğu için cümleler eşdeğerdir.",
                    ),
                    (
                        "A→B: T,F,T,T; ¬A∨B: T,F,T,T",
                        "A ve B üzerindeki bütün satırlar eşleşir.",
                    ),
                    (
                        "A ile A∨B karşılaştırılırken atomlar A ve B'dir.",
                        "B yalnız ikinci formülde geçse de ortak değerleme uzayına alınır.",
                    ),
                ],
                (
                    "Her iki ana sütunu ortak ve eksiksiz değerleme sırasıyla satır satır karşılaştırmak.",
                    "Formüller benzer göründüğü veya seçilen tek satırda aynı çıktığı için eşdeğer saymak.",
                    "Eşdeğerlik evrensel bir semantik ilişkidir; görünüşe veya örnek çoğunluğuna değil bütün değerlemelere dayanır.",
                ),
            ),
            _section(
                "Eşdeğer olmamaya bir ayırıcı değerleme yeter",
                "Bir satırda iki ana sütun farklıysa eşdeğerlik için gereken bütün-satırlar koşulu bozulur. Bu satır ayırıcı değerlemedir.",
                "Eşdeğer olmadığı ileri sürülen iki cümle için kısa fakat kesin bir tanık sunarken.",
                "v(𝒜)≠v(ℬ) olan en az bir satır → eşdeğer değiller",
                "Eşdeğerlik evrensel iddia olduğu için tek ayırıcı değerleme onu çürütür. Ayırıcı satırda atom atamaları ve hangi cümlenin T, hangisinin F olduğu birlikte yazılmalıdır.",
                "Yalnız 'sütunlar farklı' deme veya atom atamalarını gizleme. Tanık, çözümün yeniden hesaplanabilmesini sağlamalıdır.",
                [
                    (
                        "A→B ile B→A; A=T, B=F",
                        "İlk cümle F, ikinci cümle T olur; bu satır eşdeğer olmadıklarını gösterir.",
                    ),
                    (
                        "A∨B ile A∧B; A=T, B=F",
                        "A∨B T, A∧B F olur ve sütunlar ayrılır.",
                    ),
                    (
                        "A ile A∨B; A=F, B=T",
                        "A F iken A∨B T olur; ortak uzaydaki B değeri ayırıcıdır.",
                    ),
                ],
                (
                    "Ayırıcı değerlemeyi atom atamaları ve iki sonuç değeriyle açıkça raporlamak.",
                    "Bir formülün tek başına yanlış çıktığı herhangi bir satırı ayırıcı sanmak.",
                    "Ayırıcı değerleme aynı satırda iki hedef cümlenin farklı değerler almasını gerektirir.",
                ),
            ),
            _section(
                "Birlikte doyurulabilirlik ortak doğru satır arar",
                "Bir cümle kümesi, bütün üyelerini aynı anda T yapan en az bir değerleme varsa birlikte doyurulabilirdir; bu satır ortak doğru tanığıdır.",
                "Birden çok iddianın aynı olası durumda birlikte doğru olup olamayacağını sınarken.",
                "en az bir v: kümedeki her cümle v altında T",
                "Her formül için ayrı ayrı doğru satır bulmak yetmez. Aynı atom ataması, kümedeki bütün ana sütunları aynı satırda T yapmalıdır. Tek ortak doğru satır varlık iddiasını kanıtlar.",
                "Kümenin her üyesi bir yerde doğru diye kümenin birlikte doyurulabilir olduğunu sanma; doğru satırların aynı değerleme olması gerekir.",
                [
                    (
                        "{A∨B, ¬A}; A=F, B=T",
                        "A∨B ve ¬A aynı satırda T olduğundan küme birlikte doyurulabilirdir.",
                    ),
                    (
                        "{A, B}; A=T, B=T",
                        "Tek ortak doğru tanığı iki cümleyi aynı anda sağlar.",
                    ),
                    (
                        "{A→B, ¬B}; A=F, B=F",
                        "Koşul ve ¬B aynı satırda T'dir; küme doyurulabilir.",
                    ),
                ],
                (
                    "Bir ortak doğru değerlemeyi bütün cümlelerin o satırdaki T değerleriyle göstermek.",
                    "Her cümle için farklı bir doğru değerleme seçip bunları tek tanık gibi birleştirmek.",
                    "Birlikte doğruluk tek ve aynı değerlemeye göre ölçülür.",
                ),
            ),
            _section(
                "Birlikte doyurulamazlık bütün ortak adayları eler",
                "Bir cümle kümesi için hiçbir değerleme bütün üyeleri aynı anda T yapmıyorsa küme birlikte doyurulamazdır; semantik olarak tutarsızdır.",
                "Ortak doğru tanığı bulunamadığında bunun arama eksikliği mi yoksa imkânsızlık mı olduğunu kanıtlarken.",
                "her değerleme satırında en az bir küme üyesi F → birlikte doyurulamaz",
                "Yokluk iddiası tek örnekle kanıtlanmaz. Ortak atom uzayındaki bütün satırlar taranır ve her satırda en az bir cümlenin F olduğu gösterilir. Üyelerin tek tek olumsal olması ortak doğruluğu garanti etmez.",
                "İlk iki satırda ortak doğruluk bulamayınca aramayı bırakma veya kümeye bir bütün olarak 'çelişki cümlesi' deme.",
                [
                    (
                        "{A, ¬A}",
                        "A=T iken ¬A F; A=F iken A F. Ortak doğru satır yoktur.",
                    ),
                    (
                        "{A→B, A, ¬B}",
                        "A ve ¬B birlikte T olduğunda koşul F olur; diğer satırlarda A veya ¬B F'dir.",
                    ),
                    (
                        "{A∨B, ¬A, ¬B}",
                        "İki olumsuzlama T olduğunda ayrık birleşim F olur; başka satırlarda olumsuzlamalardan biri F'dir.",
                    ),
                ],
                (
                    "Bütün değerleme satırlarında en az bir üyenin neden F olduğunu görünür kılmak.",
                    "Ortak tanık bulamamayı, tam tabloyu tüketmeden imkânsızlık kanıtı saymak.",
                    "Birlikte doyurulamazlık ortak doğru satırın yokluğudur; her üyenin tek başına çelişki olması gerekmez.",
                ),
            ),
            _section(
                "Tek cümle, iki cümle ilişkisi ve cümle kümesi",
                "Totoloji, çelişki ve olumsallık tek cümleyi; eşdeğerlik iki cümle arasındaki ilişkiyi; birlikte doyurulabilirlik ise cümle kümesini sınıflandırır.",
                "Aynı tabloda farklı semantik sorular sorulduğunda doğru sonucu doğru nesneye yüklerken.",
                "tek cümle statüsü | iki cümle ilişkisi | kümenin ortak doğruluğu",
                "A↔B bir TFL cümlesidir ve kendi ana sütunu vardır. 'A ile B mantıksal olarak eşdeğerdir' ise iki cümlenin bütün değerlemelerde aynı davranmasını söyleyen üst dil iddiasıdır. Bu derste yeni bir eşdeğerlik işareti kullanılmaz.",
                "A↔B formülünü eşdeğerlik iddiasının kendisi sanma; tek cümleye tutarlı küme, kümeye olumsal cümle etiketi verme.",
                [
                    (
                        "A↔B olumsaldır.",
                        "Bu, tek TFL cümlesinin ana sütun statüsüdür.",
                    ),
                    (
                        "A→B ile ¬A∨B mantıksal olarak eşdeğerdir.",
                        "Bu, iki farklı cümlenin bütün satırlardaki ilişkisini bildirir.",
                    ),
                    (
                        "{A∨B, ¬A} birlikte doyurulabilirdir.",
                        "Bu, cümle kümesinin ortak doğru değerleme özelliğidir.",
                    ),
                ],
                (
                    "Sonuç cümlesinde değerlendirilen nesneyi ve kullanılan semantik türü açıkça adlandırmak.",
                    "TFL bağlacı, iki cümle ilişkisi ve cümle kümesi özelliğini tek işaret veya tek etiket altında toplamak.",
                    "Dil düzeyi ve nesne türü ayrımı sonraki semantik sonuç dersinde işaretlerin görevlerini korumak için zorunludur.",
                ),
            ),
        ],
        [
            _worked(
                "¬(A∨B) ile ¬A∧¬B: F,F,F,T / F,F,F,T",
                "Ortak dört satırın tamamında ana sütunlar eşleşir.",
                "Eşdeğer",
            ),
            _worked(
                "A→B ile ¬A∨B: T,F,T,T / T,F,T,T",
                "İki cümle A ve B üzerindeki her değerlemede aynı sonucu verir.",
                "Koşul biçimi",
            ),
            _worked(
                "A→B ile B→A; A=T, B=F",
                "İlk cümle F, ikinci cümle T olduğundan satır ayırıcıdır.",
                "Ayırıcı tanık",
            ),
            _worked(
                "A∨B ile A∧B; yalnız TT ve FF satırlarına bakmak",
                "TF ve FT satırları sütunları ayırır; iki eşleşme bütün-satırlar koşuluna yetmez.",
                "Eksik tarama",
                "bad",
            ),
            _worked(
                "{A∨B, ¬A}; A=F, B=T",
                "Aynı satır iki cümleyi de T yapar.",
                "Ortak tanık",
            ),
            _worked(
                "{A, ¬A}: ortak doğru satır yok",
                "İki atomik statü olumsal olsa da küme birlikte doyurulamazdır.",
                "Küme özelliği",
            ),
            _worked(
                "{A→B, A, ¬B}: ortak doğru satır yok",
                "A ve ¬B'nin T olduğu tek adayda A→B F olur.",
                "Bütün adaylar elenir",
            ),
            _worked(
                "Her cümle ayrı bir satırda doğru; öyleyse küme doyurulabilir.",
                "Birlikte doğruluk aynı değerlemeyi gerektirir; farklı satırlar tek ortak tanık oluşturmaz.",
                "Satır birleştirme",
                "bad",
            ),
            _worked(
                "A↔B formülü ile 'A ve B eşdeğerdir' iddiası",
                "İlki nesne dilinde tek cümle, ikincisi iki cümleden söz eden üst dil iddiasıdır.",
                "Dil düzeyi",
            ),
        ],
        [
            "İki cümlenin bir veya çoğu satırda aynı değeri almasını eşdeğerlik için yeterli saymak.",
            "Karşılaştırılan cümlelerin bütün atomlarının birleşimi yerine yalnız ortak görünen atomları tabloya almak.",
            "Ayırıcı değerlemede yalnız atomları yazıp iki hedef cümlenin farklı sonuçlarını göstermemek.",
            "Her cümle için farklı doğru satır seçip kümeyi birlikte doyurulabilir ilan etmek.",
            "Bir ortak doğru tanık bulunmasına rağmen bütün tabloyu gereksiz yere varlık kanıtı için zorunlu sanmak.",
            "Birkaç satırda ortak doğruluk bulamayınca kümeyi birlikte doyurulamaz saymak.",
            "Tek tek olumsal cümlelerden oluşan her kümeyi otomatik olarak tutarlı saymak.",
            "Birlikte doyurulamaz kümeye tek bir çelişki cümlesiymiş gibi davranmak.",
            "A↔B cümlesini 'A ile B mantıksal olarak eşdeğerdir' üst dil iddiasıyla aynı tür sanmak.",
            "Eşdeğerliği henüz tanıtılmamış kanıt içi yeniden yazma izni olarak kullanmak.",
        ],
        _practice(
            [
                (
                    "İki cümlenin mantıksal olarak eşdeğer olması için ne gerekir?",
                    [
                        "En az bir satırda aynı değeri almaları",
                        "Her ortak değerlemede aynı değeri almaları",
                        "Aynı sembol sayısına sahip olmaları",
                        "İkisinin de bir yerde doğru olması",
                    ],
                    "Her ortak değerlemede aynı değeri almaları",
                    "Eşdeğerlik bütün ortak değerleme uzayında sütun eşleşmesi gerektirir.",
                    "Temel",
                ),
                (
                    "Eşdeğer olmadığını göstermeye ne yeter?",
                    [
                        "Bir ayırıcı değerleme",
                        "İki aynı satır",
                        "Formüllerin farklı uzunlukta olması",
                        "Bir ortak doğru satır",
                    ],
                    "Bir ayırıcı değerleme",
                    "Tek satırda farklı doğruluk değerleri evrensel eşleşme iddiasını çürütür.",
                    "Temel",
                ),
                (
                    "A ile A∨B karşılaştırılırken ortak atom uzayı hangisidir?",
                    ["Yalnız A", "Yalnız B", "A ve B", "Hiçbiri"],
                    "A ve B",
                    "Karşılaştırılan iki cümlede geçen bütün farklı atomlar birleştirilir.",
                    "Orta",
                ),
                (
                    "A→B ile B→A için hangi satır ayırıcıdır?",
                    [
                        "A=T, B=T",
                        "A=T, B=F",
                        "A=F, B=F",
                        "Hiçbir satır",
                    ],
                    "A=T, B=F",
                    "Bu satırda A→B F, B→A T olur.",
                    "Orta",
                ),
                (
                    "Bir cümle kümesi ne zaman birlikte doyurulabilirdir?",
                    [
                        "Her üye farklı bir satırda doğruysa",
                        "En az bir değerleme bütün üyeleri aynı anda doğru yapıyorsa",
                        "Üyelerin çoğu totolojiyse",
                        "Hiç ortak atom yoksa",
                    ],
                    "En az bir değerleme bütün üyeleri aynı anda doğru yapıyorsa",
                    "Ortak doğru tanığı tek ve aynı atom atamasıdır.",
                    "Temel",
                ),
                (
                    "{A∨B, ¬A} kümesini hangi değerleme birlikte doğru yapar?",
                    [
                        "A=T, B=T",
                        "A=T, B=F",
                        "A=F, B=T",
                        "A=F, B=F",
                    ],
                    "A=F, B=T",
                    "A∨B ve ¬A bu satırda birlikte T olur.",
                    "Orta",
                ),
                (
                    "Birlikte doyurulamazlık nasıl kanıtlanır?",
                    [
                        "Tek bir başarısız satır gösterilerek",
                        "Bütün değerlemelerde en az bir üyenin F olduğu gösterilerek",
                        "Üyelerden biri olumsal bulunarak",
                        "Kümenin adı değiştirilerek",
                    ],
                    "Bütün değerlemelerde en az bir üyenin F olduğu gösterilerek",
                    "Ortak doğru satırın yokluğu bütün ortak uzayın taranmasını gerektirir.",
                    "İleri",
                ),
                (
                    "A ve ¬A tek tek hangi statüde, birlikte hangi durumdadır?",
                    [
                        "İkisi de olumsal; küme birlikte doyurulamaz",
                        "İkisi de çelişki; küme doyurulabilir",
                        "İkisi de totoloji; küme tutarlı",
                        "Statüleri yoktur",
                    ],
                    "İkisi de olumsal; küme birlikte doyurulamaz",
                    "Her biri ayrı ayrı T ve F alır, fakat aynı satırda ikisi birden T olamaz.",
                    "İleri",
                ),
                (
                    "A↔B ile 'A ve B eşdeğerdir' arasındaki doğru ayrım hangisidir?",
                    [
                        "İkisi de aynı TFL cümlesidir",
                        "İlki TFL cümlesi, ikincisi iki cümle hakkındaki üst dil iddiasıdır",
                        "İlki cümle kümesi, ikincisi atomdur",
                        "Aralarında hiçbir fark yoktur",
                    ],
                    "İlki TFL cümlesi, ikincisi iki cümle hakkındaki üst dil iddiasıdır",
                    "Nesne dili bağlacı ile semantik ilişki iddiası farklı dil düzeylerindedir.",
                    "İleri",
                ),
                (
                    "Doyurulabilir bir küme için en kısa kesin kanıt hangisidir?",
                    [
                        "Bir ortak doğru değerleme",
                        "Bir ayırıcı değerleme",
                        "Bir yanlış satır",
                        "Her formülün uzunluğu",
                    ],
                    "Bir ortak doğru değerleme",
                    "Varlık iddiasını bütün üyeleri aynı anda T yapan tek tanık kanıtlar.",
                    "Temel",
                ),
                (
                    "İki cümlenin ana sütunları üç satırda aynı, bir satırda farklıysa ne çıkar?",
                    [
                        "Eşdeğerdirler",
                        "Eşdeğer değildirler",
                        "İkisi de çelişkidir",
                        "Küme doyurulamazdır",
                    ],
                    "Eşdeğer değildirler",
                    "Tek farklı satır eşdeğerlik için gereken evrensel eşleşmeyi bozar.",
                    "Orta",
                ),
                (
                    "Hangisi tek cümlenin değil cümle kümesinin özelliğidir?",
                    ["Olumsallık", "Totoloji", "Birlikte doyurulabilirlik", "Çelişki"],
                    "Birlikte doyurulabilirlik",
                    "Bu özellik kümenin bütün üyelerinin ortak bir doğru satırı olup olmadığını sorar.",
                    "Zor",
                ),
            ]
        ),
        {
            "prompt": "İki cümle çiftini ve iki cümle kümesini ortak atom tablolarıyla incele; gereken yerde ayırıcı veya ortak doğru tanığı ver.",
            "starter": "Çift I: ¬(A∨B) / ¬A∧¬B\nÇift II: A→B / B→A\nKüme I: {A∨B, A→C, B→C}\nKüme II: {A→B, A, ¬B}",
            "checks": [
                "Her problem için bütün formüllerde geçen atomların birleşimi çıkarılır",
                "Çift I'in iki ana sütunu bütün satırlarda karşılaştırılır",
                "Çift II için en az bir ayırıcı değerleme iki sonuç değeriyle yazılır",
                "Küme I için bütün üyeleri aynı anda T yapan ortak satır gösterilir",
                "Küme II için bütün ortak doğru adaylarının neden elendiği gösterilir",
                "Tek cümle statüsü, iki cümle ilişkisi ve küme özelliği doğru terimlerle ayrılır",
            ],
            "solution": "Çift I eşdeğerdir: iki ana sütun F,F,F,T'dir. Çift II eşdeğer değildir: A=T, B=F iken A→B F, B→A T olur; bu satır ayırıcı değerlemedir. Küme I birlikte doyurulabilirdir; A=T, B=T, C=T bütün üyeleri T yapar. Küme II birlikte doyurulamazdır: A ve ¬B'nin birlikte T olduğu A=T, B=F satırında A→B F olur; diğer satırlarda A veya ¬B zaten F'dir.",
        },
        [
            _production_task(
                "İki cümle çifti ve iki cümle kümesi tasarla; her birini ortak atom sütunlu tam tabloyla sınayıp semantik tanıklarıyla raporla.",
                [
                    "Bir çift mantıksal olarak eşdeğer, bir çift eşdeğer olmayan iyi biçimlenmiş TFL cümlelerinden oluşur.",
                    "Eşdeğer çift için iki ana sütunun bütün satırlarda aynı olduğu gösterilir.",
                    "Eşdeğer olmayan çift için atom atamaları ve iki farklı sonuç değeri taşıyan ayırıcı satır verilir.",
                    "Bir küme birlikte doyurulabilir, bir küme birlikte doyurulamaz olacak biçimde en az ikişer cümle içerir.",
                    "Doyurulabilir küme için bütün üyeleri aynı anda T yapan ortak değerleme verilir.",
                    "Birlikte doyurulamaz küme için ortak atom uzayındaki bütün satırların neden elendiği gösterilir.",
                    "Her sonuç cümlesinde değerlendirilen nesnenin tek cümle, cümle çifti veya cümle kümesi olduğu açıkça yazılır.",
                ],
                "Evrensel iddialarda bütün satırları, varlık iddialarında açık tanığı ve yokluk iddialarında tam eleme kaydını görünür kıl.",
                "Üretim kısıtları",
                [
                    "Eşdeğer çift: yalnız aynı formülü iki kez yazma",
                    "Eşdeğer olmayan çift: en az bir ayırıcı satır adlandır",
                    "Doyurulabilir küme: en az üç cümle kullan",
                    "Birlikte doyurulamaz küme: üyelerin hepsi tek başına olumsal olsun",
                ],
                "Örnek aileler yalnız denetim içindir: A→B / ¬A∨B; A∨B / A∧B; {A∨B, ¬A}; {A→B, A, ¬B}. Öğrenci farklı yapılar üretmelidir.",
            ),
        ],
        [
            "Eşdeğerlik kararını iki ana sütunun ortak değerleme uzayındaki bütün satırlarıyla gerekçelendirir.",
            "Eşdeğer olmayan çift için en az bir ayırıcı değerlemeyi atom ve sonuç değerleriyle açıkça gösterir.",
            "Doyurulabilir küme için bütün üyeleri aynı anda doğru yapan ortak değerleme sunar.",
            "Birlikte doyurulamaz küme için hiçbir ortak doğru satır kalmadığını eksiksiz tabloyla gösterir.",
            "Tek cümle statüsü, iki cümle ilişkisi ve cümle kümesi özelliğini doğru terimlerle ayırır.",
            "A↔B TFL cümlesi ile iki cümlenin eşdeğer olduğunu söyleyen üst dil iddiasını birbirine dönüştürmeden açıklar.",
        ],
        [
            "Her biri olumsal iki cümle neden birlikte doyurulamaz olabilir?",
            "Eşdeğer olmadığını göstermek için nasıl bir değerleme gerekir?",
            "Doyurulabilirliği bir satırla kanıtlayabilirken birlikte doyurulamazlık neden bütün satırları gerektirir?",
            "A↔B ile 'A ve B mantıksal olarak eşdeğerdir' arasındaki dil düzeyi farkı nedir?",
        ],
        "Sonraki derste cümle kümelerinin ortak doğruluğundan öncül-sonuç ilişkisine geçerek argüman geçerliliğini ve karşı değerlemeyi sınayacağız.",
        [
            "forallx-use-mention",
            "forallx-valuations",
            "forallx-logical-concepts",
            "mit-logic-sequence",
            "mit-logic-study-guide",
        ],
        "Bu ders iki cümlenin semantik eşdeğerliği ile cümle kümelerinin birlikte doyurulabilirliğini ölçer. Argüman geçerliliği ve semantik sonuç C18'e, eşdeğerlikleri kanıt satırında yeniden yazma lisansı D aşamasına bırakılır. 'Çelişki' tek cümleye, 'birlikte doyurulamaz' ve açıklayıcı eş anlamlı olarak 'semantik tutarsız' cümle kümesine ayrılır.",
        ["ders-21-dogruluk-tablolari-ii-ve-gecerlilik"],
    )

    lesson["reading_note"] = (
        "İki cümle için ortak atom uzayında bütün sütunları karşılaştır; küme için aynı satırda bütün üyelerin T olmasını ara. Varlık iddiasına bir tanık, yokluk iddiasına tam tarama gerekir."
    )
    lesson["symbol_set"] = [
        "A",
        "B",
        "C",
        "𝒜",
        "ℬ",
        "v",
        "T",
        "F",
        "¬",
        "∧",
        "∨",
        "→",
        "↔",
        "{",
        "}",
        "(",
        ")",
    ]
    lesson["proof_tools"] = [
        "Ortak atom envanteri",
        "Yan yana ana sütun karşılaştırması",
        "Ayırıcı değerleme",
        "Ortak doğru değerleme",
        "Bütün satırları eleme kaydı",
        "Tek cümle/çift/küme tür denetimi",
        "Nesne dili/üst dil ayrımı",
    ]
    lesson["equivalence_checks"] = [
        {
            "id": "de-morgan-equivalence",
            "left": "¬(A ∨ B)",
            "right": "¬A ∧ ¬B",
            "expected_equivalent": True,
            "expected_separating_valuations": [],
        },
        {
            "id": "conditional-equivalence",
            "left": "A → B",
            "right": "¬A ∨ B",
            "expected_equivalent": True,
            "expected_separating_valuations": [],
        },
        {
            "id": "double-negation-equivalence",
            "left": "¬¬A",
            "right": "A",
            "expected_equivalent": True,
            "expected_separating_valuations": [],
        },
        {
            "id": "disjunction-commutativity",
            "left": "A ∨ B",
            "right": "B ∨ A",
            "expected_equivalent": True,
            "expected_separating_valuations": [],
        },
        {
            "id": "disjunction-vs-conjunction",
            "left": "A ∨ B",
            "right": "A ∧ B",
            "expected_equivalent": False,
            "expected_separating_valuations": [
                {"A": "T", "B": "F"},
                {"A": "F", "B": "T"},
            ],
        },
        {
            "id": "reversed-conditionals",
            "left": "A → B",
            "right": "B → A",
            "expected_equivalent": False,
            "expected_separating_valuations": [
                {"A": "T", "B": "F"},
                {"A": "F", "B": "T"},
            ],
        },
        {
            "id": "biconditional-expansion",
            "left": "A ↔ B",
            "right": "(A → B) ∧ (B → A)",
            "expected_equivalent": True,
            "expected_separating_valuations": [],
        },
        {
            "id": "union-atom-space-separator",
            "left": "A",
            "right": "A ∨ B",
            "expected_equivalent": False,
            "expected_separating_valuations": [
                {"A": "F", "B": "T"},
            ],
        },
    ]
    lesson["satisfiability_checks"] = [
        {
            "id": "direct-incompatibility",
            "formulas": ["A", "¬A"],
            "expected_jointly_satisfiable": False,
            "expected_satisfying_valuations": [],
        },
        {
            "id": "disjunction-with-negated-member",
            "formulas": ["A ∨ B", "¬A"],
            "expected_jointly_satisfiable": True,
            "expected_satisfying_valuations": [
                {"A": "F", "B": "T"},
            ],
        },
        {
            "id": "modus-ponens-incompatibility",
            "formulas": ["A → B", "A", "¬B"],
            "expected_jointly_satisfiable": False,
            "expected_satisfying_valuations": [],
        },
        {
            "id": "shared-consequent-set",
            "formulas": ["A ∨ B", "A → C", "B → C"],
            "expected_jointly_satisfiable": True,
            "expected_satisfying_valuations": [
                {"A": "T", "B": "T", "C": "T"},
                {"A": "T", "B": "F", "C": "T"},
                {"A": "F", "B": "T", "C": "T"},
            ],
        },
        {
            "id": "two-positive-atoms",
            "formulas": ["A", "B"],
            "expected_jointly_satisfiable": True,
            "expected_satisfying_valuations": [
                {"A": "T", "B": "T"},
            ],
        },
        {
            "id": "exhausted-disjunction",
            "formulas": ["A ∨ B", "¬A", "¬B"],
            "expected_jointly_satisfiable": False,
            "expected_satisfying_valuations": [],
        },
        {
            "id": "biconditional-with-positive-atom",
            "formulas": ["A ↔ B", "A"],
            "expected_jointly_satisfiable": True,
            "expected_satisfying_valuations": [
                {"A": "T", "B": "T"},
            ],
        },
        {
            "id": "conditional-with-negated-consequent",
            "formulas": ["A → B", "¬B"],
            "expected_jointly_satisfiable": True,
            "expected_satisfying_valuations": [
                {"A": "F", "B": "F"},
            ],
        },
    ]
    return lesson


def _candidate_c18():
    lesson = _lesson(
        "C18",
        "ders-gecerlilik-ve-karsi-degerleme",
        "Geçerlilik ve Karşı Değerleme",
        "Bir TFL argümanını bütün öncüllerin doğru ve sonucun yanlış olduğu bir değerleme bulunup bulunmamasına göre sınar; semantik sonuç işaretini TFL bağlaçlarından ayırır.",
        "Semantik sonuç, kötü satır ve karşı değerleme",
        45,
        [
            "ders-3-gecerlilik-ve-dogruluk",
            "ders-9-karsi-ornek-sema-ve-curutme-teknikleri",
            "ders-kullanim-anma-ve-dil-duzeyleri",
            "ders-mantiksal-esdegerlik-ve-tutarlilik",
        ],
        [
            "tfl.entailment_test",
            "tfl.validity_decide",
            "tfl.countervaluation_construct",
            "metalanguage.turnstile_distinguish",
        ],
        [
            "Semantik sonucu, öncüllerin hepsini doğru ve sonucu yanlış yapan hiçbir değerleme bulunmamasıyla tanımlamak.",
            "Tam tabloda yalnız bütün öncüllerin T ve sonucun F olduğu kötü satırları sistematik olarak aramak.",
            "Geçersizliği atom atamalarıyla yazılmış tek bir karşı değerlemeyle göstermek.",
            "Geçerliliği tek iyi örnekle değil, bütün kötü satır adaylarının elenmesiyle gerekçelendirmek.",
            "→ ve ↔ TFL bağlaçlarını, ⊨ ve ⊭ üst dil işaretlerinden kullanım/anma düzeyinde ayırmak.",
        ],
        [
            (
                "Semantik sonuç",
                "Bütün öncülleri doğru yapan her değerlemenin sonucu da doğru yapması ilişkisi.",
            ),
            (
                "Semantik çift turnike",
                "⊨ işareti; soldaki cümlelerin sağdaki cümleyi semantik olarak gerektirdiğini bildiren üst dil işareti.",
            ),
            (
                "Semantik sonuç olmama",
                "⊭ işareti; soldaki cümleleri doğru, sağdaki cümleyi yanlış yapan en az bir değerleme bulunduğunu bildiren üst dil işareti.",
            ),
            (
                "Geçerli TFL argümanı",
                "Öncüllerini doğru ve sonucunu yanlış yapan hiçbir değerlemesi bulunmayan argüman.",
            ),
            (
                "Kötü satır",
                "Bütün öncül sütunlarının T ve sonuç sütununun F olduğu tablo satırı.",
            ),
            (
                "Karşı değerleme",
                "Geçersiz bir argümanda bütün öncülleri doğru, sonucu yanlış yapan açık atom ataması.",
            ),
            (
                "Öncül-doğru adayı",
                "Bütün öncüllerin T olduğu ve sonucun karşı değerleme açısından denetlenmesi gereken satır.",
            ),
        ],
        [
            _section(
                "Geçerlilik kötü satırın yokluğudur",
                "𝒜₁, ..., 𝒜ₙ ⊨ 𝒞, bütün öncülleri T ve sonucu F yapan hiçbir değerleme olmadığını söyler. Böyle bir satır varsa argüman geçersizdir.",
                "TFL'ye sembolleştirilmiş tümdengelimsel argümanın geçerliliğini tabloyla sınarken.",
                "kötü satır = bütün öncüller T + sonuç F",
                "Tablodaki her satır olası bir atom atamasıdır. Geçerlilik, öncüllerin hepsinin doğru olduğu satırlarda sonucun yanlış kalamamasıdır. Sonucun başka satırlarda yanlış olması tek başına sorun değildir.",
                "Sonuç sütununda herhangi bir F görünce veya herhangi bir öncül F olunca geçersizlik ilan etme. Üç koşul aynı satırda birleşmelidir.",
                [
                    (
                        "A→B, A ⊨ B",
                        "A→B ve A'nın birlikte T olduğu satırda B de T'dir; kötü satır yoktur.",
                    ),
                    (
                        "A→B, B ⊭ A",
                        "A=F, B=T bütün öncülleri T, sonucu F yapar.",
                    ),
                    (
                        "Sonuç F fakat bir öncül de F",
                        "Bu satır karşı değerleme değildir; bütün öncüller T koşulu sağlanmaz.",
                    ),
                ],
                (
                    "Her satırda önce bütün öncüllerin T olup olmadığını, yalnız sonra sonucun F olup olmadığını denetlemek.",
                    "Sonucu yanlış olan her satırı karşı değerleme saymak.",
                    "Geçerlilik, sonuç doğruluğunun öncül doğruluğuna koşullu korunmasıdır.",
                ),
            ),
            _section(
                "Karşı değerleme geçersizliği tek satırda kanıtlar",
                "Bütün öncülleri T, sonucu F yapan tek bir değerleme evrensel geçerlilik iddiasını çürütür. Atom atamaları ve hedef sütun değerleri açıkça yazılmalıdır.",
                "Geçersiz bir argüman için kısa, yeniden hesaplanabilir ve kesin bir tanık sunarken.",
                "v(öncül₁)=...=v(öncülₙ)=T; v(sonuç)=F",
                "Karşı değerleme doğal dilde yalnız ikna edici bir hikâye değil, TFL atomlarına tutarlı T/F atamasıdır. Bileşik öncüllerin değerleri bu atamadan gerçekten hesaplanmalıdır.",
                "Yalnız sonucu F yapıp öncüllerden birini de F bırakan satırı kullanma; formüllerin birlikte gerçekleştirilebilirliğini denetle.",
                [
                    (
                        "A→B, B ⊭ A; A=F, B=T",
                        "A→B T ve B T iken sonuç A F'dir.",
                    ),
                    (
                        "A∨B ⊭ A; A=F, B=T",
                        "Öncül T, sonuç F olduğu için tek satır geçersizliği gösterir.",
                    ),
                    (
                        "A→B, ¬A ⊭ ¬B; A=F, B=T",
                        "İki öncül T, sonuç ¬B F olur; bu değerce karşı durumdur.",
                    ),
                ],
                (
                    "Karşı değerlemeyi atom ataması, öncül değerleri ve sonuç değeriyle üç katmanlı raporlamak.",
                    "Sonucun F olduğu fakat öncül koşullarını sağlamayan bir satırı tanık göstermek.",
                    "Karşı değerleme, geçersizliği biçimsel olarak gerçekleştirilebilir tek bir durumla gösterir.",
                ),
            ),
            _section(
                "Geçerlilik için bütün kötü satır adayları elenir",
                "Geçerli bir argümanda tek iyi satır yeterli değildir. Önce bütün öncüllerin T olduğu aday satırlar bulunur; her birinde sonuç T ise karşı değerleme yoktur.",
                "Karşı değerleme bulunmadığında geçerlilik sonucunu eksiksiz gerekçelendirmek için.",
                "öncül-doğru satırları filtrele → her birinde sonuç T mi?",
                "Öncüllerden en az biri F olan satırlar geçerlilik açısından otomatik olarak kötü satır değildir. Kritik küme, bütün öncüllerin aynı anda T olduğu satırlardır. Bu kümedeki sonuç değerleri eksiksiz denetlenir.",
                "Bir satırda öncüller ve sonuç T diye argümanı geçerli sayma; başka bir öncül-doğru satırı sonucu F bırakabilir.",
                [
                    (
                        "A→B, A ⊨ B",
                        "Tek öncül-doğru adayı A=T, B=T'dir ve sonuç T'dir.",
                    ),
                    (
                        "A→B, B→C ⊨ A→C",
                        "İki öncülün birlikte T olduğu bütün satırlarda ana koşul da T kalır.",
                    ),
                    (
                        "A∨B, ¬A ⊨ B",
                        "Öncüllerin birlikte T olduğu A=F, B=T satırında sonuç T'dir; başka aday yoktur.",
                    ),
                ],
                (
                    "Bütün öncül-doğru satırlarını sayıp sonuç sütunlarını tek tek denetlemek.",
                    "Seçilmiş bir destekleyici örnekten evrensel geçerlilik sonucu çıkarmak.",
                    "Geçerlilik yokluk iddiasıdır: hiçbir kötü satırın kalmadığı gösterilmelidir.",
                ),
            ),
            _section(
                "İlgisiz satırlar ve birlikte doyurulamaz öncüller",
                "Bir öncülün F olduğu satır, sonuç F olsa bile karşı değerleme değildir. Öncüller hiçbir satırda birlikte T olamıyorsa kötü satır da oluşmaz ve argüman klasik semantikte geçerli çıkar.",
                "Tabloda çok sayıda F görünmesine rağmen hangi satırların geçerlilik testine gerçekten girdiğini açıklarken.",
                "bütün öncüller T değilse satır kötü satır olamaz",
                "{A, ¬A} gibi birlikte doyurulamaz öncüllerin ortak doğru satırı yoktur. Dolayısıyla bu öncüllerle herhangi bir sonucu yanlış bırakan karşı değerleme de yoktur. Bu, öncüllerin iyi veya doğru olduğunu değil ilişkinin geçerlilik koşulunu boş biçimde sağladığını gösterir.",
                "Birlikte doyurulamaz öncüllerden çıkan argümanı sağlam sanma. Geçerlilik ile öncüllerin fiili doğruluğu ve sağlamlık farklıdır.",
                [
                    (
                        "A, ¬A ⊨ B",
                        "A ile ¬A hiçbir satırda birlikte T olmadığı için karşı değerleme yoktur.",
                    ),
                    (
                        "A=F satırında A ⊨ B testi",
                        "Öncül F olduğu için B'nin değeri bu satırı karşı değerleme yapamaz.",
                    ),
                    (
                        "Geçerli ama sağlam olmayan argüman",
                        "Geçerlilik yapıyı; sağlamlık ayrıca öncüllerin doğruluğunu gerektirir.",
                    ),
                ],
                (
                    "Satırları öncül-doğru filtresiyle ayırmak ve geçerliliği sağlamlıkla karıştırmamak.",
                    "Öncüller birlikte doğru olamıyorsa yöntemin bozulduğunu veya argümanın sağlam olduğunu sanmak.",
                    "Klasik semantik sonuç yalnız karşı değerleme varlığına bakar; öncül kabul edilebilirliği ayrı değerlendirmedir.",
                ),
            ),
            _section(
                "→ ve ↔ nesne dilinde, ⊨ ve ⊭ üst dilde",
                "A→B ve A↔B birer TFL cümlesidir; her değerlemede T veya F alır. A⊨B ve A⊭B ise cümleler arasındaki semantik ilişkiyi bildiren üst dil ifadeleridir.",
                "Formül kurma ile formüller hakkında semantik sonuç yazmayı birbirinden ayırırken.",
                "A→B: tek TFL cümlesi; A⊨B: iki cümle arasındaki üst dil ilişkisi",
                "Tek öncül durumunda A⊨B ile A→B'nin totoloji olması bağlantılıdır; fakat işaretler aynı sözdizimsel görevde değildir. A⊭B, en az bir karşı değerleme olduğunu söyler; buradan B'nin olumsuzunun her değerlemede doğru olduğu çıkmaz.",
                "⊨ işaretini parantez içinde ana bağlaç gibi hesaplama veya A⊭B sonucunu A⊨¬B diye güçlendirme.",
                [
                    (
                        "A→B",
                        "TFL formülüdür; ana bağlacı → ve her satırda doğruluk değeri vardır.",
                    ),
                    (
                        "A⊨B",
                        "A'yı doğru, B'yi yanlış yapan değerleme olmadığını söyleyen üst dil iddiasıdır.",
                    ),
                    (
                        "⊭A ve ⊭¬A",
                        "A olumsalsa ne A ne de ¬A öncülsüz semantik sonuçtur; birinin başarısızlığı diğerinin evrensel doğruluğunu vermez.",
                    ),
                ],
                (
                    "Her işaretin nesne dili bağlacı mı üst dil ilişki işareti mi olduğunu çözümden önce belirtmek.",
                    "→, ↔, ⊨ ve ⊭ işaretlerini aynı tür doğruluk işlevi gibi tablo sütununa koymak.",
                    "Dil düzeyi ayrımı, semantik ilişkiyi yeni bir TFL cümlesiyle karıştırmadan ifade etmeyi sağlar.",
                ),
            ),
        ],
        [
            _worked(
                "A→B, A ⊨ B",
                "Bütün öncülleri T ve B'yi F yapan satır yoktur.",
                "Geçerli",
            ),
            _worked(
                "A→B, B ⊭ A; A=F, B=T",
                "İki öncül T, sonuç F olduğu için değerleme karşı tanıktır.",
                "Karşı değerleme",
            ),
            _worked(
                "A∨B, ¬A ⊨ B",
                "Öncüllerin birlikte T olduğu tek satırda B de T'dir.",
                "Aday eleme",
            ),
            _worked(
                "A→B, ¬B ⊨ ¬A",
                "A=T, B=F koşulu ilk öncülü F yapar; kötü satır kurulamaz.",
                "Modus tollens",
            ),
            _worked(
                "A∨B ⊭ A; A=F, B=T",
                "Öncül T ve sonuç F olan tek satır geçersizliği gösterir.",
                "Tek tanık",
            ),
            _worked(
                "A, ¬A ⊨ B",
                "Öncüller hiçbir değerlemede birlikte T olmadığından karşı değerleme yoktur.",
                "Boş geçerlilik",
            ),
            _worked(
                "Bir satırda öncüller ve sonuç T; öyleyse argüman geçerlidir.",
                "Başka bir öncül-doğru satırı sonucu F bırakabilir; tek iyi satır yetmez.",
                "Eksik kanıt",
                "bad",
            ),
            _worked(
                "Sonuç F olan her satır karşı değerlemedir.",
                "Bütün öncüllerin de aynı satırda T olması gerekir.",
                "Kötü satır hatası",
                "bad",
            ),
            _worked(
                "A⊭B olduğundan A⊨¬B",
                "Bir karşı değerleme yalnız B'nin bir yerde F olduğunu gösterir; ¬B'nin bütün A-doğru satırlarda T olduğunu göstermez.",
                "İşaret hatası",
                "bad",
            ),
        ],
        [
            "Sonuç fiilen doğru olduğu için argümanı geçerli saymak.",
            "Bir öncülün F olduğu satırı geçersizlik kanıtı sanmak.",
            "Sonucu F olan her satırı, öncülleri denetlemeden karşı değerleme saymak.",
            "Öncüller ve sonuç T olan tek satırla geçerlilik kanıtlamak.",
            "Karşı değerlemede atom atamalarını veya bileşik öncül hesaplarını göstermemek.",
            "Birlikte doyurulamaz öncüllerden çıkan geçerli argümanı sağlam argüman sanmak.",
            "⊨ işaretini TFL formülünün hesaplanan ana bağlacı gibi kullanmak.",
            "A⊭B sonucunu otomatik olarak A⊨¬B biçiminde güçlendirmek.",
            "→ ile ⊨, ↔ ile eşdeğerlik iddiası arasındaki dil düzeyi farkını silmek.",
            "Geçersizliği doğal dil sezgisiyle söyleyip gerçekleştirilebilir TFL karşı değerlemesini denetlememek.",
        ],
        _practice(
            [
                (
                    "Bir karşı değerleme hangi koşulu sağlar?",
                    [
                        "Bütün öncüller T, sonuç F",
                        "Bütün öncüller F, sonuç T",
                        "En az bir öncül T, sonuç T",
                        "Yalnız sonuç F",
                    ],
                    "Bütün öncüller T, sonuç F",
                    "Geçersizlik için kötü satırın üç koşulu aynı değerlemede birleşir.",
                    "Temel",
                ),
                (
                    "Geçerli bir argümanda ne bulunmaz?",
                    ["Doğru sonuç", "Yanlış öncül", "Karşı değerleme", "Birden çok atom"],
                    "Karşı değerleme",
                    "Geçerlilik bütün öncülleri T, sonucu F yapan değerlemenin yokluğudur.",
                    "Temel",
                ),
                (
                    "A→B, B ⊭ A için karşı değerleme hangisidir?",
                    [
                        "A=T, B=T",
                        "A=T, B=F",
                        "A=F, B=T",
                        "A=F, B=F",
                    ],
                    "A=F, B=T",
                    "A→B ve B T, sonuç A F olur.",
                    "Orta",
                ),
                (
                    "Sonuç F fakat bir öncül de F olan satır için ne söylenir?",
                    [
                        "Kesin karşı değerlemedir",
                        "Bütün öncüller T olmadığı için karşı değerleme değildir",
                        "Argüman sağlamdır",
                        "Sonuç totolojidir",
                    ],
                    "Bütün öncüller T olmadığı için karşı değerleme değildir",
                    "Kötü satır bütün öncüllerin aynı anda T olmasını gerektirir.",
                    "Temel",
                ),
                (
                    "Geçerliliği göstermek için hangisi yeterlidir?",
                    [
                        "Bir iyi satır",
                        "Bir karşı değerleme",
                        "Bütün öncül-doğru satırlarda sonucun T olduğunu göstermek",
                        "Sonucun fiilen doğru olduğunu söylemek",
                    ],
                    "Bütün öncül-doğru satırlarda sonucun T olduğunu göstermek",
                    "Geçerlilik bütün kötü satır adaylarının elenmesini gerektirir.",
                    "Orta",
                ),
                (
                    "A∨B ⊭ A için hangi satır tanıktır?",
                    [
                        "A=T, B=T",
                        "A=T, B=F",
                        "A=F, B=T",
                        "A=F, B=F",
                    ],
                    "A=F, B=T",
                    "Öncül A∨B T, sonuç A F olur.",
                    "Orta",
                ),
                (
                    "A→B ile A⊨B arasındaki doğru ayrım hangisidir?",
                    [
                        "İkisi de TFL bağlacıdır",
                        "İlki TFL cümlesi, ikincisi üst dilde semantik ilişki iddiasıdır",
                        "İlki argüman, ikincisi atomdur",
                        "Aralarında fark yoktur",
                    ],
                    "İlki TFL cümlesi, ikincisi üst dilde semantik ilişki iddiasıdır",
                    "→ nesne dilinde bağlaç, ⊨ cümleler arasında üst dil işaretidir.",
                    "İleri",
                ),
                (
                    "A⊭B bilgisi tek başına hangisini vermez?",
                    [
                        "A'yı T, B'yi F yapan en az bir değerleme vardır",
                        "A⊨¬B",
                        "İlişki geçersizdir",
                        "Bir karşı değerleme vardır",
                    ],
                    "A⊨¬B",
                    "B'nin bir A-doğru satırında F olması, bütün A-doğru satırlarda F olmasını gerektirmez.",
                    "İleri",
                ),
                (
                    "A ve ¬A öncüllerinden B sonucu neden semantik olarak çıkar?",
                    [
                        "B her zaman doğrudur",
                        "Öncülleri birlikte T yapan satır olmadığından karşı değerleme yoktur",
                        "A bir totolojidir",
                        "¬A bir çelişkidir",
                    ],
                    "Öncülleri birlikte T yapan satır olmadığından karşı değerleme yoktur",
                    "Geçerlilik ölçütü kötü satırın yokluğudur; bu sağlamlık iddiası değildir.",
                    "İleri",
                ),
                (
                    "Bir satırda bütün öncüller T ve sonuç T ise bu satır nedir?",
                    [
                        "Karşı değerleme",
                        "Öncül-doğru fakat kötü olmayan satır",
                        "Geçersizlik kanıtı",
                        "Çelişki",
                    ],
                    "Öncül-doğru fakat kötü olmayan satır",
                    "Sonuç T olduğu için kötü satırın sonuç F koşulu sağlanmaz.",
                    "Temel",
                ),
                (
                    "Argüman tablosunda kötü satır bulunursa hangi ifade uygundur?",
                    [
                        "Öncüller sonucu semantik olarak gerektirir",
                        "Öncüller sonucu semantik olarak gerektirmez",
                        "Sonuç çelişkidir",
                        "Bütün öncüller yanlıştır",
                    ],
                    "Öncüller sonucu semantik olarak gerektirmez",
                    "Kötü satır, öncüllerin doğruluğunun sonucu zorunlu kılmadığını gösterir.",
                    "Orta",
                ),
                (
                    "Geçerlilik ile sağlamlık arasındaki fark hangisidir?",
                    [
                        "Geçerlilik yapısal doğruluk korumasıdır; sağlamlık ayrıca öncüllerin doğru olmasını ister",
                        "İkisi tamamen aynıdır",
                        "Sağlamlık yalnız sonucun doğru olmasıdır",
                        "Geçerlilik yalnız öncüllerin doğru olmasıdır",
                    ],
                    "Geçerlilik yapısal doğruluk korumasıdır; sağlamlık ayrıca öncüllerin doğru olmasını ister",
                    "Birlikte doyurulamaz öncüller geçerli ilişki oluşturabilir ama sağlam argüman oluşturmaz.",
                    "Zor",
                ),
            ]
        ),
        {
            "prompt": "Biri geçerli, biri geçersiz iki argüman tablosunu kötü satır ölçütüyle tamamla; işaretlerin dil düzeyini ayrıca açıkla.",
            "starter": "Argüman I: A→B, A / B\nArgüman II: A→B, B / A\nTablo sütunları: A | B | A→B | ikinci öncül | sonuç | kötü satır mı?",
            "checks": [
                "Her argüman için bütün öncül ve sonuç sütunları doğru hesaplanır",
                "Yalnız bütün öncüllerin T olduğu satırlar kötü satır adayı seçilir",
                "Argüman I için hiçbir kötü satır kalmadığı gösterilir",
                "Argüman II için A=F, B=T karşı değerlemesi açıkça yazılır",
                "Karşı değerlemede bütün öncüllerin T ve sonucun F olduğu doğrulanır",
                "→ işaretinin TFL bağlacı, ⊨ veya ⊭ işaretinin üst dil ilişkisi olduğu açıklanır",
            ],
            "solution": "Argüman I geçerlidir: A→B ve A'nın birlikte T olduğu A=T, B=T satırında B de T'dir; başka öncül-doğru aday yoktur. Bu nedenle A→B, A ⊨ B. Argüman II geçersizdir: A=F, B=T iken A→B T ve B T, sonuç A F'dir; bu karşı değerleme A→B, B ⊭ A sonucunu verir. → her satırda hesaplanan TFL bağlacıdır; ⊨ ve ⊭ ise tabloların tümü hakkında üst dilde ilişki bildirir.",
        },
        [
            _production_task(
                "Biri geçerli, biri geçersiz iki yeni TFL argümanı kur; ortak atom tablolarını, kötü satır denetimini ve dil düzeyi raporunu üret.",
                [
                    "Her argüman en az iki öncül ve bir sonuç içerir; bütün formüller iyi biçimlenmiştir.",
                    "Ortak atom uzayı ve bütün değerlemeler eksiksiz üretilir.",
                    "Her satırda bütün öncüllerin T olup olmadığı ayrı bir denetimle işaretlenir.",
                    "Geçersiz argüman için atom atamaları, öncül değerleri ve sonuç F değeri taşıyan karşı değerleme verilir.",
                    "Geçerli argüman için bütün öncül-doğru adaylarında sonucun T olduğu gösterilir.",
                    "Sonuçlar uygun biçimde ⊨ veya ⊭ kullanılarak üst dilde yazılır.",
                    "Her rapor → ya da ↔ bağlacı ile semantik ilişki işaretinin farklı görevini bir cümleyle açıklar.",
                ],
                "Geçersizlikte tek kesin tanığı, geçerlilikte ise tam kötü-satır yokluğu denetimini görünür kıl.",
                "Üretim koşulları",
                [
                    "Geçerli argüman: yalnız aynı cümleyi sonuçta tekrar etme",
                    "Geçersiz argüman: karşı değerleme en az iki atom içersin",
                    "Her tabloda 'bütün öncüller T mi?' kontrol sütunu kullan",
                    "İşaret raporunda nesne dili ve üst dil terimlerini yaz",
                ],
                "Denetim aileleri: A→B, A / B ve A→B, B / A yalnız örnektir; öğrenci farklı argümanlar kurmalıdır.",
            ),
        ],
        [
            "Bütün öncül ve sonuç sütunlarını ortak atom uzayında doğru hesaplar.",
            "Kötü satırı bütün öncüller T ve sonuç F nicelikleriyle doğru tanımlar.",
            "Geçersiz argüman için yeniden hesaplanabilir gerçek bir karşı değerleme gösterir.",
            "Geçerli argümanı tek iyi örnekle değil bütün öncül-doğru satırların elenmesiyle gerekçelendirir.",
            "Birlikte doyurulamaz öncüllerin geçerlilik ile sağlamlık üzerindeki farklı etkisini açıklar.",
            "→ ve ↔ nesne dili bağlaçlarını, ⊨ ve ⊭ üst dil ilişki işaretlerinden ayırır.",
        ],
        [
            "Bir karşı değerleme hangi sütunları hangi doğruluk değerlerinde bırakır?",
            "Bir öncül yanlışken sonuç da yanlışsa bu satır neden geçersizlik kanıtı değildir?",
            "A→B ile A⊨B neden aynı tür ifade değildir?",
            "A⊭B neden tek başına A⊨¬B sonucunu vermez?",
        ],
        "Sonraki derste iddianın kanıt yüküne göre tam, kısaltılmış tam veya tek satırlık kısmi tablo seçecek ve TFL sonucunu ifade sınırları içinde yorumlayacağız.",
        [
            "forallx-use-mention",
            "forallx-valuations",
            "forallx-logical-concepts",
            "mit-logic-sequence",
            "mit-logic-study-guide",
        ],
        "Bu ders klasik iki değerli TFL'de semantik sonuç ve argüman geçerliliğini ölçer. ⊨ ve ⊭ üst dil işaretleridir; kanıt sisteminin türetim işareti ve çıkarım kuralları D aşamasına bırakılır. Geçerlilik, sağlamlık ve öncüllerin kabul edilebilirliği birbirine indirgenmez.",
        ["ders-21-dogruluk-tablolari-ii-ve-gecerlilik"],
    )

    lesson["reading_note"] = (
        "Önce bütün öncüllerin T olduğu satırları filtrele. Yalnız bu satırlarda sonuç F ise karşı değerleme vardır; hiçbiri kalmıyorsa semantik sonuç ilişkisi geçerlidir."
    )
    lesson["symbol_set"] = [
        "A",
        "B",
        "C",
        "𝒜",
        "𝒞",
        "v",
        "T",
        "F",
        "¬",
        "∧",
        "∨",
        "→",
        "↔",
        "⊨",
        "⊭",
        "(",
        ")",
    ]
    lesson["proof_tools"] = [
        "Ortak atom envanteri",
        "Öncül-doğru satır filtresi",
        "Kötü satır denetimi",
        "Karşı değerleme raporu",
        "Bütün adayları eleme kaydı",
        "Geçerlilik/sağlamlık ayrımı",
        "Nesne dili/üst dil işaret denetimi",
    ]
    lesson["consequence_checks"] = [
        {
            "id": "modus-ponens",
            "premises": ["A → B", "A"],
            "conclusion": "B",
            "expected_entails": True,
            "expected_premise_true_count": 1,
            "expected_countervaluations": [],
        },
        {
            "id": "affirming-the-consequent",
            "premises": ["A → B", "B"],
            "conclusion": "A",
            "expected_entails": False,
            "expected_premise_true_count": 2,
            "expected_countervaluations": [
                {"A": "F", "B": "T"},
            ],
        },
        {
            "id": "disjunctive-syllogism",
            "premises": ["A ∨ B", "¬A"],
            "conclusion": "B",
            "expected_entails": True,
            "expected_premise_true_count": 1,
            "expected_countervaluations": [],
        },
        {
            "id": "conditional-converse",
            "premises": ["A → B"],
            "conclusion": "B → A",
            "expected_entails": False,
            "expected_premise_true_count": 3,
            "expected_countervaluations": [
                {"A": "F", "B": "T"},
            ],
        },
        {
            "id": "hypothetical-syllogism",
            "premises": ["A → B", "B → C"],
            "conclusion": "A → C",
            "expected_entails": True,
            "expected_premise_true_count": 4,
            "expected_countervaluations": [],
        },
        {
            "id": "disjunction-introduction",
            "premises": ["A"],
            "conclusion": "A ∨ B",
            "expected_entails": True,
            "expected_premise_true_count": 2,
            "expected_countervaluations": [],
        },
        {
            "id": "invalid-disjunction-elimination",
            "premises": ["A ∨ B"],
            "conclusion": "A",
            "expected_entails": False,
            "expected_premise_true_count": 3,
            "expected_countervaluations": [
                {"A": "F", "B": "T"},
            ],
        },
        {
            "id": "biconditional-elimination",
            "premises": ["A ↔ B", "A"],
            "conclusion": "B",
            "expected_entails": True,
            "expected_premise_true_count": 1,
            "expected_countervaluations": [],
        },
        {
            "id": "modus-tollens",
            "premises": ["A → B", "¬B"],
            "conclusion": "¬A",
            "expected_entails": True,
            "expected_premise_true_count": 1,
            "expected_countervaluations": [],
        },
        {
            "id": "denying-the-antecedent",
            "premises": ["A → B", "¬A"],
            "conclusion": "¬B",
            "expected_entails": False,
            "expected_premise_true_count": 2,
            "expected_countervaluations": [
                {"A": "F", "B": "T"},
            ],
        },
        {
            "id": "incompatible-premises",
            "premises": ["A", "¬A"],
            "conclusion": "B",
            "expected_entails": True,
            "expected_premise_true_count": 0,
            "expected_countervaluations": [],
        },
        {
            "id": "premise-free-tautology",
            "premises": [],
            "conclusion": "A ∨ ¬A",
            "expected_entails": True,
            "expected_premise_true_count": 2,
            "expected_countervaluations": [],
        },
    ]
    return lesson


def _candidate_c19():
    lesson = _lesson(
        "C19",
        "ders-kismi-tablolar-ve-tfl-sinirlari",
        "Kısmi Tablolar ve TFL'nin Sınırları",
        "Semantik iddianın kanıt yüküne göre tam, kısaltılmış tam veya hedefli kısmi tablo seçer; tablo sonucunu yalnız sembolleştirilen doğruluk işlevsel yapı içinde yorumlar.",
        "Yöntem seçimi, hedefli tanık ve ifade gücü sınırı",
        50,
        [
            "ders-belirsizlik-bulaniklik-savunulabilir-okumalar",
            "ders-kademeli-sembollestirme-atolyesi",
            "ders-gecerlilik-ve-karsi-degerleme",
        ],
        [
            "tfl.table_method_select",
            "tfl.partial_table_construct",
            "tfl.proof_burden_explain",
            "tfl.expressiveness_limit_diagnose",
        ],
        [
            "Tam tablo, kısaltılmış tam tablo ve tek tanıklık kısmi tabloyu satır kapsamına göre ayırmak.",
            "Evrensel ve varlık bildiren semantik iddialarda tek tanığın hangi yönde yeterli olduğunu belirlemek.",
            "Hedef T/F koşullarını atomik atamalardan başlayarak birlikte gerçekleştirilebilir tek bir değerlemede kurmak.",
            "Totoloji olmama, eşdeğer olmama, doyurulabilirlik ve geçersizlik için ekonomik fakat yeterli tanık üretmek.",
            "Sembolleştirme kaybını tablo hesap hatasından ayırmak ve TFL'nin ifade sınırlarını örneklerle teşhis etmek.",
            "Tablo sonucunu seçilen okuma ve sembol anahtarına bağlı, sınırlı bir semantik sonuç olarak raporlamak.",
        ],
        [
            (
                "Tam doğruluk tablosu",
                "İlgili atomlar üzerindeki bütün değerlemeleri ve gereken bütün hedef sütunları hesaplayan tablo.",
            ),
            (
                "Kısaltılmış tam tablo",
                "Bütün değerleme satırlarını koruyup sonuç açısından belirleyici olmayan bazı ara hücre hesaplarını gerekçeyle atlayan tam-kapsam yöntemi.",
            ),
            (
                "Kısmi doğruluk tablosu",
                "Belirli bir semantik iddia için gereken bir veya birkaç hedef değerlemeyi kuran, bütün satırları listelemeyen yöntem.",
            ),
            (
                "Kanıt yükü",
                "Bir iddianın doğruluğunu veya yanlışlığını göstermeye yetecek semantik kapsamın türü ve miktarı.",
            ),
            (
                "Evrensel iddia",
                "İlgili bütün değerlemeler hakkında bir koşul ileri süren ve olumlu kanıtı genel olarak tam kapsam gerektiren iddia.",
            ),
            (
                "Varlık iddiası",
                "Belirli koşulu sağlayan en az bir değerleme bulunduğunu söyleyen ve tek uygun tanıkla kanıtlanabilen iddia.",
            ),
            (
                "Hedef koşul",
                "Kısmi tabloda kurulması istenen formül ve doğruluk değeri birleşimi.",
            ),
            (
                "Sembolleştirme kaybı",
                "Doğal dilde bulunan fakat seçilen TFL atomları ve bağlaçları içinde temsil edilmeyen yapı veya anlam ilişkisi.",
            ),
            (
                "İfade gücü sınırı",
                "Bir biçimsel dilin kendi söz varlığı ve yapısıyla ayırt edemediği anlam farklarının oluşturduğu sınır.",
            ),
        ],
        [
            _section(
                "Kanıt yükü iddianın yönüne göre değişir",
                "Bir evrensel iddiayı doğrulamak bütün ilgili değerlemeleri, çürütmek ise tek karşı tanığı gerektirebilir. Bir varlık iddiasında bu asimetri ters yönde çalışır.",
                "Tablo kurmadan önce kaç satırın gerçekten yeterli olacağını belirlerken.",
                "evrensel evet → tam kapsam; evrensel hayır → tek karşı tanık; varlık evet → tek tanık; varlık hayır → tam kapsam",
                "'Totolojidir', 'eşdeğerdir' ve 'geçerlidir' bütün değerlemeler hakkında iddialardır. 'Doyurulabilirdir' en az bir ortak doğru değerleme ister. Sorunun evet/hayır yönü hangi kanıtın yeterli olduğunu değiştirir.",
                "Tek başarılı satırı evrensel iddianın kanıtı veya birkaç başarısız denemeyi varlık iddiasının çürütülmesi sanma.",
                [
                    (
                        "A→B totoloji değildir; A=T, B=F",
                        "Tek F tanığı bütün-satırlar T iddiasını çürütür.",
                    ),
                    (
                        "{A∨B, ¬A} doyurulabilirdir; A=F, B=T",
                        "Tek ortak doğru değerleme varlık iddiasını kanıtlar.",
                    ),
                    (
                        "A→B, A ⊨ B argümanı geçerlidir demek",
                        "Bütün kötü satır adaylarının yokluğu tam kapsamla gösterilmelidir.",
                    ),
                ],
                (
                    "Önce iddiayı evrensel veya varlık bildiren biçimde yeniden yazıp sonra kanıt yönünü seçmek.",
                    "Her semantik soru için otomatik olarak ya tam tablo ya tek satır kullanmak.",
                    "Yeterli yöntem, konu başlığından değil iddianın nicelik yapısı ve olumlu/olumsuz yönünden çıkar.",
                ),
            ),
            _section(
                "Kısaltılmış tam tablo bütün satırları korur",
                "Kısaltılmış tam tabloda hiçbir değerleme satırı atılmaz. Yalnız bir bağlacın sonucu belirlenmişse artık sonucu etkileyemeyecek ara hücreler gerekçeli olarak boş bırakılabilir.",
                "Evrensel iddia için tam değerleme kapsamını korurken gereksiz ara hesapları azaltmak için.",
                "satırlar tam; belirleyici hücreler hesaplı; atlanan hücreler gerekçeli",
                "Örneğin bir birleşimin bir tarafı F ise birleşim F'dir; öteki tarafın bazı ara hücreleri hedef sonuç için hesaplanmayabilir. Ancak atom ataması ve bu kısaltmayı haklı çıkaran belirleyici değer görünür kalır.",
                "Boş hücreyi bilinmeyen, önemsiz veya rastgele sanma. O hücre yalnız belirli hedef sütunun o satırdaki değerini değiştiremeyeceği kanıtlandığı için atlanır.",
                [
                    (
                        "(A∨B)∧(C↔D) satırında A∨B=F",
                        "Ana birleşim F olduğundan C↔D ara sütunu bu hedef için atlanabilir; atom değerleri ve satır yine tabloda kalır.",
                    ),
                    (
                        "(A∧B)∨(C→D) satırında A∧B=T",
                        "Ana ayrık birleşim T'dir; C→D ara sütunu hedefe etkisiz olduğu için gerekçeyle atlanabilir.",
                    ),
                    (
                        "(A↔B)→(C∨D) satırında A↔B=F",
                        "Ana maddi koşul T'dir; C∨D ara sütunu hedef koşul için hesaplanmayabilir.",
                    ),
                ],
                (
                    "Her boş hücre için hangi belirleyici bağlaç koşulunun sonucu sabitlediğini açıklamak.",
                    "İstenmeyen veya zor hücreleri gerekçesiz boş bırakıp yöntemi kısaltılmış tam tablo saymak.",
                    "Kısaltma hesap sayısını azaltır, değerleme uzayını veya kanıt yükünü azaltmaz.",
                ),
            ),
            _section(
                "Kısmi tablo hedeflenen tanığı kurar",
                "Kısmi tablo bütün değerlemeleri listelemek yerine istenen formül değerlerinden atomlara doğru koşullar çıkarır ve gerçekleştirilebilir bir tanık değerleme kurar.",
                "Tek bir yanlışlayıcı, ayırıcı, ortak doğru veya karşı değerleme iddiayı kanıtlamaya yettiğinde.",
                "hedef değer → bağlaç koşulları → alt cümle hedefleri → atom ataması → ileri doğrulama",
                "A→B'nin F olması hedeflenirse A=T ve B=F zorunludur. Daha karmaşık formüllerde dallanan olasılıklardan biri seçilir; seçilen atom ataması bütün hedef formüller ileri yönde yeniden hesaplanarak doğrulanır.",
                "Hedef hücreleri birbirinden bağımsız seçip aynı atomu hem T hem F yapma veya bağlaç koşullarının birlikte gerçekleştirilebilirliğini denetlemeden tanık ilan etme.",
                [
                    (
                        "A→B = F",
                        "Tek mümkün hedef atama A=T, B=F'dir.",
                    ),
                    (
                        "A∨B = T ve A = F",
                        "B=T seçilince iki hedef aynı değerlemede gerçekleşir.",
                    ),
                    (
                        "A→B = T, A = T, B = F",
                        "Koşullar birlikte gerçekleştirilemez; ilk hedef yeniden hesapta F çıkar.",
                    ),
                ],
                (
                    "Hedeften atomlara geri çöz, sonra atomlardan hedefe ileri hesapla ve aynı değerlemeyi koru.",
                    "Yalnız istenen T/F harflerini yazıp bunları üreten tutarlı atom atamasını göstermemek.",
                    "Kısmi tablo ekonomik olabilir; fakat tanığın semantik olarak gerçek olması tam hesap kadar sıkı denetlenir.",
                ),
            ),
            _section(
                "Beş temel soruda yöntem seçimi",
                "Totoloji, çelişki, eşdeğerlik, birlikte doyurulabilirlik ve geçerlilik sorularında evet ile hayır yönleri farklı kanıt yükleri taşır.",
                "Bir semantik soruya başlamadan önce yöntem gerekçesini kısa ve standart biçimde yazarken.",
                "totoloji/çelişki/eşdeğerlik/geçerlilik evet: tam kapsam; doyurulabilirlik evet: tanık",
                "Totoloji hayırı bir F satırı, çelişki hayırı bir T satırı, eşdeğerlik hayırı ayırıcı satır, doyurulabilirlik eveti ortak doğru satır ve geçerlilik hayırı karşı değerleme ile gösterilebilir. Ters yönler ilgili uzayın tamamını tüketir.",
                "Sorunun yalnız konu adını okuyup yönünü atlama. 'Geçerli mi?' sorusuna hayır cevabı ile evet cevabının aynı kanıt yükü yoktur.",
                [
                    (
                        "Eşdeğer değiller",
                        "İki sütunu farklı yapan tek ayırıcı değerleme yeterlidir.",
                    ),
                    (
                        "Küme birlikte doyurulamaz",
                        "Hiç ortak doğru değerleme kalmadığını tam veya kısaltılmış tam tabloyla göstermek gerekir.",
                    ),
                    (
                        "Argüman geçersiz",
                        "Bütün öncülleri T ve sonucu F yapan tek karşı değerleme yeterlidir.",
                    ),
                ],
                (
                    "Cevap yönünü yazıp seçilen yöntemin bu yöndeki kanıt yükünü nasıl karşıladığını belirtmek.",
                    "Yöntem adını yazıp neden yeterli olduğuna dair nicelik gerekçesi vermemek.",
                    "Yöntem seçimi bir hız tercihi değil, iddiayı gerçekten kanıtlayacak kapsam kararıdır.",
                ),
            ),
            _section(
                "Tablo hatası ile sembolleştirme kaybı farklıdır",
                "Doğru kurulmuş bir tablo, verilen TFL biçimi hakkında kesin sonuç verebilir; fakat doğal dildeki ilişki atomlaştırma sırasında kaybolmuşsa bu sonuç özgün argümanı eksik temsil eder.",
                "Tablo sonucu doğal dil sezgisiyle çatıştığında önce hesap mı, sembolleştirme mi sorunlu diye teşhis koyarken.",
                "doğal dil → açık okuma → sembol anahtarı → TFL formülü → doğru tablo → sınırlı yorum",
                "'Daisy'nin dört bacağı vardır; öyleyse ikiden fazla bacağı vardır' iki bağımsız atomla yazılırsa TFL aralarındaki sayısal içermeyi göremez. Tablo hesap hatası yapmaz; sembolleştirme ilişkiyi taşımamıştır.",
                "TFL'de geçersiz çıkan her doğal dil argümanını kötü argüman veya TFL'yi keyfi yöntem sayma. Önce korunan yapıyı denetle.",
                [
                    (
                        "D: Daisy'nin dört bacağı vardır; I: Daisy'nin ikiden fazla bacağı vardır",
                        "D ile I atomik bırakıldığında D⊨I çıkmaz; sayısal yapı temsil edilmemiştir.",
                    ),
                    (
                        "A: Ali uzundur",
                        "İki değerli atom, 'uzun' yükleminin bağlama ve dereceye bağlı bulanıklığını göstermez.",
                    ),
                    (
                        "A→B maddi koşulu",
                        "Nedensel, zamansal veya karşıolgusal doğal dil koşullarının bütün anlamını kodlamaz.",
                    ),
                ],
                (
                    "Tablonun hedef TFL biçimi için doğruluğunu kabul edip doğal dil sonucunu temsil kaybı kaydıyla sınırlandırmak.",
                    "Doğal dil bağlantısı kaybolduğunda tablo aritmetiğini değiştirerek sezgisel sonucu zorlamak.",
                    "Biçimsel kesinlik, yalnız biçimsel dilde açıkça temsil edilen ayrımlar üzerinde geçerlidir.",
                ),
            ),
            _section(
                "TFL'nin başlıca ifade sınırları",
                "TFL atomların iç yapısını, derece bulanıklığını, zorunluluk kipini, karşıolgusal yakınlığı, nedenselliği, zaman sırasını ve pragmatik vurguyu kendi bağlaçlarıyla çözümlemez.",
                "Bir doğal dil metninin TFL için uygun olup olmadığını ve hangi ek çözümleme aracına ihtiyaç duyduğunu değerlendirirken.",
                "sınırı adlandır → kaybolan bilgiyi göster → tablo sonucuna etkisini açıkla → daha zengin aracı belirt",
                "Her sınır TFL'nin yararsız olduğunu değil belirli bir amaç için tasarlandığını gösterir. İç yapı için yüklem ve niceleme, zorunluluk için kip, zaman için zamansal yapı gibi daha zengin araçlar gerekebilir; hangi aracın gerektiği kaybolan bilgi türüne bağlıdır.",
                "Her anlam farkı için gelişigüzel yeni atom eklemenin ilişkiyi koruduğunu sanma. Ayrı atomlar çoğu zaman bağımsız değerlenerek bağlantıyı daha da görünmez yapar.",
                [
                    (
                        "Eğer kibrit çakılsaydı yanardı.",
                        "Karşıolgusal yakınlık ve arka plan koşulları maddi koşulun T/F tablosunda temsil edilmez.",
                    ),
                    (
                        "Düğmeye bastı ve ışık yandı.",
                        "∧ birlikte doğruluğu verir; neden-sonuç ve önce-sonra sırasını vermez.",
                    ),
                    (
                        "Fakir ama dürüsttür.",
                        "Doğruluk koşulları birleşime benzese de 'ama' sözcüğünün karşıtlık vurgusu kaybolur.",
                    ),
                ],
                (
                    "Kaybolan anlam türünü somut cümle parçasıyla eşleyip TFL sonucunun kapsamını açıkça sınırlamak.",
                    "TFL'nin ifade etmediği ayrımı tablonun gizlice hesaba kattığını varsaymak.",
                    "Modelleme kalitesi, yalnız doğru hesap değil doğru temsil kapsamı ve açık sınırlılık raporu gerektirir.",
                ),
            ),
        ],
        [
            _worked(
                "A→B totoloji değildir: A=T, B=F",
                "Tek yanlışlayıcı değerleme evrensel totoloji iddiasını çürütür.",
                "Kısmi tanık",
            ),
            _worked(
                "A∨B çelişki değildir: A=T, B=F",
                "Tek T satırı bütün-satırlar F iddiasını çürütür.",
                "Doğru tanık",
            ),
            _worked(
                "A∨B ile A∧B eşdeğer değildir: A=T, B=F",
                "Aynı satırda ilk cümle T, ikincisi F olur.",
                "Ayırıcı tanık",
            ),
            _worked(
                "{A∨B, ¬A} doyurulabilirdir: A=F, B=T",
                "Tek ortak doğru değerleme varlık iddiasını kanıtlar.",
                "Ortak tanık",
            ),
            _worked(
                "A∨B ⊭ A: A=F, B=T",
                "Öncül T ve sonuç F olan tek karşı değerleme yeterlidir.",
                "Geçersizlik",
            ),
            _worked(
                "A∨¬A totolojidir çünkü A=T satırında T'dir.",
                "Tek iyi satır evrensel iddiaya yetmez; iki satırın tamamı gerekir.",
                "Kanıt yükü hatası",
                "bad",
            ),
            _worked(
                "Kısaltılmış tabloda dört satırdan üçünü silmek",
                "Satır silinirse yöntem artık tam kapsamlı değildir; yalnız ara hücreler gerekçeyle atlanabilir.",
                "Kısaltma hatası",
                "bad",
            ),
            _worked(
                "A→B=F hedefinden A=T, B=F çıkarma",
                "Maddi koşulun tek yanlış koşulu tanığı doğrudan belirler.",
                "Geri çözüm",
            ),
            _worked(
                "Daisy örneğinin TFL'de geçersiz çıkması",
                "Sayısal içerme atomlar arasında temsil edilmediği için sonuç doğal dil argümanını bütünüyle değerlendirmez.",
                "Temsil sınırı",
            ),
            _worked(
                "'Ama' bağlacını ∧ ile temsil etmek",
                "Doğruluk koşulu korunabilir; pragmatik karşıtlık vurgusu kaybolur ve raporlanmalıdır.",
                "Pragmatik kayıp",
            ),
        ],
        [
            "Tek başarılı satırla totoloji, eşdeğerlik veya geçerlilik kanıtlamak.",
            "Tek başarısız denemeyle birlikte doyurulabilirliğin yokluğunu kanıtladığını sanmak.",
            "Kısaltılmış tam tablo ile yalnız hedef satırları kuran kısmi tabloyu aynı yöntem saymak.",
            "Boş bırakılan ara hücre için sonucu sabitleyen bağlaç koşulunu açıklamamak.",
            "Kısmi tabloda hedef değerleri atomik atamalara kadar geri çözmemek.",
            "Aynı atomu farklı hedeflerde hem T hem F yaparak gerçekleştirilemez tanık kurmak.",
            "Karşı değerleme veya ortak tanığı ileri hesapla yeniden doğrulamamak.",
            "Tablo hesap hatası ile sembolleştirme kaybını aynı sorun saymak.",
            "TFL'nin geçersiz bulduğu her doğal dil argümanını kesin olarak kötü argüman ilan etmek.",
            "Nedensellik, zaman, zorunluluk veya pragmatik vurgunun TFL bağlaçlarında kendiliğinden korunduğunu varsaymak.",
        ],
        _practice(
            [
                (
                    "Bir cümlenin totoloji olmadığını göstermeye ne yeter?",
                    [
                        "Cümleyi F yapan tek değerleme",
                        "Cümleyi T yapan tek değerleme",
                        "Bir iyi örnek",
                        "Yalnız formülün uzunluğu",
                    ],
                    "Cümleyi F yapan tek değerleme",
                    "Tek karşı tanık her-satır T iddiasını çürütür.",
                    "Temel",
                ),
                (
                    "Bir cümlenin totoloji olduğunu göstermeye genel olarak ne gerekir?",
                    [
                        "Tek T satırı",
                        "Tam veya kısaltılmış tam tablo",
                        "Tek F satırı",
                        "Bir doğal dil örneği",
                    ],
                    "Tam veya kısaltılmış tam tablo",
                    "Olumlu evrensel iddia bütün ilgili değerlemeleri kapsamalıdır.",
                    "Temel",
                ),
                (
                    "Bir kümenin birlikte doyurulabilir olduğunu ne kanıtlar?",
                    [
                        "Bütün üyeleri aynı anda T yapan tek değerleme",
                        "Her üyeyi farklı satırda T yapmak",
                        "Bir başarısız satır",
                        "Bütün satırları silmek",
                    ],
                    "Bütün üyeleri aynı anda T yapan tek değerleme",
                    "Varlık iddiası ortak doğru tanıkla kanıtlanır.",
                    "Temel",
                ),
                (
                    "Bir kümenin birlikte doyurulamaz olduğunu göstermeye ne gerekir?",
                    [
                        "Tek ortak olmayan satır",
                        "Tam kapsamda hiçbir ortak doğru satır kalmadığını göstermek",
                        "Üyelerden birini yanlış yapmak",
                        "Bir ortak doğru tanık",
                    ],
                    "Tam kapsamda hiçbir ortak doğru satır kalmadığını göstermek",
                    "Yokluk iddiası bütün aday değerlemelerin elenmesini gerektirir.",
                    "Orta",
                ),
                (
                    "Kısaltılmış tam tabloda hangisi korunur?",
                    [
                        "Bütün değerleme satırları",
                        "Yalnız tek tanık satır",
                        "Hiçbir atom sütunu",
                        "Yalnız sonuç etiketi",
                    ],
                    "Bütün değerleme satırları",
                    "Kısaltma ara hesapları azaltır, değerleme kapsamını değil.",
                    "Temel",
                ),
                (
                    "Kısmi tablonun temel amacı nedir?",
                    [
                        "Her zaman bütün satırları listelemek",
                        "Belirli hedef koşulu gerçekleştiren tanık değerleme kurmak",
                        "Bağlaç kurallarını değiştirmek",
                        "Doğal dili eksiksiz çevirmek",
                    ],
                    "Belirli hedef koşulu gerçekleştiren tanık değerleme kurmak",
                    "Kısmi tablo iddianın gerektirdiği bir veya birkaç satırı hedefler.",
                    "Orta",
                ),
                (
                    "A→B formülünü F yapmak için hangi atama zorunludur?",
                    [
                        "A=T, B=F",
                        "A=F, B=T",
                        "A=T, B=T",
                        "A=F, B=F",
                    ],
                    "A=T, B=F",
                    "Maddi koşul yalnız doğru önbileşen ve yanlış artbileşende F olur.",
                    "Temel",
                ),
                (
                    "İki cümlenin eşdeğer olmadığını hangi yöntem ekonomik biçimde gösterir?",
                    [
                        "Farklı değer aldıkları tek ayırıcı satır",
                        "Tek aynı satır",
                        "Yalnız cümle uzunlukları",
                        "Bir ortak doğru satır",
                    ],
                    "Farklı değer aldıkları tek ayırıcı satır",
                    "Tek ayırıcı değerleme evrensel eşleşme iddiasını çürütür.",
                    "Orta",
                ),
                (
                    "Geçersizliği göstermeye ne yeter?",
                    [
                        "Öncülleri T, sonucu F yapan tek karşı değerleme",
                        "Öncülleri ve sonucu T yapan tek satır",
                        "Sonucu F yapan herhangi bir satır",
                        "Bir yanlış öncül",
                    ],
                    "Öncülleri T, sonucu F yapan tek karşı değerleme",
                    "Geçersizlik uygun tek kötü satırla kanıtlanabilen varlık iddiasıdır.",
                    "Orta",
                ),
                (
                    "Bir boş hücre kısaltılmış tabloda ne zaman meşrudur?",
                    [
                        "Hesap zor olduğunda",
                        "Belirleyici bağlaç değeri hedef sonucu zaten sabitlediğinde",
                        "Öğrenci değeri bilmediğinde",
                        "Satır fazla geldiğinde",
                    ],
                    "Belirleyici bağlaç değeri hedef sonucu zaten sabitlediğinde",
                    "Atlama hedef sonuç açısından semantik etkisizlik gerekçesine dayanmalıdır.",
                    "İleri",
                ),
                (
                    "Daisy'nin dört bacağı örneğinde TFL neden içermeyi göremez?",
                    [
                        "Tablo satır sayısı azdır",
                        "Sayısal iç yapı bağımsız atomlarda temsil edilmemiştir",
                        "∧ bağlacı yanlıştır",
                        "TFL'de F değeri yoktur",
                    ],
                    "Sayısal iç yapı bağımsız atomlarda temsil edilmemiştir",
                    "Sorun tablo hesabı değil sembolleştirme kaybıdır.",
                    "İleri",
                ),
                (
                    "'Düğmeye bastı ve ışık yandı' cümlesinde ∧ neyi korumaz?",
                    [
                        "İki bildirimin birlikte doğruluğunu",
                        "Nedensellik ve zaman sırasını",
                        "Her bildirimin bir atomla gösterilmesini",
                        "T/F değerlerini",
                    ],
                    "Nedensellik ve zaman sırasını",
                    "Birleşim birlikte doğruluğu verir; neden ve önce-sonra ilişkisini kodlamaz.",
                    "İleri",
                ),
                (
                    "'Fakir ama dürüsttür' ifadesinde ∧ ile hangi bilgi kaybolur?",
                    [
                        "İki tarafın doğruluk değerleri",
                        "Karşıtlık veya şaşırtıcılık vurgusu",
                        "Cümlenin iki parçası olduğu",
                        "Birleşimin doğruluk koşulu",
                    ],
                    "Karşıtlık veya şaşırtıcılık vurgusu",
                    "'Ama' çoğu bağlamda ∧ ile aynı doğruluk koşuluna sahip olsa da pragmatik vurgu taşır.",
                    "İleri",
                ),
                (
                    "Tablo doğru, doğal dil sonucu yetersiz görünüyorsa ilk ayrım ne olmalıdır?",
                    [
                        "Hesap hatası mı sembolleştirme kaybı mı?",
                        "Yazı tipi mi renk mi?",
                        "Atomlar kısa mı uzun mu?",
                        "Sonuç popüler mi?",
                    ],
                    "Hesap hatası mı sembolleştirme kaybı mı?",
                    "Doğru biçimsel hesap, eksik temsil edilmiş doğal dil ilişkisini geri getiremez.",
                    "Zor",
                ),
            ]
        ),
        {
            "prompt": "Beş semantik iddianın kanıt yükünü sınıflandır; ardından dört hedef için en ekonomik yeterli tanığı kur ve ileri hesapla doğrula.",
            "starter": "İddialar: totolojidir; çelişki değildir; eşdeğer değildir; küme doyurulabilirdir; argüman geçerlidir.\nHedefler: A→B=F; A∨B=T; A∨B ile A∧B farklı; A∨B öncülü T ve A sonucu F.",
            "checks": [
                "Her iddia evrensel veya varlık yönüyle sınıflandırılır",
                "Tam, kısaltılmış tam ve kısmi tablo birbirinden satır kapsamıyla ayrılır",
                "A→B=F hedefi A=T, B=F atamasına kadar geri çözülür",
                "Eşdeğer olmama için aynı değerlemede iki farklı sonuç gösterilir",
                "Geçersizlik için öncül T ve sonuç F aynı satırda doğrulanır",
                "Her kısmi tanık atomlardan hedef formüllere ileri yönde yeniden hesaplanır",
                "Tek satırın neden yeterli olduğu iddianın kanıt yüküyle açıklanır",
            ],
            "solution": "Totolojidir ve argüman geçerlidir iddiaları tam veya kısaltılmış tam kapsam ister. Çelişki değildir, eşdeğer değildir ve küme doyurulabilirdir iddiaları uygun tek tanıkla gösterilebilir. Kısmi hedefler hükümden atomlara geri çözülür: A→B=F için A=T, B=F; A∨B=T için örneğin A=T, B=F; A∨B ile A∧B'yi ayırmak için A=T, B=F; A∨B ⊭ A için A=F, B=T seçilir. Her atama atomlardan hedefe ileri hesaplanarak yeniden doğrulanır.",
        },
        [
            _production_task(
                "Dört semantik iddia için en ekonomik yeterli yöntemi seçip uygula; ardından TFL'nin eksik temsil ettiği bir doğal dil argümanına sınır raporu yaz.",
                [
                    "Bir cümlenin totoloji olmadığı yanlışlayıcı tek değerlemeyle gösterilir.",
                    "İki cümlenin eşdeğer olmadığı ayırıcı tek değerlemeyle gösterilir.",
                    "Bir cümle kümesinin birlikte doyurulabilir olduğu ortak doğru tek değerlemeyle gösterilir.",
                    "Bir argümanın geçersiz olduğu gerçek bir karşı değerlemeyle gösterilir.",
                    "Her tanık hedef değerlerden atom atamalarına geri çözülür ve ileri hesapla doğrulanır.",
                    "Her yöntemin neden yeterli olduğu evrensel/varlık kanıt yüküyle açıklanır.",
                    "Doğal dil örneğinde kaybolan yapı, TFL tablosunun sonucu ve gereken daha zengin bilgi türü ayrı raporlanır.",
                ],
                "Ekonomik yöntemi yalnız kısa olduğu için değil, iddiayı mantıksal olarak kanıtlamaya yettiği için seç.",
                "Zorunlu dört tanık ve sınır raporu",
                [
                    "Totoloji değil: bir F değerleme",
                    "Eşdeğer değil: iki farklı sütun değeri",
                    "Doyurulabilir: bütün üyeler T",
                    "Geçersiz: bütün öncüller T, sonuç F",
                ],
                "Sınır raporu en az üç başlık taşımalıdır: kaybolan doğal dil ilişkisi, doğru TFL hesabı, sonucu değerlendirmek için gereken ek temsil veya alan bilgisi.",
            ),
        ],
        [
            "Yöntem seçimini iddianın evrensel veya varlık bildiren kanıt yüküyle gerekçelendirir.",
            "Tam, kısaltılmış tam ve kısmi tabloyu değerleme satırı kapsamına göre doğru ayırır.",
            "Her kısmi tanığı atomik atamalardan hedef ana sütunlara kadar tutarlı biçimde kurar ve ileri doğrular.",
            "Tek tanığın yeterli olmadığı en az iki olumlu evrensel iddiayı doğru belirler.",
            "Sembolleştirme kaybı ile tablo hesap hatasını farklı teşhis ve düzeltme yollarıyla ayırır.",
            "TFL'nin iç yapı, bulanıklık, kip, nedensellik, zaman veya pragmatik vurgu sınırlarından en az üçünü doğru örneklerle açıklar.",
        ],
        [
            "Geçersizlik için tek karşı değerleme yeterliyken geçerlilik için tek iyi satır neden yetmez?",
            "Kısaltılmış tam tablo ile kısmi tablo arasındaki satır kapsamı farkı nedir?",
            "Bir hedef değerlemeyi kurduktan sonra neden ileri yönde yeniden hesaplamak gerekir?",
            "TFL'de geçersiz görünen doğal dil argümanı hangi temsil kaybı durumunda yine de iyi olabilir?",
        ],
        "Sonraki aşamada semantik sonuç ile biçimsel türetimi ayırarak doğal türetim kurallarına, satır gerekçelerine ve denetlenebilir kanıt yapılarına geçeceğiz.",
        [
            "forallx-truth-functionality",
            "forallx-logical-concepts",
            "forallx-expressiveness",
            "forallx-table-shortcuts",
            "forallx-partial-tables",
            "mit-logic-sequence",
            "mit-logic-study-guide",
        ],
        "Bu ders klasik iki değerli TFL semantiğinin yöntem seçimi ve ifade sınırlarıyla biter. Kısaltılmış tam tablo değerleme uzayını korur; kısmi tablo hedef tanık kurar. Doğal türetim ve kanıt kuralları sonraki aşamaya, niceleyici ve yüklem iç yapısı daha sonraki birinci derece mantık aşamasına bırakılır.",
        [
            "ders-20-dogruluk-tablolari-i",
            "ders-21-dogruluk-tablolari-ii-ve-gecerlilik",
        ],
    )

    lesson["reading_note"] = (
        "Önce iddianın evrensel mi varlık bildiren mi olduğunu ve cevabın yönünü yaz. Yöntemi buna göre seç; tek tanığı geri çöz ve ileri doğrula, tam-kapsam iddiasında bütün satırları koru."
    )
    lesson["symbol_set"] = [
        "A",
        "B",
        "C",
        "T",
        "F",
        "¬",
        "∧",
        "∨",
        "→",
        "↔",
        "⊨",
        "⊭",
        "(",
        ")",
    ]
    lesson["proof_tools"] = [
        "Kanıt yükü matrisi",
        "Tam tablo",
        "Kısaltılmış tam tablo",
        "Hedefli kısmi tablo",
        "Hedeften atomlara geri çözüm",
        "Atomlardan hedefe ileri doğrulama",
        "Sembolleştirme kaybı raporu",
    ]
    lesson["method_checks"] = [
        {
            "id": "tautology-yes",
            "question": "tautology",
            "answer": "yes",
            "expected_burden": "exhaustive",
            "acceptable_methods": ["complete", "shortened_complete"],
        },
        {
            "id": "tautology-no",
            "question": "tautology",
            "answer": "no",
            "expected_burden": "witness",
            "acceptable_methods": ["partial"],
        },
        {
            "id": "contradiction-yes",
            "question": "contradiction",
            "answer": "yes",
            "expected_burden": "exhaustive",
            "acceptable_methods": ["complete", "shortened_complete"],
        },
        {
            "id": "contradiction-no",
            "question": "contradiction",
            "answer": "no",
            "expected_burden": "witness",
            "acceptable_methods": ["partial"],
        },
        {
            "id": "equivalence-yes",
            "question": "equivalence",
            "answer": "yes",
            "expected_burden": "exhaustive",
            "acceptable_methods": ["complete", "shortened_complete"],
        },
        {
            "id": "equivalence-no",
            "question": "equivalence",
            "answer": "no",
            "expected_burden": "witness",
            "acceptable_methods": ["partial"],
        },
        {
            "id": "satisfiable-yes",
            "question": "joint_satisfiability",
            "answer": "yes",
            "expected_burden": "witness",
            "acceptable_methods": ["partial"],
        },
        {
            "id": "satisfiable-no",
            "question": "joint_satisfiability",
            "answer": "no",
            "expected_burden": "exhaustive",
            "acceptable_methods": ["complete", "shortened_complete"],
        },
        {
            "id": "validity-yes",
            "question": "validity",
            "answer": "yes",
            "expected_burden": "exhaustive",
            "acceptable_methods": ["complete", "shortened_complete"],
        },
        {
            "id": "validity-no",
            "question": "validity",
            "answer": "no",
            "expected_burden": "witness",
            "acceptable_methods": ["partial"],
        },
    ]
    lesson["partial_target_checks"] = [
        {
            "id": "conditional-false-witness",
            "requirements": [("A → B", "F")],
            "expected_matching_valuations": [
                {"A": "T", "B": "F"},
            ],
        },
        {
            "id": "disjunction-true-witnesses",
            "requirements": [("A ∨ B", "T")],
            "expected_matching_valuations": [
                {"A": "T", "B": "T"},
                {"A": "T", "B": "F"},
                {"A": "F", "B": "T"},
            ],
        },
        {
            "id": "shared-true-target",
            "requirements": [("A ∨ B", "T"), ("¬A", "T")],
            "expected_matching_valuations": [
                {"A": "F", "B": "T"},
            ],
        },
        {
            "id": "unrealizable-target",
            "requirements": [("A → B", "T"), ("A", "T"), ("B", "F")],
            "expected_matching_valuations": [],
        },
        {
            "id": "biconditional-separator-target",
            "requirements": [("A ↔ B", "F"), ("A", "T")],
            "expected_matching_valuations": [
                {"A": "T", "B": "F"},
            ],
        },
    ]
    lesson["witness_checks"] = [
        {
            "id": "not-equivalent-witness",
            "kind": "non_equivalence",
            "left": "A ∨ B",
            "right": "A ∧ B",
            "expected_witness": {"A": "T", "B": "F"},
        },
        {
            "id": "jointly-satisfiable-witness",
            "kind": "joint_satisfiability",
            "formulas": ["A ∨ B", "¬A"],
            "expected_witness": {"A": "F", "B": "T"},
        },
        {
            "id": "invalidity-witness",
            "kind": "countervaluation",
            "premises": ["A ∨ B"],
            "conclusion": "A",
            "expected_witness": {"A": "F", "B": "T"},
        },
    ]
    lesson["expressiveness_cases"] = [
        {
            "id": "internal-quantitative-structure",
            "category": "internal_structure",
            "example": "Daisy'nin dört bacağı vardır; öyleyse ikiden fazla bacağı vardır.",
            "loss": "Dört ile ikiden fazla arasındaki sayısal içerme bağımsız atomlarda görünmez.",
            "needed_information": "Nesnelerin özelliklerini ve sayısal ilişkileri çözümleyen daha zengin iç yapı.",
        },
        {
            "id": "vagueness",
            "category": "vagueness",
            "example": "Ali uzundur.",
            "loss": "Uzunluğun bağlama, karşılaştırma sınıfına ve dereceye bağlı sınırı T/F atomunda görünmez.",
            "needed_information": "Bağlam, ölçüt ve derece bilgisini taşıyan çözümleme.",
        },
        {
            "id": "necessity",
            "category": "modality",
            "example": "2+2=4 zorunlu olarak doğrudur.",
            "loss": "Atomik TFL biçimi fiili doğruluk ile zorunluluk kipini ayırmaz.",
            "needed_information": "Zorunluluk ve imkân kiplerini temsil eden daha zengin semantik.",
        },
        {
            "id": "counterfactual",
            "category": "counterfactual",
            "example": "Kibrit çakılsaydı yanardı.",
            "loss": "Maddi koşul karşıolgusal yakınlık ve arka plan koşullarını kodlamaz.",
            "needed_information": "Karşıolgusal senaryoları ve ilgili arka planı karşılaştıran semantik.",
        },
        {
            "id": "causation",
            "category": "causation",
            "example": "Düğmeye bastığı için ışık yandı.",
            "loss": "Birlikte doğruluk neden-sonuç yönünü göstermez.",
            "needed_information": "Nedensel mekanizma veya müdahale ilişkisi.",
        },
        {
            "id": "temporal-order",
            "category": "time",
            "example": "Düğmeye bastı ve sonra ışık yandı.",
            "loss": "Birleşim önce-sonra sırasını korumaz.",
            "needed_information": "Zamansal sıralama ve olay yapısı.",
        },
        {
            "id": "pragmatic-contrast",
            "category": "pragmatics",
            "example": "Fakirdir ama dürüsttür.",
            "loss": "∧ doğruluk koşulunu korusa da karşıtlık ve beklenti vurgusunu taşımaz.",
            "needed_information": "Söylem bağlamı, beklenti ve pragmatik vurgu.",
        },
    ]
    return lesson


STAGE_C_CANDIDATE_LESSONS = [
    _candidate_c14(),
    _candidate_c15(),
    _candidate_c16(),
    _candidate_c17(),
    _candidate_c18(),
    _candidate_c19(),
]

STAGE_C_CANDIDATE_MAP = {
    lesson["slug"]: lesson
    for lesson in STAGE_C_CANDIDATE_LESSONS
}
