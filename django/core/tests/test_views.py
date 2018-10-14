from core.models import Action
from django.test import TestCase
from utils.factory import UserFactory, ActionFactory


class WelcomeViewTest(TestCase):

    def setUp(self):
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


class ActionCreateViewTest(TestCase):

    def setUp(self):
        self.user = UserFactory(username='test', password='12345')
        self.object = {'text': 'Book Reading',
                       'color': '1',
                       'unit': 'pages'}

    def test_authorized_user(self):
        resp = self.client.login(username='test', password='12345')
        resp = self.client.post('/action-create', self.object)
        object = Action.objects.filter(user=self.user)

        # Check our user is create action
        self.assertTrue(object)

        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/dashboard/')

    def test_not_authorized_user(self):
        resp = self.client.post('/action-create', self.object)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/user/login?next=/action-create')
