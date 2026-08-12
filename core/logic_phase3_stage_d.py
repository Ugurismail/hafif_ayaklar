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
    "forallx-additional-rules": {
        "title": "forall x: Calgary - Additional rules for TFL",
        "url": "https://forallx.openlogicproject.org/html/Ch19.html",
    },
    "forallx-derived-rules": {
        "title": "forall x: Calgary - Derived rules",
        "url": "https://forallx.openlogicproject.org/html/Ch21.html",
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


def _subproof_ref(start_id, end_id):
    return {"kind": "subproof", "start": start_id, "end": end_id}


def _strategy_case(
    case_id,
    problem,
    *,
    backward_goal,
    candidate_last_rules,
    forward_resources,
    bridge,
    scope_plan,
    first_action,
    rationale,
):
    """Build one inspectable proof-search plan without claiming an algorithm."""

    return {
        "id": case_id,
        "problem": problem,
        "backward_goal": backward_goal,
        "candidate_last_rules": candidate_last_rules,
        "forward_resources": forward_resources,
        "bridge": bridge,
        "scope_plan": scope_plan,
        "first_action": first_action,
        "rationale": rationale,
    }


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


def _candidate_d21():
    lesson = _lesson(
        "D21",
        "ders-birlesim-ve-kosul-kurallari",
        "Birleşim ve Koşul Kuralları",
        "Birleşim ve koşul için giriş/eleme kurallarını hedefin ana bağlacı, erişilebilir kaynakların biçimi ve alt kanıt sınırlarıyla eşleştirir.",
        "∧ ve → kurallarıyla ilk tamamlanmış türetimler",
        50,
        [
            "ders-kanit-fikri-satir-bagimliligi-hedef-okuma",
            "ders-18-degil-ve-ve-baglaclari",
            "ders-kosul-yalnizca-cift-yonluluk",
            "ders-degerlemeler-ve-dogruluk-islevleri",
        ],
        [
            "nd.conjunction_rules",
            "nd.conditional_eliminate",
            "nd.conditional_introduce",
            "nd.subproof_discharge",
        ],
        [
            "İki erişilebilir cümleden hedefteki sıraya uygun birleşim kurmak ve birleşimin iki doğrudan bileşenini ayrı ayrı çıkarmak.",
            "Bir koşul ile tam önbileşeninden artbileşeni üretmek; sonucu onaylama ve önbileşeni yadsıma biçimlerini reddetmek.",
            "Koşul hedefinde önbileşeni geçici varsayarak alt kanıt açmak, artbileşene ulaşmak ve varsayımı doğru aralıkla boşaltmak.",
            "Dış kapsamda erişilebilir satırları alt kanıt içinde kullanırken kapanmış iç satırları dışarı taşımamak.",
            "Hedeften geriye giriş kuralı, kaynaklardan ileri eleme kuralı seçimini bir ara hedefte birleştirmek.",
        ],
        [
            (
                "Birleşim girişi (∧I)",
                "Erişilebilir 𝒜 ve ℬ satırlarından, atıf sırasına uygun 𝒜 ∧ ℬ sonucunu kuran kural.",
            ),
            (
                "Birleşim eleme (∧E)",
                "𝒜 ∧ ℬ satırından doğrudan bileşenlerden 𝒜 veya ℬ'yi çıkaran kural.",
            ),
            (
                "Koşul eleme (→E)",
                "𝒜 → ℬ koşulu ile 𝒜 önbileşeninden ℬ artbileşenini çıkaran kural.",
            ),
            (
                "Koşul girişi (→I)",
                "𝒜 varsayımıyla açılan alt kanıt ℬ ile bittiğinde bu varsayımı boşaltıp 𝒜 → ℬ kuran kural.",
            ),
            (
                "Varsayım boşaltma",
                "Alt kanıttaki geçici varsayımı artık dış kapsamın açık varsayımları arasında bırakmadan, bütün alt kanıt aralığını bir giriş kuralında kullanma.",
            ),
            (
                "Önbileşen",
                "𝒜 → ℬ koşulunun sol tarafı; →E için ayrıca erişilebilir olması gereken cümle.",
            ),
            (
                "Artbileşen",
                "𝒜 → ℬ koşulunun sağ tarafı; →E'nin ürettiği ve →I alt kanıtının bitirmesi gereken cümle.",
            ),
        ],
        [
            _section(
                "Birleşim kurmak: ∧I",
                "∧I iki erişilebilir satırı tek birleşimde bir araya getirir. Sonuçtaki sol ve sağ bileşen, atıf yapılan kaynaklarla aynı sırada ve aynı sözdizimsel yapıda olmalıdır.",
                "Hedefin ana bağlacı ∧ olduğunda veya daha sonraki bir kural için iki sonucu tek cümlede toplamak gerektiğinde.",
                "𝒜, ℬ ⟹ 𝒜 ∧ ℬ · ∧I",
                "İki kaynağın aynı satırda yan yana görünmesi yetmez; ikisi de mevcut kapsamdan erişilebilir olmalıdır. Bileşen sırası doğruluk bakımından eşdeğer sonuç verebilse de kanıt satırının formülü açıkça lisanslanmalıdır.",
                "𝒜 ile ℬ'yi kullanıp gerekçe yazmadan ℬ ∧ 𝒜 üretme; hedefteki sıraya göre atıfları da sırala.",
                [
                    (
                        "l1: A; l2: B; l3: A ∧ B ∧I l1,l2",
                        "Sol ve sağ bileşen kaynaklarla sırayla eşleşir.",
                    ),
                    (
                        "l1: A; l2: B; l3: B ∧ A ∧I l2,l1",
                        "Ters sıralı hedef de mümkündür; atıf sırası buna göre değişir.",
                    ),
                    (
                        "l1 kökte A; l2 açık s1 içinde B",
                        "s1 içinde A ∧ B kurulabilir; s1 kapandıktan sonra B'ye doğrudan dayanarak kökte kurulamaz.",
                    ),
                ],
                (
                    "Hedef bileşenlerini kaynak satırlarla soldan sağa eşlemek.",
                    "Birleşimin değişme özelliğini sessiz yeniden yazma lisansı sanmak.",
                    "Bu sistemde her satır, semantik eşdeğerlikten bağımsız olarak uygulanan kuralın şemasına uymalıdır.",
                ),
            ),
            _section(
                "Birleşimi açmak: ∧E",
                "∧E, birleşimin yalnız doğrudan sol veya sağ bileşenini çıkarır. Daha derindeki alt formüle ulaşmak için kural birden fazla kez uygulanabilir.",
                "Erişilebilir bir birleşim içindeki bileşenlerden biri sonraki kuralın girdisi olduğunda.",
                "𝒜 ∧ ℬ ⟹ 𝒜 veya ℬ · ∧E",
                "A ∧ (B ∧ C) satırından tek adımda A veya B ∧ C çıkar. B ya da C için önce sağ bileşen, sonra o birleşimin ilgili bileşeni çıkarılmalıdır.",
                "Birleşimde yalnız içeride geçen herhangi bir formülü tek ∧E adımıyla çıkarma.",
                [
                    (
                        "A ∧ B ⟹ A",
                        "Sol doğrudan bileşen ∧E ile çıkarılır.",
                    ),
                    (
                        "A ∧ B ⟹ B",
                        "Sağ doğrudan bileşen de aynı kural ailesiyle çıkarılır.",
                    ),
                    (
                        "A ∧ (B ∧ C) ⟹ B ∧ C ⟹ C",
                        "İç içe yapı iki ayrı ∧E satırı gerektirir.",
                    ),
                ],
                (
                    "Önce kaynak birleşimin oluşum ağacındaki doğrudan çocukları belirlemek.",
                    "Parantezi görmezden gelip içerideki her atomu doğrudan seçmek.",
                    "Kural, metinde geçen sembollere değil ana bağlacın doğrudan bileşenlerine uygulanır.",
                ),
            ),
            _section(
                "Koşulu uygulamak: →E",
                "→E için bir koşul ve o koşulun tam önbileşeni gerekir. Bu ikisi sağlandığında yalnız artbileşen çıkar.",
                "Erişilebilir koşulun artbileşeni hedef veya yararlı bir ara hedef olduğunda.",
                "𝒜 → ℬ, 𝒜 ⟹ ℬ · →E",
                "Kaynak satırların kanıttaki sırası önemli değildir; denetleyici hangi satırın koşul, hangisinin onun önbileşeni olduğunu yapısal olarak bulur. Formül eşleşmesi tam olmalıdır.",
                "ℬ ile 𝒜 → ℬ'den 𝒜 çıkarma veya ¬𝒜 ile 𝒜 → ℬ'den ¬ℬ çıkarma; bunlar →E değildir.",
                [
                    (
                        "A → B, A ⟹ B",
                        "Koşul ve tam önbileşen artbileşeni lisanslar.",
                    ),
                    (
                        "A → (B ∧ C), A ⟹ B ∧ C",
                        "Önce bütün artbileşen çıkar; B veya C için ayrıca ∧E gerekir.",
                    ),
                    (
                        "(A ∧ B) → C, A",
                        "A, koşulun önbileşeni A ∧ B ile aynı değildir; →E henüz uygulanamaz.",
                    ),
                ],
                (
                    "Koşulun sol alt formülünü ikinci kaynakla tam eşlemek.",
                    "Doğal dilde makul görünen ters yönü →E saymak.",
                    "→E koşulun yazılı yönünü izler; ters veya karşıt-ters yön ayrı kanıt yükü ister.",
                ),
            ),
            _section(
                "Koşul kurmak: →I ve varsayım boşaltma",
                "→I, önbileşeni geçici varsayım olarak açar; alt kanıtın son doğrudan satırı artbileşen olduğunda bütün aralığı kullanıp koşulu dış kapsamda kurar.",
                "Hedefin ana bağlacı → olduğunda ve önbileşeni varsayarak artbileşene ulaşılabildiğinde.",
                "[𝒜 AS ... ℬ] ⟹ 𝒜 → ℬ · →I alt-kanıt-aralığı",
                "Sonuç 𝒜 → ℬ, 𝒜'nın dışarıda doğru kabul edildiğini söylemez. Tam tersine 𝒜 varsayımı boşaltılır; dış kapsamın diğer açık varsayımları koşulun bağımlılığı olarak kalabilir.",
                "Alt kanıtın başlangıcını, son satırını veya kapanışını yanlış göstermek; içeride herhangi bir yerde ℬ geçmesini yeterli saymak.",
                [
                    (
                        "A öncül; B AS; A R; sonuç B → A",
                        "B varsayımı altında A'ya ulaşıldığı için B → A kurulur ve B boşaltılır.",
                    ),
                    (
                        "A AS; B AS; A R; B → A; sonuç A → (B → A)",
                        "İç varsayım önce, dış varsayım sonra boşaltılır.",
                    ),
                    (
                        "A AS; C; B; sonuç A → B",
                        "B alt kanıtın son doğrudan satırıysa aradaki C satırı sorun değildir.",
                    ),
                ],
                (
                    "Başlangıç varsayımını ve son doğrudan satırı hedef koşulun iki tarafıyla eşlemek.",
                    "Alt kanıtta hedef bir kez göründü diye daha sonraki satırları yok sayarak aralığı kapatmak.",
                    "Atıf, gerçekten kapatılan alt kanıtın tam başlangıç ve sonunu göstermelidir.",
                ),
            ),
            _section(
                "İleri ve geri çalışmayı buluşturmak",
                "Giriş kuralları hedefi alt hedeflere, eleme kuralları mevcut satırları kullanılabilir parçalara açar. İlk kısa kanıtlar bu iki yönün bir ara hedefte buluşmasıyla kurulur.",
                "Birden fazla kural seçeneği varken rastgele satır üretmek yerine küçük bir kanıt planı yapmak için.",
                "hedefin ana bağlacı → geri → alt hedef; birleşim öncülü ileri ∧E → koşula girdi",
                "Örneğin C ∧ A hedefi iki alt hedef verir. C için A → (B → C), A ∧ B zinciri ileri açılır; A aynı birleşimden çıkarılır; son adım ∧I olur.",
                "Ulaşılabilir her formülü üretmek veya hedef koşul olduğu için içeride neye ulaşılacağını planlamadan AS açmak.",
                [
                    (
                        "A → (B → C), A ∧ B ⊢ C ∧ A",
                        "A ve B ∧E ile çıkar; iki →E C'yi, son ∧I hedefi üretir.",
                    ),
                    (
                        "A ∧ B ⊢ C → (A ∧ C)",
                        "C varsayılır, A öncülden çıkarılır, A ∧ C kurulur ve →I ile C boşaltılır.",
                    ),
                    (
                        "Hedef atomik C",
                        "Giriş kuralı ipucu yoktur; erişilebilir koşul zincirlerinden ileri çalışmak gerekir.",
                    ),
                ],
                (
                    "Son kuralı hedeften, ara girdileri kaynaklardan gerekçelendirmek.",
                    "Kuralları uygulanabilir oldukları için hedefsiz biçimde sıralamak.",
                    "İyi plan her satırın nihai hedefte hangi işi yaptığını görünür kılar.",
                ),
            ),
        ],
        [
            _worked(
                "A, B ⊢ A ∧ B",
                "İki öncül kök kapsamda erişilebilir; sonuç ∧I ile aynı sırada kurulur.",
                "∧I",
            ),
            _worked(
                "A ∧ (B ∧ C) ⊢ C",
                "Önce B ∧ C, sonra C olmak üzere iki ∧E gerekir.",
                "İki aşamalı ∧E",
            ),
            _worked(
                "A → B, A ⊢ B",
                "Koşul ve tam önbileşen →E ile artbileşeni lisanslar.",
                "→E",
            ),
            _worked(
                "A → B, B ⊢ A",
                "Artbileşenden önbileşene dönüş →E değildir; sonucu onaylama hatasıdır.",
                "Yön hatası",
                "bad",
            ),
            _worked(
                "A ⊢ B → A",
                "B varsayımı altında kök A yinelenir; alt kanıt kapatılıp B → A kurulur.",
                "→I",
            ),
            _worked(
                "A ∧ B ⊢ C → (A ∧ C)",
                "C varsayılır; A, öncülden ∧E ile çıkarılır; A ∧ C kurulup C varsayımı boşaltılır.",
                "Geri + ileri",
            ),
            _worked(
                "A AS ... B ... C; A → B →I",
                "B alt kanıtın son satırı değilse gösterilen aralık A'dan B'ye bitmez.",
                "Aralık hatası",
                "bad",
            ),
        ],
        [
            "∧I sonucundaki bileşen sırası ile atıf sırasını eşleştirmemek.",
            "∧E ile yalnız doğrudan bileşen yerine iç içe herhangi bir alt formülü tek adımda çıkarmak.",
            "→E'yi sonucu onaylama veya önbileşeni yadsıma yönünde kullanmak.",
            "→I alt kanıtında hedef artbileşenin son doğrudan satır olmasını denetlememek.",
            "→I sonrasında boşaltılan varsayımı dış kapsamda yeniden kullanmak.",
            "Kapanmış alt kanıt iç satırını bir sonraki kanıtta erişilebilir saymak.",
        ],
        _practice(
            [
                (
                    "A ve B erişilebilirse B ∧ A nasıl lisanslanır?",
                    ["∧I A,B", "∧I B,A", "∧E A", "R A"],
                    "∧I B,A",
                    "Sonucun sol bileşeni B, sağ bileşeni A olduğundan atıf sırası buna uyar.",
                    "Temel",
                ),
                (
                    "A ∧ (B ∧ C) satırından tek ∧E ile hangisi çıkabilir?",
                    ["B", "C", "B ∧ C", "A ∧ C"],
                    "B ∧ C",
                    "Tek adım yalnız doğrudan sol A veya sağ B ∧ C bileşenini çıkarır.",
                    "Temel",
                ),
                (
                    "A → B ile hangi ek satır →E için gerekir?",
                    ["B", "¬A", "A", "A ∧ B"],
                    "A",
                    "→E koşulun tam önbileşenini ister.",
                    "Temel",
                ),
                (
                    "A → B ve B'den A çıkarmak hangi hatadır?",
                    ["Geçerli →E", "Sonucu onaylama", "∧E", "Yineleme"],
                    "Sonucu onaylama",
                    "Koşul yalnız A'dan B yönünü lisanslar.",
                    "Temel",
                ),
                (
                    "Hedef A → B ise →I alt kanıtı hangi satırla açılır?",
                    ["B AS", "A AS", "A → B AS", "¬B AS"],
                    "A AS",
                    "Koşul girişinde önbileşen geçici varsayılır.",
                    "Orta",
                ),
                (
                    "A AS ile açılan alt kanıt C ile biterse →I ne kurabilir?",
                    ["C → A", "A → C", "A ∧ C", "¬A"],
                    "A → C",
                    "Başlangıç varsayımı önbileşen, son doğrudan satır artbileşendir.",
                    "Orta",
                ),
                (
                    "Dış kök satır A, B AS alt kanıtında kullanılabilir mi?",
                    ["Evet", "Hayır", "Yalnız ∧I ile", "Yalnız hedef A ise"],
                    "Evet",
                    "Kök kapsam açık alt kanıtı çevrelediği için erişilebilirdir.",
                    "Orta",
                ),
                (
                    "→I uygulandıktan sonra boşaltılan AS satırı ne olur?",
                    [
                        "Kök kapsamda öncül olur",
                        "Yalnız kapalı alt kanıtın bağımlılığı olarak kalır",
                        "Doğruluk değeri F olur",
                        "PR etiketi alır",
                    ],
                    "Yalnız kapalı alt kanıtın bağımlılığı olarak kalır",
                    "Koşul dışarı çıkar; geçici varsayım dışarıda kullanılabilir satır olmaz.",
                    "Orta",
                ),
                (
                    "(A ∧ B) → C ve A varken →E neden uygulanamaz?",
                    [
                        "C atomik olduğu için",
                        "A, tam önbileşen A ∧ B olmadığı için",
                        "Koşullar kullanılamadığı için",
                        "Önce →I gerektiği için",
                    ],
                    "A, tam önbileşen A ∧ B olmadığı için",
                    "Önce B ve ardından A ∧ B için ayrıca lisans gerekir.",
                    "İleri",
                ),
                (
                    "C ∧ A hedefinde en doğal son adım hangisidir?",
                    ["→E", "∧I", "∧E", "R"],
                    "∧I",
                    "Hedefin ana bağlacı ∧ olduğundan C ve A alt hedefleri ayrı kurulabilir.",
                    "İleri",
                ),
                (
                    "A AS, B, A satırlarıyla biten alt kanıttan A → B kurulabilir mi?",
                    [
                        "Evet, B bir yerde geçti",
                        "Hayır, alt kanıtın son doğrudan satırı A'dır",
                        "Yalnız A öncülse",
                        "Yalnız B atomikse",
                    ],
                    "Hayır, alt kanıtın son doğrudan satırı A'dır",
                    "→I aralığı varsayımdan son satıra kadar olan gerçek alt kanıtı kullanır.",
                    "İleri",
                ),
                (
                    "A → (B → C), A ∧ B ⊢ C için ilk yararlı ileri adım hangisidir?",
                    [
                        "C'yi AS yapmak",
                        "A ∧ B'den A ve B'yi ∧E ile çıkarmak",
                        "A → (B → C)'yi R ile C yapmak",
                        "Hedefe ∧I uygulamak",
                    ],
                    "A ∧ B'den A ve B'yi ∧E ile çıkarmak",
                    "Bu bileşenler koşul zincirindeki iki →E adımının girdileridir.",
                    "Zor",
                ),
            ]
        ),
        {
            "prompt": "A ∧ B ⊢ C → (A ∧ C) iskeletindeki boş kural ve atıfları doldur.",
            "starter": "Hedef koşul olduğu için önce C varsayımını aç; sonra A'yı dış öncülden içeri taşıyacak yolu bul.",
            "checks": [
                "C, AS ile yeni kapsam açtı",
                "A, A ∧ B'den ∧E ile çıkarıldı",
                "A ∧ C, ∧I ile doğru sırada kuruldu",
                "→I doğru alt kanıt aralığını kapattı",
            ],
            "solution": "l1 A ∧ B PR; l2 C AS; l3 A ∧E l1; l4 A ∧ C ∧I l3,l2; l5 C → (A ∧ C) →I l2-l4.",
        },
        [
            _production_task(
                "İki türetimi kur, satır bağımlılıklarını göster ve bir hatalı koşul kanıtını ilk bozuk satırdan onar.",
                [
                    "A → (B → C), A ∧ B ⊢ C ∧ A türetiminde dört yeni kuralı gerektiği yerde kullan.",
                    "A ∧ B ⊢ C → (A ∧ C) türetiminde AS ve →I aralığını açıkça göster.",
                    "Her satırın kararlı kimliğini, kuralını ve yapılandırılmış atfını yaz.",
                    "Sonucu onaylama içeren hatalı →E satırını neden lisanssız olduğunu belirterek düzelt.",
                ],
                "Kanıt planında son kuralı hedeften geriye, →E için gerekli önbileşenleri öncüllerden ileri çıkar.",
                "Türetim problemleri",
                [
                    "A → (B → C), A ∧ B ⊢ C ∧ A",
                    "A ∧ B ⊢ C → (A ∧ C)",
                    "Hata adayı: A → B, B ⊢ A · →E",
                ],
                "İkinci türetimde C varsayımının dış kapsamda açık kalmadığını ayrıca doğrula.",
            )
        ],
        [
            "∧I, ∧E, →I ve →E kurallarını en az bir kez doğru kullanan iki bağımsız türetim kurar.",
            "→I kapanışında doğru AS başlangıcını, son doğrudan satırı ve boşaltılan kapsamı gösterir.",
            "İç içe birleşimde doğrudan bileşen ile daha derin alt formülü ayırır.",
            "Sonucu onaylama, önbileşeni yadsıma ve kapsam dışı atıf hatalarını doğru kod ve gerekçeyle teşhis eder.",
            "Hedefin ana bağlacına göre son kuralı, kaynakların ana bağlacına göre yararlı ara adımları açıklar.",
        ],
        [
            "→I neden bir alt kanıt aralığı ister?",
            "𝒜 → ℬ ile ℬ hangi sonucu tek başına lisanslamaz?",
            "Dış kapsamdaki bir öncül alt kanıt içinde ne zaman kullanılabilir?",
            "A ∧ (B ∧ C) satırından C'ye kaç ∧E adımı gerekir?",
        ],
        "Sonraki derste çelişki işareti, olumsuzlama kuralları, patlama ve klasik dolaylı kanıt için alt kanıt disiplinini genişleteceğiz.",
        [
            "forallx-basic-rules",
            "forallx-proof-strategies",
            "carnap-derivations",
            "carnap-feedback",
        ],
        "D21 yalnız PR, AS, R ile ∧I, ∧E, →I ve →E kurallarını kullanır. Eşdeğerlik dönüşümleri, MT/DS gibi türetilmiş kurallar ve olumsuzlama stratejileri henüz kapalıdır. →I, yalnız kapalı ve erişilebilir alt kanıt aralığıyla lisanslanır.",
        [
            "ders-17-cikarim-kurallari-i",
            "ders-24-dogal-turetim-i",
        ],
    )

    lesson["reading_note"] = (
        "Hedef ∧ veya → ise geriye doğru son kuralı yaz. Sonra öncüllerdeki ∧ ve → yapılarını yalnız hedefte ihtiyaç duyulan ara cümleler için ileri aç."
    )
    lesson["symbol_set"] = [
        "𝒜",
        "ℬ",
        "𝒞",
        "∧",
        "→",
        "∧I",
        "∧E",
        "→I",
        "→E",
        "PR",
        "AS",
        "R",
        "⊢",
    ]
    lesson["proof_tools"] = [
        "Hedef ana bağlaç planı",
        "Doğrudan bileşen ağacı",
        "Önbileşen eşleştirme",
        "Alt kanıt aralığı atfı",
        "Varsayım boşaltma denetimi",
        "İleri/geri ara hedef köprüsü",
    ]
    lesson["rule_scope"] = {
        "introduced": ["∧I", "∧E", "→I", "→E"],
        "review_only": ["PR", "AS", "R"],
        "locked_until_later": [
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
            "id": "d21-complete-rule-chain",
            "kind": "complete",
            "title": "Birleşimi açıp koşul zincirini uygulama",
            "expected_issue_codes": [],
            "proof": {
                "id": "d21-complete-rule-chain",
                "premises": ["A → (B → C)", "A ∧ B"],
                "target": "C ∧ A",
                "lines": [
                    _line("l1", "A → (B → C)", "PR"),
                    _line("l2", "A ∧ B", "PR"),
                    _line(
                        "l3",
                        "A",
                        "∧E",
                        citations=[_line_ref("l2")],
                    ),
                    _line(
                        "l4",
                        "B",
                        "∧E",
                        citations=[_line_ref("l2")],
                    ),
                    _line(
                        "l5",
                        "B → C",
                        "→E",
                        citations=[_line_ref("l1"), _line_ref("l3")],
                    ),
                    _line(
                        "l6",
                        "C",
                        "→E",
                        citations=[_line_ref("l4"), _line_ref("l5")],
                    ),
                    _line(
                        "l7",
                        "C ∧ A",
                        "∧I",
                        citations=[_line_ref("l6"), _line_ref("l3")],
                    ),
                ],
            },
        },
        {
            "id": "d21-complete-conditional-introduction",
            "kind": "complete",
            "title": "Kök öncülü alt kanıtta yineleyip koşul kurma",
            "expected_issue_codes": [],
            "proof": {
                "id": "d21-complete-conditional-introduction",
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
                    _line(
                        "l4",
                        "B → A",
                        "→I",
                        citations=[_subproof_ref("l2", "l3")],
                        closes=["s1"],
                    ),
                ],
            },
        },
        {
            "id": "d21-incomplete-conditional",
            "kind": "incomplete",
            "title": "→I kapanışı henüz eklenmemiş doğru alt kanıt",
            "expected_issue_codes": [],
            "next_rule": "→I l2-l3",
            "proof": {
                "id": "d21-incomplete-conditional",
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
            "id": "d21-swapped-conditional-range",
            "kind": "error",
            "title": "→I sonucunun alt kanıt başlangıç ve sonuyla ters eşleşmesi",
            "expected_issue_codes": ["rule.conditional_introduction_mismatch"],
            "proof": {
                "id": "d21-swapped-conditional-range",
                "premises": ["A"],
                "target": "A → B",
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
                        "A → B",
                        "→I",
                        citations=[_subproof_ref("l2", "l3")],
                        closes=["s1"],
                    ),
                ],
            },
        },
    ]
    return lesson


