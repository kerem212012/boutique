from django.shortcuts import render

from catalog.models import Category, Product

def home(request):
    products = Product.objects.select_related('category').filter(is_featured=True).order_by('-created_at')[:10]
    new_products = Product.objects.select_related('category').filter(is_new=True).order_by('-created_at')[:10]
    categories = Category.objects.order_by('name_tr')
    context = {
        'products': products,
        'new_products': new_products,
        'categories': categories,
    }
    return render(request, 'core/home.html', context)


def legal_page(request, page):
    pages = {
        'privacy': 'core/privacy_policy.html',
        'terms': 'core/terms.html',
        'cookies': 'core/cookie_policy.html',
        'preliminary': 'core/preliminary_information.html',
        'distance-sales': 'core/distance_sales_agreement.html',
        'returns-delivery': 'core/returns_delivery.html',
    }
    return render(request, pages[page])
