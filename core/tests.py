from django.test import TestCase
from django.urls import reverse
from django.utils.translation import override

from catalog.models import Category, Product
from catalog.context_processors import nav_categories
from core.context_processors import site_settings
from core.models import SiteSettings


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

    def test_legal_pages_are_public(self):
        for page_name in (
            'privacy-policy',
            'terms',
            'cookie-policy',
            'preliminary-information',
            'distance-sales-agreement',
            'returns-and-delivery',
        ):
            with self.subTest(page_name=page_name):
                response = self.client.get(reverse(page_name))
                self.assertEqual(response.status_code, 200)


class ContextProcessorTests(TestCase):
    def test_site_settings_processor_returns_first_settings(self):
        first = SiteSettings.objects.create(site_name='First')
        SiteSettings.objects.create(site_name='Second')

        self.assertEqual(site_settings(None)['site_settings'], first)

    def test_navigation_categories_are_ordered_by_active_language(self):
        Category.objects.create(name_tr='Zeta', name_en='Alpha', slug='zeta')
        Category.objects.create(name_tr='Alpha', name_en='Zeta', slug='alpha')

        with override('tr'):
            self.assertEqual(
                list(nav_categories(None)['nav_categories'].values_list('name_tr', flat=True)),
                ['Alpha', 'Zeta'],
            )
        with override('en'):
            self.assertEqual(
                list(nav_categories(None)['nav_categories'].values_list('name_en', flat=True)),
                ['Alpha', 'Zeta'],
            )
