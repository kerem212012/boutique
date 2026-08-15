from django.db import models
from django.utils.text import slugify
from django.utils.translation import get_language


class Category(models.Model):
    name_tr = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    description_tr = models.TextField(blank=True)
    description_en = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    @property
    def name(self):
        lang = get_language()
        if lang and lang.startswith('en') and self.name_en:
            return self.name_en
        return self.name_tr

    @name.setter
    def name(self, value):
        self.name_tr = value

    @property
    def description(self):
        lang = get_language()
        if lang and lang.startswith('en') and self.description_en:
            return self.description_en
        return self.description_tr

    @description.setter
    def description(self, value):
        self.description_tr = value

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_tr)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_tr


class Product(models.Model):
    name_tr = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    description_tr = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    sizes = models.JSONField(default=list, blank=True)
    colors = models.JSONField(default=list, blank=True)
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def name(self):
        lang = get_language()
        if lang and lang.startswith('en') and self.name_en:
            return self.name_en
        return self.name_tr

    @name.setter
    def name(self, value):
        self.name_tr = value

    @property
    def description(self):
        lang = get_language()
        if lang and lang.startswith('en') and self.description_en:
            return self.description_en
        return self.description_tr

    @description.setter
    def description(self, value):
        self.description_tr = value

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_tr)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_tr


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('sort_order', 'id')

    def __str__(self):
        return f'{self.product.name_tr} image #{self.pk}'
