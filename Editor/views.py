from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import *
from .models import *
from .models import Turno
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.views.decorators.cache import cache_page
from django.contrib import messages

from django.db.models import Prefetch
# Create your views here.









def principalView(request):
    # Obtener todos los horarios publicados
    horarios_publicados = Horario.objects.filter(publicado=True).select_related('grupo', 'balance')

    # Definir los rangos para las clases y días
    range_list = range(1, 7)  # Clases (1-6)
    range_lista = range(1, 6)  # Días (1-5)

    return render(request, 'Base/principal.html', {
        'horarios_publicados': horarios_publicados,
        'range_list': range_list,
        'range_lista': range_lista,
    })


@login_required
def selectorView(request):
    return render(request, 'Base/selector.html')




@login_required
def l_horarios(request, balance_id=None):
    # Verificar si el usuario es administrador
    is_admin = request.user.groups.filter(name='Administrador').exists()

    # Obtener todos los balances del usuario
    if is_admin:
        balances = Balance.objects.all()  # Administrador puede ver todos los balances
    else:
        balances = Balance.objects.filter(creador=request.user)  # Filtrar por creador

    # Si no se proporciona un balance_id, redirigir al usuario a seleccionar uno
    if not balance_id:
        messages.warning(request, "Por favor selecciona un balance de carga.")
        return redirect('Seleccionar_Balance')  # Cambia esto por la vista adecuada

    # Obtener el balance correspondiente al ID proporcionado
    balance = get_object_or_404(Balance, id=balance_id)

    # Filtrar los horarios según el balance (solo aquellos con turnos)
    horarios = Horario.objects.filter(balance=balance).prefetch_related('turnos', 'grupo')

    return render(request, 'Lienzo/Horarios/listar_horarios.html', {
        'horarios': horarios,
        'balances': balances,
        'balance': balance,
        'is_admin': is_admin,  # Pasar la variable is_admin al contexto
        'range_list': range(1, 7),  # Clases (1-6)
        'range_lista': range(1, 6),  # Días (1-5)
    })

#crear
@login_required
def c_horarios(request, balance_id):
    balance = get_object_or_404(Balance, id=balance_id, creador=request.user)
    grupos_usuario = Grupo.objects.filter(creador=request.user)
    grupos_con_horario = Horario.objects.filter(balance=balance, creador=request.user).values_list('grupo_id', flat=True)
    grupos_sin_horario = grupos_usuario.exclude(id__in=grupos_con_horario)
    asignaturas = Asignatura.objects.filter(creador=request.user)
    locales = Local.objects.filter(creador=request.user)
    is_admin = request.user.groups.filter(name='Administrador').exists()

    if request.method == 'POST':
        turnos_a_guardar = []
        grupos_seleccionados = request.POST.getlist('grupos[]')
        errores = []

        if not grupos_seleccionados:
            messages.warning(request, "No se han seleccionado grupos.")
            return redirect('Semanas')

        for grupo_id in grupos_seleccionados:
            grupo = Grupo.objects.get(id=grupo_id)
            horario = Horario.objects.create(
                grupo=grupo,
                semana=balance.numero_semana,
                balance=balance,
                creador=request.POST.get('creador') if is_admin else request.user
            )

            turnos_creados = 0
            for clase in range(1, 7):
                for dia in range(1, 6):
                    asignatura_id = request.POST.get(f'turnos[{grupo_id}][{clase}][{dia}][asignatura]')
                    local_id = request.POST.get(f'turnos[{grupo_id}][{clase}][{dia}][local]')
                    tipo_turno = request.POST.get(f'turnos[{grupo_id}][{clase}][{dia}][tipo]')

                    if not (asignatura_id and local_id and tipo_turno):
                        continue

                    local_ocupado = Turno.objects.filter(
                        local_id=local_id,
                        dia=dia,
                        clase=clase,
                        horario__balance__numero_semana=balance.numero_semana
                    ).exists()

                    if local_ocupado:
                        local = Local.objects.get(id=local_id)
                        local_nombre = f"{local.tipo}-{local.piso}{local.numero:02d}"
                        # Mensaje modificado para incluir el grupo
                        errores.append(
                            f"El local {local_nombre} ya está ocupado en la clase {clase} del día {dia} "
                            f"(Grupo: {grupo.facultad}{grupo.year}0{grupo.grupo})."
                        )
                    else:
                        turnos_a_guardar.append(Turno(
                            asignatura_id=asignatura_id,
                            local_id=local_id,
                            dia=dia,
                            clase=clase,
                            tipo=tipo_turno,
                            creador=request.POST.get('creador') if is_admin else request.user,
                            horario=horario
                        ))
                        turnos_creados += 1

            if turnos_creados == 0:
                horario.delete()
                messages.warning(request, f"No se han creado turnos para el grupo {grupo.facultad}{grupo.year}0{grupo.grupo}. El horario se eliminó.")

        if errores:
            for error in errores:
                messages.error(request, error)
            return render(request, 'Lienzo/Horarios/crear_horarios.html', {
                'grupos': grupos_sin_horario,
                'asignaturas': asignaturas,
                'locales': locales,
                'balance': balance,
                'range_list': range(1, 6),
                'range_lista': range(1, 7),
                'tipos_turno': Turno.tipos,
                'is_admin': is_admin,
                'users': User.objects.all() if is_admin else []
            })

        if turnos_a_guardar:
            Turno.objects.bulk_create(turnos_a_guardar)
        return redirect('Semanas')

    return render(request, 'Lienzo/Horarios/crear_horarios.html', {
        'grupos': grupos_sin_horario,
        'asignaturas': asignaturas,
        'locales': locales,
        'balance': balance,
        'range_list': range(1, 6),
        'range_lista': range(1, 7),
        'tipos_turno': Turno.tipos,
        'is_admin': is_admin,
        'users': User.objects.all() if is_admin else []
    })

