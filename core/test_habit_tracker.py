import json
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Habit, HabitEntry, MoneyCategory, MoneyTransaction


class HabitTrackerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='habit-user', password='pass1234')
        self.other_user = User.objects.create_user(username='other-habit-user', password='pass1234')
        self.today = timezone.localdate()

    def post_json(self, name, payload=None, args=None):
        return self.client.post(
            reverse(name, args=args or []),
            data=json.dumps(payload or {}),
            content_type='application/json',
        )

    def create_habit(self, **overrides):
        values = {
            'user': self.user,
            'name': 'Oku',
            'target': 20,
            'unit': 'sayfa',
            'start_date': self.today,
        }
        values.update(overrides)
        return Habit.objects.create(**values)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('habit_tracker'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_dashboard_renders_for_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('habit_tracker'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alışkanlıklar')
        self.assertContains(response, 'habitTrackerInitialData')

    def test_create_habit_normalizes_owned_data(self):
        self.client.force_login(self.user)
        response = self.post_json('habit_create', {
            'name': '  Su iç  ',
            'description': 'Günlük su hedefi',
            'target': 8,
            'unit': 'bardak',
            'icon': 'droplet',
            'color': '#3D6F8E',
            'frequency': 'custom',
            'scheduleDays': [0, 2, 4, 4, 12],
            'startDate': self.today.isoformat(),
            'date': self.today.isoformat(),
        })
        self.assertEqual(response.status_code, 201)
        habit = Habit.objects.get(user=self.user)
        self.assertEqual(habit.name, 'Su iç')
        self.assertEqual(habit.schedule_days, [0, 2, 4])
        self.assertEqual(habit.target, 8)
        self.assertEqual(response.json()['data']['habits'][0]['id'], habit.id)

    def test_custom_frequency_requires_at_least_one_day(self):
        self.client.force_login(self.user)
        response = self.post_json('habit_create', {
            'name': 'Koşu',
            'target': 1,
            'frequency': 'custom',
            'scheduleDays': [],
            'startDate': self.today.isoformat(),
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Habit.objects.filter(user=self.user).exists())

    def test_dashboard_data_is_private_per_user(self):
        own_habit = self.create_habit(name='Benim alışkanlığım')
        Habit.objects.create(
            user=self.other_user,
            name='Başkasının alışkanlığı',
            start_date=self.today,
        )
        HabitEntry.objects.create(habit=own_habit, date=self.today, value=20)

        self.client.force_login(self.user)
        response = self.client.get(reverse('habit_tracker_data'), {'date': self.today.isoformat()})
        self.assertEqual(response.status_code, 200)
        names = [habit['name'] for habit in response.json()['data']['habits']]
        self.assertEqual(names, ['Benim alışkanlığım'])
        self.assertEqual(response.json()['data']['summary']['rate'], 100)

    def test_log_increment_toggle_and_decrement(self):
        habit = self.create_habit(target=2)
        self.client.force_login(self.user)
        base_payload = {'date': self.today.isoformat()}

        response = self.post_json('habit_log', {**base_payload, 'action': 'increment'}, [habit.id])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(HabitEntry.objects.get(habit=habit, date=self.today).value, 1)

        response = self.post_json('habit_log', {**base_payload, 'action': 'toggle'}, [habit.id])
        self.assertEqual(response.json()['data']['summary']['rate'], 100)
        self.assertEqual(HabitEntry.objects.get(habit=habit, date=self.today).value, 2)

        self.post_json('habit_log', {**base_payload, 'action': 'decrement'}, [habit.id])
        self.assertEqual(HabitEntry.objects.get(habit=habit, date=self.today).value, 1)

    def test_unscheduled_day_cannot_be_logged(self):
        scheduled_day = (self.today.weekday() + 1) % 7
        habit = self.create_habit(
            frequency=Habit.FREQUENCY_CUSTOM,
            schedule_days=[scheduled_day],
        )
        self.client.force_login(self.user)
        response = self.post_json('habit_log', {
            'date': self.today.isoformat(),
            'action': 'increment',
        }, [habit.id])
        self.assertEqual(response.status_code, 400)
        self.assertFalse(HabitEntry.objects.filter(habit=habit).exists())

    def test_user_cannot_mutate_another_users_habit(self):
        habit = Habit.objects.create(
            user=self.other_user,
            name='Gizli',
            start_date=self.today,
        )
        self.client.force_login(self.user)
        endpoints = ('habit_update', 'habit_log', 'habit_archive', 'habit_delete')
        for endpoint_name in endpoints:
            with self.subTest(endpoint=endpoint_name):
                response = self.post_json(endpoint_name, {
                    'name': 'Değiştir',
                    'date': self.today.isoformat(),
                }, [habit.id])
                self.assertEqual(response.status_code, 404)
        self.assertTrue(Habit.objects.filter(id=habit.id, user=self.other_user).exists())

    def test_update_archive_restore_and_delete(self):
        habit = self.create_habit()
        self.client.force_login(self.user)
        response = self.post_json('habit_update', {
            'name': 'Her gün oku',
            'target': 30,
            'unit': 'sayfa',
            'frequency': 'daily',
            'startDate': self.today.isoformat(),
            'date': self.today.isoformat(),
        }, [habit.id])
        self.assertEqual(response.status_code, 200)
        habit.refresh_from_db()
        self.assertEqual(habit.name, 'Her gün oku')
        self.assertEqual(habit.target, 30)

        response = self.post_json('habit_archive', {'date': self.today.isoformat()}, [habit.id])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['habits'], [])
        self.assertEqual(response.json()['data']['summary']['scheduled'], 0)
        self.assertEqual(response.json()['data']['archivedHabits'][0]['id'], habit.id)

        response = self.post_json('habit_archive', {'date': self.today.isoformat()}, [habit.id])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['habits'][0]['id'], habit.id)

        response = self.post_json('habit_delete', {'date': self.today.isoformat()}, [habit.id])
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Habit.objects.filter(id=habit.id).exists())

    def test_one_entry_per_habit_and_day(self):
        habit = self.create_habit()
        HabitEntry.objects.create(habit=habit, date=self.today, value=1)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                HabitEntry.objects.create(habit=habit, date=self.today, value=2)

    def test_daily_target_can_override_default_for_one_date(self):
        habit = self.create_habit(target=20)
        self.client.force_login(self.user)
        response = self.post_json('habit_log', {
            'date': self.today.isoformat(),
            'action': 'set_day',
            'target': 30,
            'value': 25,
            'note': 'Bugün daha uzun okudum.',
        }, [habit.id])
        self.assertEqual(response.status_code, 200)
        entry = HabitEntry.objects.get(habit=habit, date=self.today)
        self.assertEqual(entry.target, 30)
        self.assertEqual(entry.value, 25)
        payload = response.json()['data']['habits'][0]
        self.assertEqual(payload['defaultTarget'], 20)
        self.assertEqual(payload['target'], 30)
        self.assertTrue(payload['targetOverridden'])
        self.assertEqual(payload['rate'], 83)

    def test_daily_target_equal_to_default_is_not_stored_as_override(self):
        habit = self.create_habit(target=20)
        self.client.force_login(self.user)
        response = self.post_json('habit_log', {
            'date': self.today.isoformat(),
            'action': 'set_day',
            'target': 20,
            'value': 5,
        }, [habit.id])
        self.assertEqual(response.status_code, 200)
        entry = HabitEntry.objects.get(habit=habit, date=self.today)
        self.assertIsNone(entry.target)
        self.assertFalse(response.json()['data']['habits'][0]['targetOverridden'])


class MoneyTrackerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='money-user', password='pass1234')
        self.other_user = User.objects.create_user(username='other-money-user', password='pass1234')
        self.today = timezone.localdate()

    def post_json(self, name, payload=None, args=None):
        return self.client.post(
            reverse(name, args=args or []),
            data=json.dumps(payload or {}),
            content_type='application/json',
        )

    def test_money_data_requires_login_and_creates_private_defaults(self):
        response = self.client.get(reverse('money_tracker_data'))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.user)
        response = self.client.get(reverse('money_tracker_data'))
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()['data']['categories']), 10)
        self.assertFalse(MoneyCategory.objects.filter(user=self.other_user).exists())

    def test_create_income_and_expense_updates_month_summary(self):
        self.client.force_login(self.user)
        data = self.client.get(reverse('money_tracker_data')).json()['data']
        expense_category = next(item for item in data['categories'] if item['kind'] == 'expense')
        income_category = next(item for item in data['categories'] if item['kind'] == 'income')

        expense_response = self.post_json('money_transaction_create', {
            'kind': 'expense',
            'amount': '125.50',
            'categoryId': expense_category['id'],
            'date': self.today.isoformat(),
            'note': 'Market',
            'month': self.today.strftime('%Y-%m'),
        })
        self.assertEqual(expense_response.status_code, 201)
        income_response = self.post_json('money_transaction_create', {
            'kind': 'income',
            'amount': '500',
            'categoryId': income_category['id'],
            'date': self.today.isoformat(),
            'month': self.today.strftime('%Y-%m'),
        })
        self.assertEqual(income_response.status_code, 201)
        summary = income_response.json()['data']['summary']
        self.assertEqual(Decimal(summary['expense']), Decimal('125.50'))
        self.assertEqual(Decimal(summary['income']), Decimal('500.00'))
        self.assertEqual(Decimal(summary['balance']), Decimal('374.50'))

    def test_category_must_belong_to_user_and_match_kind(self):
        foreign_category = MoneyCategory.objects.create(
            user=self.other_user,
            name='Gizli',
            kind=MoneyCategory.KIND_EXPENSE,
        )
        self.client.force_login(self.user)
        response = self.post_json('money_transaction_create', {
            'kind': 'expense',
            'amount': '10',
            'categoryId': foreign_category.id,
            'date': self.today.isoformat(),
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(MoneyTransaction.objects.filter(user=self.user).exists())

    def test_user_cannot_update_or_delete_another_users_transaction(self):
        category = MoneyCategory.objects.create(
            user=self.other_user,
            name='Özel',
            kind=MoneyCategory.KIND_EXPENSE,
        )
        item = MoneyTransaction.objects.create(
            user=self.other_user,
            kind=MoneyTransaction.KIND_EXPENSE,
            amount=Decimal('20.00'),
            category=category,
            date=self.today,
        )
        self.client.force_login(self.user)
        for name in ('money_transaction_update', 'money_transaction_delete'):
            with self.subTest(name=name):
                response = self.post_json(name, {'month': self.today.strftime('%Y-%m')}, [item.id])
                self.assertEqual(response.status_code, 404)
        self.assertTrue(MoneyTransaction.objects.filter(id=item.id).exists())

    def test_user_can_create_a_custom_category_but_not_a_duplicate(self):
        self.client.force_login(self.user)
        response = self.post_json('money_category_create', {
            'kind': MoneyCategory.KIND_EXPENSE,
            'name': 'Kitap',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['category']['name'], 'Kitap')

        duplicate = self.post_json('money_category_create', {
            'kind': MoneyCategory.KIND_EXPENSE,
            'name': 'kitap',
        })
        self.assertEqual(duplicate.status_code, 400)
        self.assertEqual(
            MoneyCategory.objects.filter(user=self.user, kind='expense', name__iexact='kitap').count(),
            1,
        )

    def test_owner_can_update_and_delete_a_transaction(self):
        category = MoneyCategory.objects.create(
            user=self.user,
            name='Market',
            kind=MoneyCategory.KIND_EXPENSE,
        )
        item = MoneyTransaction.objects.create(
            user=self.user,
            kind=MoneyTransaction.KIND_EXPENSE,
            amount=Decimal('20.00'),
            category=category,
            date=self.today,
        )
        self.client.force_login(self.user)
        response = self.post_json('money_transaction_update', {
            'kind': MoneyTransaction.KIND_EXPENSE,
            'amount': '35.75',
            'categoryId': category.id,
            'date': self.today.isoformat(),
            'note': 'Güncellendi',
            'month': self.today.strftime('%Y-%m'),
        }, [item.id])
        self.assertEqual(response.status_code, 200)
        item.refresh_from_db()
        self.assertEqual(item.amount, Decimal('35.75'))
        self.assertEqual(item.note, 'Güncellendi')

        response = self.post_json('money_transaction_delete', {
            'month': self.today.strftime('%Y-%m'),
        }, [item.id])
        self.assertEqual(response.status_code, 200)
        self.assertFalse(MoneyTransaction.objects.filter(id=item.id).exists())

    def test_future_transaction_is_rejected(self):
        self.client.force_login(self.user)
        category = MoneyCategory.objects.create(
            user=self.user,
            name='Market',
            kind=MoneyCategory.KIND_EXPENSE,
        )
        response = self.post_json('money_transaction_create', {
            'kind': MoneyTransaction.KIND_EXPENSE,
            'amount': '10',
            'categoryId': category.id,
            'date': (self.today + timedelta(days=1)).isoformat(),
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(MoneyTransaction.objects.filter(user=self.user).exists())
