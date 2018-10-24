from django.test import TestCase
from django.utils import timezone

from utils.factory import ActionFactory, UserFactory


class ActionCurrentMonthViewTest(TestCase):

    def setUp(self):
        self.user = UserFactory(username='test', password='12345')
        self.action = ActionFactory(user=self.user)

    def test_redirect_url(self):
        resp = self.client.login(username='test', password='12345')

        # Check our user is logged in
        self.assertTrue(resp)

        resp = self.client.get('/statistic/{}'.format(self.action.id))
        date = timezone.now().strftime('%Y-%m')

        self.assertRedirects(resp, '/statistic/{}/{}'.format(self.action.id, date))
