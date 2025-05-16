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
     path('Recursos/', recursosView, name='Recursos'),
#Para los recursos

    # aqui los crear
    path('CrearLocales/',  CrearLocales.as_view(), name='Crear_Locales'),
    path('CrearAsignaturas/',  c_asignaturas, name='Crear_Asignaturas'),
    path('CrearGrupos/',  c_grupos, name='Crear_Grupos'),
    path('CrearProfesores/',  c_profesores, name='Crear_Profesores'),
    
    # aqui los listar
    path('ListarLocales/', ListarLocales.as_view(), name='Listar_Locales'),
    path('ListarAsignaturas/', l_asignaturas, name='Listar_Asignaturas'),
    path('ListarGrupos/', l_grupos, name='Listar_Grupos'),
    path('ListarProfesores/', l_profesores, name='Listar_Profesores'),

   # aqui los editar
    path('EditarLocales/<int:id>/', e_locales, name='Editar_Locales'),
    path('EditarAsignaturas/<int:id>/', e_asignaturas, name='Editar_Asignaturas'),
    path('EditarGrupos/<int:id>/', e_grupos, name='Editar_Grupos'),
    path('EditarProfesores/<int:id>/', e_profesores, name='Editar_Profesores'),

    #aqui los eliminar
    path('QuitarLocales/<int:id>/', QuitarLocales.as_view(), name='Quitar_Locales'),
    path('QuitarAsignaturas/<int:id>/', q_asignaturas, name='Quitar_Asignaturas'),
    path('QuitarGrupos/<int:id>/', q_grupos, name='Quitar_Grupos'),
    path('QuitarProfesores/<int:id>/', q_profesores, name='Quitar_Profesores'),
    
    path('CrearBalances/',  c_balances, name='Crear_Balances'),
    path('ListarBalances/',  l_balances, name='Listar_Balances'),
    path('EditarBalances/<int:id>/', e_balances, name='Editar_Balances'),
    path('QuitarBalances/<int:id>/', q_balances, name='Quitar_Balances'),

    path('Filtrar_Locales/', filtrar_locales, name='Filtrar_Locales'),

]
