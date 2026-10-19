from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from lxml import html


class PasswordVisibilityTests(TestCase):
    def test_auth_forms_keep_password_widgets_and_load_scoped_controls(self):
        user = User.objects.create_user(username='visibility-test')
        for route, count in (('login', 1), ('signup', 1), ('password_change', 3)):
            with self.subTest(route=route):
                if route == 'password_change':
                    self.client.force_login(user)
                response = self.client.get(reverse(route))
                self.assertEqual(response.status_code, 200)
                document = html.fromstring(response.content)
                fields = document.xpath('//form[@data-password-controls]//input[@type="password"]')
                self.assertEqual(len(fields), count)
                self.assertTrue(all(field.get('id') and field.get('name') for field in fields))
                self.assertTrue(document.xpath('//form[@data-password-controls]//input[@name="csrfmiddlewaretoken"]'))
                self.assertContains(response, 'js/password_visibility.js')
                self.assertContains(response, 'css/password_visibility.css')

    def test_controls_are_not_loaded_on_other_pages(self):
        self.client.force_login(User.objects.create_user(username='visibility-reader'))
        self.assertNotContains(self.client.get(reverse('notification_list')), 'password_visibility.js')
