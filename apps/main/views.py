from django.shortcuts import render
from django.views.generic import TemplateView, ListView
import serial
from .models import Gabarit
class GabaritView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        com_port = 'COM3'  # Arduino COM portini moslang
        baud_rate = 9600
        h_max, h_min = 0, 30
        x_max, x_min = 0, 30
        y_max, y_min = 0, 30

        try:
            with serial.Serial(com_port, baud_rate, timeout=2) as ser:
                ser.flush()

                if ser.in_waiting > 0:
                    # Sensor ma’lumotlarini olish
                    data = ser.readline().decode('latin-1').strip()
                    data = data[:-4].split()

                    if len(data) >= 6:  # Ma'lumotlar formati to'g'ri ekanligini tekshiramiz
                        h, x, y = int(data[1]), int(data[3]), int(data[5])
                        print(h,x,y)

                        h_max = max(h_max, h)
                        h_min = min(h_min, h)
                        x_max = max(x_max, x)
                        x_min = min(x_min, x)
                        y_max = max(y_max, y)
                        y_min = min(y_min, y)

                        h_result = h_max - h_min
                        x_result = x_max - x_min
                        y_result = y_max - y_min

                        context['h'] = h_result
                        context['x'] = x_result
                        context['y'] = y_result

                        # Modelga saqlash
                        Gabarit.objects.create(width=x_result, length=y_result, high=h_result)

                        print(f"Saqlangan qiymatlar: H={h_result}, X={x_result}, Y={y_result}")

        except serial.SerialException as e:
            print(f"Xatolik: {e}")

        return context

class CarsView(ListView):
    model = Gabarit  # Model bilan bog'lash
    template_name = 'cars.html'  # Template nomi
    context_object_name = 'cars'  # Template ichida foydalaniladigan o'zgaruvchi
    paginate_by = 5  # Har bir sahifada 25 ta obyekt bo‘lishi

    def get_queryset(self):
        return Gabarit.objects.all().order_by('-created_date')  # Yangi ma'lumotlarni avval chiqarish

