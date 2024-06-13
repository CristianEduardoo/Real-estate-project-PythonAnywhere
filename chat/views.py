from django.shortcuts import render

# descorador para validar si el usuario esta autenticado
from django.contrib.auth.decorators import login_required

# Importamos los modelos o formularios
from .models import Room

# Create your views here.


def viewHome(request):
    # rooms = Room.objects.all()
    room_name = Room.objects.first()
    return render(request, "chat/home.html", {"room_name": room_name})


# ====== Codigo para permitir a cualquier usuario logged entrar en cualquier sala ======
@login_required
def viewRoom(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        error_message = "La sala de chat no existe."
        return render( request, "chat/home.html",
            {"error_message": error_message, "room_name": Room.objects.first()},
        )

    return render(request, "chat/room.html", {"room": room})


# @login_required
# def viewRoom(request, room_id):
#     try:
#         # Conecta al usuario con el id de la sala
#         room = request.user.rooms_joined.get(id=room_id)
#     except Room.DoesNotExist:
#         # return HttpResponseForbidden("No tienes permiso de acceso a este chat")
#         error_message = "No tienes permiso de acceso a este chat"
#         return render(request, "chat/home.html",
#             {"error_message": error_message, "rooms": Room.objects.all()},
#         )

#     return render(request, "chat/room.html", {"room": room})
