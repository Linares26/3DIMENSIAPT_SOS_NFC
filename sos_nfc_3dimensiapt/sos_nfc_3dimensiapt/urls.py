"""
3DimensiaPT - Enrutador Principal de URLs
Archivo: sos_nfc_3dimensiapt/urls.py
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),

    # Redirección de la raíz al panel de llaveros (o login si no está autenticado)
    path('', RedirectView.as_view(pattern_name='mis_llaveros', permanent=False), name='inicio'),

    # Rutas de autenticación y panel de padres
    path('', include('cuentas.urls')),

    # Rutas públicas y de edición de fichas NFC
    path('', include('emergencias.urls')),
]

# Servir archivos estáticos y multimedia en entorno de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
