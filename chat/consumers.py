import json # Todas las comunicaciones son por via JSON
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone

# Importamos los modelos o formularios
from .models import Message


# Definir todos los consumer que tiene nuestra applicación
# Solo tenenmos un 1 solo evento de comunicación
class ChatConsumer(WebsocketConsumer):
    # Definir un Diccionario de usuarios conectados
    connected_users = {}

    def connect(self):
        # Id de la sala
        self.id = self.scope["url_route"]["kwargs"]["room_id"]
        # Group name => nombre/id de la sala
        self.room_group_name = "sala_chat_%s" % self.id
        self.user = self.scope["user"]

        print("conexión establecida al room_group_name " + self.room_group_name)
        # Channel name para hacerla sincrona => el hash unico que tiene el usuario
        print("Conexión establecida channel_name " + self.channel_name)

        if self.user.is_authenticated:
            self.username = self.user.username
            print(self.username)
        else:
            None

        # Agregamos al usuario al diccionario de usuarios conectados
        if self.room_group_name not in self.connected_users:
            self.connected_users[self.room_group_name] = []
        if self.username:
            self.connected_users[self.room_group_name].append(self.username)

        # Paso el nombre de la sala y el usuario conectado a ella
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        # Para realizar la conexión
        self.accept()

        # Despues de acceptar
        # Enviamos la lista de usuarios conectados a todos los usuarios de la sala
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "user_list", 
                "users": self.connected_users[self.room_group_name]
            },
        )

    def receive(self, text_data):
        print("mensaje recibido")
        print(text_data)

        # Obtener el Id del usuario que envia el mensaje
        try:
            text_data_json = json.loads(text_data)
            event_type = text_data_json.get("type")

            if event_type == "chat_message":
                message = text_data_json["message"]

                # Obtenemos el ID del usuario que envia el mensaje
                if self.scope["user"].is_authenticated:
                    sender_id = self.scope["user"].id
                else:
                    None

                # Si el usuario existe
                if sender_id:
                    # Grabamos el mensaje en la base de datos
                    message_save = Message.objects.create(
                        user_id=sender_id, room_id=self.id, message=message
                    )
                    message_save.save()

                    # Sincronizamos y enviamos el mensaje a la sala de chat
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            "type": "chat_message",
                            "message": message,
                            "username": self.user.username,
                            "datetime": timezone.localtime(timezone.now()).strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            "sender_id": sender_id,
                        },
                    )
                else:
                    print("Usuario no autenticado. Ignorando el mensaje")
            elif event_type == "user_list":
                # Este evento lo manejamos con JS del lado del cliente
                pass

        except json.JSONDecodeError as e:
            print("Hubo un error al decodificar el JSON: ", e)
        except KeyError as e:
            print("Clave faltante en el JSON: ", e)
        except Exception as e:
            print("Error desconocido: ", e)

    def disconnect(self, close_code):
        print("conexión cerrada")

        # Eliminar al usuario del diccionario de usuarios conectados
        if self.username in self.connected_users[self.room_group_name]:
            self.connected_users[self.room_group_name].remove(self.username)

        # Enviamos la lista de usuarios conectados Actualizada
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": "user_list", "users": self.connected_users[self.room_group_name]},
        )

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # ======================== Funciónes externas ======================== */

    # === Función externa de la funcion connect/disconnect === */
    def user_list(self, event):
        # Enviar la lista de usuarios conectados
        self.send(text_data=json.dumps({
            "type": "user_list", 
            "users": event["users"]
        }))

    # === Función externa de la funcion receive === */
    def chat_message(self, event):
        # Todos los parametros del
        # async_to_sync(self.channel_layer.group_send)(self.room_group_name,
        message = event["message"]
        username = event["username"]
        datetime = event["datetime"]
        sender_id = event["sender_id"]

        # Verificamos que sea el usuario atenticado sea quien envia el mensaje
        current_user_id = self.scope["user"].id
        if sender_id != current_user_id:
            # Envia el mensaje
            self.send(
                text_data=json.dumps(
                    {
                        "type": "chat_message",
                        "message": message,
                        "username": username,
                        "datetime": datetime,
                    }
                )
            )
