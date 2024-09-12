from django.urls import path
from . import views

app_name = "api-v1"
urlpatterns = [
    # View the user cart.
    path("my-cart", views.MyCartViewEndpoint.as_view(), name="my-cart"),
    # Remove Card Item Endpoint.
    path('cart/remove/<int:id>/', views.RemoveFromCartView.as_view(), name='remove'),
    # Clear Card Endpoint.
    path("cart/clear/", views.ClearCartView.as_view(), name='clear-cart'),
]
