from django.db import models
from django.utils import timezone

# Create your models here.

class Clientes(models.Model):
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    telefono = models.IntegerField()
    email = models.EmailField()
    fecha_alta = models.DateField(default=timezone.now)  # Valor por defecto: fecha actual

    # es opcional, ya que se mejora en el admin.py
    def __str__(self):
        return self.nombre


class Vendedores(models.Model):
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    telefono = models.IntegerField()
    email = models.EmailField()
    fecha_alta = models.DateField(default=timezone.now)
    # es opcional, ya que se mejora en el admin.py
    def __str__(self):
        return self.nombre


class Propiedades(models.Model):
    titulo = models.CharField(max_length=45)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.ImageField(upload_to="images/")  # null=True, blank=True => blank indica que el campo no es obligatorio
    descripcion = models.CharField(max_length=260)
    contentido = models.TextField()
    habitaciones = models.IntegerField()
    wc = models.IntegerField()
    garaje = models.IntegerField()
    fecha_alta = models.DateField(default=timezone.now)
    vendido = models.BooleanField(default=False)
    # es opcional, ya que se mejora en el admin.py
    def __str__(self):
        return self.titulo

    # cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, null=True, blank=True)
    # vendedor = models.ForeignKey(Vendedores, on_delete=models.CASCADE, null=True, blank=True)


""" Django requiere la biblioteca Pillow para manejar imágenes. 
Pillow es una biblioteca de procesamiento de imágenes para Python que Django utiliza para manejar campos de imagen """
# python -m pip install Pillow


class Ventas(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedores, on_delete=models.CASCADE)
    propiedad = models.ForeignKey(Propiedades, on_delete=models.CASCADE)
    fecha_venta = models.DateField(default=timezone.now)
    # es opcional, ya que se mejora en el admin.py
    def __str__(self):
        return self.cliente.nombre


class Propiedad_Vendedor(models.Model):
    propiedad = models.ForeignKey(Propiedades, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedores, on_delete=models.CASCADE)
    fecha_alta = models.DateField(default=timezone.now)

    # es opcional, ya que se mejora en el admin.py
    def __str__(self):
        return self.vendedor.nombre