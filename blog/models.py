from django.db import models
from django.utils import timezone
from users.models import User

# Create your models here.

# table Blog con sus campos title, img, nombre_titular, fecha, descripcion, contenido
class Blog(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    nombre_titular = models.CharField(max_length=50, null=True, blank=True)
    img_jpg = models.ImageField(upload_to="blog/", verbose_name="Imagen JPG") # null=True, blank=True => blank indica que el campo no es obligatorio
    img_webp = models.ImageField(upload_to="blog/", verbose_name="Imagen WEBP", null=True, blank=True)
    fecha = models.DateField(default=timezone.now)  # Valor por defecto: fecha actual
    descripcion = models.CharField(max_length=260)
    contenido = models.TextField()

    # Para tener una mejor visualizacion en la interfaz del admin
    # Es opcional, ya que se mejora en el admin.py
    def __str__(self):
        return self.title
    # Devuelve el nombre como su representación de cadena
    
    
    
# AQUI ES MEJOR USAR DIRECTAMENTE EL ResizedImageField(Size[600,600], quality=85, upload_to...)   