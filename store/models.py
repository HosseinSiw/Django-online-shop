from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.defaultfilters import slugify
from django.utils import timezone

from decimal import Decimal
from datetime import timedelta


size_choices = [(int(size), int(size)) for size in range(37, 46)]
User = settings.AUTH_USER_MODEL


class Product(models.Model):
    """
    The main product model.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100, null=False, blank=False)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    stock = models.PositiveIntegerField(default=1)  # Use PositiveIntegerField to enforce non-negative values
    size = models.IntegerField(choices=size_choices)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=1)

    is_active = models.BooleanField(default=True)  # Allows for easy deactivation of products
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        generating slug for the model.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_relative_url(self):
        """
        :return: Relative url of product from the landing page.
        """
        return f'/{self.slug}/'

    def get_owner_username(self):
        """
        I used these methods on my serializers /api/v1/serializers.py
        :return: the username of the owner of the product.
        """
        return self.owner.username

    def get_owner_id(self):
        return self.owner.id

    def get_category_name(self):
        return self.category.name

    def get_average_rate(self):
        if len(self.rates.all()) == 0:
            return 5
        else:
            rates = [int(i.rate) for i in self.rates.all()]
            return sum(rates) / len(rates)

    def get_reviews(self):
        if len(self.rates.all()) != 0:
            return self.rates.all()
        else:
            return None


class ProductImage(models.Model):
    """
    This model will represent the Images of each product.
    """
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image for {self.product.name}"


class Category(models.Model):
    """
    This model will represent the categories of products.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Coupon(models.Model):
    code = models.CharField(max_length=15, unique=True)
    percent = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    valid_days = models.IntegerField(default=14)  # two weeks validation for each coupon by default.
    expired = models.BooleanField(default=False)

    def is_valid(self):
        time_valid = self.created_at + timedelta(days=self.valid_days)
        now = timezone.now()

        if now < time_valid and not self.expired:
            return True
        else:
            return False

    def __str__(self):
        return f"Code: {self.code}, Days: {self.valid_days}, Expired: {self.expired}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rates')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.CharField(max_length=50, null=True, blank=True)
