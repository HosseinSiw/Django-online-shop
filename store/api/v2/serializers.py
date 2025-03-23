from rest_framework import serializers
from django.urls import reverse

from ...models import Product, Category


class ProductSerializerV2(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    relative_url = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', "name", 'owner',
                  "price", "stock", 'size', "absolute_url",
                  'category_name', 'slug', 'relative_url')

    def get_absolute_url(self, obj):
        request = self.context.get('request')
        if request:
            url = reverse("store:api-v2:product-details", kwargs={'slug': obj.slug})
            return request.build_absolute_uri(url)
        return None

    def get_relative_url(self, obj):
        return obj.get_relative_url()

    def get_category_name(self, obj):
        return obj.category.name

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")

        if request:
            parser_context = getattr(request, "parser_context", {})
            slug = parser_context.get("kwargs", {}).get("slug")

            if slug is not None:
                rep.pop("absolute_url", None)
                rep.pop("relative_url", None)
            else:
                rep.pop("stock", None)
                rep.pop("size", None)

        return rep

