from __future__ import annotations

import json
import re
from pathlib import Path

import pdfplumber


PDF_PATH = Path("/Users/ugurismail/Desktop/2025AdayMemurSorulari.pdf")
OUTPUT_JSON = Path("/Users/ugurismail/Desktop/memur sınavı/questions.json")
OUTPUT_JS = Path("/Users/ugurismail/Desktop/memur sınavı/questions.js")

SECTIONS = [
    {
        "id": "ataturk-ilkeleri-ve-inkilap-tarihi",
        "title": "Atatürk İlkeleri ve İnkılap Tarihi",
        "short_title": "Atatürk İlkeleri",
        "page_start": 258,
        "page_end": 283,
        "expected_count": 100,
        "answer_start": "ATATÜRK İLKELERİ ve İNKILAP TARİHİ SORULARI",
        "answer_end": "T.C. ANAYASASI SORULARI CEVAP ANAHTARI",
    },
    {
        "id": "tc-anayasasi",
        "title": "T.C. Anayasası",
        "short_title": "Anayasa",
        "page_start": 284,
        "page_end": 293,
        "expected_count": 28,
        "answer_start": "T.C. ANAYASASI SORULARI CEVAP ANAHTARI",
        "answer_end": "GENEL OLARAK DEVLET TEŞKİLATI SORULARI CEVAP ANAHTARI",
    },
    {
        "id": "genel-olarak-devlet-teskilati",
        "title": "Genel Olarak Devlet Teşkilatı",
        "short_title": "Devlet Teşkilatı",
        "page_start": 294,
        "page_end": 300,
        "expected_count": 28,
        "answer_start": "GENEL OLARAK DEVLET TEŞKİLATI SORULARI CEVAP ANAHTARI",
        "answer_end": "657 SAYILI DEVLET MEMURLARI KANUNU SORULARI CEVAP ANAHTARI",
    },
    {
        "id": "657-sayili-devlet-memurlari-kanunu",
        "title": "657 Sayılı Devlet Memurları Kanunu",
        "short_title": "657 Sayılı Kanun",
        "page_start": 301,
        "page_end": 319,
        "expected_count": 70,
        "answer_start": "657 SAYILI DEVLET MEMURLARI KANUNU SORULARI CEVAP ANAHTARI",
        "answer_end": "DOSYALAMA-USULLERİ SORULARI CEVAP ANAHTARI",
    },
    {
        "id": "yazisma-dosyalama-usulleri",
        "title": "Yazışma - Dosyalama Usulleri",
        "short_title": "Yazışma - Dosyalama",
        "page_start": 320,
        "page_end": 330,
        "expected_count": 40,
        "answer_start": "DOSYALAMA-USULLERİ SORULARI CEVAP ANAHTARI",
        "answer_end": "DEVLET MALINI KORUMA ve TASARRUF TEDBİRLERİ SORULARI CEVAP ANAHTARI",
    },
    {
        "id": "devlet-malini-koruma-ve-tasarruf-tedbirleri",
        "title": "Devlet Malını Koruma ve Tasarruf Tedbirleri",
        "short_title": "Devlet Malı",
        "page_start": 331,
        "page_end": 337,
        "expected_count": 20,
        "answer_start": "DEVLET MALINI KORUMA ve TASARRUF TEDBİRLERİ SORULARI CEVAP ANAHTARI",
        "answer_end": "HALKLA İLİŞKİLER SORULARI CEVAP ANAHTARI",
    },
    {
        "id": "halkla-iliskiler",
        "title": "Halkla İlişkiler",
        "short_title": "Halkla İlişkiler",
        "page_start": 338,
        "page_end": 345,
        "expected_count": 28,
        "answer_start": "HALKLA İLİŞKİLER SORULARI CEVAP ANAHTARI",
        "answer_end": "GİZLİLİK VE GİZLİLİĞİN ÖNEMİ SORULARI CEVAP ANAHTARI",
    },
    {
        "id": "gizlilik-ve-gizliligin-onemi",
        "title": "Gizlilik ve Gizliliğin Önemi",
        "short_title": "Gizlilik",
        "page_start": 346,
        "page_end": 353,
        "expected_count": 24,
        "answer_start": "GİZLİLİK VE GİZLİLİĞİN ÖNEMİ SORULARI CEVAP ANAHTARI",
        "answer_end": "MİLLİ GÜVENLİK BİLGİLERİ SORULARI CEVAP ANAHTARI",
    },
    {
        "id": "milli-guvenlik-bilgileri",
        "title": "Millî Güvenlik Bilgileri",
        "short_title": "Millî Güvenlik",
        "page_start": 354,
        "page_end": 360,
        "expected_count": 23,
        "answer_start": "MİLLİ GÜVENLİK BİLGİLERİ SORULARI CEVAP ANAHTARI",
        "answer_end": "HABERLEŞME SORULARI CEVAP ANAHTARI",
    },
    {
        "id": "haberlesme",
        "title": "Haberleşme",
        "short_title": "Haberleşme",
        "page_start": 361,
        "page_end": 366,
        "expected_count": 20,
        "answer_start": "HABERLEŞME SORULARI CEVAP ANAHTARI",
        "answer_end": "TÜRKÇE DİL BİLGİSİ KURALLARI SORULARI CEVAP ANAHTARI",
    },
    {
        "id": "turkce-dil-bilgisi-kurallari",
        "title": "Türkçe Dil Bilgisi Kuralları",
        "short_title": "Türkçe",
        "page_start": 367,
        "page_end": 381,
        "expected_count": 54,
        "answer_start": "TÜRKÇE DİL BİLGİSİ KURALLARI SORULARI CEVAP ANAHTARI",
        "answer_end": "İNSAN HAKLARI SORULARI CEVAP ANAHTARI",
    },
    {
        "id": "insan-haklari",
        "title": "İnsan Hakları",
        "short_title": "İnsan Hakları",
        "page_start": 382,
        "page_end": 388,
        "expected_count": 25,
        "answer_start": "İNSAN HAKLARI SORULARI CEVAP ANAHTARI",
        "answer_end": None,
    },
]

