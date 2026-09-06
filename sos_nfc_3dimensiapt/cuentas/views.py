"""
3DimensiaPT - App de Cuentas y Autenticación de Padres
Archivo: cuentas/views.py
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from emergencias.models import LlaveroNFC
from .forms import RegistroPadreForm, LoginFormPersonalizado


def registro_padre_view(request):
    """
    VISTA DE REGISTRO DE PADRES/TUTORES.
    - Crea el usuario en auth_user.
    - Inicia sesión automáticamente (auto-login).
    - Redirige al panel familiar de 'mis_llaveros' o a la URL '?next='.
    """
    if request.user.is_authenticated:
        return redirect('mis_llaveros')

    if request.method == 'POST':
        form = RegistroPadreForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Iniciar sesión automáticamente
            login(request, user)
            messages.success(
                request,
                f"¡Bienvenido/a {user.first_name}! Tu cuenta de tutor ha sido creada con éxito."
            )
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('mis_llaveros')
        else:
            messages.error(request, "Por favor revisa los errores en el formulario.")
    else:
        form = RegistroPadreForm()

    return render(request, 'cuentas/registro.html', {'form': form})


def login_padre_view(request):
    """
    VISTA DE INICIO DE SESIÓN CON SOPORTE PARA '?next='.
    Si un padre escanea el llavero y pulsa 'Editar', la URL contiene '?next=/nfc/<uuid>/editar/'.
    Al autenticarse, vuelve inmediatamente a la ficha de su hijo.
    """
    if request.user.is_authenticated:
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('mis_llaveros')

    next_url = request.GET.get('next', '')

    if request.method == 'POST':
        form = LoginFormPersonalizado(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Sesión iniciada como {user.get_full_name() or user.username}.")
            
            # Redirección inteligente al parámetro 'next' si existe
            redirect_to = request.POST.get('next') or request.GET.get('next') or 'mis_llaveros'
            return redirect(redirect_to)
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = LoginFormPersonalizado()

    return render(request, 'cuentas/login.html', {'form': form, 'next': next_url})


def logout_padre_view(request):
    """Cierra la sesión del padre y redirige con mensaje amistoso"""
    logout(request)
    messages.info(request, "Has cerrado sesión de forma segura.")
    return redirect('login')


@login_required
def mis_llaveros_view(request):
    """
    PANEL PRIVADO DE PADRES:
    Muestra la lista de todos los llaveros pertenecientes al padre logueado,
    sus estados (activo/inactivo), total de lecturas NFC y accesos directos a edición.
    """
    llaveros = LlaveroNFC.objects.filter(padre=request.user).order_by('-fecha_creacion')
    
    context = {
        'llaveros': llaveros,
        'total_escaneos': sum(l.contador_escaneos for l in llaveros),
    }
    return render(request, 'cuentas/mis_llaveros.html', context)
