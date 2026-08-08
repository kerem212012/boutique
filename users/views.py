from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from .forms import UserProfileForm
from .models import UserProfile


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your profile has been updated.'))
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=profile)

    orders = profile.orders.prefetch_related('items__product').order_by('-created_at')
    return render(request, 'users/profile.html', {'form': form, 'orders': orders})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration completed successfully.')
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration completed successfully.')
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})
