from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from .forms import *
from .models import *
from Administrador.models import *
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.views import View

# Controlador de acceso
def grupo_requerido(grupo):
    def in_grupo(user):
        return user.groups.filter(name=grupo).exists()
    return user_passes_test(in_grupo)

@login_required
@grupo_requerido('Profesor de Año')
def recursosView(request):
    return render(request, 'Recursos/recursos.html')

# Para los Recursos

# Los crear
@method_decorator(login_required, name='dispatch')
class CrearLocales(View):
    def get(self, request):
        local_form = LocalForm()  # Crear una instancia del formulario

        # Verificar si el usuario es administrador
        is_admin = request.user.groups.filter(name='Administrador').exists()

        return render(request, 'Recursos/Locales/crear_locales.html', {
            'form': local_form,
            'is_admin': is_admin,
            'users': User.objects.all() if is_admin else []  # Pasar lista de usuarios si es admin
        })

    def post(self, request):
        local_form = LocalForm(data=request.POST)  # Crear una instancia del formulario con los datos POST

        # Verificar si el usuario es administrador
        is_admin = request.user.groups.filter(name='Administrador').exists()

        if local_form.is_valid():
            nuevo_local = local_form.save(commit=False)  # No guardar aún

            if is_admin:
                # Establecer el creador desde el formulario
                creador_id = request.POST.get('creador')
                nuevo_local.creador = User.objects.get(id=creador_id)  # Obtener el usuario por ID
            else:
                nuevo_local.creador = request.user  # Establecer el creador como el usuario autenticado

            nuevo_local.save()  # Ahora guardar
            return redirect(reverse('Crear_Locales') + '?ok')
        
        return render(request, 'Recursos/Locales/crear_locales.html', {
            'form': local_form,
            'is_admin': is_admin,
            'users': User.objects.all() if is_admin else []  # Pasar lista de usuarios si es admin
        })

@login_required
def c_asignaturas(request):
    asignatura_form = AsignaturaForm()

    # Verificar si el usuario es administrador
    is_admin = request.user.groups.filter(name='Administrador').exists()

    if request.method == "POST":
        asignatura_form = AsignaturaForm(data=request.POST)
        if asignatura_form.is_valid():
            nueva_asignatura = asignatura_form.save(commit=False)  # No guardar aún

            if is_admin:
                # Establecer el creador desde el formulario
                creador_id = request.POST.get('creador')
                nueva_asignatura.creador = User.objects.get(id=creador_id)  # Obtener el usuario por ID
            else:
                nueva_asignatura.creador = request.user  # Establecer el creador como el usuario autenticado

            nueva_asignatura.save()  # Ahora guardar
            return redirect(reverse('Crear_Asignaturas') + '?ok')
        else:
            return render(request, 'Recursos/Asignaturas/crear_asignaturas.html', {
                'form': asignatura_form,
                'is_admin': is_admin,
                'users': User.objects.all() if is_admin else []  # Pasar lista de usuarios si es admin
            })

    return render(request, 'Recursos/Asignaturas/crear_asignaturas.html', {
        'form': asignatura_form,
        'is_admin': is_admin,
        'users': User.objects.all() if is_admin else []  # Pasar lista de usuarios si es admin
    })

