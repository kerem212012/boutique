from django.shortcuts import get_object_or_404, render

from .models import Product


def product_list(request):
    products = Product.objects.select_related('category').order_by('-created_at')
    return render(request, 'catalog/product_list.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.prefetch_related('gallery'),
        slug=slug,
    )
    return render(request, 'catalog/product_detail.html', {'product': product})
