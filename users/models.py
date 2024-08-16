from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from datetime import datetime, timedelta, timezone
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Personal Information
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    # Permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Dating Information
    date_joined = models.DateTimeField(auto_now_add=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class PasswordResetModel(models.Model):
    """
    This Model represents the password reset process of each user
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    times = models.IntegerField(default=0, validators=[MaxValueValidator(5)])
    token = models.CharField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True,)
    verified = models.BooleanField(default=True)

    def __str__(self):
        return f"User: {self.user.unsername} - {self.token} - times: {str(self.times)}"

    def times_valid(self):
        if self.times < 5:
            return True
        else:
            return False

    def time_valid(self):
        if self.created_time < timedelta(minutes=5):
            return True
        else:
            return False
