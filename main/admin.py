from django.contrib import admin
from .models import Clientes, Vendedores, Propiedades, Ventas, Propiedad_Vendedor
from django.utils.text import Truncator

# Register your models here.

# Decoradores para manejar mejor la UI del Admin en la web
@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ["nombre", "apellido", "telefono", "email"]
    list_filter = ["email"]
    class Meta:
        verbose_name_plural = "Cliente"


@admin.register(Vendedores)
class VendedoresAdmin(admin.ModelAdmin):
    list_display = ["nombre", "apellido", "telefono", "email"]
    list_filter = ["email"]
    class Meta:
        verbose_name_plural = "Vendedore"


@admin.register(Propiedades)
class PropiedadesAdmin(admin.ModelAdmin):
    list_display = [
        "titulo",
        "precio",
        "img",
        "get_short_description",
        "get_short_contentido",
        "habitaciones",
        "wc",
        "garaje",
        "fecha_alta",
        "vendido",
    ]
    list_filter = ["titulo"]

    class Meta:
        verbose_name_plural = "Propiedade"

    def get_short_description(self, obj):
        return Truncator(obj.descripcion).words(5)

    def get_short_contentido(self, obj):
        return Truncator(obj.contentido).words(5)

    get_short_description.short_description = "Descripción"
    get_short_contentido.short_description = "Contenido"
    # .short_description => atributo especial que puedo asignar a una función personalizada
    # Descripción => Nombre más legible y descriptivo para la columna que representa la salida en la interfaz del Admin de Django


# Decoradores para manejar mejor la UI del Admin en la web
@admin.register(Ventas)
class VentasAdmin(admin.ModelAdmin):
    list_display = ["cliente", "vendedor", "propiedad", "fecha_venta"]
    list_filter = ["propiedad"]


@admin.register(Propiedad_Vendedor)
class VentasAdmin(admin.ModelAdmin):
    list_display = ["propiedad", "vendedor", "fecha_alta"]
    list_filter = ["propiedad"]
