import os
from pathlib import Path
import json

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

#### datos de configuración
ruta = os.path.dirname(os.path.abspath(__file__))
f = open('{}/conf.json'.format(ruta),'r')
conf_String = f.read()
f.close()
conf = json.loads(conf_String)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-i*a8jk32x^ydk6rnz5)f$-f4+w-ps-fs1!8r#(!)yr3a4&+%$d'

# SECURITY WARNING: don't run with debug turned on in production!

# Desacoplamiento de datos sensibles
RUTA = conf['ruta']
RUTA2 = conf['ruta2']
SERVER_SMTP = conf['smtp']
PUERTO_SMTP = conf['smtp_puerto']
MAIL_SALIDA = conf['email']
PASSWORD_MAIL_SALIDA = conf['email_password']
WEBPAY_URL = conf['webpay_url']
WEBPAY_ID = conf['webpay_id']
WEBPAY_SECRET = conf['webpay_secret']
BASE_URL = conf['base_url']  # ← agregar esto
DEBUG = conf['debug']

ALLOWED_HOSTS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'productos',
    'carro',
    'acceso',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = 'tienda.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'tienda.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default':{
        'ENGINE':'django.db.backends.mysql',
        'NAME':conf['bd'],
	'USER':conf['user'],
	'PASSWORD':conf['password'],
	'HOST':conf['server'],
	'PORT': str(conf['puerto']), # Convertimos a string por segueidad (maria db)
	'OPTIONS':{
	'autocommit':True,
 	},
	},
    }

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/assets/'
STATICFILES_DIRS=(os.path.join(BASE_DIR,'assets'),)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'