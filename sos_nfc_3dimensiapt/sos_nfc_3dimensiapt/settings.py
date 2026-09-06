"""
3DimensiaPT - Configuración Django
Archivo: sos_nfc_3dimensiapt/settings.py
"""
import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-3dimensiapt-nfc-key')
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['.vercel.app', '.3dimensiapt.com', '3dimensiapt.com', 'localhost', '127.0.0.1']

# APPS INSTALADAS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps del Proyecto 3DimensiaPT
    'emergencias.apps.EmergenciasConfig',
    'cuentas.apps.CuentasConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'sos_nfc_3dimensiapt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sos_nfc_3dimensiapt.wsgi.application'

# ==========================================
# BASE DE DATOS
# ==========================================
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ==========================================
# ARCHIVOS ESTÁTICOS Y MULTIMEDIA (FOTOS)
# ==========================================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- ALMACENAMIENTO DE ARCHIVOS MEDIA (SUPABASE STORAGE) ---
AWS_ACCESS_KEY_ID = os.environ.get('SUPABASE_S3_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('SUPABASE_S3_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = 'media'
AWS_S3_ENDPOINT_URL = os.environ.get('SUPABASE_S3_ENDPOINT')
AWS_S3_REGION_NAME = 'us-east-1'  # Región genérica requerida por boto3
AWS_S3_FILE_OVERWRITE = False

if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
else:
    # Configuración local de respaldo
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==========================================
# CONFIGURACIÓN DE AUTENTICACIÓN Y REDIRECCIONES
# ==========================================
LOGIN_URL = 'login'                           # URL a la que envía @login_required
LOGIN_REDIRECT_URL = 'mis_llaveros'           # Redirección por defecto tras login
LOGOUT_REDIRECT_URL = 'login'                 # Redirección tras cerrar sesión

# VALIDADORES DE CONTRASEÑA ESTRICTOS
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==========================================
# CONFIGURACIÓN DE CORREO ELECTRÓNICO (RECUPERACIÓN DE CLAVES)
# ==========================================
# En desarrollo: imprime en consola. En producción: configurar SMTP (SendGrid, Mailgun, Amazon SES).
EMAIL_BACKEND = os.environ.get(
    'DJANGO_EMAIL_BACKEND', 
    'django.core.mail.backends.console.EmailBackend'
)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.sendgrid.net')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = '3DimensiaPT SOS <soporte@3dimensiapt.com>'

# TIEMPO DE EXPIRACIÓN DEL TOKEN DE RECUPERACIÓN (1 día = 86400 seg)
PASSWORD_RESET_TIMEOUT = 86400
