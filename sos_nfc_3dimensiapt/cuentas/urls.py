"""
3DimensiaPT - App de Cuentas y Autenticación de Padres
Archivo: cuentas/urls.py
"""
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from .forms import SolicitarRecuperacionPasswordForm, NuevaPasswordForm

urlpatterns = [
    # 1. REGISTRO, LOGIN Y LOGOUT
    path('registro/', views.registro_padre_view, name='registro'),
    path('login/', views.login_padre_view, name='login'),
    path('logout/', views.logout_padre_view, name='logout'),

    # 2. PANEL DE CONTROL DE PADRES
    path('mis-llaveros/', views.mis_llaveros_view, name='mis_llaveros'),

    # 3. FLUJO COMPLETO DE RECUPERACIÓN DE CONTRASEÑA POR EMAIL (Django Built-in Views)
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='cuentas/password_reset.html',
            email_template_name='cuentas/emails/password_reset_email.html',
            subject_template_name='cuentas/emails/password_reset_subject.txt',
            form_class=SolicitarRecuperacionPasswordForm,
            success_url=reverse_lazy('password_reset_done')
        ),
        name='password_reset'
    ),
    path(
        'password-reset/enviado/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='cuentas/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='cuentas/password_reset_confirm.html',
            form_class=NuevaPasswordForm,
            success_url=reverse_lazy('password_reset_complete')
        ),
        name='password_reset_confirm'
    ),
    path(
        'password-reset/completado/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='cuentas/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    # 4. CAMBIO DE CONTRASEÑA
    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(
            template_name='cuentas/password_change.html',
            success_url=reverse_lazy('mis_llaveros')
        ),
        name='password_change'
    ),
]