MANUAL_QUESTION_PATCHES = {
    ("yazisma-dosyalama-usulleri", 18): {
        "options": {
            "a": "T.C. / Dışişleri Bakanlığı / AVRUPA BİRLİĞİ BAŞKANLIĞI",
            "b": "T.C. / DIŞİŞLERİ BAKANLIĞI / Avrupa Birliği Başkanlığı",
            "c": "T.C. / DIŞİŞLERİ BAKANLIĞI / AVRUPA BİRLİĞİ BAŞKANLIĞI",
            "d": "T.C. / Dışişleri Bakanlığı / Avrupa Birliği Başkanlığı",
        }
    },
    ("yazisma-dosyalama-usulleri", 24): {
        "options": {
            "a": "Başkan Vekili / Hasan ÇALIŞKAN",
            "b": "Hasan ÇALIŞKAN / Başkan V.",
            "c": "Hasan ÇALIŞKAN / Başkan Vekili",
            "d": "Başkan V. / Hasan ÇALIŞKAN",
        }
    },
    ("turkce-dil-bilgisi-kurallari", 15): {
        "options": {
            "a": "TBMM’ye",
            "b": "DTCF’nin",
            "c": "TTK’nun",
            "d": "DDY’nin",
        }
    },
    ("turkce-dil-bilgisi-kurallari", 1): {
        "options": {
            "a": "[[u]]Bartın’a[[/u]] hiç gittin mi?",
            "b": "Vadideki [[u]]Zambak’ı[[/u]] okuduğumda uzun süre etkisinde kaldım.",
            "c": "[[u]]Türkçe’nin[[/u]] gücünü bilmek lazım.",
            "d": "[[u]]Avusturalya’da[[/u]] arkadaşımı ziyaret ettim.",
        }
    },
    ("turkce-dil-bilgisi-kurallari", 34): {
        "question": "“Kentimiz, [[u]]bayındırlı[[/u]] ve gelişmiş bir kenttir.” Yukarıdaki cümlede altı çizili sözcük yerine aşağıdakilerden hangisi gelmelidir?"
    },
    ("turkce-dil-bilgisi-kurallari", 42): {
        "options": {
            "a": "[[u]]Ucuzca[[/u]] bir otel arıyordu.",
            "b": "[[u]]Ahbapca[[/u]] bir tutum takındı.",
            "c": "Başını [[u]]hafifce[[/u]] öne eğdi.",
            "d": "[[u]]Kitapın[[/u]] kapağı yırtılmış.",
        }
    },
    ("yazisma-dosyalama-usulleri", 27): {
        "question": "“Belgenin hangi dosya ile ilişkili olduğunu veya işlemi biten belgenin hangi dosya/klasöre konulacağını gösteren alfabetik, sayısal, alfa-nümerik tanımlama” aşağıdakilerden hangisinin tanımıdır?"
    },
}