def _candidate_d22():
    lesson = _lesson(
        "D22",
        "ders-olumsuzlama-alt-kanit-ve-celiskiye-indirgeme",
        "Olumsuzlama, Alt Kanıt ve Çelişkiye İndirgeme",
        "Açık bir cümle/olumsuzu çiftinden çelişki üretir; çelişkiyi olumsuzlama girişi, patlama ve klasik dolaylı kanıt içinde kapsamı bozmadan kullanır.",
        "¬, ⊥ ve varsayım boşaltma biçimlerini ayırma",
        55,
        [
            "ders-birlesim-ve-kosul-kurallari",
            "ders-totoloji-celiski-ve-olumsallik",
            "ders-mantiksal-esdegerlik-ve-tutarlilik",
        ],
        [
            "nd.contradiction_build",
            "nd.negation_rules",
            "nd.explosion_apply",
            "nd.indirect_proof",
        ],
        [
            "Erişilebilir 𝒜 ve ¬𝒜 satırlarını tam sözdizimsel eşleşmeyle belirleyip ¬E ile ⊥ üretmek.",
            "𝒜 varsayımından ⊥a ulaşan kapalı alt kanıtı ¬I ile boşaltıp ¬𝒜 kurmak.",
            "Erişilebilir ⊥ satırından X ile herhangi bir TFL cümlesini üretirken X'in yeni bir alt kanıt kapatmadığını göstermek.",
            "¬𝒜 varsayımından ⊥a ulaşan kapalı alt kanıtı klasik IP ile boşaltıp 𝒜 kurmak.",
            "¬I, ¬E, X ve IP kurallarını girdi, çıktı, atıf türü ve boşalttıkları varsayım bakımından ayırmak.",
        ],
        [
            (
                "Açık çelişki",
                "Aynı kapsamdan erişilebilen bir TFL cümlesi 𝒜 ile onun tam olumsuzu ¬𝒜'nın birlikte bulunması.",
            ),
            (
                "Çelişki işareti (⊥)",
                "Bir 𝒜/¬𝒜 çiftinin ¬E ile açıkça kaydedildiğini gösteren, kanıt satırlarında kullanılan özel işaret.",
            ),
            (
                "Olumsuzlama eleme (¬E)",
                "Erişilebilir 𝒜 ve ¬𝒜 satırlarından ⊥ üreten iki satırlı kural.",
            ),
            (
                "Olumsuzlama giriş (¬I)",
                "𝒜 varsayımı altında ⊥ türeten kapalı alt kanıttan ¬𝒜 çıkarıp 𝒜 varsayımını boşaltan kural.",
            ),
            (
                "Patlama (X)",
                "Erişilebilir ⊥ satırından istenen herhangi bir TFL cümlesini üreten, fakat tek başına alt kanıt kapatmayan kural.",
            ),
            (
                "Dolaylı kanıt (IP)",
                "¬𝒜 varsayımı altında ⊥ türeten kapalı alt kanıttan klasik olarak 𝒜 çıkaran kural.",
            ),
            (
                "Varsayım boşaltma",
                "Alt kanıt sonucunu dış kapsamda lisanslarken geçici başlangıç varsayımını artık doğrudan erişilebilir satır olmaktan çıkarma.",
            ),
        ],
        [
            _section(
                "Çelişkiyi biçimsel olarak tanımak",
                "Kanıt sisteminde iki cümlenin gerilimli görünmesi yetmez. ¬E için erişilebilir satırlardan biri tam olarak 𝒜, diğeri tam olarak ¬𝒜 olmalıdır; ancak o zaman ⊥ yazılır.",
                "Bir alt kanıtı çelişkiyle bitirmek veya patlama için kaynak hazırlamak gerektiğinde.",
                "𝒜, ¬𝒜 ⟹ ⊥ · ¬E",
                "Atıfların sırası sonucu değiştirmez. Buna karşılık A ile ¬B, A ile ¬(A ∧ B) veya yalnız iki farklı atom açık çelişki değildir.",
                "Semantik olarak birlikte yanlış olabilecek iki cümleyi, sözdizimsel 𝒜/¬𝒜 çifti göstermeden ¬E kaynağı saymak.",
                [
                    ("A; ¬A", "Tam olumlu/olumsuz çifti olduğu için ⊥ lisanslanır."),
                    ("A ∧ B; ¬(A ∧ B)", "Bileşik cümlenin bütünü ile tam olumsuzu çelişir."),
                    ("A; ¬B", "Atomlar farklı olduğu için ¬E uygulanamaz."),
                ],
                (
                    "Önce iki formülün sözdizim ağaçlarını tam eşleştir, sonra ⊥ yaz.",
                    "İki satır aynı anda doğru olamaz gibi göründüğü için doğrudan ⊥ yaz.",
                    "¬E yerel ve açık bir çelişki çiftini belgeleyen biçimsel bir kuraldır.",
                ),
            ),
            _section(
                "Olumsuzlama eleme ile ⊥ üretmek",
                "¬E iki erişilebilir satıra atıf yapar ve yalnız ⊥ sonucunu üretir. Çelişen satırlar bitişik olmak zorunda değildir; fakat ikisi de mevcut kapsamdan erişilebilir olmalıdır.",
                "Çelişkiyi bir sonraki ¬I, IP veya X adımında kullanılabilecek açık bir satıra dönüştürmek için.",
                "¬E m,n: m ve n satırları 𝒜/¬𝒜; sonuç ⊥",
                "Kapanmış bir kardeş alt kanıttaki 𝒜 ile mevcut kapsamdaki ¬𝒜 birlikte kullanılamaz. Erişilebilirlik, formül eşleşmesi kadar kuralın parçasıdır.",
                "¬E sonucuna hedef cümleyi yazmak veya yalnız bir olumsuz cümleye atıf yapmak.",
                [
                    ("l2 ¬B; l7 B; l8 ⊥ ¬E l2,l7", "Satırlar ayrı olsa da aynı kapsamdan erişilebilirdir."),
                    ("l2 B; l7 ¬B; l8 ⊥ ¬E l2,l7", "Ters atıf sırası da lisanslıdır."),
                    ("l2 ¬B; l7 B; l8 C ¬E l2,l7", "Sonuç ⊥ olmadığı için kural şemasını ihlal eder."),
                ],
                (
                    "Çelişki çiftini ve ⊥ sonucunu ayrı satırlarda görünür kıl.",
                    "Çelişen satırlardan istediğin hedefi doğrudan ¬E ile çıkar.",
                    "Önce ¬E ile ⊥, gerekiyorsa sonraki satırda X kullanılır.",
                ),
            ),
            _section(
                "¬I ile varsayımı boşaltmak",
                "Hedef ¬𝒜 ise 𝒜 geçici varsayılır. Bu varsayımın açık olduğu alt kanıtta ⊥ elde edilirse alt kanıt kapatılır ve dış kapsamda ¬𝒜 yazılır.",
                "Olumsuz hedefi doğrudan kuracak erişilebilir bir kural yokken, hedefin olumlusunun çelişkiye götürülebildiği durumda.",
                "[𝒜 AS ... ⊥] ⟹ ¬𝒜 · ¬I alt-kanıt-aralığı",
                "¬I atfı varsayım satırından alt kanıtın son doğrudan ⊥ satırına kadar uzanır. İçeride bir yerde ⊥ görülmesi, ardından başka satırlar yazıldıysa eski aralığı kapatmaya yetmez.",
                "¬𝒜'yı varsayıp yine ¬𝒜 sonucuna ulaşmak veya alt kanıt ⊥ yerine başka formülle biterken ¬I uygulamak.",
                [
                    ("A → B, A → ¬B ⊢ ¬A", "A varsayımı iki koşulla B ve ¬B üretir; ¬E sonrası ¬I A'yı boşaltır."),
                    ("A AS ... ⊥; sonuç ¬A", "Başlangıç ve sonuç ¬I şemasına tam uyar."),
                    ("¬A AS ... ⊥; sonuç ¬A", "Bu ¬I değil; aynı alt kanıt klasik IP ile A'yı lisanslayabilir."),
                ],
                (
                    "Olumsuz hedefin içindeki cümleyi varsay ve alt kanıtı tam ⊥ ile bitir.",
                    "Hedef olumsuz diye hedefin kendisini varsay.",
                    "¬I, varsayılan cümlenin yanlışlığını göstererek onun olumsuzunu dışarı çıkarır.",
                ),
            ),
            _section(
                "Patlamayı sınırlı ve açık kullanmak",
                "X, erişilebilir bir ⊥ satırından herhangi bir TFL cümlesini üretir. Gücü sınırsız görünen sonuç tarafındadır; kullanım koşulu ise son derece dardır: gerçek bir ⊥ satırı bulunmalıdır.",
                "Özellikle bir vaka veya alt kanıt dalı çelişkiye ulaştığında o dalda ortak hedefi üretmek gerektiğinde.",
                "⊥ ⟹ 𝒜 · X",
                "X bir alt kanıt aralığına değil tek ⊥ satırına atıf yapar. ⊥ kapanmış bir alt kanıtta kalmışsa dışarıdan erişilemez; önce onu boşaltan uygun kural gerekir.",
                "Birbirine uymayan iki öncülden doğrudan hedefe sıçramak veya kapanmış alt kanıtın ⊥ satırını dışarıda kullanmak.",
                [
                    ("A, ¬A ⊢ C", "Önce ⊥ ¬E, ardından C X kurulabilir."),
                    ("⊥ erişilebilir; hedef (A → B) ∧ C", "X'in sonucu atomik olmak zorunda değildir."),
                    ("A, ¬B ⊢ C · X", "Erişilebilir ⊥ bulunmadığı için patlama lisanssızdır."),
                ],
                (
                    "X atfını tek ve erişilebilir ⊥ satırına bağla.",
                    "Çelişki ihtimali gördüğün anda X yaz.",
                    "Patlama, çelişkinin kendisinden değil biçimsel olarak kurulmuş ⊥ satırından çalışır.",
                ),
            ),
            _section(
                "Klasik IP ile ¬I'yi ayırmak",
                "IP olumlu 𝒜 hedefi için ¬𝒜 varsayımını açar; alt kanıt ⊥ ile bittiğinde ¬𝒜 boşaltılır ve 𝒜 çıkar. ¬I ise 𝒜 varsayımını boşaltıp ¬𝒜 üretir.",
                "Doğrudan giriş/eleme planı sonuç vermediğinde ve hedefin olumsuzunun çelişkiye götürülebileceği klasik TFL kanıtlarında.",
                "[¬𝒜 AS ... ⊥] ⟹ 𝒜 · IP",
                "IP klasik bir ilkedir. Bu derste kullanılan sistemde lisanslıdır; fakat sezgici veya ilgili mantıklara otomatik olarak genellenmez. Doğrudan kısa yol varken gereksiz IP kanıtı okunurluğu azaltır.",
                "𝒜 varsayımından ⊥ elde edip IP ile 𝒜 yazmak ya da ¬𝒜 varsayımından ⊥ elde edip ¬¬𝒜 yazmak.",
                [
                    ("¬¬A ⊢ A", "¬A varsayılır; ¬¬A ile ¬E sonucu ⊥; IP ile A."),
                    ("A ⊢ ¬¬A", "¬A varsayımı altında ⊥ kurulur; sonuç ¬¬A için kullanılan kural ¬I'dir."),
                    ("Hedef B, varsayım ¬A", "Varsayım hedefin tam olumsuzu olmadığı için IP B'yi lisanslamaz."),
                ],
                (
                    "Önce hedef 𝒜'yı belirle, tam ¬𝒜 varsayımını aç ve son satırı ⊥ yap.",
                    "Her olumlu hedefte otomatik olarak herhangi bir olumsuz varsayım aç.",
                    "IP'nin lisansı hedef ile varsayım arasındaki tam olumsuzluk ve alt kanıtın ⊥ ile bitmesidir.",
                ),
            ),
            _section(
                "Dört kuralı kanıt planında ayırmak",
                "¬E çelişkiyi görünür yapar; ¬I ve IP farklı başlangıç varsayımlarını boşaltır; X ise mevcut ⊥ı hedef cümleye taşır. Aynı ⊥ satırı çevresinde görünseler de kanıt yükleri farklıdır.",
                "Hedef ve erişilebilir kaynaklara bakarak doğru kural ailesini seçmek, ilk hatalı satırı teşhis etmek için.",
                "¬E: iki satır→⊥; ¬I: alt kanıt→¬𝒜; IP: alt kanıt→𝒜; X: ⊥→herhangi 𝒜",
                "Hedef ¬ ile başlıyorsa ¬I güçlü bir geri plan ipucudur. Hedef olumluysa önce doğrudan kurallar aranır; IP ancak hedefin olumsuzundan çelişki planı varsa seçilir.",
                "Bütün çelişki temelli adımları 'çelişkiye indirgeme' adı altında aynı atıf ve kapsam biçimine sokmak.",
                [
                    ("Hedef ¬A; A varsayımı", "Plan ¬I yönündedir."),
                    ("Hedef A; ¬A varsayımı", "Plan klasik IP yönündedir."),
                    ("Erişilebilir ⊥; hedef C", "Tek satırlı X yeterlidir; yeni AS açılmaz."),
                ],
                (
                    "Kuralı hedef biçimi, kaynak türü ve boşaltılan varsayıma göre adlandır.",
                    "⊥ geçen her adımı aynı kural san.",
                    "Kural şemalarını ayırmak kapsam hatalarını ve yanlış hedef eşleşmelerini görünür kılar.",
                ),
            ),
        ],
        [
            _worked(
                "A, ¬A ⊢ ⊥",
                "Tam çelişki çifti iki erişilebilir satırdan ¬E ile açıklaştırılır.",
                "¬E",
            ),
            _worked(
                "A, ¬B ⊢ ⊥",
                "A ile ¬B aynı formülün olumlu/olumsuz biçimleri değildir.",
                "Sahte çelişki",
                "bad",
            ),
            _worked(
                "A → B, A → ¬B ⊢ ¬A",
                "A varsayımı B ve ¬B üretir; ⊥ ile biten alt kanıt ¬I tarafından boşaltılır.",
                "¬I",
            ),
            _worked(
                "A, ¬A ⊢ C",
                "¬E ile ⊥ kurulmadan X uygulanamaz; iki ayrı satır gerekir.",
                "¬E + X",
            ),
            _worked(
                "¬¬A ⊢ A",
                "¬A varsayımı ¬¬A ile çelişir; IP bu varsayımı boşaltıp A üretir.",
                "IP",
            ),
            _worked(
                "A ⊢ ¬¬A",
                "¬A varsayımı altında ⊥ elde edilir; sonuç varsayımın olumsuzu olduğu için ¬I kullanılır.",
                "¬I, IP değil",
            ),
            _worked(
                "[A AS ... ⊥ ... B] ⟹ ¬A · ¬I",
                "Alt kanıtın son doğrudan satırı B ise A'dan ⊥a biten eski aralık kapatılamaz.",
                "Aralık hatası",
                "bad",
            ),
            _worked(
                "Kapalı alt kanıttaki ⊥; dışarıda C X",
                "Kapanmış kapsamın iç satırı dışarıdan erişilemez; X kapsam duvarını aşmaz.",
                "Kapsam hatası",
                "bad",
            ),
        ],
        [
            "Aynı cümlenin tam olumsuzu yerine yalnız farklı görünen iki formülü çelişki saymak.",
            "¬E sonucuna ⊥ yerine hedef cümleyi yazmak.",
            "¬I için hedefin olumlusunu değil olumsuzunu varsaymak.",
            "IP için hedefin tam olumsuzu yerine ilgisiz bir olumsuz cümle varsaymak.",
            "X'i erişilebilir ⊥ olmadan veya kapalı alt kanıttaki ⊥a doğrudan atıfla kullanmak.",
            "Alt kanıt içindeki ⊥tan sonra başka satırlar ekleyip eski ⊥ satırını aralığın sonuymuş gibi göstermek.",
            "Doğrudan kısa bir kanıt varken her olumlu hedef için gereksiz IP açmak.",
        ],
        _practice(
            [
                (
                    "Hangi çift ¬E ile ⊥ üretir?",
                    ["A ve ¬A", "A ve ¬B", "A → B ve ¬B", "A ∧ B ve ¬A"],
                    "A ve ¬A",
                    "İkinci satır birincinin tam olumsuzudur.",
                    "Temel",
                ),
                (
                    "¬E satırının sonucu hangisidir?",
                    ["𝒜", "¬𝒜", "⊥", "Herhangi bir hedef"],
                    "⊥",
                    "Herhangi hedef için sonraki ayrı adım X'tir.",
                    "Temel",
                ),
                (
                    "Hedef ¬A ise ¬I alt kanıtı hangi varsayımla açılır?",
                    ["¬A", "A", "⊥", "B"],
                    "A",
                    "¬I hedefin içindeki olumlu cümleyi varsayar.",
                    "Temel",
                ),
                (
                    "Hedef A ise IP alt kanıtı hangi varsayımla açılır?",
                    ["A", "¬A", "¬¬A", "⊥"],
                    "¬A",
                    "IP hedefin tam olumsuzunu varsayar.",
                    "Temel",
                ),
                (
                    "X hangi tür atıf ister?",
                    ["Bir AS aralığı", "İki çelişen satır", "Tek erişilebilir ⊥ satırı", "Bir koşul"],
                    "Tek erişilebilir ⊥ satırı",
                    "X alt kanıt boşaltmaz; hazır ⊥ satırını kullanır.",
                    "Orta",
                ),
                (
                    "A ∧ B ile ¬(A ∧ B) neden çelişir?",
                    [
                        "İkisi de birleşim içerdiği için",
                        "İkincisi birincinin tam olumsuzu olduğu için",
                        "B olumsuz olduğu için",
                        "Her bileşik cümle çeliştiği için",
                    ],
                    "İkincisi birincinin tam olumsuzu olduğu için",
                    "Eşleşme bileşik formülün bütünü üzerinde yapılır.",
                    "Orta",
                ),
                (
                    "¬A AS ... ⊥ alt kanıtı hangi sonucu IP ile lisanslar?",
                    ["¬A", "¬¬A", "A", "⊥"],
                    "A",
                    "IP hedefin olumsuzunu boşaltarak hedefi üretir.",
                    "Orta",
                ),
                (
                    "¬A AS ... ⊥ alt kanıtı ¬I ile hangi sonucu lisanslar?",
                    ["A", "¬A", "¬¬A", "Herhangi B"],
                    "¬¬A",
                    "¬I varsayımın olumsuzunu üretir; burada varsayım ¬A'dır.",
                    "Orta",
                ),
                (
                    "Alt kanıtta l5 ⊥tan sonra l6 B yazıldı. ¬I aralığı l2-l5 olabilir mi?",
                    ["Evet", "Hayır, son doğrudan satır l6'dır", "Yalnız B atomikse", "Yalnız l5 erişilebilirse"],
                    "Hayır, son doğrudan satır l6'dır",
                    "Boşaltılan aralık alt kanıtın gerçek son satırında bitmelidir.",
                    "İleri",
                ),
                (
                    "Kapanmış s1 içindeki ⊥ dış kökte X kaynağı olabilir mi?",
                    ["Evet", "Hayır", "Yalnız hedef atomikse", "Yalnız IP sonrası"],
                    "Hayır",
                    "Kapanmış alt kanıtın tekil satırları dışarıdan erişilemez.",
                    "İleri",
                ),
                (
                    "A → B ve A → ¬B öncüllerinden ¬A için ilk geri plan nedir?",
                    [
                        "¬A'yı AS yapmak",
                        "A'yı AS yapıp B ve ¬B üretmek",
                        "Doğrudan X kullanmak",
                        "B'yi PR yazmak",
                    ],
                    "A'yı AS yapıp B ve ¬B üretmek",
                    "Hedef ¬A olduğundan ¬I, A varsayımı altında ⊥ alt hedefini verir.",
                    "İleri",
                ),
                (
                    "¬¬A ⊢ A kanıtında ¬A varsayımı ile ¬¬A hangi kuralı besler?",
                    ["→E", "¬E", "X", "∧I"],
                    "¬E",
                    "¬¬A, ¬A cümlesinin tam olumsuzudur; çift ⊥ üretir.",
                    "Zor",
                ),
            ]
        ),
        {
            "prompt": "A → B, A → ¬B ⊢ ¬A iskeletindeki AS, koşul eleme, çelişki ve kapanış satırlarını tamamla.",
            "starter": "Hedefin ana bağlacı ¬ olduğundan A'yı varsay; iki koşulun aynı A girdisiyle hangi çifti ürettiğini izle.",
            "checks": [
                "A, AS ile yeni kapsam açtı",
                "B ve ¬B, iki ayrı →E satırıyla üretildi",
                "⊥, tam çelişki çiftine atıflı ¬E ile kuruldu",
                "¬I, A varsayımından son ⊥ satırına kadar doğru aralığı kapattı",
            ],
            "solution": "l1 A → B PR; l2 A → ¬B PR; l3 A AS; l4 B →E l1,l3; l5 ¬B →E l2,l3; l6 ⊥ ¬E l4,l5; l7 ¬A ¬I l3-l6.",
        },
        [
            _production_task(
                "Üç çelişki temelli türetimi kur ve her birinde kullanılan kuralın farklı kanıt yükünü açıkla.",
                [
                    "A → B, A → ¬B ⊢ ¬A türetiminde ¬I alt kanıtını doğru kapat.",
                    "¬¬A ⊢ A türetiminde klasik IP'nin hedefe tam eşleşen olumsuz varsayımını göster.",
                    "A, ¬A ⊢ C türetiminde ¬E ile X'i iki ayrı satırda kullan.",
                    "Her ⊥ satırında tam çelişki çiftini ve erişilebilirlik durumunu belirt.",
                ],
                "Önce hedef biçiminden ¬I/IP/X adayını seç; ardından gerekli ⊥ satırını hangi erişilebilir çiftin üreteceğini planla.",
                "Türetim problemleri",
                [
                    "A → B, A → ¬B ⊢ ¬A",
                    "¬¬A ⊢ A",
                    "A, ¬A ⊢ C",
                ],
                "IP'nin klasik sisteme özgü olduğunu, X'in ise bu derste kullanılan klasik TFL sistemi içinde lisanslandığını not et.",
            )
        ],
        [
            "¬E ile yalnız tam 𝒜/¬𝒜 çiftinden ve iki erişilebilir satırdan ⊥ üretir.",
            "¬I uygulamasında varsayım formülünü hedef olumsuzun içiyle, alt kanıt sonunu ⊥ ile eşler.",
            "IP uygulamasında başlangıç varsayımını hedefin tam olumsuzuyla, alt kanıt sonunu ⊥ ile eşler.",
            "X'i yalnız tek erişilebilir ⊥ satırına atıfla uygular ve kapalı kapsam içindeki ⊥ı reddeder.",
            "¬I, IP, ¬E ve X için atıf türü ile varsayım boşaltma farklarını bağımsız örneklerde açıklar.",
            "Doğrudan kanıt ile klasik IP arasında gerekçeli strateji seçimi yapar.",
        ],
        [
            "¬I ile IP hangi farklı varsayımları boşaltır?",
            "¬E neden herhangi iki tutarsız görünen cümleden uygulanamaz?",
            "⊥ hangi durumda dış kapsamda X kaynağı olarak kullanılabilir?",
            "Patlama neden çelişki çiftinden doğrudan değil, ayrı ⊥ satırından çalışır?",
        ],
        "Sonraki derste ayrık bağlaç için iki kardeş alt kanıtı aynı hedefte birleştirecek, çift yönlülüğün iki yönünü ayrı kanıt yükleri olarak kuracağız.",
        [
            "forallx-basic-rules",
            "forallx-proof-strategies",
            "carnap-derivations",
            "carnap-feedback",
        ],
        "D22, ⊥ işaretini yalnız yapılandırılmış kanıt satırlarında özel bir çelişki göstergesi olarak işler. ¬I ile IP aynı kural değildir; IP klasik TFL sistemi içinde açıkça etiketlenir. D23'te açılacak ∨ ve ↔ kuralları ile D25'teki türetilmiş kurallar bu derste kapalıdır.",
        [
            "ders-18-degil-ve-ve-baglaclari",
            "ders-25-dogal-turetim-ii",
        ],
    )

    lesson["reading_note"] = (
        "Çelişki gördüğünde önce tam 𝒜/¬𝒜 çiftini ve erişilebilirliği doğrula. Hedef ¬𝒜 ise 𝒜 ile ¬I, hedef 𝒜 ise gerekirse ¬𝒜 ile IP planla; hazır ⊥ varsa X'i ayrı satırda uygula."
    )
    lesson["symbol_set"] = [
        "𝒜",
        "ℬ",
        "¬",
        "⊥",
        "¬I",
        "¬E",
        "X",
        "IP",
        "AS",
        "⊢",
    ]
    lesson["proof_tools"] = [
        "Tam çelişki çifti denetimi",
        "⊥ bağımlılık izi",
        "¬I/IP varsayım eşleştirme",
        "Alt kanıt son satır denetimi",
        "Patlama kaynak denetimi",
        "Doğrudan/dolaylı strateji karşılaştırması",
    ]
    lesson["rule_scope"] = {
        "introduced": ["¬I", "¬E", "X", "IP"],
        "review_only": ["PR", "AS", "R", "∧I", "∧E", "→I", "→E"],
        "locked_until_later": [
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
            "id": "d22-complete-negation-introduction",
            "kind": "complete",
            "title": "Koşul çiftinden ¬I ile olumsuz hedef kurma",
            "expected_issue_codes": [],
            "proof": {
                "id": "d22-complete-negation-introduction",
                "premises": ["A → B", "A → ¬B"],
                "target": "¬A",
                "lines": [
                    _line("l1", "A → B", "PR"),
                    _line("l2", "A → ¬B", "PR"),
                    _line("l3", "A", "AS", depth=1, opens="s1"),
                    _line(
                        "l4",
                        "B",
                        "→E",
                        citations=[_line_ref("l1"), _line_ref("l3")],
                        depth=1,
                    ),
                    _line(
                        "l5",
                        "¬B",
                        "→E",
                        citations=[_line_ref("l2"), _line_ref("l3")],
                        depth=1,
                    ),
                    _line(
                        "l6",
                        "⊥",
                        "¬E",
                        citations=[_line_ref("l5"), _line_ref("l4")],
                        depth=1,
                    ),
                    _line(
                        "l7",
                        "¬A",
                        "¬I",
                        citations=[_subproof_ref("l3", "l6")],
                        closes=["s1"],
                    ),
                ],
            },
        },
        {
            "id": "d22-complete-indirect-proof",
            "kind": "complete",
            "title": "Çifte olumsuzdan klasik IP ile olumlu hedef",
            "expected_issue_codes": [],
            "proof": {
                "id": "d22-complete-indirect-proof",
                "premises": ["¬¬A"],
                "target": "A",
                "lines": [
                    _line("l1", "¬¬A", "PR"),
                    _line("l2", "¬A", "AS", depth=1, opens="s1"),
                    _line(
                        "l3",
                        "⊥",
                        "¬E",
                        citations=[_line_ref("l1"), _line_ref("l2")],
                        depth=1,
                    ),
                    _line(
                        "l4",
                        "A",
                        "IP",
                        citations=[_subproof_ref("l2", "l3")],
                        closes=["s1"],
                    ),
                ],
            },
        },
        {
            "id": "d22-complete-explosion",
            "kind": "complete",
            "title": "Açık çelişkiden ayrı X adımıyla hedef üretme",
            "expected_issue_codes": [],
            "proof": {
                "id": "d22-complete-explosion",
                "premises": ["A", "¬A"],
                "target": "C",
                "lines": [
                    _line("l1", "A", "PR"),
                    _line("l2", "¬A", "PR"),
                    _line(
                        "l3",
                        "⊥",
                        "¬E",
                        citations=[_line_ref("l1"), _line_ref("l2")],
                    ),
                    _line(
                        "l4",
                        "C",
                        "X",
                        citations=[_line_ref("l3")],
                    ),
                ],
            },
        },
        {
            "id": "d22-incomplete-negation-introduction",
            "kind": "incomplete",
            "title": "¬I kapanışı henüz eklenmemiş doğru çelişki alt kanıtı",
            "expected_issue_codes": [],
            "next_rule": "¬I l3-l6",
            "proof": {
                "id": "d22-incomplete-negation-introduction",
                "premises": ["A → B", "A → ¬B"],
                "target": "¬A",
                "lines": [
                    _line("l1", "A → B", "PR"),
                    _line("l2", "A → ¬B", "PR"),
                    _line("l3", "A", "AS", depth=1, opens="s1"),
                    _line(
                        "l4",
                        "B",
                        "→E",
                        citations=[_line_ref("l1"), _line_ref("l3")],
                        depth=1,
                    ),
                    _line(
                        "l5",
                        "¬B",
                        "→E",
                        citations=[_line_ref("l2"), _line_ref("l3")],
                        depth=1,
                    ),
                    _line(
                        "l6",
                        "⊥",
                        "¬E",
                        citations=[_line_ref("l4"), _line_ref("l5")],
                        depth=1,
                    ),
                ],
            },
        },
        {
            "id": "d22-false-contradiction",
            "kind": "error",
            "title": "Farklı atomları çelişki çifti sanma",
            "expected_issue_codes": ["rule.negation_elimination_mismatch"],
            "proof": {
                "id": "d22-false-contradiction",
                "premises": ["A", "¬B"],
                "target": "⊥",
                "lines": [
                    _line("l1", "A", "PR"),
                    _line("l2", "¬B", "PR"),
                    _line(
                        "l3",
                        "⊥",
                        "¬E",
                        citations=[_line_ref("l1"), _line_ref("l2")],
                    ),
                ],
            },
        },
    ]
    return lesson


