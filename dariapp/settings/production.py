from __future__ import absolute_import

from .base import *
import os

env=os.environ.copy()

SECRET_KEY = config("SECRET_KEY", default="dadmin")
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1', cast=Csv())
# ALLOWED_HOSTS = ['0.0.0.0', '.herokuapp.com', '127.0.0.1']
DEBUG = False

try:
    from .local import *
except ImportError:
    pass



# email backend
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="kipngeno.gibeon@gmail.com")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="tetyty9iodjw!")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "Darius Team <noreply@darispin.com>"


DJANGO_SETTINGS_MODULE = config(
    "DJANGO_SETTINGS_MODULE",
    default='dariapp.settings.production')


# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/3.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'   
# 
# 
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("DB_NAME", default="darius_db"),
        "USER": config("DB_USER", default="daru"),
        "PASSWORD": config("DB_PASSWORD", default="password"),
        "HOST": "localhost",
        "PORT": "",
    }
}
  