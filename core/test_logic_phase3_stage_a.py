from html import unescape

from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from .models import LogicLessonProgress
from .logic_phase3_stage_a import (
    STAGE_A_CANDIDATE_LESSONS,
    STAGE_A_CANDIDATE_MAP,
    STAGE_A_SOURCE_REFERENCES,
)
from .logic_course_data import VISIBLE_LOGIC_LESSONS


class LogicPhase3StageACandidateTests(SimpleTestCase):
    required_fields = {
        "curriculum_id",
        "release_status",
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
        "source_ids",
    }

    def test_candidate_is_isolated_and_machine_readable(self):
        self.assertEqual(len(STAGE_A_CANDIDATE_LESSONS), 6)
        self.assertEqual(
            [lesson["curriculum_id"] for lesson in STAGE_A_CANDIDATE_LESSONS],
            ["A1", "A2", "A3", "A4", "A5", "A6"],
        )
        self.assertEqual(
            len(STAGE_A_CANDIDATE_MAP),
            len(STAGE_A_CANDIDATE_LESSONS),
        )

        for lesson in STAGE_A_CANDIDATE_LESSONS:
            with self.subTest(lesson=lesson["curriculum_id"]):
                self.assertTrue(self.required_fields.issubset(lesson))
                self.assertEqual(lesson["release_status"], "candidate")
                self.assertEqual(
                    lesson["duration"],
                    f'{lesson["estimated_minutes"]} dk',
                )

    def test_candidate_is_not_activated_in_the_learner_facing_course(self):
        visible_map = {
            lesson["slug"]: lesson
            for lesson in VISIBLE_LOGIC_LESSONS
        }

        self.assertEqual(len(VISIBLE_LOGIC_LESSONS), 45)
        self.assertNotIn("ders-kullanim-anma-ve-dil-duzeyleri", visible_map)
        self.assertEqual(
            visible_map["ders-1-onerme-nedir"]["title"],
            "Önerme Nedir?",
        )

    def test_competency_ids_are_stable_and_unique_within_stage_a(self):
        competency_ids = [
            competency
            for lesson in STAGE_A_CANDIDATE_LESSONS
            for competency in lesson["competencies"]
        ]

        self.assertEqual(len(competency_ids), len(set(competency_ids)))
        self.assertTrue(
            all(
                competency.count(".") == 1
                and competency.replace(".", "").replace("_", "").isalnum()
                for competency in competency_ids
            ),
        )

    def test_prerequisites_are_acyclic_and_refer_to_earlier_candidate_lessons(self):
        position = {
            lesson["slug"]: index
            for index, lesson in enumerate(STAGE_A_CANDIDATE_LESSONS)
        }

        for lesson in STAGE_A_CANDIDATE_LESSONS:
            for prerequisite in lesson["prerequisites"]:
                self.assertIn(prerequisite, position)
                self.assertLess(position[prerequisite], position[lesson["slug"]])

    def test_each_lesson_has_full_instructional_sequence(self):
        for lesson in STAGE_A_CANDIDATE_LESSONS:
            with self.subTest(lesson=lesson["curriculum_id"]):
                self.assertGreaterEqual(len(lesson["goals"]), 3)
                self.assertGreaterEqual(len(lesson["sections"]), 2)
                self.assertGreaterEqual(len(lesson["worked_examples"]), 3)
                self.assertGreaterEqual(len(lesson["mistakes"]), 3)
                self.assertGreaterEqual(len(lesson["practice"]), 6)
                self.assertGreaterEqual(len(lesson["production_tasks"]), 1)
                self.assertGreaterEqual(len(lesson["mastery_evidence"]), 3)
                self.assertGreaterEqual(len(lesson["review_prompts"]), 2)

                guided = lesson["guided_practice"]
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
                    self.assertTrue(
                        all(item.strip() for item in task["stimulus"]["items"]),
                    )

    def test_practice_answers_are_valid_and_choices_are_not_duplicated(self):
        for lesson in STAGE_A_CANDIDATE_LESSONS:
            for item in lesson["practice"]:
                with self.subTest(lesson=lesson["curriculum_id"], prompt=item["prompt"]):
                    self.assertIn(item["answer"], item["choices"])
                    self.assertEqual(len(item["choices"]), len(set(item["choices"])))
                    self.assertTrue(item["explanation"].strip())
                    self.assertIn(
                        item["difficulty_label"],
                        {"Temel", "Orta", "İleri", "Zor", "Çok Zor"},
                    )

    def test_academic_sources_are_explicit_and_known(self):
        known_sources = set(STAGE_A_SOURCE_REFERENCES)

        for lesson in STAGE_A_CANDIDATE_LESSONS:
            self.assertTrue(lesson["source_ids"])
            self.assertTrue(set(lesson["source_ids"]).issubset(known_sources))

    def test_premature_formal_vocabulary_is_not_used(self):
        blocked_symbols = {"∧", "∨", "¬", "→", "↔", "∀", "∃", "⊢", "⊨"}

        for lesson in STAGE_A_CANDIDATE_LESSONS:
            searchable = str(lesson)
            with self.subTest(lesson=lesson["curriculum_id"]):
                self.assertTrue(blocked_symbols.isdisjoint(searchable))

    def test_stage_a_uses_the_planned_terminology_distinctions(self):
        validity_lesson = STAGE_A_CANDIDATE_MAP["ders-3-gecerlilik-ve-dogruluk"]
        countercase_lesson = STAGE_A_CANDIDATE_MAP[
            "ders-9-karsi-ornek-sema-ve-curutme-teknikleri"
        ]

        self.assertIn("Sağlamlık", str(validity_lesson))
        self.assertNotIn("Güvenirlik", str(validity_lesson["key_terms"]))
        self.assertIn("Karşı durum", str(countercase_lesson))
        self.assertNotIn("Karşı model", str(countercase_lesson["key_terms"]))

    def test_a1_instruction_and_assessment_cover_each_target_expression_type(self):
        lesson = STAGE_A_CANDIDATE_MAP["ders-1-onerme-nedir"]
        worked_labels = {
            item["badge_label"] for item in lesson["worked_examples"]
        }

        self.assertTrue({"Soru", "Emir", "Ünlem", "Önerme"}.issubset(worked_labels))
        self.assertIn("yalın ünlem", str(lesson["production_tasks"]).lower())
        self.assertIn("yalın ünlem", str(lesson["mastery_evidence"]).lower())

    def test_a2_teaches_support_roles_without_indicator_shortcuts(self):
        lesson = STAGE_A_CANDIDATE_MAP["ders-2-arguman-oncul-ve-sonuc"]
        lesson_text = str(lesson).lower()

        self.assertIn("destek", lesson["summary"].lower())
        self.assertIn("ipucu", lesson_text)
        self.assertIn("açıklama", lesson_text)
        self.assertIn("ara sonuç", lesson_text)
        self.assertIn("örtük öncül", lesson_text)

        practice_text = str(lesson["practice"]).lower()
        self.assertIn("cümlelerin destek işlevi incelenmeli", practice_text)
        self.assertIn("zaten kabul edilip nedeni soruluyorsa", practice_text)

        production_text = str(lesson["production_tasks"]).lower()
        self.assertIn("kütüphane", production_text)
        self.assertIn("normatif bağlantı", production_text)

    def test_a3_separates_truth_validity_soundness_and_support_type(self):
        lesson = STAGE_A_CANDIDATE_MAP["ders-3-gecerlilik-ve-dogruluk"]
        lesson_text = str(lesson).lower()

        self.assertIn("önermenin fiilen doğru", lesson["summary"].lower())
        self.assertIn("geçerlilik", lesson_text)
        self.assertIn("sağlamlık", lesson_text)
        self.assertIn("olasılıksal destek", lesson_text)
        self.assertEqual(lesson["source_ids"], ["forallx-validity"])

        production_text = str(lesson["production_tasks"]).lower()
        self.assertIn("önce amaçlanan destek türünü belirle", production_text)
        self.assertIn("yalnız geçerlilikten sonra", production_text)
        self.assertIn("tümdengelimsel sağlamlık etiketi vermek yerine", production_text)

    def test_a4_separates_form_counterexample_and_countercase_targets(self):
        lesson = STAGE_A_CANDIDATE_MAP[
            "ders-9-karsi-ornek-sema-ve-curutme-teknikleri"
        ]
        lesson_text = str(lesson).lower()

        self.assertIn("tek bir başarılı örnek", lesson_text)
        self.assertIn("sözcük anlamları", lesson_text)
        self.assertIn("karşı örnek", lesson_text)
        self.assertIn("karşı durum", lesson_text)
        self.assertNotIn("karşı model", str(lesson["key_terms"]).lower())
        self.assertEqual(lesson["source_ids"], ["forallx-validity"])

        production_text = str(lesson["production_tasks"]).lower()
        self.assertIn("biçimini çıkar", production_text)
        self.assertIn("yer tutucularla şemalaştır", production_text)
        self.assertIn("bütün öncülleri doğru, sonucu yanlış", production_text)

    def test_a5_teaches_direction_without_treating_markers_as_automatic_rules(self):
        lesson = STAGE_A_CANDIDATE_MAP["ders-5-zorunlu-ve-yeterli-kosul"]
        lesson_text = str(lesson).lower()

        self.assertIn("standart çıkarımsal", lesson_text)
        self.assertIn("yalnızca", lesson_text)
        self.assertIn("koşul kuran ancak", lesson_text)
        self.assertIn("-medikçe", lesson_text)
        self.assertIn("karşıtlık", lesson_text)
        self.assertIn("tek başına", lesson_text)
        self.assertEqual(
            lesson["source_ids"],
            [
                "openstax-conditionals",
                "dowden-only-unless",
                "sep-necessary-sufficient",
            ],
        )

        practice_text = str(lesson["practice"]).lower()
        self.assertIn("dosya ancak ödeme", practice_text)
        self.assertIn("rapor uzundu; ancak anlaşılırdı", practice_text)

        production = lesson["production_tasks"][0]
        self.assertEqual(len(production["stimulus"]["items"]), 6)
        self.assertIn("önce koşul kurulup kurulmadığını", production["prompt"].lower())
        self.assertIn(
            "toplantı uzundu; ancak verimli geçti.",
            [item.lower() for item in production["stimulus"]["items"]],
        )

    def test_a6_separates_use_mention_language_levels_and_evaluation_types(self):
        lesson = STAGE_A_CANDIDATE_MAP["ders-kullanim-anma-ve-dil-duzeyleri"]
        lesson_text = str(lesson).lower()

        self.assertIn("kullanım", lesson_text)
        self.assertIn("anma", lesson_text)
        self.assertIn("nesne dili", lesson_text)
        self.assertIn("üst dil", lesson_text)
        self.assertIn("sözdizimsel", lesson_text)
        self.assertIn("anlamsal", lesson_text)
        self.assertIn("iyi kurulmuş fakat yanlış", lesson_text)
        self.assertIn("iyi kurulmamış", lesson_text)
        self.assertEqual(lesson["source_ids"], ["forallx-use-mention"])

        production = lesson["production_tasks"][0]
        self.assertEqual(len(production["stimulus"]["items"]), 6)
        self.assertIn("doğru kontrol örneklerini", production["prompt"].lower())
        self.assertIn("iki sözdizimsel ve iki anlamsal", str(production).lower())
        self.assertIn("l'de yalnız 'a' ve 'b'", str(production).lower())


