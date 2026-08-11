import json

from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from .logic_course_data import (
    VISIBLE_LOGIC_LESSONS,
    get_logic_course,
    practice,
)
from .logic_curriculum import LOGIC_MASTERY_THRESHOLD
from .logic_interactives import LOGIC_INTERACTIVES
from .logic_level_test_bank import LOGIC_LEVEL_TEST_BANK, build_logic_level_test
from .models import LogicLessonProgress


class LogicCurriculumTests(SimpleTestCase):
    def test_every_visible_lesson_appears_once_in_explicit_curriculum(self):
        course = get_logic_course()
        configured_slugs = [
            lesson['slug']
            for stage in course['levels']
            for lesson in stage['lessons']
        ]
        visible_slugs = [lesson['slug'] for lesson in VISIBLE_LOGIC_LESSONS]

        self.assertEqual(len(configured_slugs), 45)
        self.assertEqual(len(configured_slugs), len(set(configured_slugs)))
        self.assertEqual(set(configured_slugs), set(visible_slugs))
        self.assertEqual(
            [lesson['display_order'] for lesson in course['lessons']],
            list(range(1, 46)),
        )

    def test_every_visible_lesson_has_recognition_and_production_practice(self):
        for lesson in VISIBLE_LOGIC_LESSONS:
            with self.subTest(lesson=lesson['slug']):
                self.assertGreaterEqual(len(lesson.get('practice', [])), 1)
                self.assertGreaterEqual(len(lesson.get('production_tasks', [])), 1)

                for item in lesson['practice']:
                    self.assertIn(item['answer'], item['choices'])

                for production in lesson['production_tasks']:
                    self.assertTrue(production['prompt'].strip())
                    self.assertGreaterEqual(len(production['checkpoints']), 3)
                    self.assertTrue(production['sample_focus'].strip())

    def test_natural_deduction_precedes_predicate_logic(self):
        lessons = get_logic_course()['lessons']
        order = {lesson['slug']: lesson['display_order'] for lesson in lessons}

        self.assertLess(
            order['ders-34-dogal-turetim-i'],
            order['ders-26-niceleyicilere-giris'],
        )
        self.assertLess(
            order['ders-37-dogruluk-agaclari-ve-meta-teori'],
            order['ders-33-semantik-ve-modeller'],
        )

    def test_practice_difficulty_is_generated_for_any_item_count(self):
        items = [
            (f'Soru {index}', ['A', 'B'], 'A', 'Açıklama')
            for index in range(7)
        ]

        generated = practice(items)

        self.assertEqual(len(generated), 7)
        self.assertTrue(all(item['difficulty_label'] for item in generated))
        self.assertTrue(all(item['answer'] in item['choices'] for item in generated))

    def test_assessment_bank_answers_are_valid_and_seed_is_stable(self):
        self.assertTrue(
            all(question['correct'] in question['options'] for question in LOGIC_LEVEL_TEST_BANK),
        )
        first = build_logic_level_test(seed='stable-attempt')
        second = build_logic_level_test(seed='stable-attempt')

        self.assertEqual(first, second)
        self.assertEqual(first['sample_size'], 50)

    def test_interactive_labs_have_valid_curriculum_contracts(self):
        visible_slugs = {lesson['slug'] for lesson in VISIBLE_LOGIC_LESSONS}
        supported_types = {
            'truth_table',
            'symbolization',
            'proof_builder',
            'model_builder',
        }

        self.assertGreaterEqual(len(LOGIC_INTERACTIVES), 10)
        for lesson_slug, interactive in LOGIC_INTERACTIVES.items():
            with self.subTest(lesson=lesson_slug):
                self.assertIn(lesson_slug, visible_slugs)
                self.assertIn(interactive['type'], supported_types)
                self.assertTrue(interactive['title'].strip())
                self.assertTrue(interactive['description'].strip())

                if interactive['type'] == 'truth_table':
                    self.assertTrue(interactive['rows'])
                    self.assertTrue(all(row['answer'] in {'D', 'Y'} for row in interactive['rows']))

                if interactive['type'] == 'symbolization':
                    token_set = set(interactive['tokens'])
                    self.assertGreaterEqual(len(interactive['tasks']), 3)
                    for task in interactive['tasks']:
                        self.assertTrue(task['answers'])
                        self.assertTrue(task['key'])
                        for answer in task['answers']:
                            self.assertTrue(answer)
                            self.assertTrue(set(answer).issubset(token_set))

                if interactive['type'] == 'proof_builder':
                    step_ids = [step['id'] for step in interactive['steps']]
                    self.assertEqual(len(step_ids), len(set(step_ids)))
                    self.assertTrue(interactive['answer_order'])
                    self.assertTrue(set(interactive['answer_order']).issubset(step_ids))
                    self.assertTrue(all(step['depth'] >= 0 for step in interactive['steps']))

                if interactive['type'] == 'model_builder':
                    object_ids = {item['id'] for item in interactive['objects']}
                    predicate_ids = {item['id'] for item in interactive['predicates']}
                    relation_ids = {item['id'] for item in interactive['relations']}
                    self.assertGreaterEqual(len(object_ids), 3)
                    self.assertTrue(predicate_ids)
                    self.assertTrue(relation_ids)
                    for challenge in interactive['challenges']:
                        self.assertTrue(challenge['conditions'])
                        for condition in challenge['conditions']:
                            referenced_predicates = set(condition.get('all', []))
                            referenced_predicates.update(condition.get('none', []))
                            referenced_predicates.update(
                                value
                                for key, value in condition.items()
                                if key in {'left', 'right', 'source_predicate', 'target_predicate'}
                            )
                            self.assertTrue(referenced_predicates.issubset(predicate_ids))
                            if condition.get('relation'):
                                self.assertIn(condition['relation'], relation_ids)


class LogicCourseViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='logic-student',
            password='test-pass',
        )
        self.lesson_slug = 'ders-1-onerme-nedir'
        self.progress_url = reverse('logic_lesson_progress')

    def post_progress(self, payload):
        return self.client.post(
            self.progress_url,
            data=json.dumps(payload),
            content_type='application/json',
        )

    def test_public_course_and_lesson_pages_render(self):
        course_response = self.client.get(reverse('logic_home'))
        lesson_response = self.client.get(
            reverse('logic_lesson_detail', args=[self.lesson_slug]),
        )

        self.assertEqual(course_response.status_code, 200)
        self.assertEqual(lesson_response.status_code, 200)
        self.assertContains(course_response, 'Akıl Yürütmenin Temelleri')
        self.assertContains(lesson_response, 'Bilgini dene')
        self.assertContains(lesson_response, 'data-logic-lesson-page')

    def test_each_interactive_lab_type_renders_its_workspace(self):
        cases = [
            ('ders-17-sembollestirmeye-giris', 'data-symbolization-lab'),
            ('ders-20-dogruluk-tablolari-i', 'data-truth-table-lab'),
            ('ders-34-dogal-turetim-i', 'data-proof-builder'),
            ('ders-33-semantik-ve-modeller', 'data-model-builder'),
        ]

        for lesson_slug, marker in cases:
            with self.subTest(lesson=lesson_slug):
                response = self.client.get(
                    reverse('logic_lesson_detail', args=[lesson_slug]),
                )

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, marker)
                self.assertContains(response, 'logic-interactive-config')

    def test_legacy_lesson_url_redirects_permanently(self):
        response = self.client.get(
            reverse('logic_lesson_detail', args=['ders-20-dogruluk-tablolari']),
        )

        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response['Location'],
            reverse('logic_lesson_detail', args=['ders-20-dogruluk-tablolari-i']),
        )

    def test_progress_endpoint_requires_login(self):
        response = self.post_progress({
            'lesson_slug': self.lesson_slug,
            'action': 'opened',
        })

        self.assertEqual(response.status_code, 401)
        self.assertFalse(response.json()['ok'])

    def test_grading_tracks_attempts_best_score_and_mastery(self):
        self.client.force_login(self.user)
        opened = self.post_progress({
            'lesson_slug': self.lesson_slug,
            'action': 'opened',
        })
        first = self.post_progress({
            'lesson_slug': self.lesson_slug,
            'action': 'graded',
            'score': LOGIC_MASTERY_THRESHOLD - 10,
        })
        mastered = self.post_progress({
            'lesson_slug': self.lesson_slug,
            'action': 'graded',
            'score': LOGIC_MASTERY_THRESHOLD + 10,
        })
        lower_retry = self.post_progress({
            'lesson_slug': self.lesson_slug,
            'action': 'graded',
            'score': 20,
        })

        self.assertEqual(opened.status_code, 200)
        self.assertEqual(first.json()['status'], LogicLessonProgress.STATUS_STARTED)
        self.assertEqual(mastered.json()['status'], LogicLessonProgress.STATUS_COMPLETED)
        self.assertEqual(lower_retry.json()['status'], LogicLessonProgress.STATUS_COMPLETED)
        progress = LogicLessonProgress.objects.get(
            user=self.user,
            lesson_slug=self.lesson_slug,
        )
        self.assertEqual(progress.attempt_count, 3)
        self.assertEqual(progress.last_score, 20)
        self.assertEqual(progress.best_score, LOGIC_MASTERY_THRESHOLD + 10)
        self.assertIsNotNone(progress.completed_at)

    def test_progress_cannot_be_completed_without_a_graded_score(self):
        self.client.force_login(self.user)

        response = self.post_progress({
            'lesson_slug': self.lesson_slug,
            'action': 'completed',
        })

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()['ok'])
        self.assertFalse(
            LogicLessonProgress.objects.filter(
                user=self.user,
                lesson_slug=self.lesson_slug,
            ).exists()
        )

    def test_logic_pages_are_in_sitemap(self):
        response = self.client.get(
            reverse('django.contrib.sitemaps.views.sitemap'),
            secure=True,
            HTTP_HOST='hafifayaklar.com',
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'https://hafifayaklar.com/mantik/')
        self.assertContains(
            response,
            'https://hafifayaklar.com/mantik/ders-1-onerme-nedir/',
        )

    def test_assessment_questions_stay_stable_until_new_attempt_is_requested(self):
        first = self.client.get(reverse('logic_level_test'))
        second = self.client.get(reverse('logic_level_test'))
        first_ids = [
            question['id']
            for exercise in first.context['assessment']['exercises']
            for question in exercise['questions']
        ]
        second_ids = [
            question['id']
            for exercise in second.context['assessment']['exercises']
            for question in exercise['questions']
        ]

        self.assertEqual(first_ids, second_ids)
        reset = self.client.get(reverse('logic_level_test'), {'yeni': '1'})
        self.assertRedirects(reset, reverse('logic_level_test'))
