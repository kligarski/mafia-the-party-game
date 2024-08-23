from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/game/(?P<game_code>[a-zA-Z0-9]{6})/$", consumers.GameConsumer.as_asgi()),
]