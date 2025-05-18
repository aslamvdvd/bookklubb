"""
ASGI config for bookhaven project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack # For user authentication in WebSockets
import groupchat.routing # Import the routing from your app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookhaven.settings')

# Get the default Django ASGI application to handle HTTP requests
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,

    # WebSocket chat handler
    "websocket": AuthMiddlewareStack( # Wrap with AuthMiddlewareStack to access request.user
        URLRouter(
            groupchat.routing.websocket_urlpatterns
        )
    ),
})
