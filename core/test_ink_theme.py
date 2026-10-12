import json

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from lxml import html

from core.templatetags.custom_filters import is_system_font


class InkThemeTests(TestCase):
    def setUp(self):
        cache.clear()
        self.addCleanup(cache.clear)
        self.user = get_user_model().objects.create_user(username='ink-reader')
        self.other = get_user_model().objects.create_user(username='ink-other')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('user_settings'))
        source = self.response.content.decode().split('"ink":', 1)[1].lstrip()
        self.theme, _ = json.JSONDecoder().raw_decode(source)

    def test_complete_neutral_preset_preserves_existing_options(self):
        for name in ['ink', 'monochrome', 'astra', 'the_philosopher', 'default']:
            self.assertContains(self.response, f'value="{name}"')
        astra, _ = json.JSONDecoder().raw_decode(
            self.response.content.decode().split('"astra":', 1)[1].lstrip())
        self.assertEqual(set(self.theme), set(astra))
        self.assertTrue(is_system_font(self.theme['font_family']))
        for value in self.theme.values():
            if value.startswith('#'):
                self.assertEqual(value[1:3], value[3:5])
                self.assertEqual(value[3:5], value[5:7])

    def test_mobile_menu_icon_uses_header_text_color(self):
        page = html.fromstring(self.response.content)
        toggle = page.xpath('//button[@aria-controls="navbarNav"]')[0]
        self.assertIn('color: var(--header-text-color)', toggle.get('style'))
        self.assertEqual(len(toggle.xpath('.//i[contains(@class, "bi-list")]')), 1)

    def test_save_persists_only_current_user_theme_and_can_be_reset(self):
        old_color = self.other.userprofile.background_color
        quota = self.user.userprofile.invitation_quota
        response = self.client.post(reverse('user_settings'), self.theme)
        self.assertRedirects(response, reverse('user_settings'))
        profile = self.user.userprofile
        profile.refresh_from_db()
        for key, value in self.theme.items():
            if key != 'hover_text_color':
                self.assertEqual(str(getattr(profile, key)), value)
        self.assertEqual(profile.invitation_quota, quota)
        self.other.userprofile.refresh_from_db()
        self.assertEqual(self.other.userprofile.background_color, old_color)
        self.assertContains(self.client.get(reverse('user_homepage')), '--background-color: #FAFAFA')
        self.client.post(reverse('user_settings'), {'reset': '1'})
        profile.refresh_from_db()
        self.assertEqual(profile.background_color, '#F5F0E6')

    def test_text_and_hover_states_have_at_least_aa_contrast(self):
        def luminance(key):
            value = int(self.theme[key][1:3], 16) / 255
            return value / 12.92 if value <= .04045 else ((value + .055) / 1.055) ** 2.4

        pairs = [
            ('text_color', background) for background in
            ['background_color', 'content_background_color', 'answer_background_color',
             'yanit_card', 'message_bubble_color']
        ] + [
            ('header_text_color', 'header_background_color'),
            ('link_color', 'background_color'), ('link_hover_color', 'background_color'),
            ('button_text_color', 'button_background_color'),
            ('button_text_color', 'button_hover_background_color'),
            ('secondary_button_text_color', 'secondary_button_background_color'),
            ('secondary_button_text_color', 'secondary_button_hover_background_color'),
            ('hover_text_color', 'hover_background_color'),
            ('tab_text_color', 'tab_background_color'),
            ('tab_active_text_color', 'tab_active_background_color'),
            ('dropdown_text_color', 'content_background_color'),
            ('dropdown_hover_text_color', 'dropdown_hover_background_color'),
            ('nav_link_hover_color', 'nav_link_hover_bg'),
            ('pagination_text_color', 'pagination_background_color'),
            ('icon_color', 'background_color'), ('tbas_color', 'background_color'),
        ]
        for foreground, background in pairs:
            light, dark = sorted([luminance(foreground), luminance(background)], reverse=True)
            self.assertGreaterEqual((light + .05) / (dark + .05), 4.5, (foreground, background))
