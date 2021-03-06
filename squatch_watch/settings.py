"""
Django settings for squatch_watch project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import os

import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%q^vd^^-ymab0_cr3*98_*x5$4k#5bgvu*qyp8g@f8rq@ipw5&'

# SECURITY WARNING: don't run with debug turned on in production!
ENV_STAGE = "DEV"
#ENV_STAGE = "QA"
#ENV_STAGE = "PROD"

DEBUG = False

if ENV_STAGE == "DEV":
    DEBUG = True
    
POSTGRES_DB = False
ALLOWED_HOSTS = ['*']

DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS = ['127.0.0.1',]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'monsters',
    'accounts',
    'api',
    'mathfilters',
    'crispy_forms',
    'import_export',
    'rest_framework',
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    #'whitenoise.middleware.WhiteNoiseMiddleware', Deployment
]

ROOT_URLCONF = 'squatch_watch.urls'

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

WSGI_APPLICATION = 'squatch_watch.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
if POSTGRES_DB:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'squatch_watch_db',
            'USER': 'postgres',
            'PASSWORD': 'Squatch_Admin22!',
            'HOST': 'localhost',
            'POST': '5432',
        }
    }
else:    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

# Logging settings
import logging

LOGGING = {
        'version': 1,
        'formatters': {
            'detailed': {
                'class': 'logging.Formatter',
                'format': '%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
            },
            'development_logfile': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'logs/temp/debug.log',
                'formatter': 'detailed',
            },
            'production_logfile': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/debug.log',
                'maxBytes' : 1024*1024*100, # 100MB
                'backupCount' : 5,
                'formatter': 'detailed',
            },
        },
         'root': {
             'level': 'DEBUG',
             'handlers': ['console','development_logfile','production_logfile'],
         },
    }

logging.config.dictConfig(LOGGING)

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
#USE_TZ = True
USE_TZ = False

# -------------------------------------------------------------------------
IMPORT_EXPORT_USE_TRANSACTIONS = True 
# Info about IMPORT_EXPORT_USE_TRANSACTIONS 
#https://simpleisbetterthancomplex.com/packages/2016/08/11/django-import-export.html
# -----------------------------------------------------------------------------------

CRISPY_TEMPLATE_PACK = 'bootstrap4' # BootStrap Templates

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if ENV_STAGE != "DEV":
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'

os.makedirs(STATIC_URL, exist_ok=True)

# Deployment use -------------------------------------------------------------

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    #'/var/www/static/', 
]

# For Monster Images 
MEDIA_ROOT = BASE_DIR
MEDIA_URL = '/media/'

MEDIA_REPORT_URL = '/media/monsters/reports/'
MEDIA_MONSTER_IMAGE_URL = '/media/monsters/images/'
MEDIA_ACCOUNT_IMAGE_URL = '/media/account/images/'

# Emails 
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_ROOT = BASE_DIR
EMAIL_URL = '/emails/'

django_heroku.settings(locals())