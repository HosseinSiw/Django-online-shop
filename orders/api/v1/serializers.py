from rest_framework import serializers

from ...models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("order_date", "order_total_price", "status", "purchased_items", "order_total_price")
        read_only_fields = ('created_at', 'updated_at', "order_total_price",
                            "status", "purchased_items")
