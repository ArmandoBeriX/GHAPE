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
from django.contrib.messages import get_messages
from django.http import JsonResponse
from django.db.models import Prefetch
# Create your views here.
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from django.db.models import Q  # Añade esta importación al inicio del archivo

@csrf_exempt
def verificar_disponibilidad_local(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            local_id = data.get('local_id')
            dia = data.get('dia')
            clase = data.get('clase')
            semana = data.get('semana')
            grupo_id = data.get('grupo_id')
            horario_id = data.get('horario_id')

            # Consulta base para locales ocupados (eliminada verificación de creador)
            query = Q(
                local_id=local_id,
                dia=dia,
                clase=clase,
                horario__balance__numero_semana=semana
            )

            # Excluir turnos del mismo grupo o del mismo horario (para edición)
            exclusion_query = Q()
            if grupo_id:
                exclusion_query |= Q(horario__grupo_id=grupo_id)
            if horario_id:
                exclusion_query |= Q(horario_id=horario_id)

            local_ocupado = Turno.objects.filter(query).exclude(exclusion_query).exists()

            return JsonResponse({
                'ocupado': local_ocupado,
                'local_id': local_id,
                'dia': dia,
                'clase': clase,
                'semana': semana
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)





def principalView(request):
    # 1. Obtener todos los horarios publicados con sus turnos
    horarios_publicados = Horario.objects.filter(
        publicado=True
    ).select_related('grupo', 'balance').prefetch_related(
        Prefetch('turnos', queryset=Turno.objects.select_related('asignatura', 'local')))
    
  
            
    
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

    # Todos los usuarios ven los mismos balances
    balances = Balance.objects.all()

    # Si no se proporciona un balance_id, redirigir al usuario a seleccionar uno
    if not balance_id:
        messages.warning(request, "Por favor selecciona una semana académica.")
        return redirect('Listar_Semanas')

    # Obtener el balance correspondiente al ID proporcionado
    balance = get_object_or_404(Balance, id=balance_id)

    # Filtrar los horarios según el balance (solo aquellos con turnos)
    horarios = Horario.objects.filter(balance=balance).prefetch_related(
        'turnos', 
        'grupo',
        'profesores'  # Prefetch para optimizar
    )

    return render(request, 'Lienzo/Horarios/listar_horarios.html', {
        'horarios': horarios,
        'balances': balances,
        'balance': balance,
        'is_admin': is_admin,
        'range_list': range(1, 7),  # Clases (1-6)
        'range_lista': range(1, 6),  # Días (1-5)
    })
#crear

# En la función c_horarios (crear horarios)
@login_required
def c_horarios(request, balance_id):
    balance = get_object_or_404(Balance, id=balance_id)
    
    grupos_sin_horario = Grupo.objects.filter(creador=request.user).exclude(
        id__in=Horario.objects.filter(balance=balance).values_list('grupo_id', flat=True))
    
    turnos_ocupados = Turno.objects.filter(horario__balance=balance).values('local', 'dia', 'clase')
    
    is_admin = request.user.groups.filter(name='Administrador').exists()

    if request.method == 'POST':
        grupos_seleccionados = request.POST.getlist('grupos[]')
        
        if not grupos_seleccionados:
            messages.error(request, "Debe seleccionar al menos un grupo")
            return redirect('Listar_Horarios', balance_id=balance.id)

        errores_por_celda = {}
        tiene_errores = False
        
        datos_formulario = {
            'grupos': {},
            'errores': {}
        }

        for grupo_id in grupos_seleccionados:
            grupo = get_object_or_404(Grupo, id=grupo_id, creador=request.user)
            datos_formulario['grupos'][grupo_id] = {}
            
            for clase in range(1, 7):
                for dia in range(1, 6):
                    local_id = request.POST.get(f'turnos[{grupo_id}][{clase}][{dia}][local]')
                    asignatura_id = request.POST.get(f'turnos[{grupo_id}][{clase}][{dia}][asignatura]')
                    tipo_turno = request.POST.get(f'turnos[{grupo_id}][{clase}][{dia}][tipo]')
                    
                    datos_formulario['grupos'][grupo_id][f'{clase}-{dia}'] = {
                        'asignatura': asignatura_id,
                        'local': local_id,
                        'tipo': tipo_turno
                    }
                    
                    if local_id:
                        local_ocupado = Turno.objects.filter(
                            local_id=local_id,
                            dia=dia,
                            clase=clase,
                            horario__balance=balance
                        ).exists()
                        
                        if local_ocupado:
                            tiene_errores = True
                            local = Local.objects.get(id=local_id)
                            errores_por_celda.setdefault(grupo_id, {}).setdefault(clase, {})[dia] = {
                                'mensaje': f'El local {local} ha sido ocupado recientemente para ese momento',
                                'valores': {
                                    'asignatura': asignatura_id,
                                    'local': local_id,
                                    'tipo': tipo_turno
                                }
                            }

        if tiene_errores:
            context = {
                'grupos': grupos_sin_horario,
                'asignaturas': Asignatura.objects.filter(creador=request.user),
                'locales': Local.objects.all(),
                'balance': balance,
                'range_list': range(1, 6),
                'range_lista': range(1, 7),
                'tipos_turno': Turno.tipos,
                'turnos_ocupados': list(turnos_ocupados),
                'errores_por_celda': errores_por_celda,
                'datos_formulario': datos_formulario
            }
            return render(request, 'Lienzo/Horarios/crear_horarios.html', context)

        for grupo_id in grupos_seleccionados:
            grupo = get_object_or_404(Grupo, id=grupo_id, creador=request.user)
            turnos_validos = 0
            turnos_a_crear = []
            
            for clase in range(1, 7):
                for dia in range(1, 6):
                    asignatura_id = request.POST.get(f'turnos[{grupo_id}][{clase}][{dia}][asignatura]')
                    local_id = request.POST.get(f'turnos[{grupo_id}][{clase}][{dia}][local]')
                    tipo_turno = request.POST.get(f'turnos[{grupo_id}][{clase}][{dia}][tipo]')
                    
                    if all([asignatura_id, local_id, tipo_turno]):
                        if not Asignatura.objects.filter(id=asignatura_id, creador=request.user).exists():
                            continue
                            
                        turnos_a_crear.append({
                            'asignatura_id': asignatura_id,
                            'local_id': local_id,
                            'dia': dia,
                            'clase': clase,
                            'tipo': tipo_turno
                        })
                        turnos_validos += 1

            if turnos_validos > 0:
                horario = Horario.objects.create(
                    grupo=grupo,
                    semana=balance.numero_semana,
                    balance=balance,
                    creador=request.user
                )
                
                Turno.objects.bulk_create([
                    Turno(
                        horario=horario,
                        creador=request.user,
                        **turno_data
                    ) for turno_data in turnos_a_crear
                ])

        messages.success(request, "Horarios creados exitosamente.")
        return redirect('Listar_Horarios', balance_id=balance.id)

    context = {
        'grupos': grupos_sin_horario,
        'asignaturas': Asignatura.objects.filter(creador=request.user),
        'locales': Local.objects.all(),
        'balance': balance,
        'range_list': range(1, 6),
        'range_lista': range(1, 7),
        'tipos_turno': Turno.tipos,
        'turnos_ocupados': list(turnos_ocupados),
        'datos_formulario': {
            'grupos': {}
        }
    }
    return render(request, 'Lienzo/Horarios/crear_horarios.html', context)

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
    
    # Verificar permisos
    is_admin = request.user.groups.filter(name='Administrador').exists()
    if not is_admin and horario.creador != request.user:
        messages.error(request, "No tienes permiso para editar este horario.")
        return redirect('Listar_Horarios', balance_id=horario.balance.id)

    # Obtener datos necesarios
    turnos = Turno.objects.filter(horario=horario)
    semana = horario.balance.numero_semana
    
    # Obtener turnos ocupados (excluyendo los del horario actual)
    turnos_ocupados = Turno.objects.filter(
        horario__balance__numero_semana=semana
    ).exclude(horario=horario).values(
        'local', 'dia', 'clase', 'horario__balance__numero_semana'
    )

    # Obtener recursos según permisos
    if is_admin:
        grupos = Grupo.objects.all()
        asignaturas = Asignatura.objects.all()
        locales = Local.objects.all()
        users = User.objects.all()
    else:
        grupos = Grupo.objects.filter(creador=request.user)
        asignaturas = Asignatura.objects.filter(creador=request.user)
        locales = Local.objects.filter()
        users = []

    if request.method == 'POST':
        errores = {}
        turnos_a_eliminar = set(turnos.values_list('id', flat=True))
        turnos_a_crear = []
        turnos_a_actualizar = []

        for clase in range(1, 7):  # 6 clases
            for dia in range(1, 6):  # 5 días
                celda_key = f'{clase}-{dia}'
                asignatura_id = request.POST.get(f'turnos[{horario.grupo.id}][{clase}][{dia}][asignatura]')
                local_id = request.POST.get(f'turnos[{horario.grupo.id}][{clase}][{dia}][local]')
                tipo_turno = request.POST.get(f'turnos[{horario.grupo.id}][{clase}][{dia}][tipo]')

                # Buscar turno existente
                turno_existente = turnos.filter(clase=clase, dia=dia).first()

                # Si está vacío, marcar para eliminar si existe
                if not all([asignatura_id, local_id, tipo_turno]):
                    if turno_existente:
                        turnos_a_eliminar.add(turno_existente.id)
                    continue

                # Verificar colisión
                local_ocupado = Turno.objects.filter(
                    local_id=local_id,
                    dia=dia,
                    clase=clase,
                    horario__balance__numero_semana=semana
                ).exclude(
                    Q(horario=horario) | Q(horario__grupo=horario.grupo)
                ).exists()

                if local_ocupado:
                    local = get_object_or_404(Local, id=local_id)
                    errores[celda_key] = {
                        'mensaje': f'Local {local} ya ocupado',
                        'valores': {
                            'asignatura': asignatura_id,
                            'tipo': tipo_turno,
                            'local': local_id
                        }
                    }
                    continue

                # Si pasa validación, procesar
                if turno_existente:
                    turno_existente.asignatura_id = asignatura_id
                    turno_existente.local_id = local_id
                    turno_existente.tipo = tipo_turno
                    turnos_a_actualizar.append(turno_existente)
                    turnos_a_eliminar.discard(turno_existente.id)
                else:
                    turnos_a_crear.append(Turno(
                        horario=horario,
                        creador=request.user,
                        asignatura_id=asignatura_id,
                        local_id=local_id,
                        dia=dia,
                        clase=clase,
                        tipo=tipo_turno
                    ))

        if errores:
            context = {
                'horario': horario,
                'turnos': turnos,
                'grupos': grupos,
                'asignaturas': asignaturas,
                'locales': locales,
                'range_list': range(1, 7),
                'range_lista': range(1, 6),
                'tipos_turno': Turno.tipos,
                'is_admin': is_admin,
                'users': users,
                'errores_por_celda': errores,
                'turnos_ocupados': list(turnos_ocupados),
                'datos_formulario': request.POST
            }
            return render(request, 'Lienzo/Horarios/editar_horarios.html', context)

        # Si no hay errores, guardar cambios
        Turno.objects.filter(id__in=turnos_a_eliminar).delete()
        for turno in turnos_a_actualizar:
            turno.save()
        Turno.objects.bulk_create(turnos_a_crear)

        if is_admin:
            creador_id = request.POST.get('creador')
            if creador_id:
                horario.creador = User.objects.get(id=creador_id)
        horario.save()

        messages.success(request, "Horario actualizado exitosamente.")
        return redirect('Listar_Horarios', balance_id=horario.balance.id)

    context = {
        'horario': horario,
        'turnos': turnos,
        'grupos': grupos,
        'asignaturas': asignaturas,
        'locales': locales,
        'range_list': range(1, 7),
        'range_lista': range(1, 6),
        'tipos_turno': Turno.tipos,
        'is_admin': is_admin,
        'users': users,
        'turnos_ocupados': list(turnos_ocupados)
    }
    return render(request, 'Lienzo/Horarios/editar_horarios.html', context)

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
    # Todos los usuarios ven los mismos balances
    balances = Balance.objects.all()
    is_admin = request.user.groups.filter(name='Administrador').exists()
    
    return render(request, 'Base/listar_semanas.html', {
        'balances': balances,
        'is_admin': is_admin
    })


# para no volver a cerrar sesion
@login_required
def vista_previa(request):
    horarios_publicados = Horario.objects.filter(
        publicado=True
    ).select_related('grupo', 'balance').prefetch_related(
        Prefetch('turnos', queryset=Turno.objects.select_related('asignatura', 'local')),
        'profesores'  # Añadir prefetch para profesores
    )
    
    range_list = range(1, 7)
    range_lista = range(1, 6)

    return render(request, 'Lienzo/Horarios/vista_previa.html', {
        'horarios_publicados': horarios_publicados,
        'range_list': range_list,
        'range_lista': range_lista,
        'is_admin': request.user.groups.filter(name='Administrador').exists(),
    })

#ponerle los profes a los horarios
@login_required
def asignar_profesores(request, horario_id):
    horario = get_object_or_404(Horario, id=horario_id)
    
    # Verificar permisos
    is_admin = request.user.groups.filter(name='Administrador').exists()
    if not is_admin and horario.creador != request.user:
        messages.error(request, "No tienes permiso para asignar profesores a este horario.")
        return redirect('Listar_Horarios', balance_id=horario.balance.id)

    # Obtener profesores del grupo del horario
    profesores = Profesor.objects.filter(
        grupos_ids__contains=str(horario.grupo.id),
        asignatura__in=horario.turnos.values_list('asignatura', flat=True).distinct()
    )
    
    if not is_admin:
        profesores = profesores.filter(creador=request.user)

    if request.method == 'POST':
        profesores_seleccionados = request.POST.getlist('profesores')
        
        # Actualizar la relación muchos-a-muchos
        horario.profesores.clear()
        for profesor_id in profesores_seleccionados:
            profesor = get_object_or_404(Profesor, id=profesor_id)
            horario.profesores.add(profesor)
        
        messages.success(request, "Profesores asignados exitosamente.")
        return redirect('Listar_Horarios', balance_id=horario.balance.id)

    # Obtener IDs de profesores ya asignados
    profesores_seleccionados_ids = horario.get_profesores_seleccionados()

    context = {
        'horario': horario,
        'profesores': profesores,
        'profesores_seleccionados_ids': profesores_seleccionados_ids,
        'range_list': range(1, 7),
        'range_lista': range(1, 6),
        'turnos_por_dia_clase': obtener_turnos_por_dia_clase(horario)
    }
    return render(request, 'Lienzo/Horarios/asignar_profesores.html', context)

def obtener_turnos_por_dia_clase(horario):
    turnos_por_dia_clase = {}
    for turno in horario.turnos.all():
        clave = f"{turno.dia}-{turno.clase}"
        if clave not in turnos_por_dia_clase:
            turnos_por_dia_clase[clave] = []
        turnos_por_dia_clase[clave].append(turno)
    return turnos_por_dia_clase