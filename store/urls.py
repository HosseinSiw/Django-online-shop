from django.urls import path, include


urlpatterns = [
    path("api-v1/", include("store.api.v1.urls")),
]
