import pytest

from rest_framework import status
from rest_framework.test import APIClient

from django.urls import reverse

from ..models import CustomUser as User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    def make_user(username, email, password):
        return User.objects.create_user(username=username, email=email, password=password, is_verified=True)
    return make_user


@pytest.mark.django_db
class TestAuthViews:
    def test_login(self, api_client, create_user):
        # Create a test user
        create_user(username="alitest", email='alitest@test.com', password='lkj/5896/',)

        data = {"username": "alitest",
                "email": 'alitest@test.com',
                "password": 'lkj/5896/'}

        url = reverse('users:api-v1-urls:jwt_create')
        response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("access") is not None
        assert response.json().get("refresh") is not None

    def test_user_registration(self, api_client, create_user):
        data = {"username": "alitest",
                "email": "alitest@test.com",
                "password1": "<PASSWORD>/12356",
                "password": "<PASSWORD>/12356"
                }

        url = reverse('users:api-v1-urls:user-registration')
        response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.get(pk=1).username == "alitest"
        assert User.objects.get(pk=1).email == "alitest@test.com"
        assert User.objects.get(pk=1).password != "<PASSWORD>/12356"  # Password hashing test

    def test_user_registration_with_invalid_info(self, api_client, create_user):
        data = {"username": "alitest",
                "email": "alitest@test,com",
                "password1": "<PASSWORD>/12356",
                "password": "<PASSWORD>12356",
                }
        url = reverse('users:api-v1-urls:user-registration')
        response = api_client.post(url, data=data)
        print(response.json())
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.status_code != status.HTTP_201_CREATED
