from datetime import timedelta
from importlib import import_module

from django.contrib import admin
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import connection
from django.db.migrations.loader import MigrationLoader
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import NoReverseMatch, resolve, reverse
from django.utils import timezone

from .models import (
    CikisTesti, CikisTestiResult, CikisTestiSik, CikisTestiSoru,
    RadioChatMessage, RadioProgram, UserProfile,
)
from .views.retired_views import retired_feature


class RetiredFeatureTests(TestCase):
    def setUp(self):
        cache.clear()
        self.addCleanup(cache.clear)
        self.user = User.objects.create_user(username='retirement-reader')

    def test_old_routes_are_gone_for_visitors_and_members(self):
        paths = [
            '/radio/', '/radio/program/1/', '/radio/dj/', '/radio/dj/create/',
            '/radio/dj/edit/1/', '/radio/dj/delete/1/', '/radio/dj/start/1/',
            '/radio/dj/stop/1/', '/radio/token/1/', '/radio/listener-count/1/',
            '/radio/chat/1/', '/cikis_testleri/', '/cikis_testleri/olustur/',
            '/cikis_testleri/1/', '/cikis_testleri/1/soru_ekle/',
            '/cikis_testleri/soru/1/sik_ekle/', '/cikis_testleri/soru/1/dogru_sik/',
            '/cikis_testleri/1/coz/', '/cikis_testleri/1/sonuclar/',
            '/cikis_testleri/1/dogru_ayarla/', '/cikis-testleri/',
            '/cikis-test/1/coz/', '/cikis_testleri/sonuc/1/sil/',
            '/cikis_testleri/soru/1/edit/', '/cikis_testleri/soru/1/sil/',
            '/cikis_testi/1/sil/', '/cikis_testleri/sik/1/edit/',
            '/radio', '/cikis-testleri',
        ]
        for authenticated in (False, True):
            if authenticated:
                self.client.force_login(self.user)
            for path in paths:
                self.assertIs(resolve(path).func, retired_feature)
                for method in ('get', 'post', 'delete'):
                    with self.subTest(path=path, method=method, authenticated=authenticated):
                        response = getattr(self.client, method)(path)
                        self.assertEqual(response.status_code, 410)
                        self.assertEqual(response['X-Robots-Tag'], 'noindex')

    def test_old_named_routes_and_admin_editors_are_removed(self):
        for name in ('radio_home', 'get_agora_token', 'cikis_test_list', 'cikis_testleri_list'):
            with self.assertRaises(NoReverseMatch):
                reverse(name)
        for model in (RadioProgram, RadioChatMessage, CikisTesti, CikisTestiSoru, CikisTestiSik, CikisTestiResult):
            self.assertFalse(admin.site.is_registered(model))
        self.assertTrue(admin.site.is_registered(UserProfile))

    def test_home_renders_without_radio_queries_or_links(self):
        self.client.force_login(self.user)
        with CaptureQueriesContext(connection) as captured:
            response = self.client.get(reverse('user_homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '/radio/')
        self.assertNotContains(response, 'radio-live')
        self.assertNotContains(response, 'agora.io')
        for query in captured:
            self.assertNotIn('core_radioprogram', query['sql'].lower())
            self.assertNotIn('core_radiochatmessage', query['sql'].lower())

    def test_archived_records_are_not_deleted_or_mutated(self):
        now = timezone.now()
        program = RadioProgram.objects.create(
            dj=self.user, title='Archived broadcast', start_time=now,
            end_time=now + timedelta(hours=1), listener_count=7,
        )
        test = CikisTesti.objects.create(owner=self.user, title='Archived test')
        self.client.post(f'/radio/listener-count/{program.pk}/', {'count': 100})
        self.client.post(f'/radio/dj/delete/{program.pk}/')
        self.client.post(f'/cikis_testi/{test.pk}/sil/')
        program.refresh_from_db()
        self.assertEqual(program.listener_count, 7)
        self.assertTrue(CikisTesti.objects.filter(pk=test.pk).exists())

    def test_attendance_permission_uses_existing_column_and_remains_restricted(self):
        self.client.force_login(self.user)
        url = reverse('attendance_sheet_tool')
        self.assertEqual(self.client.get(url).status_code, 403)
        field = UserProfile._meta.get_field('can_manage_attendance')
        self.assertEqual(field.column, 'is_dj')
        with connection.cursor() as cursor:
            cursor.execute('UPDATE core_userprofile SET is_dj = %s WHERE user_id = %s', [True, self.user.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertEqual(self.client.get(reverse('attendance_sheet_day_state')).status_code, 200)
        response = self.client.get(reverse('user_homepage'))
        self.assertContains(response, url)
        UserProfile.objects.filter(user=self.user).update(can_manage_attendance=False)
        self.assertEqual(self.client.get(url).status_code, 403)
        self.user.is_staff = True
        self.user.save()
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_permission_migration_preserves_schema_and_is_reversible(self):
        loader = MigrationLoader(connection)
        before = loader.project_state([('core', '0062_habit_reminder_enabled_habit_reminder_time_and_more')])
        migration = import_module('core.migrations.0063_attendance_permission_name').Migration
        operation = migration.operations[0]
        self.assertEqual(operation.database_operations, [])
        after = before.clone()
        operation.state_forwards('core', after)
        old_field = before.apps.get_model('core', 'UserProfile')._meta.get_field('is_dj')
        new_field = after.apps.get_model('core', 'UserProfile')._meta.get_field('can_manage_attendance')
        self.assertEqual(old_field.column, new_field.column)
        editor = connection.schema_editor(collect_sql=True)
        operation.database_forwards('core', editor, before, after)
        operation.database_backwards('core', editor, after, before)
        self.assertEqual(editor.collected_sql, [])
