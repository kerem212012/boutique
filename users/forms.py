from django import forms
from django.utils.translation import gettext_lazy as _

from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address']
        labels = {
            'phone': _('Phone'),
            'address': _('Address'),
        }
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': _('Phone')}),
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': _('Address')}),
        }
