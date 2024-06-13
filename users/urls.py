from django.urls import path  # path nos permite crear las urls que necesitemos
from . import views  # me traigo todas las vistas

## from django.contrib.auth import views as auth_views  # Importa las vistas de autenticación

app_name = "namespaceusers"

urlpatterns = [
    path("", views.viewLogin, name="login"),
    path("user-register", views.viewSignUp, name="user-register"),
    # path("login/", auth_views.LoginView.as_view(), name="login"),
]

# path("datos-usuario/", views.user_data_and_notes, name="user-dates"),
