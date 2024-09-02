from django.urls import path
from . import views


app_name = 'api-v1'
urlpatterns = [
    # All products
    path('', views.ProductHomeView.as_view(), name='index'),
    # A single product (detail page)
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-details'),
    # Add to Card Endpoint.
    path('add-to-card/<int:id>/', views.AddToCartView.as_view(), name='add-to-card'),
    # View Card Endpoint.
    path('my-card/', views.MyCardView.as_view(), name='my-card'),
    # Update Card Item Endpoint.
    # Remove Card Item Endpoint.
    # Clear Card Endpoint.
    # Apply Coupon to Card Endpoint.
]
