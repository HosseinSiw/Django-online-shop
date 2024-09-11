from django.urls import path
from . import views as v

urlpatterns = [
    path("my_orders/", v.OrderListAPIView.as_view(), name='orders-list')
]
