from django import forms
from Recursos.models import *
from .models import *
from django.contrib.auth.forms import UserCreationForm




class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['asignatura', 'local']  # Excluimos 'posicion' del formulario
""""
class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['nombre', 'grupo', 'turnos']
"""