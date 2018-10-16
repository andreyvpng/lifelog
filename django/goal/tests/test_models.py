from django.test import TestCase
from utils.factory import GoalFactory


class GoalTest(TestCase):

    def setUp(self):
        self.goal = GoalFactory()

    def test_str(self):
        self.assertEqual(self.goal.__str__(),
                         'Goal: {} {} {}'.format(
            self.goal.action.text,
            self.goal.daily_value,
            self.goal.action.unit
        ))