GLOBAL_TEXT_PATCHES = {
    "14)Sivas": "14) Sivas",
    "18)Aşağıdakilerden": "18) Aşağıdakilerden",
    "20)Aşağıdakilerden": "20) Aşağıdakilerden",
    "35)Mustafa": "35) Mustafa",
    "14)Aşağıdaki": "14) Aşağıdaki",
    "1)Kuvvetler": "1) Kuvvetler",
    "1)Merkezi": "1) Merkezi",
    "1)Aşağıdakilerden": "1) Aşağıdakilerden",
    "17)Aşağıdakilerden": "17) Aşağıdakilerden",
    "(IV)tatlı": "(IV) tatlı",
    "(III)Çünkü": "(III) Çünkü",
}


def load_pdf_text(page_start: int, page_end: int) -> str:
    with pdfplumber.open(PDF_PATH) as pdf:
        texts = []
        for idx in range(page_start, page_end + 1):
            texts.append((pdf.pages[idx].extract_text() or "").replace("\u00ad", ""))
    text = "\n".join(texts)
    text = re.sub(r"\n\d{3}\n", "\n", text)
    text = re.sub(
        r"([A-Za-zÇĞİÖŞÜçğıöşüÂâÎîÛû])-\n([A-Za-zÇĞİÖŞÜçğıöşüÂâÎîÛû])",
        r"\1\2",
        text,
    )
    for old, new in GLOBAL_TEXT_PATCHES.items():
        text = text.replace(old, new)
    return text


def normalize_lines(text: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines()]
    return [line for line in lines if line]


def fix_split_question_numbers(lines: list[str]) -> list[str]:
    fixed: list[str] = []
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        if line.startswith(")") and idx + 1 < len(lines) and re.fullmatch(r"\d+", lines[idx + 1]):
            fixed.append(f"{lines[idx + 1]}) {line[1:].strip()}")
            idx += 2
            continue
        fixed.append(line)
        idx += 1
    return fixed


def merge_wrapped_lines(lines: list[str]) -> list[str]:
    merged: list[str] = []
    for line in lines:
        if re.match(r"^\d+[\).]", line) or re.match(r"^[a-e]\)", line):
            merged.append(line)
        elif merged:
            merged[-1] += f" {line}"
        else:
            merged.append(line)
    return merged


def extract_questions(section: dict) -> list[dict]:
    text = load_pdf_text(section["page_start"], section["page_end"])
    lines = normalize_lines(text)
    lines = [
        line
        for line in lines
        if "SORULARI" not in line
        and "(YÜKSEKÖĞRETİM)" not in line
        and line not in {"ADAY MEMUR", "TEMEL EĞİTİM"}
    ]
    lines = fix_split_question_numbers(lines)
    merged = merge_wrapped_lines(lines)

    questions: list[dict] = []
    current: dict | None = None

    for line in merged:
        question_match = re.match(r"^(\d+)[\).]\s*(.*)$", line)
        if question_match:
            if current:
                questions.append(current)
            current = {
                "number": int(question_match.group(1)),
                "question": question_match.group(2).strip(),
                "options": {},
            }
            continue

        option_match = re.match(r"^([a-e])\)\s*(.*)$", line)
        if option_match and current:
            option_key = option_match.group(1)
            option_text = re.sub(r"\s+\d{3}$", "", option_match.group(2)).strip()
            current["options"][option_key] = option_text

    if current:
        questions.append(current)

    for question in questions:
        patch = MANUAL_QUESTION_PATCHES.get((section["id"], question["number"]))
        if patch:
            question.update(patch)

        question["question"] = (
            question["question"]
            .replace("Milli Mücadele'nn", "Millî Mücadele'nin")
            .replace("yasamda", "yaşamda")
            .replace("Takriri", "Takrir-i")
            .replace("Misakı", "Misak-ı")
        )

    return questions


