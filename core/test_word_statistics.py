from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from core.models import Answer, Question
from core.word_statistics import excluded_word_set, word_tokens


class WordNormalizationTests(SimpleTestCase):
    def test_turkish_case_and_decomposed_letters_share_tokens(self):
        self.assertEqual(word_tokens('İNSAN insan IŞIK ışık I\u0307nsan'),
                         ['insan', 'insan', 'ışık', 'ışık', 'insan'])
        self.assertEqual(excluded_word_set(' İNSAN , ,  IŞIK  , insan'), {'insan', 'ışık'})


class WordStatisticsTests(TestCase):
    def setUp(self):
        cache.clear()
        self.addCleanup(cache.clear)
        self.author = User.objects.create_user(username='word-stat-reader')
        self.question = Question.objects.create(user=self.author, question_text='Okuma')
        self.entry = Answer.objects.create(user=self.author, question=self.question,
                                          answer_text='İNSAN insan ve kitap kitap kitap IŞIK ışık')
        Answer.objects.create(user=self.author, question=self.question, answer_text='kitap ve insan')
        self.client.force_login(self.author)
        self.site = reverse('site_statistics')
        self.profile = reverse('user_profile', args=[self.author.username])

    def test_site_exclusions_only_filter_frequency_list_not_search_or_totals(self):
        before = self.client.get(self.site).context
        response = self.client.get(self.site, {'exclude_words': ' insan , ve ', 'search_word': 'İNSAN'})
        self.assertEqual(response.context['search_word_count'], 3)
        top = dict(response.context['top_words'])
        self.assertNotIn('insan', top)
        self.assertNotIn('ve', top)
        self.assertEqual(top['kitap'], 4)
        for key in ['total_questions', 'total_answers', 'total_words', 'total_characters',
                    'avg_words_per_entry', 'avg_chars_per_entry']:
            self.assertEqual(response.context[key], before[key], key)
        self.entry.refresh_from_db()
        self.assertIn('İNSAN insan ve kitap', self.entry.answer_text)

    def test_site_search_handles_turkish_case_and_exact_words(self):
        for word, expected in [('İNSAN', 3), ('insan', 3), ('IŞIK', 2), ('kitap', 4), ('kita', 0)]:
            response = self.client.get(self.site, {'search_word': word, 'exclude_words': word})
            self.assertEqual(response.context['search_word_count'], expected)

    def test_profile_exclusions_preserve_search_other_words_and_entry_totals(self):
        before = self.client.get(self.profile, {'tab': 'kelimeler'}).context
        response = self.client.get(self.profile, {
            'tab': 'kelimeler', 'exclude_words': 'İNSAN, ve', 'search_word': 'insan',
        })
        self.assertEqual(response.context['search_word_count'], 3)
        self.assertNotIn('insan', dict(response.context['top_words']))
        self.assertEqual(dict(response.context['top_words'])['kitap'], 4)
        for key in ['total_entries', 'total_words', 'total_chars', 'avg_words_per_entry']:
            self.assertEqual(response.context[key], before[key], key)
        later = self.client.get(self.profile, {'tab': 'kelimeler', 'search_word': 'İNSAN'})
        self.assertEqual(later.context['search_word_count'], 3)
        self.assertNotIn('insan', dict(later.context['top_words']))
        restored = self.client.get(self.profile, {'tab': 'kelimeler', 'include_word': 'İNSAN'})
        self.assertEqual(dict(restored.context['top_words'])['insan'], 3)

    def test_visitor_exclusions_do_not_change_authors_preferences(self):
        other = User.objects.create_user(username='word-stat-visitor')
        self.client.force_login(other)
        self.client.get(self.profile, {'tab': 'kelimeler', 'exclude_word': 'kitap'})
        self.author.userprofile.refresh_from_db()
        self.assertEqual(self.author.userprofile.excluded_words, '')
