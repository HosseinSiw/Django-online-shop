from django.db import models
from django.conf import settings

PAYMENT_STATUS_CHOICES = [
    ("P", "Pending"),
    ("S", "Success",),
    ("F", "Failed"),
]

user_model = settings.AUTH_USER_MODEL


class PaymentModel(models.Model):
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    authority_id = models.CharField(max_length=255,)
    ref_id = models.BigIntegerField(null=True, blank=True)
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=0,)
    response_json = models.JSONField(default=dict)
    response_code = models.IntegerField(null=True, blank=True)
    payment_status = models.CharField(choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_CHOICES[0][0],
                                      max_length=1)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.authority_id
