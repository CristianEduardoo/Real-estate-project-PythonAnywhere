from django.urls import path  # path nos permite crear las urls que necesitemos
from . import views  # me traigo todas las vistas
# Tambien se puede acceder => views.my_main.etc

app_name = "namespaceraices"

urlpatterns = [
    path("", views.my_main, name="main"),
    path("nosotros/", views.nosotros, name="nosotros"),
    path("anuncios/", views.anuncios, name="anuncios"),
    path("<int:id>/", views.anuncio_detalles, name="anuncio_detalles"),
    path("contacto/", views.contacto, name="contacto"),
    path("testimoniales/", views.viewTestimoniales, name="testimonials"),
    path("check_user_testimonial/", views.check_user_testimonial, name="check_user_testimonial"),
]