def _candidate_d23():
    lesson = _lesson(
        "D23",
        "ders-ayrik-baglac-ve-cift-yonluluk-kurallari",
        "Ayrık Bağlaç ve Çift Yönlülük Kuralları",
        "Ayrık bir öncülü iki kardeş alt kanıtta tüketip ortak sonuca ulaşır; çift yönlülüğü ise iki yönü bağımsız olarak lisanslayarak kurar ve kullanır.",
        "Durum analizi, kardeş kapsamlar ve iki yönlü kanıt yükü",
        55,
        [
            "ders-olumsuzlama-alt-kanit-ve-celiskiye-indirgeme",
            "ders-19-veya-ve-ise",
            "ders-kosul-yalnizca-cift-yonluluk",
            "ders-mantiksal-esdegerlik-ve-tutarlilik",
        ],
        [
            "nd.disjunction_introduce",
            "nd.cases_prove",
            "nd.biconditional_rules",
            "nd.sibling_scope_manage",
        ],
        [
            "Erişilebilir bir cümleyi hedef ayrık yapının sol veya sağ doğrudan ayrılanı olarak ∨I ile yerleştirmek.",
            "𝒜 ∨ ℬ satırı için 𝒜 ve ℬ ile açılan iki kardeş alt kanıtta aynı 𝒞 sonucuna ulaşıp ∨E ile 𝒞'yi dışarı taşımak.",
            "Bir kardeş alt kanıtın varsayım ve iç satırlarını diğer kardeş dalda kullanmamak.",
            "𝒜 ↔ ℬ ile taraflardan birini kullanarak ↔E ile tam karşı tarafı üretmek.",
            "𝒜'dan ℬ'ye ve ℬ'den 𝒜'ya giden iki ayrı kardeş alt kanıtı ↔I ile boşaltarak 𝒜 ↔ ℬ kurmak.",
        ],
        [
            (
                "Ayrık bağlaç giriş (∨I)",
                "Erişilebilir 𝒜 cümlesinden, 𝒜'nın iki doğrudan ayrılandan biri olduğu 𝒜 ∨ ℬ veya ℬ ∨ 𝒜 cümlesini üretme kuralı.",
            ),
            (
                "Durum analizi (∨E)",
                "𝒜 ∨ ℬ ile, 𝒜 varsayımından 𝒞 ve ℬ varsayımından aynı 𝒞 sonucunu veren iki kardeş alt kanıttan 𝒞 çıkarma kuralı.",
            ),
            (
                "Kardeş alt kanıt",
                "Aynı ana kapsam altında açılan, birbirinin içinde olmayan ve iç satırları karşılıklı erişilemez iki ayrı alt kanıt.",
            ),
            (
                "Ortak dal sonucu",
                "∨E ile dışarı çıkarılan ve iki alt kanıtın da son doğrudan satırında aynen bulunan cümle.",
            ),
            (
                "Çift yönlülük eleme (↔E)",
                "𝒜 ↔ ℬ ve taraflardan biri erişilebilirken tam karşı tarafı çıkarma kuralı.",
            ),
            (
                "Çift yönlülük giriş (↔I)",
                "𝒜 varsayımından ℬ ve ℬ varsayımından 𝒜 çıkaran iki ayrı kardeş alt kanıtı kullanarak 𝒜 ↔ ℬ kurma kuralı.",
            ),
            (
                "İki yönlü kanıt yükü",
                "Bir çift yönlülüğün sol-sağ ve sağ-sol yönlerinin birbirinden bağımsız olarak lisanslanması gereği.",
            ),
        ],
        [
            _section(
                "∨I ile ayrık hedef kurmak",
                "∨I, eldeki bir cümleyi daha zayıf bir ayrık iddiaya yerleştirir. Kaynak cümle sonuçtaki iki doğrudan ayrılandan biri olmalıdır; öteki ayrılan için ayrıca kanıt gerekmez.",
                "Hedefin ana bağlacı ∨ olduğunda ve ayrılanlardan en az biri zaten erişilebilir olduğunda.",
                "𝒜 ⟹ 𝒜 ∨ ℬ veya ℬ ∨ 𝒜 · ∨I",
                "Eklenen ℬ herhangi bir TFL cümlesi olabilir. Buna rağmen kaynak 𝒜 sonuçta aynen bir doğrudan ayrılan olarak görünmelidir; iç içe bir alt formül yetmez.",
                "A'dan (A ∧ B) ∨ C üretmek veya hedefte hazır ayrılan varken gereksiz alt kanıt açmak.",
                [
                    ("A ⊢ A ∨ B", "A sol ayrılan olduğu için tek ∨I adımı yeterlidir."),
                    ("A ⊢ B ∨ A", "A sağ ayrılan olarak da yerleştirilebilir."),
                    ("A ⊢ (A ∧ B) ∨ C", "A, A ∧ B'nin yalnız alt formülüdür; doğrudan ayrılan değildir."),
                ],
                (
                    "Kaynağı hedefin iki doğrudan ayrılanıyla tam eşleştir.",
                    "Kaynak hedefin herhangi bir yerinde geçiyorsa ∨I uygula.",
                    "Kural sözdizim ağacının yalnız ana ∨ düğümündeki çocuklarını kullanır.",
                ),
            ),
            _section(
                "∨E ile bütün durumları tüketmek",
                "Ayrık bir satır tek başına hangi ayrılanın doğru olduğunu söylemez. ∨E, her ayrılanı geçici olarak varsayan iki ayrı dalda aynı sonucu kurarak bu belirsizliği güvenli biçimde tüketir.",
                "Erişilebilir 𝒜 ∨ ℬ satırından, iki olası durumda da kanıtlanabilen ortak 𝒞 sonucuna ihtiyaç duyulduğunda.",
                "𝒜 ∨ ℬ; [𝒜 AS ... 𝒞]; [ℬ AS ... 𝒞] ⟹ 𝒞 · ∨E",
                "∨E üç kaynak türü ister: bir ayrık satır ve iki kapalı alt kanıt. Dalların başlangıçları iki ayrılanla, sonları ise dışarı yazılan aynı 𝒞 ile tam eşleşir.",
                "A ∨ B'den doğrudan A çıkarmak, yalnız A dalını kanıtlamak veya dalları C ve D gibi farklı sonuçlarda bitirmek.",
                [
                    ("A ∨ B, A → C, B → C ⊢ C", "A ve B dalları ayrı →E adımlarıyla C'de buluşur."),
                    ("(P ∧ Q) ∨ (P ∧ R) ⊢ P", "Her dalda ∧E ile aynı P çıkarılır."),
                    ("A dalı C; B dalı D; sonuç C", "İkinci dal C'yi garanti etmediği için ∨E lisanssızdır."),
                ],
                (
                    "Önce dışarı taşınacak ortak 𝒞'yi seç, sonra iki dalı ona göre kur.",
                    "Her dalda ulaşılabilen herhangi bir sonuç yeterlidir.",
                    "Durum analizi, hangi durum gerçekleşirse gerçekleşsin aynı sonucun güvence altında olduğunu gösterir.",
                ),
            ),
            _section(
                "Kardeş kapsamları korumak",
                "∨E dalları aynı ana kapsamda açılır, fakat birbirinin içinde değildir. İlk dal kapandığında onun varsayımı ve türetilmiş satırları ikinci dalda kullanılamaz; yalnız ortak üst kapsam satırları iki dalda da erişilebilirdir.",
                "İki veya daha fazla vaka dalı içeren kanıtlarda gizli varsayım aktarımını önlemek için.",
                "ana kapsam Γ; dal 1 Γ+𝒜; dal 2 Γ+ℬ; dal 1 ↛ dal 2",
                "İkinci dalı açan AS satırı aynı anda ilk dalı kapatabilir. İki dalın `parent_path` değeri aynı, kapsam kimlikleri ayrı olmalıdır.",
                "İlk dalda elde edilen C'yi ikinci dalda R ile yinelemek veya ikinci dalı birinci dalın içinde açarak kardeş sanmak.",
                [
                    ("Kök P; A dalı P kullanır; B dalı P kullanır", "Kök P iki dalın ortak üst kapsamında olduğu için erişilebilirdir."),
                    ("A dalında C; B dalında C R", "İlk dal kapanınca C ikinci dal için erişilemez olur."),
                    ("A dalının içinde B dalı", "B dalı kardeş değil iç içe alt kanıttır; ∨E şemasına uymaz."),
                ],
                (
                    "Her dalın bağımlılıklarını yalnız üst kapsam ve kendi açık varsayımlarıyla izle.",
                    "Ekranda önce görünen her satırı sonraki dalda kullanılabilir say.",
                    "Erişilebilirlik kronolojiye değil açık kapsam yoluna bağlıdır.",
                ),
            ),
            _section(
                "↔E ile doğru yönü seçmek",
                "𝒜 ↔ ℬ iki koşul yönünü birlikte taşır. ↔E, çift yönlülük satırıyla 𝒜 verilmişse ℬ'yi; ℬ verilmişse 𝒜'yı üretir.",
                "Bir çift yönlülüğün taraflarından biri erişilebilirken diğer taraf ara hedef olduğunda.",
                "𝒜 ↔ ℬ, 𝒜 ⟹ ℬ; 𝒜 ↔ ℬ, ℬ ⟹ 𝒜 · ↔E",
                "Atıf sırası kural motorunda esnek olsa da okunurluk için çift yönlülüğü önce göstermek iyidir. Verilen argüman iki taraftan biriyle tam eşleşmelidir.",
                "𝒜 ↔ ℬ ile ilgisiz 𝒞'den 𝒜 çıkarmak veya sonucu verilen tarafla aynı bırakmak.",
                [
                    ("A ↔ B, A ⊢ B", "Sol taraftan sağ tarafa ↔E."),
                    ("A ↔ B, B ⊢ A", "Sağ taraftan sol tarafa ↔E."),
                    ("A ↔ B, C ⊢ A", "C çift yönlülüğün tarafı olmadığı için kural uygulanamaz."),
                ],
                (
                    "Verilen tarafı belirle ve tam karşı tarafı sonuç olarak yaz.",
                    "↔ işaretini iki formül arasında serbest geçiş izni san.",
                    "Kural yalnız aynı çift yönlülüğün iki doğrudan tarafını bağlar.",
                ),
            ),
            _section(
                "↔I ile iki yönü ayrı kanıtlamak",
                "𝒜 ↔ ℬ hedefi iki bağımsız yük doğurur: 𝒜 varsayımı altında ℬ ve ℬ varsayımı altında 𝒜. ↔I bu iki kardeş alt kanıtın ikisini birden boşaltır.",
                "Hedefin ana bağlacı ↔ olduğunda ve iki yönün her biri mevcut kurallarla kurulabildiğinde.",
                "[𝒜 AS ... ℬ] ve [ℬ AS ... 𝒜] ⟹ 𝒜 ↔ ℬ · ↔I",
                "Yön alt kanıtları herhangi sırada gelebilir ve aralarında başka kök satırlar bulunabilir. Ancak tek bir koşul, aynı alt kanıtı iki kez göstermek veya iki aynı yön yeterli değildir.",
                "Yalnız A'dan B'ye yönü kurup A ↔ B yazmak; A ve B'yi birlikte erişilebilir gördüğü için ↔I uygulamak.",
                [
                    ("A ∧ B ↔ B ∧ A", "Her yönde ∧E ile bileşenler çıkarılıp ters sırada ∧I yapılır."),
                    ("A ↔ A", "Yine de iki ayrı kardeş alt kanıtta iki yön gösterilir."),
                    ("A AS ... B; aynı aralığı iki kez ↔I", "İki ayrı yön yükü yerine aynı kanıt tekrarlandığı için lisanssızdır."),
                ],
                (
                    "İki yönü ayrı alt hedef ve ayrı kapsam kimlikleriyle planla.",
                    "Bir yön kanıtlandıysa ters yönü simetriden otomatik kabul et.",
                    "Doğal dilde simetrik görünen ilişkiler bile biçimsel kanıtta iki ayrı lisans ister.",
                ),
            ),
            _section(
                "Durum analizi ile iki yönlü yükü planlamak",
                "∨E ve ↔I ikişer alt kanıt kullanır ama amaçları farklıdır. ∨E farklı başlangıçlardan aynı sonuca, ↔I ise iki taraf arasında ters yönlü sonuçlara gider.",
                "Çoklu alt kanıt gerektiren bir hedefte doğru kural şemasını seçmek ve dalları ekonomik biçimde düzenlemek için.",
                "∨E: A→C ve B→C; ↔I: A→B ve B→A (alt kanıt biçiminde)",
                "Plan tablosunda her dal için başlangıç varsayımı, gereken son satır ve ortak üst kapsam kaynakları önceden yazılabilir. Bu, kardeş kapsam sızıntısını erkenden görünür kılar.",
                "İki alt kanıt gördüğü için ↔I ile ∨E'yi birbirinin yerine kullanmak veya dal sonlarını planlamadan AS satırları açmak.",
                [
                    ("A ∨ B, A → C, B → C ⊢ C", "İki başlangıç, tek ortak sonuç: ∨E."),
                    ("⊢ (A ∧ B) ↔ (B ∧ A)", "İki başlangıç birbirinin sonucuna gider: ↔I."),
                    ("A ↔ B, A ∨ B ⊢ A ∧ B", "Vaka dallarında ↔E ile eksik taraf bulunur, sonra ortak birleşim kurulur."),
                ],
                (
                    "Kuralı dal başlangıç/son desenine göre seç.",
                    "Alt kanıt sayısını görüp kuralı tahmin et.",
                    "Yapısal şema, yalnız kaç dal bulunduğundan daha fazla bilgi taşır.",
                ),
            ),
        ],
        [
            _worked("A ⊢ A ∨ B", "Kaynak A hedefin sol doğrudan ayrılanıdır.", "∨I"),
            _worked("A ⊢ B ∨ A", "Kaynak A sağ doğrudan ayrılan olarak da kullanılabilir.", "∨I"),
            _worked(
                "A ∨ B, A → C, B → C ⊢ C",
                "A ve B kardeş dalları ayrı →E adımlarıyla aynı C'de biter.",
                "∨E",
            ),
            _worked(
                "A ∨ B; A dalı C; B dalı D; sonuç C",
                "İkinci dal C'yi güvenceye almadığı için durum analizi tamamlanmamıştır.",
                "Farklı dal sonucu",
                "bad",
            ),
            _worked("A ↔ B, A ⊢ B", "↔E verilen taraftan tam karşı tarafa geçer.", "↔E"),
            _worked("A ↔ B, B ⊢ A", "↔E ters yönde de aynı çift yönlülüğü kullanır.", "↔E"),
            _worked(
                "⊢ (A ∧ B) ↔ (B ∧ A)",
                "İki kardeş alt kanıt birleşimin iki sırasını karşılıklı kurar.",
                "↔I",
            ),
            _worked(
                "A AS ... B; aynı aralık iki kez; sonuç A ↔ B",
                "Tek alt kanıt iki ayrı yönün kanıtı sayılamaz.",
                "Eksik yön",
                "bad",
            ),
        ],
        [
            "∨I kaynağını hedefte doğrudan ayrılan yerine yalnız alt formül olarak bulmak.",
            "A ∨ B'den doğrudan A veya B çıkarmak.",
            "∨E için yalnız bir dal kurmak veya iki dalı farklı sonuçlarda bitirmek.",
            "İlk kardeş dalın varsayım ya da iç satırını ikinci dalda kullanmak.",
            "↔E ile verilen tarafı aynen tekrar etmek veya ilgisiz bir cümleyi yön girdisi yapmak.",
            "↔I için tek yönü, aynı yönü iki kez veya aynı alt kanıtı iki kez göstermek.",
            "Kardeş olması gereken iki alt kanıttan birini diğerinin içinde açmak.",
        ],
        _practice(
            [
                ("A'dan hangisi tek ∨I ile çıkar?", ["A ∨ B", "A ∧ B", "B", "A → B"], "A ∨ B", "A hedefin doğrudan ayrılanıdır.", "Temel"),
                ("A'dan B ∨ A çıkar mı?", ["Evet", "Hayır", "Yalnız B öncülse", "Yalnız IP ile"], "Evet", "Kaynak sağ ayrılan olarak yerleştirilebilir.", "Temel"),
                ("A ∨ B tek başına hangisini lisanslar?", ["A", "B", "Ne A ne B tek başına", "A ∧ B"], "Ne A ne B tek başına", "Hangi ayrılanın doğru olduğu belirlenmemiştir.", "Temel"),
                ("∨E dalları hangi sonuçla bitmelidir?", ["Farklı sonuçlarla", "Aynı dış sonuçla", "Daima ⊥ ile", "Kendi varsayımlarıyla"], "Aynı dış sonuçla", "Her olası durumda dış sonucun güvenceye alınması gerekir.", "Temel"),
                ("A ↔ B ve A hangi sonucu ↔E ile verir?", ["A", "B", "A ↔ A", "⊥"], "B", "Verilen sol taraf karşı sağ tarafı lisanslar.", "Temel"),
                ("A ↔ B hedefi için ↔I kaç alt kanıt ister?", ["Sıfır", "Bir", "İki", "Üç"], "İki", "Her yön ayrı bir alt kanıtta kanıtlanır.", "Orta"),
                ("A ∨ B için ∨E dal varsayımları hangileridir?", ["İki kez A", "A ve B", "¬A ve ¬B", "A ∧ B ve A"], "A ve B", "Dallar iki doğrudan ayrılanla açılır.", "Orta"),
                ("İlk ∨E dalındaki C ikinci dalda R ile kullanılabilir mi?", ["Evet", "Hayır", "Yalnız C atomikse", "Yalnız hedef C ise"], "Hayır", "İlk dal kapandığında iç satırları kardeş dal için erişilemezdir.", "Orta"),
                ("↔I yönleri hangi biçimdedir?", ["A'dan B ve B'den A", "A'dan B ve A'dan B", "A'dan A ve B'den B", "A ∨ B'den A"], "A'dan B ve B'den A", "İki ters yön çift yönlülüğü lisanslar.", "Orta"),
                ("(A ∧ B) ∨ (A ∧ C) ⊢ A için dal sonları ne olmalı?", ["B ve C", "A ve A", "A ∧ B ve A ∧ C", "⊥ ve A"], "A ve A", "Her dalda ∧E ile ortak A elde edilir.", "İleri"),
                ("A ↔ B ve A ∨ B'den A ∧ B planında her dal ne yapar?", ["Yalnız varsayımı tekrarlar", "↔E ile eksik tarafı bulup ∧I yapar", "X kullanır", "IP ile dalı kapatır"], "↔E ile eksik tarafı bulup ∧I yapar", "Her iki durumda da ortak A ∧ B sonucu kurulur.", "İleri"),
                ("İki alt kanıt aynı parent altında ama aynı scope kimliğine sahip. ↔I olur mu?", ["Evet", "Hayır, iki ayrı yön kapsamı gerekir", "Yalnız sonuç atomikse", "Yalnız R kullanıldıysa"], "Hayır, iki ayrı yön kapsamı gerekir", "Aynı alt kanıtı iki kez göstermek iki bağımsız yön değildir.", "Zor"),
            ]
        ),
        {
            "prompt": "A ∨ B, A → C, B → C ⊢ C iskeletinde iki kardeş dalı ve son ∨E atfını tamamla.",
            "starter": "Ayrık öncülün sol ayrılanıyla ilk dalı, sağ ayrılanıyla ikinci dalı aç; iki koşulu ortak C hedefine bağla.",
            "checks": [
                "İlk dal A AS ile açıldı ve C ile bitti",
                "İkinci dal aynı ana kapsamda B AS ile açıldı ve C ile bitti",
                "İlk dalın iç satırları ikinci dalda kullanılmadı",
                "∨E bir ayrık satır ile iki tam alt kanıt aralığına atıf yaptı",
            ],
            "solution": "l1 A ∨ B PR; l2 A → C PR; l3 B → C PR; l4 A AS; l5 C →E l2,l4; l6 B AS; l7 C →E l3,l6; l8 C ∨E l1,l4-l5,l6-l7.",
        },
        [
            _production_task(
                "Bir durum analizi ve bir çift yönlülük kanıtı kur; dal bağımlılıklarını açıkça göster.",
                [
                    "A ∨ B, A → C, B → C ⊢ C türetiminde iki kardeş dalı aynı C'de bitir.",
                    "A ↔ B ⊢ (A ∧ B) ∨ (¬A ∧ ¬B) için önce vaka ayrımını sağlayacak ara hedefi planla.",
                    "İkinci kanıtta A dalında ve ¬A dalında ortak ayrık hedefe nasıl ulaşılacağını ayrı yaz.",
                    "Her kapatılan alt kanıtın başlangıç, son ve ana kapsam kimliğini denetle.",
                ],
                "İkinci problemde önce A ∨ ¬A ara hedefini klasik IP ile kurabilir, ardından iki vakayı A ↔ B ile ortak hedefe bağlayabilirsin.",
                "Türetim problemleri",
                [
                    "A ∨ B, A → C, B → C ⊢ C",
                    "A ↔ B ⊢ (A ∧ B) ∨ (¬A ∧ ¬B)",
                ],
                "Uzun ikinci kanıtta önce yalnız kapsam planını yaz; doğru ama kontrol edilemeyen tek seferlik bir satır yığını kurma.",
            )
        ],
        [
            "∨I kaynağını hedef ayrık yapının doğrudan ayrılanlarından biriyle tam eşleştirir.",
            "∨E için ayrık kaynak, iki ayrı kardeş alt kanıt ve aynı dal sonucunu eksiksiz gösterir.",
            "Kardeş dallar arasında tekil satır atfını reddeder, ortak üst kapsam kaynaklarını doğru kullanır.",
            "↔E ile verilen tarafın tam karşı tarafını iki yönde de doğru üretir.",
            "↔I için iki ters yönü ayrı kardeş alt kanıtlarda tamamlar ve aynı alt kanıtı iki kez kullanmaz.",
            "∨E ile ↔I yapılarını başlangıç/son desenleri ve kanıt amaçları bakımından açıklar.",
        ],
        [
            "∨E dalları neden aynı cümleyle bitmelidir?",
            "Bir kardeş alt kanıttaki satır öteki dalda neden kullanılamaz?",
            "↔I için tek bir yön neden yetersizdir?",
            "∨I neden eklenen öteki ayrılan için ayrıca kanıt istemez?",
        ],
        "Sonraki derste yeni kural eklemek yerine bütün temel kuralları hedefe göre geriye ve kaynaklara göre ileri planlamayı öğreneceğiz.",
        [
            "forallx-basic-rules",
            "forallx-proof-strategies",
            "carnap-derivations",
            "carnap-feedback",
        ],
        "D23'te ∨E iki ayrı kardeş alt kanıtın aynı sonuçla bitmesini, ↔I ise iki ters yönün ayrı alt kanıtlarda kurulmasını zorunlu kılar. DS, MT, LEM ve eşdeğerlik dönüşümleri D25'e kadar kapalıdır; uzun üretim görevi yalnız o ana kadar açılmış temel kurallarla çözülür.",
        [
            "ders-19-veya-ve-ise",
            "ders-25-dogal-turetim-ii",
        ],
    )

    lesson["reading_note"] = (
        "∨E planında iki dalın başlangıçlarını ayrılanlarla, sonlarını ortak hedefle eşleştir. ↔I planında ise aynı hedefe değil, sol-sağ ve sağ-sol yönlerine giden iki ayrı kardeş kapsam kur."
    )
    lesson["symbol_set"] = [
        "𝒜",
        "ℬ",
        "𝒞",
        "∨",
        "↔",
        "∨I",
        "∨E",
        "↔I",
        "↔E",
        "AS",
        "⊢",
    ]
    lesson["proof_tools"] = [
        "Doğrudan ayrılan eşleştirme",
        "Durum analizi dal tablosu",
        "Kardeş kapsam yolu denetimi",
        "Ortak dal sonucu denetimi",
        "Çift yön yükü matrisi",
        "Çoklu alt kanıt atfı",
    ]
    lesson["rule_scope"] = {
        "introduced": ["∨I", "∨E", "↔I", "↔E"],
        "review_only": [
            "PR",
            "AS",
            "R",
            "∧I",
            "∧E",
            "→I",
            "→E",
            "¬I",
            "¬E",
            "X",
            "IP",
        ],
        "locked_until_later": ["DS", "MT", "DNE", "LEM", "DeM"],
    }
    lesson["proof_fixtures"] = [
        {
            "id": "d23-complete-disjunction-introduction",
            "kind": "complete",
            "title": "Hazır cümleyi sağ ayrılan olarak yerleştirme",
            "expected_issue_codes": [],
            "proof": {
                "id": "d23-complete-disjunction-introduction",
                "premises": ["A"],
                "target": "B ∨ A",
                "lines": [
                    _line("l1", "A", "PR"),
                    _line(
                        "l2",
                        "B ∨ A",
                        "∨I",
                        citations=[_line_ref("l1")],
                    ),
                ],
            },
        },
        {
            "id": "d23-complete-disjunction-elimination",
            "kind": "complete",
            "title": "İki kardeş koşul dalını ortak sonuçta birleştirme",
            "expected_issue_codes": [],
            "proof": {
                "id": "d23-complete-disjunction-elimination",
                "premises": ["A ∨ B", "A → C", "B → C"],
                "target": "C",
                "lines": [
                    _line("l1", "A ∨ B", "PR"),
                    _line("l2", "A → C", "PR"),
                    _line("l3", "B → C", "PR"),
                    _line("l4", "A", "AS", depth=1, opens="s1"),
                    _line(
                        "l5",
                        "C",
                        "→E",
                        citations=[_line_ref("l2"), _line_ref("l4")],
                        depth=1,
                    ),
                    _line(
                        "l6",
                        "B",
                        "AS",
                        depth=1,
                        opens="s2",
                        closes=["s1"],
                    ),
                    _line(
                        "l7",
                        "C",
                        "→E",
                        citations=[_line_ref("l3"), _line_ref("l6")],
                        depth=1,
                    ),
                    _line(
                        "l8",
                        "C",
                        "∨E",
                        citations=[
                            _line_ref("l1"),
                            _subproof_ref("l4", "l5"),
                            _subproof_ref("l6", "l7"),
                        ],
                        closes=["s2"],
                    ),
                ],
            },
        },
        {
            "id": "d23-complete-biconditional-elimination",
            "kind": "complete",
            "title": "Çift yönlülüğün sağından soluna geçme",
            "expected_issue_codes": [],
            "proof": {
                "id": "d23-complete-biconditional-elimination",
                "premises": ["A ↔ B", "B"],
                "target": "A",
                "lines": [
                    _line("l1", "A ↔ B", "PR"),
                    _line("l2", "B", "PR"),
                    _line(
                        "l3",
                        "A",
                        "↔E",
                        citations=[_line_ref("l1"), _line_ref("l2")],
                    ),
                ],
            },
        },
        {
            "id": "d23-complete-biconditional-introduction",
            "kind": "complete",
            "title": "Birleşim sırasını iki yönde kanıtlama",
            "expected_issue_codes": [],
            "proof": {
                "id": "d23-complete-biconditional-introduction",
                "premises": [],
                "target": "(A ∧ B) ↔ (B ∧ A)",
                "lines": [
                    _line("l1", "A ∧ B", "AS", depth=1, opens="s1"),
                    _line("l2", "A", "∧E", citations=[_line_ref("l1")], depth=1),
                    _line("l3", "B", "∧E", citations=[_line_ref("l1")], depth=1),
                    _line("l4", "B ∧ A", "∧I", citations=[_line_ref("l3"), _line_ref("l2")], depth=1),
                    _line("l5", "B ∧ A", "AS", depth=1, opens="s2", closes=["s1"]),
                    _line("l6", "B", "∧E", citations=[_line_ref("l5")], depth=1),
                    _line("l7", "A", "∧E", citations=[_line_ref("l5")], depth=1),
                    _line("l8", "A ∧ B", "∧I", citations=[_line_ref("l7"), _line_ref("l6")], depth=1),
                    _line(
                        "l9",
                        "(A ∧ B) ↔ (B ∧ A)",
                        "↔I",
                        citations=[
                            _subproof_ref("l1", "l4"),
                            _subproof_ref("l5", "l8"),
                        ],
                        closes=["s2"],
                    ),
                ],
            },
        },
        {
            "id": "d23-incomplete-disjunction-elimination",
            "kind": "incomplete",
            "title": "İkinci kardeş dalı henüz eklenmemiş doğru ilk dal",
            "expected_issue_codes": [],
            "next_rule": "s1'i kapat, B AS ile s2'yi aç",
            "proof": {
                "id": "d23-incomplete-disjunction-elimination",
                "premises": ["A ∨ B", "A → C", "B → C"],
                "target": "C",
                "lines": [
                    _line("l1", "A ∨ B", "PR"),
                    _line("l2", "A → C", "PR"),
                    _line("l3", "B → C", "PR"),
                    _line("l4", "A", "AS", depth=1, opens="s1"),
                    _line(
                        "l5",
                        "C",
                        "→E",
                        citations=[_line_ref("l2"), _line_ref("l4")],
                        depth=1,
                    ),
                ],
            },
        },
        {
            "id": "d23-different-branch-results",
            "kind": "error",
            "title": "∨E dallarını farklı sonuçlarda bitirme",
            "expected_issue_codes": ["rule.disjunction_elimination_conclusions"],
            "proof": {
                "id": "d23-different-branch-results",
                "premises": ["A ∨ B", "A → C", "B → D"],
                "target": "C",
                "lines": [
                    _line("l1", "A ∨ B", "PR"),
                    _line("l2", "A → C", "PR"),
                    _line("l3", "B → D", "PR"),
                    _line("l4", "A", "AS", depth=1, opens="s1"),
                    _line("l5", "C", "→E", citations=[_line_ref("l2"), _line_ref("l4")], depth=1),
                    _line("l6", "B", "AS", depth=1, opens="s2", closes=["s1"]),
                    _line("l7", "D", "→E", citations=[_line_ref("l3"), _line_ref("l6")], depth=1),
                    _line(
                        "l8",
                        "C",
                        "∨E",
                        citations=[
                            _line_ref("l1"),
                            _subproof_ref("l4", "l5"),
                            _subproof_ref("l6", "l7"),
                        ],
                        closes=["s2"],
                    ),
                ],
            },
        },
    ]
    return lesson


