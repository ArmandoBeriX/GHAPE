from django.db import models
from django.contrib.auth.models import User, Group

class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación uno a uno con el modelo User
    activo = models.BooleanField(default=True)                 # Estado activo
    personal = models.BooleanField(default=False)                  # Permisos de staff
    creado = models.DateTimeField(auto_now_add=True)         # Fecha de creación
    grupo = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    año = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username  # Devuelve el nombre de usuario del modelo User