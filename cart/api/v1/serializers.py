from rest_framework import serializers
from ...models import Cart, CartItem
from store.api.v1.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


"""
class CartSerializer(ModelSerializer):
    total_price = serializers.SerializerMethodField(source="get_total_price")
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ('user', "items", "total_price")

    def get_total_price(self, obj):
        return obj.total_price
"""


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,)

    class Meta:
        model = Cart
        fields = ("user", "items",)
