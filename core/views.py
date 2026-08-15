from django.shortcuts import render

from catalog.models import Category, Product

from .models import SiteSettings


def home(request):
    settings = SiteSettings.objects.first()
    products = Product.objects.select_related('category').filter(is_featured=True).order_by('-created_at')[:10]
    new_products = Product.objects.select_related('category').filter(is_new=True).order_by('-created_at')[:10]
    categories = Category.objects.order_by('name_tr')
    context = {
        'site_settings': settings,
        'products': products,
        'new_products': new_products,
        'categories': categories,
    }
    return render(request, 'core/home.html', context)
