"""Curriculum structure and validation for the logic course.

The lesson content still lives in ``logic_course_data.py``.  This module keeps
the pedagogical structure separate so that lessons cannot silently drift out
of a stage or appear twice in the course.
"""

from copy import deepcopy


LOGIC_CURRICULUM_VERSION = "2026.1"
LOGIC_MASTERY_THRESHOLD = 70


LOGIC_CURRICULUM_SOURCES = [
    {
        "id": "forallx",
        "title": "forall x: Calgary",
        "publisher": "Open Logic Project",
        "url": "https://forallx.openlogicproject.org/",
        "role": "Önerme ve yüklem mantığı, doğruluk tabloları, modeller ve Fitch tarzı doğal türetim omurgası.",
    },
    {
        "id": "mit-logic-i",
        "title": "Logic I",
        "publisher": "MIT OpenCourseWare",
        "url": "https://ocw.mit.edu/courses/24-241-logic-i-fall-2009/",
        "role": "Geçerlilik ve sağlamlıktan önerme/yüklem mantığına, ardından güvenirlik ve tamlığa ilerleyen ders kapsamı.",
    },
    {
        "id": "carnap",
        "title": "Carnap",
        "publisher": "Carnap Project",
        "url": "https://carnap.io/about",
        "role": "Sembolleştirme, doğruluk tablosu ve doğal türetimde anlık geri bildirim veren etkileşimli alıştırma modeli.",
    },
    {
        "id": "slc",
        "title": "Sets, Logic, Computation",
        "publisher": "Open Logic Project",
        "url": "https://slc.openlogicproject.org/",
        "role": "Metateori, hesaplanabilirlik ve karar verilemezlik için lisans düzeyi ileri rota.",
    },
]


