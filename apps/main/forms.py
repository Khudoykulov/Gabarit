from django import forms
from .models import Gabarit

class GabaritForm(forms.ModelForm):

    class Meta:
        fields = ['name' ,'high', 'length', 'width',]