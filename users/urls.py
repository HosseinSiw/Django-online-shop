from django.urls import path, include


app_name = 'users'
urlpatterns = [
    path("api/v1/", include("users.api.v1.urls"), name='api-v1'),
    # path("api/v2/", include("djoser.urls"), name='api-v2'),
]
