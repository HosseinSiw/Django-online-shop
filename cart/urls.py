from django.urls import include, path


app_name = 'cart'
urlpatterns = [
    path("", include("cart.api.v2.urls"), name='api-v1')
]
