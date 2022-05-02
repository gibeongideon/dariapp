from .base import *

DEBUG = False
ALLOWED_HOSTS = ['159.223.9.47', 'www.dariplay.ga', '127.0.0.1','dariplay.ga','localhost'] 
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("DB_NAME", default="dariusdb"),
        "USER": config("DB_USER", default="darius"),
        "PASSWORD": config("DB_PASSWORD", default="darius54321"),
        "HOST": "localhost",
        "PORT": "",
    }
}


PAYPAL_TEST = False
PAYPAL_RECEIVER_EMAIL =config(
     "PAYPAL_RECEIVER_EMAIL",
     default="elihu.kipyegon@gmail.com")