@login_required
def c_grupos(request):
    # Obtener el año del usuario actual
    usuario = get_object_or_404(Usuario, usuario=request.user)
    año_usuario = usuario.año  # Obtener el año del usuario

    # Verificar si el usuario es administrador
    is_admin = request.user.groups.filter(name='Administrador').exists()

    if request.method == "POST":
        grupo_form = GrupoForm(data=request.POST, año_usuario=año_usuario)  # Pasar año al formulario
        if grupo_form.is_valid():
            nuevo_grupo = grupo_form.save(commit=False)
            
            if is_admin:
                # Establecer el creador desde el formulario
                creador_id = request.POST.get('creador')
                nuevo_grupo.creador = User.objects.get(id=creador_id)  # Obtener el usuario por ID
            else:
                nuevo_grupo.creador = request.user  # Establecer el creador como el usuario autenticado
            
            nuevo_grupo.year = año_usuario  # Asignar el año del usuario
            nuevo_grupo.save()
           
            return redirect('Crear_Grupos')
       
    else:
        grupo_form = GrupoForm(año_usuario=año_usuario)  # Pasar año al formulario

    return render(request, 'Recursos/Grupos/crear_grupos.html', {
        'form': grupo_form,
        'año_usuario': año_usuario,  # Pasar el año al contexto para mostrarlo en la plantilla
        'is_admin': is_admin,  # Pasar la variable is_admin al contexto
        'users': User.objects.all() if is_admin else []  # Pasar lista de usuarios si es admin
    })

@login_required
def c_profesores(request):
    profesor_form = ProfesorForm()

    # Verificar si el usuario es administrador
    is_admin = request.user.groups.filter(name='Administrador').exists()

    if request.method == "POST":
        profesor_form = ProfesorForm(data=request.POST)
        if profesor_form.is_valid():
            nuevo_profesor = profesor_form.save(commit=False)  # No guardar aún
            
            if is_admin:
                # Establecer el creador desde el formulario
                creador_id = request.POST.get('creador')
                nuevo_profesor.creador = User.objects.get(id=creador_id)  # Obtener el usuario por ID
            else:
                nuevo_profesor.creador = request.user  # Establecer el creador como el usuario autenticado

            nuevo_profesor.save()  # Ahora guardar
            return redirect(reverse('Crear_Profesores') + '?ok')
        else:
            return render(request, 'Recursos/Profesores/crear_profesores.html', {
                'form': profesor_form,
                'is_admin': is_admin,
                'users': User.objects.all() if is_admin else []  # Pasar lista de usuarios si es admin
            })

    return render(request, 'Recursos/Profesores/crear_profesores.html', {
        'form': profesor_form,
        'is_admin': is_admin,
        'users': User.objects.all() if is_admin else []  # Pasar lista de usuarios si es admin
    })

# Los listar
@method_decorator(login_required, name='dispatch')
@method_decorator(grupo_requerido('Profesor de Año'), name='dispatch')
class ListarLocales(View):
    def get(self, request):
        is_admin = request.user.groups.filter(name='Administrador').exists()  # Verificar si es administrador
        
        if is_admin:
            # Si el usuario es administrador, mostrar todos los locales
            locales = Local.objects.all()
        else:
            # Si no es administrador, mostrar solo los locales creados por el usuario
            locales = Local.objects.filter(creador=request.user)

        return render(request, 'Recursos/Locales/listar_locales.html', {
            'locales': locales,
            'is_admin': is_admin
        })

@login_required
@grupo_requerido('Profesor de Año')
def l_asignaturas(request):
    is_admin = request.user.groups.filter(name='Administrador').exists()  # Verificar si es administrador
    
    if is_admin:
        # Si el usuario es administrador, mostrar todas las asignaturas
        asignaturas = Asignatura.objects.all()
    else:
        # Si no es administrador, mostrar solo las asignaturas creadas por el usuario
        asignaturas = Asignatura.objects.filter(creador=request.user)

    return render(request, 'Recursos/Asignaturas/listar_asignaturas.html', {'asignaturas': asignaturas, 'is_admin': is_admin})

@login_required
@grupo_requerido('Profesor de Año')
def l_grupos(request):
    is_admin = request.user.groups.filter(name='Administrador').exists()  # Verificar si es administrador
    
    if is_admin:
        # Si el usuario es administrador, mostrar todos los grupos
        grupos = Grupo.objects.all()
    else:
        # Si no es administrador, mostrar solo los grupos creados por el usuario
        grupos = Grupo.objects.filter(creador=request.user)

    return render(request, 'Recursos/Grupos/listar_grupos.html', {'grupos': grupos, 'is_admin': is_admin})

