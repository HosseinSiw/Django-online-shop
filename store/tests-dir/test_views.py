from django.shortcuts import get_object_or_404
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from store.api.v1.serializers import ProductSerializer
from store.models import Product, Category
from users.models import CustomUser


class TestProductHomeView(TestCase):
    def setUp(self):
        client = APIClient()
        user = CustomUser.objects.create_user(email="ema@ema.com", password="<PASSWORD>/5896", username="ali", is_verified=True)
        client.force_authenticate(user=user)
        category = Category.objects.create(name='name')
        product_1 = Product.objects.create(owner=user, name='testing-1', price=10.10, stock=1, size=41,
                                           category=category)
        product_2 = Product.objects.create(owner=user, name='testing-2', price=10.10, stock=1, size=41,
                                           category=category)
        product_3 = Product.objects.create(owner=user, name='testing-3', price=10.10, stock=1, size=41,
                                           category=category)

    def test_product_list(self):
        url = '/products/api/v1/'
        response = self.client.get(path=url)
        products = Product.objects.filter(is_active=True)
        serializer = ProductSerializer(products, many=True, context={'request': self.client.request()})

        self.assertEqual(serializer.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
