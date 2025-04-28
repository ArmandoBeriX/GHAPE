from django.contrib import admin
from .models import *

# Register your models here.

class AsignaturasAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'siglas')
    search_fields = ('nombre', 'siglas')

class LocalesAdmin(admin.ModelAdmin):
    list_display = ('numero', 'tipo')
    search_fields = ('codigo', 'tipo')

class GruposAdmin(admin.ModelAdmin):
    list_display = ('facultad', 'year', 'grupo')
    search_fields = ('year', 'grupo')

class ProfesoresAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'asignatura', 'tipo')
    search_fields = ('nombre', 'siglas')



# Registro de modelos en el admin
admin.site.register(Local, LocalesAdmin)
admin.site.register(Grupo, GruposAdmin)
admin.site.register(Profesor, ProfesoresAdmin)
admin.site.register(Asignatura, AsignaturasAdmin)