@login_required
@grupo_requerido('Profesor de Año')
def l_profesores(request):
    is_admin = request.user.groups.filter(name='Administrador').exists()  # Verificar si es administrador
    
    if is_admin:
        # Si el usuario es administrador, mostrar todos los profesores
        profesores = Profesor.objects.all()
    else:
        # Si no es administrador, mostrar solo los profesores creados por el usuario
        profesores = Profesor.objects.filter(creador=request.user)

    return render(request, 'Recursos/Profesores/listar_profesores.html', {'profesores': profesores, 'is_admin': is_admin})

@never_cache
# Los editar
@login_required
@grupo_requerido('Profesor de Año')
def e_locales(request, id):
    # Obtener el local asegurándose de que el creador es el usuario autenticado
    local = get_object_or_404(Local, id=id, creador=request.user)  # Verificar que el creador es el usuario actual

    if request.method == 'POST':
        form = LocalForm(request.POST, instance=local)
        if form.is_valid():
            form.save()
            return redirect('Listar_Locales') 
    else:
        form = LocalForm(instance=local)

    return render(request, 'Recursos/Locales/editar_locales.html', {'form': form})  # Corregir la plantilla

@login_required
@grupo_requerido('Profesor de Año')
def e_grupos(request, id):
    # Obtener el grupo asegurándose de que el creador es el usuario autenticado
    grupo = get_object_or_404(Grupo, id=id)

    # Verificar si el usuario es administrador
    is_admin = request.user.groups.filter(name='Administrador').exists()

    if request.method == 'POST':
        form = GrupoForm(request.POST, instance=grupo)
        if form.is_valid():
            # Si es administrador, establecer el creador desde el formulario
            if is_admin:
                creador_id = request.POST.get('creador')
                grupo.creador = User.objects.get(id=creador_id)  # Obtener el usuario por ID
            else:
                grupo.creador = request.user  # Establecer el creador como el usuario autenticado

            form.save()  # Guardar los cambios en el grupo
            return redirect('Listar_Grupos')  # Redirigir a la lista de grupos
    else:
        form = GrupoForm(instance=grupo)  # Cargar el grupo existente en el formulario

    return render(request, 'Recursos/Grupos/editar_grupos.html', {
        'form': form,
        'is_admin': is_admin,  # Pasar la variable is_admin al contexto
        'users': User.objects.all() if is_admin else []  # Pasar lista de usuarios si es admin
    })

@login_required
def e_asignaturas(request, id):
    # Obtener la asignatura asegurándose de que el creador es el usuario autenticado
    asignatura = get_object_or_404(Asignatura, id=id)

    # Verificar si el usuario es administrador
    is_admin = request.user.groups.filter(name='Administrador').exists()

    if request.method == 'POST':
        form = AsignaturaForm(request.POST, instance=asignatura)
        if form.is_valid():
            # Si es administrador, establecer el creador desde el formulario
            if is_admin:
                creador_id = request.POST.get('creador')
                asignatura.creador = User.objects.get(id=creador_id)  # Obtener el usuario por ID
            else:
                asignatura.creador = request.user  # Establecer el creador como el usuario autenticado

            form.save()
            return redirect('Listar_Asignaturas') 
    else:
        form = AsignaturaForm(instance=asignatura)

    return render(request, 'Recursos/Asignaturas/editar_asignaturas.html', {
        'form': form,
        'is_admin': is_admin,  # Pasar la variable is_admin al contexto
        'users': User.objects.all() if is_admin else []  # Pasar lista de usuarios si es admin
    })

