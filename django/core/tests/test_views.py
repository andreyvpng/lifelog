from django.test import TestCase, RequestFactory
from utils.factory import UserFactory


class WelcomeViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory(username='test', password='12345')

    def test_not_authorized_user(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'core/welcome.html')

    def test_authorized_user(self):
        resp = self.client.login(username='test', password='12345')

        # Check our user is logged in
        self.assertTrue(resp)

        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/dashboard/')
