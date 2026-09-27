from io import BytesIO
import json

from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import reverse
from docx import Document
from pypdf import PdfReader

from core.answer_git import render_answer_content_html
from core.content_link_preload import preload_content_links
from core.entry_references import (
    available_entry_ids, entry_references_for_export, link_entry_references,
    referenced_entry_ids,
)
from core.models import Answer, Question
from core.paper_export import PaperTextRenderer, build_paper_docx
from core.paper_pdf import paper_docx_to_pdf
from core.templatetags.custom_tags import safe_markdownify
from core.utils import extract_hashtags


class EntryReferenceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='entry-reference-author')
        cls.question = Question.objects.create(user=cls.user, question_text='Referans hedefi')
        cls.answer = Answer.objects.create(user=cls.user, question=cls.question, answer_text='Hedef entry')
        cls.ref = f'#{cls.answer.id}'
        cls.path = reverse('entry_permalink', args=[cls.answer.id])
        cls.url = 'https://hafifayaklar.com' + cls.path

    def test_plain_and_formatted_references(self):
        for source in [self.ref, f'Bakınız ({self.ref}).', f'**{self.ref}**',
                       f'== {self.ref}', f'1.1. {self.ref}']:
            with self.subTest(source=source):
                html = safe_markdownify(source)
                self.assertIn(f'href="{self.path}"', html)
                self.assertIn(f'>{self.ref}</a>', html)
                self.assertNotIn('/hashtag/', html)

    def test_unknown_deleted_and_inactive_entries_are_plain_text(self):
        for action in ['missing', 'inactive', 'deleted']:
            with self.subTest(action=action):
                if action == 'missing':
                    text = '#2147483647'
                else:
                    text = self.ref
                    if action == 'inactive':
                        User.objects.filter(pk=self.user.pk).update(is_active=False)
                    else:
                        self.answer.delete()
                html = safe_markdownify(text)
                self.assertIn(text, html)
                self.assertNotIn('<a ', html)

    def test_literals_and_existing_links_are_not_rewritten(self):
        for source in [f'`{self.ref}`', f'```\n{self.ref}\n```',
                       f'    {self.ref}', f'${self.ref}$', f'$${self.ref}$$',
                       f'[{self.ref}](https://example.com)', f'\\{self.ref}',
                       f'https://example.com/path{self.ref}', f'word{self.ref}']:
            with self.subTest(source=source):
                html = safe_markdownify(source)
                self.assertNotIn('class="entry-reference"', html)

    def test_hashtags_keep_their_existing_meaning(self):
        html = safe_markdownify(f'{self.ref} #felsefe #2026yılı')
        self.assertIn('class="entry-reference"', html)
        self.assertEqual(html.count('class="hashtag-link"'), 2)
        self.assertEqual(set(extract_hashtags(f'{self.ref} #felsefe #2026yılı')), {'felsefe', '2026yılı'})

    def test_backslashes_in_code_and_math_are_preserved(self):
        for source in [f'`\\{self.ref}`', f'$\\{self.ref}$']:
            with self.subTest(source=source):
                self.assertIn(f'\\{self.ref}', safe_markdownify(source))

    def test_saved_reference_does_not_create_numeric_hashtag(self):
        from core.models import Hashtag

        self.answer.answer_text = f'{self.ref} #felsefe'
        self.answer.save()
        self.assertFalse(Hashtag.objects.filter(name=str(self.answer.id)).exists())
        self.assertTrue(Hashtag.objects.filter(name='felsefe').exists())

    def test_live_preview_endpoint(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('answer_live_preview'),
                                    json.dumps({'content': self.ref}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(f'href="{self.path}"', response.json()['html'])

    def test_ids_are_bounded_and_do_not_partially_match(self):
        text = '#0 #01 #2147483648 #' + '9' * 5000
        self.assertEqual(referenced_entry_ids(text), set())
        with self.assertNumQueries(0):
            self.assertNotIn('class="entry-reference"', safe_markdownify(text))

    def test_html_attributes_and_svg_are_unchanged(self):
        source = (f'<svg viewBox="0 0 10 10"><text>{self.ref}</text></svg>'
                  f'<img alt="{self.ref}" src="/x.svg"/>'
                  f'<a href="{self.path}">{self.ref}</a>')
        with self.assertNumQueries(0):
            self.assertEqual(link_entry_references(source), source)

    def test_safe_html_remains_safe(self):
        html = safe_markdownify(f'{self.ref} <script>alert(1)</script><img src=x onerror="alert(2)">')
        self.assertNotIn('<script', html)
        self.assertNotIn('onerror=', html)
        self.assertIn(f'href="{self.path}"', html)

    def test_repeated_references_use_one_query(self):
        with self.assertNumQueries(1):
            html = safe_markdownify(' '.join([self.ref] * 100))
        self.assertEqual(html.count('class="entry-reference"'), 100)

    def test_preload_avoids_queries_per_entry_and_resets(self):
        with self.assertNumQueries(1):
            with preload_content_links([self.ref] * 10):
                for _ in range(10):
                    self.assertIn('class="entry-reference"', safe_markdownify(self.ref))
        with self.assertNumQueries(1):
            self.assertIn('class="entry-reference"', safe_markdownify(self.ref))

    def test_empty_bulk_lookup_makes_no_query(self):
        with self.assertNumQueries(0):
            self.assertEqual(available_entry_ids(set()), set())

    def test_permalink_get_and_head_redirect_to_current_entry(self):
        expected = reverse('single_answer', args=[self.question.slug, self.answer.id])
        for method in [self.client.get, self.client.head]:
            response = method(self.path)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response['Location'], expected)

    def test_permalink_follows_a_changed_slug(self):
        Question.objects.filter(pk=self.question.pk).update(slug='yeni-baslik')
        response = self.client.get(self.path)
        self.assertEqual(response['Location'], reverse('single_answer', args=['yeni-baslik', self.answer.id]))

    def test_permalink_rejects_missing_inactive_and_unsafe_methods(self):
        self.assertEqual(self.client.get('/entry/2147483648/').status_code, 404)
        self.assertEqual(self.client.get('/entry/0/').status_code, 404)
        self.assertEqual(self.client.get('/entry/2147483647/').status_code, 404)
        self.assertEqual(self.client.post(self.path).status_code, 405)
        User.objects.filter(pk=self.user.pk).update(is_active=False)
        self.assertEqual(self.client.get(self.path).status_code, 404)

    def test_shared_preview_renderer_and_copy_action(self):
        self.assertIn(f'href="{self.path}"', render_answer_content_html(self.ref))
        html = render_to_string('core/_entry_reference_action.html', {'entry_id': self.answer.id})
        self.assertIn(f'data-copy-entry-reference="{self.ref}"', html)

    def test_export_skips_literals_links_formulas_and_url_fragments(self):
        for source in [f'`{self.ref}`', f'```\n{self.ref}\n```', f'    {self.ref}',
                       f'[{self.ref}](https://example.com)', f'${self.ref}$',
                       f'https://example.com/path{self.ref}', f'\\{self.ref}']:
            with self.subTest(source=source):
                self.assertEqual(entry_references_for_export(source, {self.answer.id}), source)

    def test_word_and_pdf_contain_clickable_entry_reference(self):
        self.answer.answer_text = f'Normal {self.ref}. **Kalın {self.ref}** ve *{self.ref}*.'
        docx = build_paper_docx([self.answer], self.user)
        document = Document(BytesIO(docx))
        self.assertIn(self.url, [rel.target_ref for rel in document.part.rels.values() if rel.is_external])
        self.assertNotIn(f']({self.url})', document.element.xml)
        pdf = PdfReader(BytesIO(paper_docx_to_pdf(docx)))
        uris = []
        for page in pdf.pages:
            for annotation in page.get('/Annots', []):
                action = annotation.get_object().get('/A', {})
                if '/URI' in action:
                    uris.append(action['/URI'])
        self.assertIn(self.url, uris)

    def test_footnote_entry_reference_includes_its_destination(self):
        self.answer.answer_text = f'-g- Bkz. {self.ref} -g-'
        renderer = PaperTextRenderer([self.answer])
        renderer.prepare_text(self.answer.answer_text)
        self.assertIn(self.url, renderer.notes[0]['text'])
