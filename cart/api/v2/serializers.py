from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from ...models import Cart, CartItem

from store.api.v2.serializers import ProductSerializerV2
from store.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializerV2()

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['product'] = ProductSerializerV2(instance.product, context=self.context,).data
        return rep


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('items', "total_price", 'user')

    def to_representation(self, instance):
        rep = super().to_representation(instance=instance)
        rep['user'] = instance.user.username
        return rep


class AddToCartSerializer(serializers.Serializer):
    """
    I've defined this serializer for validation product info.
    """

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError(_("Quantity must be greater than 0."))

    def validate_product_id(self, value):
        try:
            Product.objects.get(pk=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist.")
        return value

