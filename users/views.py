from django.contrib.auth import authenticate, login, get_backends
from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import JsonResponse

# descorador para validar si el usuario esta autenticado
from django.contrib.auth.decorators import login_required

from django.utils.html import escape  # Función escape para escapar codigo malisioso

# Importamos los modelos o formularios
# from .forms import SignUpUser
# OBLIGATORIO, si queremos que se registre en la DB de la tabla de usuario
from .models import User


# @login_required
def viewLogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # Verificar si el usuario es un superusuario
            if user.is_superuser:
                return JsonResponse({"redirect": "/"})  # Redirigir al panel de administración => /admin/
            else:
                return JsonResponse({"redirect": "/"})  # Redirigir a la página principal
        else:
            return JsonResponse({"error": "Credenciales inválidas"}, status=400)


def viewSignUp(request):
    if request.method == "POST":
        # Obtener los datos del formulario POST
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Escapa los datos antes de procesarlos
        username = escape(username)
        first_name = escape(first_name)
        last_name = escape(last_name)
        email = escape(email)
        phone = escape(phone)
        password1 = escape(password1)
        password2 = escape(password2)

        # Verificar si las contraseñas coinciden
        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect("namespaceusers:user-register")

        # Validar el correo electrónico
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "El correo electrónico no es válido.")
            return redirect("namespaceusers:user-register")

        # Convertir la primera letra del username a mayúsculas
        username = username.capitalize()

        # Crear un nuevo usuario con los datos del formulario
        user = User.objects.create_user(
            username=username, 
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=password1
        )

        # Especificar el backend y autenticar al usuario
        # backend = get_backends()[0]  # Usar el primer backend configurado
        backend = "django.contrib.auth.backends.ModelBackend"
        user.backend = backend

        # Autenticar al usuario después de registrarse
        login(request, user, backend=backend)

        # Redirigir al usuario a la página deseada
        return redirect("namespaceraices:main")

    return render(request, "registration/signup.html")
