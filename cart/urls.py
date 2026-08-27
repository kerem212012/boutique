from django.urls import path

from .views import add_to_cart, cart_view, checkout_view, remove_from_cart, update_cart_item

app_name = 'cart'

urlpatterns = [
    path('', cart_view, name='cart-view'),
    path('add/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('update/<int:item_id>/', update_cart_item, name='update-cart-item'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove-from-cart'),
    path('checkout/', checkout_view, name='checkout'),
]