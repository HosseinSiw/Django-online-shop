from django.contrib import admin
from .models import PaymentModel


@admin.register(PaymentModel)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "authority_id",
        "amount",
        "response_code",
        "payment_status",
        "created_date"
    )
