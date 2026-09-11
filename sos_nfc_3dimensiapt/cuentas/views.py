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
                f"Bem-vindo/a {user.first_name}! A sua conta de tutor foi criada com sucesso."
            )
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('mis_llaveros')
        else:
            messages.error(request, "Por favor, reveja os erros no formulário.")
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
            messages.success(request, f"Sessão iniciada como {user.get_full_name() or user.username}.")
            
            # Redirección inteligente al parámetro 'next' si existe
            redirect_to = request.POST.get('next') or request.GET.get('next') or 'mis_llaveros'
            return redirect(redirect_to)
        else:
            messages.error(request, "Usuario ou senha incorretos.")
    else:
        form = LoginFormPersonalizado()

    return render(request, 'cuentas/login.html', {'form': form, 'next': next_url})


def logout_padre_view(request):
    """Encerra a sessão do pai e redireciona com mensagem de boas-vindas"""
    logout(request)
    messages.info(request, "Sessão encerrada de forma segura.")
    return redirect('login')


@login_required
def mis_llaveros_view(request):
    """
    PAINEL PRIVADO DE PAIS:
    Mostra a lista de todos os porta-chaves pertencentes ao pai logado,
    seus estados (ativo/inativo), total de leituras NFC e acessos diretos a edição.
    """
    llaveros = LlaveroNFC.objects.filter(padre=request.user).order_by('-fecha_creacion')
    
    context = {
        'llaveros': llaveros,
        'total_escaneos': sum(l.contador_escaneos for l in llaveros),
    }
    return render(request, 'cuentas/mis_llaveros.html', context)
