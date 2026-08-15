from django.urls import path

from . import views

app_name = 'panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('site-settings/', views.site_settings, name='site-settings'),

    path('products/', views.product_list, name='products'),
    path('products/add/', views.product_add, name='product-add'),
    path('products/<int:pk>/edit/', views.product_edit, name='product-edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product-delete'),
    path('products/<int:pk>/photos/', views.product_photos, name='product-photos'),
    path('products/<int:pk>/photos/<int:photo_pk>/delete/', views.photo_delete, name='photo-delete'),

    path('categories/', views.category_list, name='categories'),
    path('categories/add/', views.category_add, name='category-add'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category-edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category-delete'),
]
