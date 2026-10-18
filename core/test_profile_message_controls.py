from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from lxml import html

from core.models import Answer, Message, Question


class ProfilePaginationSummaryTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='page-owner')
        self.viewer = User.objects.create_user(username='page-reader')
        self.question = Question.objects.create(user=self.owner, question_text='Pagination fixture')
        self.url = reverse('user_profile', args=[self.owner.username])
        self.client.force_login(self.owner)

    def add_entries(self, count):
        Answer.objects.bulk_create([
            Answer(user=self.owner, question=self.question, answer_text=f'Entry {index}')
            for index in range(count)
        ])

    def summary(self, page):
        response = self.client.get(self.url, {'tab': 'girdiler', 'answer_page': page})
        self.assertEqual(response.status_code, 200)
        return html.fromstring(response.content)

    def test_first_middle_and_last_page_show_current_and_total(self):
        self.add_entries(21)
        for page in (1, 2, 3):
            document = self.summary(page)
            self.assertEqual(document.get_element_by_id('answerPageSummary').text_content(), f'Sayfa {page} / 3')
            self.assertEqual(document.xpath('//select[@id="answerPageSelect"]/option[@selected]/@value'), [str(page)])
            self.assertEqual(len(document.xpath('//div[@id="answersList"]/div')), 1 if page == 3 else 10)
        self.assertTrue(self.summary(2).xpath('//a[@href="?answer_page=3&tab=girdiler"]'))

    def test_empty_and_single_page(self):
        self.assertFalse(self.summary(1).xpath('//*[@id="answerPageSummary"]'))
        self.add_entries(1)
        document = self.summary(1)
        self.assertEqual(document.get_element_by_id('answerPageSummary').text_content(), 'Sayfa 1 / 1')
        self.assertFalse(document.xpath('//*[@id="answerPageSelect"]'))

    def test_other_profile_invalid_page_and_other_tab(self):
        self.add_entries(11)
        self.client.force_login(self.viewer)
        for page in ('bad', 999, -1):
            self.assertEqual(self.summary(page).get_element_by_id('answerPageSummary').text_content(), 'Sayfa 1 / 2')
        response = self.client.get(self.url, {'tab': 'tanimlar'})
        self.assertNotContains(response, 'id="answerPageSummary"')


class MessageComposeControlsTests(TestCase):
    def test_scoped_script_and_multiline_post(self):
        sender = User.objects.create_user(username='compose-sender')
        recipient = User.objects.create_user(username='compose-recipient')
        self.client.force_login(sender)
        url = reverse('message_detail', args=[recipient.username])
        response = self.client.get(url)
        self.assertContains(response, 'js/message_compose.js')
        form = html.fromstring(response.content).xpath('//form[contains(@class,"message-compose")]')[0]
        self.assertTrue(form.xpath('.//input[@name="csrfmiddlewaretoken"]'))
        self.assertEqual(form.xpath('.//textarea/@maxlength'), ['5000'])
        self.assertRedirects(self.client.post(url, {'body': 'First line\nSecond line'}), url)
        self.assertEqual(Message.objects.get(sender=sender, recipient=recipient).body, 'First line\nSecond line')
        self.assertNotContains(self.client.get(reverse('message_list')), 'js/message_compose.js')
