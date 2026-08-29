from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate

from .forms import RegistrationForm, UserProfileForm
from orders.models import Order
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

    def test_profile_page_language_tr_translates_order_status(self):
        activate('tr')
        self.client.login(username='profileuser', password='pass1234')
        Order.objects.create(user=self.profile, status='paid', total='100.00')

        response = self.client.get(reverse('users:profile'))

        self.assertContains(response, 'Ödendi')

    def test_logout_ends_authenticated_session(self):
        self.client.login(username='profileuser', password='pass1234')
        response = self.client.post(reverse('users:logout'))

        self.assertRedirects(response, reverse('home'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_profile_post_updates_phone_and_address(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('users:profile'), {
            'phone': '+90 555 000 00 00', 'address': 'New address',
        })

        self.assertRedirects(response, reverse('users:profile'))
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.phone, '+90 555 000 00 00')
        self.assertEqual(self.profile.address, 'New address')

    def test_invalid_profile_post_does_not_change_profile(self):
        self.profile.phone = 'old phone'
        self.profile.save(update_fields=('phone',))
        self.client.force_login(self.user)

        response = self.client.post(reverse('users:profile'), {
            'phone': 'x' * 21, 'address': 'New address',
        })

        self.assertEqual(response.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.phone, 'old phone')


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


class UserFormTests(TestCase):
    def test_registration_form_normalizes_email_and_rejects_duplicates(self):
        form = RegistrationForm(data={
            'username': 'newuser', 'email': ' NewUser@Example.COM ',
            'password1': 'StrongPass742!', 'password2': 'StrongPass742!',
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['email'], 'newuser@example.com')

        User.objects.create_user(username='existing', email='used@example.com')
        duplicate = RegistrationForm(data={
            'username': 'another', 'email': 'USED@example.com',
            'password1': 'StrongPass742!', 'password2': 'StrongPass742!',
        })
        self.assertFalse(duplicate.is_valid())

    def test_user_profile_form_accepts_valid_profile_data(self):
        form = UserProfileForm(data={'phone': '+90 555 123 45 67', 'address': 'Antalya'})

        self.assertTrue(form.is_valid())
