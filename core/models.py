from django.db import models


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default='Kalkan Nilüfer Butik')
    tagline = models.CharField(max_length=200, default='Doğallığın ve şıklığın buluştuğu adres...')
    tagline_en = models.CharField(max_length=200, blank=True)
    email = models.EmailField(default='hello@butikmail.local')
    about_text = models.TextField(blank=True)
    about_text_en = models.TextField(blank=True)
    location = models.CharField(max_length=200, default='Kalkan, Antalya')
    hero_image = models.ImageField(upload_to='site/', blank=True, null=True)
    new_arrivals_image = models.ImageField(upload_to='site/', blank=True, null=True)
    bottom_image = models.ImageField(upload_to='site/', blank=True, null=True)

    class Meta:
        verbose_name = 'Site settings'
        verbose_name_plural = 'Site settings'

    def __str__(self):
        return self.site_name
