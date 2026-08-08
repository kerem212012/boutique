from django.shortcuts import render

from catalog.models import Product

from .models import SiteSettings


def home(request):
    settings = SiteSettings.objects.first()
    products = Product.objects.filter(is_featured=True).order_by('-created_at')[:10]
    new_products = Product.objects.order_by('-created_at')[:10]
    context = {
        'site_settings': settings,
        'products': products,
        'new_products': new_products,
    }
    return render(request, 'core/home.html', context)
