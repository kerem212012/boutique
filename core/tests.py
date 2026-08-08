from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    def test_home_page_returns_200_and_hero_content(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Öne Çıkan Parçalar')
        self.assertContains(response, 'Yeni Ürünler')
