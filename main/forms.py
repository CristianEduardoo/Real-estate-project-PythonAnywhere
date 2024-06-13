from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.html import escape

# OBLIGATORIO, si queremos que se registre en la DB, debemos inportar como en admin.py
from users.models import Testimoniales


class ContactForm(forms.Form):
    # ======== Campos de información personal ========
    nombre = forms.CharField(
        label="Nombre completo",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Ingrese su nombre"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "Ingrese su email"}),
    )
    telefono = forms.IntegerField(
        label="Teléfono",
        widget=forms.NumberInput(
            attrs={"type": "tel", "placeholder": "Ingrese su teléfono"}
        ),
    )
    mensaje = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(
            attrs={"placeholder": "Escriba un breve mensaje"}
        ),
    )

    # ======== Campos de información sobre la propiedad ========
    # venta_compra_choices = [
    #     ("", "--Seleccione una opción--"),
    #     ("vender", "Vendo"),
    #     ("comprar", "Compro"),
    # ]
    # venta_compra = forms.ChoiceField(
    #     label="Vende o Compra", choices=venta_compra_choices, initial="", required=False
    # )
    # presupuesto = forms.DecimalField(
    #     label="Precio o presupuesto",
    #     min_value=0,
    #     widget=forms.NumberInput(attrs={"placeholder": "2,000,000"}),
    #     required=False,
    # )

    # ======== Campos de método de contacto ========
    # contacto_choices = [
    #     ("", "--Seleccione una opción--"),
    #     ("telefono", "Teléfono"),
    #     ("email", "Email"),
    # ]
    # contacto = forms.ChoiceField(
    #     label="¿Cómo desea ser contactado?", choices=contacto_choices, initial=""
    # )
    # fecha = forms.DateField(
    #     label="Fecha",
    #     widget=forms.DateInput(attrs={"type": "date"}),
    #     required=False,
    # )
    # hora = forms.TimeField(
    #     label="Hora",
    #     widget=forms.TimeInput(
    #         attrs={
    #             "type": "time",
    #             "min": "09:00",
    #             "max": "18:00",
    #         }
    #     ),
    #     required=False,
    # )

    # Definir fieldsets como una lista de tuplas
    fieldsets = [
        ("Información personal", ["nombre", "email", "telefono", "mensaje"]),
        # ("Información sobre la propiedad", ["venta_compra", "presupuesto"]),
        # ("Método de contacto", ["contacto", "fecha", "hora"]),
    ]

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()
        return escape(nombre)

    def clean_email(self):
        email = self.cleaned_data.get("email").strip()
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Por favor, ingrese un correo electrónico válido.")
        return escape(email)

    def clean_telefono(self):
        telefono = self.cleaned_data["telefono"]
        return escape(telefono)

    def clean_mensaje(self):
        mensaje = self.cleaned_data["mensaje"].strip()
        return escape(mensaje)


class TestimonialForm(forms.ModelForm):

    contenido = forms.CharField(label="Contenido", widget=forms.Textarea, required=True)

    def clean_contenido(self):
        contenido = self.cleaned_data["contenido"].strip()
        max_words = 20  # define la cantidad máxima de palabras permitidas
        if len(contenido.split()) > max_words:
            raise forms.ValidationError(
                f"El contenido no puede tener más de {max_words} palabras"
            )
        return escape(contenido)

    class Meta:
        model = Testimoniales
        fields = [
            "contenido"
        ]
