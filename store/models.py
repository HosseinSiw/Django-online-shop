from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.template.defaultfilters import slugify

from users.models import CustomUser as User

size_choices = [(int(size), int(size)) for size in range(37, 46)]


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    stock = models.PositiveIntegerField(default=0)  # Use PositiveIntegerField to enforce non-negative values
    size = models.IntegerField(choices=size_choices)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=1)

    is_active = models.BooleanField(default=True)  # Allows for easy deactivation of products
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_relative_url(self):
        return f'/shoes/{self.slug}/'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image for {self.product.name}"


class Cart(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('products', 'user')  # Ensures a user can't add the same product to the cart more than once

    def __str__(self):
        return f"{self.user.username}'s Cart - {self.products.name} (x{self.quantity})"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
