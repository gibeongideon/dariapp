from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ispin_wheel/", consumers.QspinConsumer.as_asgi()),
    re_path(r"ispinx_wheel/", consumers.XspinConsumer.as_asgi()),
]