LOGIC_CURRICULUM_STAGES = [
    {
        "id": "akil-yurutme",
        "number": 1,
        "title": "Akıl Yürütmenin Temelleri",
        "short_title": "Temeller",
        "track": "core",
        "estimated_weeks": "1-2 hafta",
        "summary": "Önerme, argüman, geçerlilik, koşullar ve karşı örnek üzerinden iyi akıl yürütmenin iskeletini kur.",
        "outcomes": [
            "Bir metinde öncül, ara sonuç ve ana sonucu ayırt etmek.",
            "Doğruluk, geçerlilik ve sağlamlığı birbirine karıştırmamak.",
            "Zorunlu ve yeterli koşulların yönünü doğru okumak.",
            "Evrensel bir iddiayı uygun karşı örnekle sınamak.",
        ],
        "checkpoint": "Kısa bir metnin argüman şemasını çıkar ve geçerlilik iddiasını gerekçelendir.",
        "lesson_slugs": [
            "ders-1-onerme-nedir",
            "ders-2-arguman-oncul-ve-sonuc",
            "ders-3-gecerlilik-ve-dogruluk",
            "ders-4-mantik-baglaclari",
            "ders-5-zorunlu-ve-yeterli-kosul",
            "ders-6-gecerli-kaliplar-ve-yon-hatalari",
            "ders-7-metin-icinde-arguman-ayiklama",
            "ders-9-karsi-ornek-sema-ve-curutme-teknikleri",
            "ders-10-tanim-ve-kavramsal-cerceve",
        ],
        "source_ids": ["forallx", "mit-logic-i"],
    },
    {
        "id": "arguman-cozumleme",
        "number": 2,
        "title": "Argüman Çözümleme Atölyesi",
        "short_title": "Çözümleme",
        "track": "core",
        "estimated_weeks": "1 hafta",
        "summary": "Safsata adlarını ezberlemek yerine gerçek metinlerde ilgililik, destek ve nedensellik kusurlarını teşhis et.",
        "outcomes": [
            "Kişiye saldırı ile tezin eleştirisini ayırmak.",
            "Yanlış ikilem, kaygan zemin ve saman adamın bozduğu çıkarım bağını göstermek.",
            "Korelasyon ile nedensellik arasındaki farkı açıklamak.",
            "Bir safsata etiketini, metindeki somut hata ile gerekçelendirmek.",
        ],
        "checkpoint": "Gerçek bir paragrafı yeniden kur; hata varsa yerini göster ve daha güçlü hâlini yaz.",
        "lesson_slugs": [
            "ders-12-ad-hominem-ve-otoriteye-basvuru",
            "ders-13-yanlis-ikilem-ve-kaygan-zemin",
            "ders-14-dongusel-gerekce-ve-saman-adam",
            "ders-15-neden-sonuc-karisikliklari",
            "ders-16-safsata-atolyesi-ve-yogun-vaka-analizi",
        ],
        "source_ids": ["forallx"],
    },
    {
        "id": "onermeler-mantigi",
        "number": 3,
        "title": "Önermeler Mantığı: Dil ve Semantik",
        "short_title": "Önermeler Mantığı",
        "track": "core",
        "estimated_weeks": "2-3 hafta",
        "summary": "Doğal dili biçimsel dile çevir; formülleri doğruluk tabloları ve eşdeğerlikler yoluyla semantik olarak çözümle.",
        "outcomes": [
            "Bir cümlenin ana bağlacını ve doğru parantez yapısını belirlemek.",
            "Doğal dil cümlelerini tutarlı bir sembol anahtarıyla çevirmek.",
            "Doğruluk tablosuyla totoloji, çelişki, olumsallık ve geçerliliği sınamak.",
            "Eşdeğerlik dönüşümlerini anlamı koruyarak uygulamak.",
        ],
        "checkpoint": "Bir argümanı sembolleştir, tam doğruluk tablosunu kur ve geçerlilik kararını karşı satırla açıkla.",
        "lesson_slugs": [
            "ders-17-sembollestirmeye-giris",
            "ders-18-degil-ve-ve-baglaclari",
            "ders-19-veya-ve-ise",
            "ders-20-dogruluk-tablolari-i",
            "ders-21-dogruluk-tablolari-ii-ve-gecerlilik",
            "ders-22-esdegerlik-kurallari-i",
            "ders-23-esdegerlik-kurallari-ii",
        ],
        "source_ids": ["forallx", "mit-logic-i", "carnap"],
    },
    {
        "id": "kanit-ve-sonuc",
        "number": 4,
        "title": "Kanıt, Türetim ve Mantıksal Sonuç",
        "short_title": "Kanıt",
        "track": "core",
        "estimated_weeks": "2 hafta",
        "summary": "Çıkarım kalıplarından Fitch tarzı doğal türetime geç; sentaktik kanıt ile semantik geçerliliğin ilişkisini kur.",
        "outcomes": [
            "Giriş ve çıkış kurallarının hangi hedeflerde kullanılacağını seçmek.",
            "Alt kanıt, varsayım boşaltma ve reductio adımlarını gerekçelendirmek.",
            "Kısa bir doğal türetim kanıtını satır satır kurmak.",
            "Açık doğruluk ağacından karşı model okumak.",
        ],
        "checkpoint": "Aynı sonucu hem doğal türetimle kanıtla hem de doğruluk ağacı açısından yorumla.",
        "lesson_slugs": [
            "ders-24-cikarim-kurallari-i",
            "ders-25-cikarim-kurallari-ii-ve-kisa-ispatlar",
            "ders-34-dogal-turetim-i",
            "ders-35-dogal-turetim-ii",
            "ders-37-dogruluk-agaclari-ve-meta-teori",
        ],
        "source_ids": ["forallx", "mit-logic-i", "carnap"],
    },
    {
        "id": "yuklem-mantigi",
        "number": 5,
        "title": "Yüklem Mantığı: Niceleme, Modeller ve Kanıt",
        "short_title": "Yüklem Mantığı",
        "track": "core",
        "estimated_weeks": "3-4 hafta",
        "summary": "Nesneler, özellikler ve bağıntılar hakkında konuşan dili niceleyiciler, modeller, kimlik ve doğal türetimle yönet.",
        "outcomes": [
            "Tümel ve varoluşsal niceleyicilerin kapsamını doğru belirlemek.",
            "Çoklu niceleme sırasının anlamı nasıl değiştirdiğini modelle göstermek.",
            "Doğal dil cümlelerini kimlik ve bağıntılarla yüklem mantığına çevirmek.",
            "Yüklem mantığında yorum, karşı model ve doğal türetim kullanmak.",
        ],
        "checkpoint": "Niceleyici kapsamı içeren bir argümanı çevir, modelle sınayıp uygun türetim adımlarını kur.",
        "lesson_slugs": [
            "ders-26-niceleyicilere-giris",
            "ders-27-niceleyici-olumsuzlamalari",
            "ders-28-coklu-niceleyici-ve-kapsam",
            "ders-29-kimlik-yuklemler-ve-alan",
            "ders-30-dogal-dilden-sembole-i",
            "ders-31-dogal-dilden-sembole-ii",
            "ders-32-bicimsel-sozdizim",
            "ders-33-semantik-ve-modeller",
            "ders-36-yuklem-mantiginda-turetim",
            "ders-38-identity-rules-ve-esitlik",
            "ders-39-function-symbols-ve-terimler",
            "ders-40-prenex-normal-form",
            "ders-41-definite-descriptions",
        ],
        "source_ids": ["forallx", "mit-logic-i", "carnap"],
    },
    {
        "id": "ileri-mantik",
        "number": 6,
        "title": "İleri Mantık, Metateori ve Felsefi Sınırlar",
        "short_title": "İleri Rota",
        "track": "advanced",
        "estimated_weeks": "Seçmeli rota",
        "summary": "Aksiyomatik sistemleri, metateoremleri ve biçimsel yöntemin felsefi sınırlarını çekirdek yeterlikten sonra incele.",
        "outcomes": [
            "Aksiyom, teorem, lemma ve türetilmiş kuralı ayırmak.",
            "Güvenirlik, tamlık, kompaktlık ve karar verilebilirliğin yönünü doğru okumak.",
            "Doğal türetim ile Hilbert tarzı sistemlerin mimarisini karşılaştırmak.",
            "Biçimsel gösterim ile kullanım/anlam sorunları arasındaki felsefi gerilimi açıklamak.",
        ],
        "checkpoint": "Bir biçimsel sistemin neyi kanıtladığını, neyi semantik olarak güvenceye aldığını ve sınırlarını ayrı ayrı açıkla.",
        "lesson_slugs": [
            "ders-43-aksiyomatik-sistem-i",
            "ders-44-aksiyomatik-sistem-ii",
            "ders-45-yuklem-mantiginda-aksiyomlar",
            "ders-46-metateoremler-ve-sinirlar",
            "ders-47-teoremler-ve-derived-rules",
            "ders-42-wittgenstein-koprusu",
        ],
        "source_ids": ["forallx", "slc"],
    },
]


