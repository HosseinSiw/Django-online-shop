from django.urls import path, include


app_name = 'store'
urlpatterns = [
    path("api/v1/", include("store.api.v1.urls")),
    path('api/v2/', include('store.api.v2.urls')),
]
