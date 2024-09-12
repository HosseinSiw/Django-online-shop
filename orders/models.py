from django.db import models
import uuid

from cart.models import Cart


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    shipping_address = models.CharField(max_length=500)

    STATUS_CHOICES = [
        ("P", "Pending"),
        ("S", "Shipped"),
        ("C", "Cancelled"),
        ("D", "Delivered",)
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="P")

    @property
    def purchased_items(self):
        """
        Enhance this method.
        :return: a fucking dict !
        """
        values = []
        items = self.cart.items.all()
        for item in items:
            values.append(f'{item.product.name} ({item.product.id}) * {item.quantity}\n')

        return values

    @property
    def order_total_price(self):
        if self.coupon:
            percent = (1 - self.coupon.amount)
            price = self.cart.total_price * percent
            return price
        else:
            return self.cart.total_price

    SHIPPING_METHOD_CHOICES = [
        ("EXP", "Express"),
        ("STD", "Standard"),
    ]
    shipping_method = models.CharField(max_length=3, choices=SHIPPING_METHOD_CHOICES, default="STD")
    order_notes = models.CharField(max_length=255, blank=True, null=True)
    coupon = models.ForeignKey('OrderCoupon', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"Order by {self.cart.user.username} ID: {self.order_id}"


class OrderCoupon(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=2, decimal_places=2, default=0.15)

    def __str__(self):
        return f"{self.name} -- {self.amount}"
