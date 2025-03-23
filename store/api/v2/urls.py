from django.urls import path
from . import views as v


app_name = 'api-v2'
urlpatterns = [
    path('', v.ProductListAPIViewV2.as_view(), name='index'),
    path('<slug:slug>/', v.ProductDetailAPIViewV2.as_view(), name='product-details'),
]
