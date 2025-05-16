from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, update_session_auth_hash
from .forms import UserRegisterForm, UserNewPasswordForm, UserEditForm
from .models import *
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.http import JsonResponse

# Controlador de acceso
def grupo_requerido(grupo):
    def in_grupo(user):
        return user.groups.filter(name=grupo).exists()
    return user_passes_test(in_grupo)

# Los crear
@login_required
@grupo_requerido('Administrador')
def c_usuarios(request):
    usuario_form = UserRegisterForm()

    if request.method == "POST":
        usuario_form = UserRegisterForm(data=request.POST)
        if usuario_form.is_valid():
           
            usuario = usuario_form.save()
            
            grupo = usuario_form.cleaned_data.get('grupo')
            usuario.groups.add(grupo)

            # Crear o actualizar la instancia del modelo Usuario
            año = usuario_form.cleaned_data.get('año')  # Obtener el año del formulario
            Usuario.objects.create(usuario=usuario, año=año) 

            return redirect('Listar_Usuarios')
        else:
            return redirect(reverse('Crear_Usuario') + '?error')

    return render(request, 'Administracion/Usuarios/crear_usuarios.html', {'form': usuario_form})

# Los listar
@login_required
@grupo_requerido('Administrador')
def l_usuarios(request):
    # Obtener todos los usuarios de la tabla User
    all_users = User.objects.all()
    
    # Crear un diccionario para almacenar los años de cada usuario
    usuarios_con_año = {usuario.usuario.id: usuario.año for usuario in Usuario.objects.all()}

    # Preparar la lista de usuarios con sus años
    usuarios = []
    for user in all_users:
        año = usuarios_con_año.get(user.id, "No Asignado")  # Obtener el año o "No Asignado" si no existe
        usuarios.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'año': año,
            'is_active': user.is_active,
            'groups': user.groups.all()
        })

    return render(request, 'Administracion/Usuarios/listar_usuarios.html', {'usuarios': usuarios})

@never_cache
# Los editar
@login_required
@grupo_requerido('Administrador')
def e_usuarios(request, id):
    # Obtener el usuario y su perfil extendido (o crearlo si no existe)
    user = get_object_or_404(User, id=id)
    perfil_usuario, created = Usuario.objects.get_or_create(usuario=user)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            # Guardar datos básicos del User
            user = form.save()
            
            # Actualizar campos adicionales en el modelo Usuario
            perfil_usuario.año = form.cleaned_data.get('año', None)
            perfil_usuario.save()
            
            # Actualizar grupos (many-to-many necesita save_m2m)
            form.save()
            
            
            return redirect('Listar_Usuarios')
    else:
        # Inicializar el formulario con datos actuales
        form = UserEditForm(instance=user, initial={
            'año': perfil_usuario.año,
            'groups': user.groups.all()
        })

    context = {
        'form': form,
        'usuario': user,
        'perfil': perfil_usuario
    }
    return render(request, 'Administracion/Usuarios/editar_usuarios.html', context)

# Los quitar
@login_required
@grupo_requerido('Administrador')
def q_usuarios(request, id):
    # Obtener el usuario y su perfil extendido (si existe)
    user = get_object_or_404(User, id=id)
    
    try:
        perfil_usuario = Usuario.objects.get(usuario=user)
        tiene_perfil = True
    except Usuario.DoesNotExist:
        tiene_perfil = False
    
    if request.method == 'POST':
        username = user.username
        
        # Eliminar primero el perfil extendido si existe
        if tiene_perfil:
            perfil_usuario.delete()
        
        # Luego eliminar el usuario
        user.delete()
        
       
        return redirect('Listar_Usuarios')

    context = {
        'usuario': user,
        'tiene_perfil': tiene_perfil,
        'perfil': perfil_usuario if tiene_perfil else None
    }
    
    return render(request, 'Administracion/Usuarios/quitar_usuarios.html', context)

@login_required
@grupo_requerido('Administrador')
def cambiar_clave(request, id):
    usuario = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserNewPasswordForm(data=request.POST)
        if form.is_valid():
            # Cambiar la contraseña del usuario
            usuario.set_password(form.cleaned_data['new_password'])
            usuario.save() 
            update_session_auth_hash(request, usuario)
            
            return redirect('Listar_Usuarios') 
    else:
        form = UserNewPasswordForm()
    return render(request, 'Administracion/Usuarios/cambiar_clave.html', {'form': form})  