from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from catalog.models import Product
from .models import Cart, CartItem
from orders.models import Order, OrderItem
from users.models import UserProfile


def get_cart(request):
    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        cart, _ = Cart.objects.get_or_create(user=profile)
    else:
        cart_id = request.session.get('cart_id')
        cart = None
        if cart_id:
            cart = Cart.objects.filter(pk=cart_id, user__isnull=True).first()
        if not cart:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.pk
    return cart


def cart_view(request):
    cart = get_cart(request)
    items = cart.items.select_related('product').all()
    total = sum(item.quantity * item.product.price for item in items)
    return render(request, 'cart/cart.html', {'cart': cart, 'items': items, 'total': total})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = get_cart(request)
    selected_size = request.POST.get('size', '').strip() if request.method == 'POST' else ''
    selected_color = request.POST.get('color', '').strip() if request.method == 'POST' else ''
    if product.sizes and selected_size not in product.sizes:
        messages.error(request, _('Please choose a valid size.'))
        return redirect('catalog:product-detail', slug=product.slug)
    if product.colors and selected_color not in product.colors:
        messages.error(request, _('Please choose a valid color.'))
        return redirect('catalog:product-detail', slug=product.slug)
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        selected_size=selected_size,
        selected_color=selected_color,
        defaults={'quantity': 1},
    )
    if not created:
        item.quantity += 1
        item.save()
    return redirect('cart:cart-view')


def remove_from_cart(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    item.delete()
    messages.success(request, _('Item removed from cart.'))
    return redirect('cart:cart-view')


def update_cart_item(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', ''))
        except (TypeError, ValueError):
            quantity = 0
        if quantity > 0:
            item.quantity = quantity
            item.save(update_fields=('quantity',))
    return redirect('cart:cart-view')


@login_required
def checkout_view(request):
    cart = get_cart(request)
    items = cart.items.select_related('product').all()
    if not items:
        return redirect('cart:cart-view')

    total = sum(item.quantity * item.product.price for item in items)
    profile = request.user.profile

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        email_error = None
        phone_error = None
        if not email:
            email_error = _('Email is required.')
        else:
            try:
                validate_email(email)
            except ValidationError:
                email_error = _('Please enter a valid email address.')
        if not phone:
            phone_error = _('Phone number is required.')

        if email_error or phone_error:
            return render(request, 'cart/checkout.html', {
                'items': items,
                'total': total,
                'address': address,
                'email': email,
                'phone': phone,
                'email_error': email_error,
                'phone_error': phone_error,
                'iban': settings.BANK_TRANSFER_IBAN,
                'recipient': settings.BANK_TRANSFER_RECIPIENT,
            })

        request.user.email = email
        request.user.save(update_fields=('email',))
        if address:
            profile.address = address
        profile.phone = phone
        profile.save()
        order = Order.objects.create(user=profile, status='new')
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                selected_size=item.selected_size,
                selected_color=item.selected_color,
            )
        order.total = total
        order.save()
        cart.items.all().delete()
        messages.success(request, _('Your order has been placed. Please complete the bank transfer.'))
        return render(request, 'cart/payment_success.html', {
            'total': total,
            'iban': settings.BANK_TRANSFER_IBAN,
            'recipient': settings.BANK_TRANSFER_RECIPIENT,
        })

    return render(request, 'cart/checkout.html', {
        'items': items,
        'total': total,
        'address': profile.address,
        'email': request.user.email,
        'phone': profile.phone,
        'iban': settings.BANK_TRANSFER_IBAN,
        'recipient': settings.BANK_TRANSFER_RECIPIENT,
    })
