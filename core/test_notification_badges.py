from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from lxml import html

from core.models import Notification


class NotificationBadgeTests(TestCase):
    def setUp(self):
        cache.clear()
        self.addCleanup(cache.clear)
        self.user = User.objects.create_user(username='badge-owner')
        self.other = User.objects.create_user(username='badge-other')
        self.client.force_login(self.user)

    def notify(self, recipient=None, **kwargs):
        return Notification.objects.create(recipient=recipient or self.user,
            notification_type='system', message='Sayaç denemesi', **kwargs)

    def test_initial_html_shows_unread_count_without_javascript(self):
        self.notify()
        self.notify()
        self.notify(is_read=True)
        self.notify(recipient=self.other)
        page = html.fromstring(self.client.get(reverse('user_homepage')).content)
        badge = page.get_element_by_id('notification-badge')
        self.assertEqual(badge.text_content().strip(), '2')
        self.assertNotIn('display: none', badge.get('style'))

    def test_empty_badge_is_hidden(self):
        page = html.fromstring(self.client.get(reverse('user_homepage')).content)
        self.assertIn('display: none', page.get_element_by_id('notification-badge').get('style'))

    def test_new_notification_overrides_cached_zero_and_response_is_not_cached(self):
        self.assertEqual(self.client.get(reverse('navbar_status')).json()['notification_count'], 0)
        self.notify()
        response = self.client.get(reverse('navbar_status'))
        self.assertEqual(response.json()['notification_count'], 1)
        self.assertIn('no-store', response['Cache-Control'])

    def test_read_actions_override_cached_positive_count(self):
        first = self.notify()
        self.notify()
        self.assertEqual(self.client.get(reverse('navbar_status')).json()['notification_count'], 2)
        self.client.post(reverse('mark_notification_read', args=[first.pk]))
        self.assertEqual(self.client.get(reverse('navbar_status')).json()['notification_count'], 1)
        self.client.post(reverse('mark_all_notifications_read'))
        self.assertEqual(self.client.get(reverse('navbar_status')).json()['notification_count'], 0)

    def test_opening_or_filtering_list_does_not_mark_notifications_read(self):
        notice = self.notify()
        for params in [{}, {'status': 'unread'}, {'type': 'entry_reference'}]:
            response = self.client.get(reverse('notification_list'), params)
            self.assertEqual(response.context['unread_count'], 1)
            notice.refresh_from_db()
            self.assertFalse(notice.is_read)
        response = self.client.get(reverse('notification_list'), {'status': 'unread'})
        self.assertContains(response, notice.message)

    def test_read_actions_are_private_and_post_only(self):
        other_notice = self.notify(recipient=self.other)
        self.assertEqual(self.client.post(reverse('mark_notification_read', args=[other_notice.pk])).status_code, 404)
        self.assertEqual(self.client.get(reverse('mark_all_notifications_read')).status_code, 405)
        self.client.post(reverse('mark_all_notifications_read'))
        other_notice.refresh_from_db()
        self.assertFalse(other_notice.is_read)

    def test_guest_does_not_receive_badges(self):
        self.notify()
        self.client.logout()
        self.assertNotContains(self.client.get(reverse('user_homepage')), 'id="notification-badge"')
