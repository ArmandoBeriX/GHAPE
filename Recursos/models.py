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
    # Campos existentes
    siglas = models.CharField(max_length=10, default='')
    nombre = models.CharField(max_length=253)
    catedra = models.CharField(max_length=255, default='')
    creador = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Nuevos campos para frecuencia de clases
    clases_por_semana = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Clases por semana",
        help_text="Número de veces que esta asignatura se imparte cada semana"
    )
    
    clases_por_semestre = models.PositiveSmallIntegerField(
        default=15,
        verbose_name="Clases por semestre",
        help_text="Número total de clases que tendrá esta asignatura en el semestre"
    )
    
    # Campos para horarios preferentes
    MANANA = 'M'
    TARDE = 'T'
    AMBOS = 'A'
    HORARIO_CHOICES = [
        (MANANA, 'Mañana (8:00 AM - 12:30 PM)'),
        (TARDE, 'Tarde (12:30 PM - 4:50 PM)'),
        (AMBOS, 'Ambos horarios'),
    ]
    horario_preferente = models.CharField(
        max_length=1,
        choices=HORARIO_CHOICES,
        default=AMBOS,
        verbose_name="Horario preferente",
        help_text="Indica si la asignatura debe impartirse por la mañana, tarde o ambos"
    )
    
    def __str__(self):
        return f"{self.siglas}/{self.nombre}"

    class Meta:
        verbose_name = "Asignatura"
        verbose_name_plural = "Asignaturas"
        ordering = ['siglas']

class Local(models.Model):
    tipos = [('A', 'Aula'), ('SC', 'Salón de Conferencias'), ('L', 'Laboratorio')]
    tipo = models.CharField(max_length=2, choices=tipos, default='A')
    piso = models.PositiveSmallIntegerField(default=1)
    numero = models.PositiveSmallIntegerField(default=1)
    capacidad = models.PositiveSmallIntegerField(
        default=30,
        verbose_name="Capacidad",
        help_text="Cantidad máxima de personas que puede albergar"
    )
    
    class Meta:
        permissions = [
            ("can_manage_locales", "Puede gestionar locales académicos")
        ]
        unique_together = ['tipo', 'piso', 'numero']  # Evitar duplicados

    def __str__(self):
        return f"{self.tipo}-{self.piso}{self.numero:02d} (Cap: {self.capacidad})"

class Profesor(models.Model):
    tipo = models.CharField(max_length=2, choices=[('CP', 'Clase Practica'), ('C', 'Conferencia'), ('L', 'Laboratorio'), ('T', 'Taller'), ('S', 'Seminario')], default='C')
    asignatura = models.ForeignKey(Asignatura, null=True, blank=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=253)
    creador = models.ForeignKey(User, on_delete=models.CASCADE)
    grupos_ids = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name="IDs de Grupos",
        help_text="IDs de grupos asociados separados por comas (ej: 1,5,7)"
    )

    def get_grupos_list(self):
        """Devuelve una lista de IDs de grupos como enteros"""
        if not self.grupos_ids:
            return []
        return [int(gid.strip()) for gid in self.grupos_ids.split(',') if gid.strip().isdigit()]

    def set_grupos_list(self, ids_list):
        """Establece los IDs de grupos desde una lista"""
        self.grupos_ids = ','.join(map(str, ids_list))

    def get_grupos_objects(self):
        """Devuelve los objetos Grupo relacionados"""
        from .models import Grupo  # Import aquí para evitar circular imports
        ids = self.get_grupos_list()
        return Grupo.objects.filter(id__in=ids)

    def __str__(self):
        grupos_str = ', '.join(str(g) for g in self.get_grupos_objects())
        return f"{self.nombre} ({self.tipo}) - Grupos: {grupos_str if grupos_str else 'Ninguno'}"
    
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