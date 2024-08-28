
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_school.settings')
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
django_asgi_app = get_asgi_application()
from channels.auth import AuthMiddlewareStack
from my_chat import routing


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
