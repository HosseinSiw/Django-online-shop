from django.urls import path
from . import views as v

app_name = 'api-v2'

urlpatterns = [
    path('my-cart/', v.MyCartViewV2.as_view(), name='my-cart')
]
