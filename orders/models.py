from django.db import models
from django.utils.translation import gettext_lazy as _

from catalog.models import Product
from users.models import UserProfile


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', _('New')),
        ('paid', _('Paid')),
        ('shipped', _('Shipped')),
    ]
    user = models.ForeignKey(UserProfile, related_name='orders', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_address = models.TextField(blank=True)

    @property
    def shipping_address(self):
        return self.delivery_address or (self.user.address if self.user else '')

    def __str__(self):
        return f'Order #{self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selected_size = models.CharField(max_length=50, blank=True)
    selected_color = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
