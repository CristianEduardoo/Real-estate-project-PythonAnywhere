from django.contrib import admin
from .models import Room, Message

# Register your models here.

# admin.site.register(Room)
# Decorador para registrar el modelo Room tunneado en el sitio de administrador
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    # Metodo para mostrar el numero de usuarios
    def number_of_users(self, obj):
        return obj.users.count()

    # List of fields to display in the admin change list
    list_display = ["name", "number_of_users"]

    # List of fields to filter the admin change list
    list_filter = ["name"]

    # Campos de búsqueda
    search_fields = ["name"]


class MessageAdmin(admin.ModelAdmin):
    list_display = ("user", "room", "message", "timestamp")
    list_filter = ("room", "user")


# Otra forma de registrar en el Admin => (Modelo, Clase)
admin.site.register(Message, MessageAdmin)