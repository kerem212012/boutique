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
        self.order = Order.objects.create(
            user=self.profile,
            total='49.99',
            delivery_address='123 Main St, Antalya, Türkiye',
        )
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
        self.assertContains(response, '123 Main St, Antalya, Türkiye')

    def test_orders_page_hides_other_users_orders(self):
        other_user = User.objects.create_user(username='other-order-user', password='pass1234')
        other_profile = UserProfile.objects.get(user=other_user)
        other_order = Order.objects.create(user=other_profile, total='25.00')
        OrderItem.objects.create(order=other_order, product=self.product, quantity=1, price='25.00')
        self.client.login(username='orderuser', password='pass1234')

        response = self.client.get(reverse('orders:order-list'))

        self.assertContains(response, '49,99')
        self.assertNotContains(response, '25,00')

    def test_shipping_address_uses_empty_value_without_profile(self):
        order = Order.objects.create(user=None, total='1.00')

        self.assertEqual(order.shipping_address, '')

    def test_orders_page_falls_back_to_profile_address_for_old_orders(self):
        self.order.delivery_address = ''
        self.order.save(update_fields=('delivery_address',))
        self.profile.address = 'Old profile address, Antalya'
        self.profile.save(update_fields=('address',))
        self.client.login(username='orderuser', password='pass1234')

        response = self.client.get(reverse('orders:order-list'))

        self.assertContains(response, 'Old profile address, Antalya')

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
