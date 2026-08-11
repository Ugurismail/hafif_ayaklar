from html import unescape

from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from .logic_course_data import VISIBLE_LOGIC_LESSONS
from .logic_phase3_stage_a import STAGE_A_CANDIDATE_MAP
from .logic_phase3_stage_b import (
    STAGE_B_CANDIDATE_LESSONS,
    STAGE_B_CANDIDATE_MAP,
    STAGE_B_SOURCE_REFERENCES,
)
from .models import LogicLessonProgress


class LogicPhase3StageBCandidateTests(SimpleTestCase):
    required_fields = {
        "curriculum_id",
        "release_status",
        "order",
        "slug",
        "title",
        "summary",
        "focus",
        "duration",
        "estimated_minutes",
        "prerequisites",
        "competencies",
        "goals",
        "key_terms",
        "sections",
        "worked_examples",
        "mistakes",
        "practice",
        "guided_practice",
        "production_tasks",
        "mastery_evidence",
        "review_prompts",
        "next_step",
        "source_ids",
        "reading_note",
        "rigor_note",
        "symbol_set",
        "proof_tools",
        "legacy_sources",
    }

    def test_stage_b_is_complete_as_an_isolated_candidate(self):
        self.assertEqual(len(STAGE_B_CANDIDATE_LESSONS), 7)
        self.assertEqual(
            [lesson["curriculum_id"] for lesson in STAGE_B_CANDIDATE_LESSONS],
            ["B7", "B8", "B9", "B10", "B11", "B12", "B13"],
        )
        self.assertEqual(len(STAGE_B_CANDIDATE_MAP), 7)

        for lesson in STAGE_B_CANDIDATE_LESSONS:
            with self.subTest(lesson=lesson["curriculum_id"]):
                self.assertTrue(self.required_fields.issubset(lesson))
                self.assertEqual(lesson["release_status"], "candidate")
                self.assertEqual(
                    lesson["duration"],
                    f'{lesson["estimated_minutes"]} dk',
                )

        self.assertEqual(STAGE_B_CANDIDATE_LESSONS[0]["order"], 7)
        self.assertEqual(STAGE_B_CANDIDATE_LESSONS[0]["estimated_minutes"], 30)
        self.assertEqual(STAGE_B_CANDIDATE_LESSONS[1]["order"], 8)
        self.assertEqual(STAGE_B_CANDIDATE_LESSONS[1]["estimated_minutes"], 35)
        self.assertEqual(STAGE_B_CANDIDATE_LESSONS[2]["order"], 9)
        self.assertEqual(STAGE_B_CANDIDATE_LESSONS[2]["estimated_minutes"], 30)
        self.assertEqual(STAGE_B_CANDIDATE_LESSONS[3]["order"], 10)
        self.assertEqual(STAGE_B_CANDIDATE_LESSONS[3]["estimated_minutes"], 40)
        self.assertEqual(STAGE_B_CANDIDATE_LESSONS[4]["order"], 11)
        self.assertEqual(STAGE_B_CANDIDATE_LESSONS[4]["estimated_minutes"], 40)
        self.assertEqual(STAGE_B_CANDIDATE_LESSONS[5]["order"], 12)
        self.assertEqual(STAGE_B_CANDIDATE_LESSONS[5]["estimated_minutes"], 35)
        self.assertEqual(STAGE_B_CANDIDATE_LESSONS[6]["order"], 13)
        self.assertEqual(STAGE_B_CANDIDATE_LESSONS[6]["estimated_minutes"], 50)

    def test_b7_is_not_activated_in_the_learner_facing_course(self):
        visible_map = {lesson["slug"]: lesson for lesson in VISIBLE_LOGIC_LESSONS}
        candidate = STAGE_B_CANDIDATE_LESSONS[0]

        self.assertEqual(len(VISIBLE_LOGIC_LESSONS), 45)
        self.assertEqual(candidate["slug"], "ders-17-sembollestirmeye-giris")
        self.assertEqual(
            visible_map[candidate["slug"]]["title"],
            "Sembolleştirmeye Giriş",
        )
        self.assertEqual(
            candidate["title"],
            "Atomik TFL Cümleleri ve Sembol Anahtarı",
        )

    def test_b7_prerequisites_exist_in_the_stage_a_candidate(self):
        lesson = STAGE_B_CANDIDATE_LESSONS[0]

        self.assertEqual(
            lesson["prerequisites"],
            [
                "ders-1-onerme-nedir",
                "ders-9-karsi-ornek-sema-ve-curutme-teknikleri",
                "ders-kullanim-anma-ve-dil-duzeyleri",
            ],
        )
        self.assertTrue(
            set(lesson["prerequisites"]).issubset(STAGE_A_CANDIDATE_MAP),
        )

    def test_b8_prerequisite_is_the_completed_b7_candidate(self):
        lesson = STAGE_B_CANDIDATE_MAP["ders-18-degil-ve-ve-baglaclari"]

        self.assertEqual(
            lesson["prerequisites"],
            ["ders-17-sembollestirmeye-giris"],
        )
        self.assertIn(lesson["prerequisites"][0], STAGE_B_CANDIDATE_MAP)
        self.assertLess(
            STAGE_B_CANDIDATE_MAP[lesson["prerequisites"][0]]["order"],
            lesson["order"],
        )

    def test_b9_prerequisite_is_the_completed_b8_candidate(self):
        lesson = STAGE_B_CANDIDATE_MAP["ders-19-veya-ve-ise"]

        self.assertEqual(
            lesson["prerequisites"],
            ["ders-18-degil-ve-ve-baglaclari"],
        )
        self.assertIn(lesson["prerequisites"][0], STAGE_B_CANDIDATE_MAP)
        self.assertLess(
            STAGE_B_CANDIDATE_MAP[lesson["prerequisites"][0]]["order"],
            lesson["order"],
        )

    def test_b10_prerequisites_bridge_stage_a_and_current_stage_b(self):
        lesson = STAGE_B_CANDIDATE_MAP[
            "ders-kosul-yalnizca-cift-yonluluk"
        ]

        self.assertEqual(
            lesson["prerequisites"],
            ["ders-5-zorunlu-ve-yeterli-kosul", "ders-19-veya-ve-ise"],
        )
        self.assertIn(lesson["prerequisites"][0], STAGE_A_CANDIDATE_MAP)
        self.assertIn(lesson["prerequisites"][1], STAGE_B_CANDIDATE_MAP)
        self.assertLess(
            STAGE_B_CANDIDATE_MAP[lesson["prerequisites"][1]]["order"],
            lesson["order"],
        )

        visible_slugs = {lesson["slug"] for lesson in VISIBLE_LOGIC_LESSONS}
        self.assertNotIn(lesson["slug"], visible_slugs)
        self.assertEqual(lesson["legacy_sources"], ["ders-19-veya-ve-ise"])

    def test_b11_prerequisites_bridge_stage_a_and_current_stage_b(self):
        lesson = STAGE_B_CANDIDATE_MAP[
            "ders-tfl-cumlesi-ana-baglac-ve-kapsam"
        ]

        self.assertEqual(
            lesson["prerequisites"],
            [
                "ders-kullanim-anma-ve-dil-duzeyleri",
                "ders-kosul-yalnizca-cift-yonluluk",
            ],
        )
        self.assertIn(lesson["prerequisites"][0], STAGE_A_CANDIDATE_MAP)
        self.assertIn(lesson["prerequisites"][1], STAGE_B_CANDIDATE_MAP)
        self.assertLess(
            STAGE_B_CANDIDATE_MAP[lesson["prerequisites"][1]]["order"],
            lesson["order"],
        )

        visible_slugs = {lesson["slug"] for lesson in VISIBLE_LOGIC_LESSONS}
        self.assertNotIn(lesson["slug"], visible_slugs)
        self.assertEqual(
            lesson["legacy_sources"],
            [
                "ders-kullanim-anma-ve-dil-duzeyleri",
                "ders-20-dogruluk-tablolari-i",
            ],
        )

    def test_b12_prerequisite_is_the_completed_b11_candidate(self):
        lesson = STAGE_B_CANDIDATE_MAP[
            "ders-belirsizlik-bulaniklik-savunulabilir-okumalar"
        ]

        self.assertEqual(
            lesson["prerequisites"],
            ["ders-tfl-cumlesi-ana-baglac-ve-kapsam"],
        )
        self.assertIn(lesson["prerequisites"][0], STAGE_B_CANDIDATE_MAP)
        self.assertLess(
            STAGE_B_CANDIDATE_MAP[lesson["prerequisites"][0]]["order"],
            lesson["order"],
        )

        visible_slugs = {lesson["slug"] for lesson in VISIBLE_LOGIC_LESSONS}
        self.assertNotIn(lesson["slug"], visible_slugs)
        self.assertEqual(lesson["legacy_sources"], [])

    def test_b13_requires_every_completed_stage_b_candidate(self):
        lesson = STAGE_B_CANDIDATE_MAP[
            "ders-kademeli-sembollestirme-atolyesi"
        ]
        expected_prerequisites = [
            "ders-17-sembollestirmeye-giris",
            "ders-18-degil-ve-ve-baglaclari",
            "ders-19-veya-ve-ise",
            "ders-kosul-yalnizca-cift-yonluluk",
            "ders-tfl-cumlesi-ana-baglac-ve-kapsam",
            "ders-belirsizlik-bulaniklik-savunulabilir-okumalar",
        ]

        self.assertEqual(lesson["prerequisites"], expected_prerequisites)
        self.assertTrue(
            set(lesson["prerequisites"]).issubset(STAGE_B_CANDIDATE_MAP),
        )
        self.assertTrue(
            all(
                STAGE_B_CANDIDATE_MAP[slug]["order"] < lesson["order"]
                for slug in lesson["prerequisites"]
            ),
        )
        visible_slugs = {lesson["slug"] for lesson in VISIBLE_LOGIC_LESSONS}
        self.assertNotIn(lesson["slug"], visible_slugs)

    def test_each_candidate_has_a_complete_instructional_sequence(self):
        for lesson in STAGE_B_CANDIDATE_LESSONS:
            with self.subTest(lesson=lesson["curriculum_id"]):
                self.assertGreaterEqual(len(lesson["goals"]), 3)
                self.assertGreaterEqual(len(lesson["sections"]), 3)
                self.assertGreaterEqual(len(lesson["worked_examples"]), 5)
                self.assertGreaterEqual(len(lesson["mistakes"]), 4)
                self.assertGreaterEqual(len(lesson["practice"]), 8)
                self.assertGreaterEqual(len(lesson["production_tasks"]), 1)
                self.assertGreaterEqual(len(lesson["mastery_evidence"]), 4)
                self.assertGreaterEqual(len(lesson["review_prompts"]), 2)

                guided = lesson["guided_practice"]
                self.assertEqual(
                    set(guided),
                    {"prompt", "starter", "checks", "solution"},
                )
                self.assertTrue(guided["prompt"].strip())
                self.assertTrue(guided["starter"].strip())
                self.assertGreaterEqual(len(guided["checks"]), 3)
                self.assertTrue(guided["solution"].strip())

                for task in lesson["production_tasks"]:
                    self.assertTrue(task["prompt"].strip())
                    self.assertGreaterEqual(len(task["checkpoints"]), 3)
                    self.assertTrue(task["sample_focus"].strip())
                    self.assertTrue(task["stimulus"]["label"].strip())
                    self.assertTrue(task["stimulus"]["items"])

    def test_candidate_practice_answers_are_valid_and_unique(self):
        for lesson in STAGE_B_CANDIDATE_LESSONS:
            for item in lesson["practice"]:
                with self.subTest(
                    lesson=lesson["curriculum_id"],
                    prompt=item["prompt"],
                ):
                    self.assertIn(item["answer"], item["choices"])
                    self.assertEqual(len(item["choices"]), len(set(item["choices"])))
                    self.assertTrue(item["explanation"].strip())
                    self.assertIn(
                        item["difficulty_label"],
                        {"Temel", "Orta", "İleri", "Zor", "Çok Zor"},
                    )

    def test_b7_sources_are_explicit_and_known(self):
        lesson = STAGE_B_CANDIDATE_LESSONS[0]

        self.assertEqual(
            lesson["source_ids"],
            ["forallx-first-symbolization", "mit-logic-sequence"],
        )
        self.assertTrue(
            set(lesson["source_ids"]).issubset(STAGE_B_SOURCE_REFERENCES),
        )

    def test_every_candidate_source_is_explicit_and_known(self):
        for lesson in STAGE_B_CANDIDATE_LESSONS:
            with self.subTest(lesson=lesson["curriculum_id"]):
                self.assertTrue(lesson["source_ids"])
                self.assertTrue(
                    set(lesson["source_ids"]).issubset(STAGE_B_SOURCE_REFERENCES),
                )

    def test_b7_does_not_teach_later_symbols_or_semantics(self):
        lesson = STAGE_B_CANDIDATE_LESSONS[0]
        searchable = str(lesson)
        blocked_symbols = {"¬", "∧", "∨", "→", "↔", "∀", "∃", "⊢", "⊨", "𝒜", "ℬ"}

        self.assertTrue(blocked_symbols.isdisjoint(searchable))
        self.assertNotIn("doğruluk tablosu", searchable.lower())
        self.assertNotIn("truth table", searchable.lower())
        self.assertEqual(lesson["symbol_set"], ["A", "B", "C", "A₁"])
        self.assertTrue(all(symbol.upper() == symbol for symbol in lesson["symbol_set"]))

    def test_b8_uses_only_negation_and_conjunction_formal_vocabulary(self):
        lesson = STAGE_B_CANDIDATE_MAP["ders-18-degil-ve-ve-baglaclari"]
        searchable = str(lesson)
        blocked_symbols = {"∨", "→", "↔", "∀", "∃", "⊢", "⊨", "𝒜", "ℬ"}

        self.assertTrue(blocked_symbols.isdisjoint(searchable))
        self.assertNotIn("doğruluk tablosu", searchable.lower())
        self.assertNotIn("truth table", searchable.lower())
        self.assertEqual(lesson["symbol_set"], ["A", "B", "¬", "∧", "(", ")"])

    def test_b9_does_not_teach_conditionals_or_formal_semantics(self):
        lesson = STAGE_B_CANDIDATE_MAP["ders-19-veya-ve-ise"]
        searchable = str(lesson)
        blocked_symbols = {"→", "↔", "∀", "∃", "⊢", "⊨", "𝒜", "ℬ"}

        self.assertTrue(blocked_symbols.isdisjoint(searchable))
        self.assertNotIn("doğruluk tablosu", searchable.lower())
        self.assertNotIn("truth table", searchable.lower())
        self.assertEqual(
            lesson["symbol_set"],
            ["A", "B", "C", "¬", "∧", "∨", "(", ")"],
        )

    def test_b10_does_not_teach_quantifiers_proofs_or_formal_semantics(self):
        lesson = STAGE_B_CANDIDATE_MAP[
            "ders-kosul-yalnizca-cift-yonluluk"
        ]
        searchable = str(lesson)
        blocked_symbols = {"∀", "∃", "⊢", "⊨", "𝒜", "ℬ"}

        self.assertTrue(blocked_symbols.isdisjoint(searchable))
        self.assertNotIn("doğruluk tablosu", searchable.lower())
        self.assertNotIn("truth table", searchable.lower())
        self.assertEqual(
            lesson["symbol_set"],
            ["A", "B", "¬", "∧", "∨", "→", "↔", "(", ")"],
        )

    def test_b11_stays_with_syntax_and_keeps_metavariables_out_of_object_language(self):
        lesson = STAGE_B_CANDIDATE_MAP[
            "ders-tfl-cumlesi-ana-baglac-ve-kapsam"
        ]
        searchable = str(lesson)
        blocked_symbols = {"∀", "∃", "⊢", "⊨"}

        self.assertTrue(blocked_symbols.isdisjoint(searchable))
        self.assertNotIn("doğruluk tablosu", searchable.lower())
        self.assertNotIn("truth table", searchable.lower())
        self.assertEqual(
            lesson["symbol_set"],
            ["A", "A₁", "¬", "∧", "∨", "→", "↔", "(", ")"],
        )
        self.assertNotIn("𝒜", lesson["symbol_set"])
        self.assertNotIn("ℬ", lesson["symbol_set"])
        self.assertIn("𝒜", searchable)
        self.assertIn("ℬ", searchable)

    def test_b12_stays_with_language_analysis_not_later_semantics_or_proofs(self):
        lesson = STAGE_B_CANDIDATE_MAP[
            "ders-belirsizlik-bulaniklik-savunulabilir-okumalar"
        ]
        searchable = str(lesson)
        blocked_symbols = {"∀", "∃", "⊢", "⊨", "𝒜", "ℬ"}

        self.assertTrue(blocked_symbols.isdisjoint(searchable))
        self.assertNotIn("doğruluk tablosu", searchable.lower())
        self.assertNotIn("truth table", searchable.lower())
        self.assertEqual(
            lesson["symbol_set"],
            ["A", "B", "C", "¬", "∧", "∨", "→", "↔", "(", ")"],
        )

    def test_b13_integrates_stage_b_without_teaching_later_methods(self):
        lesson = STAGE_B_CANDIDATE_MAP[
            "ders-kademeli-sembollestirme-atolyesi"
        ]
        searchable = str(lesson)
        blocked_symbols = {"∀", "∃", "⊢", "⊨", "𝒜", "ℬ"}

        self.assertTrue(blocked_symbols.isdisjoint(searchable))
        self.assertNotIn("doğruluk tablosu", searchable.lower())
        self.assertNotIn("truth table", searchable.lower())
        self.assertEqual(
            lesson["symbol_set"],
            ["A", "B", "C", "A₁", "¬", "∧", "∨", "→", "↔", "(", ")"],
        )

    def test_b7_teaches_the_atomic_sentence_boundary_and_local_key(self):
        lesson = STAGE_B_CANDIDATE_LESSONS[0]
        lesson_text = str(lesson).lower()

        self.assertIn("tam bildirim", lesson_text)
        self.assertIn("geçici", lesson_text)
        self.assertIn("iç yapı", lesson_text)
        self.assertIn("deniz ve ece kardeştir", lesson_text)
        self.assertIn("kişi adı", lesson_text)
        self.assertIn("cümle parçası", lesson_text)
        self.assertIn("mutlak basitlik", lesson_text)

        production = lesson["production_tasks"][0]
        self.assertEqual(len(production["stimulus"]["items"]), 5)
        self.assertIn("yalnız bir sembol anahtarı kur", production["prompt"].lower())
        self.assertIn("henüz bileşik formül yazma", production["prompt"].lower())

    def test_b8_teaches_scope_lexical_limits_and_information_loss(self):
        lesson = STAGE_B_CANDIDATE_MAP["ders-18-degil-ve-ve-baglaclari"]
        lesson_text = str(lesson).lower()

        self.assertEqual(lesson["source_ids"], ["forallx-connectives"])
        self.assertIn("mutsuz", lesson_text)
        self.assertIn("sözcüksel karşıtlık", lesson_text)
        self.assertIn("¬(a ∧ b)", lesson_text)
        self.assertIn("(¬a ∧ ¬b)", lesson_text)
        self.assertIn("ikisi birden değil", lesson_text)
        self.assertIn("ikisi de değil", lesson_text)
        self.assertIn("karşıtlık", lesson_text)
        self.assertIn("zaman sırası", lesson_text)
        self.assertIn("geri çeviri", lesson_text)

        production = lesson["production_tasks"][0]
        production_text = str(production)
        for target in ["(¬A ∧ B)", "(A ∧ ¬B)", "¬(A ∧ B)", "(¬A ∧ ¬B)"]:
            self.assertIn(target, production_text)
        self.assertEqual(len(production["stimulus"]["items"]), 4)

    def test_b9_separates_inclusive_exclusive_and_neither_nor_readings(self):
        lesson = STAGE_B_CANDIDATE_MAP["ders-19-veya-ve-ise"]
        lesson_text = str(lesson).lower()

        self.assertEqual(lesson["source_ids"], ["forallx-connectives"])
        self.assertIn("kapsayıcı", lesson_text)
        self.assertIn("dışlayıcı", lesson_text)
        self.assertIn("en az biri", lesson_text)
        self.assertIn("ikisi birlikte değil", lesson_text)
        self.assertIn("bağlam kanıtı", lesson_text)
        self.assertIn("((a ∨ b) ∧ ¬(a ∧ b))", lesson_text)
        self.assertIn("(¬a ∧ ¬b)", lesson_text)
        self.assertIn("(¬a ∨ ¬b)", lesson_text)
        self.assertIn("((a ∨ b) ∨ c)", lesson_text)

        production = lesson["production_tasks"][0]
        self.assertEqual(len(production["stimulus"]["items"]), 4)
        self.assertIn("kapsayıcı en-az-biri", str(production).lower())
        self.assertIn("dışlayıcı yapı", str(production).lower())
        self.assertIn("bağlam kanıtını", str(production).lower())

    def test_b10_teaches_direction_biconditional_unless_and_language_loss(self):
        lesson = STAGE_B_CANDIDATE_MAP[
            "ders-kosul-yalnizca-cift-yonluluk"
        ]
        lesson_text = str(lesson).lower()

        self.assertEqual(lesson["source_ids"], ["forallx-connectives"])
        self.assertIn("önbileşen", lesson_text)
        self.assertIn("artbileşen", lesson_text)
        self.assertIn("argümanın öncülü", lesson_text)
        self.assertIn("garanti", lesson_text)
        self.assertIn("gerekli koşul", lesson_text)
        self.assertIn("yeterli koşul", lesson_text)
        self.assertIn("a yalnızca b ise: a → b", lesson_text)
        self.assertIn("a ↔ b", lesson_text)
        self.assertIn("(a → b) ∧ (b → a)", lesson_text)
        self.assertIn("¬k → ¬t", lesson_text)
        self.assertIn("karşıtlık", lesson_text)
        self.assertIn("nedensellik", lesson_text)
        self.assertIn("söz verme", lesson_text)

        production = lesson["production_tasks"][0]
        self.assertEqual(len(production["stimulus"]["items"]), 7)
        self.assertIn("koşulu reddeder", production["stimulus"]["note"].lower())
        self.assertIn("koşul olmayan 'ancak'", production["prompt"].lower())

    def test_b11_teaches_inductive_syntax_parsing_and_language_levels(self):
        lesson = STAGE_B_CANDIDATE_MAP[
            "ders-tfl-cumlesi-ana-baglac-ve-kapsam"
        ]
        lesson_text = str(lesson).lower()

        self.assertEqual(lesson["source_ids"], ["forallx-tfl-sentences"])
        self.assertIn("tfl ifadesi", lesson_text)
        self.assertIn("tfl cümlesi", lesson_text)
        self.assertIn("tümevarımsal tanım", lesson_text)
        self.assertIn("bunların dışında hiçbir dizi", lesson_text)
        self.assertIn("oluşum ağacı", lesson_text)
        self.assertIn("ana bağlaç", lesson_text)
        self.assertIn("doğrudan alt cümle", lesson_text)
        self.assertIn("en kısa alt cümle", lesson_text)
        self.assertIn("üst değişken", lesson_text)
        self.assertIn("nesne dili", lesson_text)
        self.assertIn("a → b → c", lesson_text)
        self.assertIn("sessiz öncelik", lesson_text)
        self.assertIn("yalnız en dış parantez", lesson_text)

        production = lesson["production_tasks"][0]
        self.assertEqual(len(production["stimulus"]["items"]), 8)
        self.assertIn("katı tfl cümlesi", production["prompt"].lower())
        self.assertIn("yalnız dış-parantez", production["prompt"].lower())
        self.assertIn("tfl ifadesi fakat cümle değil", production["prompt"].lower())
        self.assertIn("atomik yapraklara", str(production).lower())

    def test_b12_teaches_turkish_ambiguity_vagueness_and_context_limits(self):
        lesson = STAGE_B_CANDIDATE_MAP[
            "ders-belirsizlik-bulaniklik-savunulabilir-okumalar"
        ]
        lesson_text = str(lesson).lower()

        self.assertEqual(lesson["source_ids"], ["forallx-ambiguity"])
        self.assertIn("sözcüksel belirsizlik", lesson_text)
        self.assertIn("yapısal belirsizlik", lesson_text)
        self.assertIn("kapsam belirsizliği", lesson_text)
        self.assertIn("bulanıklık", lesson_text)
        self.assertIn("açık ara okuma", lesson_text)
        self.assertIn("kazı gördüm", lesson_text)
        self.assertIn("çocuk kitabı aldı", lesson_text)
        self.assertIn("¬(l ∧ s)", lesson_text)
        self.assertIn("(¬l ∧ s)", lesson_text)
        self.assertIn("((a ∧ b) ∨ c)", lesson_text)
        self.assertIn("(a ∧ (b ∨ c))", lesson_text)
        self.assertIn("¬(a ∧ b)", lesson_text)
        self.assertIn("(¬a ∧ ¬b)", lesson_text)
        self.assertIn("parantez kapsamı belirler", lesson_text)
        self.assertIn("mantıksal zorunluluk", lesson_text)
        self.assertNotIn("bankaya gitti", lesson_text)

        production = lesson["production_tasks"][0]
        self.assertEqual(len(production["stimulus"]["items"]), 6)
        self.assertIn("belirsiz olmayan kontrol", str(production).lower())
        self.assertIn("konuşmacı niyetini", str(production).lower())

    def test_b13_is_a_seven_step_stage_exit_workshop(self):
        lesson = STAGE_B_CANDIDATE_MAP[
            "ders-kademeli-sembollestirme-atolyesi"
        ]
        lesson_text = str(lesson).lower()

        self.assertEqual(
            lesson["source_ids"],
            [
                "forallx-first-symbolization",
                "forallx-connectives",
                "forallx-tfl-sentences",
                "forallx-ambiguity",
                "mit-logic-sequence",
                "mit-logic-study-guide",
            ],
        )
        self.assertIn("yedi adımlı çözüm günlüğü", lesson_text)
        self.assertIn("1 bağlam", lesson_text)
        self.assertIn("2 atomlar/anahtar", lesson_text)
        self.assertIn("3 açık okuma", lesson_text)
        self.assertIn("4 dıştan içe yapı", lesson_text)
        self.assertIn("5 formül", lesson_text)
        self.assertIn("6 sözdizimi", lesson_text)
        self.assertIn("7 geri çeviri/kayıp", lesson_text)
        self.assertIn("atom envanteri", lesson_text)
        self.assertIn("dıştan içe", lesson_text)
        self.assertIn("anahtar ve sözdizimi iki ayrı denetimdir", lesson_text)
        self.assertIn("geri çeviri", lesson_text)
        self.assertIn("kayıp bilgi raporu", lesson_text)
        self.assertIn("alternatif okuma rubriği", lesson_text)
        self.assertIn("(k → r)", lesson_text)
        self.assertIn("(p → (a ∧ b))", lesson_text)
        self.assertIn("((m ∨ i) ∧ ¬(m ∧ i))", lesson_text)

        production = lesson["production_tasks"][0]
        self.assertEqual(len(production["stimulus"]["items"]), 6)
        self.assertGreaterEqual(len(production["checkpoints"]), 7)
        self.assertIn("aşama çıkış", production["prompt"].lower())
        self.assertIn("iki savunulabilir okumayla", production["prompt"].lower())
        self.assertIn("bulanık", str(production).lower())
        self.assertIn("yalnız anahtarla geri çevir", str(production).lower())

    def test_competencies_are_stable_and_unique_across_current_stage_b(self):
        lesson = STAGE_B_CANDIDATE_LESSONS[0]

        self.assertEqual(
            lesson["competencies"],
            [
                "tfl.atomic_identify",
                "tfl.key_construct",
                "tfl.abstraction_explain",
            ],
        )
        competency_ids = [
            competency
            for candidate in STAGE_B_CANDIDATE_LESSONS
            for competency in candidate["competencies"]
        ]
        self.assertEqual(len(competency_ids), len(set(competency_ids)))
        self.assertTrue(
            all(
                competency.count(".") == 1
                and competency.replace(".", "").replace("_", "").isalnum()
                for competency in competency_ids
            ),
        )


