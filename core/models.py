from django.db import models


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default='Kalkan Nilüfer Butik')
    tagline = models.CharField(max_length=200, default='Modern boutique experience')
    email = models.EmailField(default='hello@butikmail.local')
    about_text = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Site settings'
        verbose_name_plural = 'Site settings'

    def __str__(self):
        return self.site_name
