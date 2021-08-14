from .base import *

SECRET_KEY = config("SECRET_KEY", default="dadmin")

DEBUG = False

try:
    from .local import *
except ImportError:
    pass
