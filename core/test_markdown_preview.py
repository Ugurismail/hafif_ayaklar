from django.test import SimpleTestCase

from core.answer_git import build_answer_render_preview
from core.templatetags.custom_tags import safe_markdownify, truncate_math_safe


class MarkdownPreviewTests(SimpleTestCase):
    def test_triple_emphasis_is_closed_when_preview_cuts_inside_it(self):
        raw_text = (
            '***"Diğer primatlarda da ahlaki yargının izleri görülüyor. '
            + ('Bu uzun alıntı önizleme sınırını geçiyor. ' * 40)
            + '"***'
        )

        preview = truncate_math_safe(raw_text, 1000)
        rendered = str(safe_markdownify(preview))

        self.assertTrue(preview.endswith('***'))
        self.assertNotIn('***', rendered)
        self.assertIn('<strong><em>', rendered)
        self.assertIn('</em></strong>', rendered)

    def test_preview_uses_a_nearby_word_boundary(self):
        raw_text = ('tamkelime ' * 150) + 'son'

        preview = truncate_math_safe(raw_text, 1003)

        self.assertTrue(preview.endswith('tamkelime'))
        self.assertNotIn('tamkeli***', preview)

    def test_preview_does_not_include_a_partial_markdown_link(self):
        raw_text = (
            ('Önceki metin. ' * 70)
            + '[çok uzun bağlantı başlığı '
            + ('devam ' * 50)
            + '](https://example.com/uzun-baglanti)'
        )

        preview = truncate_math_safe(raw_text, 1000)

        self.assertNotIn('[çok uzun bağlantı', preview)

    def test_preview_does_not_cut_inside_display_math(self):
        raw_text = 'Başlangıç metni $$' + ('x + y ' * 300) + '$$ son'

        preview = truncate_math_safe(raw_text, 1000)

        self.assertEqual(preview, 'Başlangıç metni')

    def test_revision_preview_uses_markup_safe_truncation(self):
        raw_text = '***' + ('biçimli uzun metin ' * 80).rstrip() + '***'

        rendered = build_answer_render_preview(raw_text, 520)

        self.assertNotIn('***', rendered)
        self.assertIn('<strong><em>', rendered)
