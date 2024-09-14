from django.urls import path, include


app_name = 'payment'
urlpatterns = [
    path('', include('payment.api.v1.urls'), name='index'),
]