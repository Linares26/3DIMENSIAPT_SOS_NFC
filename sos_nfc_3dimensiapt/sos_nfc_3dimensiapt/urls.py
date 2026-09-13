"""
3DimensiaPT - Enrutador Principal de URLs
Archivo: sos_nfc_3dimensiapt/urls.py
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')), # Sin prefijo de idioma
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='mis_llaveros', permanent=False), name='inicio'),
    path('', include('cuentas.urls')),
    path('', include('emergencias.urls')),
    prefix_default_language=True,
)

# Servir archivos estáticos y multimedia en entorno de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
