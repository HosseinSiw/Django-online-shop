from rest_framework import serializers
from ...models import Cart, CartItem
from store.api.v2.serializers import ProductSerializerV2


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializerV2()

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['product'] = ProductSerializerV2(instance, context=self.context, many=True).data
        return rep


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    # total_price = serializers.Met()

    class Meta:
        model = Cart
        fields = ('user', 'items', "total_price",)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['username'] = instance.user.username
        return rep