from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.html import escape
from django.http import Http404


# descorador para validar si el usuario esta autenticado
from django.contrib.auth.decorators import login_required

# libreria para enviar un correo electronico
from django.core.mail import send_mail

# Importamos los modelos o formularios
from .models import Propiedades
from users.models import Testimoniales
from blog.models import Blog  # Importa el modelo Blog de la app blog
from .forms import ContactForm
from .forms import TestimonialForm


# Create your views here.

def my_main(request):
    # Obtener los tres primeros elementos de Propiedades
    solo_tres_propiedades = Propiedades.objects.filter(vendido=False)[:3]

    # Obtener los dos primeros elementos de Blog
    solo_dos_blog = Blog.objects.all()[:2]

    # Testimoniales
    testimoniales_result = Testimoniales.objects.all()

    return render(request, "plantillas/index.html", {"solo_tres": solo_tres_propiedades, "solo_dos": solo_dos_blog, "testimoniales": testimoniales_result})


def nosotros(request):
    return render(request, 'plantillas/nosotros.html')


# descorador para validar si el usuario esta autenticado
@login_required
def viewTestimoniales(request):

    user = request.user

    # Verificar si el usuario ya tiene una reseña
    if Testimoniales.objects.filter(usuario=user).exists():
        messages.error(request, "Ya has escrito una reseña.")

    if request.method == "POST":
        form = TestimonialForm(request.POST)
        if (form.is_valid()):  # valida  los campos del formulario, que no esten vacion, etc

            # Si el formulario es válido, guardamos el blog en la base de datos
            new_testimonials = form.save(commit=False)
            new_testimonials.usuario = (request.user)  # Establecer el nombre del titular como el nombre de usuario autenticado
            new_testimonials.save()

            # Guarda el nuevo registro en BD
            new_testimonials = form.save()
            messages.success(request, "Reseña creada con éxito!")
            # Redirecciona a un Url
            return redirect("namespaceraices:main")
    else:
        form = TestimonialForm()

    return render(request, "plantillas/testimoniales.html", {"form_testimoniales": form})


# Endpoind de verificacion de usuario y evitar que vuelva a escribir
@login_required
def check_user_testimonial(request):
    user = request.user
    has_testimonial = Testimoniales.objects.filter(usuario=user).exists()
    return JsonResponse({"has_testimonial": has_testimonial})


def anuncios(request):
    # query_result = Propiedades.objects.all()
    query_result = Propiedades.objects.filter(vendido=False)
    return render(request, "plantillas/anuncios.html", {"clave": query_result})


def anuncio_detalles(request, id):
    try:
        # busca el registro cuyo ID es igual al pasado por URL
        detail = Propiedades.objects.get(id=id)
    except Propiedades.DoesNotExist:
        # Si no existe ese ID lanza la excepcion DoesNotExist y capturada con un try-except
        raise Http404("La Propiedad no existe")

    return render(request, "plantillas/anuncio.html", {"details": detail})


def contacto(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Aquí puedes acceder a los datos del formulario validado
            nombre = form.cleaned_data["nombre"]
            email = form.cleaned_data["email"]
            telefono = form.cleaned_data["telefono"]
            mensaje = form.cleaned_data["mensaje"]

            # Aquí puedes hacer lo que quieras con los datos del formulario,
            # como enviar un correo electrónico, almacenarlos en la base de datos, etc.

            # Después de manejar los datos del formulario, puedes redirigir o renderizar una plantilla
            return render(request, "plantillas/contacto.html", {"success": True})
    else:
        initial_data = {
            "nombre": request.user.username if request.user.is_authenticated else ""
        }
        form = ContactForm(initial=initial_data)

    return render(request, "plantillas/contacto.html", {"formContacto": form})
