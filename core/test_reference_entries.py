from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from .models import Answer, Question, Reference


class ReferenceUsageTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username='sourceuser', password='testpass123')
        self.reference = Reference.objects.create(
            author_surname='Arendt',
            author_name='Hannah',
            year=1958,
            metin_ismi='The Human Condition',
            rest='University of Chicago Press.',
            abbreviation='HC',
            created_by=self.user,
        )
        self.question = Question.objects.create(
            question_text='Kaynaklı başlık',
            user=self.user,
        )
        self.first_answer = Answer.objects.create(
            question=self.question,
            user=self.user,
            answer_text=(
                f'İlk kullanım (kaynak:{self.reference.id}, sayfa:12). '
                f'İkinci kullanım (k:{self.reference.id} s:18).'
            ),
        )
        self.second_answer = Answer.objects.create(
            question=self.question,
            user=self.user,
            answer_text=f'Boşluklu kullanım (KAYNAK : {self.reference.id}, s : 21-22).',
        )
        self.decoy_answer = Answer.objects.create(
            question=self.question,
            user=self.user,
            answer_text=f'Farklı kaynak (kaynak:{self.reference.id}0, sayfa:9).',
        )
        self.client.force_login(self.user)

    def test_reference_usage_data_lists_exact_matches_with_pages(self):
        response = self.client.get(reverse('reference_usage_data', args=[self.reference.id]))

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['counts'], {'entries': 2, 'usages': 3})
        self.assertEqual(
            {entry['id'] for entry in payload['entries']},
            {self.first_answer.id, self.second_answer.id},
        )
        first_entry = next(entry for entry in payload['entries'] if entry['id'] == self.first_answer.id)
        self.assertEqual(first_entry['usage_count'], 2)
        self.assertEqual(first_entry['pages'], ['12', '18'])
        self.assertIn('İlk kullanım', first_entry['excerpt'])
        self.assertEqual(
            first_entry['url'],
            reverse('single_answer', args=[self.question.slug, self.first_answer.id]),
        )
        self.assertNotIn(self.decoy_answer.id, {entry['id'] for entry in payload['entries']})

    def test_reference_usage_data_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('reference_usage_data', args=[self.reference.id]))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_profile_and_statistics_include_usage_modal_trigger(self):
        usage_url = reverse('reference_usage_data', args=[self.reference.id])

        profile_response = self.client.get(
            reverse('user_profile', args=[self.user.username]),
            {'tab': 'kaynaklarim'},
        )
        statistics_response = self.client.get(reverse('site_statistics'), {'tab': 'references'})

        self.assertEqual(profile_response.status_code, 200)
        self.assertEqual(statistics_response.status_code, 200)
        self.assertContains(profile_response, f'data-reference-usage-url="{usage_url}"')
        self.assertContains(statistics_response, f'data-reference-usage-url="{usage_url}"')
        self.assertContains(profile_response, 'id="referenceUsageModal"')
        self.assertContains(statistics_response, 'id="referenceUsageModal"')

    def test_reference_ajax_response_includes_usage_url(self):
        response = self.client.get(reverse('get_references'), {
            'scope': 'all',
            'q': 'Arendt',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['references'][0]['usage_url'],
            reverse('reference_usage_data', args=[self.reference.id]),
        )

    def test_reference_search_orders_direct_match_before_details_match(self):
        details_match = Reference.objects.create(
            author_surname='Aardvark',
            author_name='Ada',
            year=2020,
            metin_ismi='Başka Bir Kitap',
            rest='Arendt üzerine açıklamalar.',
            created_by=self.user,
        )

        response = self.client.get(reverse('get_references'), {
            'scope': 'all',
            'q': 'Arendt',
            'sort': 'relevance',
        })

        self.assertEqual(response.status_code, 200)
        reference_ids = [item['id'] for item in response.json()['references']]
        self.assertEqual(reference_ids[0], self.reference.id)
        self.assertIn(details_match.id, reference_ids)

    def test_reference_usage_data_is_paginated(self):
        for index in range(7):
            Answer.objects.create(
                question=self.question,
                user=self.user,
                answer_text=f'Ek kullanım {index} (kaynak:{self.reference.id}, sayfa:{index + 30}).',
            )

        first_page = self.client.get(reverse('reference_usage_data', args=[self.reference.id])).json()
        second_page = self.client.get(
            reverse('reference_usage_data', args=[self.reference.id]),
            {'page': 2},
        ).json()

        self.assertEqual(first_page['counts']['entries'], 9)
        self.assertEqual(len(first_page['entries']), 8)
        self.assertTrue(first_page['pagination']['has_next'])
        self.assertEqual(first_page['pagination']['next_page'], 2)
        self.assertEqual(len(second_page['entries']), 1)
        self.assertFalse(second_page['pagination']['has_next'])
