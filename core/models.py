from django.db import models
from django.contrib.auth.models import User

class Archivito(models.Model):
    nombre = models.CharField(max_length=1500)
    contenido = models.TextField()

    def __str__(self):
        return self.nombre

class HistorialTraducciones(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    cantidad_traducciones = models.IntegerField(default=0)
# Create your models here.