def _candidate_d24():
    lesson = _lesson(
        "D24",
        "ders-geriye-dogru-planlama-ve-kanit-stratejisi",
        "Geriye Doğru Planlama ve Kanıt Stratejisi",
        "Hedefin yapısından geriye, erişilebilir satırların yapısından ileri çalışır; iki aramayı işe yaradığı açık bir ara hedefte buluşturur ve başarısız taslağı ilk stratejik çıkmazdan onarır.",
        "Hedef güdümlü arama, kaynak güdümlü açılım ve kanıt onarımı",
        55,
        ["ders-ayrik-baglac-ve-cift-yonluluk-kurallari"],
        [
            "nd.backward_plan",
            "nd.forward_expand",
            "nd.subgoal_choose",
            "nd.proof_repair",
        ],
        [
            "Hedefin ana bağlacından olası son kuralı ve bu kuralın açtığı alt hedefleri çıkarmak.",
            "Erişilebilir satırların ana bağlaçlarından hedefe yararlı eleme olanaklarını belirlemek.",
            "Geri ve ileri aramayı, hangi sonraki adımı mümkün kıldığı açıklanabilen bir köprü ara hedefte buluşturmak.",
            "Alt kanıtları satır yazmadan önce kapsam ve boşaltılacak varsayım bakımından planlamak.",
            "Kör IP, gereksiz patlama ve hedefsiz satır üretimini teşhis edip ilk stratejik çıkmazdan onarmak.",
        ],
        [
            (
                "Geriye doğru planlama",
                "Hedefin ana bağlacına bakıp olası son kuralı ve bu kural için daha önce kurulması gereken alt hedefleri yazma yöntemi.",
            ),
            (
                "İleri doğru açılım",
                "Erişilebilir öncül ve varsayımların ana bağlaçlarına uygun eleme kurallarıyla gerçekten yararlı sonuç adayları üretme yöntemi.",
            ),
            (
                "Köprü ara hedef",
                "İleri kaynaklardan elde edilebilen ve geriye doğru plandaki bir eksik yükü doğrudan kapatan cümle.",
            ),
            (
                "Son kural adayı",
                "Hedef biçiminin düşündürdüğü, fakat kaynaklar denetlenmeden zorunlu sayılmayan olası son adım.",
            ),
            (
                "Kapsam planı",
                "Hangi varsayımın nerede açılacağını, hangi hedefle kapanacağını ve dışarı hangi kural aracılığıyla taşınacağını gösteren alt kanıt taslağı.",
            ),
            (
                "Stratejik çıkmaz",
                "Satırlar tek tek lisanslı görünse bile hiçbirinin hedefe veya gerekli ara hedefe yaklaşmadığı kanıt durumu.",
            ),
            (
                "İlk onarılacak karar",
                "Başarısız taslakta sonraki hataları doğuran en erken yanlış hedef, kural, kaynak veya kapsam seçimi.",
            ),
            (
                "Satır ekonomisi",
                "Kanıtı sırf kısaltmak değil, her satırın sonraki açık bir yükü yerine getirmesini sağlamak.",
            ),
        ],
        [
            _section(
                "Hedeften geriye çalışmak",
                "Hedefin ana bağlacı olası son giriş kuralını düşündürür. Plan önce son adımı varsayımsal olarak yazar, sonra bu adımın gerektirdiği alt hedefleri açar.",
                "Kanıta hangi satırla başlanacağı belirsizken veya hedef bileşik bir TFL cümlesiyken.",
                "𝒜 ∧ ℬ ⇒ alt hedefler 𝒜, ℬ; 𝒜 → ℬ ⇒ [𝒜 AS ... ℬ]; ¬𝒜 ⇒ [𝒜 AS ... ⊥]",
                "Ana bağlaç aramayı daraltır, fakat son kuralı tek başına zorunlu kılmaz. Hedef daha önce elde edilebilir, R ile taşınabilir veya dolaylı bir yol gerektirebilir.",
                "Hedef koşul diye kaynaklara bakmadan AS açmak ya da hedef atomik diye geriye planlamanın bittiğini sanmak.",
                [
                    ("Hedef A → C", "Olası →I planı A varsayımı altında C alt hedefini açar."),
                    ("Hedef A ∧ C", "Olası ∧I planı A ve C için iki ayrı kanıt yükü çıkarır."),
                    ("Hedef C", "Atomik hedef son giriş kuralı söylemez; kaynaklardan ileri çalışma öne çıkar."),
                ],
                (
                    "Son kural adayını ve onun alt hedeflerini kurşun kalemle yazmak.",
                    "Ana bağlacı görünce kuralı uygulanmış saymak.",
                    "Plan bir yük listesi üretir; her yük yine lisanslı satırlarla gerçekten karşılanmalıdır.",
                ),
            ),
            _section(
                "Kaynaklardan ileri çalışmak",
                "Öncül ve açık varsayımların ana bağlaçları hangi eleme sonuçlarının elde edilebileceğini gösterir. Yalnız hedef veya planlanan ara hedefle ilişkili açılımlar seçilir.",
                "Hedef atomik olduğunda, geriye plan bir ara cümle istediğinde veya erişilebilir koşul/çift yönlülük/ayrık yapı bulunduğunda.",
                "𝒜 ∧ ℬ ⇒ 𝒜 veya ℬ; 𝒜 → ℬ + 𝒜 ⇒ ℬ; 𝒜 ↔ ℬ + bir taraf ⇒ öteki taraf",
                "İleri çalışma, uygulanabilen bütün kuralları tüketmek değildir. Her yeni satır için 'bu satır hangi açık yükü kapatacak?' sorusu cevaplanır.",
                "Her birleşimi parçalamak, her hazır cümleye ∨I uygulamak veya hedefle ilgisiz uzun zincirler üretmek.",
                [
                    ("A ∧ B, B → C; hedef C", "∧E ile B, ardından →E ile C hedefe doğrudan ilerler."),
                    ("A ↔ B, A; hedef B", "↔E hedefi tek adımda üretir."),
                    ("A; hedef C", "A'dan A ∨ D üretmek lisanslıdır, fakat C için köprü sağlamıyorsa stratejik olarak yararsızdır."),
                ],
                (
                    "Yalnız açık yükle bağlantısı gösterilebilen eleme adımını üretmek.",
                    "Lisanslı olan her satırı yararlı saymak.",
                    "Kural doğruluğu zorunludur; stratejik yararlılık ise doğru kanıtı makul bir aramayla bulmayı sağlar.",
                ),
            ),
            _section(
                "İleri ve geri izi köprüde buluşturmak",
                "Geri planın istediği cümle ile ileri kaynakların üretebildiği cümle aynı olduğunda bir köprü oluşur. İyi ara hedef, elde edilme yolu ve sonraki kullanım yeri birlikte açıklanabilen cümledir.",
                "Ne yalnız hedef analizi ne de yalnız kaynak açılımı kanıtı hemen tamamladığında.",
                "kaynaklar ⟹ köprü 𝒦 ⟹ açık alt hedef ⟹ hedef",
                "Ara hedefin değeri bağımsız olarak ilginç olmasından değil, belirli bir kuralın eksik girdisini sağlamasından gelir.",
                "Hedefte geçen her atomu ara hedef saymak veya üretilebilse bile hiçbir sonraki kuralı açmayan cümleyi seçmek.",
                [
                    ("A → B, B → C ⊢ A → C", "A varsayımından çıkan B, ikinci koşul ile iç hedef C arasında köprüdür."),
                    ("A ∧ B, B → C ⊢ A ∧ C", "İleri elde edilen A ve C, geriye plandaki iki ∧I yükünü kapatır."),
                    ("A ∨ B, A → C, B → C ⊢ C", "Burada köprü tek satır değil, iki kardeş dalda kurulan ortak C'dir."),
                ],
                (
                    "Ara hedef için hem üretim yolunu hem sonraki kullanımını yazmak.",
                    "Sadece hedefte geçen bir sembolü seçmek.",
                    "Köprü iki yönlü bir bağlantıdır: soldan erişilebilir, sağda belirli bir yükü kapatır.",
                ),
            ),
            _section(
                "Satırdan önce kapsam planı kurmak",
                "→I, ¬I, IP, ∨E ve ↔I kullanılacaksa alt kanıtların başlangıçları, beklenen sonları, kardeşlik ilişkileri ve kapanış noktaları önce tasarlanır.",
                "Birden çok alt kanıt açılacaksa veya geçici varsayıma bağımlı sonuçların yanlışlıkla dışarı taşınma riski varsa.",
                "aç: varsayım + kapsam kimliği; içeride: alt hedef; kapat: yalnız uygun giriş/eleme kuralıyla",
                "Kapsam planı, varsayımın doğru olduğunu ileri sürmez; hangi koşullu kanıt yükü için geçici olarak kullanılacağını kaydeder.",
                "İlk dalı kapatmadan kardeş dal açmak, dış sonuç yazılmadan kapsamı terk etmek veya iç satırı doğrudan dışarı yinelemek.",
                [
                    ("A → C hedefi", "A AS ile bir kapsam; son doğrudan satır C; dışarıda →I."),
                    ("A ∨ B kaynağıyla C", "A...C ve B...C aynı parent altında iki kardeş kapsam; dışarıda ∨E."),
                    ("A ↔ B hedefi", "A...B ve B...A iki ayrı kardeş kapsam; dışarıda ↔I."),
                ],
                (
                    "Alt kanıtın başlangıç, son, parent ve boşaltma kuralını önceden yazmak.",
                    "Önce AS satırları açıp ne zaman kapanacağını sonra düşünmek.",
                    "Geçici varsayım bağımlılığı kanıtın mantıksal yapısıdır; sonradan yapılan görsel düzenleme değildir.",
                ),
            ),
            _section(
                "Doğrudan yol ile dolaylı yolu seçmek",
                "Önce hedefin giriş kuralı ve kaynakların eleme olanakları denenir. IP ancak hedefin olumsuzunu varsaymaktan erişilebilir bir 𝒜/¬𝒜 çiftine giden somut bir plan bulunduğunda seçilir.",
                "Doğrudan ileri/geri izler birleşmediğinde ve hedefin tersinin çelişki üreteceği açıkça gösterilebildiğinde.",
                "doğrudan plan yok + ¬hedef ⟹ ... ⊥ planı var ⇒ IP adayı",
                "Dolaylı kanıt başarısızlığın otomatik kaçış kapısı değildir. Patlama da yalnız erişilebilir ⊥ zaten kurulduktan sonra istenen cümleyi verir.",
                "Her atomik hedefte IP açmak, çelişkiyi hangi tam karşıt çiftten üreteceğini bilmeden ¬hedef varsaymak veya X'i ⊥ olmadan kullanmak.",
                [
                    ("A → B, A → ¬B ⊢ ¬A", "Hedef ¬A olduğu için A varsayımı altında B ve ¬B üretmek doğrudan ¬I planıdır."),
                    ("¬¬A ⊢ A", "Doğrudan giriş/eleme yolu yoksa ¬A varsayımı hazır ¬¬A ile ⊥ verir; IP planı somuttur."),
                    ("A → B ⊢ B", "¬B varsayımından çelişkiye götüren yol yoktur; kör IP eksik öncülü yaratmaz."),
                ],
                (
                    "IP seçmeden önce çelişki çiftini ve ona giden satır zincirini yazmak.",
                    "Doğrudan yol hemen görünmüyorsa IP açmak.",
                    "Dolaylı strateji de bütün diğer stratejiler gibi önceden tanımlanmış bir kanıt yükü ister.",
                ),
            ),
            _section(
                "İlk stratejik çıkmazdan onarmak",
                "Başarısız taslak son satırdan geriye rastgele silinmez. Önce hedefe hizmet etmeyen ilk kural, ara hedef, kaynak veya kapsam kararı bulunur; yalnız o karar ve ona bağımlı bölüm yeniden kurulur.",
                "Kanıt uzadığı hâlde açık yük kapanmıyorsa, kapsamlar karıştıysa veya doğru formüller yanlış yönde birikiyorsa.",
                "hedef yükleri → ilk karşılanmayan yük → onu doğuran karar → yerel onarım",
                "İlk lisanssız satır ile ilk stratejik hata aynı olmak zorunda değildir. Bütün satırlar lisanslı olduğu hâlde plan hedefe bağlanmıyorsa stratejik hata daha erkendedir.",
                "Bütün taslağı silmek, yalnız son hata mesajını düzeltmek veya en kısa görünen kanıtı açıklamasız seçmek.",
                [
                    ("A → B, B → C ⊢ A → C; A AS altında yalnız B'ye ulaşıp →I", "Kural hatası son satırdadır; stratejik eksik köprü B'yi ikinci koşulla C'ye bağlamamaktır."),
                    ("Hedef C iken A'dan A ∨ D, sonra (A ∨ D) ∨ E", "Satırlar lisanslı olabilir; ilk stratejik hata hedefle ilgisiz ilk ∨I'dır."),
                    ("∨E'nin ikinci dalı birincinin içinde", "İlk kapsam kararı düzeltilir; ikinci dal kardeş olarak yeniden açılır."),
                ],
                (
                    "İlk çıkmazı türüyle adlandırıp yalnız bağımlı bölümü yeniden kurmak.",
                    "Son satırı değiştirerek bütün planı düzelmiş saymak.",
                    "Yerel onarım, hem hata nedenini görünür tutar hem doğru kalan kanıt emeğini korur.",
                ),
            ),
        ],
        [
            _worked("A → B, B → C ⊢ A → C", "→I geri planı A altında C ister; B iki →E adımı arasında köprüdür.", "İki yönlü arama"),
            _worked("A ∧ B, B → C ⊢ A ∧ C", "∧I iki alt hedef açar; ∧E ile A ve B, ardından →E ile C ileri üretilir.", "Köprü"),
            _worked("A ∨ B, A → C, B → C ⊢ C", "Atomik hedef kaynak ayrıklığına göre iki kardeş C dalıyla kurulur.", "Durum planı"),
            _worked("A → B, A → ¬B ⊢ ¬A", "¬I geri planı A varsayımı altında tam B/¬B çiftini hedefler.", "Çelişki planı"),
            _worked("¬¬A ⊢ A", "Doğrudan kural yoksa ¬A varsayımı hazır ¬¬A ile somut bir IP yolu açar.", "Gerekçeli IP"),
            _worked("A → B ⊢ B için ¬B AS", "¬B'den çelişkiye giden bir yol yoktur; IP yalnız görünmeyen öncülü icat eder.", "Kör IP", "bad"),
            _worked("Hedef C; A'dan A ∨ D, sonra (A ∨ D) ∨ E", "Her satır lisanslı olsa da hiçbir açık yük kapanmadığı için ilk ∨I stratejik çıkmazdır.", "Hedefsiz üretim", "bad"),
            _worked("A → B, B → C ⊢ A → C; alt kanıt A...B", "→I için son cümle C olmalıdır; B köprüde bırakılmıştır.", "Eksik köprü", "bad"),
        ],
        [
            "Ana bağlaçtan çıkan son kural adayını zorunlu son kural sanmak.",
            "Uygulanabilen her eleme veya ∨I adımını hedefle ilişkisine bakmadan üretmek.",
            "Ara hedefin hangi sonraki yükü kapattığını açıklayamamak.",
            "Alt kanıtları başlangıç, son ve parent kapsamı planlamadan açmak.",
            "Atomik hedef veya ilk güçlük karşısında otomatik IP seçmek.",
            "İlk stratejik karar hatalıyken yalnız son hata mesajını yamamak.",
            "Daha kısa kanıtı kapsamı ve gerekçeleri denetlemeden daha doğru saymak.",
        ],
        _practice(
            [
                ("Hedef A ∧ B için ilk geri plan hangisidir?", ["A ve B alt hedeflerini ayırmak", "¬(A ∧ B) varsaymak", "A ∨ B üretmek", "Her öncülü yinelemek"], "A ve B alt hedeflerini ayırmak", "∧I olası son adım olarak iki doğrudan bileşeni ister.", "Temel"),
                ("Hedef A → B hangi kapsam planını düşündürür?", ["A AS altında B", "B AS altında A", "A ve B kardeş dalları", "Hiç alt kanıt yok"], "A AS altında B", "→I önbileşeni varsayıp artbileşeni alt hedef yapar.", "Temel"),
                ("A ∧ B ve B → C kaynaklarıyla C için yararlı ilk ileri adım nedir?", ["∧E ile B", "∨I ile A ∨ D", "IP ile ¬C", "↔I"], "∧E ile B", "B ikinci koşulun önbileşenidir ve →E ile C'yi açar.", "Temel"),
                ("İyi bir köprü ara hedef için hangi iki bilgi gerekir?", ["Nasıl üretileceği ve sonra nerede kullanılacağı", "Yalnız kısa olması", "Hedefteki bütün atomları içermesi", "Bir varsayım olması"], "Nasıl üretileceği ve sonra nerede kullanılacağı", "Köprü ileri ve geri izleri gerçekten bağlamalıdır.", "Temel"),
                ("Atomik hedef C ise ne sonuç çıkar?", ["Kanıt olanaksızdır", "Tek bir giriş kuralı belirlenmez; kaynak analizi gerekir", "Daima IP gerekir", "Daima X gerekir"], "Tek bir giriş kuralı belirlenmez; kaynak analizi gerekir", "Atomik biçim son giriş kuralı sağlamaz.", "Orta"),
                ("∨E planında satır yazmadan önce ne belirlenmelidir?", ["İki ayrılan varsayımı, ortak dal sonucu ve kardeş parent", "Yalnız ilk dal", "Yalnız ayrık satırın numarası", "Bir IP varsayımı"], "İki ayrılan varsayımı, ortak dal sonucu ve kardeş parent", "Durum analizi iki ayrı durumda aynı sonucu güvenceye alır.", "Orta"),
                ("IP ne zaman gerekçeli bir adaydır?", ["Doğrudan plan hemen görünmediğinde otomatik", "Hedefin olumsuzundan somut bir çelişki yolu planlandığında", "Hedef atomik olduğunda", "Her uzun kanıtta"], "Hedefin olumsuzundan somut bir çelişki yolu planlandığında", "Dolaylı kanıt da belirli bir ⊥ üretim yükü gerektirir.", "Orta"),
                ("A → B, B → C ⊢ A → C planında B'nin rolü nedir?", ["Köprü ara hedef", "Son hedef", "Açılacak varsayım", "Çelişki"], "Köprü ara hedef", "A'dan elde edilir ve ikinci koşulla C'ye geçişi açar.", "Orta"),
                ("Lisanslı ama hedefle ilgisiz ilk satır hangi tür sorundur?", ["Yalnız sözdizimi hatası", "Stratejik çıkmazın başlangıcı", "Geçerli son kural", "Semantik karşı örnek"], "Stratejik çıkmazın başlangıcı", "Kural doğru olabilir; yine de hiçbir açık yükü kapatmayabilir.", "İleri"),
                ("Başarısız taslak nasıl onarılmalıdır?", ["Her şeyi silerek", "İlk yanlış stratejik kararı ve bağımlı bölümünü değiştirerek", "Yalnız son satırı gizleyerek", "Yeni bir öncül ekleyerek"], "İlk yanlış stratejik kararı ve bağımlı bölümünü değiştirerek", "Yerel onarım doğru kalan bölümü korur ve nedeni görünür tutar.", "İleri"),
                ("A → B ⊢ B için ¬B varsaymak neden yetmez?", ["¬B atomik olduğu için", "A'yı sağlayan veya çelişki üreten bir yol olmadığı için", "IP hiçbir zaman kullanılamadığı için", "B hedef olamadığı için"], "A'yı sağlayan veya çelişki üreten bir yol olmadığı için", "Varsayım eksik öncülü yaratmaz; somut çelişki zinciri yoktur.", "İleri"),
                ("İki geçerli kanıttan hangisi stratejik olarak daha açıklayıcıdır?", ["Her zaman daha kısa olan", "Her satırın hangi açık yükü kapattığını ve kapsam bağımlılığını görünür kılan", "Daha çok IP kullanan", "Daha çok satır üreten"], "Her satırın hangi açık yükü kapattığını ve kapsam bağımlılığını görünür kılan", "Satır sayısı tek başına doğruluk veya pedagojik açıklık ölçütü değildir.", "Zor"),
            ]
        ),
        {
            "prompt": "A → B, B → C ⊢ A → C problemi için önce yalnız geri hedef, ileri kaynak, köprü ve kapsam planını yaz; sonra kanıtı tamamla.",
            "starter": "Ana hedefin olası son kuralını seç; o kuralın iç hedefini ve A varsayımından üretilebilecek ilk cümleyi ayrı sütunlara yaz.",
            "checks": [
                "Olası son kural →I olarak gerekçelendirildi",
                "A varsayımı altında iç hedef C yazıldı",
                "B'nin A → B ile üretileceği ve B → C'yi açacağı belirtildi",
                "Alt kanıt A ile açılıp C ile kapandı",
                "Son →I tam alt kanıt aralığına atıf yaptı",
            ],
            "solution": "Geri: A → C için →I, dolayısıyla A AS altında C. İleri: A ve A → B ile B; B ve B → C ile C. Köprü B. Fitch: l1 A → B PR; l2 B → C PR; l3 A AS; l4 B →E l1,l3; l5 C →E l2,l4; l6 A → C →I l3-l5.",
        },
        [
            _production_task(
                "Üç problem için kanıt satırı yazmadan strateji kartı hazırla; birini tamamla, birindeki kötü başlangıcı yerel olarak onar.",
                [
                    "Her problem için olası son kuralı veya atomik hedefte kaynak yönünü yaz.",
                    "En az bir ileri kaynak ve varsa köprü ara hedef belirle.",
                    "Alt kanıt gerekiyorsa başlangıç, beklenen son, parent ve kapatma kuralını göster.",
                    "Tamamlanan kanıtta her türetilmiş satırın hangi açık yükü kapattığını not et.",
                    "Hatalı taslakta ilk stratejik çıkmazı ve yalnız değiştirilecek bağımlı bölümü belirt.",
                ],
                "Yanıt, yalnız doğru son kanıtı değil arama kararlarını görünür kılmalı; IP seçildiyse hedefin olumsuzundan tam hangi karşıt çifte ulaşılacağı önceden yazılmalıdır.",
                "Planlanacak problemler",
                [
                    "A → B, B → C ⊢ A → C",
                    "A ∨ B, A → C, B → C ⊢ C",
                    "A → B, A → ¬B ⊢ ¬A",
                    "Onarılacak taslak: A → B, B → C ⊢ A → C; A AS altında B'ye ulaşıp doğrudan →I ile A → C yazıyor.",
                ],
                "İlk problemi tamamla; dördüncü taslakta B'yi silmek yerine köprü olarak kullanıp eksik C satırını ekle.",
            )
        ],
        [
            "Yeni bir bileşik hedef için olası son kuralı ve onun alt hedeflerini gerekçeli biçimde yazar.",
            "Erişilebilir kaynaklardan en az iki hedefle ilişkili eleme adımı seçer ve ilgisiz lisanslı adımı reddeder.",
            "Bir ara hedefin hem üretim yolunu hem hangi sonraki kuralı açtığını gösterir.",
            "Çoklu alt kanıt probleminde kapsam başlangıçlarını, sonlarını ve sibling/parent ilişkisini satırlardan önce planlar.",
            "IP kullanacaksa hedefin olumsuzundan erişilebilir tam karşıt çifte giden somut zinciri açıklar.",
            "Başarısız kanıtta ilk lisanssız satır ile ilk stratejik çıkmazı ayırıp yerel onarım yapar.",
        ],
        [
            "Koşul hedefi hangi son kuralı ve hangi iç hedefi düşündürür?",
            "Ayrık bir erişilebilir satır hangi tür ileri çalışma olanağı verir?",
            "Bir ara hedefin gerçekten köprü olduğunu nasıl anlarsın?",
            "IP açmadan önce hangi çelişki planı yazılmalıdır?",
            "İlk lisanssız satır ile ilk stratejik hata neden farklı olabilir?",
        ],
        "Sonraki derste DS, MT, DNE, LEM ve De Morgan gibi kısaltmaların temel kurallarla açılabilir lisanslı şemalar olduğunu inceleyeceğiz.",
        [
            "forallx-proof-strategies",
            "forallx-basic-rules",
            "carnap-derivations",
            "carnap-feedback",
            "mit-logic-sequence",
        ],
        "Kanıt bulmak için her problemi çözen mekanik bir algoritma vaat edilmez. Hedef yapısı ve erişilebilir kaynaklar aramayı disipline eder; stratejik açıklık kural doğruluğuna eklenir, onun yerine geçmez. D25'e kadar türetilmiş kural ve sessiz eşdeğerlik dönüşümü kullanılmaz.",
        [
            "ders-18-cikarim-kurallari-ii-ve-kisa-ispatlar",
            "ders-25-dogal-turetim-ii",
            "ders-26-reductio-ad-absurdum",
        ],
    )

    lesson["reading_note"] = (
        "Önce hedef sütununu, sonra kaynak sütununu doldur. Bir satırı ancak hangi açık yükü kapattığını söyleyebiliyorsan kanıta ekle; alt kanıt açmadan önce kapanış biçimini yaz."
    )
    lesson["symbol_set"] = [
        "𝒜",
        "ℬ",
        "𝒞",
        "𝒦",
        "⊢",
        "PR",
        "AS",
        "R",
        "∧I/E",
        "→I/E",
        "¬I/E",
        "∨I/E",
        "↔I/E",
        "IP",
        "X",
    ]
    lesson["proof_tools"] = [
        "Geri hedef ağacı",
        "İleri kaynak tablosu",
        "Köprü ara hedef kartı",
        "Kapsam planı",
        "Doğrudan/dolaylı yol kararı",
        "İlk stratejik çıkmaz raporu",
        "Yerel onarım günlüğü",
    ]
    lesson["rule_scope"] = {
        "introduced": [],
        "review_only": [
            "PR",
            "AS",
            "R",
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
        ],
        "locked_until_later": ["DS", "MT", "DNE", "LEM", "DeM"],
    }
    lesson["strategy_cases"] = [
        _strategy_case(
            "d24-conditional-chain-plan",
            "A → B, B → C ⊢ A → C",
            backward_goal="→I adayı: A varsayımı altında C",
            candidate_last_rules=["→I"],
            forward_resources=["A + A → B ile B", "B + B → C ile C"],
            bridge="B",
            scope_plan="s1: A AS ile aç, C ile bitir, →I ile kapat",
            first_action="A → B ve B → C öncüllerini yaz; sonra A için s1 aç",
            rationale="B hem ilk koşulun çıktısı hem ikinci koşulun girdisidir.",
        ),
        _strategy_case(
            "d24-conjunction-plan",
            "A ∧ B, B → C ⊢ A ∧ C",
            backward_goal="∧I adayı: A ve C alt hedefleri",
            candidate_last_rules=["∧I"],
            forward_resources=["A ∧ B ile A", "A ∧ B ile B", "B + B → C ile C"],
            bridge="B",
            scope_plan="Alt kanıt gerekmez",
            first_action="A ∧ B'yi ∧E ile hedef yüklerine yarayan bileşenlerine ayır",
            rationale="A doğrudan bir yükü kapatır; B ise C yüküne giden koşulu açar.",
        ),
        _strategy_case(
            "d24-case-analysis-plan",
            "A ∨ B, A → C, B → C ⊢ C",
            backward_goal="Atomik C için tek giriş kuralı yok; ayrık kaynağı tüket",
            candidate_last_rules=["∨E"],
            forward_resources=["A dalında A → C", "B dalında B → C"],
            bridge="İki kardeş dalın ortak C sonucu",
            scope_plan="s1: A...C; s2: B...C; aynı parent; dışarıda ∨E",
            first_action="Ortak C dal sonunu sabitle, sonra A için ilk kardeş kapsamı aç",
            rationale="Ayrıklığın hangi tarafı doğru olursa olsun C aynı biçimde güvence altındadır.",
        ),
        _strategy_case(
            "d24-negation-plan",
            "A → B, A → ¬B ⊢ ¬A",
            backward_goal="¬I adayı: A varsayımı altında ⊥",
            candidate_last_rules=["¬I"],
            forward_resources=["A + A → B ile B", "A + A → ¬B ile ¬B", "B + ¬B ile ⊥"],
            bridge="Tam B/¬B çifti",
            scope_plan="s1: A AS ile aç, ⊥ ile bitir, ¬I ile kapat",
            first_action="A varsayımını açmadan önce çelişki çiftinin B ve ¬B olacağını yaz",
            rationale="Hedefin olumsuzlama yapısı ve iki koşul aynı varsayım altında somut çelişki yolu verir.",
        ),
        _strategy_case(
            "d24-repair-plan",
            "A → B, B → C ⊢ A → C; taslak A AS altında B'de duruyor",
            backward_goal="→I için alt kanıtın son doğrudan satırı C olmalı",
            candidate_last_rules=["→I"],
            forward_resources=["Mevcut B + B → C ile C"],
            bridge="B zaten doğru kurulmuş köprüdür",
            scope_plan="Mevcut s1'i açık tut, C satırını ekle, sonra kapat",
            first_action="B'yi silme; onu B → C ile kullanan eksik →E satırını ekle",
            rationale="İlk sorun B satırı değil, köprünün hedeflenen C'ye kadar tamamlanmamasıdır.",
        ),
    ]
    lesson["proof_fixtures"] = [
        {
            "id": "d24-complete-conditional-chain",
            "kind": "complete",
            "title": "Geri hedef ile ileri koşul zincirini B köprüsünde buluşturma",
            "strategy_case_id": "d24-conditional-chain-plan",
            "expected_issue_codes": [],
            "proof": {
                "id": "d24-complete-conditional-chain",
                "premises": ["A → B", "B → C"],
                "target": "A → C",
                "lines": [
                    _line("l1", "A → B", "PR"),
                    _line("l2", "B → C", "PR"),
                    _line("l3", "A", "AS", depth=1, opens="s1"),
                    _line("l4", "B", "→E", citations=[_line_ref("l1"), _line_ref("l3")], depth=1),
                    _line("l5", "C", "→E", citations=[_line_ref("l2"), _line_ref("l4")], depth=1),
                    _line("l6", "A → C", "→I", citations=[_subproof_ref("l3", "l5")], closes=["s1"]),
                ],
            },
        },
        {
            "id": "d24-complete-conjunction-bridge",
            "kind": "complete",
            "title": "İki birleşim yükünü ileri kaynaklarla kapatma",
            "strategy_case_id": "d24-conjunction-plan",
            "expected_issue_codes": [],
            "proof": {
                "id": "d24-complete-conjunction-bridge",
                "premises": ["A ∧ B", "B → C"],
                "target": "A ∧ C",
                "lines": [
                    _line("l1", "A ∧ B", "PR"),
                    _line("l2", "B → C", "PR"),
                    _line("l3", "A", "∧E", citations=[_line_ref("l1")]),
                    _line("l4", "B", "∧E", citations=[_line_ref("l1")]),
                    _line("l5", "C", "→E", citations=[_line_ref("l2"), _line_ref("l4")]),
                    _line("l6", "A ∧ C", "∧I", citations=[_line_ref("l3"), _line_ref("l5")]),
                ],
            },
        },
        {
            "id": "d24-complete-negation-plan",
            "kind": "complete",
            "title": "Olumsuz hedefi önceden seçilmiş çelişki çiftine bağlama",
            "strategy_case_id": "d24-negation-plan",
            "expected_issue_codes": [],
            "proof": {
                "id": "d24-complete-negation-plan",
                "premises": ["A → B", "A → ¬B"],
                "target": "¬A",
                "lines": [
                    _line("l1", "A → B", "PR"),
                    _line("l2", "A → ¬B", "PR"),
                    _line("l3", "A", "AS", depth=1, opens="s1"),
                    _line("l4", "B", "→E", citations=[_line_ref("l1"), _line_ref("l3")], depth=1),
                    _line("l5", "¬B", "→E", citations=[_line_ref("l2"), _line_ref("l3")], depth=1),
                    _line("l6", "⊥", "¬E", citations=[_line_ref("l4"), _line_ref("l5")], depth=1),
                    _line("l7", "¬A", "¬I", citations=[_subproof_ref("l3", "l6")], closes=["s1"]),
                ],
            },
        },
        {
            "id": "d24-incomplete-conditional-chain",
            "kind": "incomplete",
            "title": "Doğru köprü kurulmuş ve kapanış bekleyen planlı taslak",
            "strategy_case_id": "d24-conditional-chain-plan",
            "expected_issue_codes": [],
            "next_rule": "s1'i kapatıp l3-l5 aralığıyla →I uygula",
            "proof": {
                "id": "d24-incomplete-conditional-chain",
                "premises": ["A → B", "B → C"],
                "target": "A → C",
                "lines": [
                    _line("l1", "A → B", "PR"),
                    _line("l2", "B → C", "PR"),
                    _line("l3", "A", "AS", depth=1, opens="s1"),
                    _line("l4", "B", "→E", citations=[_line_ref("l1"), _line_ref("l3")], depth=1),
                    _line("l5", "C", "→E", citations=[_line_ref("l2"), _line_ref("l4")], depth=1),
                ],
            },
        },
        {
            "id": "d24-premature-conditional-closure",
            "kind": "error",
            "title": "Köprü B'de durup C'ye ulaşmadan →I uygulama",
            "strategy_case_id": "d24-repair-plan",
            "expected_issue_codes": ["rule.conditional_introduction_mismatch"],
            "repair": "B satırını koru; B → C ve B ile C üret, alt kanıtı C'de bitir.",
            "proof": {
                "id": "d24-premature-conditional-closure",
                "premises": ["A → B", "B → C"],
                "target": "A → C",
                "lines": [
                    _line("l1", "A → B", "PR"),
                    _line("l2", "B → C", "PR"),
                    _line("l3", "A", "AS", depth=1, opens="s1"),
                    _line("l4", "B", "→E", citations=[_line_ref("l1"), _line_ref("l3")], depth=1),
                    _line("l5", "A → C", "→I", citations=[_subproof_ref("l3", "l4")], closes=["s1"]),
                ],
            },
        },
    ]
    return lesson


