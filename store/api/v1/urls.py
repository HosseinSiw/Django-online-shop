from django.urls import path
from . import views


app_name = 'api-v1'
urlpatterns = [
    # All products
    path('', views.ProductHomeView.as_view(), name='index'),
    # A single product (detail page)
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-details'),
    # Add to Card Endpoint.

    # path('cart/add/<int:id>/', views.AddToCartView.as_view(), name='add-to-card'),
    # View Card Endpoint.

    # path('my-cart/', views.MyCartView.as_view(), name='my-card'),
    # path("my-cart-test/", views.get_cart_by_user_test, name='my-cart-test'),
    # path("my-cart/", views.MyCartViewEndpoint.as_view(), name='my-cart'),


    # Apply Coupon to Card Endpoint.
]
