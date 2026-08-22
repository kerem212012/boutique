from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.template import loader
from django.utils.translation import gettext_lazy as _

from .models import UserProfile
from .tasks import send_email

User = get_user_model()


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label=_('Email'), required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_('An account with this email already exists.'))
        return email


class QueuedPasswordResetForm(PasswordResetForm):
    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        subject = ''.join(loader.render_to_string(subject_template_name, context).splitlines())
        body = loader.render_to_string(email_template_name, context)
        html_message = None
        if html_email_template_name is not None:
            html_message = loader.render_to_string(html_email_template_name, context)

        send_email.delay(subject, body, from_email, [to_email], html_message)


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
