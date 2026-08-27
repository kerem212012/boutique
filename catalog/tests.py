from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate, override

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

    def test_product_list_filters_by_category(self):
        other_category = Category.objects.create(name='Other', slug='other')
        other_product = Product.objects.create(
            name='Other Product', slug='other-product', category=other_category, price='10.00'
        )

        response = self.client.get(reverse('catalog:product-list'), {'category': 'test-category'})

        self.assertContains(response, self.product.name)
        self.assertNotContains(response, other_product.name)

    def test_product_list_filters_new_products(self):
        self.product.is_new = True
        self.product.save(update_fields=('is_new',))
        Product.objects.create(
            name='Old Product', slug='old-product', category=self.category, price='10.00'
        )

        response = self.client.get(reverse('catalog:product-list'), {'new': '1'})

        self.assertContains(response, self.product.name)
        self.assertNotContains(response, 'Old Product')

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

    def test_new_product_shows_badge(self):
        self.product.is_new = True
        self.product.save(update_fields=('is_new',))

        with override('en'):
            response = self.client.get(reverse('catalog:product-list'))

        self.assertContains(response, 'product-badge')
        self.assertContains(response, 'New')

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

    def test_product_detail_shows_english_color_labels(self):
        self.product.colors = ['Beyaz', 'Siyah']
        self.product.colors_en = ['White', 'Black']
        self.product.save(update_fields=('colors', 'colors_en'))

        with override('en'):
            response = self.client.get(reverse('catalog:product-detail', args=[self.product.slug]))

        self.assertContains(response, 'White')
        self.assertContains(response, 'Black')
        self.assertContains(response, 'value="Beyaz"')
