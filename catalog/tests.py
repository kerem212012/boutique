from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate

from cart.models import CartItem

from .models import Category, Product


class CatalogPageTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            category=self.category,
            price='49.99',
        )

    def test_product_list_page_is_available(self):
        response = self.client.get(reverse('catalog:product-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_list_page_in_english(self):
        activate('en')
        response = self.client.get(reverse('catalog:product-list'))
        self.assertContains(response, 'Catalog')
        self.assertContains(response, self.product.name)

    def test_product_list_page_in_turkish(self):
        activate('tr')
        response = self.client.get(reverse('catalog:product-list'))
        self.assertContains(response, 'Katalog')
        self.assertContains(response, 'Detayları Gör')
        self.assertContains(response, self.product.name)

    def test_product_detail_shows_options_and_adds_selected_variant(self):
        self.product.sizes = ['S', 'M']
        self.product.colors = ['Black', 'White']
        self.product.save(update_fields=('sizes', 'colors'))

        response = self.client.get(reverse('catalog:product-detail', args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Black')
        self.assertContains(response, 'M')

        self.client.post(reverse('cart:add-to-cart', args=[self.product.pk]), {
            'size': 'M',
            'color': 'Black',
        })

        item = CartItem.objects.get(product=self.product)
        self.assertEqual(item.selected_size, 'M')
        self.assertEqual(item.selected_color, 'Black')
