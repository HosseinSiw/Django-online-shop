from django.test import TestCase
from django.contrib.auth import authenticate
from unittest.mock import patch

from ..models import CustomUser as User


class CustomUserModelTest(TestCase):
    email = "test@test.com"
    name = "testing_name"
    username = "testing_username"
    superuser_name = "testing_superuser_name"
    superuser_mail = 'test@admin.com'

    def test_user_creation(self):
        user = User.objects.create_user(email=self.email, name=self.name, username=self.username, password="s@#4587df")
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.name, self.name)
        self.assertEqual(user.username, self.username)
        self.assertNotEqual(user.password, "s@#4587df")

    def test_superuser_creation(self):
        super_user = User.objects.create_superuser(email=self.superuser_mail, name=self.name,
                                                   username=self.superuser_name, password="<PASSWORD>@test45896")
        self.assertEqual(super_user.email, self.superuser_mail)
        self.assertEqual(super_user.name, self.name)
        self.assertEqual(super_user.username, self.superuser_name)
        self.assertNotEqual(super_user.password, "<PASSWORD>@test45896")  # Check password hashing

    def test_user_creation_without_username(self):
        """
        Check that users are able to use empty username or not.
        :return: None.
        """
        with self.assertRaises(ValueError):
            User.objects.create_user(email='email@ea.com', password='1245/test', username="")

    def test_required_fields(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, passowrd='a/1456sd', username=None)

    def test_user_authentication(self):
        User.objects.create_user(email="main@main.com", password='pass@123456', username="NONE")
        authenticated_user = authenticate(email='main@main.com', password='pass@123456')
        self.assertIsNotNone(authenticated_user)

    def test_simple_user_perms(self):
        user = User.objects.create_user(email="main@main2.com", password='pass@123456', username="NONE1")
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_verified, False)
        self.assertEqual(user.is_superuser, False)

    def test_superuser_perms(self):
        super_user = User.objects.create_superuser(email="email@super.com", password='R123/654', username='IN_TEST')
        self.assertEqual(super_user.is_superuser, True)
        self.assertEqual(super_user.is_staff, True)

    def test_string_representation(self):
        user = User.objects.create_user(email="main@main5.com", password='pass@123456', username="NON3E1")
        self.assertEqual(str(user), "NON3E1")

    def test_password_reset_signal(self):
        with patch("django.db.models.signals.post_save.send") as pass_reset_signal:
            User.objects.create_user(username="testuser", password="testpass123", email='passemail@jimi.com')
            self.assertTrue(pass_reset_signal.called)
            self.assertEqual(pass_reset_signal.call_count, 1)
            self.assertEqual(pass_reset_signal.call_args[1]['instance'].username, "testuser")
