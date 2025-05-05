from django import forms
from .models import Grupo, Local, Asignatura, Profesor, Balance
from Administrador.models import *

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['facultad', 'year', 'grupo', 'matricula']
        widgets = {
            'facultad': forms.TextInput(attrs={
                'class': 'form-control',
                'value': '3',  # Valor predeterminado
                'placeholder': 'Ej: 3, 7, A, B...'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '5'
            }),
            'grupo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '20'
            }),
            'matricula': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            })
        }

    def __init__(self, *args, **kwargs):
        is_admin = kwargs.pop('is_admin', False)
        año_usuario = kwargs.pop('año_usuario', None)
        super().__init__(*args, **kwargs)
        
        if not is_admin and año_usuario:
            self.fields['year'].initial = año_usuario
            self.fields['year'].widget.attrs['readonly'] = True
        
        # Establecemos facultad predeterminada a "3" pero editable
        self.fields['facultad'].initial = '3'
        self.fields['facultad'].widget.attrs['value'] = '3'

class LocalForm(forms.ModelForm):
    class Meta:
        model = Local
        fields = ['tipo', 'piso', 'numero']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'piso': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control'})
        }

class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ['nombre', 'siglas', 'catedra']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'siglas': forms.TextInput(attrs={'class': 'form-control'}),
            'catedra': forms.TextInput(attrs={'class': 'form-control'})
        }

class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['nombre', 'asignatura', 'tipo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'asignatura': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'})
        }

class BalanceForm(forms.ModelForm):
    class Meta:
        model = Balance
        fields = ['numero_semana', 'dia_inicio', 'dia_fin']
        widgets = {
            'numero_semana': forms.NumberInput(attrs={'class': 'form-control'}),
            'dia_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dia_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }

    def clean(self):
        cleaned_data = super().clean()
        dia_inicio = cleaned_data.get("dia_inicio")
        dia_fin = cleaned_data.get("dia_fin")

        if dia_inicio and dia_fin:
            if dia_inicio > dia_fin:
                raise forms.ValidationError("La fecha de inicio no puede ser mayor que la fecha de fin.")
        return cleaned_data