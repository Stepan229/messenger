"""
ASGI config for social_network project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
https://www.geeksforgeeks.org/token-authentication-in-django-channels-and-websockets/
"""

import os



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from messanger.routing import websocket_urlpatterns
from channels.security.websocket import AllowedHostsOriginValidator
from messanger.middleware import TokenAuthMiddleware

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            TokenAuthMiddleware(URLRouter(websocket_urlpatterns))
        ),
    }
)

# application = ProtocolTypeRouter(
#     {
#         "http": get_asgi_application(),
#         "websocket": AllowedHostsOriginValidator(
#             TokenAuthMiddleware(URLRouter(websocket_urlpatterns))
#         ),
#     }
# )
