from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from ..api.v2.views import ProductDetailAPIViewV2

from store.api.v2.serializers import ProductSerializerV2
from users.models import CustomUser
from ..models import Product, Category


class TestProductHomeView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='testbygoxton@gmail.com',
         password="<PASSWORD/789>", username='goxtone')

        self.client.force_authenticate(user=self.user)
        self.cat = Category.objects.create(name='cat')
        self.product_1 = Product.objects.create(owner=self.user, name='testing-1', 
                                                price=10.10, stock=1, size=41,
                                                category=self.cat, is_active=True)
        self.product_2 = Product.objects.create(owner=self.user, name='testing-2', 
                                                price=10.10, stock=1, size=41,
                                                category=self.cat, is_active=True)
        self.product_3 = Product.objects.create(owner=self.user, name='testing-3', 
                                                price=10.10, stock=1, size=41,
                                                category=self.cat, is_active=True)
        self.factory = APIRequestFactory()

    def test_main_page_status_code(self):
        url = '/products/api/v2/'
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_main_page_data(self):
        url = reverse("store:api-v2:index")
        factory = APIRequestFactory()
        request = factory.get(url)
        response = self.client.get(url)  
        products = Product.objects.filter(name__contains='test')
        serializer = ProductSerializerV2(products, many=True, context={"request": request})
        self.assertEqual(response.data.get('results', []), serializer.data)

    def test_details_page_status_code(self):
        url = reverse('store:api-v2:product-details', kwargs={"slug": self.product_1.slug})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_detail_page_data(self):
        url = reverse('store:api-v2:product-details', kwargs={"slug": self.product_1.slug})
        
        response = self.client.get(url) 
        request = response.wsgi_request 
        
        view = ProductDetailAPIViewV2.as_view()
        force_response = view(request, slug=self.product_1.slug)
        expected_data = force_response.data  
        self.assertEqual(response.data, expected_data)

