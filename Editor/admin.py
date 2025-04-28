from django.contrib import admin
from .models import *

# Register your models here.



class TurnosAdmin(admin.ModelAdmin):
    list_display = ('asignatura', 'local')  # Puedes agregar más campos si es necesario
    search_fields = ('asignatura__nombre', 'local__codigo')  # Búsqueda por nombre de asignatura y código de local

 # Búsqueda por nombre del horario

# Registro de modelos en el admin

admin.site.register(Turno, TurnosAdmin)  # Registro del modelo Turno
 # Registro del modelo Horario
