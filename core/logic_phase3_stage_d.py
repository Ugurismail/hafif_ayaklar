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


def _subproof_ref(start_id, end_id):
    return {"kind": "subproof", "start": start_id, "end": end_id}


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


STAGE_D_CANDIDATE_LESSONS = [
    _candidate_d20(),
    _candidate_d21(),
    _candidate_d22(),
]

STAGE_D_CANDIDATE_MAP = {
    lesson["slug"]: lesson
    for lesson in STAGE_D_CANDIDATE_LESSONS
}
