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
SECRET_PASS = os.environ.get('SECRET_PASS')
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sos_nfc_3dimensiapt.settings')

application = get_wsgi_application()

# --- MIGRACIONES Y SUPERUSUARIO AUTO-EJECUTABLES ---
try:
    from django.core.management import call_command
    from django.contrib.auth import get_user_model

    # Ejecutar migraciones en /tmp/db.sqlite3
    call_command('migrate', interactive=False)

    # Crear superusuario automáticamente si no existe
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('3dimensiapt_admin', '3dimensiapt@gmail.com', SECRET_PASS)
except Exception as e:
    print(f"Error en autoconfiguración de BD: {e}")

app = application
