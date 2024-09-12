from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from django.dispatch import receiver

from users.models import CustomUser as User

from datetime import timedelta
from django.utils import timezone


size_choices = [(int(size), int(size)) for size in range(37, 46)]


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


class CartItem(models.Model):
    """
    This model will represent the items of each card.
    """
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        price = self.quantity * self.product.price
        return price

    class Meta:
        unique_together = ('product', 'cart',)
        verbose_name = 'Cart item'
        verbose_name_plural = 'Carts items'


class Cart(models.Model):
    """
    This model will represent the card of each user, and it will create whenever a user registered via a signal
    named: create_user_cart.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return f'Cart of {self.user.username}'

    @property
    def total_price(self):
        total = sum(item.total_price for item in self.items.all())
        return total

    @property
    def item_count(self):
        return self.items.count()

    @property
    def item_names(self):
        items = self.items.all()
        return [item.product.name for item in items]

    def clear_cart(self):
        self.items.all().delete()


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


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    """
    I used signals to create a new cart whenever a user registered.
    :param sender:  The User model.
    :param instance: The Cart model instance.
    :return: None.
    """
    if created:
        Cart.objects.create(user=instance)
