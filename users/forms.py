from django import forms

# OBLIGATORIO, si queremos que se registre en la DB de la tabla de user
from .models import User

# Para dar de alta un usuario
from django.contrib.auth.forms import UserCreationForm
from django.utils.html import escape  # Para escapar codigo malisioso


class SignUpUser(UserCreationForm):
    username = forms.CharField(label="Nombre de usuario", max_length=30, required=True)
    email = forms.EmailField(
        label="Correo electrónico",
        max_length=30,
        required=True,
        # help_text="Required. Inform a valid email address.", solo funciona .as_p
    )
    phone = forms.IntegerField(
        label="Teléfono",
        widget=forms.NumberInput(
            attrs={"type": "tel", "placeholder": "Ingrese su teléfono"}
        ),
    )
    password1 = forms.CharField(
        label="Contaseña", 
        max_length=30, 
        widget=forms.PasswordInput, 
        required=True,
    )
    password2 = forms.CharField(
        label="Repita la contraseña",
        max_length=30,
        widget=forms.PasswordInput,
        required=True
    )

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if len(username) < 4:
            raise forms.ValidationError(
                "El nombre de usuario debe tener al menos 4 caracteres"
            )
        return escape(username)

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        if not email.endswith(".com"):
            raise forms.ValidationError(
                "El correo electrónico debe ser de dominio example@example.com"
            )
        return escape(email)

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        return escape(phone)

    def clean_password1(self):
        password = self.cleaned_data["password1"]
        if len(password) < 8:
            raise forms.ValidationError(
                "La contraseña debe tener al menos 8 caracteres."
            )
        return escape(password)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.") # excepciones de validación
        return password2

    class Meta:
        # Modelo al que está asociado el formulario
        model = User

        # Campos que se deben incluir en el formulario
        fields = ["username", "email", "phone", "password1"]

        # Define las etiquetas para los campos del formulario
        labels = {
            "username": "Nombre de usuario",
            "email": "Correo electrónico",
            "phone": "Ingrese su teléfono",
            "password1": "Contraseña",
        }
