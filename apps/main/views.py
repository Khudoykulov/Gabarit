from django.shortcuts import render
from django.views.generic import TemplateView, ListView
import serial
from .models import Gabarit
class GabaritView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ser = None

        # Serial portni ochamiz
        com_port = 'COM3'  # Arduino COM port
        baud_rate = 9600
        h, x, y, = 1, 2, 3
        # HTML sahifaga jo‘natiladigan qiymatlar
        context['h'] = h
        context['x'] = x
        context['y'] = y

        # try:
        #     ser = serial.Serial(com_port, baud_rate, timeout=2)  # 2 soniya kutish
        #     ser.flush()
        #
        #     if ser.in_waiting > 0:
        #         data = ser.readline().decode('latin-1').strip()
        #         data = data[:-4].split()
        #         # h, x, y = int(data[1]), int(data[3]), int(data[5])
        #         h, x, y, = 1, 2, 3
        #         # HTML sahifaga jo‘natiladigan qiymatlar
        #         context['h'] = h
        #         context['x'] = x
        #         context['y'] = y
        #
        # except Exception as e:
        #     context['error'] = f"Xatolik yuz berdi: {e}"
        #
        # finally:
        #     if ser:
        #        ser.close()  # Serial portni yopamiz
        print(context)
        Gabarit.objects.create(width=x, length=y, high=h)
        return context


class CarsView(ListView):
    model = Gabarit  # Model bilan bog'lash
    template_name = 'cars.html'  # Template nomi
    context_object_name = 'cars'  # Template ichida foydalaniladigan o'zgaruvchi
    paginate_by = 5  # Har bir sahifada 25 ta obyekt bo‘lishi

    def get_queryset(self):
        return Gabarit.objects.all().order_by('-created_date')  # Yangi ma'lumotlarni avval chiqarish

