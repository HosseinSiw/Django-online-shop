from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.ProductListAPIViewV2.as_view(), name='index'),  # index or home
    path('<slug:slug>/', v.ProductDetailAPIViewV2.as_view(), name='product-details'),
]
