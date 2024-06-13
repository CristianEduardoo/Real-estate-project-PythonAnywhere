from django.contrib import admin

from .models import Blog
from django.utils.text import Truncator

# Register your models here.

# Decoradores para manejar mejor la UI del Admin en la web
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    # List of fields to display in the admin change list
    list_display = [
        "title",
        "nombre_titular",
        "img_jpg",
        "img_webp",
        "fecha",
        "get_short_description",
        "get_short_contentido",
    ]

    # List of fields to filter the admin change list
    list_filter = ["title", "nombre_titular"]

    # Campos de búsqueda por medio de 2 campos
    search_fields = ["title", "nombre_titular"]

    class Meta:
        model = Blog

    # Función para mostrar el texto en 5 palabras
    def get_short_description(self, obj):
        return Truncator(obj.descripcion).words(5)

    def get_short_contentido(self, obj):
        return Truncator(obj.contenido).words(5)

    get_short_description.short_description = "Descripción"
    get_short_contentido.short_description = "contenido"
