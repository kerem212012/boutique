from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate

from users.models import UserProfile

User = get_user_model()


class UserProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='profileuser', password='pass1234', email='user@example.com')
        self.profile = UserProfile.objects.get(user=self.user)

    def test_profile_page_requires_login(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('users:login'), response.url)

    def test_profile_page_loads_for_logged_in_user(self):
        activate('en')
        self.client.login(username='profileuser', password='pass1234')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Account Details')
        self.assertContains(response, self.user.username)

    def test_profile_page_language_tr(self):
        activate('tr')
        self.client.login(username='profileuser', password='pass1234')
        response = self.client.get(reverse('users:profile'))
        self.assertContains(response, 'Profil')
        self.assertContains(response, 'Hesap Bilgileri')
        self.assertContains(response, 'Profili Kaydet')
        self.assertContains(response, 'Telefon')
        self.assertContains(response, 'Adres')

    def test_profile_page_language_en(self):
        activate('en')
        self.client.login(username='profileuser', password='pass1234')
        response = self.client.get(reverse('users:profile'))
        self.assertContains(response, 'Profile')

    def test_logout_ends_authenticated_session(self):
        self.client.login(username='profileuser', password='pass1234')
        response = self.client.post(reverse('users:logout'))

        self.assertRedirects(response, reverse('home'))
        self.assertNotIn('_auth_user_id', self.client.session)


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    CELERY_TASK_ALWAYS_EAGER=True,
)
class RegistrationTests(TestCase):
    valid_registration = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password1': 'StrongPass742!',
        'password2': 'StrongPass742!',
    }

    def test_registration_saves_email(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'email': 'NewUser@example.com',
            'password1': 'StrongPass742!',
            'password2': 'StrongPass742!',
        })

        self.assertRedirects(response, reverse('home'))
        self.assertEqual(User.objects.get(username='newuser').email, 'newuser@example.com')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['newuser@example.com'])
        self.assertIn('newuser', mail.outbox[0].body)

    def test_registration_rejects_duplicate_email(self):
        User.objects.create_user(username='existing', email='user@example.com')
        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'email': 'USER@example.com',
            'password1': 'StrongPass742!',
            'password2': 'StrongPass742!',
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_invalid_registration_never_creates_records(self):
        User.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='StrongPass742!',
        )
        invalid_values = (
            {'username': ''},
            {'username': 'existing'},
            {'email': ''},
            {'email': 'not-an-email'},
            {'email': 'EXISTING@example.com'},
            {'password1': '', 'password2': ''},
            {'password1': 'short', 'password2': 'short'},
            {'password1': 'password', 'password2': 'password'},
            {'password1': '123456789', 'password2': '123456789'},
            {'password1': 'newuser2026!', 'password2': 'newuser2026!'},
            {'password2': 'DifferentPass742!'},
        )

        for overrides in invalid_values:
            with self.subTest(overrides=overrides):
                payload = self.valid_registration | overrides
                users_before = User.objects.count()
                profiles_before = UserProfile.objects.count()

                response = self.client.post(reverse('users:register'), payload)

                self.assertEqual(response.status_code, 200)
                self.assertEqual(User.objects.count(), users_before)
                self.assertEqual(UserProfile.objects.count(), profiles_before)
                self.assertNotIn('_auth_user_id', self.client.session)
                self.assertEqual(mail.outbox, [])

    def test_profile_creation_failure_rolls_back_user(self):
        with patch('users.models.UserProfile.objects.create', side_effect=RuntimeError('profile failure')):
            with self.assertRaises(RuntimeError):
                self.client.post(reverse('users:register'), self.valid_registration)

        self.assertFalse(User.objects.filter(username='newuser').exists())
        self.assertFalse(UserProfile.objects.exists())
        self.assertEqual(mail.outbox, [])


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    CELERY_TASK_ALWAYS_EAGER=True,
)
class PasswordResetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='resetuser',
            email='reset@example.com',
            password='OldPass742!',
        )

    def test_reset_page_is_linked_from_login(self):
        response = self.client.get(reverse('users:login'))
        self.assertContains(response, reverse('users:password_reset'))

    def test_reset_request_sends_email_with_valid_link(self):
        response = self.client.post(
            reverse('users:password_reset'),
            {'email': self.user.email},
        )

        self.assertRedirects(response, reverse('users:password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('/password-reset/', mail.outbox[0].body)
        self.assertIn('reset@example.com', mail.outbox[0].to)

    def test_unknown_email_does_not_send_email(self):
        response = self.client.post(
            reverse('users:password_reset'),
            {'email': 'unknown@example.com'},
        )

        self.assertRedirects(response, reverse('users:password_reset_done'))
        self.assertEqual(mail.outbox, [])
