from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate, override
from decimal import Decimal

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


class CatalogModelTests(TestCase):
    def test_category_and_product_fallback_to_turkish_text(self):
        category = Category.objects.create(
            name_tr='Keten', name_en='Linen', slug='keten',
            description_tr='Türkçe açıklama', description_en='',
        )
        product = Product.objects.create(
            name_tr='Gömlek', name_en='', slug='gomlek', category=category,
            description_tr='Ürün açıklaması', description_en='', price='10.00',
        )

        with override('en'):
            self.assertEqual(category.name, 'Linen')
            self.assertEqual(category.description, 'Türkçe açıklama')
            self.assertEqual(product.name, 'Gömlek')
            self.assertEqual(product.description, 'Ürün açıklaması')

    def test_color_options_keep_turkish_values_and_use_english_labels(self):
        category = Category.objects.create(name_tr='Kategori', slug='kategori')
        product = Product.objects.create(
            name_tr='Ürün', slug='urun', category=category, price='10.00',
            colors=['Beyaz', 'Siyah'], colors_en=['White'],
        )

        with override('en'):
            self.assertEqual(product.color_options, [('Beyaz', 'White'), ('Siyah', 'Siyah')])

        with override('tr'):
            self.assertEqual(product.color_options, [('Beyaz', 'Beyaz'), ('Siyah', 'Siyah')])

    def test_slug_is_generated_when_omitted(self):
        category = Category.objects.create(name_tr='Yeni Kategori', slug='')
        product = Product.objects.create(
            name_tr='Yaz Elbisesi', slug='', category=category, price='20.00',
        )

        self.assertEqual(category.slug, 'yeni-kategori')
        self.assertEqual(product.slug, 'yaz-elbisesi')


class SeedProductsCommandTests(TestCase):
    def test_seed_command_is_idempotent(self):
        from django.core.management import call_command

        call_command('seed_products')
        call_command('seed_products')

        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(Product.objects.count(), 3)
        self.assertEqual(Product.objects.get(slug='linen-summer-dress').price, Decimal('129.99'))