def extract_answer_block(answer_pages_text: str, section: dict) -> str:
    start = answer_pages_text.index(section["answer_start"])
    end = (
        answer_pages_text.index(section["answer_end"], start)
        if section["answer_end"]
        else len(answer_pages_text)
    )
    return answer_pages_text[start:end]


def parse_answers(block: str) -> dict[int, str]:
    answers: dict[int, str] = {}
    pending_letters: list[str] = []

    lines = normalize_lines(block)
    for line in lines:
        if (
            "CEVAP ANAHTARI" in line
            or "SORULARI" in line
            or "(YÜKSEKÖĞRETİM)" in line
            or "TEMEL EĞİTİM" in line
            or re.fullmatch(r"\d{3}", line)
        ):
            continue

        if re.fullmatch(r"(?:[a-d]\s+)*[a-d]", line):
            pending_letters.extend(line.split())
            continue

        if not re.search(r"\d", line):
            continue

        tokens = line.split()
        idx = 0
        while idx < len(tokens):
            token = tokens[idx]
            if not token.isdigit():
                idx += 1
                continue

            number = int(token)
            if idx + 1 < len(tokens) and re.fullmatch(r"[a-d]", tokens[idx + 1]):
                answers[number] = tokens[idx + 1]
                idx += 2
            else:
                if not pending_letters:
                    raise ValueError(f"Missing pending answer letter for question {number} in line: {line}")
                answers[number] = pending_letters.pop(0)
                idx += 1

    return answers


def build_dataset() -> dict:
    answer_pages_text = load_pdf_text(389, 392)
    topics: list[dict] = []

    for section in SECTIONS:
        questions = extract_questions(section)
        answer_block = extract_answer_block(answer_pages_text, section)
        answers = parse_answers(answer_block)

        numbers = [question["number"] for question in questions]
        expected_numbers = list(range(1, section["expected_count"] + 1))

        if len(questions) != section["expected_count"]:
            raise ValueError(
                f"{section['title']}: expected {section['expected_count']} questions, got {len(questions)}"
            )

        if numbers != expected_numbers:
            raise ValueError(
                f"{section['title']}: question sequence mismatch. Expected {expected_numbers[:3]}...{expected_numbers[-3:]}, got {numbers[:3]}...{numbers[-3:]}"
            )

        if len(answers) != section["expected_count"]:
            raise ValueError(
                f"{section['title']}: expected {section['expected_count']} answers, got {len(answers)}"
            )

        for question in questions:
            if set(question["options"]) != {"a", "b", "c", "d"}:
                raise ValueError(
                    f"{section['title']} {question['number']}: option set is {sorted(question['options'])}"
                )

        topic_questions = []
        for question in questions:
            topic_questions.append(
                {
                    "id": f"{section['id']}-{question['number']}",
                    "number": question["number"],
                    "question": question["question"],
                    "options": question["options"],
                    "answer": answers[question["number"]],
                }
            )

        topics.append(
            {
                "id": section["id"],
                "title": section["title"],
                "shortTitle": section["short_title"],
                "pageStart": section["page_start"] + 1,
                "pageEnd": section["page_end"] + 1,
                "questionCount": section["expected_count"],
                "questions": topic_questions,
            }
        )

    return {
        "version": "2026-03-31-topics-v1",
        "source": {
            "pdf": str(PDF_PATH),
            "questionPages": "259-389",
            "answerPages": "390-393",
        },
        "topics": topics,
    }


def main() -> None:
    dataset = build_dataset()
    OUTPUT_JSON.write_text(
        json.dumps(dataset, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    OUTPUT_JS.write_text(
        "window.EXAM_DATA = " + json.dumps(dataset, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT_JSON}")
    print(f"Wrote {OUTPUT_JS}")


if __name__ == "__main__":
    main()
