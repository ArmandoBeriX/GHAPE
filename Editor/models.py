from django.db import models
from django.contrib.auth.models import User
from Recursos.models import Asignatura, Local, Grupo, Balance

class Turno(models.Model):
    tipos = [
        ('CP', 'Clase Practica'),
        ('C', 'Conferencia'),
        ('L', 'Laboratorio'),
        ('T', 'Taller'),
        ('S', 'Seminario')
    ]
    tipo = models.CharField(max_length=2, choices=tipos, default='C')  # Tipo de turno
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    local = models.ForeignKey(Local, on_delete=models.CASCADE)
    dia = models.PositiveSmallIntegerField(blank=True, null=True)  # Día de la semana (1-7)
    clase = models.PositiveSmallIntegerField(blank=True, null=True)  # Clase o sesión
    horario = models.ForeignKey('Horario', on_delete=models.CASCADE, related_name='turnos')  # Relación con Horario
    creador = models.ForeignKey(User, on_delete=models.CASCADE)  # Creador del turno

    def __str__(self):
        return f"{self.asignatura} en {self.local} - Tipo: {self.tipo} - El: {self.dia} a {self.clase}"

class Horario(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    semana = models.PositiveSmallIntegerField()  # Número de la semana
    balance = models.ForeignKey(Balance, on_delete=models.CASCADE)  # Nuevo campo para relacionar con Balance
    creador = models.ForeignKey(User, on_delete=models.CASCADE)  # Creador del horario
    publicado = models.BooleanField(default=False)  # Nuevo campo para indicar si el horario está publicado

    def __str__(self):
        return f"Horario para {self.grupo} - Semana: {self.semana} (Balance ID: {self.balance.id}) del usuario {self.creador}"
   