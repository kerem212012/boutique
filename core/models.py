from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default='Kalkan Nilüfer Butik', verbose_name=_('Site adı'))
    tagline = models.CharField(max_length=200, default='Doğallığın ve şıklığın buluştuğu adres...', verbose_name=_('Slogan (TR)'))
    tagline_en = models.CharField(max_length=200, blank=True, verbose_name=_('Slogan (EN)'))
    email = models.EmailField(default='hello@butikmail.local', verbose_name=_('E-posta'))
    about_text = models.TextField(blank=True, verbose_name=_('Hakkımızda (TR)'))
    about_text_en = models.TextField(blank=True, verbose_name=_('Hakkımızda (EN)'))
    location = models.CharField(max_length=200, default='Kalkan, Antalya', verbose_name=_('Konum'))
    hero_image = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name=_('Ana sayfa görseli'))
    new_arrivals_image = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name=_('Yeni gelenler görseli'))
    bottom_image = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name=_('Alt görsel'))

    class Meta:
        verbose_name = 'Site ayarları'
        verbose_name_plural = 'Site ayarları'

    def __str__(self):
        return self.site_name
