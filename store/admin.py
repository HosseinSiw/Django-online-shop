from django.contrib import admin
from .models import Product, Category, Cart, CartItem, Coupon


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'total_price', "item_count")
    empty_value_display = 'N/A'

    fieldsets = (
        ("User info", {"fields": ("user",)}),
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', "stock", 'size', "is_active",)
    empty_value_display = 'N/A'
    ordering = ('stock',)
    search_fields = ('name',)
    list_filter = ('is_active',)
    fieldsets = (
        ("Product info", {"fields": ("name", "price", "stock", "size", "is_active",)}),
        ("Ownership", {"fields": ("owner",)}),
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)

admin.site.register(Category)
admin.site.register(Coupon)
