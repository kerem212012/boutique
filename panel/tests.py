from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Product, ProductImage
from core.models import SiteSettings

from panel.forms import CategoryForm, ProductForm

User = get_user_model()


class PanelAccessTests(TestCase):
    urls = (
        'panel:dashboard',
        'panel:site-settings',
        'panel:products',
        'panel:product-add',
        'panel:categories',
        'panel:category-add',
    )

    def test_anonymous_users_are_redirected_from_panel(self):
        for url_name in self.urls:
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                self.assertRedirects(response, f'{reverse("admin:login")}?next={reverse(url_name)}')

    def test_non_staff_users_are_redirected_from_panel(self):
        user = User.objects.create_user(username='customer', password='pass1234')
        self.client.force_login(user)

        response = self.client.get(reverse('panel:dashboard'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('admin:login'), response.url)


class PanelCrudTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='AdminPass742!',
        )
        self.category = Category.objects.create(
            name_tr='Keten', name_en='Linen', slug='keten',
        )
        self.product = Product.objects.create(
            name_tr='Gömlek', name_en='Shirt', slug='gomlek',
            category=self.category, price='49.99',
        )
        self.client.force_login(self.admin)

    def test_dashboard_contains_counts(self):
        response = self.client.get(reverse('panel:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1')

    def test_product_list_and_edit(self):
        response = self.client.get(reverse('panel:products'))
        self.assertContains(response, self.product.name_tr)

        response = self.client.post(reverse('panel:product-edit', args=[self.product.pk]), {
            'name_tr': 'Yeni Gömlek',
            'name_en': 'New Shirt',
            'description_tr': '',
            'description_en': '',
            'category': self.category.pk,
            'price': '59.99',
            'is_featured': 'on',
            'slug': 'yeni-gomlek',
            'sizes_text': 'S, M',
            'colors_text': 'Beyaz, Siyah',
            'colors_en_text': 'White, Black',
        })

        self.assertRedirects(response, reverse('panel:products'))
        self.product.refresh_from_db()
        self.assertEqual(self.product.name_tr, 'Yeni Gömlek')
        self.assertEqual(self.product.sizes, ['S', 'M'])
        self.assertTrue(self.product.is_featured)

    def test_product_add_and_delete(self):
        response = self.client.post(reverse('panel:product-add'), {
            'name_tr': 'Elbise',
            'name_en': 'Dress',
            'description_tr': '',
            'description_en': '',
            'category': self.category.pk,
            'price': '89.90',
            'slug': 'elbise',
            'sizes_text': 'S,L',
            'colors_text': 'Kırmızı',
            'colors_en_text': 'Red',
        })
        self.assertRedirects(response, reverse('panel:products'))
        product = Product.objects.get(slug='elbise')
        self.assertEqual(product.colors_en, ['Red'])

        response = self.client.post(reverse('panel:product-delete', args=[product.pk]))
        self.assertRedirects(response, reverse('panel:products'))
        self.assertFalse(Product.objects.filter(pk=product.pk).exists())

    def test_category_crud(self):
        response = self.client.post(reverse('panel:category-add'), {
            'name_tr': 'Elbiseler', 'name_en': 'Dresses',
            'description_tr': '', 'description_en': '', 'slug': 'elbise',
        })
        self.assertRedirects(response, reverse('panel:categories'))
        category = Category.objects.get(slug='elbise')

        response = self.client.post(reverse('panel:category-edit', args=[category.pk]), {
            'name_tr': 'Yeni Elbiseler', 'name_en': 'New Dresses',
            'description_tr': '', 'description_en': '', 'slug': 'yeni-elbise',
        })
        self.assertRedirects(response, reverse('panel:categories'))
        category.refresh_from_db()
        self.assertEqual(category.name_en, 'New Dresses')

        response = self.client.post(reverse('panel:category-delete', args=[category.pk]))
        self.assertRedirects(response, reverse('panel:categories'))
        self.assertFalse(Category.objects.filter(pk=category.pk).exists())

    def test_site_settings_are_created_and_updated(self):
        response = self.client.get(reverse('panel:site-settings'))
        self.assertEqual(response.status_code, 200)
        settings = SiteSettings.objects.get()

        response = self.client.post(reverse('panel:site-settings'), {
            'site_name': 'Updated Boutique',
            'tagline': 'New tagline',
            'tagline_en': 'English tagline',
            'email': 'hello@example.com',
            'location': 'Antalya',
            'about_text': '',
            'about_text_en': '',
        })
        self.assertRedirects(response, reverse('panel:site-settings'))
        settings.refresh_from_db()
        self.assertEqual(settings.site_name, 'Updated Boutique')

    def test_product_photo_upload_and_delete(self):
        image = SimpleUploadedFile('photo.jpg', self._jpeg_bytes(), content_type='image/jpeg')
        response = self.client.post(reverse('panel:product-photos', args=[self.product.pk]), {
            'image': image, 'alt_text': 'Product photo', 'sort_order': '1',
        })
        self.assertRedirects(response, reverse('panel:product-photos', args=[self.product.pk]))
        photo = ProductImage.objects.get(product=self.product)

        response = self.client.post(reverse('panel:photo-delete', args=[self.product.pk, photo.pk]))
        self.assertRedirects(response, reverse('panel:product-photos', args=[self.product.pk]))
        self.assertFalse(ProductImage.objects.filter(pk=photo.pk).exists())

    @staticmethod
    def _jpeg_bytes():
        from PIL import Image

        image = Image.new('RGB', (2, 2), color='white')
        output = BytesIO()
        image.save(output, format='JPEG')
        return output.getvalue()


class PanelFormTests(TestCase):
    def test_product_form_serializes_variant_fields(self):
        category = Category.objects.create(name_tr='Keten', slug='keten')
        form = ProductForm(data={
            'name_tr': 'Gömlek', 'name_en': '', 'description_tr': '', 'description_en': '',
            'category': category.pk, 'price': '10.00', 'slug': 'gomlek',
            'sizes_text': ' S, M ', 'colors_text': ' Beyaz, Siyah ',
            'colors_en_text': ' White, Black ',
        })

        self.assertTrue(form.is_valid())
        product = form.save()
        self.assertEqual(product.sizes, ['S', 'M'])
        self.assertEqual(product.colors, ['Beyaz', 'Siyah'])
        self.assertEqual(product.colors_en, ['White', 'Black'])

    def test_category_form_allows_automatic_slug(self):
        form = CategoryForm(data={
            'name_tr': 'Yeni Kategori', 'name_en': '',
            'description_tr': '', 'description_en': '', 'slug': '',
        })

        self.assertTrue(form.is_valid())
        category = form.save()
        self.assertEqual(category.slug, 'yeni-kategori')