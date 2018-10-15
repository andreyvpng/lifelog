from core.models import Action, Record
from django.db.models import Sum
from django.test import TestCase
from utils.factory import ActionFactory, RecordFactory, UserFactory


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


class ActionListViewTest(TestCase):
    ACTION_LIST_HTML = """
        <tr>
          <th scope="row">{text}</th>
          <td>{unit}</td>
        </tr>
    """

    def setUp(self):
        self.user = UserFactory(username='test', password='12345')
        self.other_user = UserFactory(username='test1', password='12345')
        users = [self.user, self.other_user]

        for user in users:
            for _ in range(1, 10):
                ActionFactory(user=user)

        self.url = '/actions'

    def test_list_of_actions_for_user(self):
        resp = self.client.login(username='test', password='12345')
        resp = self.client.get(self.url)
        actions_in_template = list(resp.context_data['object_list'])
        actions_of_user = list(Action.objects.filter(user=self.user))
        self.assertEqual(actions_in_template, actions_of_user)

    def test_list_of_actions_for_other_user(self):
        resp = self.client.login(username='test1', password='12345')
        resp = self.client.get(self.url)
        actions_in_template = list(resp.context_data['object_list'])
        actions_of_other_user = list(Action.objects.filter(user=self.other_user))
        self.assertEqual(actions_in_template, actions_of_other_user)

    def test_list_of_actions_template(self):
        resp = self.client.login(username='test', password='12345')
        resp = self.client.get(self.url)
        rendered_content = resp.rendered_content

        full_list_of_actions = ''
        actions = resp.context_data['object_list']

        for action in actions:
            full_list_of_actions += self.ACTION_LIST_HTML.format(
                text=action.text,
                unit=action.unit
            )

        self.assertInHTML(full_list_of_actions, rendered_content)
        self.assertTemplateUsed(resp, 'core/action_list.html')


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


class ActionUpdateViewTest(TestCase):

    def setUp(self):
        self.user = UserFactory(username='test', password='12345')
        self.other_user = UserFactory(username='test1', password='12345')

        self.object = {'text': 'Action',
                       'color': 2,
                       'unit': 'unit'}

        self.action = ActionFactory(user=self.user, **self.object)

        self.update_object = {'text': 'Book Reading',
                              'color': 1,
                              'unit': 'pages'}

        self.url = '/action-update/{}'.format(self.action.id)

    def test_update_action_by_user(self):
        resp = self.client.login(username='test', password='12345')
        resp = self.client.post(self.url, self.update_object)
        object = Action.objects.filter(user=self.user)[0]

        # Check that the user has update our action
        self.assertEqual(object.text, self.update_object['text'])
        self.assertEqual(object.color, self.update_object['color'])
        self.assertEqual(object.unit, self.update_object['unit'])

        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/dashboard/')

    def test_update_action_by_other_user(self):
        resp = self.client.login(username='test1', password='12345')
        resp = self.client.post(self.url, self.update_object)
        object = Action.objects.filter(user=self.user)[0]

        # Check that the user does not have updated our action
        self.assertEqual(object.text, self.object['text'])
        self.assertEqual(object.color, self.object['color'])
        self.assertEqual(object.unit, self.object['unit'])

        self.assertEqual(resp.status_code, 403)


class RecordCreateViewTest(TestCase):

    def setUp(self):
        self.user = UserFactory(username='test', password='12345')
        self.other_user = UserFactory(username='test1', password='12345')

        self.object = {'text': 'Book Reading',
                       'color': 1,
                       'unit': 'pages',
                       'user': self.user}

        self.action = ActionFactory(**self.object)
        self.url = '/record-create'

        self.new_record = {'action': self.action.id,
                           'value': 100}

    def get_value_sum_of_action(self):
        sum = Record.objects.filter(action=self.action).aggregate(Sum('value'))
        return sum['value__sum']

    def test_create_record_by_user(self):
        resp = self.client.login(username='test', password='12345')
        resp = self.client.post(self.url, self.new_record)

        self.assertEqual(self.get_value_sum_of_action(), 100)
        self.assertEqual(resp.status_code, 302)

    def test_create_record_by_other_user(self):
        resp = self.client.login(username='test1', password='12345')
        resp = self.client.post(self.url, self.new_record)

        self.assertEqual(self.get_value_sum_of_action(), None)
        self.assertEqual(resp.status_code, 200)


class RecordListViewTest(TestCase):
    RECORD_LIST_HTML = """
        <tr>
          <th scope="row">{text}</th>
          <td>{value} {unit}</td>
        </tr>
    """

    def setUp(self):
        self.user = UserFactory(username='test', password='12345')
        self.other_user = UserFactory(username='test1', password='12345')

        self.action = ActionFactory(user=self.user)
        self.action1 = ActionFactory(user=self.other_user)
        actions = [self.action, self.action1]

        for action in actions:
            for _ in range(1, 10):
                RecordFactory(action=action)

        self.url = '/records'

    def test_list_of_actions_for_user(self):
        resp = self.client.login(username='test', password='12345')
        resp = self.client.get(self.url)
        records_in_template = list(resp.context_data['object_list'])
        records_of_user = list(Record.objects.filter(action__user=self.user))
        self.assertEqual(records_in_template, records_of_user)

    def test_list_of_actions_for_other_user(self):
        resp = self.client.login(username='test1', password='12345')
        resp = self.client.get(self.url)
        records_in_template = list(resp.context_data['object_list'])
        records_of_user = list(Record.objects.filter(action__user=self.other_user))
        self.assertEqual(records_in_template, records_of_user)

    def test_list_of_actions_template(self):
        resp = self.client.login(username='test', password='12345')
        resp = self.client.get(self.url)
        rendered_content = resp.rendered_content

        full_list_of_records = ''
        records = resp.context_data['object_list']

        for record in records:
            full_list_of_records += self.RECORD_LIST_HTML.format(
                text=record.action.text,
                unit=record.action.unit,
                value=record.value
            )

        self.assertInHTML(full_list_of_records, rendered_content)
        self.assertTemplateUsed(resp, 'core/record_list.html')