LOGIC_PATHWAYS = [
    {
        "id": "baslangic",
        "title": "Başlangıç rotası",
        "description": "Gündelik metinlerde argüman kurmak ve çözümlemek isteyenler için ilk iki aşama.",
        "stage_ids": ["akil-yurutme", "arguman-cozumleme"],
    },
    {
        "id": "bicimsel-cekirdek",
        "title": "Biçimsel mantık çekirdeği",
        "description": "Önerme mantığı, doğal türetim ve yüklem mantığında lisans düzeyi temel yeterlik.",
        "stage_ids": ["onermeler-mantigi", "kanit-ve-sonuc", "yuklem-mantigi"],
    },
    {
        "id": "ileri",
        "title": "İleri rota",
        "description": "Çekirdek tamamlandıktan sonra aksiyomatik sistemler, metateori ve mantık felsefesi.",
        "stage_ids": ["ileri-mantik"],
    },
]


def build_logic_curriculum(visible_lessons):
    """Return validated stages and lessons in pedagogical order."""

    lesson_map = {lesson["slug"]: lesson for lesson in visible_lessons}
    configured_slugs = [
        slug
        for stage in LOGIC_CURRICULUM_STAGES
        for slug in stage["lesson_slugs"]
    ]

    duplicates = sorted({slug for slug in configured_slugs if configured_slugs.count(slug) > 1})
    missing = sorted(set(lesson_map) - set(configured_slugs))
    unknown = sorted(set(configured_slugs) - set(lesson_map))
    if duplicates or missing or unknown:
        raise ValueError(
            "Mantık müfredatı tutarsız: "
            f"tekrar={duplicates}, eksik={missing}, bilinmeyen={unknown}"
        )

    ordered_lessons = []
    stages = []
    display_order = 0

    for stage in LOGIC_CURRICULUM_STAGES:
        stage_payload = deepcopy(stage)
        stage_lessons = []

        for stage_index, slug in enumerate(stage["lesson_slugs"], start=1):
            display_order += 1
            lesson_payload = deepcopy(lesson_map[slug])
            lesson_payload.update(
                {
                    "display_order": display_order,
                    "stage_id": stage["id"],
                    "stage_number": stage["number"],
                    "stage_title": stage["title"],
                    "stage_short_title": stage["short_title"],
                    "stage_lesson_order": stage_index,
                    "track": stage["track"],
                    "is_advanced": stage["track"] == "advanced",
                }
            )
            stage_lessons.append(lesson_payload)
            ordered_lessons.append(lesson_payload)

        stage_payload["lessons"] = stage_lessons
        stage_payload["lesson_count"] = len(stage_lessons)
        stages.append(stage_payload)

    return stages, ordered_lessons


def get_logic_pathways(stages):
    stage_map = {stage["id"]: stage for stage in stages}
    pathways = []
    for pathway in LOGIC_PATHWAYS:
        payload = deepcopy(pathway)
        payload["lesson_count"] = sum(
            stage_map[stage_id]["lesson_count"] for stage_id in pathway["stage_ids"]
        )
        payload["stage_count"] = len(pathway["stage_ids"])
        pathways.append(payload)
    return pathways
