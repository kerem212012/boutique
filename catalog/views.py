from django.shortcuts import get_object_or_404, render

from .models import Product


def product_list(request):
    products = Product.objects.select_related('category').order_by('-created_at')
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if request.GET.get('new') == '1':
        products = products.filter(is_new=True)
    return render(request, 'catalog/product_list.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.prefetch_related('gallery'),
        slug=slug,
    )
    return render(request, 'catalog/product_detail.html', {'product': product})
