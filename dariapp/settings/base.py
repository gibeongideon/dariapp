"""
Django settings for daruapp project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
# import os
from pathlib import Path
from celery.schedules import crontab

# import dj_database_url
from decouple import config
from decouple import Csv
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/
SECRET_ADMIN_URL = config("SECRET_ADMIN_URL", default="dadmin")
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default="dadmin")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "channels",
        # "functional_tests",
    # ...
    "admin_interface",
    "colorfield",
    # ...
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',    
    'home',   

    # 'search',
    'users',
    "account",
    # "dashboard",
    "daru_wheel",
    "mpesa_api.core",
    "mpesa_api.util",
    "rest_framework",
    # 'rest_framework.authtoken',
    'paypal.pro',
    'paypal.standard.ipn',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'dariapp.urls'
TEMPLATE_DIR = BASE_DIR / "templates"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
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

WSGI_APPLICATION = 'dariapp.wsgi.application'
ASGI_APPLICATION = "dariapp.asgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "./db.sqlite3",

    }
 }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = "Africa/Nairobi"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [BASE_DIR / 'staticfiles',]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/3.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = (
    BASE_DIR / "./static"
) 

MEDIA_ROOT = (
    BASE_DIR / "./media"
)

MEDIA_URL = '/media/'


AUTH_USER_MODEL = "users.User"

# email backend
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="kipngeno.gibeon@gmail.com")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="tetyty9iodjw!")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "Darius Team <noreply@darispin.com>"

# login/logout redirect
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

##### Channels-specific settings

# redis_host = os.environ.get('REDIS_HOST', 'localhost')
# Channel layer definitions
# http://channels.readthedocs.io/en/latest/topics/channel_layers.html

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [("127.0.0.1", 6379)],},
    }
}


###### CELERY-specific settings
SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"
# CELERY_BROKER_URL = 'amqp://localhost:5672'
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CELERY_BEAT_SCHEDULE = {
    "create_spin_wheel_market": {
        "task": "daru_wheel.tasks.create_spinwheel",
        "schedule": crontab(minute=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]),
    },
    "run_count_down_timer": {
        "task": "daru_wheel.tasks.start_count_down",
        "schedule": crontab(minute=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]),
    },
}


# log stuff to console
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"level": "DEBUG", "class": "logging.StreamHandler",},
        "logfile": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "./logfile",
        },
    },
    "root": {"level": "INFO", "handlers": ["console", "logfile"]},
}



JET_SIDE_MENU_COMPACT = True


# Safaricom-specific settings Configs

# B2C (Bulk Payment) Configs
# see https://developer.safaricom.co.ke/test_credentials
# https://developer.safaricom.co.ke/b2c/apis/post/paymentrequest

MPESA_B2C_ACCESS_KEY = config("MPESA_B2C_ACCESS_KEY", default="")
MPESA_B2C_CONSUMER_SECRET = config("MPESA_B2C_CONSUMER_SECRET", default="")

B2C_SECURITY_TOKEN = config("B2C_SECURITY_TOKEN", default="")
B2C_INITIATOR_NAME = config("B2C_INITIATOR_NAME", default="")
B2C_COMMAND_ID = config("B2C_COMMAND_ID", default="")
B2C_SHORTCODE = config("B2C_SHORTCODE", default="")
B2C_QUEUE_TIMEOUT_URL = config("B2C_QUEUE_TIMEOUT_URL", default="")
B2C_RESULT_URL = config("B2C_RESULT_URL", default="")
MPESA_URL = config("MPESA_URL", default="https://sandbox.safaricom.co.ke")

# C2B (Paybill) Configs
# See https://developer.safaricom.co.ke/c2b/apis/post/registerurl

MPESA_C2B_ACCESS_KEY = config("MPESA_C2B_ACCESS_KEY", default="")
MPESA_C2B_CONSUMER_SECRET = config("MPESA_C2B_CONSUMER_SECRET", default="")

C2B_REGISTER_URL = config("C2B_REGISTER_URL", default="")
C2B_VALIDATE_URL = config("C2B_VALIDATE_URL", default="")
C2B_CONFIRMATION_URL = config("C2B_CONFIRMATION_URL", default="")
C2B_SHORT_CODE = config("C2B_SHORT_CODE", default="")
C2B_RESPONSE_TYPE = config("C2B_RESPONSE_TYPE", default="Completed")
C2B_ONLINE_CHECKOUT_CALLBACK_URL = config(
    "C2B_ONLINE_CHECKOUT_CALLBACK_URL", default=""
)
C2B_ONLINE_PASSKEY = config("C2B_ONLINE_PASSKEY", default="")
C2B_ONLINE_SHORT_CODE = config("C2B_ONLINE_SHORT_CODE", default="")
C2B_ONLINE_PARTY_B = config("C2B_ONLINE_PARTY_B", default="")

TOKEN_THRESHOLD = config("TOKEN_THRESHOLD", default=600)  # , cast=int)

#Paypal


PAYPAL_RECEIVER_EMAIL = config(
    "PAYPAL_RECEIVER_EMAIL",
    default="darius.option@gmail.com")

PAYPAL_TEST = config("PAYPAL_TEST", default=False)


###USA/CANADA&UK

PAYPAL_WPP_USER = config(
    "PAYPAL_WPP_USER",
    default="sb-h2ded6675419_api1.business.example.com")

PAYPAL_WPP_PASSWORD = config(
    "PAYPAL_WPP_PASSWORD",
    default="DFXXXTJPDKBFA5KG")

PAYPAL_WPP_SIGNATURE = config(
    "PAYPAL_WPP_SIGNATURE",
    default="AM1aGgn2bz5QbLwfJWgM8rQPCVdfAjz3hKc8w9Pa8XdIFnHt-9r143O2")



DJANGO_SETTINGS_MODULE = config(
    "DJANGO_SETTINGS_MODULE",
    default='dariapp.settings.dev')



# Heroku: Update database configuration from $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

SITE_DOMAIN = config(
    "SITE_DOMAIN",
    default="localhost:8000")


# Creating Access Token for Sandbox
PAYPAL_CLIENT_ID = config("PAYPAL_CLIENT_ID", default="")
PAYPAL_CLIENT_SECRET = config("PAYPAL_CLIENT_SECRET", default="")

