from django.contrib import admin
from .models import User, Testimoniales
from django.utils.text import Truncator

# Register your models here.


# Decoradores para manejar mejor la UI del Admin en la web
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # List of fields to display in the admin change list
    list_display = [
        "username",
        "email",
        "phone",
        "first_name",
        "last_name",
        "is_superuser",
        "is_staff",
        "is_active",
        "date_joined",
        "last_login",
    ]

    # List of fields to filter the admin change list
    list_filter = ["username", "email"]

    class Meta:
        model = User


@admin.register(Testimoniales)
class TestimonialesAdmin(admin.ModelAdmin):
    list_display = ["usuario", "get_short_testimonial"]
    list_filter = ["usuario"]

    class Meta:
        verbose_name_plural = "Testimoniale"

    def get_short_testimonial(self, obj):
        return Truncator(obj.contenido).words(5)

    get_short_testimonial.short_description = "Contenido"
