from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate

from catalog.models import Category, Product
from cart.models import CartItem
from orders.models import Order
from users.models import UserProfile

User = get_user_model()


class CartTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass1234')
        self.profile = UserProfile.objects.get(user=self.user)
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            category=self.category,
            price='49.99',
        )

    def test_cart_page_is_available(self):
        response = self.client.get(reverse('cart:cart-view'))
        self.assertEqual(response.status_code, 200)

    def test_adding_same_product_increases_quantity_without_duplicate_row(self):
        self.client.login(username='testuser', password='pass1234')

        self.client.get(reverse('cart:add-to-cart', args=[self.product.pk]))
        self.client.get(reverse('cart:add-to-cart', args=[self.product.pk]))

        self.assertEqual(CartItem.objects.filter(product=self.product).count(), 1)
        self.assertEqual(CartItem.objects.get(product=self.product).quantity, 2)

    def test_add_to_cart_and_checkout_as_logged_in_user(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.get(reverse('cart:add-to-cart', args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('cart:cart-view'))
        self.assertContains(response, self.product.name)
        self.assertNotContains(response, 'sepete eklendi')

        response = self.client.get(reverse('cart:checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Teslimat Adresi')

        response = self.client.post(reverse('cart:checkout'), {
            'email': 'test@example.com',
            'phone': '+90 555 123 45 67',
            'address': '123 Main St, Antalya, Türkiye',
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.profile.phone, '+90 555 123 45 67')
        self.assertContains(response, 'Banka havalesi bekleniyor')
        self.assertEqual(Order.objects.get(user=self.profile).status, 'new')

    def test_checkout_requires_email(self):
        self.client.login(username='testuser', password='pass1234')
        self.client.get(reverse('cart:add-to-cart', args=[self.product.pk]))

        response = self.client.post(reverse('cart:checkout'), {
            'address': '123 Main St, Antalya, Türkiye',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'E-posta zorunludur.')
        self.assertContains(response, 'Telefon numarası zorunludur.')

    def test_checkout_redirects_when_not_logged_in(self):
        response = self.client.get(reverse('cart:checkout'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('users:login'), response.url)

    def test_cart_page_language_tr(self):
        activate('tr')
        response = self.client.get(reverse('cart:cart-view'))
        self.assertContains(response, 'Sepetim')

    def test_cart_page_language_en(self):
        activate('en')
        response = self.client.get(reverse('cart:cart-view'))
        self.assertContains(response, 'Shopping Cart')

    def test_payment_url_is_removed(self):
        activate('en')
        self.client.login(username='testuser', password='pass1234')
        self.client.get(reverse('cart:add-to-cart', args=[self.product.pk]))

        response = self.client.get('/tr/cart/payment/')

        self.assertEqual(response.status_code, 404)
