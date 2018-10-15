from django.test import TestCase
from utils.factory import ActionFactory, RecordFactory


class ActionTest(TestCase):

    def setUp(self):
        self.action = ActionFactory()

    def test_str(self):
        self.assertEqual(self.action.__str__(), '{} ({})'.format(
            self.action.text,
            self.action.unit
        ))


class RecordTest(TestCase):

    def setUp(self):
        self.record = RecordFactory()

    def test_str(self):
        self.assertEqual(self.record.__str__(), '{} {}'.format(
            self.record.value,
            self.record.action.unit
        ))
