from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path("regiser", views.UserRegistrationEndPoint.as_view(), name="user-registration"),
    path("regiser/activation/<str:token>/", views.UserVerificationEndPoint.as_view(), name="user-activation"),
    # login JWT
    path("jwt/create/", views.CustomTokenObtainPairView.as_view(), name='jwt_create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt_verify'),

    # Password endpoints. (forgotten and reset.)
    path("forgot-password/<int:user_id>/", views.ForgotPasswordRequestView.as_view(), name='forgot_password'),
    path("reset-password/<str:token>/", views.ForgotPasswordConfirmView.as_view(), name='reset_password'),
    # being a seller endpoint.
    # path("selling/", views.SetUserAsSeller.as_view(), name='seller',),
]
