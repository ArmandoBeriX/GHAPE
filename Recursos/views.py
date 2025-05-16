from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from .forms import *
from .models import *
from Editor.models import *
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
@method_decorator(grupo_requerido('Administrador'), name='dispatch')  # Solo admin
class CrearLocales(View):
    def get(self, request):
        local_form = LocalForm()
        return render(request, 'Recursos/Locales/crear_locales.html', {
            'form': local_form
        })

    def post(self, request):
        local_form = LocalForm(data=request.POST)
        if local_form.is_valid():
            local_form.save()
            return redirect('Listar_Locales')
        return render(request, 'Recursos/Locales/crear_locales.html', {
            'form': local_form
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
            return redirect('Listar_Asignaturas')
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
           
            return redirect('Listar_Grupos')
       
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
    is_admin = request.user.groups.filter(name='Administrador').exists()
    grupos_disponibles = Grupo.objects.all() if is_admin else Grupo.objects.filter(creador=request.user)

    if request.method == "POST":
        profesor_form = ProfesorForm(request.POST)
        if profesor_form.is_valid():
            nuevo_profesor = profesor_form.save(commit=False)
            nuevo_profesor.creador = request.user
            nuevo_profesor.save()
            return redirect('Listar_Profesores')
    else:
        profesor_form = ProfesorForm()

    return render(request, 'Recursos/Profesores/crear_profesores.html', {
        'form': profesor_form,
        'is_admin': is_admin,
        'grupos_disponibles': grupos_disponibles,
        'users': User.objects.all() if is_admin else []
    })

# Los listar
@method_decorator(login_required, name='dispatch')
@method_decorator(grupo_requerido('Profesor de Año'), name='dispatch')
@method_decorator(login_required, name='dispatch')
class ListarLocales(View):
    def get(self, request):
        locales = Local.objects.all()  # Todos ven los mismos locales
        return render(request, 'Recursos/Locales/listar_locales.html', {
            'locales': locales,
            'is_admin': request.user.groups.filter(name='Administrador').exists()
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
@grupo_requerido('Administrador')  # Solo admin
def e_locales(request, id):
    local = get_object_or_404(Local, id=id)
    
    if request.method == 'POST':
        form = LocalForm(request.POST, instance=local)
        if form.is_valid():
            form.save()
            return redirect('Listar_Locales') 
    else:
        form = LocalForm(instance=local)

    return render(request, 'Recursos/Locales/editar_locales.html', {'form': form})

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
    # Obtener el profesor asegurándose de que existe
    profesor = get_object_or_404(Profesor, id=id)
    
    # Verificar permisos
    is_admin = request.user.groups.filter(name='Administrador').exists()
    if not is_admin and profesor.creador != request.user:
        return render(request, '403.html', status=403)

    # Obtener grupos disponibles (todos para admin, solo los del usuario para no-admin)
    grupos_disponibles = Grupo.objects.all() if is_admin else Grupo.objects.filter(creador=request.user)

    if request.method == 'POST':
        form = ProfesorForm(request.POST, instance=profesor)
        if form.is_valid():
            profesor_editado = form.save(commit=False)
            
            # Manejar el creador solo si es admin
            if is_admin:
                creador_id = request.POST.get('creador')
                profesor_editado.creador = User.objects.get(id=creador_id)
            
            profesor_editado.save()
            return redirect('Listar_Profesores')
    else:
        # Inicializar el formulario con los grupos actuales
        initial_data = {
            'grupos_input': ','.join(map(str, profesor.get_grupos_list()))
        }
        form = ProfesorForm(instance=profesor, initial=initial_data)

    return render(request, 'Recursos/Profesores/editar_profesores.html', {
        'form': form,
        'profesor': profesor,
        'is_admin': is_admin,
        'grupos_disponibles': grupos_disponibles,
        'users': User.objects.all() if is_admin else []
    })

# Los quitar
@method_decorator(login_required, name='dispatch')
@method_decorator(grupo_requerido('Administrador'), name='dispatch')  # Solo admin
class QuitarLocales(View):
    def get(self, request, id):
        local = get_object_or_404(Local, id=id)
        return render(request, 'Recursos/Locales/quitar_locales.html', {
            'local': local
        })

    def post(self, request, id):
        local = get_object_or_404(Local, id=id)
        local.delete()
        return redirect('Listar_Locales')
        
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
@grupo_requerido('Administrador')  # Solo admin puede crear balances
def c_balances(request):
    balance_form = BalanceForm()

    if request.method == "POST":
        balance_form = BalanceForm(data=request.POST)
        if balance_form.is_valid():
            balance_form.save()  # Guardar directamente sin creador
            return redirect('Listar_Balances')

    return render(request, 'Recursos/Balances/crear_balances.html', {
        'form': balance_form,
        'is_admin': True  # Siempre será admin quien acceda
    })

@login_required
def l_balances(request):
    # Todos los usuarios ven los mismos balances
    balances = Balance.objects.all()
    return render(request, 'Recursos/Balances/listar_balances.html', {
        'balances': balances,
        'is_admin': request.user.groups.filter(name='Administrador').exists()
    })

@login_required
@grupo_requerido('Administrador')  # Solo admin puede editar balances
def e_balances(request, id):
    balance = get_object_or_404(Balance, id=id)

    if request.method == 'POST':
        form = BalanceForm(request.POST, instance=balance)
        if form.is_valid():
            form.save()
            return redirect('Listar_Balances')
    else:
        form = BalanceForm(instance=balance)

    return render(request, 'Recursos/Balances/editar_balances.html', {
        'form': form,
        'is_admin': True
    })


@login_required
@grupo_requerido('Administrador')  # Solo admin puede eliminar balances
def q_balances(request, id):
    balance = get_object_or_404(Balance, id=id)

    if request.method == 'POST':
        balance.delete()
        return redirect('Listar_Balances')

    return render(request, 'Recursos/Balances/quitar_balances.html', {
        'balance': balance,
        'is_admin': True
    })

#Filtrado avanzado
@login_required
def filtrar_locales(request):
    balances = Balance.objects.all().order_by('numero_semana')
    semana_seleccionada = request.GET.get('semana')
    ocupaciones = []
    
    if semana_seleccionada:
        semana_seleccionada = int(semana_seleccionada)
        ocupaciones = Turno.objects.filter(
            horario__balance__numero_semana=semana_seleccionada,
            horario__publicado=True  # Solo horarios publicados
        ).select_related(
            'local',
            'asignatura',
            'horario__balance',
            'horario__grupo'
        ).order_by(
            'dia',
            'clase'
        )
    
    return render(request, 'Recursos/Locales/filtrado_locales.html', {
        'balances': balances,
        'semana_seleccionada': semana_seleccionada,
        'ocupaciones': ocupaciones,
        'is_admin': request.user.groups.filter(name='Administrador').exists()
    })