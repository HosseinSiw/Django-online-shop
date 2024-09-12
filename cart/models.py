from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from store.models import Product
from users.models import CustomUser as User


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
