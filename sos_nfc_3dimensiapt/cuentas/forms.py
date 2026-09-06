"""
3DimensiaPT - App de Cuentas y Autenticación de Padres
Archivo: cuentas/forms.py
"""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm, 
    AuthenticationForm, 
    PasswordResetForm, 
    SetPasswordForm,
    PasswordChangeForm
)

User = get_user_model()


class RegistroPadreForm(UserCreationForm):
    """
    Formulario de registro para nuevos padres/tutores.
    Exige correo electrónico único para recuperación de contraseñas y avisos SOS.
    """
    first_name = forms.CharField(
        max_length=30, 
        required=True,
        label="Nombre",
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none focus:ring-2 focus:ring-rose-500/20 text-sm font-semibold',
            'placeholder': 'Ej. Carlos'
        })
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True,
        label="Apellidos",
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none focus:ring-2 focus:ring-rose-500/20 text-sm font-semibold',
            'placeholder': 'Ej. Martínez'
        })
    )
    email = forms.EmailField(
        required=True,
        label="Correo Electrónico (para recuperación y alertas)",
        widget=forms.EmailInput(attrs={
            'class': 'w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none focus:ring-2 focus:ring-rose-500/20 text-sm',
            'placeholder': 'carlos@ejemplo.com'
        })
    )
    terminos_privacidad = forms.BooleanField(
        required=True,
        label="Acepto los términos de custodia de datos médicos de emergencia RGPD/COPPA",
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 rounded border-slate-300 text-rose-600 focus:ring-rose-500 cursor-pointer'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none focus:ring-2 focus:ring-rose-500/20 text-sm font-semibold',
                'placeholder': 'carlos_padre'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clases de Tailwind CSS a los campos de contraseña heredados
        for fieldname in ['password1', 'password2']:
            if fieldname in self.fields:
                self.fields[fieldname].widget.attrs.update({
                    'class': 'w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none focus:ring-2 focus:ring-rose-500/20 text-sm font-mono',
                    'placeholder': 'Mínimo 8 caracteres'
                })

    def clean_email(self):
        email = self.cleaned_data.get('email').strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe una cuenta registrada con este correo electrónico.")
        return email


class LoginFormPersonalizado(AuthenticationForm):
    """
    Formulario de Login estilizado con Tailwind CSS.
    Permite autenticación por nombre de usuario o email.
    """
    username = forms.CharField(
        label="Usuario o Email",
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none focus:ring-2 focus:ring-rose-500/20 text-sm font-semibold',
            'placeholder': 'carlos_padre o tu@correo.com'
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none focus:ring-2 focus:ring-rose-500/20 text-sm font-mono',
            'placeholder': '••••••••'
        })
    )


class SolicitarRecuperacionPasswordForm(PasswordResetForm):
    """Formulario para solicitar enlace de recuperación de contraseña por email"""
    email = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none focus:ring-2 focus:ring-rose-500/20 text-sm',
            'placeholder': 'ejemplo@correo.com'
        })
    )


class NuevaPasswordForm(SetPasswordForm):
    """Formulario cuando el padre hace clic en el enlace con token seguro"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['new_password1', 'new_password2']:
            if fieldname in self.fields:
                self.fields[fieldname].widget.attrs.update({
                    'class': 'w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none focus:ring-2 focus:ring-rose-500/20 text-sm font-mono',
                    'placeholder': 'Nueva contraseña segura'
                })