#quitar 
@login_required
def q_horarios(request, horario_id):
    # Obtener el horario asegurándose de que existe
    horario = get_object_or_404(Horario, id=horario_id)  # No filtrar por creador

    # Verificar si el usuario es el creador o un administrador
    is_creator = horario.creador == request.user
    is_admin = request.user.groups.filter(name='Administrador').exists()

    # Denegar acceso si no es ni creador ni administrador
    if not is_creator and not is_admin:
        return render(request, 'Lienzo/Horarios/quitar_horarios.html', {
            'horario': horario,
            'error': "No tienes permiso para eliminar este horario."
        })

    # Obtener los turnos asociados al horario
    turnos = Turno.objects.filter(horario=horario)

    if request.method == 'POST':
        # Eliminar todos los turnos relacionados
        turnos.delete()
        # Eliminar el horario
        horario.delete()
        
        return redirect('Listar_Horarios', balance_id=horario.balance.id)  # Redirigir a la lista de horarios

    return render(request, 'Lienzo/Horarios/quitar_horarios.html', {
        'horario': horario,
        'turnos': turnos,
        'range_list': range(1, 7),  # Clases (1-6)
        'range_lista': range(1, 6),  # Días (1-5)
    })

#editar
@login_required
def e_horarios(request, horario_id):
    # Obtener el horario a editar
    horario = get_object_or_404(Horario, id=horario_id)

    # Verificar si el creador es el usuario autenticado
    is_creator = horario.creador == request.user

    # Verificar si el usuario es administrador
    is_admin = request.user.groups.filter(name='Administrador').exists()

    # Obtener los turnos asociados al horario
    turnos = Turno.objects.filter(horario=horario)

    # Obtener grupos, asignaturas y locales del usuario o todos si es admin
    if is_admin:
        grupos = Grupo.objects.all()  # Todos los grupos
        asignaturas = Asignatura.objects.all()  # Todas las asignaturas
        locales = Local.objects.all()  # Todos los locales
    else:
        grupos = Grupo.objects.filter(creador=request.user)
        asignaturas = Asignatura.objects.filter(creador=request.user)
        locales = Local.objects.filter(creador=request.user)

    # Lista para almacenar mensajes de error
    errores = []

    if request.method == 'POST':
        # Crear un conjunto de turnos a eliminar
        turnos_a_eliminar = set(turnos.values_list('id', flat=True))

        # Variable para verificar si hay al menos un turno válido
        hay_turnos_validos = False

        # Actualizar los turnos según la información enviada
        for clase in range(1, 7):
            for dia in range(1, 6):
                asignatura_id = request.POST.get(f'turnos[{clase}][{dia}][asignatura]')
                local_id = request.POST.get(f'turnos[{clase}][{dia}][local]')
                tipo_turno = request.POST.get(f'turnos[{clase}][{dia}][tipo]')

                # Si no hay datos válidos, omitir este turno
                if not (asignatura_id and local_id and tipo_turno):
                    continue

                # Buscar el turno existente
                turno = turnos.filter(clase=clase, dia=dia).first()

                if turno:
                    # Verificar si el local ya está ocupado en este día, clase y semana (excluyendo el turno actual)
                    local_ocupado = Turno.objects.filter(
                        local_id=local_id,
                        dia=dia,
                        clase=clase,
                        horario__balance__numero_semana=horario.balance.numero_semana
                    ).exclude(id=turno.id).exists()

                    if local_ocupado:
                        # Obtener el local para mostrar su nombre en el mensaje de error
                        local = Local.objects.get(id=local_id)
                        local_nombre = f"{local.tipo} - {local.piso}{local.numero:02d}"  # Formato: Tipo - PisoNúmero
                        errores.append(f"El local {local_nombre} ya está ocupado en la clase {clase} del día {dia} en la semana {horario.balance.numero_semana}.")
                    else:
                        # Si el local no está ocupado, actualizar el turno existente
                        turno.asignatura_id = asignatura_id
                        turno.local_id = local_id
                        turno.tipo = tipo_turno
                        turno.save()
                        # Eliminar de la lista de turnos a eliminar ya que se ha actualizado
                        turnos_a_eliminar.discard(turno.id)
                        hay_turnos_validos = True
                else:
                    # Verificar si el local ya está ocupado en este día, clase y semana
                    local_ocupado = Turno.objects.filter(
                        local_id=local_id,
                        dia=dia,
                        clase=clase,
                        horario__balance__numero_semana=horario.balance.numero_semana
                    ).exists()

                    if local_ocupado:
                        # Obtener el local para mostrar su nombre en el mensaje de error
                        local = Local.objects.get(id=local_id)
                        local_nombre = f"{local.tipo} - {local.piso}{local.numero:02d}"  # Formato: Tipo - PisoNúmero
                        errores.append(f"El local {local_nombre} ya está ocupado en la clase {clase} del día {dia} en la semana {horario.balance.numero_semana}.")
                    else:
                        # Si el local no está ocupado, crear el turno
                        Turno.objects.create(
                            asignatura_id=asignatura_id,
                            local_id=local_id,
                            dia=dia,
                            clase=clase,
                            tipo=tipo_turno,
                            creador=request.user,
                            horario=horario
                        )
                        hay_turnos_validos = True

        # Si hay errores, no guardar los cambios y mostrar los mensajes de error
        if errores:
            for error in errores:
                messages.error(request, error)
        else:
            # Eliminar los turnos marcados para eliminación
            Turno.objects.filter(id__in=turnos_a_eliminar).delete()

            # Cambiar el creador si es administrador y se proporciona un nuevo creador
            if is_admin:
                creador_id = request.POST.get('creador')
                if creador_id:
                    horario.creador = User.objects.get(id=creador_id)  # Obtener el nuevo creador por ID

            # Si no hay turnos válidos, eliminar el horario
            if not hay_turnos_validos:
                horario.delete()
                messages.warning(request, "El horario se eliminó porque no tiene turnos válidos.")
                return redirect('Listar_Horarios', balance_id=horario.balance.id)

            # Guardar los cambios en el horario
            horario.save()

            messages.success(request, "Horario actualizado exitosamente.")
            return redirect('Listar_Horarios', balance_id=horario.balance.id)

    return render(request, 'Lienzo/Horarios/editar_horarios.html', {
        'horario': horario,
        'turnos': turnos,
        'grupos': grupos,
        'asignaturas': asignaturas,
        'locales': locales,
        'range_list': range(1, 7),  # Clases (1-6)
        'range_lista': range(1, 6),  # Días (1-5)
        'tipos_turno': Turno.tipos,
        'is_admin': is_admin,  # Pasar la variable is_admin al contexto
        'users': User.objects.all() if is_admin else [],  # Pasar lista de usuarios si es admin
        'messages': messages.get_messages(request)  # Pasar mensajes de error
    })

