"""
3DimensiaPT - Sistema de Llaveros NFC de Emergencia
Archivo: emergencias/urls.py
"""
from django.urls import path
from . import views

urlpatterns = [
    # 1. VISTA PÚBLICA ESCANEADA POR NFC (Sin login)
    path('nfc/<uuid:uuid>/', views.ficha_publica_view, name='ficha_publica'),

    # 2. VISTA PRIVADA DE EDICIÓN PARA PADRES (@login_required)
    path('nfc/<uuid:uuid>/editar/', views.editar_ficha_view, name='editar_ficha'),
]
