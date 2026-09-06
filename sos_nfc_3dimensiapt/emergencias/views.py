"""
3DimensiaPT - Sistema de Llaveros NFC de Emergencia
Archivo: emergencias/views.py
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.utils import timezone
from django.db.models import F
from .models import LlaveroNFC
from .forms import FichaEmergenciaForm


def ficha_publica_view(request, uuid):
    """
    VISTA PÚBLICA (Accedida al escanear el chip NFC con un móvil).
    URL: https://3dimensiapt.com/nfc/<uuid>/
    
    - No requiere login.
    - Consulta por UUID v4.
    - Incrementa el contador de escaneos y fecha.
    - Renderiza la plantilla optimizada para urgencias con botones 'tel:'.
    """
    # 1. Recuperar el llavero o devolver 404
    llavero = get_object_or_404(LlaveroNFC, id=uuid)

    # 2. Si el llavero está desactivado por el padre (ej. pérdida/robo)
    if not llavero.esta_activo:
        return render(
            request, 
            'emergencias/ficha_inactiva.html', 
            {'llavero': llavero},
            status=403
        )

    # 3. Registrar métrica de escaneo atómicamente
    try:
        LlaveroNFC.objects.filter(id=uuid).update(
            contador_escaneos=F('contador_escaneos') + 1,
            ultimo_escaneo=timezone.now()
        )
    except Exception:
        pass

    # 4. Contexto para la vista pública
    context = {
        'llavero': llavero,
        'es_propietario': request.user.is_authenticated and request.user == llavero.padre,
    }
    
    return render(request, 'emergencias/ficha_publica.html', context)


@login_required
def editar_ficha_view(request, uuid):
    """
    VISTA PRIVADA DE EDICIÓN (Solo para el padre/madre propietario).
    URL: https://3dimensiapt.com/nfc/<uuid>/editar/
    
    Seguridad:
    - Valida que request.user == llavero.padre.
    - Si no coincide -> Lanza PermissionDenied (HTTP 403).
    - Maneja subida de fotos (request.FILES).
    """
    llavero = get_object_or_404(LlaveroNFC, id=uuid)

    # Validación de propiedad estricta
    if llavero.padre != request.user:
        raise PermissionDenied("No tienes autorización para modificar este llavero de emergencia.")

    if request.method == 'POST':
        form = FichaEmergenciaForm(request.POST, request.FILES, instance=llavero)
        if form.is_valid():
            form.save()
            messages.success(
                request, 
                f"✅ La ficha de emergencia de {llavero.nombre_menor} ha sido actualizada con éxito."
            )
            return redirect('ficha_publica', uuid=llavero.id)
        else:
            messages.error(
                request, 
                "⚠️ Por favor, corrige los errores del formulario."
            )
    else:
        form = FichaEmergenciaForm(instance=llavero)

    context = {
        'form': form,
        'llavero': llavero,
    }
    
    return render(request, 'emergencias/editar_ficha.html', context)
