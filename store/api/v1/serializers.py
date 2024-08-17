from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.urls import reverse

from ...models import Product


class ProductSerializer(ModelSerializer):
    relative_url = serializers.ReadOnlyField(source='get_relative_url')
    absolute_url = serializers.SerializerMethodField(source='get_absolute_url')

    class Meta:
        model = Product
        fields = ("name", 'price', "stock", "size", "absolute_url", "relative_url")

    def get_absolute_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(
            reverse("store:api-v1:product-detail", kwargs={"slug": obj.slug})
        )

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        slug = request.parser_context.get("kwargs").get('slug')
        if slug is None:
            return rep
        else:
            rep.pop("absolute_url", None)
            rep.pop("relative_url", None)
