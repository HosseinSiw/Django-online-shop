from django.urls import path, include


app_name = 'store'
urlpatterns = [
    path("api/v1/", include("store.api.v1.urls")),
]
