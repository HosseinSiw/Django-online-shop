from django.urls import path
from . import views

app_name = 'api-v1'
urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
]
