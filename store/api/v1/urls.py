from django.urls import path
from . import views


app_name = 'api-v1'
urlpatterns = [
    path('', views.ProductHomeView.as_view(), name='index'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),
]
