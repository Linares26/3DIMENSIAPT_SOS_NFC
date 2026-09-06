"""
WSGI config for sos_nfc_3dimensiapt project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Configurar rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sos_nfc_3dimensiapt.settings')

application = get_wsgi_application()

# --- MIGRACIONES Y SUPERUSUARIO SEGURO ---
SECRET_PASS = os.environ.get('SECRET_PASS')

if SECRET_PASS:
    try:
        from django.core.management import call_command
        from django.contrib.auth import get_user_model

        call_command('migrate', interactive=False)

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username='3dimensiapt_admin',
            defaults={'email': '3dimensiapt@gmail.com', 'is_staff': True, 'is_superuser': True}
        )
        # Sincroniza la clave con la variable de Vercel sin guardarla en código
        user.set_password(SECRET_PASS)
        user.save()
    except Exception as e:
        print(f"Error en autoconfiguración de BD: {e}")

app = application
