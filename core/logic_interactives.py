"""Curriculum-bound interactive exercises for logic lessons."""

from copy import deepcopy


LOGIC_INTERACTIVES = {
    "ders-17-sembollestirmeye-giris": {
        "type": "symbolization",
        "title": "Cümleden mantıksal biçime",
        "description": "Sembol anahtarını kullan, parçaları doğru sırayla birleştir ve kapsamı görünür kıl.",
        "tokens": ["p", "q", "r", "¬", "∧", "∨", "→", "(", ")"],
        "tasks": [
            {
                "statement": "Yağmur yağıyor ve hava soğuk.",
                "key": [
                    {"symbol": "p", "meaning": "Yağmur yağıyor."},
                    {"symbol": "q", "meaning": "Hava soğuk."},
                ],
                "answers": [["p", "∧", "q"]],
                "hint": "İki atomik önerme, cümledeki 've' bağlacıyla birleşiyor.",
                "success": "İki atomik önermeyi birleşim olarak doğru kurdun.",
            },
            {
                "statement": "Yağmur yağmıyorsa piknik yapılır.",
                "key": [
                    {"symbol": "p", "meaning": "Yağmur yağıyor."},
                    {"symbol": "q", "meaning": "Piknik yapılıyor."},
                ],
                "answers": [["¬", "p", "→", "q"]],
                "hint": "Koşulun ön bileşeni, p'nin olumsuzlamasıdır.",
                "success": "Olumsuzlanan ön bileşeni koşulun doğru tarafına yerleştirdin.",
            },
            {
                "statement": "Ali çalışırsa hem sınavı geçer hem burs alır.",
                "key": [
                    {"symbol": "p", "meaning": "Ali çalışıyor."},
                    {"symbol": "q", "meaning": "Ali sınavı geçiyor."},
                    {"symbol": "r", "meaning": "Ali burs alıyor."},
                ],
                "answers": [["p", "→", "(", "q", "∧", "r", ")"]],
                "hint": "Son bileşende iki sonuç birlikte isteniyor; birleşimi parantez içine al.",
                "success": "Ana bağlacı ve son bileşenin kapsamını doğru gösterdin.",
            },
        ],
    },
    "ders-19-veya-ve-ise": {
        "type": "symbolization",
        "title": "Yönü ve bağlacı ayırt et",
        "description": "Ayrık bağlaç, koşul ve çift yönlülük arasındaki farkı formül kurarak sınayın.",
        "tokens": ["p", "q", "¬", "∧", "∨", "→", "↔", "(", ")"],
        "tasks": [
            {
                "statement": "Ali evdedir veya kütüphanededir; iki olasılık birlikte dışlanmıyor.",
                "key": [
                    {"symbol": "p", "meaning": "Ali evde."},
                    {"symbol": "q", "meaning": "Ali kütüphanede."},
                ],
                "answers": [["p", "∨", "q"]],
                "hint": "Standart mantıksal 'veya' kapsayıcıdır.",
                "success": "Kapsayıcı ayrık bağlacı doğru kullandın.",
            },
            {
                "statement": "Bir sayı çifttir ancak ve ancak ikiye kalansız bölünür.",
                "key": [
                    {"symbol": "p", "meaning": "Sayı çifttir."},
                    {"symbol": "q", "meaning": "Sayı ikiye kalansız bölünür."},
                ],
                "answers": [["p", "↔", "q"]],
                "hint": "'Ancak ve ancak' iki koşul yönünü birlikte ister.",
                "success": "Karşılıklı yeterlilik ve zorunluluğu çift yönlülükle gösterdin.",
            },
            {
                "statement": "Maç ancak yağmur yağarsa iptal edilir.",
                "key": [
                    {"symbol": "p", "meaning": "Yağmur yağıyor."},
                    {"symbol": "q", "meaning": "Maç iptal ediliyor."},
                ],
                "answers": [["q", "→", "p"]],
                "hint": "'q ancak p ise', q → p demektir; p burada gerekli koşuldur.",
                "success": "'Ancak' ifadesinin koşul yönünü doğru okudun.",
            },
        ],
    },
    "ders-20-dogruluk-tablolari-i": {
        "type": "truth_table",
        "title": "Doğruluk tablosunu sen tamamla",
        "description": "p→q formülünün yalnız bir durumda yanlış olduğunu tabloyu doldurarak göster.",
        "formula": "p → q",
        "result_label": "p → q",
        "atoms": ["p", "q"],
        "rows": [
            {"values": ["D", "D"], "answer": "D"},
            {"values": ["D", "Y"], "answer": "Y"},
            {"values": ["Y", "D"], "answer": "D"},
            {"values": ["Y", "Y"], "answer": "D"},
        ],
        "success": "Koşulun tek yanlış satırını doğru belirledin: ön bileşen doğruyken son bileşen yanlış.",
        "review": "Önce p'nin doğru, q'nun yanlış olduğu satırı bul; maddi koşul yalnız o satırda yanlıştır.",
    },
    "ders-21-dogruluk-tablolari-ii-ve-gecerlilik": {
        "type": "truth_table",
        "title": "Geçerliliği totolojiyle sınama",
        "description": "Modus ponens biçimini tek formüle dönüştüren ((p→q)∧p)→q ifadesinin bütün satırlarını doldur.",
        "formula": "((p → q) ∧ p) → q",
        "result_label": "((p→q)∧p)→q",
        "atoms": ["p", "q"],
        "rows": [
            {"values": ["D", "D"], "answer": "D"},
            {"values": ["D", "Y"], "answer": "D"},
            {"values": ["Y", "D"], "answer": "D"},
            {"values": ["Y", "Y"], "answer": "D"},
        ],
        "success": "Bütün satırlar doğru: koşulluya çevrilen modus ponens biçimi bir totolojidir.",
        "review": "Dış koşulun ön bileşeni ((p→q)∧p) yanlış olduğunda bütün formül doğrudur; ön bileşen doğru olduğunda q da doğrudur.",
    },
    "ders-24-cikarim-kurallari-i": {
        "type": "proof_builder",
        "title": "Kurallı türetimi sıraya koy",
        "description": "Aday satırları seçerek öncüllerden hedefe giden en kısa lisanslı türetimi kur.",
        "premises": [
            {"line": 1, "formula": "p → q", "rule": "Öncül"},
            {"line": 2, "formula": "q → r", "rule": "Öncül"},
            {"line": 3, "formula": "p", "rule": "Öncül"},
        ],
        "goal": "r",
        "steps": [
            {"id": "mp-q", "formula": "q", "rule": "→E 1, 3", "depth": 0, "hint": "Önce 1 ve 3. satırlardan q elde edilir."},
            {"id": "mp-r", "formula": "r", "rule": "→E 2, 4", "depth": 0, "hint": "q elde edildikten sonra 2. satırla hedefe geçebilirsin."},
            {"id": "wrong-converse", "formula": "p", "rule": "→E 1, 2", "depth": 0, "hint": "→E için koşullunun ön bileşeni ayrıca bulunmalıdır."},
            {"id": "wrong-negation", "formula": "¬r", "rule": "¬I 2–3", "depth": 0, "hint": "Burada açılmış ve çelişkiyle kapanmış bir alt kanıt yok."},
        ],
        "answer_order": ["mp-q", "mp-r"],
        "success": "İki modus ponens adımını doğru bağımlılık sırasıyla kurdun.",
    },
    "ders-30-dogal-dilden-sembole-i": {
        "type": "symbolization",
        "title": "Niceleyiciyi ve kapsamı kur",
        "description": "Alan bütün varlıklar olsun. Sembol anahtarındaki yükü kaybetmeden cümleleri yüklem mantığına çevir.",
        "tokens": ["∀x", "∃x", "Kx", "Ux", "¬", "∧", "→", "(", ")"],
        "tasks": [
            {
                "statement": "Bütün kuşlar uçar.",
                "key": [
                    {"symbol": "Kx", "meaning": "x kuştur."},
                    {"symbol": "Ux", "meaning": "x uçar."},
                ],
                "answers": [["∀x", "(", "Kx", "→", "Ux", ")"]],
                "hint": "Tümel sınıf cümlesinde kuş olmak, uçmanın koşulu olarak yazılır.",
                "success": "Tümel cümleyi doğru koşullu yapıyla kurdun.",
            },
            {
                "statement": "Bazı kuşlar uçmaz.",
                "key": [
                    {"symbol": "Kx", "meaning": "x kuştur."},
                    {"symbol": "Ux", "meaning": "x uçar."},
                ],
                "answers": [["∃x", "(", "Kx", "∧", "¬", "Ux", ")"]],
                "hint": "Aynı tanığın hem kuş hem uçmayan olması gerekir.",
                "success": "Varoluş tanığındaki sınıf ve özellik yükünü birlikte korudun.",
            },
            {
                "statement": "Hiçbir kuş uçmaz.",
                "key": [
                    {"symbol": "Kx", "meaning": "x kuştur."},
                    {"symbol": "Ux", "meaning": "x uçar."},
                ],
                "answers": [
                    ["∀x", "(", "Kx", "→", "¬", "Ux", ")"],
                    ["¬", "∃x", "(", "Kx", "∧", "Ux", ")"],
                ],
                "hint": "Bunu tümel bir olumsuz koşul veya uçan kuş bulunmadığını söyleyen varoluşsal olumsuzlama olarak yazabilirsin.",
                "success": "Eşdeğer iki doğru okumadan birini kurdun.",
            },
        ],
    },
    "ders-31-dogal-dilden-sembole-ii": {
        "type": "symbolization",
        "title": "Bağımlılığı sembolle göster",
        "description": "Niceleyici sırasını değiştirerek 'her biri için bir' ile 'herkes için aynı' ayrımını görünür kıl.",
        "tokens": ["∀x", "∃y", "Ox", "Ky", "Rxy", "¬", "∧", "→", "(", ")"],
        "tasks": [
            {
                "statement": "Her öğrenci en az bir kitap okudu.",
                "key": [
                    {"symbol": "Ox", "meaning": "x öğrencidir."},
                    {"symbol": "Ky", "meaning": "y kitaptır."},
                    {"symbol": "Rxy", "meaning": "x, y'yi okudu."},
                ],
                "answers": [["∀x", "(", "Ox", "→", "∃y", "(", "Ky", "∧", "Rxy", ")", ")"]],
                "hint": "Kitap tanığı her öğrenciye göre değişebileceği için ∃y, ∀x'in kapsamındadır.",
                "success": "Öğrenciye bağlı kitap tanığını doğru kapsamda kurdun.",
            },
            {
                "statement": "Bütün öğrencilerin okuduğu en az bir kitap vardır.",
                "key": [
                    {"symbol": "Ox", "meaning": "x öğrencidir."},
                    {"symbol": "Ky", "meaning": "y kitaptır."},
                    {"symbol": "Rxy", "meaning": "x, y'yi okudu."},
                ],
                "answers": [["∃y", "(", "Ky", "∧", "∀x", "(", "Ox", "→", "Rxy", ")", ")"]],
                "hint": "Tek bir kitap bütün öğrenciler için çalışacağı için ∃y en dıştadır.",
                "success": "Ortak kitap tanığını niceleyici sırasıyla doğru gösterdin.",
            },
            {
                "statement": "Hiçbir öğrenci hiçbir kitap okumadı.",
                "key": [
                    {"symbol": "Ox", "meaning": "x öğrencidir."},
                    {"symbol": "Ky", "meaning": "y kitaptır."},
                    {"symbol": "Rxy", "meaning": "x, y'yi okudu."},
                ],
                "answers": [["∀x", "(", "Ox", "→", "¬", "∃y", "(", "Ky", "∧", "Rxy", ")", ")"]],
                "hint": "Her öğrenci için, onun okuduğu bir kitap tanığının bulunmadığını söyle.",
                "success": "Olumsuzluğun varoluş niceleyicisi üzerindeki kapsamını doğru kurdun.",
            },
        ],
    },
    "ders-33-semantik-ve-modeller": {
        "type": "model_builder",
        "title": "Bir karşı model kur",
        "description": "Nesnelere özellik ve ilişki ata; formüllerin yalnız sembolle değil yorumla doğruluk kazandığını gör.",
        "objects": [
            {"id": "a", "label": "a"},
            {"id": "b", "label": "b"},
            {"id": "c", "label": "c"},
        ],
        "predicates": [
            {"id": "O", "label": "Öğrenci"},
            {"id": "K", "label": "Kitapsever"},
        ],
        "relations": [{"id": "T", "label": "tanır"}],
        "challenges": [
            {
                "title": "Bazı, fakat bütün değil",
                "prompt": "En az bir öğrenci kitapsever olsun; ayrıca kitapsever olmayan en az bir öğrenci bulunsun.",
                "formula": "∃x(Ox ∧ Kx) ∧ ∃x(Ox ∧ ¬Kx)",
                "uses_relations": False,
                "conditions": [
                    {"kind": "exists", "all": ["O", "K"], "none": [], "label": "Kitapsever bir öğrenci var."},
                    {"kind": "exists", "all": ["O"], "none": ["K"], "label": "Kitapsever olmayan bir öğrenci var."},
                ],
            },
            {
                "title": "Tümel koşulu gerçekleştir",
                "prompt": "En az bir öğrenci bulunsun ve bütün öğrenciler kitapsever olsun.",
                "formula": "∃xOx ∧ ∀x(Ox → Kx)",
                "uses_relations": False,
                "conditions": [
                    {"kind": "exists", "all": ["O"], "none": [], "label": "En az bir öğrenci var."},
                    {"kind": "subset", "left": "O", "right": "K", "label": "Her öğrenci kitapsever."},
                ],
            },
            {
                "title": "İlişkili tanık kur",
                "prompt": "En az bir öğrenci bulunsun ve her öğrenci en az bir kitapseveri tanısın.",
                "formula": "∃xOx ∧ ∀x(Ox → ∃y(Ky ∧ Txy))",
                "uses_relations": True,
                "conditions": [
                    {"kind": "exists", "all": ["O"], "none": [], "label": "En az bir öğrenci var."},
                    {
                        "kind": "forall_exists_relation",
                        "source_predicate": "O",
                        "relation": "T",
                        "target_predicate": "K",
                        "label": "Her öğrenci bir kitapseveri tanıyor.",
                    },
                ],
            },
        ],
    },
    "ders-34-dogal-turetim-i": {
        "type": "proof_builder",
        "title": "Kanıtı satır satır kur",
        "description": "Formül ve gerekçesi birlikte verilen aday satırları seç; her satırın önceki satırlara nasıl dayandığını izle.",
        "premises": [
            {"line": 1, "formula": "(p ∧ q) → r", "rule": "Öncül"},
            {"line": 2, "formula": "p", "rule": "Öncül"},
            {"line": 3, "formula": "q", "rule": "Öncül"},
        ],
        "goal": "r ∧ p",
        "steps": [
            {"id": "join-pq", "formula": "p ∧ q", "rule": "∧I 2, 3", "depth": 0, "hint": "Koşullunun ön bileşenini önce 2 ve 3. satırlardan kur."},
            {"id": "derive-r", "formula": "r", "rule": "→E 1, 4", "depth": 0, "hint": "1. satırdaki koşullu, ön bileşeni elde edilince kullanılabilir."},
            {"id": "goal", "formula": "r ∧ p", "rule": "∧I 5, 2", "depth": 0, "hint": "Hedef birleşimi, elde edilen r ile mevcut p'den kur."},
            {"id": "wrong-split", "formula": "p ∧ q", "rule": "∧E 2, 3", "depth": 0, "hint": "∧E birleşimi parçalar; burada birleşim üretmek için ∧I gerekir."},
            {"id": "wrong-arrow", "formula": "r", "rule": "→E 1, 2", "depth": 0, "hint": "2. satır tek başına (p ∧ q) ön bileşenini sağlamaz."},
        ],
        "answer_order": ["join-pq", "derive-r", "goal"],
        "success": "Her satırı lisanslayan öncülleri ve kuralları doğru sıraya koydun.",
    },
    "ders-35-dogal-turetim-ii": {
        "type": "proof_builder",
        "title": "Alt kanıtla olumsuzlama üret",
        "description": "Geçici varsayımı aç, çelişkiye ulaş ve varsayımı boşaltarak hedef olumsuzlamayı türet.",
        "premises": [
            {"line": 1, "formula": "p → q", "rule": "Öncül"},
            {"line": 2, "formula": "¬q", "rule": "Öncül"},
        ],
        "goal": "¬p",
        "steps": [
            {"id": "assume-p", "formula": "p", "rule": "Varsayım", "depth": 1, "hint": "¬p hedefi için p varsayımıyla bir alt kanıt aç."},
            {"id": "derive-q", "formula": "q", "rule": "→E 1, 3", "depth": 1, "hint": "Varsayılan p ile 1. satırdaki koşulluyu uygula."},
            {"id": "contradiction", "formula": "⊥", "rule": "¬E 2, 4", "depth": 1, "hint": "q ve ¬q birlikte çelişki verir."},
            {"id": "not-p", "formula": "¬p", "rule": "¬I 3–5", "depth": 0, "hint": "Alt kanıtın p varsayımını, ulaşılan çelişki üzerinden boşalt."},
            {"id": "wrong-denial", "formula": "¬p", "rule": "→E 1, 2", "depth": 0, "hint": "Sonucun değillenmesinden ön bileşenin değillenmesi →E ile doğrudan çıkmaz."},
            {"id": "wrong-bottom", "formula": "⊥", "rule": "∧I 2, 4", "depth": 1, "hint": "Çelişki, q ile ¬q'nun olumsuzlama elemesiyle birleşmesinden doğar."},
        ],
        "answer_order": ["assume-p", "derive-q", "contradiction", "not-p"],
        "success": "Varsayımın kapsamını koruyup ¬I ile doğru satır aralığını boşalttın.",
    },
}


def get_logic_interactive(lesson_slug):
    interactive = LOGIC_INTERACTIVES.get(lesson_slug)
    return deepcopy(interactive) if interactive else None
