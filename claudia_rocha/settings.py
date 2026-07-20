import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Em produção, defina DJANGO_SECRET_KEY no ambiente do servidor.
# O valor abaixo só é usado como fallback em desenvolvimento local.
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-4t2_b$r)w)8=-0!84k=z^w+d7%y+6-wj^xp6ixbfglv*dmx=g*',
)

DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    h.strip() for h in os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',') if h.strip()
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'core',
    'blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'claudia_rocha.urls'

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

WSGI_APPLICATION = 'claudia_rocha.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/painel/login/'

# ── E-mail (recuperação de senha do painel) ──
# Em desenvolvimento local, sem variáveis definidas, os e-mails aparecem
# apenas no terminal (console backend) — não é necessário configurar nada
# para testar. Em produção, defina as variáveis DJANGO_EMAIL_* no servidor.
if os.environ.get('DJANGO_EMAIL_HOST'):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('DJANGO_EMAIL_HOST')
    EMAIL_PORT = int(os.environ.get('DJANGO_EMAIL_PORT', '587'))
    EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_HOST_PASSWORD')
    EMAIL_USE_TLS = os.environ.get('DJANGO_EMAIL_USE_TLS', 'True') == 'True'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = os.environ.get('DJANGO_DEFAULT_FROM_EMAIL', 'nao-responda@claudiarochaadv.com')
PASSWORD_RESET_TIMEOUT = 3600  # link válido por 1 hora

# Endurecimento de segurança — ativo apenas em produção (DEBUG=False)
# HTTPS_READY controla tudo que depende de certificado SSL já emitido.
# Deixe em False (via DJANGO_HTTPS_READY=False) até o domínio ter HTTPS
# configurado, senão o site fica inacessível (cookies/redirect exigem HTTPS
# que ainda não existe).
if not DEBUG:
    HTTPS_READY = os.environ.get('DJANGO_HTTPS_READY', 'True') == 'True'
    SECURE_SSL_REDIRECT = HTTPS_READY
    SESSION_COOKIE_SECURE = HTTPS_READY
    CSRF_COOKIE_SECURE = HTTPS_READY
    SECURE_HSTS_SECONDS = 31536000 if HTTPS_READY else 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = HTTPS_READY
    SECURE_HSTS_PRELOAD = HTTPS_READY
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
