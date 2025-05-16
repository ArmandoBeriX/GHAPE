"""
URL configuration for GHAPE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import *
urlpatterns = [
    path('Horarios/', l_horarios, name='Listar_Horarios'),

#para los horarios
    path('ListarHorarios/<int:balance_id>/', l_horarios, name='Listar_Horarios'),
    path('CrearHorarios/<int:balance_id>/', c_horarios, name='Crear_Horarios'),
    path('Eliminar_Horarios/<int:horario_id>/', q_horarios, name='Eliminar_Horarios'),
    path('Editar_Horarios/<int:horario_id>/', e_horarios, name='Editar_Horarios'),
    path('Publicar_Horarios/<int:horario_id>/', publicar_horarios, name='Publicar_Horarios'),
    #path('verificar-disponibilidad/', verificar_disponibilidad_local, name='verificar_disponibilidad'),


    path('Asignar_Profesores/<int:horario_id>/', asignar_profesores, name='Asignar_Profesores'),

    path('verificar-disponibilidad/', verificar_disponibilidad_local, name='verificar_disponibilidad'),

    path('',principalView, name='#'),
    
    path('Selector/', selectorView, name='Selector'),
  
    path('Principal/', principalView, name='Principal'),

    path('Semanas/', l_semanas, name='Semanas'),
    
    path('Vista_Previa/', vista_previa, name='Vista_Previa'),
]
