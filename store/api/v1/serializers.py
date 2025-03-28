from rest_framework import serializers
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...models import Product


class ProductSerializer(serializers.ModelSerializer):
    relative_url = serializers.ReadOnlyField(source='get_relative_url')
    absolute_url = serializers.SerializerMethodField(source='get_absolute_url')
    owner_username = serializers.ReadOnlyField(source='get_owner_username')
    owner_id = serializers.ReadOnlyField(source='get_owner_id')
    category_name = serializers.ReadOnlyField(source='get_category_name')
    average_rate = serializers.ReadOnlyField(source='get_average_rate')
    reviews = serializers.ReadOnlyField(source='get_reviews')

    class Meta:
        model = Product
        fields = ('id', "name",
                  'price', "stock", "size",
                  "absolute_url", "relative_url",
                  "owner_username", "owner_id", "category_name", "images", "average_rate", "reviews",)

    def get_absolute_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(
                reverse("store:api-v1:product-details", kwargs={"slug": obj.slug})
            )
        else:
            return None

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if request:
            slug = request.parser_context.get("kwargs").get('slug')
            if slug is None:
                rep.pop("stock", None)
                rep.pop("size", None)
                rep.pop("reviews", None)
                return rep
            else:
                rep.pop("absolute_url", None)
                rep.pop("relative_url", None)
                return rep
        return rep


class AddToCartSerializer(serializers.Serializer):
    """
    I defined this serializer class for validation purposes.
    """
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1,)

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError(_("Quantity must be greater than 0."))

    def validate_product_id(self, value):
        try:
            Product.objects.get(pk=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist.")
        return value
