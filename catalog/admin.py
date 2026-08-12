from django.contrib import admin

from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_tr', 'category', 'price', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured')
    search_fields = ('name_tr', 'name_en', 'slug', 'category__name_tr')
    prepopulated_fields = {'slug': ('name_tr',)}
    inlines = (ProductImageInline,)
    fieldsets = (
        ('Türkçe', {'fields': ('name_tr', 'description_tr')}),
        ('English', {'fields': ('name_en', 'description_en')}),
        ('Detaylar', {'fields': ('slug', 'category', 'price', 'image', 'sizes', 'colors', 'is_featured')}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_tr', 'slug')
    search_fields = ('name_tr', 'name_en', 'slug')
    prepopulated_fields = {'slug': ('name_tr',)}
    fieldsets = (
        ('Türkçe', {'fields': ('name_tr', 'description_tr')}),
        ('English', {'fields': ('name_en', 'description_en')}),
        ('Detaylar', {'fields': ('slug',)}),
    )
