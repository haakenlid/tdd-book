from django.test import TestCase
from unittest.mock import patch
from accounts.authentication import (
    PERSONA_VERIFY_URL, DOMAIN, PersonaAuthenticationBackend
)
from django.contrib.auth import get_user_model
User = get_user_model()


@patch('accounts.authentication.requests.post')
class AuthenticateTest(TestCase):

    def setUp(self):
        self.backend = PersonaAuthenticationBackend()
        user = User(email='other@user.com')
        user.username = 'otheruser'
        user.save()

    def test_sends_assertion_to_mozilla_with_domain(self, mock_post):
        self.backend.authenticate('xxx')
        mock_post.assert_called_once_with(
            PERSONA_VERIFY_URL,
            data={'assertion': 'xxx', 'audience': DOMAIN},
        )

    def test_returns_none_if_response_errors(self, mock_post):
        mock_post.return_value.ok = False
        mock_post.return_value.json.return_value = {}
        user = self.backend.authenticate('an assertion')
        self.assertIsNone(user)

    def test_returns_none_if_status_not_okay(self, mock_post):
        mock_post.return_value.json.return_value = {'status': 'not okay!'}
        user = self.backend.authenticate('an assertion')
        self.assertIsNone(user)

    def test_finds_existing_user_with_email(self, mock_post):
        email = 'a@b.com'
        mock_post.return_value.json.return_value = {'status': 'okay', 'email': email, }
        actual_user = User.objects.create(email=email)
        found_user = self.backend.authenticate('an assertion')
        self.assertEqual(found_user, actual_user)

    def test_creates_new_user_if_necessarty_for_valid_assertion(self, mock_post):
        email = 'a@b.com'
        mock_post.return_value.json.return_value = {'status': 'okay', 'email': email, }
        found_user = self.backend.authenticate('an assertion')
        new_user = User.objects.get(email=email)
        self.assertEqual(found_user, new_user)


class GetUserTest(TestCase):

    def test_gets_user_by_email(self):
        backend = PersonaAuthenticationBackend()
        other_user = User(email='other@user.com')
        other_user.username = 'otheruser'
        other_user.save()
        desired_user = User.objects.create(email='a@b.com')
        found_user = backend.get_user('a@b.com')
        self.assertEqual(found_user, desired_user)

    def test_returns_none_if_no_user_with_that_email(self):
        backend = PersonaAuthenticationBackend()
        self.assertIsNone(backend.get_user('unknown@user.com'))