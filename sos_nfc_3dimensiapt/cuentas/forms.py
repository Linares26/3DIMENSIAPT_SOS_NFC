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
        label="Nome",
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none focus:ring-2 focus:ring-rose-500/20 text-sm font-semibold',
            'placeholder': 'Ej. José'
        })
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True,
        label="Apelidos",
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none focus:ring-2 focus:ring-rose-500/20 text-sm font-semibold',
            'placeholder': 'Ej. Pereira Silva'
        })
    )
    email = forms.EmailField(
        required=True,
        label="Endereço de e-mail (para recuperação e alertas)",
        widget=forms.EmailInput(attrs={
            'class': 'w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none focus:ring-2 focus:ring-rose-500/20 text-sm',
            'placeholder': 'jose@ejemplo.com'
        })
    )
    terminos_privacidad = forms.BooleanField(
        required=True,
        label="Aceito os termos relativos à conservação de dados médicos de emergência ao abrigo do RGPD/COPPA",
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
                'placeholder': 'jose_pai'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clases de Tailwind CSS a los campos de contraseña heredados
        for fieldname in ['password1', 'password2']:
            if fieldname in self.fields:
                self.fields[fieldname].widget.attrs.update({
                    'class': 'w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none focus:ring-2 focus:ring-rose-500/20 text-sm font-mono',
                    'placeholder': 'Mínimo de 8 caracteres'
                })

    def clean_email(self):
        email = self.cleaned_data.get('email').strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Já existe uma conta registada com este endereço de e-mail.")
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
            'placeholder': 'jose_pai ou o teu email'
        })
    )
    password = forms.CharField(
        label="Palavra-passe",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none focus:ring-2 focus:ring-rose-500/20 text-sm font-mono',
            'placeholder': '••••••••'
        })
    )


class SolicitarRecuperacionPasswordForm(PasswordResetForm):
    """Formulario para solicitar enlace de recuperación de contraseña por email"""
    email = forms.EmailField(
        label="Endereço de e-mail",
        widget=forms.EmailInput(attrs={
            'class': 'w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none focus:ring-2 focus:ring-rose-500/20 text-sm',
            'placeholder': 'exemplo@correo.com'
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
                    'placeholder': 'Nova palavra-passe segura'
                })
