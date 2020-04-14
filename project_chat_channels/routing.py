from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from app_chat_channels.consumers import ChatConsumer


# higher versions of django may give errors while doing runserver

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url(r"^messages/(?P<username>[\w.@+-]+)", ChatConsumer),
                ]
            )
        )
    )
})

# ws://domain/<username>
