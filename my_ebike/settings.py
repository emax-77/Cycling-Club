# env values setup 
import os
from django.core.exceptions import ImproperlyConfigured
def _require_env(name):
    value = os.getenv(name)
    if value is None:
        raise ImproperlyConfigured('Required environment variable "{}" is not set.'.format(name))
    return value

# ensure SSL_CERT_FILE is set to certifi's bundle if not already set
if 'SSL_CERT_FILE' not in os.environ:
    try:
        import certifi
        os.environ['SSL_CERT_FILE'] = certifi.where()
    except Exception:
        # If certifi is not installed, leave environment as-is and let the OS handle certs
        pass

# smtp setup
email_name = _require_env('EMAIL_HOST_USER')
email_password = _require_env('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = email_name 
EMAIL_HOST_PASSWORD = email_password 
EMAIL_BACKEND = 'my_ebike.email_backend.CertifiEmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_TIMEOUT = 20

# Contact form recipient(s)
CONTACT_RECIPIENT_EMAIL = os.getenv('CONTACT_RECIPIENT_EMAIL', EMAIL_HOST_USER)
CONTACT_RECIPIENT_LIST = [CONTACT_RECIPIENT_EMAIL]

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y%h8io-jgj1dv=wh*3&6$45el91=_x_%x-2mhgv23w!=$4oav)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']

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
    'debug_toolbar'
    
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
    "debug_toolbar.middleware.DebugToolbarMiddleware"

]

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/' 
STATIC_ROOT = BASE_DIR / 'productionfiles'  # For production use 
STATICFILES_DIRS = [
    BASE_DIR / 'mystaticfiles'  # Additional static directories in development !!!
]

# Media files (uploaded user files)
MEDIA_URL = '/media/' 
MEDIA_ROOT = BASE_DIR / 'media'  # Directory for storing user-uploaded files

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# After login redirect here 
LOGIN_REDIRECT_URL = '/welcome/'
# Where to redirect after logout
LOGOUT_REDIRECT_URL = '/'
