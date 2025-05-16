from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.cache import cache_page
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from Editor.models import *
# Create your views here.


def principalView(request):
    # Obtener todos los horarios publicados de todos los usuarios
    horarios_publicados = Horario.objects.filter(publicado=True)

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

