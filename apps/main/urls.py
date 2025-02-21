from django.urls import path
from .views import GabaritView, CarsView
app_name = 'main'

urlpatterns = [
    path('', GabaritView.as_view(), name='index'),
    path('cars/', CarsView.as_view(), name='cars'),
]