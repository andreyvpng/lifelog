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

        # Check that the user has created our action
        self.assertTrue(object)

        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/dashboard/')

    def test_not_authorized_user(self):
        resp = self.client.post('/action-create', self.object)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/user/login?next=/action-create')


class ActionDeleteViewTest(TestCase):

    def setUp(self):
        self.user = UserFactory(username='test', password='12345')
        self.other_user = UserFactory(username='test1', password='12345')
        self.action = ActionFactory(user=self.user)
        self.url = '/action-delete/{}'.format(self.action.id)

    def test_delete_action_by_user(self):
        resp = self.client.login(username='test', password='12345')
        resp = self.client.post(self.url)
        object = Action.objects.filter(user=self.user)

        # Check that the user has deleted our action
        self.assertFalse(object)

        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/dashboard/')

    def test_delete_action_by_other_user(self):
        resp = self.client.login(username='test1', password='12345')
        resp = self.client.post(self.url)
        object = Action.objects.filter(user=self.user)

        # Check that the other user does not remove the action
        self.assertTrue(object)

        self.assertEqual(resp.status_code, 403)