@login_required
@grupo_requerido('Profesor de Año')
def e_profesores(request, id):
    # Obtener el profesor asegurándose de que el creador es el usuario autenticado
    profesor = get_object_or_404(Profesor, id=id)

    # Verificar si el usuario es administrador
    is_admin = request.user.groups.filter(name='Administrador').exists()

    if request.method == 'POST':
        form = ProfesorForm(request.POST, instance=profesor)
        if form.is_valid():
            # Si es administrador, establecer el creador desde el formulario
            if is_admin:
                creador_id = request.POST.get('creador')
                profesor.creador = User.objects.get(id=creador_id)  # Obtener el usuario por ID
            else:
                profesor.creador = request.user  # Establecer el creador como el usuario autenticado

            form.save()  # Guardar los cambios en el profesor
            return redirect('Listar_Profesores')  # Redirigir a la lista de profesores
    else:
        form = ProfesorForm(instance=profesor)  # Cargar el profesor existente en el formulario

    return render(request, 'Recursos/Profesores/editar_profesores.html', {
        'form': form,
        'is_admin': is_admin,  # Pasar la variable is_admin al contexto
        'users': User.objects.all() if is_admin else []  # Pasar lista de usuarios si es admin
    })

# Los quitar
@method_decorator(login_required, name='dispatch')
@method_decorator(grupo_requerido('Profesor de Año'), name='dispatch')
class QuitarLocales(View):
    def get(self, request, id):
        # Obtener el local asegurándose de que el creador es el usuario autenticado o si es un administrador
        local = get_object_or_404(Local, id=id)  # No filtrar por creador

        # Verificar si el usuario es el creador o un administrador
        is_creator = local.creador == request.user
        is_admin = request.user.groups.filter(name='Administrador').exists()

        return render(request, 'Recursos/Locales/quitar_locales.html', {
            'local': local,
            'is_creator': is_creator,
            'is_admin': is_admin
        })

    def post(self, request, id):
       
        local = get_object_or_404(Local, id=id)  

        is_creator = local.creador == request.user
        is_admin = request.user.groups.filter(name='Administrador').exists()

        if is_creator or is_admin:
            local.delete() 
            return redirect('Listar_Locales') 
        
        return render(request, 'Recursos/Locales/quitar_locales.html', {
            'local': local,
            'is_creator': is_creator,
            'is_admin': is_admin,
            'error': 'No tienes permiso para eliminar este local.'  
        })
        
@login_required
@grupo_requerido('Profesor de Año')
def q_grupos(request, id):
    # Obtener el grupo asegurándose de que el creador es el usuario autenticado
    grupo = get_object_or_404(Grupo, id=id, creador=request.user)  # Verificar que el creador es el usuario actual

    if request.method == 'POST':
        grupo.delete()
        return redirect('Listar_Grupos')

    return render(request, 'Recursos/Grupos/quitar_grupos.html', {'grupo': grupo})  # Corregir la variable a pasar

@never_cache
@login_required
@grupo_requerido('Profesor de Año')
def q_asignaturas(request, id):
    # Obtener la asignatura asegurándose de que existe
    asignatura = get_object_or_404(Asignatura, id=id)  # No filtrar por creador

    # Verificar si el usuario es el creador o un administrador
    is_creator = asignatura.creador == request.user
    is_admin = request.user.groups.filter(name='Administrador').exists()


    if request.method == 'POST':
        asignatura.delete()  # Eliminar la asignatura
      
        return redirect('Listar_Asignaturas')  # Redirigir a la lista de asignaturas

    return render(request, 'Recursos/Asignaturas/quitar_asignaturas.html', {'asignatura': asignatura})  # Pasar la asignatura a la plantilla

@login_required
@grupo_requerido('Profesor de Año')
def q_profesores(request, id):
    # Obtener el profesor asegurándose de que existe
    profesor = get_object_or_404(Profesor, id=id)  # No filtrar por creador

    # Verificar si el usuario es el creador o un administrador
    is_creator = profesor.creador == request.user
    is_admin = request.user.groups.filter(name='Administrador').exists()

    # Denegar acceso si no es ni creador ni administrador
    if not is_creator and not is_admin:
        return render(request, 'Recursos/Profesores/quitar_profesores.html', {
            'profesor': profesor,
            'error': "No tienes permiso para eliminar este profesor."
        })

    if request.method == 'POST':
        profesor.delete()  # Eliminar el profesor
        return redirect('Listar_Profesores')  # Redirigir a la lista de profesores

    return render(request, 'Recursos/Profesores/quitar_profesores.html', {'profesor': profesor})  # Pasar el profesor a la plantilla