class LogicPhase3StageBPreviewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.staff_user = user_model.objects.create_user(
            username="logic-stage-b-reviewer",
            password="review-pass",
            is_staff=True,
        )
        cls.regular_user = user_model.objects.create_user(
            username="logic-stage-b-student",
            password="student-pass",
        )

    def test_preview_requires_staff_access(self):
        url = reverse("logic_stage_b_preview")

        anonymous_response = self.client.get(url)
        self.assertEqual(anonymous_response.status_code, 302)
        self.assertIn(reverse("admin:login"), anonymous_response.url)

        self.client.force_login(self.regular_user)
        regular_response = self.client.get(url)
        self.assertEqual(regular_response.status_code, 302)
        self.assertIn(reverse("admin:login"), regular_response.url)

    def test_staff_preview_contains_every_stage_b_candidate(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("logic_stage_b_preview"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/logic_stage_a_preview.html")
        self.assertContains(response, "Faz 3B: TFL dili ve sembolleştirme")
        for lesson in STAGE_B_CANDIDATE_LESSONS:
            with self.subTest(lesson=lesson["curriculum_id"]):
                self.assertContains(response, lesson["curriculum_id"])
                self.assertContains(response, lesson["title"])

    def test_staff_preview_contains_each_production_stimulus(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("logic_stage_b_preview"))
        rendered_text = unescape(response.content.decode())

        for lesson in STAGE_B_CANDIDATE_LESSONS:
            for task in lesson["production_tasks"]:
                stimulus = task["stimulus"]
                with self.subTest(lesson=lesson["curriculum_id"]):
                    self.assertIn(stimulus["label"], rendered_text)
                    for item in stimulus["items"]:
                        self.assertIn(item, rendered_text)

    def test_preview_is_read_only_and_has_no_learner_progress_hooks(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("logic_stage_b_preview"))

        self.assertEqual(LogicLessonProgress.objects.count(), 0)
        self.assertNotContains(response, "data-logic-lesson-page")
        self.assertNotContains(response, "data-progress-url")
        self.assertNotContains(response, reverse("logic_lesson_progress"))
        self.assertNotContains(response, "logic_lesson.js")
