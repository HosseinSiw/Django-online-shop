from ..api.v1.serializers import UserSerializer
from django.test import TestCase
from ..models import CustomUser as User


class UserSerializerTest(TestCase):
    serializer_class = UserSerializer

    def test_creation(self):
        data = {
            "email": "email@test.com",
            "password": "<PASSWORD>1245",
            "password1": "<PASSWORD>1245",
            "username": "John",
        }
        self.serializer_class().create(validated_data=data)

        self.assertEqual(User.objects.get(pk=1).email, data["email"])
        self.assertNotEqual(User.objects.get(pk=1).password, data["password"])
        self.assertEqual(User.objects.get(pk=1).username, data["username"])

    def test_validation(self):
        invalid_data = {
            "email": "email@test.com",
            "password": "123",
            "password1": "123",
            "username": "John",
        }
        serializer = self.serializer_class(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_output(self):
        instance = User.objects.create_user(email='EMAIL@rmal.com', password='<PASSWORD>@2345', username='John-doe')
        serialized_data = self.serializer_class(instance).data
        expected_data = {
            "email": "EMAIL@rmal.com",
            "username": "John-doe",
            "password": "<PASSWORD>@2345",
        }
        self.assertEqual(serialized_data['email'], expected_data['email'])
        self.assertEqual(serialized_data['username'], expected_data["username"])
        self.assertNotEqual(serialized_data['password'], expected_data["password"])
