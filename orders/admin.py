from django.contrib import admin
from .models import Order, OrderCoupon

admin.site.register(OrderCoupon)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('cart', 'order_date', 'order_total_price', 'status',)
    list_filter = ('cart', 'order_date', 'status')
    date_hierarchy = 'order_date'
    ordering = ('order_date',)
    search_fields = ('user', 'order_date', 'status')


admin.site.register(Order, OrderAdmin)
