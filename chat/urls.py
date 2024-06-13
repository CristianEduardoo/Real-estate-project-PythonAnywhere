from django.urls import path  # path nos permite crear las urls que necesitemos
from . import views  # me traigo todas las vistas

app_name = "namespacechat"

urlpatterns = [
    path("", views.viewHome, name="home"),
    path("room/<int:room_id>/", views.viewRoom, name="room-datail"),
]