from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from .forms import RegistrationForm, UserProfileForm
from .models import UserProfile
from .tasks import send_email


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
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            subject = str(_('Welcome to Kalkan Nilüfer Butik'))
            message = render_to_string('users/registration_success_email.txt', {
                'user': user,
            })
            send_email.delay(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            login(request, user)
            messages.success(request, _('Registration completed successfully.'))
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'users/register.html', {'form': form})
