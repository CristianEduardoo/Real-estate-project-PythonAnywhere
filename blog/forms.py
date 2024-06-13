from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError

# OBLIGATORIO, si queremos que se registre en la DB, debemos inportar como en admin.py
from .models import Blog
from django.utils.html import escape  # para escapar codigo malisioso

from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile

# class BlogForm (forms.Form): => de formulario regular a PERSISTENTE
class BlogForm(forms.ModelForm):
    title = forms.CharField(
        label="Título del blog", 
        max_length=50,
        required=True,
    )
    nombre_titular = forms.CharField(
        label="Nombre del titular",
        max_length=50,
        required=False,
        # disabled=True,
    )
    img_jpg = forms.ImageField(
        label="Imagen JPG",
        widget=forms.FileInput(attrs={"accept": ".jpg"}),
    )
    img_webp = forms.ImageField(
        label="Imagen WEBP",
        widget=forms.FileInput(attrs={"accept": ".webp"}),
        required=False,
    )
    fecha = forms.DateField(
        label="Fecha",
        widget=forms.DateInput(attrs={"type": "date"}),
        disabled=True,
        initial=timezone.now().date(),  # Establece la fecha actual como valor inicial
    )
    descripcion = forms.CharField(label="Descripción", max_length=260, required=True)
    contenido = forms.CharField(label="Contenido", widget=forms.Textarea, required=True)

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title.split()) > 10:
            raise forms.ValidationError("El título no debe exceder las 10 palabras")
        return escape(title)

    # def clean_nombre_titular => por defecto de sesion

    def clean_descripcion(self):
        descripcion = self.cleaned_data["descripcion"].strip()
        if len(descripcion.split()) > 22:
            raise forms.ValidationError("La descripción no debe exceder las 22 palabras")
        return escape(descripcion)

    def clean_contenido(self):
        contenido = self.cleaned_data["contenido"].strip()
        return escape(contenido)

    def clean_img_jpg(self):
        img_jpg = self.cleaned_data.get("img_jpg")
        if img_jpg:
            if img_jpg.size > 100 * 1024:
                raise forms.ValidationError("La imagen JPG debe ser menor de 100 KB.")
            if not img_jpg.name.endswith(".jpg"):
                raise forms.ValidationError("La imagen JPG debe tener extensión .jpg")
            self._resize_image(img_jpg)
        return img_jpg

    def clean_img_webp(self):
        img_webp = self.cleaned_data.get("img_webp")
        if img_webp:
            if img_webp.size > 100 * 1024:
                raise forms.ValidationError("La imagen WEBP debe ser menor de 100 KB.")
            if not img_webp.name.endswith(".webp"):
                raise forms.ValidationError("La imagen WEBP debe tener extensión .webp")
            self._resize_image(img_webp)
        return img_webp

    def _resize_image(self, image_field):
        image = Image.open(image_field)
        original_width, original_height = image.size
        target_width, target_height = 600, 450

        # Primero redimensionar la imagen manteniendo el aspecto
        image.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)

        # Luego recortar la imagen centrada si no coincide con las dimensiones exactas
        left = (image.width - target_width) / 2
        top = (image.height - target_height) / 2
        right = (image.width + target_width) / 2
        bottom = (image.height + target_height) / 2

        image = image.crop((left, top, right, bottom))

        # Determinar el formato basado en la extensión del archivo
        extension = image_field.name.split('.')[-1].lower()
        format_dict = {'jpg': 'JPEG', 'jpeg': 'JPEG', 'webp': 'WEBP'}
        image_format = format_dict.get(extension, 'JPEG')

        image_io = io.BytesIO()
        image.save(image_io, format=image_format)
        image_file = InMemoryUploadedFile(image_io, None, image_field.name, image_format, image_io.tell, None)
        image_field.file = image_file

    def clean(self):
        cleaned_data = super().clean()
        img_jpg = cleaned_data.get("img_jpg")
        img_webp = cleaned_data.get("img_webp")

        if not img_jpg and not img_webp:
            raise ValidationError("Debe cargar al menos una imagen.")

        return cleaned_data

    class Meta:
        model = Blog
        fields = [
            "title",
            "nombre_titular",
            "img_jpg",
            "img_webp",
            "fecha",
            "descripcion",
            "contenido",
        ]


# def _resize_image(self, image_field):
#     image = Image.open(image_field)
#     original_width, original_height = image.size
#     target_width, target_height = 600, 450

#     # Calcular las proporciones de la imagen original y las dimensiones objetivo
#     original_ratio = original_width / original_height
#     target_ratio = target_width / target_height

#     # Si la proporción original es mayor que la proporción objetivo,
#     # significa que la imagen es más ancha, entonces cortamos los lados
#     if original_ratio > target_ratio:
#         new_width = int(target_ratio * original_height)
#         offset = (original_width - new_width) // 2
#         image = image.crop((offset, 0, offset + new_width, original_height))
#     # Si la proporción original es menor que la proporción objetivo,
#     # significa que la imagen es más alta, entonces cortamos la parte superior e inferior
#     elif original_ratio < target_ratio:
#         new_height = int(original_width / target_ratio)
#         offset = (original_height - new_height) // 2
#         image = image.crop((0, offset, original_width, offset + new_height))
#     # Si las proporciones son iguales, no hacemos ningún recorte

#     # Redimensionar la imagen
#     image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)

#     # Determinar el formato basado en la extensión del archivo
#     extension = image_field.name.split(".")[-1].lower()
#     format_dict = {"jpg": "JPEG", "jpeg": "JPEG", "webp": "WEBP"}
#     image_format = format_dict.get(extension, "JPEG")

#     image_io = io.BytesIO()
#     image.save(image_io, format=image_format)
#     image_file = InMemoryUploadedFile(
#         image_io, None, image_field.name, image_format, image_io.tell, None
#     )
#     image_field.file = image_file
