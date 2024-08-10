from django.urls import path
from . import views

app_name = 'api-v1'
urlpatterns = [
    # REGISTRATION
    path("register", views.UserRegisterEndpoint.as_view(), name='register'),
    # VERIFICATION

    # LOGIN JWT

    # /jwt/create/
    # /jwt/refresh/
    # /jwt/verify/

    # Password Resetting
    # Password Forgotten handler
]

