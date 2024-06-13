from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.http import JsonResponse
from chat.models import Room  # Importa el Room User de la app chat
from django.utils import timezone

# descorador para validar si el usuario esta autenticado
from django.contrib.auth.decorators import login_required

# Importamos los modelos o formularios
from .models import Blog
from .forms import BlogForm

# Create your views here.

def viewBlog(request):
    # Traemos la sala de chat
    ## => room = Room.objects.first()
    # Query de los blogs
    query_result = Blog.objects.all().order_by("-id")[:4]

    return render(
        request, "plantillas_blog/blog.html", {"clave": query_result} ## => , "room": room
    )


def viewBlogDetail(request, id):
    try:
        # busca el registro cuyo ID es igual al pasado por URL
        query_result = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        # Si no existe ese ID lanza la excepcion DoesNotExist y capturada con un try-except
        raise Http404("La publicación del blog no existe")

    return render(request, "plantillas_blog/blog_detail.html", {"blog_detail": query_result})


# descorador para validar si el usuario esta autenticado
@login_required
def viewCreateBlog(request):

    user = request.user

    # Verificar si el usuario ya tiene un blog escrito
    if Blog.objects.filter(usuario=user).exists():
        messages.error(request, "Ya has escrito un blog.")

    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if (form.is_valid()):  # valida  los campos del formulario, que no esten vacion, etc

            # Si el formulario es válido, guardamos el blog en la base de datos
            new_blog = form.save(commit=False)
            new_blog.nombre_titular = request.user.username  # Establecer el nombre del titular como el nombre de usuario autenticado
            new_blog.usuario = (request.user)
            new_blog.save()

            # Guarda el nuevo registro en BD
            new_blog = form.save()

            messages.success(request, "Publicacion creada con éxito!")
            # Redirecciona a un Url
            return redirect("namespaceblog:blog_details", id=new_blog.id)
    else:
        current_date = timezone.now().date()  # Obtener la fecha actual
        formatted_date = current_date.strftime("%Y-%m-%d")  # Formatear la fecha en el formato YYYY-MM-DD
        initial_data = {
            "nombre_titular": request.user.username,
            "fecha": formatted_date,
        }  # Establecer el valor inicial del campo nombre_titular como el nombre de usuario autenticado
        form = BlogForm(initial=initial_data)  # Pasar la fecha actual como valor inicial para el campo de fecha

    return render(request, "plantillas_blog/create_blog.html", {"registrar_blog": form})


# Endpoind de verificacion de usuario y evitar que vuelva a escribir
@login_required
def check_user_createBlog(request):
    user = request.user
    has_blog = Blog.objects.filter(usuario=user).exists()
    return JsonResponse({"has_blog": has_blog})