class LogicPhase3StageAPreviewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.staff_user = user_model.objects.create_user(
            username="logic-reviewer",
            password="review-pass",
            is_staff=True,
        )
        cls.regular_user = user_model.objects.create_user(
            username="logic-student",
            password="student-pass",
        )

    def test_preview_requires_staff_access(self):
        url = reverse("logic_stage_a_preview")

        anonymous_response = self.client.get(url)
        self.assertEqual(anonymous_response.status_code, 302)
        self.assertIn(reverse("admin:login"), anonymous_response.url)

        self.client.force_login(self.regular_user)
        regular_response = self.client.get(url)
        self.assertEqual(regular_response.status_code, 302)
        self.assertIn(reverse("admin:login"), regular_response.url)

    def test_staff_preview_contains_all_candidate_lessons(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("logic_stage_a_preview"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/logic_stage_a_preview.html")
        for lesson in STAGE_A_CANDIDATE_LESSONS:
            with self.subTest(lesson=lesson["curriculum_id"]):
                self.assertContains(response, lesson["curriculum_id"])
                self.assertContains(response, lesson["title"])

    def test_staff_preview_contains_each_production_stimulus(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("logic_stage_a_preview"))
        rendered_text = unescape(response.content.decode())

        for lesson in STAGE_A_CANDIDATE_LESSONS:
            for task in lesson["production_tasks"]:
                stimulus = task["stimulus"]
                with self.subTest(lesson=lesson["curriculum_id"]):
                    self.assertIn(stimulus["label"], rendered_text)
                    for item in stimulus["items"]:
                        self.assertIn(item, rendered_text)

    def test_preview_is_read_only_and_has_no_learner_progress_hooks(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("logic_stage_a_preview"))

        self.assertEqual(LogicLessonProgress.objects.count(), 0)
        self.assertNotContains(response, "data-logic-lesson-page")
        self.assertNotContains(response, "data-progress-url")
        self.assertNotContains(response, reverse("logic_lesson_progress"))
        self.assertNotContains(response, "logic_lesson.js")
