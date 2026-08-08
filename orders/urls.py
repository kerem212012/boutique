from django.urls import path

from .views import order_list

app_name = 'orders'

urlpatterns = [
    path('', order_list, name='order-list'),
]
