from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView
from . import views

app_name = 'api-v1'
urlpatterns = [
    # REGISTRATION
    path("register", views.UserRegisterEndpoint.as_view(), name='register'),
    # VERIFICATION
    path("activate/<str:token>/", views.UserActivationEndpoint.as_view(), name='activate'),
    # /jwt/create/
    path("jwt/create/", views.CustomTokenObtainEndpoint.as_view(), name='jwt_create'),
    # /jwt/refresh/
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    # /jwt/verify/
    path("jwt/verify/", TokenVerifyView.as_view(), name='jwt_verify'),
    # Password Resetting (updating)
    path("password/resset/<str:token>/", views.PasswordResetEndpoint.as_view(), name='password_reset'),
    # Password resetting request
    path("password/reset/", views.RequestPasswordResettingEndpoint.as_view(), name='password_reset_done'),
]
