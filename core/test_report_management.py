from unittest.mock import patch

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import Client, TestCase
from django.urls import reverse

from .content_reports import save_content_report
from .models import Answer, ContentReport, Notification, Question


class ReportManagementTests(TestCase):
    def setUp(self):
        self.reporter = User.objects.create_user('reporter')
        self.author = User.objects.create_user('author')
        self.staff = User.objects.create_user('manager', is_staff=True)
        self.superuser = User.objects.create_user('super', is_superuser=True)
        self.inactive = User.objects.create_user('inactive', is_staff=True, is_active=False)
        self.question = Question.objects.create(user=self.author, question_text='Reported topic')
        self.answer = Answer.objects.create(user=self.author, question=self.question, answer_text='<script>alert(1)</script> Entry')
        self.client.force_login(self.reporter)

    def create_report(self, obj=None):
        return save_content_report(self.reporter, obj or self.answer, 'spam', 'Private report')[0]

    def review_url(self, report):
        return reverse('report_review', args=[report.pk])

    def test_both_report_endpoints_notify_only_active_managers_once(self):
        for route, kind, obj in (('report_content', 'question', self.question),
                                 ('report_content_ajax', 'answer', self.answer)):
            with self.subTest(route=route):
                data = {'content_type': kind, 'object_id': obj.pk, 'reason': 'spam', 'details': 'Private report'}
                response = self.client.post(reverse(route), data)
                self.assertEqual(response.status_code, 302 if route == 'report_content' else 200)
                report = ContentReport.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.pk)
                notices = Notification.objects.filter(related_report=report)
                self.assertEqual(set(notices.values_list('recipient_id', flat=True)), {self.staff.pk, self.superuser.pk})
                self.client.post(reverse(route), data)
                data['details'] = 'Updated private text'
                self.client.post(reverse(route), data)
                self.assertEqual(notices.count(), 2)
                self.assertEqual(notices.first().get_target_url(), self.review_url(report))
                self.assertNotIn('Private', notices.first().message)

    def test_reopening_reviewed_report_notifies_again_and_resets_review(self):
        report = self.create_report()
        report.status = 'dismissed'
        report.resolution_note = 'Old review'
        report.reviewed_by = self.staff
        report.save()
        updated, created = save_content_report(self.reporter, self.answer, 'other', 'New information')
        self.assertFalse(created)
        self.assertEqual(updated.status, 'open')
        self.assertIsNone(updated.reviewed_by)
        self.assertEqual(updated.resolution_note, '')
        self.assertEqual(Notification.objects.filter(related_report=report).count(), 4)
        save_content_report(self.reporter, self.answer, 'other', 'New information')
        self.assertEqual(Notification.objects.filter(related_report=report).count(), 4)

    def test_notification_failure_rolls_back_report(self):
        with patch('core.content_reports.Notification.objects.bulk_create', side_effect=RuntimeError('test')):
            with self.assertRaises(RuntimeError):
                self.create_report()
        self.assertFalse(ContentReport.objects.exists())

    def test_inbox_and_review_are_private_including_posts(self):
        report = self.create_report()
        urls = (reverse('report_inbox'), self.review_url(report))
        for url in urls:
            self.assertEqual(Client().get(url).status_code, 302)
            self.assertEqual(self.client.get(url).status_code, 403)
            self.assertEqual(self.client.post(url, {'status': 'dismissed'}).status_code, 403)
        for manager in (self.staff, self.superuser):
            self.client.force_login(manager)
            for url in urls:
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response['X-Robots-Tag'], 'noindex, nofollow')
                self.assertIn('no-store', response['Cache-Control'])
        self.superuser.is_superuser = False
        self.superuser.save()
        self.assertEqual(self.client.get(self.review_url(report)).status_code, 403)

    def test_bell_count_and_notification_target_and_menu(self):
        report = self.create_report()
        self.client.force_login(self.staff)
        self.assertEqual(self.client.get(reverse('navbar_status')).json()['notification_count'], 1)
        response = self.client.get(reverse('notification_list'))
        self.assertContains(response, self.review_url(report))
        self.assertContains(response, reverse('report_inbox'))
        self.client.force_login(self.reporter)
        response = self.client.get(reverse('notification_list'))
        self.assertNotContains(response, reverse('report_inbox'))

    def test_review_is_post_only_csrf_protected_and_records_reviewer(self):
        report = self.create_report()
        self.client.force_login(self.staff)
        url = self.review_url(report)
        response = self.client.get(url, {'status': 'dismissed'})
        report.refresh_from_db()
        self.assertEqual(report.status, 'open')
        data = {'status': 'reviewed', 'resolution_note': 'Checked', 'version': report.updated_at.isoformat()}
        protected = Client(enforce_csrf_checks=True)
        protected.force_login(self.staff)
        self.assertEqual(protected.post(url, data).status_code, 403)
        self.assertRedirects(self.client.post(url, data), url)
        report.refresh_from_db()
        self.assertEqual((report.status, report.resolution_note, report.reviewed_by), ('reviewed', 'Checked', self.staff))
        self.assertIsNotNone(report.reviewed_at)
        self.assertFalse(Notification.objects.filter(recipient=self.staff, is_read=False).exists())
        self.assertTrue(Notification.objects.filter(recipient=self.superuser, is_read=False).exists())
        self.assertTrue(Answer.objects.filter(pk=self.answer.pk).exists())

    def test_stale_review_cannot_overwrite_updated_report(self):
        report = self.create_report()
        version = report.updated_at.isoformat()
        save_content_report(self.reporter, self.answer, 'abuse', 'Changed while manager was reading')
        self.client.force_login(self.staff)
        response = self.client.post(self.review_url(report), {'status': 'dismissed', 'version': version})
        self.assertEqual(response.status_code, 409)
        report.refresh_from_db()
        self.assertEqual(report.status, 'open')
        self.assertEqual(report.reason, 'abuse')

    def test_invalid_review_data_does_not_change_report(self):
        report = self.create_report()
        self.client.force_login(self.staff)
        for fields in ({'status': 'bad'}, {'resolution_note': 'x' * 2001}, {'version': ''}):
            data = {'status': 'reviewed', 'version': report.updated_at.isoformat()}
            data.update(fields)
            self.assertEqual(self.client.post(self.review_url(report), data).status_code, 400)
        report.refresh_from_db()
        self.assertEqual(report.status, 'open')

    def test_second_manager_cannot_replace_first_managers_decision(self):
        report = self.create_report()
        data = {'status': 'dismissed', 'resolution_note': 'First decision', 'version': report.updated_at.isoformat()}
        self.client.force_login(self.staff)
        self.assertEqual(self.client.post(self.review_url(report), data).status_code, 302)
        self.client.force_login(self.superuser)
        data['status'] = 'actioned'
        self.assertEqual(self.client.post(self.review_url(report), data).status_code, 409)
        report.refresh_from_db()
        self.assertEqual((report.status, report.reviewed_by), ('dismissed', self.staff))

    def test_rejected_submissions_do_not_notify(self):
        self.client.force_login(self.author)
        data = {'content_type': 'answer', 'object_id': self.answer.pk, 'reason': 'spam'}
        self.assertEqual(self.client.post(reverse('report_content_ajax'), data).status_code, 400)
        self.client.force_login(self.reporter)
        data['reason'] = 'invalid'
        self.assertEqual(self.client.post(reverse('report_content_ajax'), data).status_code, 400)
        self.assertFalse(ContentReport.objects.exists())
        self.assertFalse(Notification.objects.filter(notification_type='content_report').exists())

    def test_plain_text_escaping_deleted_target_and_deleted_report(self):
        report = self.create_report()
        report.details = '<script>private()</script>'
        report.save()
        self.client.force_login(self.staff)
        response = self.client.get(self.review_url(report))
        self.assertNotContains(response, '<script>private()')
        self.assertNotContains(response, '<script>alert(1)')
        self.assertContains(response, '&lt;script&gt;private()')
        self.answer.delete()
        self.assertContains(self.client.get(self.review_url(report)), 'İçerik artık mevcut değil.')
        notice = Notification.objects.get(recipient=self.staff, related_report=report)
        url = self.review_url(report)
        report.delete()
        notice.refresh_from_db()
        self.assertEqual(notice.get_target_url(), reverse('report_inbox'))
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_filters_pagination_and_old_reports(self):
        content_type = ContentType.objects.get_for_model(self.answer)
        ContentReport.objects.bulk_create([
            ContentReport(reporter=self.reporter, content_type=content_type,
                          object_id=1000 + i, reason='spam', status='open' if i < 26 else 'reviewed')
            for i in range(27)
        ])
        self.client.force_login(self.staff)
        url = reverse('report_inbox')
        response = self.client.get(url, {'page': 2})
        self.assertEqual(len(response.context['reports']), 1)
        self.assertEqual(response.context['reports'].paginator.count, 26)
        self.assertEqual(self.client.get(url, {'status': 'all'}).context['reports'].paginator.count, 27)
        self.assertEqual(self.client.get(url, {'status': 'reviewed'}).context['reports'].paginator.count, 1)
        self.assertEqual(self.client.get(url, {'status': 'bad'}).context['current_status'], 'open')
