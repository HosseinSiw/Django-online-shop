from django.urls import path
from . import views as v

app_name = 'api-v2'

urlpatterns = [
    path('my-cart/', v.MyCartViewV2.as_view(), name='my-cart'),
    path('add-to-cart/<int:product_id>/', v.AddToCartViewV2.as_view(), name='add-to-cart'),
    path('cart/clear/', v.CartClearViewV2.as_view(), name='cart-clear'),
]
