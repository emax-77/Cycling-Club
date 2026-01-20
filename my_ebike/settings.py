import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == '':
        raise ImproperlyConfigured(f'Required environment variable "{name}" is not set.')
    return value


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {'1', 'true', 'yes', 'y', 'on'}


def _env_list(name: str, default: list[str] | None = None) -> list[str]:
    raw = os.getenv(name)
    if raw is None:
        return list(default or [])
    return [part.strip() for part in raw.split(',') if part.strip()]

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
# Default stays True for local dev convenience.
DEBUG = _env_bool('DJANGO_DEBUG', True)

# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-y%h8io-jgj1dv=wh*3&6$45el91=_x_%x-2mhgv23w!=$4oav)')
else:
    SECRET_KEY = _require_env('SECRET_KEY')

if DEBUG:
    ALLOWED_HOSTS = _env_list('DJANGO_ALLOWED_HOSTS', ['localhost', '127.0.0.1', '[::1]'])
else:
    ALLOWED_HOSTS = _env_list('DJANGO_ALLOWED_HOSTS')
    if not ALLOWED_HOSTS:
        raise ImproperlyConfigured('DJANGO_ALLOWED_HOSTS must be set in production (comma-separated).')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentication',
    'members',
]

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'my_ebike.middleware.LoginRequiredMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

INTERNAL_IPS = ["127.0.0.1"] if DEBUG else []

ROOT_URLCONF = 'my_ebike.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'my_ebike.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    try:
        import dj_database_url

        DATABASES = {
            'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=not DEBUG),
        }
    except Exception as exc:
        raise ImproperlyConfigured('DATABASE_URL is set but dj-database-url is not installed or failed to parse it.') from exc
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', 'English'),
    ('sk', 'Slovenčina'),
]

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'productionfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'mystaticfiles',
]

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

# Media files (uploaded user files)
MEDIA_URL = '/media/' 
MEDIA_ROOT = BASE_DIR / 'media'  # Directory for storing user-uploaded files

# ensure SSL_CERT_FILE is set to certifi's bundle if not already set
if 'SSL_CERT_FILE' not in os.environ:
    try:
        import certifi

        os.environ['SSL_CERT_FILE'] = certifi.where()
    except Exception:
        pass

# Email
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

if DEBUG and (not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD):
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    if not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD:
        raise ImproperlyConfigured('EMAIL_HOST_USER and EMAIL_HOST_PASSWORD must be set for SMTP email.')
    EMAIL_BACKEND = 'my_ebike.email_backend.CertifiEmailBackend'
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_USE_TLS = _env_bool('EMAIL_USE_TLS', True)
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
    EMAIL_TIMEOUT = int(os.getenv('EMAIL_TIMEOUT', '20'))

# Contact form recipient(s)
CONTACT_RECIPIENT_EMAIL = os.getenv('CONTACT_RECIPIENT_EMAIL', EMAIL_HOST_USER or '')
CONTACT_RECIPIENT_LIST = [CONTACT_RECIPIENT_EMAIL] if CONTACT_RECIPIENT_EMAIL else []

# Production security
CSRF_TRUSTED_ORIGINS = _env_list('DJANGO_CSRF_TRUSTED_ORIGINS', [])

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = _env_bool('DJANGO_SECURE_SSL_REDIRECT', True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.getenv('DJANGO_SECURE_HSTS_SECONDS', '3600'))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = _env_bool('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', False)
    SECURE_HSTS_PRELOAD = _env_bool('DJANGO_SECURE_HSTS_PRELOAD', False)

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# After login redirect here 
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Public routes (everything else requires authentication via LoginRequiredMiddleware)
LOGIN_REQUIRED_EXEMPT_PATHS = [
    '/',
    '/welcome/',
    '/login/',
    '/register/',
    '/contact/',
]
LOGIN_REQUIRED_EXEMPT_PREFIXES = [
    '/admin/',
    '/accounts/',
    '/i18n/',
    '/static/',
    '/media/',
    '/__debug__/',
]
