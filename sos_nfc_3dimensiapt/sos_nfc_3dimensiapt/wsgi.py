"""
WSGI config for sos_nfc_3dimensiapt project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Configurar la ruta raíz del proyecto para que Python reconozca los módulos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Indicar el archivo de configuración settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sos_nfc_3dimensiapt.settings')

# Inicializar la aplicación WSGI
application = get_wsgi_application()

# Variable requerida por el runtime de Vercel
app = application
