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


STAGE_C_CANDIDATE_LESSONS = [_candidate_c14(), _candidate_c15()]

STAGE_C_CANDIDATE_MAP = {
    lesson["slug"]: lesson
    for lesson in STAGE_C_CANDIDATE_LESSONS
}
