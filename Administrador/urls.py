
from django.urls import path
from .views import *
urlpatterns = [
     
    path('/CambiarClave/<int:id>/',  cambiar_clave, name='Cambiar_Clave'),
    
    # aqui los crear
   
    path('/CrearUsuarios/',  c_usuarios, name='Crear_Usuarios'),
    
    # aqui los listar
  
    path('ListarUsuarios/', l_usuarios, name='Listar_Usuarios'),

   # aqui los editar
   
    path('EditarUsuarios/<int:id>/', e_usuarios, name='Editar_Usuarios'),

    #aqui los eliminar
  
    path('QuitarUsuarios/<int:id>/', q_usuarios, name='Quitar_Usuarios'),
  

]
