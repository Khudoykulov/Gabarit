from django.urls import path
from .views import GabaritView, CarsView, gabarit_json
app_name = 'main'

app_name = 'app'
urlpatterns = [
    path('', GabaritView.as_view(), name='index'),
    path('gab', gabarit_json, name='gab'),
    path('cars/', CarsView.as_view(), name='cars'),
]