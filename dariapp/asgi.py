import os
# from django.conf import settings
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dariapp.settings.dev')
# os.environ['DJANGO_SETTINGS_MODULE'] = settings.DJANGO_SETTINGS_MODULE

asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import daru_wheel.routing

application = ProtocolTypeRouter({
    "http": asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            daru_wheel.routing.websocket_urlpatterns
        )
    )
})