#Exclusivo para los Balances

@login_required
def c_balances(request):
    balance_form = BalanceForm()

    # Verificar si el usuario es administrador
    is_admin = request.user.groups.filter(name='Administrador').exists()

    if request.method == "POST":
        balance_form = BalanceForm(data=request.POST)
        if balance_form.is_valid():
            nuevo_balance = balance_form.save(commit=False)  # No guardar aún

            if is_admin:
                # Establecer el creador desde el formulario
                creador_id = request.POST.get('creador')
                nuevo_balance.creador = User.objects.get(id=creador_id)  # Obtener el usuario por ID
            else:
                nuevo_balance.creador = request.user  # Establecer el creador como el usuario autenticado

            nuevo_balance.save()  # Ahora guardar
            return redirect('Listar_Balances')  # Asegúrate de tener esta URL configurada

    return render(request, 'Recursos/Balances/crear_balances.html', {
        'form': balance_form,
        'is_admin': is_admin,
        'users': User.objects.all() if is_admin else []  # Pasar lista de usuarios si es admin
    })

@login_required
@grupo_requerido('Profesor de Año')
def l_balances(request):
    is_admin = request.user.groups.filter(name='Administrador').exists()  # Verificar si es administrador
    
    if is_admin:
        # Si el usuario es administrador, mostrar todos los balances
        balances = Balance.objects.all()
    else:
        # Si no es administrador, mostrar solo los balances creados por el usuario
        balances = Balance.objects.filter(creador=request.user)

    return render(request, 'Recursos/Balances/listar_balances.html', {'balances': balances, 'is_admin': is_admin})

@login_required
@grupo_requerido('Profesor de Año')
def e_balances(request, id):
    # Obtener el balance asegurándose de que el creador es el usuario autenticado
    balance = get_object_or_404(Balance, id=id)

    # Verificar si el usuario es administrador
    is_admin = request.user.groups.filter(name='Administrador').exists()

    if request.method == 'POST':
        form = BalanceForm(request.POST, instance=balance)
        if form.is_valid():
            # Si es administrador, establecer el creador desde el formulario
            if is_admin:
                creador_id = request.POST.get('creador')
                balance.creador = User.objects.get(id=creador_id)  # Obtener el usuario por ID
            else:
                balance.creador = request.user  # Establecer el creador como el usuario autenticado

            form.save()  # Guardar los cambios en el balance
            return redirect('Listar_Balances')  # Redirigir a la lista de balances
    else:
        form = BalanceForm(instance=balance)  # Cargar el balance existente en el formulario

    return render(request, 'Recursos/Balances/editar_balances.html', {
        'form': form,
        'is_admin': is_admin,  # Pasar la variable is_admin al contexto
        'users': User.objects.all() if is_admin else []  # Pasar lista de usuarios si es admin
    })

@login_required
@grupo_requerido('Profesor de Año')
def q_balances(request, id):
    # Obtener el balance asegurándose de que existe
    balance = get_object_or_404(Balance, id=id)  # No filtrar por creador

    # Verificar si el usuario es el creador o un administrador
    is_creator = balance.creador == request.user
    is_admin = request.user.groups.filter(name='Administrador').exists()

    # Denegar acceso si no es ni creador ni administrador
    if not is_creator and not is_admin:
        return render(request, 'Recursos/Balances/quitar_balances.html', {
            'balance': balance,
            'error': "No tienes permiso para eliminar este balance."
        })

    if request.method == 'POST':
        balance.delete()  # Eliminar el balance
        return redirect('Listar_Balances')  # Redirigir a la lista de balances

    return render(request, 'Recursos/Balances/quitar_balances.html', {'balance': balance})  # Pasar el balance a la plantilla