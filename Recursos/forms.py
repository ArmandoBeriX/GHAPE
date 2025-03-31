from django import forms
from .models import Grupo, Local, Asignatura, Profesor, Balance
from Administrador.models import *

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['facultad', 'grupo', 'matricula']  # Excluye 'year' porque lo estableceremos automáticamente

    # Este método se puede usar para agregar un campo adicional al contexto del formulario
    def __init__(self, *args, **kwargs):
        self.año_usuario = kwargs.pop('año_usuario', None)  # Extraer el año del usuario
        super().__init__(*args, **kwargs)

    def get_año_usuario(self):
        return self.año_usuario  # Método para obtener el año del usuario


class LocalForm(forms.ModelForm):
    

    class Meta:
        model = Local
        fields = ['tipo', 'piso', 'numero']  # Incluir 'creador'

class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ['siglas', 'nombre', 'catedra']  # Excluye 'creador'

class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['tipo', 'asignatura', 'nombre']  # Excluye 'creador'



class BalanceForm(forms.ModelForm):
    class Meta:
        model = Balance
        fields = ['numero_semana', 'dia_inicio', 'dia_fin']  # Excluye 'creador'
        widgets = {
            'dia_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dia_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        dia_inicio = cleaned_data.get("dia_inicio")
        dia_fin = cleaned_data.get("dia_fin")

        if dia_inicio and dia_fin:
            if dia_inicio > dia_fin:
                raise forms.ValidationError("La fecha de inicio no puede ser mayor que la fecha de fin.")
            if dia_fin < dia_inicio:
                raise forms.ValidationError("La fecha de fin no puede ser menor que la fecha de inicio.")

        return cleaned_data