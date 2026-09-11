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
    Modelo representativo de cada porta-chaves físico 3D com chip NFC integrado.
    Utiliza UUID v4 para gerar URLs não sequenciais e invulneráveis a escaneos por força bruta.
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
        DESCONOCIDO = 'DESC', 'Desconhecido / Não especificado'

    # 1. IDENTIFICADOR CRIPTOGRÁFICO ÚNICO (Para la URL del NFC)
    # Ejemplo: https://3dimensiapt.com/nfc/550e8400-e29b-41d4-a716-446655440000/
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text="Identificador único e não previsível gravado na memória do chip NFC."
    )

    # 2. PROPIETARIO / TUTOR LEGAL (Usuario estándar de Django)
    padre = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='llaveros_nfc',
        verbose_name="Pai/Mãe ou Tutor",
        help_text="Usuário registrado com permissões exclusivas de edição para esta ficha."
    )

    # 3. DATOS BÁSICOS DEL MENOR
    nombre_menor = models.CharField(
        max_length=60,
        verbose_name="Nome do Menino/a",
        help_text="Ex: Tiago"
    )
    apellidos_menor = models.CharField(
        max_length=100,
        verbose_name="Apellidos do Menino/a",
        help_text="Ex: Pereira Silva"
    )
    fecha_nacimiento = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data de nascimento"
    )
    foto = models.ImageField(
        upload_to='llaveros/avatares/',
        null=True,
        blank=True,
        verbose_name="Foto do Menino/a para identificação",
        help_text="Foto clara do rosto para identificação rápida em caso de perda."
    )

    # 4. CONTACTOS DE EMERGÊNCIA (Con validación de formato telefónico)
    validador_telefono = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="O número de telefone deve ter um formato internacional válido (por exemplo: +351912345678 ou 912345678)."
    )

    nombre_contacto_1 = models.CharField(
        max_length=80,
        verbose_name="Nome do Contato de Emergência",
        help_text="Ex: Mãe (Laura Pereira)"
    )
    parentesco_contacto_1 = models.CharField(
        max_length=40,
        default="Mãe",
        verbose_name="Parentesco do Contato 1"
    )
    telefono_contacto_1 = models.CharField(
        validators=[validador_telefono],
        max_length=20,
        verbose_name="Telefone de Emergência",
        help_text="Número ao qual o botão de emergência principal ligará."
    )

    nombre_contacto_2 = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        verbose_name="Nome do Contato de Emergência 2",
        help_text="Ex: Pai (Carlos Pereira) ou Avós"
    )
    parentesco_contacto_2 = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        verbose_name="Parentesco do Contato 2"
    )
    telefono_contacto_2 = models.CharField(
        validators=[validador_telefono],
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Telefone de Emergência 2"
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
        help_text="Alergias a alimentos, medicamentos e picadas (por exemplo: amendoins, penicilina, látex)."
    )
    enfermedades_condiciones = models.TextField(
        blank=True,
        verbose_name="Condições Médicas",
        help_text="Ex: Asma, Diabetes Tipo 1, Epilepsia, Autismo / TEA (não verbal)."
    )
    medicacion_urgencia = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Medicação de Urgência / Localização",
        help_text="Ex.: Leva o autoinjetor de adrenalina (Epipen) no bolso lateral da mochila."
    )
    observaciones_medicas = models.TextField(
        blank=True,
        verbose_name="Instruções Adicionais",
        help_text="Qualquer indicação crucial para os socorristas ou quem encontrar a criança."
    )

    # 6. METADATOS TÉCNICOS Y HARDWARE IOT
    codigo_chip_fisico = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="UID do Chip NFC Físico",
        help_text="Identificador de fábrica do chip NTAG213/215/216 (opcional para controle de estoque)."
    )
    esta_activo = models.BooleanField(
        default=True,
        verbose_name="Porta-chaves Ativo",
        help_text="Se desativar, a ficha pública mostrará um aviso de porta-chaves desabilitado."
    )
    contador_escaneos = models.PositiveIntegerField(
        default=0,
        verbose_name="Total de Escaneamentos NFC"
    )
    ultimo_escaneo = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Último Escaneamento Registrado"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Porta-chaves NFC"
        verbose_name_plural = "Porta-chaves NFC"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Porta-chaves de {self.nombre_menor} {self.apellidos_menor} (UUID: {str(self.id)[:8]}...)"

    def get_absolute_url(self):
        """Devolve a URL pública que está fisicamente gravada no chip NFC"""
        return reverse('ficha_publica', kwargs={'uuid': self.id})

    def get_edit_url(self):
        """Devolve a URL de edição protegida para os pais"""
        return reverse('editar_ficha', kwargs={'uuid': self.id})
