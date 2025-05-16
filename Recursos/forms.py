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
        fields = ['tipo', 'piso', 'numero', 'capacidad']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'piso': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '10'
            }),
            'numero': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '50'
            }),
            'capacidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '200',
                'value': '30'
            })
        }

class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ['nombre', 'siglas', 'catedra', 'clases_por_semana', 'clases_por_semestre', 'horario_preferente']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'siglas': forms.TextInput(attrs={'class': 'form-control'}),
            'catedra': forms.TextInput(attrs={'class': 'form-control'}),
            'clases_por_semana': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '10',
                'step': '1'
            }),
            'clases_por_semestre': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '60',
                'step': '1'
            }),
            'horario_preferente': forms.Select(attrs={'class': 'form-select'})
        }

    def __init__(self, *args, **kwargs):
        is_admin = kwargs.pop('is_admin', False)
        super().__init__(*args, **kwargs)
        
        # Establecer valores por defecto
        self.fields['clases_por_semana'].initial = 1
        self.fields['clases_por_semestre'].initial = 15
        self.fields['horario_preferente'].initial = 'A'

class ProfesorForm(forms.ModelForm):
    grupos_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 1,3,5 (IDs separados por comas)'
        }),
        help_text="IDs de grupos separados por comas"
    )

    class Meta:
        model = Profesor
        fields = ['nombre', 'asignatura', 'tipo', 'grupos_input']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'asignatura': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.grupos_ids:
            self.initial['grupos_input'] = self.instance.grupos_ids

    def save(self, commit=True):
        instance = super().save(commit=False)
        grupos_str = self.cleaned_data.get('grupos_input', '')
        # Validar que todos los IDs existen
        from .models import Grupo
        ids_validos = []
        for gid in grupos_str.split(','):
            gid = gid.strip()
            if gid.isdigit() and Grupo.objects.filter(id=int(gid)).exists():
                ids_validos.append(gid)
        instance.grupos_ids = ','.join(ids_validos)
        if commit:
            instance.save()
        return instance

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