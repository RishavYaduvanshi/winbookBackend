from django.urls import path
from channels.routing import URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from custom.authentication import (
    TokenHeaderAuthenticationMiddleware,
    TokenPathAuthenticationMiddleware,
)
from chat import consumers as chatConsumers

websocket_urlpatterns = [
    path("ws/chat/", chatConsumers.ChatConsumer.as_asgi()),
]


def get_router():
    routes = []
    routes.extend(websocket_urlpatterns)
    return AllowedHostsOriginValidator(
        TokenPathAuthenticationMiddleware(URLRouter(routes))
    )
