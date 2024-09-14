from rest_framework import serializers
from ...models import Cart, CartItem
from store.api.v1.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['product'] = ProductSerializer(instance, context=self.context, many=True).data
        return data


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,)

    class Meta:
        model = Cart
        fields = ("user", "items",)
