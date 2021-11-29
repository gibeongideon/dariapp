from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-cbk=3tx++3-x+1$ohy2g960+o$+f1y5*cv4o*mrp-hphmxgc8p'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ['0.0.0.0', '.herokuapp.com', '127.0.0.1'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


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