#Publicacion o cambio del atributo publicado del horario
@login_required
def publicar_horarios(request, horario_id):
    # Obtener el horario a publicar
    horario = get_object_or_404(Horario, id=horario_id, creador=request.user)

    if request.method == 'POST':
        # Alternar el estado de publicado
        horario.publicado = not horario.publicado  # Cambia el estado a True o False
        horario.save()

        if horario.publicado:
            messages.success(request, "Horario publicado exitosamente.")
        else:
            messages.success(request, "Horario des-publicado exitosamente.")
        
        return redirect('Semanas')  # Redirigir a la página de Semanas

    # Definir los rangos para las clases y días
    range_list = range(1, 7)  # Clases (1-6)
    range_lista = range(1, 6)  # Días (1-5)

    return render(request, 'Lienzo/Horarios/publicar_horarios.html', {
        'horario': horario,
        'range_list': range_list,
        'range_lista': range_lista,
    })

#Ver el listado de semanas
@login_required
def l_semanas(request):
    is_admin = request.user.groups.filter(name='Administrador').exists()  # Verificar si es administrador
    
    if is_admin:
        # Si el usuario es administrador, mostrar todos los balances
        balances = Balance.objects.all()
    else:
        # Si no es administrador, mostrar solo los balances creados por el usuario
        balances = Balance.objects.filter(creador=request.user)

    return render(request, 'Base/listar_semanas.html', {'balances': balances, 'is_admin': is_admin})
