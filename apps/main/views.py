from django.shortcuts import render
from django.views.generic import TemplateView, ListView
import serial
from .models import Gabarit
# Server o'chirilganda portni yopish uchun signal qo'shish mumkin
import atexit
from django.http import JsonResponse
import os
import time
import json
from dotenv import load_dotenv
import pickle


class GabaritView(TemplateView):
    template_name = 'index.html'


def gabarit_json(request):
    file_path = 'object_sizes.pkl'
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            raw_data = pickle.load(file)
        
        # Musbat x_size va h_size qiymatlarini oxirgisini topish
        latest_h = None
        latest_x = None

        for item in raw_data:
            h = item.get('h_size', 0)
            x = item.get('x_size', 0)

            if h > 0:
                latest_h = h
            if x > 0:
                latest_x = x

        result = {
            "h": latest_h,
            "x": latest_x
        }

        return JsonResponse(result)
    
    else:
        return JsonResponse({'error': 'File not found'}, status=404)

class CarsView(ListView):
    model = Gabarit
    template_name = 'cars.html'
    context_object_name = 'cars'
    paginate_by = 5

    def get_queryset(self):
        return Gabarit.objects.all().order_by('-created_date')


def close_serial_port():
    global serial_port
    if serial_port is not None and serial_port.is_open:
        serial_port.close()
        print("Serial port yopildi")

atexit.register(close_serial_port)
