"""
WSGI config for sos_nfc_3dimensiapt project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Agregar la carpeta del proyecto Django al path de Python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sos_nfc_3dimensiapt.settings')

application = get_wsgi_application()

# Punto de entrada para Vercel
app = application
