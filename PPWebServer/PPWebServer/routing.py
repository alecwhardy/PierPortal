from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import PPLive.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)

    # Any ws:// or wss:// connections are handled by AuthMiddlewareStack
    'websocket': AuthMiddlewareStack(
        URLRouter(
            PPLive.routing.websocket_urlpatterns
        )
    ),
})