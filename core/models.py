from django.db import models
from django.contrib.auth.models import User

class Archivito(models.Model):
    nombre = models.CharField(max_length=1500)
    contenido = models.TextField()

    def __str__(self):
        return self.nombre

class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='archivos_usuario/')
# Create your models here.
