from django.contrib import admin
from .models import Product, Category, Cart, CartItem, Coupon


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', "item_count", "item_names")
    empty_value_display = 'N/A'
    readonly_fields = ("user",)

    fieldsets = (
        ("User info", {"fields": ("user",)}),
        # ("Cart info", {"fields": ("total_price", "item_count",)})
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
