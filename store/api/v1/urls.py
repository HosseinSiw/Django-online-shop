from django.urls import path
from . import views


app_name = 'api-v1'
urlpatterns = [
    # All products
    path('', views.ProductHomeView.as_view(), name='index'),
    # A single product (detail page)
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-details'),
    # Add to Card Endpoint.
    path('cart/add/<int:id>/', views.AddToCartView.as_view(), name='add-to-card'),
    # View Card Endpoint.
    path('card/', views.MyCartView.as_view(), name='my-card'),

    # Remove Card Item Endpoint.
    path('card/remove/<int:id>/', views.RemoveFromCartView.as_view(), name='remove'),
    # Clear Card Endpoint.
    path("card/clear/", views.ClearCartView.as_view(), name='clear-cart'),
    # Apply Coupon to Card Endpoint.
]
