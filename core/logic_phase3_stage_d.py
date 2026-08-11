"""Release-candidate content for Phase 3, Stage D of the logic course.

Stage D is developed one lesson at a time. Candidate lessons and structured
Fitch fixtures remain isolated from the learner-facing course until the full
stage passes the gates in ``docs/logic_phase3_stage_d_spec.md``.
"""

from .logic_phase3_stage_a import (
    _lesson,
    _practice,
    _production_task,
    _section,
    _worked,
)


STAGE_D_SOURCE_REFERENCES = {
    "forallx-natural-deduction": {
        "title": "forall x: Calgary - The idea of natural deduction",
        "url": "https://forallx.openlogicproject.org/html/Ch16.html",
    },
    "forallx-basic-rules": {
        "title": "forall x: Calgary - Basic rules for TFL",
        "url": "https://forallx.openlogicproject.org/html/Ch17.html",
    },
    "forallx-proof-strategies": {
        "title": "forall x: Calgary - Constructing proofs",
        "url": "https://forallx.openlogicproject.org/html/Ch18.html",
    },
    "carnap-derivations": {
        "title": "Carnap - Derivations and proof checking",
        "url": "https://carnap.io/srv/doc/derivations.md",
    },
    "carnap-feedback": {
        "title": "Carnap - Exercise feedback modes",
        "url": "https://carnap.io/srv/doc/faq.md",
    },
    "mit-logic-sequence": {
        "title": "MIT OpenCourseWare Logic I",
        "url": "https://ocw.mit.edu/courses/24-241-logic-i-fall-2009/",
    },
}


def _line(
    line_id,
    formula,
    rule,
    *,
    citations=None,
    depth=0,
    opens=None,
    closes=None,
):
    """Build one stable, machine-auditable Fitch line fixture."""

    return {
        "id": line_id,
        "formula": formula,
        "rule": rule,
        "citations": citations or [],
        "depth": depth,
        "opens": opens,
        "closes": closes or [],
    }


def _line_ref(line_id):
    return {"kind": "line", "id": line_id}


