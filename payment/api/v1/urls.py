from django.urls import path
from . import views


app_name = 'api-v1'
urlpatterns = [
    path("payment/request/", views.PaymentRequestView.as_view(), name="payment_request"),
    path("payment/verify/", views.PaymentVerifyView.as_view(), name="payment_verify"),
]
