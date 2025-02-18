from django.urls import path
from .views import GabaritView
app_name = 'main'

urlpatterns = [
    path('index/', GabaritView.as_view(), name='index'),
]