def _candidate_d20():
    lesson = _lesson(
        "D20",
        "ders-kanit-fikri-satir-bagimliligi-hedef-okuma",
        "Kanıt Fikri, Satır Bağımlılığı ve Hedef Okuma",
        "Bir Fitch türetimini doğru cümleler listesi olarak değil, her satırı erişilebilir kaynaklar ve açık varsayımlar tarafından lisanslanan bir yapı olarak okur.",
        "Kanıt anatomisi, kapsam ve satır lisansı",
        40,
        [
            "ders-9-karsi-ornek-sema-ve-curutme-teknikleri",
            "ders-kullanim-anma-ve-dil-duzeyleri",
            "ders-gecerlilik-ve-karsi-degerleme",
            "ders-kismi-tablolar-ve-tfl-sinirlari",
        ],
        [
            "nd.sequent_read",
            "nd.line_audit",
            "nd.scope_read",
            "nd.target_classify",
        ],
        [
            "Γ ⊢ 𝒞 yazımında öncül kümesini, hedefi ve türetim iddiasını birbirinden ayırmak.",
            "Bir Fitch satırında numara, formül, kural, atıf ve kapsam derinliğinin ayrı işlevlerini göstermek.",
            "Açık ve kapalı alt kanıtları ayırıp bir satırın mevcut konumdan erişilebilir olup olmadığını belirlemek.",
            "PR, AS ve R etiketlerini yalnız lisansladıkları satır türlerinde kullanmak.",
            "Hedefin ana bağlacından ileride gerekebilecek son kural ailesini tahmin etmek; henüz uygulanmayan kuralı kullanmamak.",
        ],
        [
            (
                "Türetim",
                "Öncül ve açık varsayımlardan, izin verilen kurallarla hedefe ulaşan sonlu ve satırları gerekçeli yapı.",
            ),
            (
                "Türetilebilirlik",
                "Γ ⊢ 𝒞 yazımıyla, açık varsayımları Γ içinde olan ve 𝒞 ile biten en az bir doğru türetim bulunduğu iddiası.",
            ),
            (
                "Kanıt satırı",
                "Formülün yanında onu lisanslayan kuralı, kaynak atıflarını ve kapsam konumunu taşıyan kayıt.",
            ),
            (
                "Öncül (PR)",
                "Kanıt probleminde başlangıç verisi olarak sunulan, başka satırdan çıkarılmayan cümle.",
            ),
            (
                "Varsayım (AS)",
                "Belirli bir alt kanıtı açan ve yalnız o açık kapsam ile onun iç kapsamlarında erişilebilir olan geçici cümle.",
            ),
            (
                "Yineleme (R)",
                "Erişilebilir önceki bir satırdaki formülü değiştirmeden mevcut konuma yeniden yazma kuralı.",
            ),
            (
                "Erişilebilirlik",
                "Bir önceki satırın mevcut kapsamda veya onu çevreleyen hâlâ açık bir kapsamda kaynak olarak kullanılabilmesi.",
            ),
            (
                "Hedef",
                "Kanıt probleminin kök kapsamda türetilmesi gereken son cümlesi.",
            ),
        ],
        [
            _section(
                "Doğruluk tablosundan türetime geçiş",
                "Doğruluk tablosu değerlemeleri tarar; doğal türetim ise sonuç formülüne hangi lisanslı adımlarla ulaşıldığını gösterir. Aynı geçerlilik ilişkisine farklı kanıt yükleriyle yaklaşırlar.",
                "Bir argümanın yalnız sonucunu değil, sonuç ile öncüller arasındaki biçimsel adım yapısını görünür kılmak istediğinde.",
                "Γ ⊢ 𝒞: Γ'dan 𝒞'ye doğru bir türetim vardır.",
                "`⊢` TFL cümlesinin içinde kullanılan yeni bir bağlaç değildir. Kanıt sistemi hakkında üst dilde konuşur; `⊨` ile aynı işaret veya aynı yöntem değildir.",
                "Bir örnekte hedefe ulaşılmasını bütün sistemin güvenirliğiyle veya öncüllerin gerçek dünyada doğru olmasıyla karıştırma.",
                [
                    (
                        "A, A → B ⊢ B",
                        "Sol taraf başlangıç verilerini, sağ taraf hedefi; turnike ise türetilebilirlik iddiasını gösterir.",
                    ),
                    (
                        "A, A → B ⊨ B",
                        "Bu kez hiçbir değerlemenin öncülleri doğru, sonucu yanlış yapmadığı semantik iddia edilir.",
                    ),
                    (
                        "Bir kanıt denemesi başarısız oldu.",
                        "Bu yalnız denemenin bitmediğini gösterir; türetimin hiç bulunmadığını kanıtlamaz.",
                    ),
                ],
                (
                    "`⊢` ile kanıt varlığı, `⊨` ile semantik sonuç iddiasını ayrı okumak.",
                    "İki işareti yalnız farklı yazım biçimleri sanmak.",
                    "Faz D sentaktik kural adımlarını, Faz C ise değerlemeler üzerindeki semantik ilişkiyi inceler.",
                ),
            ),
            _section(
                "Bir Fitch satırının beş parçası",
                "Her satır; kararlı kimlik/numara, TFL formülü, kural etiketi, kaynak atfı ve kapsam konumu taşır. Formül doğru görünse bile bu parçalardan biri bozuksa satır lisanssızdır.",
                "Hazır bir kanıtı denetlerken veya kendi kanıtında ilk hatalı satırı ararken.",
                "satır = kimlik + kapsam + formül + kural + atıf",
                "Satır numarası okuma sırasını, kararlı kimlik ise satır araya eklendiğinde atıfların bozulmamasını sağlar. Kural, kaynak formüllerin hedef formülü nasıl lisansladığını açıklar.",
                "Son formül hedefe eşit diye önceki gerekçe ve atıfları atlama; bir kanıt bütün satırlarının doğruluğunu ister.",
                [
                    (
                        "l1 · derinlik 0 · A · PR · atıf yok",
                        "A problemde verilen öncülse başlangıç satırı lisanslıdır.",
                    ),
                    (
                        "l3 · derinlik 1 · A · R · l1",
                        "l1 kök kapsamda olduğu için açık alt kanıtın içinde erişilebilirdir.",
                    ),
                    (
                        "l4 · derinlik 0 · B · R · l2",
                        "l2 kapanmış alt kanıtta kaldıysa formül aynı olsa bile atıf erişilemezdir.",
                    ),
                ],
                (
                    "Denetimi ilk satırdan başlayıp her lisansı sırayla doğrulamak.",
                    "Yalnız sonuca bakıp aradaki satırları dekorasyon saymak.",
                    "Sonraki satırın lisansı önceki satırların gerçekten kurulmuş ve erişilebilir olmasına bağlıdır.",
                ),
            ),
            _section(
                "Kapsam ve erişilebilirlik",
                "Alt kanıt geçici bir varsayımla açılır. İçerideki satırlar o varsayıma bağımlıdır; alt kanıt kapandığında iç satırlar dışarıdan tek tek kullanılamaz.",
                "Bir atfın yalnız önce gelmesini değil, mevcut satırdan erişilebilir olmasını sınarken.",
                "Kaynak kapsam yolu, mevcut kapsam yolunun başlangıcıysa satır erişilebilirdir.",
                "Kök satır açık bütün alt kanıtlarda; aynı açık kapsamın önceki satırı kendi devamında erişilebilir. Kapanmış çocuk veya kardeş kapsam satırı dışarıdan erişilebilir değildir.",
                "Alt kanıtın sayfada yukarıda görünmesini erişilebilirlik için yeterli sanma. Sıra koşulu ile kapsam koşulu birlikte gerekir.",
                [
                    (
                        "kök l1 → açık s1 içindeki l3",
                        "Kök kapsam s1'i çevrelediği için l1, l3'te erişilebilirdir.",
                    ),
                    (
                        "s1 içindeki l2 → s1 kapandıktan sonraki l4",
                        "l2 geçici varsayıma bağımlıdır ve doğrudan dışarı taşınamaz.",
                    ),
                    (
                        "s1 içindeki l3 → kardeş s2 içindeki l6",
                        "Kardeş alt kanıtlar birbirlerinin iç satırlarını kaynak alamaz.",
                    ),
                ],
                (
                    "Atıf için hem satır sırasını hem kapsam yolunu kontrol etmek.",
                    "Önce yazılmış her satırı erişilebilir saymak.",
                    "Fitch çizgileri görsel süs değil, varsayım bağımlılıklarının sınırıdır.",
                ),
            ),
            _section(
                "PR, AS ve R neyi lisanslar?",
                "PR yalnız verilen öncülü kaydeder; AS yeni bir geçici kapsam açar; R erişilebilir bir formülü değiştirmeden tekrarlar. Hiçbiri yeni bağlaç sonucu üretmez.",
                "Kanıtın başlangıç verisini, alt kanıt başlangıcını ve dışarıdan içeri taşınacak erişilebilir satırı birbirinden ayırırken.",
                "PR: öncül; AS: yeni kapsam; R: aynı formül + bir erişilebilir satır",
                "Kural etiketi formülün metinsel görünüşünden değil satırın kanıttaki işlevinden seçilir. Aynı A formülü farklı konumlarda PR, AS veya R olabilir.",
                "R ile eşdeğer, benzer veya sonucu çağrıştıran başka formüle geçme. Yineleme tam sözdizimsel özdeşlik ister.",
                [
                    (
                        "A problemde öncül, l1: A PR",
                        "Başka satır atfı gerekmez ve yazılmaz.",
                    ),
                    (
                        "l2: B AS, s1 açılır",
                        "B doğru kabul edilmiş kalıcı sonuç değil, yalnız s1 içindeki geçici varsayımdır.",
                    ),
                    (
                        "l3: A R l1",
                        "l1 erişilebilirse A değiştirilmeden yeniden yazılabilir.",
                    ),
                ],
                (
                    "Kuralı satırın kanıttaki rolüne göre seçmek.",
                    "Her hazır formülü PR veya her benzer formülü R ile yazmak.",
                    "PR problem verisine, AS kapsam açılışına, R ise belirli bir erişilebilir kaynağa bağlıdır.",
                ),
            ),
            _section(
                "Hedefin ana bağlacını okumak",
                "Hedefin ana bağlacı ileride hangi giriş kuralının son adım olmaya aday olduğunu gösterir. Bu, kanıtı tamamlamaz; yalnız aramayı yapılandırır.",
                "Kanıta rastgele satır eklemeden önce hedefi alt görevlere ayırmak için.",
                "Ana bağlaç ∧: olası ∧I; →: olası →I; ¬: olası ¬I; ∨: olası ∨I veya başka yol; ↔: olası ↔I",
                "D20'de bu kurallar henüz uygulanmaz. Öğrenci yalnız hedef biçimini sınıflandırır ve sonraki derslerde hangi kanıt yüklerinin açılacağını tahmin eder.",
                "Ana bağlaçtan tek zorunlu strateji çıktığını sanma. Özellikle ayrık ve atomik hedeflerde dolaylı yollar da mümkün olabilir.",
                [
                    (
                        "Hedef A → (B ∧ C)",
                        "Ana bağlaç → olduğundan olası son adım →I; bunun iç hedefi B ∧ C olur.",
                    ),
                    (
                        "Hedef ¬(A ∨ B)",
                        "Ana bağlaç ¬ olduğundan olası son adım ¬I; varsayım altında çelişki aranacaktır.",
                    ),
                    (
                        "Hedef A",
                        "Atomik hedef doğrudan bir giriş kuralı söylemez; erişilebilir verilerden ileri çalışma gerekebilir.",
                    ),
                ],
                (
                    "Ana bağlacı bir plan ipucu olarak kullanmak.",
                    "Hedef biçimini görmekle kanıtı tamamlanmış saymak.",
                    "Strateji kural doğruluğunu yönlendirir; onun yerine geçmez.",
                ),
            ),
        ],
        [
            _worked(
                "A, A → B ⊢ B",
                "Virgülün solu öncülleri, turnikenin sağı hedefi; bütün ifade türetim varlığı iddiasını gösterir.",
                "Kanıt problemi",
            ),
            _worked(
                "l1 · A · PR",
                "A başlangıçta verilen öncüllerden biriyse başka satıra atıf yapmadan yazılır.",
                "Lisanslı",
            ),
            _worked(
                "l2 · B · AS · s1 açılır",
                "B yalnız s1 kapsamı içinde geçici olarak kullanılabilir.",
                "Alt kanıt",
            ),
            _worked(
                "l3 · A · R l1 · s1 içinde",
                "Kök satır l1, onu çevreleyen açık s1 içinde erişilebilirdir.",
                "Lisanslı",
            ),
            _worked(
                "l4 · B · R l2 · s1 kapandıktan sonra",
                "l2 kapanmış alt kanıtta kaldığı için dışarıdan doğrudan kullanılamaz.",
                "Kapsam hatası",
                "bad",
            ),
            _worked(
                "Hedef A ↔ B",
                "Ana bağlaç ↔, ileride iki yönlü kanıt yükü doğuracak olası ↔I son adımını düşündürür.",
                "Plan ipucu",
            ),
        ],
        [
            "Son satır hedefe eşitse önceki satırları otomatik doğru saymak.",
            "Önce yazılmış her satırı kapsamdan bağımsız erişilebilir görmek.",
            "AS ile açılan cümleyi kanıtın kalıcı sonucu sanmak.",
            "R ile kaynak formülü değiştirmek veya eşdeğer bir formüle sessizce geçmek.",
            "`⊢` işaretini TFL'nin nesne dili bağlacı ya da `⊨`nin farklı yazımı sanmak.",
            "Başarısız bir kanıt denemesinden türetimin bulunmadığı sonucunu çıkarmak.",
        ],
        _practice(
            [
                (
                    "Γ ⊢ 𝒞 neyi ileri sürer?",
                    [
                        "Γ'daki bütün cümlelerin fiilen doğru olduğunu",
                        "Γ açık varsayımlarıyla 𝒞'ye ulaşan doğru bir türetim bulunduğunu",
                        "𝒞'nin her değerlemede yanlış olduğunu",
                        "⊢ işaretinin TFL bağlacı olduğunu",
                    ],
                    "Γ açık varsayımlarıyla 𝒞'ye ulaşan doğru bir türetim bulunduğunu",
                    "Turnike, uygun bir kanıt yapısının varlığını bildiren üst dil gösterimidir.",
                    "Temel",
                ),
                (
                    "Bir kanıt satırının lisansı için hangisi tek başına yeterli değildir?",
                    [
                        "Formülün hedefe benzemesi",
                        "Kuralın doğru eşleşmesi",
                        "Atıfların erişilebilir olması",
                        "Kapsam derinliğinin doğru olması",
                    ],
                    "Formülün hedefe benzemesi",
                    "Doğru görünen formül yanlış kural, atıf veya kapsamla lisanssız olabilir.",
                    "Temel",
                ),
                (
                    "PR satırı hangisini gerektirir?",
                    [
                        "Bir önceki satıra atıf",
                        "Formülün problemde verilen öncüllerden biri olması",
                        "Yeni alt kanıt açılması",
                        "Hedefin ana bağlacının → olması",
                    ],
                    "Formülün problemde verilen öncüllerden biri olması",
                    "PR başlangıç verisini kaydeder ve başka satıra dayanmaz.",
                    "Temel",
                ),
                (
                    "AS satırının özel işi nedir?",
                    [
                        "Bir değerleme kurmak",
                        "Yeni geçici kapsam açmak",
                        "Herhangi bir hedefi ispatlamak",
                        "Öncülü kalıcı olarak silmek",
                    ],
                    "Yeni geçici kapsam açmak",
                    "Varsayım yalnız açtığı alt kanıt ve onun açık iç kapsamlarında kullanılabilir.",
                    "Temel",
                ),
                (
                    "R hangi dönüşüme izin verir?",
                    [
                        "A'dan ¬¬A'ya",
                        "A ∧ B'den B ∧ A'ya",
                        "Erişilebilir A satırından yine A'ya",
                        "A'dan herhangi bir B'ye",
                    ],
                    "Erişilebilir A satırından yine A'ya",
                    "Yineleme kaynak formülü değiştirmez.",
                    "Orta",
                ),
                (
                    "Kök kapsamdaki l1 satırı açık s1 alt kanıtında kullanılabilir mi?",
                    ["Evet", "Hayır", "Yalnız hedef atomikse", "Yalnız l1 PR değilse"],
                    "Evet",
                    "Dıştaki açık kapsamın satırları iç kapsamda erişilebilirdir.",
                    "Orta",
                ),
                (
                    "s1 içindeki l2, s1 kapandıktan sonra kök kapsamda doğrudan kullanılabilir mi?",
                    ["Evet", "Hayır", "Yalnız R ile", "Yalnız formül doğruysa"],
                    "Hayır",
                    "Kapanan varsayıma bağımlı iç satır dışarıdan tek tek erişilebilir değildir.",
                    "Orta",
                ),
                (
                    "Hedef A → B ise ilk strateji ipucu nedir?",
                    [
                        "A'yı kalıcı öncül saymak",
                        "Olası son kural olarak →I'yi ve A varsayımı altında B hedefini düşünmek",
                        "Doğruluk tablosunu yasaklamak",
                        "Her durumda IP açmak",
                    ],
                    "Olası son kural olarak →I'yi ve A varsayımı altında B hedefini düşünmek",
                    "Ana bağlaç son kural ailesini düşündürür; kural D21'de uygulanacaktır.",
                    "Orta",
                ),
                (
                    "Hangi atıf kapsam bakımından geçersizdir?",
                    [
                        "Kök l1'den açık s1 içindeki l3'e",
                        "Aynı açık s1 içindeki l2'den sonraki l3'e",
                        "Kapanmış s1 içindeki l2'den kök l4'e",
                        "Kök l1'den sonraki kök l4'e",
                    ],
                    "Kapanmış s1 içindeki l2'den kök l4'e",
                    "Kaynak kapsam yolu mevcut kapsamın dış/üst yolu değildir.",
                    "İleri",
                ),
                (
                    "Bir hedef satır alt kanıtın içinde doğru biçimde yazılmışsa kanıt tamamlanmış mıdır?",
                    [
                        "Her zaman",
                        "Hayır; hedef kök kapsamda erişilebilir olmalı ve açık varsayım kalmamalı",
                        "Yalnız satır sonuncuysa",
                        "Yalnız formül atomikse",
                    ],
                    "Hayır; hedef kök kapsamda erişilebilir olmalı ve açık varsayım kalmamalı",
                    "Geçici varsayıma bağımlı hedef, problemde istenen koşulsuz sonuç değildir.",
                    "İleri",
                ),
            ]
        ),
        {
            "prompt": "Dört satırlık türetimde ilk lisanssız satırı bul ve yalnız o satırı düzelt.",
            "starter": "Önce her satırın kapsam yolunu çıkar; sonra kuralın istediği atıfların erişilebilirliğini denetle.",
            "checks": [
                "Her satırın kapsamı belirlendi",
                "Atıf satırdan önce geliyor",
                "Kaynak kapsam erişilebilir",
                "R formülü değiştirmiyor",
            ],
            "solution": "l4, kapanmış s1 içindeki l2'ye R ile atıf yapamaz. Hedef A ise erişilebilir kök l1, l4'te A R l1 olarak yinelenebilir.",
        },
        [
            _production_task(
                "Verilen Fitch türetimini satır bağımlılıklarıyla denetle; iki lisanssız satırı düzelt ve hedef biçimine göre bir sonraki ders için kanıt planı çıkar.",
                [
                    "Her satır için kimlik, formül, kural, atıf ve kapsam derinliğini ayrı yaz.",
                    "Her atfın hem önce gelme hem kapsam erişilebilirliği koşulunu denetle.",
                    "İlk bozuk satırdan sonra zincirleme oluşan hataları ayrı işaretle.",
                    "Hedefin ana bağlacını ve olası son kural ailesini gerekçelendir.",
                ],
                "Düzeltme yalnız doğru formülü yazmakla kalmamalı; neden önceki satırın erişilebilir ve kural şemasına uygun olduğunu göstermeli.",
                "Denetlenecek türetim",
                [
                    "l1 · 0 · A · PR",
                    "l2 · 1 · B · AS · s1 açılır",
                    "l3 · 1 · A · R l1",
                    "l4 · 0 · B · R l2 · s1 kapanır",
                    "Hedef: A → A",
                ],
                "l4'ün kapsam hatasını bul; hedefin ana bağlacından D21'de açılacak alt hedefi yaz.",
            )
        ],
        [
            "Sekiz satırlık bir türetimde her satırın lisansını doğru veya bozuk olarak sınıflandırır.",
            "Kapsam ihlalini hangi kaynak satırın neden erişilemez olduğunu belirterek açıklar.",
            "PR, AS ve R kurallarını kaynak, kapsam ve formül koşullarıyla doğru uygular.",
            "`⊢` ile `⊨` arasındaki yöntem farkını kendi kısa örneğinde doğru gösterir.",
            "Yeni bir hedef için olası son kural ailesini ana bağlaçtan gerekçelendirir.",
        ],
        [
            "Kapanmış bir alt kanıtın iç satırı neden doğrudan dışarı taşınamaz?",
            "Γ ⊢ 𝒞 neyin varlığını bildirir?",
            "Doğru formül hangi nedenlerle yine de lisanssız kanıt satırı olabilir?",
            "R neden semantik eşdeğerlik dönüşümü değildir?",
        ],
        "Sonraki derste ∧ ve → için giriş/eleme kurallarını kullanacak, koşul hedefinde alt kanıtı lisanslı biçimde kapatacağız.",
        [
            "forallx-natural-deduction",
            "forallx-basic-rules",
            "carnap-derivations",
            "carnap-feedback",
            "mit-logic-sequence",
        ],
        "D20 yalnız PR, AS ve R kurallarını etkinleştirir. Öğrenci henüz bağlaç kuralı uygulamaz; hedefin ana bağlacını yalnız sonraki kanıt yükünü öngören strateji ipucu olarak kullanır. Türetilebilirlik ile semantik sonuç ayrı tutulur.",
        [
            "ders-24-dogal-turetim-i",
            "ders-17-cikarim-kurallari-i",
        ],
    )

    lesson["reading_note"] = (
        "Kanıtı aşağıdan yukarı tahmin etme. Önce problemi öncüller ve hedef olarak ayır; sonra her satırda formül, kural, atıf ve kapsamı sırayla denetle."
    )
    lesson["symbol_set"] = [
        "Γ",
        "𝒜",
        "ℬ",
        "𝒞",
        "⊢",
        "⊨",
        "PR",
        "AS",
        "R",
        "∧",
        "∨",
        "→",
        "↔",
        "¬",
    ]
    lesson["proof_tools"] = [
        "Satır anatomisi tablosu",
        "Kapsam yolu",
        "Erişilebilirlik denetimi",
        "Kararlı satır kimliği",
        "Hedef ana bağlaç sınıflandırması",
        "İlk bozuk satır raporu",
    ]
    lesson["rule_scope"] = {
        "introduced": ["PR", "AS", "R"],
        "review_only": [],
        "locked_until_later": [
            "∧I",
            "∧E",
            "→I",
            "→E",
            "¬I",
            "¬E",
            "X",
            "IP",
            "∨I",
            "∨E",
            "↔I",
            "↔E",
            "DS",
            "MT",
            "DNE",
            "LEM",
            "DeM",
        ],
    }
    lesson["proof_fixtures"] = [
        {
            "id": "d20-complete-reiteration",
            "kind": "complete",
            "title": "Kök satırı alt kanıtta ve kapanıştan sonra yineleme",
            "expected_issue_codes": [],
            "proof": {
                "id": "d20-complete-reiteration",
                "premises": ["A"],
                "target": "A",
                "lines": [
                    _line("l1", "A", "PR"),
                    _line("l2", "B", "AS", depth=1, opens="s1"),
                    _line(
                        "l3",
                        "A",
                        "R",
                        citations=[_line_ref("l1")],
                        depth=1,
                    ),
                    _line(
                        "l4",
                        "A",
                        "R",
                        citations=[_line_ref("l1")],
                        closes=["s1"],
                    ),
                ],
            },
        },
        {
            "id": "d20-incomplete-conditional-plan",
            "kind": "incomplete",
            "title": "Koşul hedefi için henüz kapatılmamış iskelet",
            "expected_issue_codes": [],
            "next_rule": "→I · D21'de etkinleşecek",
            "proof": {
                "id": "d20-incomplete-conditional-plan",
                "premises": ["A"],
                "target": "B → A",
                "lines": [
                    _line("l1", "A", "PR"),
                    _line("l2", "B", "AS", depth=1, opens="s1"),
                    _line(
                        "l3",
                        "A",
                        "R",
                        citations=[_line_ref("l1")],
                        depth=1,
                    ),
                ],
            },
        },
        {
            "id": "d20-inaccessible-reiteration",
            "kind": "error",
            "title": "Kapanmış alt kanıttan lisanssız yineleme",
            "expected_issue_codes": ["citation.inaccessible"],
            "proof": {
                "id": "d20-inaccessible-reiteration",
                "premises": ["A"],
                "target": "B",
                "lines": [
                    _line("l1", "A", "PR"),
                    _line("l2", "B", "AS", depth=1, opens="s1"),
                    _line(
                        "l3",
                        "B",
                        "R",
                        citations=[_line_ref("l2")],
                        depth=1,
                    ),
                    _line(
                        "l4",
                        "B",
                        "R",
                        citations=[_line_ref("l2")],
                        closes=["s1"],
                    ),
                ],
            },
        },
    ]
    return lesson


STAGE_D_CANDIDATE_LESSONS = [_candidate_d20()]

STAGE_D_CANDIDATE_MAP = {
    lesson["slug"]: lesson
    for lesson in STAGE_D_CANDIDATE_LESSONS
}
