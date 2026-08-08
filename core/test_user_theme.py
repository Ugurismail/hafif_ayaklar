from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

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
