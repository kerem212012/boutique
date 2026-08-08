from django.contrib import admin

from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'price', 'is_featured', 'created_at')
	list_filter = ('category', 'is_featured')
	search_fields = ('name', 'slug', 'category__name')
	prepopulated_fields = {'slug': ('name',)}
	inlines = (ProductImageInline,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug')
	search_fields = ('name', 'slug')
	prepopulated_fields = {'slug': ('name',)}
