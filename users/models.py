import uuid
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from datetime import timedelta
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Personal Information
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=255, unique=True, null=False, blank=False)
    # Permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Dating Information
    date_joined = models.DateTimeField(auto_now_add=True, null=True)

    # Password information
    password_reset_times = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class PasswordResetModel(models.Model):
    """
    This Model represents the password reset process of each user, and its created whenever a new user is created.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    times = models.IntegerField(default=0, validators=[MaxValueValidator(5)])
    token = models.CharField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True,)
    verified = models.BooleanField(default=True)

    def __str__(self):
        if self.times == 0:
            return f"User: {self.user.username} - zero times"
        else:
            return f"User: {self.user.username} - {self.token} - times: {str(self.times)}"

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

    def generate_reset_token(self):
        self.token = str(uuid.uuid4())
        self.times += 1
        return self.token


# Signal which create a Password reset instance when a user creates.
@receiver(post_save, sender=CustomUser)
def create_user_reset_model(sender, instance, created, **kwargs):
    if created:
        PasswordResetModel.objects.create(user=instance, times=0, )
