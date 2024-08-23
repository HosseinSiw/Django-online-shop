from django.urls import path
from . import views


app_name = 'api-v1'
urlpatterns = [
    # All products
    path('', views.ProductHomeView.as_view(), name='index'),
    # A single product (detail page)
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-details'),
    # Add to Cart Endpoint.
    path('add-to-card/<int:id>/', views.AddToCartView.as_view(), name='add-to-card'),
    # View Cart Endpoint.
    # Update Cart Item Endpoint.
    # Remove Cart Item Endpoint.
    # Clear Cart Endpoint.
    # Apply Coupon Endpoint.
]
