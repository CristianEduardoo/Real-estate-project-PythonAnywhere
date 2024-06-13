from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/chat/room/<room_id>/", ChatConsumer.as_asgi()),
]


# Para que Django Channels pueda manejar correctamente esta conexión WebSocket, 
# el consumidor debe ser convertido a un objeto ASGI. Esto es lo que hace as_asgi().