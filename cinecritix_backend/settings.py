"""
Django settings for cinecritix_backend project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import dj_database_url
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!


SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
#SECRET_KEY = 'SFXGHDFXBGR852S613DV1S65HSR12H1D65GB1X5S1DEG51RSBFS1B5'
#DEBUG = True

ALLOWED_HOSTS = [
    '*'
    # Agrega cualquier otro host que necesites permitir
]

CORS_ALLOWED_ALL_ORIGINS = True


# Configuración para archivos de medios
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'coreapi',
    'rest_framework.authtoken',
    'rest_framework',
    'django_rest_passwordreset',
    'users_cinecritix',
    'modulo_peliculas_cinecritix',
    'modulo_series_cinecritix'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cinecritix_backend.urls'

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

WSGI_APPLICATION = 'cinecritix_backend.wsgi.application'

# Database URL



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Usa el motor de base de datos que necesitas
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  # Ruta a la base de datos
    }
} 

# Database configuration using dj-database-url
#database_url = os.environ.get("DATABASE_URL")
DATABASES["default"]=dj_database_url.parse("postgres://cinecritixapp_bd_wdxx_user:NyMHPaTSWbmBtbML0Za1cKaEF3dpxfAq@dpg-clha67fjc5ks73ekhh3g-a.ohio-postgres.render.com/cinecritixapp_bd_wdxx")



#DATABASES["default"]=dj_database_url.parse("postgres://cinecritixapp_bd_user:XQCQrEZrRJ3MGlKZHt3Yi2vj5zEoFbyh@dpg-cksts30168ec73ears40-a.oregon-postgres.render.com/cinecritixapp_bd")

#"postgres://cinecritixapp_bd_user:XQCQrEZrRJ3MGlKZHt3Yi2vj5zEoFbyh@dpg-cksts30168ec73ears40-a.oregon-postgres.render.com/cinecritixapp_bd"
AUTH_USER_MODEL = 'users_cinecritix.CustomUser'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME= 0.03
SEND_API = os.getenv('SEND_API')
EMAIL_SENDER = os.getenv('EMAIL_SENDER')