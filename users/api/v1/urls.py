from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path("user-regiser", views.UserRegistrationEndPoint.as_view(), name="user-registration"),
    path("user-regiser/activation/<str:token>/", views.UserVerificationEndPoint.as_view(), name="user-activation"),
    # login JWT
    path("jwt/create/", views.CustomTokenObtainPairView.as_view(), name='jwt_create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt_verify'),
    # Password endpoints. (forgotten and reset.)
    # path()
    # being a seller endpoint.
]
