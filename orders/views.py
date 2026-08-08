from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def order_list(request):
    orders = request.user.profile.orders.prefetch_related('items__product').order_by('-created_at')
    return render(request, 'orders/orders.html', {'orders': orders})
