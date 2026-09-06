"""
3DimensiaPT - Sistema de Llaveros NFC de Emergencia
Archivo: emergencias/admin.py
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import LlaveroNFC


@admin.register(LlaveroNFC)
class LlaveroNFCAdmin(admin.ModelAdmin):
    list_display = [
        'nombre_completo',
        'padre',
        'telefono_contacto_1',
        'grupo_sanguineo',
        'contador_escaneos',
        'esta_activo',
        'enlace_nfc_publico',
        'fecha_creacion'
    ]
    list_filter = ['esta_activo', 'grupo_sanguineo', 'fecha_creacion']
    search_fields = ['id', 'nombre_menor', 'apellidos_menor', 'padre__username', 'telefono_contacto_1']
    readonly_fields = ['id', 'contador_escaneos', 'ultimo_escaneo', 'fecha_creacion', 'fecha_actualizacion']

    def nombre_completo(self, obj):
        return f"{obj.nombre_menor} {obj.apellidos_menor}"
    nombre_completo.short_description = "Menor"

    def enlace_nfc_publico(self, obj):
        url = obj.get_absolute_url()
        return format_html('<a href="{}" target="_blank" style="color: #e11d48; font-weight: bold;">🔗 Ver Ficha NFC</a>', url)
    enlace_nfc_publico.short_description = "URL Pública"
