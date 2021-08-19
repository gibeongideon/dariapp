from .base import *

SECRET_KEY = config("SECRET_KEY", default="dadmin")

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