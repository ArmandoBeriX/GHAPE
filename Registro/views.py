from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib import messages
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from django.views.decorators.http import require_http_methods
# Create your views here.



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo usuario
            return redirect('Login')  # Redirige a la página de inicio de sesión o a donde desees
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/agregar.html', {'form': form})








@require_http_methods(["GET", "POST"])  # Asegura que solo acepte GET/POST
@never_cache  # Evita almacenamiento en caché (seguridad para login)
def login(request):
    # Redirige si ya está autenticado
    if request.user.is_authenticated:
        return redirect('Selector')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Validación básica de campos
        if not username or not password:
            messages.error(request, "⚠️ Complete todos los campos.")
            return render(request, 'registration/login.html', {'username': username})
        
        # Autenticación del usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Verificar si el usuario pertenece a los grupos permitidos
            allowed_groups = ['Administrador', 'Profesor de Año']
            user_groups = user.groups.values_list('name', flat=True)
            
            if any(group in user_groups for group in allowed_groups):
                auth_login(request, user)
                messages.success(request, f"¡Bienvenido, {user.username}!")
                
                
                next_url = request.GET.get('next')
                return redirect(next_url if next_url else 'Selector')
            else:
                messages.error(request, "⛔ No tienes permisos para acceder al sistema.")
                return render(request, 'registration/login.html', {'username': username})
        else:
            messages.error(request, "🔐 Usuario o contraseña incorrectos.")
            return render(request, 'registration/login.html', {'username': username})
    
    return render(request, 'registration/login.html')

def exit(request):
    logout(request)
    request.session.flush()
    return redirect('Principal')