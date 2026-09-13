from io import BytesIO
from zipfile import ZipFile
from xml.etree import ElementTree

from django.contrib.auth.models import User
from django.test import TestCase
from openpyxl import load_workbook

from core.models import Answer, Question, Reference


class SpreadsheetExportSecurityTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='xlsx-owner', password='pass')
        cls.other = User.objects.create_user(username='xlsx-other', password='pass')
        cls.question = Question.objects.create(user=cls.user, question_text='=1+1')
        cls.answer = Answer.objects.create(
            user=cls.user, question=cls.question, answer_text='=SUM(1,2)',
        )
        cls.other_answer = Answer.objects.create(
            user=cls.other, question=cls.question, answer_text='private-other-entry',
        )

    def setUp(self):
        self.client.force_login(self.user)

    def download(self, **options):
        response = self.client.post(
            f'/profile/{self.user.username}/download_entries_xlsx/', options,
        )
        self.assertEqual(response.status_code, 200)
        with ZipFile(BytesIO(response.content)) as archive:
            for name in archive.namelist():
                if name.startswith('xl/worksheets/') and name.endswith('.xml'):
                    root = ElementTree.fromstring(archive.read(name))
                    self.assertEqual(root.findall('.//{*}f'), [], name)
            self.assertFalse(any(name.startswith('xl/externalLinks/')
                                 for name in archive.namelist()))
        return load_workbook(BytesIO(response.content), data_only=False)

    def test_grouped_export_keeps_formula_like_text_literal(self):
        workbook = self.download()
        self.assertEqual(workbook['Entries']['A1'].value, '=1+1')
        self.assertEqual(workbook['Entries']['A1'].data_type, 's')
        self.assertEqual(workbook['Entries']['B1'].value, '=SUM(1,2)')
        self.assertEqual(workbook['Entries']['B1'].data_type, 's')

    def test_custom_order_and_owner_filter_remain_intact(self):
        second = Answer.objects.create(
            user=self.user, question=self.question, answer_text='=2+2',
        )
        workbook = self.download(order='custom', entry_ids=(
            f'{second.pk},{self.other_answer.pk},{self.answer.pk}'
        ))
        rows = list(workbook['Entries'].values)
        self.assertEqual(len(rows), 3)
        self.assertEqual([row[2] for row in rows[1:]], ['=2+2', '=SUM(1,2)'])
        self.assertEqual(rows[1][0], '=1+1')
        self.assertEqual(rows[1][1], second.created_at.strftime('%Y-%m-%d %H:%M'))

    def test_bibliography_text_is_literal_and_numeric_fields_stay_numeric(self):
        reference = Reference.objects.create(
            created_by=self.user, author_surname='=1+1', author_name='',
            year=2026, metin_ismi='=SUM(2,3)', rest='=4+4',
        )
        self.answer.answer_text = f'(k:{reference.pk}, s:=5+5)'
        self.answer.save(update_fields=['answer_text'])
        workbook = self.download()
        sheet = workbook['Kaynaklar']
        for address, value in [('B2', '=1+1'), ('D2', '=SUM(2,3)'),
                               ('E2', '=4+4'), ('F2', '=5+5')]:
            self.assertEqual(sheet[address].value, value)
            self.assertEqual(sheet[address].data_type, 's')
        self.assertEqual(sheet['A2'].value, reference.pk)
        self.assertEqual(sheet['C2'].value, 2026)
        self.assertEqual(sheet['C2'].data_type, 'n')

    def test_prefixes_errors_unicode_and_newlines_are_not_rewritten(self):
        self.question.question_text = 'Normal title'
        self.question.save(update_fields=['question_text'])
        samples = ['=1+1', '+1+1', '-1+1', '@SUM(1,2)', '#N/A',
                   '\t=1+1', '\n=1+1', 'https://example.com', 'Türkçe\nİkinci satır']
        for sample in samples:
            with self.subTest(sample=sample):
                self.answer.answer_text = sample
                self.answer.save(update_fields=['answer_text'])
                cell = self.download()['Entries']['B1']
                self.assertEqual(cell.value, sample)
                self.assertEqual(cell.data_type, 's')
                self.assertIsNone(cell.hyperlink)

    def test_other_account_export_is_forbidden(self):
        response = self.client.get(
            f'/profile/{self.other.username}/download_entries_xlsx/',
        )
        self.assertEqual(response.status_code, 403)
