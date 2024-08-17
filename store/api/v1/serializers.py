from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.urls import reverse

from ...models import Product


class ProductSerializer(ModelSerializer):
    # relative_url = serializers.Field(source='get_relative_url')
    # absolute_url = serializers.SerializerMethodField(source='get_absolute_url')

    class Meta:
        model = Product
        fields = ("name", 'price', "stock", "size",)

    def get_absolute_url(self, obj):
            request = self.get_context("request")
            return request.build_absolute_uri(
            reverse("store:api-v1:product-detail", kwargs={"slug": obj.slug})
        )

