from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from .models import Answer, Question, Reference


class ReferenceEntriesTests(TestCase):
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

    def test_reference_entries_lists_exact_matches_with_pages(self):
        response = self.client.get(reverse('reference_entries', args=[self.reference.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['unique_entry_count'], 2)
        self.assertEqual(response.context['total_citation_count'], 3)

        entries = list(response.context['entries_page'].object_list)
        self.assertEqual({entry.id for entry in entries}, {self.first_answer.id, self.second_answer.id})
        first_entry = next(entry for entry in entries if entry.id == self.first_answer.id)
        self.assertEqual(first_entry.reference_citation_count, 2)
        self.assertEqual(first_entry.reference_pages, ['12', '18'])
        self.assertNotContains(response, self.decoy_answer.answer_text)
        self.assertContains(
            response,
            reverse('single_answer', args=[self.question.slug, self.first_answer.id]),
        )

    def test_reference_entries_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('reference_entries', args=[self.reference.id]))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_profile_and_statistics_link_to_reference_entries(self):
        entries_url = reverse('reference_entries', args=[self.reference.id])

        profile_response = self.client.get(
            reverse('user_profile', args=[self.user.username]),
            {'tab': 'kaynaklarim'},
        )
        statistics_response = self.client.get(reverse('site_statistics'), {'tab': 'references'})

        self.assertEqual(profile_response.status_code, 200)
        self.assertEqual(statistics_response.status_code, 200)
        self.assertContains(profile_response, entries_url)
        self.assertContains(statistics_response, entries_url)

    def test_reference_ajax_response_includes_entries_url(self):
        response = self.client.get(reverse('get_references'), {
            'scope': 'all',
            'q': 'Arendt',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['references'][0]['entries_url'],
            reverse('reference_entries', args=[self.reference.id]),
        )
