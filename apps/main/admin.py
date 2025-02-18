from django.contrib import admin
from .models import Gabarit
# Register your models here.


@admin.register(Gabarit)
class GabaritAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'high', 'length', 'width', 'created_date']
    search_fields = ['name']
