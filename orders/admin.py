from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 0
	readonly_fields = ('product', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'status', 'total', 'created_at')
	list_filter = ('status', 'created_at')
	search_fields = ('user__user__username', 'user__user__email')
	readonly_fields = ('user', 'total', 'created_at')
	fields = ('user', 'status', 'total', 'created_at')
	inlines = (OrderItemInline,)
