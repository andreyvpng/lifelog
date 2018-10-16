from core.models import Action, Record
from goal.models import Goal
from django.test import TestCase
from utils.factory import ActionFactory, RecordFactory, UserFactory, GoalFactory


class GoalCreateViewTest(TestCase):

    def setUp(self):
        self.user = UserFactory(username='test', password='12345')
        self.other_user = UserFactory(username='test1', password='12345')
        self.action = ActionFactory(user=self.user)
        self.url = '/goal/create/action/{}'.format(
            self.action.id)
        self.url_update = '/goal/update/action/{}'.format(
            self.action.id)

        self.object = {'action': self.action,
                       'daily_value': 100}

    def test_create_goal_by_user(self):
        resp = self.client.login(username='test', password='12345')
        resp = self.client.post(self.url, self.object)
        object = Goal.objects.filter(action__user=self.user)

        # Check that the user has created our goal
        self.assertTrue(object)

        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/dashboard/')

    def test_create_goal_by_other_user(self):
        resp = self.client.login(username='test1', password='12345')
        resp = self.client.post(self.url, self.object)
        object = Goal.objects.filter(action__user=self.user)

        # Check that the user does not have updated our goal
        self.assertFalse(object)

        self.assertEqual(resp.status_code, 400)

    def test_create_goal_if_goal_exists(self):
        GoalFactory(action=self.action)

        resp = self.client.login(username='test', password='12345')
        resp = self.client.post(self.url, self.object)

        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.url_update)


class GoalUpdateViewTest(TestCase):

    def setUp(self):
        self.user = UserFactory(username='test', password='12345')
        self.other = UserFactory(username='test1', password='12345')
        self.action = ActionFactory(user=self.user)
        self.goal = GoalFactory(action=self.action)
        self.url = '/goal/update/action/{}'.format(
            self.action.id)
        self.object = {'action': self.action,
                       'daily_value': 100}

    def test_update_goal_by_user(self):
        resp = self.client.login(username='test', password='12345')
        resp = self.client.post(self.url, self.object)

        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/dashboard/')

    def test_update_goal_by_other_user(self):
        resp = self.client.login(username='test1', password='12345')
        resp = self.client.post(self.url, self.object)

        self.assertEqual(resp.status_code, 403)
