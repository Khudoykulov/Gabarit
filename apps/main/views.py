from django.shortcuts import render
from .models import Gabarit
from django.views.generic import TemplateView, DetailView, ListView

class GabaritView(TemplateView):
    template_name = 'index.html'
