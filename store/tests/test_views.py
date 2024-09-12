from django.shortcuts import get_object_or_404
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from store.api.v1.serializers import ProductSerializer
from users.api.utils import get_token_for_user

from users.models import CustomUser
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from ..models import Product, Cart, CartItem, Category

"""
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
"""


class AddToCartViewTest(APITestCase):
    """
    This class is a test class for the AddToCartView which is located on views.py in the current directory.
    endpoint url: /products/api/v1/add/{id}/
    """

    def setUp(self):
        self.user = CustomUser.objects.create_user(email="test@test.com", username='testuser', password='12345')
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            owner=self.user,
            name="Test Product",
            price=Decimal('50.00'),
            stock=10,
            size=40,
            category=self.category
        )
        self.cart, _ = Cart.objects.get_or_create(user=self.user)

        self.add_to_cart_url = reverse('store:api-v1:add-to-card', args=[self.product.id])

    def test_add_to_cart_authenticated(self):
        self.client = APIClient()
        token = get_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.post(self.add_to_cart_url, data={'quantity': 2, "product_id": self.product.id},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cart_item_quantity'], 2)
        self.assertEqual(response.data['product name'], self.product.name)
        self.assertEqual(response.data['product owner'], self.user.username)

        cart_item = CartItem.objects.get(cart_id=self.cart.id, product=self.product)
        self.assertEqual(cart_item.quantity, 2)

    def test_update_existing_cart_item(self):
        self.client = APIClient()
        token = get_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)

        response = self.client.post(self.add_to_cart_url, data={'quantity': 3}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cart_item_quantity'], 4)  # 1 + 3

        cart_item = CartItem.objects.get(cart=self.cart, product=self.product)
        self.assertEqual(cart_item.quantity, 4)

    def test_quantity_exceeds_stock(self):
        self.client = APIClient()
        token = get_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.post(self.add_to_cart_url, data={'quantity': self.product.stock + 2,
                                                                "product_id": self.product.id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Quantity exceeds available stock.')

    def test_add_to_cart_unauthenticated(self):
        response = self.client.post(self.add_to_cart_url, data={'quantity': 2}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_data(self):
        self.client = APIClient()
        token = get_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.post(self.add_to_cart_url, data={'quantity': 0}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