def _candidate_d25():
    lesson = _lesson(
        "D25",
        "ders-turetilmis-kurallar-ve-esdegerliklerin-lisansi",
        "Türetilmiş Kurallar ve Eşdeğerliklerin Lisansı",
        "DS, MT, DNE, LEM ve De Morgan kurallarını ezberlenmiş kestirmeler olarak değil, temel kurallarla geri açılabilen ve yalnız açık kural etiketiyle kullanılabilen kanıt şemaları olarak uygular.",
        "Kanıt şeması, kural ikamesi ve denetlenebilir kanıt sıkıştırması",
        50,
        [
            "ders-geriye-dogru-planlama-ve-kanit-stratejisi",
            "ders-mantiksal-esdegerlik-ve-tutarlilik",
        ],
        [
            "nd.derived_rule_expand",
            "nd.derived_rule_apply",
            "nd.equivalence_license",
            "nd.proof_compress",
        ],
        [
            "Temel kural, ek kural ve türetilmiş kuralı kanıt sistemindeki işlevlerine göre ayırmak.",
            "DS ve MT'nin her kullanımını temel kurallı bir kanıt şemasıyla ikame etmek.",
            "DNE ve LEM'in bu dersteki klasik doğal türetim sistemine bağımlılığını görünür tutmak.",
            "De Morgan dönüşümlerinin dört izinli yönünü kaynak, sonuç ve kural etiketiyle uygulamak.",
            "Semantik eşdeğerlik ile kanıt içinde dönüşüm yapma lisansını birbirine karıştırmamak.",
            "Kısa kanıtı, gizlediği temel şemayı ve koruduğu kapsam bağımlılıklarını açıklayarak denetlemek.",
        ],
        [
            (
                "Temel kural",
                "Kanıt sisteminin başlangıç kural envanterinde doğrudan lisanslanan ve diğer kuralların açılımında kullanılan kural.",
            ),
            (
                "Türetilmiş kural",
                "Her örneği temel kurallarla aynı öncül ve hedefi koruyan bir kanıt şemasıyla sistematik olarak ikame edilebilen kısaltma.",
            ),
            (
                "Kanıt şeması",
                "𝒜, ℬ gibi üst dil değişkenleriyle yazılan ve yerine uygun TFL cümleleri konduğunda gerçek kanıtlar üreten tarif.",
            ),
            (
                "DS",
                "𝒜 ∨ ℬ ile doğrudan ayrılanlardan birinin olumsuzundan öteki doğrudan ayrılanı çıkaran ayrık tasım kuralı.",
            ),
            (
                "MT",
                "𝒜 → ℬ ile ¬ℬ'den ¬𝒜 çıkaran modus tollens kuralı.",
            ),
            (
                "DNE",
                "¬¬𝒜 biçiminden tam 𝒜 sonucuna geçen çift olumsuzlama giderme kuralı.",
            ),
            (
                "LEM",
                "𝒜 ve ¬𝒜 kardeş durumlarının ikisinde de aynı 𝒞 sonucu kurulunca 𝒞'yi dışarı taşıyan dışlanan orta kuralı.",
            ),
            (
                "DeM",
                "Olumsuzlanmış birleşim/ayrıklık ile bileşenlerin olumsuzlarından kurulan karşılık arasında dört açık yönde dönüşüm lisansı.",
            ),
            (
                "Dönüşüm lisansı",
                "Bir satırın belirli başka bir biçimde yazılmasına bu kanıt sistemi içinde açıkça izin veren kural ve yön.",
            ),
            (
                "Kanıt sıkıştırması",
                "Temel şemayı tek türetilmiş kural satırıyla değiştirirken öncül, hedef ve açık varsayım bağımlılıklarını koruma işlemi.",
            ),
        ],
        [
            _section(
                "Temel kural ile türetilmiş kuralı ayırmak",
                "Türetilmiş kural yeni sonuç üretme gücü eklemez. Onun her doğru kullanımı, aynı açık varsayımlar altında aynı sonuçla biten temel-kural şemasıyla değiştirilebilir.",
                "Bir kısa kuralın neden meşru olduğunu açıklarken veya sistemin çekirdeği ile kullanıcı kolaylıklarını ayırırken.",
                "türetilmiş satır ⇝ aynı öncül/varsayım bağımlılıklarıyla temel-kural bloğu",
                "Şema tek bir somut kanıt değildir; 𝒜 ve ℬ yerine uygun TFL cümleleri konduğunda her kullanım için kanıt üretir. İkame, yalnız son formülü değil kapsam ve açık varsayım yükünü de korur.",
                "Kısa, tanıdık veya semantik olarak geçerli görünen her çıkarımı otomatik kural sayma. Kuralın sistem sözleşmesinde bulunması ve temel açılımının gösterilebilmesi gerekir.",
                [
                    ("A ∨ B, ¬A ⊢ B; tek DS satırı", "Aynı problem ∨E, ¬E, X ve R ile daha uzun kurulabildiği için DS bir kısaltmadır."),
                    ("A → B, ¬B ⊢ ¬A; tek MT satırı", "A varsayımı altında B ve ¬B'den ⊥ üretip ¬I ile kapatılan temel blokla ikame edilir."),
                    ("A → B, B ⊢ A", "Semantik olarak geçersiz bu kalıp için kural listesinde veya temel sistemde bir açılım yoktur."),
                ],
                (
                    "Kısa satırı, aynı öncül ve hedefi koruyan açık temel şemayla ilişkilendirmek.",
                    "Türetilmiş kuralı temel kurallardan daha güçlü saymak.",
                    "İkame edilebilirlik yeni türetilebilir sonuç eklenmediğini; yalnız kanıt yazımının kısaldığını gösterir.",
                ),
            ),
            _section(
                "DS'yi durum analizine geri açmak",
                "DS, bir ayrık cümlenin doğrudan ayrılanlarından biri yadsındığında öteki doğrudan ayrılanı verir. Temel açılımda ∨E'nin iki kardeş dalı aynı sonuçla bitirilir.",
                "Erişilebilir 𝒜 ∨ ℬ ile ¬𝒜'dan ℬ veya ¬ℬ'den 𝒜 hedeflenirken.",
                "𝒜 ∨ ℬ, ¬𝒜 ⟹DS ℬ; açılım: [𝒜...⊥...ℬ] [ℬ...ℬ] ∨E",
                "Olumsuzlanan dalda ¬E ile ⊥, X ile ortak sonuç üretilir. Öteki dal kendi varsayımını R ile ortak sonuç yapar. Dallar kardeştir ve sonuç doğrudan öteki ayrılan olmalıdır.",
                "İç içe bir alt ayrılanı doğrudan ayrılan sanma; ¬𝒜 ile (𝒜 ∧ 𝒞) ∨ ℬ kaynağından DS kullanılamaz.",
                [
                    ("A ∨ B, ¬A ⊢ B", "A dalı çelişki ve X ile B'ye; B dalı R ile B'ye gider, sonra ∨E uygulanır."),
                    ("A ∨ B, ¬B ⊢ A", "DS'nin simetrik biçimidir; yadsınan doğrudan ayrılan B, sonuç A'dır."),
                    ("(A ∧ C) ∨ B, ¬A ⊢ B", "¬A, sol doğrudan ayrılan ¬(A ∧ C) değildir; DS satırı lisanssızdır."),
                ],
                (
                    "Ayrık kaynağı, tam yadsınan ayrılanı ve kalan doğrudan ayrılanı eşleştirmek.",
                    "Ayrılanın yalnız bir parçası yadsındı diye öteki tarafa geçmek.",
                    "DS sözdizimsel olarak doğrudan bileşenlerle çalışır; benzer anlam veya içerme ilişkisi yetmez.",
                ),
            ),
            _section(
                "MT'yi olumsuzlama alt kanıtına geri açmak",
                "MT, koşulun artbileşeninin tam olumsuzundan önbileşenin tam olumsuzunu çıkarır. Temel açılım, önbileşeni varsayıp →E ile artbileşeni ve ¬E ile ⊥'yi üretir.",
                "𝒜 → ℬ ve ¬ℬ erişilebilirken hedef ¬𝒜 olduğunda.",
                "𝒜 → ℬ, ¬ℬ ⟹MT ¬𝒜; açılım: [𝒜 AS, ℬ →E, ⊥ ¬E] ¬I",
                "MT, geçerli karşıt-ters çıkarım şemasıdır. Sonucu onaylama veya önbileşeni yadsıma değildir; artbileşenin olumsuzu tam olarak eşleşmelidir.",
                "𝒜 → ℬ ve ¬𝒜'dan ¬ℬ çıkarma. Bu, MT değil önbileşeni yadsıma safsatasıdır.",
                [
                    ("A → (B ∧ C), ¬(B ∧ C) ⊢ ¬A", "Artbileşenin tam olumsuzu verildiği için bileşik formülle MT uygulanır."),
                    ("A → B, ¬B ⊢ ¬A", "A varsayımı →E ile B, hazır ¬B ile ⊥ ve ¬I ile ¬A verir."),
                    ("A → B, ¬A ⊢ ¬B", "Artbileşen değil önbileşen yadsınmıştır; MT lisansı yoktur."),
                ],
                (
                    "Koşulun sağ tarafını yadsıyan kaynaktan sol tarafın olumsuzuna geçmek.",
                    "Koşulun herhangi bir tarafındaki olumsuzluğu MT saymak.",
                    "MT'nin yönü, → bağlacının önbileşen/artbileşen yapısı tarafından belirlenir.",
                ),
            ),
            _section(
                "DNE ve LEM'de klasik bağımlılığı göstermek",
                "DNE ve bu dersteki LEM kuralı klasik doğal türetimin kısaltmalarıdır. DNE'nin temel açılımı IP kullanır; LEM de klasik dışlanan orta veya onu kuran IP düzenine dayanır.",
                "Çift olumsuzlamayı kaldırırken veya 𝒜/¬𝒜 durumlarının her ikisinden aynı sonucu çıkarırken.",
                "¬¬𝒜 ⟹DNE 𝒜; [𝒜...𝒞] [¬𝒜...𝒞] ⟹LEM 𝒞",
                "DNE'de ¬𝒜 varsayımı hazır ¬¬𝒜 ile ⊥ üretir ve IP hedef 𝒜'yı verir. LEM iki ayrı kardeş kapsam ister; dallar tam karşıt varsayımlarla açılıp aynı doğrudan sonuçla biter.",
                "Klasik sistemde lisanslanan DNE'yi bütün mantık sistemlerinde veya doğal dildeki her çift olumsuz ifadede anlam eşitliği sayma.",
                [
                    ("¬¬A ⊢ A", "¬A varsayımı ve ¬¬A çelişir; IP ile A elde edilir."),
                    ("A → C, ¬A → C ⊢ C", "A ve ¬A kardeş dallarının ikisi de C verdiği için LEM ile C dışarı taşınır."),
                    ("A...C ve ¬B...C dalları", "Başlangıçlar tam karşıt olmadığı için LEM değildir."),
                ],
                (
                    "DNE/LEM kullanırken klasik kural envanterini ve alt kanıt yükünü açıkça belirtmek.",
                    "DNE'yi yalnız iki ¬ işaretini metinden silmek, LEM'i de iki rastgele durum diye kullanmak.",
                    "Kurallar formül yapısı ve sistem seçimine bağlıdır; doğal dil sezgisi tek başına lisans vermez.",
                ),
            ),
            _section(
                "De Morgan'ın dört yönünü açıkça uygulamak",
                "DeM bu derste yalnız iki eşdeğerlik ailesinin iki yönünü lisanslar: olumsuzlanmış birleşim ile olumsuzların ayrıklığı; olumsuzlanmış ayrıklık ile olumsuzların birleşimi.",
                "Kaynak satır bu dört biçimden biriyken karşı biçime tek satırda geçmek için.",
                "¬(𝒜∧ℬ) ⇄ ¬𝒜∨¬ℬ; ¬(𝒜∨ℬ) ⇄ ¬𝒜∧¬ℬ",
                "Ana bağlaç dönüşür ve her doğrudan bileşen olumsuzlanır ya da olumsuzluğu ortak dış olumsuzluğa taşınır. Kaynaktaki sol-sağ sıra korunur; değişme, dağılma veya koşul dönüşümü DeM değildir.",
                "A ∧ B'den B ∧ A'ya, A → B'den ¬A ∨ B'ye veya yalnız bir bileşeni olumsuzlayarak geçme.",
                [
                    ("¬(A ∧ B) ⊢ ¬A ∨ ¬B", "Birinci ileri DeM yönüdür."),
                    ("¬A ∨ ¬B ⊢ ¬(A ∧ B)", "Aynı ailenin ters DeM yönüdür."),
                    ("¬(A ∨ B) ⊢ ¬A ∧ ¬B", "Ayrıklık ailesinin ileri DeM yönüdür."),
                    ("¬A ∧ ¬B ⊢ ¬(A ∨ B)", "Ayrıklık ailesinin ters DeM yönüdür."),
                ],
                (
                    "Kaynak biçimini dört şablondan biriyle eşleştirip yönü kural etiketiyle göstermek.",
                    "Doğruluk tablosunda eşdeğer bulunan her ifadeyi DeM adıyla yeniden yazmak.",
                    "DeM genel eşdeğerlik motoru değil, açıkça sınırlandırılmış dört sözdizimsel dönüşümdür.",
                ),
            ),
            _section(
                "Semantik eşdeğerlikten kanıt lisansına geçiş",
                "C17'de iki cümlenin bütün değerlemelerde aynı değeri aldığı gösterilmiş olabilir. D25'te bir kanıt satırını dönüştürmek için ayrıca bu sistemde kabul edilmiş bir kural ve doğru yön gerekir.",
                "Doğruluk tablosu sonucunu Fitch kanıtında kullanırken veya kısa kanıtın geçerli dönüşüm adımlarını denetlerken.",
                "𝒜 ≡ ℬ semantik bulgusu; 𝒜 ⟹kural ℬ ise kanıt içi lisans",
                "Semantik eşdeğerlik ile karşılıklı türetilebilirlik bu TFL sistemi için yakından ilişkilidir, fakat biri değerlemeler, diğeri lisanslı kanıtlar hakkındadır. Sessiz yeniden yazma denetlenebilir satır yapısını ortadan kaldırır.",
                "Kaynak göstermeden parantez, bağlaç, bileşen sırası veya olumsuzluk değiştirmek; doğru sonuca ulaştığı için ara dönüşümü kabul etmek.",
                [
                    ("¬(A ∨ B) satırından ¬A ∧ ¬B, DeM l1", "Semantik eşdeğerlik açık kanıt lisansıyla kullanılmıştır."),
                    ("A ∧ B satırından B ∧ A, açıklama yok", "Sonuç semantik olarak eşdeğer olsa da bu dersin dönüşüm listesinde sessiz adım lisanssızdır."),
                    ("Uzun DS bloğunu tek DS satırıyla değiştirmek", "Aynı açık kaynaklar ve hedef korunursa denetlenebilir sıkıştırmadır."),
                ],
                (
                    "Her dönüşümde kaynak satırı, kural adı ve doğru yönü görünür yazmak.",
                    "Semantik eşdeğerliği metin düzenleme izni saymak.",
                    "Kanıt sistemi yalnız doğru sonuca değil, sonuca götüren lisansın açık olmasına da ihtiyaç duyar.",
                ),
            ),
        ],
        [
            _worked("A ∨ B, ¬A ⊢ B", "DS tek satırda B verir; temel açılım iki kardeş ∨E dalında B sonucunu kurar.", "DS ve açılım"),
            _worked("A ∨ B, ¬B ⊢ A", "Olumsuzlanan doğrudan ayrılan B olduğundan kalan doğrudan ayrılan A'dır.", "DS simetrisi"),
            _worked("(A ∧ C) ∨ B, ¬A ⊢ B", "¬A sol doğrudan ayrılanın tam olumsuzu değildir; DS kullanılamaz.", "DS sınırı", "bad"),
            _worked("A → B, ¬B ⊢ ¬A", "MT, A varsayımı altında B/¬B çelişkisini ve ¬I kapanışını kısaltır.", "MT ve açılım"),
            _worked("A → B, ¬A ⊢ ¬B", "Önbileşeni yadsıma MT değildir ve hedef lisanslanmaz.", "MT safsatası", "bad"),
            _worked("¬¬A ⊢ A", "DNE, ¬A varsayımıyla kurulan IP bloğunu tek satırda sıkıştırır.", "Klasik DNE"),
            _worked("A → C, ¬A → C ⊢ C", "A ve ¬A kardeş dalları aynı C ile bittiği için LEM uygulanır.", "Klasik LEM"),
            _worked("¬(A ∧ B) ⊢ ¬A ∨ ¬B", "DeM'nin birleşim ailesindeki ileri yönü uygulanır.", "DeM"),
            _worked("¬A ∧ ¬B ⊢ ¬(A ∨ B)", "DeM'nin ayrıklık ailesindeki ters yönü uygulanır.", "DeM ters yön"),
            _worked("A ∧ B ⊢ B ∧ A; sessiz yeniden yazma", "Semantik eşdeğerlik doğru olsa bile listelenmiş kural ve atıf olmadan kanıt satırı lisanssızdır.", "Lisanssız dönüşüm", "bad"),
        ],
        [
            "Türetilmiş kuralı temel kurallardan daha güçlü veya daha doğru saymak.",
            "DS'de doğrudan ayrılan yerine onun içindeki bir bileşenin olumsuzunu kullanmak.",
            "MT ile önbileşeni yadsıma veya sonucu onaylama kalıplarını karıştırmak.",
            "DNE ve LEM'in klasik sistem bağımlılığını gizlemek.",
            "LEM dallarını kardeş açmamak veya farklı sonuçlarla bitirmek.",
            "DeM etiketini değişme, dağılma veya koşul eşdeğerliği için kullanmak.",
            "Semantik eşdeğerlik gördüğünde kaynak ve kural yazmadan satırı değiştirmek.",
            "Kısaltmanın kapsam bağımlılıklarını koruyup korumadığını denetlememek.",
        ],
        _practice(
            [
                ("Türetilmiş kuralı meşru kılan nedir?", ["Kısa görünmesi", "Her kullanımının temel kurallarla sistematik olarak ikame edilebilmesi", "Doğal dilde tanıdık olması", "En az iki öncül istemesi"], "Her kullanımının temel kurallarla sistematik olarak ikame edilebilmesi", "Türetilmişlik bir kanıt şeması ve ikame edilebilirlik iddiasıdır.", "Temel"),
                ("A ∨ B ve ¬A'dan DS ile ne çıkar?", ["A", "B", "¬B", "A ∧ B"], "B", "Olumsuzlanan doğrudan ayrılan A olduğundan öteki doğrudan ayrılan B kalır.", "Temel"),
                ("DS'nin temel açılımındaki son ana kural hangisidir?", ["∨E", "→E", "↔I", "DNE"], "∨E", "İki kardeş ayrılan dalında aynı sonuç kurularak durum analizi tamamlanır.", "Temel"),
                ("A → B ve ¬B'den MT hangi sonucu lisanslar?", ["A", "B", "¬A", "¬¬B"], "¬A", "Artbileşenin olumsuzu önbileşenin olumsuzunu verir.", "Temel"),
                ("MT'nin temel açılımında hangi varsayım açılır?", ["A", "B", "¬A", "¬B"], "A", "A varsayımından B elde edilip hazır ¬B ile çelişki kurulur.", "Orta"),
                ("¬¬(A ∨ B) satırından DNE ile ne çıkar?", ["A ∨ B", "¬A ∨ ¬B", "A ∧ B", "¬(A ∨ B)"], "A ∨ B", "DNE iki dış olumsuzluğu kaldırır ve içteki tam cümleyi korur.", "Orta"),
                ("LEM için iki dal nasıl başlamalıdır?", ["A ve B", "A ve ¬A", "¬A ve ¬B", "A ∨ B ve ¬A"], "A ve ¬A", "Dallar aynı cümlenin tam olumlu ve olumsuz biçimleriyle açılır.", "Orta"),
                ("LEM dallarının son satırları için ne gerekir?", ["Birbirinin olumsuzu olmaları", "Aynı sonuç olmaları", "İkisinin de ⊥ olması", "Birinin öncül olması"], "Aynı sonuç olmaları", "Dışarı taşınan sonuç her iki durumda da doğrudan kurulmalıdır.", "Orta"),
                ("¬(A ∨ B) için doğru DeM sonucu hangisidir?", ["¬A ∨ ¬B", "¬A ∧ ¬B", "A ∧ B", "A → ¬B"], "¬A ∧ ¬B", "Olumsuzlanmış ayrıklık, olumsuzların birleşimine dönüşür.", "Orta"),
                ("¬A ∨ ¬B kaynağından DeM ile hangisi çıkar?", ["¬(A ∧ B)", "¬(A ∨ B)", "A ∨ B", "A ∧ B"], "¬(A ∧ B)", "Bu, birleşim ailesinin ters DeM yönüdür.", "İleri"),
                ("A ∧ B'nin B ∧ A ile semantik eşdeğerliği bu derste ne sağlar?", ["Sessiz yeniden yazma izni", "Tek başına hiçbir kanıt satırı lisansı sağlamaz", "Daima DeM kullanımı", "PR etiketi kullanımı"], "Tek başına hiçbir kanıt satırı lisansı sağlamaz", "Kanıt içinde ayrıca sistemde açık bir kural ve kaynak atfı gerekir.", "İleri"),
                ("DNE neden sistem bağımlılığı notuyla öğretilir?", ["Yalnız atomlarda çalıştığı için", "Temel açılımı bu sistemde klasik IP kullandığı için", "İki öncül istediği için", "Semantik olarak geçersiz olduğu için"], "Temel açılımı bu sistemde klasik IP kullandığı için", "Kural klasik doğal türetim envanteri içinde lisanslanır; bütün mantık sistemlerine sessizce taşınmaz.", "Zor"),
            ]
        ),
        {
            "prompt": "A ∨ B, ¬A ⊢ B problemini önce yalnız temel kurallarla, sonra tek DS satırıyla çöz; iki sürümün açık kaynaklarını ve hedefini karşılaştır.",
            "starter": "Uzun sürümde A ve B için kardeş dallar aç. Kısa sürümde ayrık satır ile tam ¬A satırını DS kaynağı yap.",
            "checks": [
                "Temel sürümde A ve B dalları aynı parent altında açıldı",
                "A dalında ¬E ile ⊥ ve X ile B üretildi",
                "B dalında R ile B korundu",
                "∨E bir ayrık satır ve iki tam alt kanıt aralığına atıf yaptı",
                "Kısa sürüm aynı iki açık kaynaktan aynı B hedefini DS ile üretti",
                "Kısaltmanın yeni bir öncül veya açık varsayım eklemediği açıklandı",
            ],
            "solution": "Temel: l1 A ∨ B PR; l2 ¬A PR; l3 A AS; l4 ⊥ ¬E l2,l3; l5 B X l4; l6 B AS; l7 B R l6; l8 B ∨E l1,l3-l5,l6-l7. Kısa: l1 A ∨ B PR; l2 ¬A PR; l3 B DS l1,l2.",
        },
        [
            _production_task(
                "İki kanıtı önce temel kurallarla, sonra lisanslı türetilmiş kurallarla yaz; her kısa satırın gizlediği temel bloğu ve varsa klasik bağımlılığı ekle.",
                [
                    "A ∨ B, ¬A ⊢ B için uzun ∨E açılımını ve kısa DS sürümünü ver.",
                    "A → B, ¬B ⊢ ¬A için uzun ¬I açılımını ve kısa MT sürümünü ver.",
                    "En az bir DNE veya LEM kullanımında klasik IP/dışlanan orta bağımlılığını açıkla.",
                    "Bir DeM dönüşümünde kaynak satırı, yönü ve tam sonucu göster.",
                    "Her sıkıştırmada öncül, hedef ve açık varsayım bağımlılıklarının korunduğunu denetle.",
                    "Semantik olarak eşdeğer fakat bu görevde lisanssız bir sessiz dönüşüm örneğini reddet.",
                ],
                "Değerlendirme yalnız kısa sonuca bakmaz; temel sürüm, kısa sürüm ve aralarındaki ikame gerekçesi birlikte incelenir.",
                "Kanıt çiftleri",
                [
                    "A ∨ B, ¬A ⊢ B",
                    "A → B, ¬B ⊢ ¬A",
                    "¬¬(C ∨ D) ⊢ C ∨ D",
                    "¬(E ∨ F) ⊢ ¬E ∧ ¬F",
                ],
                "DS ve MT zorunlu karşılaştırmalardır; DNE ile DeM'den en az biri ayrıca tamamlanmalıdır.",
            )
        ],
        [
            "Temel ve türetilmiş kuralı yeni mantıksal güç iddiasına başvurmadan doğru ayırır.",
            "DS ve MT için aynı öncül/hedefi koruyan temel-kural açılımlarını eksiksiz kurar.",
            "DNE veya LEM kullanımının klasik sistem bağımlılığını doğru adlandırır.",
            "DeM'nin dört yönünden en az ikisini doğru kaynak, yön ve atıfla uygular.",
            "Semantik eşdeğerlik ile kanıt içi dönüşüm lisansını ayırır ve sessiz adımı reddeder.",
            "Kanıt sıkıştırmasında kapsam ve açık varsayım bağımlılıklarının korunduğunu denetler.",
        ],
        [
            "Türetilmiş kural neden yeni türetilebilir sonuç eklemez?",
            "DS'nin temel açılımında iki kardeş dal nasıl aynı sonuca ulaşır?",
            "MT ile önbileşeni yadsıma arasındaki yapısal fark nedir?",
            "DNE ve LEM neden klasik sistem notuyla birlikte okunmalıdır?",
            "Semantik eşdeğerlik neden tek başına satır yeniden yazma lisansı değildir?",
        ],
        "Sonraki derste ⊢ ile ⊨ arasındaki farkı, güvenirlik ve tamlığın yönlerini ve aynı argümanın kanıt/semantik yöntemlerle bağımsız çapraz doğrulanmasını kuracağız.",
        [
            "forallx-basic-rules",
            "forallx-proof-strategies",
            "forallx-additional-rules",
            "forallx-derived-rules",
            "carnap-derivations",
        ],
        "Bu derste DS, MT, DNE, LEM ve dört DeM yönü açıkça lisanslanır. DNE ve LEM, seçilen klasik TFL doğal türetim sistemi içinde değerlendirilir. C17'deki semantik eşdeğerlikler kendiliğinden Fitch yeniden yazma kuralına dönüşmez; her kanıt dönüşümü etkin kural envanterine ve açık atfa dayanır.",
        [
            "ders-18-cikarim-kurallari-ii-ve-kisa-ispatlar",
            "ders-25-dogal-turetim-ii",
            "ders-26-reductio-ad-absurdum",
        ],
    )

    lesson["reading_note"] = (
        "Önce kısa kuralın kaynak ve sonucunu eşleştir; sonra aynı adımı temel kurallarla açabildiğini kontrol et. Eşdeğer bir cümle görmen yetmez: kanıt satırında dönüşüm kuralını ve yönünü açıkça yaz."
    )
    lesson["symbol_set"] = [
        "𝒜",
        "ℬ",
        "𝒞",
        "⊢",
        "DS",
        "MT",
        "DNE",
        "LEM",
        "DeM",
        "⇝",
        "¬",
        "∧",
        "∨",
        "→",
        "⊥",
    ]
    lesson["proof_tools"] = [
        "Temel/türetilmiş kural sınıflandırıcısı",
        "Kısa satır kaynak eşleştiricisi",
        "Temel-kural açılım kartı",
        "Klasik bağımlılık etiketi",
        "De Morgan dört yön tablosu",
        "Sessiz dönüşüm denetimi",
        "Kapsam koruyan sıkıştırma karşılaştırıcısı",
    ]
    lesson["rule_scope"] = {
        "introduced": ["DS", "MT", "DNE", "LEM", "DeM"],
        "review_only": [
            "PR",
            "AS",
            "R",
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
        ],
        "locked_until_later": [],
    }
    lesson["derived_rule_expansions"] = [
        {
            "rule": "DS",
            "problem": "A ∨ B, ¬A ⊢ B",
            "short_steps": ["A ∨ B", "¬A", "B DS"],
            "basic_rules": ["AS", "¬E", "X", "R", "∨E"],
            "preserves": ["premises", "target", "open assumptions"],
            "classical_dependency": False,
        },
        {
            "rule": "MT",
            "problem": "A → B, ¬B ⊢ ¬A",
            "short_steps": ["A → B", "¬B", "¬A MT"],
            "basic_rules": ["AS", "→E", "¬E", "¬I"],
            "preserves": ["premises", "target", "open assumptions"],
            "classical_dependency": False,
        },
        {
            "rule": "DNE",
            "problem": "¬¬A ⊢ A",
            "short_steps": ["¬¬A", "A DNE"],
            "basic_rules": ["AS", "¬E", "IP"],
            "preserves": ["premises", "target", "open assumptions"],
            "classical_dependency": True,
        },
    ]
    lesson["proof_fixtures"] = [
        {
            "id": "d25-complete-ds-short",
            "kind": "complete",
            "title": "DS ile kısa ayrık tasım",
            "expected_issue_codes": [],
            "proof": {
                "id": "d25-complete-ds-short",
                "premises": ["A ∨ B", "¬A"],
                "target": "B",
                "lines": [
                    _line("l1", "A ∨ B", "PR"),
                    _line("l2", "¬A", "PR"),
                    _line("l3", "B", "DS", citations=[_line_ref("l1"), _line_ref("l2")]),
                ],
            },
        },
        {
            "id": "d25-complete-ds-expanded",
            "kind": "complete",
            "title": "DS'nin temel-kural açılımı",
            "expected_issue_codes": [],
            "proof": {
                "id": "d25-complete-ds-expanded",
                "premises": ["A ∨ B", "¬A"],
                "target": "B",
                "lines": [
                    _line("l1", "A ∨ B", "PR"),
                    _line("l2", "¬A", "PR"),
                    _line("l3", "A", "AS", depth=1, opens="s1"),
                    _line("l4", "⊥", "¬E", citations=[_line_ref("l2"), _line_ref("l3")], depth=1),
                    _line("l5", "B", "X", citations=[_line_ref("l4")], depth=1),
                    _line("l6", "B", "AS", depth=1, opens="s2", closes=["s1"]),
                    _line("l7", "B", "R", citations=[_line_ref("l6")], depth=1),
                    _line(
                        "l8",
                        "B",
                        "∨E",
                        citations=[_line_ref("l1"), _subproof_ref("l3", "l5"), _subproof_ref("l6", "l7")],
                        closes=["s2"],
                    ),
                ],
            },
        },
        {
            "id": "d25-complete-mt-short",
            "kind": "complete",
            "title": "MT ile kısa karşıt-ters çıkarım",
            "expected_issue_codes": [],
            "proof": {
                "id": "d25-complete-mt-short",
                "premises": ["A → B", "¬B"],
                "target": "¬A",
                "lines": [
                    _line("l1", "A → B", "PR"),
                    _line("l2", "¬B", "PR"),
                    _line("l3", "¬A", "MT", citations=[_line_ref("l1"), _line_ref("l2")]),
                ],
            },
        },
        {
            "id": "d25-complete-mt-expanded",
            "kind": "complete",
            "title": "MT'nin temel-kural açılımı",
            "expected_issue_codes": [],
            "proof": {
                "id": "d25-complete-mt-expanded",
                "premises": ["A → B", "¬B"],
                "target": "¬A",
                "lines": [
                    _line("l1", "A → B", "PR"),
                    _line("l2", "¬B", "PR"),
                    _line("l3", "A", "AS", depth=1, opens="s1"),
                    _line("l4", "B", "→E", citations=[_line_ref("l1"), _line_ref("l3")], depth=1),
                    _line("l5", "⊥", "¬E", citations=[_line_ref("l2"), _line_ref("l4")], depth=1),
                    _line("l6", "¬A", "¬I", citations=[_subproof_ref("l3", "l5")], closes=["s1"]),
                ],
            },
        },
        {
            "id": "d25-complete-dne-short",
            "kind": "complete",
            "title": "DNE ile çift olumsuzlama giderme",
            "expected_issue_codes": [],
            "proof": {
                "id": "d25-complete-dne-short",
                "premises": ["¬¬A"],
                "target": "A",
                "lines": [
                    _line("l1", "¬¬A", "PR"),
                    _line("l2", "A", "DNE", citations=[_line_ref("l1")]),
                ],
            },
        },
        {
            "id": "d25-complete-dne-expanded",
            "kind": "complete",
            "title": "DNE'nin klasik IP açılımı",
            "expected_issue_codes": [],
            "proof": {
                "id": "d25-complete-dne-expanded",
                "premises": ["¬¬A"],
                "target": "A",
                "lines": [
                    _line("l1", "¬¬A", "PR"),
                    _line("l2", "¬A", "AS", depth=1, opens="s1"),
                    _line("l3", "⊥", "¬E", citations=[_line_ref("l1"), _line_ref("l2")], depth=1),
                    _line("l4", "A", "IP", citations=[_subproof_ref("l2", "l3")], closes=["s1"]),
                ],
            },
        },
        {
            "id": "d25-complete-lem",
            "kind": "complete",
            "title": "Tam karşıt kardeş dallarla LEM",
            "expected_issue_codes": [],
            "proof": {
                "id": "d25-complete-lem",
                "premises": ["A → C", "¬A → C"],
                "target": "C",
                "lines": [
                    _line("l1", "A → C", "PR"),
                    _line("l2", "¬A → C", "PR"),
                    _line("l3", "A", "AS", depth=1, opens="s1"),
                    _line("l4", "C", "→E", citations=[_line_ref("l1"), _line_ref("l3")], depth=1),
                    _line("l5", "¬A", "AS", depth=1, opens="s2", closes=["s1"]),
                    _line("l6", "C", "→E", citations=[_line_ref("l2"), _line_ref("l5")], depth=1),
                    _line("l7", "C", "LEM", citations=[_subproof_ref("l3", "l4"), _subproof_ref("l5", "l6")], closes=["s2"]),
                ],
            },
        },
        {
            "id": "d25-complete-dem-conjunction",
            "kind": "complete",
            "title": "Birleşim ailesinde ileri De Morgan",
            "expected_issue_codes": [],
            "proof": {
                "id": "d25-complete-dem-conjunction",
                "premises": ["¬(A ∧ B)"],
                "target": "¬A ∨ ¬B",
                "lines": [
                    _line("l1", "¬(A ∧ B)", "PR"),
                    _line("l2", "¬A ∨ ¬B", "DeM", citations=[_line_ref("l1")]),
                ],
            },
        },
        {
            "id": "d25-complete-dem-disjunction-reverse",
            "kind": "complete",
            "title": "Ayrıklık ailesinde ters De Morgan",
            "expected_issue_codes": [],
            "proof": {
                "id": "d25-complete-dem-disjunction-reverse",
                "premises": ["¬A ∧ ¬B"],
                "target": "¬(A ∨ B)",
                "lines": [
                    _line("l1", "¬A ∧ ¬B", "PR"),
                    _line("l2", "¬(A ∨ B)", "DeM", citations=[_line_ref("l1")]),
                ],
            },
        },
        {
            "id": "d25-incomplete-lem-second-branch",
            "kind": "incomplete",
            "title": "İki dalı tamamlanmış ve LEM kapanışı bekleyen taslak",
            "expected_issue_codes": [],
            "next_rule": "s2'yi kapatıp l3-l4 ile l5-l6 aralıklarından LEM ile C yaz",
            "proof": {
                "id": "d25-incomplete-lem-second-branch",
                "premises": ["A → C", "¬A → C"],
                "target": "C",
                "lines": [
                    _line("l1", "A → C", "PR"),
                    _line("l2", "¬A → C", "PR"),
                    _line("l3", "A", "AS", depth=1, opens="s1"),
                    _line("l4", "C", "→E", citations=[_line_ref("l1"), _line_ref("l3")], depth=1),
                    _line("l5", "¬A", "AS", depth=1, opens="s2", closes=["s1"]),
                    _line("l6", "C", "→E", citations=[_line_ref("l2"), _line_ref("l5")], depth=1),
                ],
            },
        },
        {
            "id": "d25-error-silent-commutation-as-dem",
            "kind": "error",
            "title": "DeM etiketiyle gizlenen değişme dönüşümü",
            "expected_issue_codes": ["rule.de_morgan_mismatch"],
            "repair": "Bu derste A ∧ B'den B ∧ A'ya sessiz veya DeM etiketli geçme; sonucu temel ∧E ve ∧I adımlarıyla kur.",
            "proof": {
                "id": "d25-error-silent-commutation-as-dem",
                "premises": ["A ∧ B"],
                "target": "B ∧ A",
                "lines": [
                    _line("l1", "A ∧ B", "PR"),
                    _line("l2", "B ∧ A", "DeM", citations=[_line_ref("l1")]),
                ],
            },
        },
    ]
    return lesson


STAGE_D_CANDIDATE_LESSONS = [
    _candidate_d20(),
    _candidate_d21(),
    _candidate_d22(),
    _candidate_d23(),
    _candidate_d24(),
    _candidate_d25(),
]

STAGE_D_CANDIDATE_MAP = {
    lesson["slug"]: lesson
    for lesson in STAGE_D_CANDIDATE_LESSONS
}
