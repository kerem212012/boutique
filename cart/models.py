from django.db import models

from catalog.models import Product
from users.models import UserProfile


class Cart(models.Model):
    user = models.ForeignKey(UserProfile, related_name='carts', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart #{self.pk}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    selected_size = models.CharField(max_length=50, blank=True)
    selected_color = models.CharField(max_length=100, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('cart', 'product', 'selected_size', 'selected_color'),
                name='unique_variant_per_cart',
            ),
        ]

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
