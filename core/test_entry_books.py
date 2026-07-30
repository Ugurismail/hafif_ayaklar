import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.models import Answer, EntryBook, Question


class EntryBookApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='book-owner',
            password='pass',
        )
        self.other_user = User.objects.create_user(
            username='other-book-owner',
            password='pass',
        )
        self.question = Question.objects.create(
            question_text='Kitap başlığı',
            user=self.user,
        )
        self.first_answer = Answer.objects.create(
            question=self.question,
            user=self.user,
            answer_text='Birinci kitap entrysi',
        )
        self.second_answer = Answer.objects.create(
            question=self.question,
            user=self.user,
            answer_text='İkinci kitap entrysi',
        )
        self.other_answer = Answer.objects.create(
            question=self.question,
            user=self.other_user,
            answer_text='Başka kullanıcı entrysi',
        )
        self.client.force_login(self.user)

    def _json_request(self, method, url, payload=None):
        return getattr(self.client, method)(
            url,
            data=json.dumps(payload or {}),
            content_type='application/json',
        )

    def test_book_can_be_created_and_loaded_in_custom_order(self):
        create_response = self._json_request(
            'post',
            reverse('entry_books'),
            {
                'title': 'Felsefe Kitabım',
                'entry_ids': [self.second_answer.id, self.first_answer.id],
            },
        )

        self.assertEqual(create_response.status_code, 201)
        book_id = create_response.json()['book']['id']
        detail_response = self.client.get(
            reverse('entry_book_detail', args=[book_id]),
        )

        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(
            [
                entry['id']
                for entry in detail_response.json()['book']['entries']
            ],
            [self.second_answer.id, self.first_answer.id],
        )

    def test_book_can_be_renamed_and_its_entries_replaced(self):
        book = EntryBook.objects.create(user=self.user, title='Eski Ad')
        book.items.create(answer=self.first_answer, position=1)

        update_response = self._json_request(
            'put',
            reverse('entry_book_detail', args=[book.id]),
            {
                'title': 'Yeni Ad',
                'entry_ids': [self.second_answer.id],
            },
        )

        self.assertEqual(update_response.status_code, 200)
        book.refresh_from_db()
        self.assertEqual(book.title, 'Yeni Ad')
        self.assertEqual(
            list(book.items.values_list('answer_id', flat=True)),
            [self.second_answer.id],
        )

    def test_book_rejects_entries_owned_by_another_user(self):
        response = self._json_request(
            'post',
            reverse('entry_books'),
            {
                'title': 'Geçersiz Kitap',
                'entry_ids': [self.first_answer.id, self.other_answer.id],
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(EntryBook.objects.filter(user=self.user).exists())

    def test_users_cannot_see_or_change_each_others_books(self):
        other_book = EntryBook.objects.create(
            user=self.other_user,
            title='Gizli Kitap',
        )
        own_book = EntryBook.objects.create(
            user=self.user,
            title='Benim Kitabım',
        )
        own_book.items.create(answer=self.first_answer, position=1)

        list_response = self.client.get(reverse('entry_books'))
        foreign_detail = self.client.get(
            reverse('entry_book_detail', args=[other_book.id]),
        )

        self.assertEqual(
            [book['id'] for book in list_response.json()['books']],
            [own_book.id],
        )
        self.assertEqual(foreign_detail.status_code, 404)

    def test_book_can_be_deleted(self):
        book = EntryBook.objects.create(user=self.user, title='Silinecek Kitap')
        book.items.create(answer=self.first_answer, position=1)

        response = self.client.delete(
            reverse('entry_book_detail', args=[book.id]),
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(EntryBook.objects.filter(id=book.id).exists())

    def test_entry_can_be_appended_to_book_without_creating_a_duplicate(self):
        book = EntryBook.objects.create(user=self.user, title='Büyüyen Kitap')
        book.items.create(answer=self.first_answer, position=1)
        url = reverse('entry_book_add_entry', args=[book.id])

        add_response = self._json_request(
            'post',
            url,
            {'entry_id': self.second_answer.id},
        )
        duplicate_response = self._json_request(
            'post',
            url,
            {'entry_id': self.second_answer.id},
        )

        self.assertEqual(add_response.status_code, 200)
        self.assertTrue(add_response.json()['added'])
        self.assertEqual(duplicate_response.status_code, 200)
        self.assertFalse(duplicate_response.json()['added'])
        self.assertEqual(
            list(
                book.items.order_by('position').values_list(
                    'answer_id',
                    flat=True,
                )
            ),
            [self.first_answer.id, self.second_answer.id],
        )

    def test_book_list_marks_books_that_already_contain_the_entry(self):
        containing_book = EntryBook.objects.create(
            user=self.user,
            title='Entry Var',
        )
        containing_book.items.create(answer=self.first_answer, position=1)
        EntryBook.objects.create(user=self.user, title='Entry Yok')

        response = self.client.get(
            reverse('entry_books'),
            {'entry_id': self.first_answer.id},
        )

        self.assertEqual(response.status_code, 200)
        books = {
            book['title']: book['contains_entry']
            for book in response.json()['books']
        }
        self.assertEqual(books, {'Entry Yok': False, 'Entry Var': True})

    def test_entry_from_another_user_cannot_be_added_to_book(self):
        book = EntryBook.objects.create(user=self.user, title='Benim Kitabım')

        response = self._json_request(
            'post',
            reverse('entry_book_add_entry', args=[book.id]),
            {'entry_id': self.other_answer.id},
        )

        self.assertEqual(response.status_code, 404)
        self.assertFalse(book.items.exists())

    def test_profile_contains_entry_book_controls(self):
        response = self.client.get(
            reverse('user_profile', args=[self.user.username]),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="entryBookSelect"')
        self.assertContains(response, 'id="entryBookName"')
        self.assertContains(response, 'id="saveEntryBookButton"')
        self.assertContains(response, 'css/profile.css')
        self.assertContains(response, 'data-entry-book-add')
        self.assertContains(response, 'id="entryBookQuickAddModal"')
        self.assertContains(response, 'entry_books.js')
