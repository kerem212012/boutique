from django.contrib.auth import get_user_model
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
