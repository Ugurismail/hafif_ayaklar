from django.contrib.auth.models import User
from django.test import TestCase
from lxml import html

from core.models import Reference
from core.templatetags.custom_tags import (
    extract_bibliography,
    reference_link,
    safe_markdownify,
    spoiler_link,
)


class ReferenceNumberingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="reference-numbering-user",
            password="pass",
        )
        self.first = self.create_reference("Birinci")
        self.footnote = self.create_reference("Dipnot")
        self.last = self.create_reference("Sonuncu")

    def create_reference(self, surname):
        return Reference.objects.create(
            author_surname=surname,
            author_name="Yazar",
            year=2026,
            metin_ismi=f"{surname} kaynak",
            rest="Test yayını.",
            created_by=self.user,
        )

    def render_answer(self, text):
        markdown = safe_markdownify(text)
        return str(reference_link(spoiler_link(markdown)))

    def test_footnote_references_keep_inline_and_bibliography_numbers_aligned(self):
        text = (
            f"İlk kaynak (kaynak:{self.first.id}). "
            f"-g- Dipnot kaynağı (kaynak:{self.footnote.id}) -g- "
            f"Son kaynak (kaynak:{self.last.id})."
        )

        rendered = html.fragment_fromstring(
            self.render_answer(text),
            create_parent=True,
        )
        visible_numbers = rendered.xpath(
            './/sup[contains(@class, "reference-tooltip") '
            'and not(ancestor::*[@hidden])]/text()'
        )
        hidden_numbers = rendered.xpath(
            './/*[@hidden]//sup[contains(@class, "reference-tooltip")]/text()'
        )
        bibliography = extract_bibliography(text)

        self.assertEqual(visible_numbers, ["[1]", "[3]"])
        self.assertEqual(hidden_numbers, ["[2]"])
        self.assertEqual(
            [item["number"] for item in bibliography],
            [1, 2, 3],
        )
        self.assertEqual(
            [item["reference"].id for item in bibliography],
            [self.first.id, self.footnote.id, self.last.id],
        )

    def test_repeated_footnote_reference_reuses_its_original_number(self):
        text = (
            f"-g- Dipnot kaynağı (k:{self.footnote.id} s:12) -g- "
            f"Metindeki aynı kaynak (kaynak:{self.footnote.id}, sayfa:15)."
        )

        rendered = html.fragment_fromstring(
            self.render_answer(text),
            create_parent=True,
        )
        all_numbers = rendered.xpath(
            './/sup[contains(@class, "reference-tooltip")]/text()'
        )
        bibliography = extract_bibliography(text)

        self.assertEqual(all_numbers, ["[1]", "[1]"])
        self.assertEqual(len(bibliography), 1)
        self.assertEqual(bibliography[0]["number"], 1)
        self.assertEqual(bibliography[0]["reference"].id, self.footnote.id)
        self.assertEqual(bibliography[0]["pages"], ["12", "15"])
