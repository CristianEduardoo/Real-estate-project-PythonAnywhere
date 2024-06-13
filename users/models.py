from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField('email', unique=True)
    phone = models.IntegerField("phone", null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    

class Testimoniales(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.CharField(max_length=250)

    # es opcional, ya que se mejora en el admin.py
    def __str__(self):
        return self.usuario.username