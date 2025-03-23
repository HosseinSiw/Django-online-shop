from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser as User
from ..models import Cart


'''
class TestCartAPIViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='email@email.com', password='123/test/456', username='eraser')
        self.cart = Cart.objects.get_or_create(user=self.user)

    def test_add_to_cart(self):
        add_to_cart_url = reverse('cart:api-v2:add-to-cart')
        print(reverse(add_to_cart_url))
        self.client.force_authenticate(user=self.user)
        self.assertEqual(2, 2)
'''