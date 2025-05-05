from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class Grupo(models.Model):
    facultad = models.PositiveSmallIntegerField(default=3)
    year = models.PositiveSmallIntegerField(default=1)
    grupo = models.PositiveSmallIntegerField(default=1)
    matricula = models.PositiveSmallIntegerField(default=30)
    creador = models.ForeignKey(User, on_delete=models.CASCADE)  # Nuevo campo

    def __str__(self):
        return f"{self.facultad}{self.year}0{self.grupo}"

class Asignatura(models.Model):
    siglas = models.CharField(max_length=10, default='')
    nombre = models.CharField(max_length=253)
    catedra = models.CharField(max_length=255, default='')
    creador = models.ForeignKey(User, on_delete=models.CASCADE)  # Nuevo campo

    def __str__(self):
        return f"{self.siglas}/{self.nombre}"

class Local(models.Model):
    tipos = [('A', 'Aula'), ('SC', 'Salón de Conferencias'), ('L', 'Laboratorio')]
    tipo = models.CharField(max_length=2, choices=tipos, default='A')
    piso = models.PositiveSmallIntegerField(default=1)
    numero = models.PositiveSmallIntegerField(default=1)
    # Eliminado el campo creador ya que solo los admins pueden gestionar locales
    
    class Meta:
        permissions = [
            ("can_manage_locales", "Puede gestionar locales académicos")
        ]
        unique_together = ['tipo', 'piso', 'numero']  # Evitar duplicados

    def __str__(self):
        return f"{self.tipo}-{self.piso}{self.numero:02d}"  # Formato mejorado

class Profesor(models.Model):
    tipo = models.CharField(max_length=2, choices=[('CP', 'Clase Practica'), ('C', 'Conferencia'), ('L', 'Laboratorio'), ('T', 'Taller'), ('S', 'Seminario')], default='C')
    asignatura = models.ForeignKey(Asignatura, null=True, blank=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=253)
    creador = models.ForeignKey(User, on_delete=models.CASCADE)  # Nuevo campo

    def __str__(self):
        return f"{self.nombre} --> {self.tipo} de: {self.asignatura.siglas if self.asignatura else 'N/A'}"

class Balance(models.Model):
    numero_semana = models.PositiveIntegerField(unique=True)  # Semana única para todo el sistema
    dia_inicio = models.DateField(unique=True)  # No puede haber solapamiento
    dia_fin = models.DateField(unique=True)
    # Eliminar el campo creador
    
    class Meta:
        permissions = [
            ("can_manage_balances", "Puede gestionar semanas académicas")
        ]

    def __str__(self):
        return f"Semana {self.numero_semana} ({self.dia_inicio} a {self.dia_fin})"