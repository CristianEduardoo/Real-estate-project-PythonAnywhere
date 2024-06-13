from rest_framework import serializers # Se encargan de convertir la información de los modelos a JSON
from main.models import Propiedades


class PropiedadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propiedades
        fields = (
            "id",
            "titulo",
            "precio",
            "img",
            "descripcion",
            "contentido",
            "habitaciones",
            "wc",
            "garaje",
            "fecha_alta",
            "vendido",
        )
        # Los campos que voy a serializar a Json