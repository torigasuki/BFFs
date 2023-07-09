import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BFFs.settings")
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from .middleware import JwtAuthMiddlewareStack
from alarm import routing

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": JwtAuthMiddlewareStack(
            URLRouter(routing.websocket_urlpatterns),
        ),
    }
)
