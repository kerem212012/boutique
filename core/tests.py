from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Product


class HomePageTests(TestCase):
    def test_featured_product_is_rendered_once(self):
        category = Category.objects.create(name='Category', slug='category')
        Product.objects.create(
            name='Unique Featured Product',
            slug='unique-featured-product',
            category=category,
            price='10.00',
            is_featured=True,
        )

        response = self.client.get(reverse('home'))

        self.assertEqual(response.content.decode().count('Unique Featured Product'), 1)
from django.urls import reverse


class HomePageTests(TestCase):
    def test_home_page_returns_200_and_hero_content(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Öne Çıkan Parçalar')
        self.assertContains(response, 'Yeni Ürünler')
