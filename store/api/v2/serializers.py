from rest_framework import serializers
from django.urls import reverse

from ...models import Product, Category


class ProductSerializerV2(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField(source='get_absolute_url')
    relative_url = serializers.ReadOnlyField(source='get_relative_url')
    category__name = serializers.SerializerMethodField(source='get_category__name')

    class Meta:
        model = Product
        fields = ('id', "name", 'owner',
                  "price", "stock", 'size', "absolute_url",
                  'category__name', 'slug', 'relative_url')

    def get_absolute_url(self, obj):
        request = self.context.get('request')
        if request:
            url = reverse("store:api-v1:product-details", kwargs={'pk': obj.slug})
            return request.build_absolute_uri(url)
        else:
            return None

    def get_category__name(self, obj):
        return obj.category.name

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")
        if request:
            slug = request.parser_context.get("kwargs").get("slug")
            if slug is not None:
                rep.pop("absolute_url", None)
                rep.pop("relative_url", None)
            else:
                rep.pop("stock", None)
                rep.pop("size", None)
            return rep
        return rep
