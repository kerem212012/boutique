from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Category, Product, ProductImage

from .forms import CategoryForm, ProductForm, ProductImageUploadForm


@staff_member_required
def dashboard(request):
    return render(request, 'panel/dashboard.html', {
        'product_count': Product.objects.count(),
        'category_count': Category.objects.count(),
        'featured_count': Product.objects.filter(is_featured=True).count(),
        'photo_count': ProductImage.objects.count(),
    })


# ── Products ──────────────────────────────────────────────────────────────────

@staff_member_required
def product_list(request):
    products = Product.objects.select_related('category').order_by('-created_at')
    return render(request, 'panel/products.html', {'products': products})


@staff_member_required
def product_add(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Ürün eklendi.')
        return redirect('panel:products')
    return render(request, 'panel/product_form.html', {'form': form, 'title': 'Yeni Ürün'})


@staff_member_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Ürün güncellendi.')
        return redirect('panel:products')
    return render(request, 'panel/product_form.html', {
        'form': form, 'product': product, 'title': 'Ürünü Düzenle',
    })


@staff_member_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Ürün silindi.')
        return redirect('panel:products')
    return render(request, 'panel/product_delete.html', {'product': product})


# ── Photos ────────────────────────────────────────────────────────────────────

@staff_member_required
def product_photos(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductImageUploadForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        photo = form.save(commit=False)
        photo.product = product
        photo.save()
        messages.success(request, 'Fotoğraf yüklendi.')
        return redirect('panel:product-photos', pk=pk)
    return render(request, 'panel/photos.html', {
        'product': product,
        'photos': product.gallery.all(),
        'form': form,
    })


@staff_member_required
def photo_delete(request, pk, photo_pk):
    photo = get_object_or_404(ProductImage, pk=photo_pk, product_id=pk)
    if request.method == 'POST':
        photo.image.delete(save=False)
        photo.delete()
        messages.success(request, 'Fotoğraf silindi.')
    return redirect('panel:product-photos', pk=pk)


# ── Categories ────────────────────────────────────────────────────────────────

@staff_member_required
def category_list(request):
    categories = Category.objects.order_by('name_tr')
    return render(request, 'panel/categories.html', {'categories': categories})


@staff_member_required
def category_add(request):
    form = CategoryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Kategori eklendi.')
        return redirect('panel:categories')
    return render(request, 'panel/category_form.html', {'form': form, 'title': 'Yeni Kategori'})


@staff_member_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Kategori güncellendi.')
        return redirect('panel:categories')
    return render(request, 'panel/category_form.html', {
        'form': form, 'category': category, 'title': 'Kategoriyi Düzenle',
    })


@staff_member_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Kategori silindi.')
        return redirect('panel:categories')
    return render(request, 'panel/category_delete.html', {'category': category})
