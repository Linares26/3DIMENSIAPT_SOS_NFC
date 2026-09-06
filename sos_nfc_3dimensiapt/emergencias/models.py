"""
3DimensiaPT - Sistema de Llaveros NFC de Emergencia
Archivo: emergencias/models.py
"""
import uuid
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import RegexValidator


class LlaveroNFC(models.Model):
    """
    Modelo representativo de cada llavero físico 3D con chip NFC integrado.
    Utiliza UUID v4 para generar URLs no secuenciales e invulnerables a escaneo por fuerza bruta.
    """
    
    # Opciones de grupo sanguíneo
    class GrupoSanguineo(models.TextChoices):
        A_POSITIVO = 'A+', 'A Positivo (A+)'
        A_NEGATIVO = 'A-', 'A Negativo (A-)'
        B_POSITIVO = 'B+', 'B Positivo (B+)'
        B_NEGATIVO = 'B-', 'B Negativo (B-)'
        AB_POSITIVO = 'AB+', 'AB Positivo (AB+)'
        AB_NEGATIVO = 'AB-', 'AB Negativo (AB-)'
        O_POSITIVO = 'O+', 'O Positivo (O+)'
        O_NEGATIVO = 'O-', 'O Negativo (O-)'
        DESCONOCIDO = 'DESC', 'Desconocido / No especificado'

    # 1. IDENTIFICADOR CRIPTOGRÁFICO ÚNICO (Para la URL del NFC)
    # Ejemplo: https://3dimensiapt.com/nfc/550e8400-e29b-41d4-a716-446655440000/
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text="Identificador único no predecible grabado en la memoria del chip NFC."
    )

    # 2. PROPIETARIO / TUTOR LEGAL (Usuario estándar de Django)
    padre = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='llaveros_nfc',
        verbose_name="Padre/Madre o Tutor",
        help_text="Usuario registrado con permisos exclusivos de edición para esta ficha."
    )

    # 3. DATOS BÁSICOS DEL MENOR
    nombre_menor = models.CharField(
        max_length=60,
        verbose_name="Nombre del niño/a",
        help_text="Ej: Lucas"
    )
    apellidos_menor = models.CharField(
        max_length=100,
        verbose_name="Apellidos del niño/a",
        help_text="Ej: Martínez Gómez"
    )
    fecha_nacimiento = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de Nacimiento"
    )
    foto = models.ImageField(
        upload_to='llaveros/avatares/',
        null=True,
        blank=True,
        verbose_name="Foto / Avatar reciente",
        help_text="Foto clara del rostro para identificación rápida en caso de pérdida."
    )

    # 4. CONTACTOS DE EMERGENCIA (Con validación de formato telefónico)
    validador_telefono = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El teléfono debe tener formato internacional válido (ej: +34612345678 o 612345678)."
    )

    nombre_contacto_1 = models.CharField(
        max_length=80,
        verbose_name="Nombre Contacto Principal",
        help_text="Ej: Mamá (Laura Gómez)"
    )
    parentesco_contacto_1 = models.CharField(
        max_length=40,
        default="Madre",
        verbose_name="Parentesco Contacto 1"
    )
    telefono_contacto_1 = models.CharField(
        validators=[validador_telefono],
        max_length=20,
        verbose_name="Teléfono SOS Principal",
        help_text="Número al que llamará el botón principal de emergencia."
    )

    nombre_contacto_2 = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        verbose_name="Nombre Contacto Secundario",
        help_text="Ej: Papá (Carlos Martínez) o Abuelos"
    )
    parentesco_contacto_2 = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        verbose_name="Parentesco Contacto 2"
    )
    telefono_contacto_2 = models.CharField(
        validators=[validador_telefono],
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Teléfono SOS Secundario"
    )

    # 5. INFORMACIÓN MÉDICA CRÍTICA PARA URGENCIAS
    grupo_sanguineo = models.CharField(
        max_length=5,
        choices=GrupoSanguineo.choices,
        default=GrupoSanguineo.DESCONOCIDO,
        verbose_name="Grupo Sanguíneo"
    )
    alergias_graves = models.TextField(
        blank=True,
        verbose_name="Alergias Críticas",
        help_text="Alergias a alimentos, medicamentos, picaduras (ej: Cacahuetes, Penicilina, Látex)."
    )
    enfermedades_condiciones = models.TextField(
        blank=True,
        verbose_name="Condiciones Médicas",
        help_text="Ej: Asma, Diabetes Tipo 1, Epilepsia, Autismo / TEA (no verbal)."
    )
    medicacion_urgencia = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Medicación de Urgencia / Ubicación",
        help_text="Ej: Lleva Autoinyector de Adrenalina (Epipen) en el bolsillo lateral de la mochila."
    )
    observaciones_medicas = models.TextField(
        blank=True,
        verbose_name="Instrucciones Adicionales",
        help_text="Cualquier indicación crucial para los sanitarios o quien encuentre al menor."
    )

    # 6. METADATOS TÉCNICOS Y HARDWARE IOT
    codigo_chip_fisico = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="UID del Chip NFC Físico",
        help_text="Identificador de fábrica del chip NTAG213/215/216 (opcional para control de stock)."
    )
    esta_activo = models.BooleanField(
        default=True,
        verbose_name="Llavero Activo",
        help_text="Si se desactiva, la ficha pública mostrará un aviso de llavero inhabilitado."
    )
    contador_escaneos = models.PositiveIntegerField(
        default=0,
        verbose_name="Total de Escaneos NFC"
    )
    ultimo_escaneo = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Último Escaneo Registrado"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Llavero NFC"
        verbose_name_plural = "Llaveros NFC"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Llavero de {self.nombre_menor} {self.apellidos_menor} (UUID: {str(self.id)[:8]}...)"

    def get_absolute_url(self):
        """Retorna la URL pública que se graba físicamente en el chip NFC"""
        return reverse('ficha_publica', kwargs={'uuid': self.id})

    def get_edit_url(self):
        """Retorna la URL de edición protegida para los padres"""
        return reverse('editar_ficha', kwargs={'uuid': self.id})
