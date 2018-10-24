from user.models import User

from django.test import TestCase


class RegisterView(TestCase):

    def test_success_url(self):
        resp = self.client.post(
            '/user/register',
            {
                'username': 'andrey',
                'password1': 'GwuYLr9z',
                'password2': 'GwuYLr9z'
            }
        )
        user = User.objects.filter(username='andrey')

        self.assertTrue(user)
        self.assertEqual(resp.status_code, 302)
