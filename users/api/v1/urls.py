from django.urls import path
from . import views


urlpatterns = [
    path("user-regiser", views.UserRegistrationEndPoint.as_view(), name="user-registration"),

]
