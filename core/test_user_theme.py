import json

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from lxml import html

from core.font_catalog import ADDITIONAL_FONT_FAMILIES, additional_font_options
from core.templatetags.custom_filters import is_system_font, url_to_font_name


class Gpt56ThemeTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="theme-tester",
            password="test-password",
        )
        self.client.force_login(self.user)

    def test_settings_exposes_theme_and_local_font(self):
        response = self.client.get(reverse("user_settings"))

        self.assertContains(response, 'value="gpt56"')
        self.assertContains(response, "gpt5.6 (Editoryal Seladon)")
        self.assertContains(response, 'value="ITC+Galliard"')
        self.assertContains(response, '"font_family": "ITC+Galliard"')

    def test_theme_values_can_be_saved_to_profile(self):
        response = self.client.post(
            reverse("user_settings"),
            {
                "background_color": "#E8EEEA",
                "text_color": "#18231F",
                "header_background_color": "#481B2B",
                "header_text_color": "#F8F3EB",
                "link_color": "#0B6B66",
                "link_hover_color": "#084A47",
                "button_background_color": "#BC5236",
                "button_hover_background_color": "#A94931",
                "button_text_color": "#FFF8F1",
                "secondary_button_background_color": "#245A56",
                "secondary_button_hover_background_color": "#194743",
                "secondary_button_text_color": "#F8F3EB",
                "message_bubble_color": "#D8E5DF",
                "tbas_color": "#481B2B",
                "yanit_card": "#FBF8F2",
                "font_size": "18",
                "hover_background_color": "#DCE6E1",
                "icon_color": "#245A56",
                "icon_hover_color": "#BC5236",
                "answer_background_color": "#E8EEEA",
                "content_background_color": "#FFFDFC",
                "tab_background_color": "#D5E0DA",
                "tab_text_color": "#18231F",
                "tab_active_background_color": "#FBF8F2",
                "tab_active_text_color": "#481B2B",
                "dropdown_text_color": "#18231F",
                "dropdown_hover_background_color": "#D4E1DB",
                "dropdown_hover_text_color": "#084A47",
                "nav_link_hover_color": "#FFF8F1",
                "nav_link_hover_bg": "#5B2637",
                "pagination_background_color": "#FBF8F2",
                "pagination_text_color": "#481B2B",
                "font_family": "ITC+Galliard",
            },
        )

        self.assertRedirects(response, reverse("user_settings"))
        profile = self.user.userprofile
        profile.refresh_from_db()
        self.assertEqual(profile.background_color, "#E8EEEA")
        self.assertEqual(profile.header_background_color, "#481B2B")
        self.assertEqual(profile.button_background_color, "#BC5236")
        self.assertEqual(profile.font_family, "ITC+Galliard")

    def test_itc_galliard_is_treated_as_a_local_font(self):
        self.assertTrue(is_system_font("ITC+Galliard"))
        self.assertEqual(url_to_font_name("ITC+Galliard"), "ITC Galliard")


class AstraThemeTests(TestCase):
    def setUp(self):
        # Homepage's shared ID cache outlives Django's per-test database rollback.
        cache.clear()
        self.addCleanup(cache.clear)
        self.user = get_user_model().objects.create_user(username='astra-test')
        self.other = get_user_model().objects.create_user(username='other-theme')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('user_settings'))
        source = self.response.content.decode().split('"astra":', 1)[1].lstrip()
        self.theme, _ = json.JSONDecoder().raw_decode(source)

    def test_preset_is_available_with_system_font_and_existing_themes(self):
        self.assertContains(self.response, '<option value="astra">Astra</option>')
        self.assertContains(self.response, 'value="default"')
        self.assertContains(self.response, 'value="gpt56"')
        self.assertEqual(self.theme['font_family'], 'Georgia')
        self.assertTrue(is_system_font(self.theme['font_family']))

    def test_save_is_personal_persists_colors_and_preserves_quota(self):
        quota = self.user.userprofile.invitation_quota
        previous = self.other.userprofile.background_color
        response = self.client.post(reverse('user_settings'), self.theme)
        self.assertRedirects(response, reverse('user_settings'))
        profile = self.user.userprofile
        profile.refresh_from_db()
        for key, value in self.theme.items():
            if key != 'hover_text_color':  # Legacy preview-only variable, not a profile field.
                self.assertEqual(str(getattr(profile, key)), value)
        self.assertEqual(profile.invitation_quota, quota)
        self.other.userprofile.refresh_from_db()
        self.assertEqual(self.other.userprofile.background_color, previous)
        self.assertContains(self.client.get(reverse('user_homepage')), '--background-color: #F4F6F7')
        self.client.post(reverse('user_settings'), {'reset': '1'})
        profile.refresh_from_db()
        self.assertEqual(profile.background_color, '#F5F0E6')

    def test_text_and_interactive_colors_have_readable_contrast(self):
        def luminance(color):
            values = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
            linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in values]
            return sum(v * weight for v, weight in zip(linear, (.2126, .7152, .0722)))

        pairs = [('text_color', 'background_color'), ('text_color', 'content_background_color'),
                 ('header_text_color', 'header_background_color'), ('link_color', 'background_color'),
                 ('button_text_color', 'button_background_color'),
                 ('secondary_button_text_color', 'secondary_button_background_color'),
                 ('tbas_color', 'background_color'), ('tab_text_color', 'tab_background_color')]
        for foreground, background in pairs:
            light, dark = sorted([luminance(self.theme[foreground]), luminance(self.theme[background])], reverse=True)
            self.assertGreaterEqual((light + .05) / (dark + .05), 4.5, foreground)


class FontCatalogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='font-catalog-test')
        self.client.force_login(self.user)

    def test_forty_additions_are_grouped_unique_and_not_eagerly_requested(self):
        response = self.client.get(reverse('user_settings'))
        page = html.fromstring(response.content)
        values = page.xpath('//*[@id="font_family"]//option/@value')
        additions = [value for group in additional_font_options().values() for value, _ in group]
        self.assertEqual(len(additions), 40)
        self.assertEqual(len(values), len(set(values)))
        self.assertTrue(set(additions).issubset(values))
        self.assertEqual(len(ADDITIONAL_FONT_FAMILIES), 5)
        font_requests = page.xpath('//link[contains(@href, "fonts.googleapis.com")]/@href')
        self.assertFalse(any('Literata' in href or 'Manrope' in href for href in font_requests))
        self.assertEqual(page.xpath('//label[@for="font_size"]/text()'), ['Yazı Boyutu:'])

    def test_each_added_family_survives_save_and_is_selected_on_reload(self):
        from core.views.user_views import PROFILE_APPEARANCE_FIELDS
        profile = self.user.userprofile
        data = {field: str(getattr(profile, field)) for field in PROFILE_APPEARANCE_FIELDS}
        for group in additional_font_options().values():
            for value, name in group:
                with self.subTest(font=name):
                    data['font_family'] = value
                    response = self.client.post(reverse('user_settings'), data, follow=True)
                    page = html.fromstring(response.content)
                    self.assertEqual(page.xpath('//*[@id="font_family"]/optgroup/option[@selected]/@value'), [value])
                    profile.refresh_from_db()
                    self.assertEqual(profile.font_family, value)
                    self.assertEqual(profile.background_color, data['background_color'])
