from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate

from catalog.models import Category, Product
from orders.models import Order, OrderItem
from users.models import UserProfile

User = get_user_model()


class OrdersTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='orderuser', password='pass1234')
        self.profile = UserProfile.objects.get(user=self.user)
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            category=self.category,
            price='49.99',
        )
        self.order = Order.objects.create(user=self.profile, total='49.99')
        OrderItem.objects.create(order=self.order, product=self.product, quantity=1, price='49.99')

    def test_orders_page_requires_login(self):
        response = self.client.get(reverse('orders:order-list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('users:login'), response.url)

    def test_orders_page_shows_orders_for_logged_in_user(self):
        self.client.login(username='orderuser', password='pass1234')
        response = self.client.get(reverse('orders:order-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(response, '49,99')

    def test_orders_page_language_tr(self):
        activate('tr')
        self.client.login(username='orderuser', password='pass1234')
        response = self.client.get(reverse('orders:order-list'))
        self.assertContains(response, 'Siparişler')
        self.assertContains(response, 'Sipariş ayrıntıları')
        self.assertContains(response, 'Ürün sayısı')
        self.assertContains(response, 'Yeni')

    def test_orders_page_language_en(self):
        activate('en')
        self.client.login(username='orderuser', password='pass1234')
        response = self.client.get(reverse('orders:order-list'))
        self.assertContains(response, 'Orders')

    def test_admin_can_change_order_status(self):
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
        )
        self.client.force_login(admin_user)
        change_url = reverse('admin:orders_order_change', args=[self.order.pk])

        response = self.client.get(change_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="status"')
        self.assertContains(response, 'value="paid"')
        self.assertContains(response, 'value="shipped"')
