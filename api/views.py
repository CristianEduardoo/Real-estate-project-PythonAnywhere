# Nos olvidamos del render y usamos un viewsets y permissions
from rest_framework import viewsets, permissions
from main.models import Propiedades  # Importamos el modelo
from .serializers import PropiedadesSerializer  # Importamos el serializador

# Create your views here.

class PropiedadesViewSet(viewsets.ModelViewSet):
    queryset = Propiedades.objects.all()  # queryset => es convención. Le decimos que nos traiga todos las propiedades
    serializer_class = PropiedadesSerializer  # Le decimos que serializador va a usar

    permission_classes = [
        permissions.AllowAny  # Le decimos que cualquier usuario puede acceder a los datos
    ]
    
    """ def get_queryset(self):
        queryset = self.queryset
        return queryset  # Devolvemos el queryset  """