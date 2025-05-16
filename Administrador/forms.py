from django import forms

from .models import Usuario # Asegúrate de importar tu modelo Profile
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth.models import User, Group

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    grupo = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Tipo de Usuario")
    año = forms.IntegerField(required=False, label="Año")  # Nuevo campo para el año

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'grupo', 'año']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        # Agregar clases de Bootstrap a los campos del formulario
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nombre de Usuario'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Correo Electrónico'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar Contraseña'
        })
        self.fields['grupo'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Tipo de Usuario'
        })
        self.fields['año'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Año (opcional)'
        })



class UserNewPasswordForm(forms.Form):
    new_password = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nueva Contraseña'
        }),
        min_length=8,  # Puedes ajustar la longitud mínima según tus requisitos
    )

    def clean_new_password(self):
        password = self.cleaned_data.get('new_password')
        # Aquí puedes agregar validaciones adicionales si es necesario
        return password


class UserEditForm(forms.ModelForm):
    año = forms.IntegerField(required=False, label="Año", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Año (opcional)'}))  # Nuevo campo para el año

    class Meta:
        model = User
        fields = ['username', 'email', 'groups', 'año']  # Incluye el campo de grupos y el nuevo campo 'año'

    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de Usuario'})
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'})
    )

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=True,
        label="Grupos"
    )

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)