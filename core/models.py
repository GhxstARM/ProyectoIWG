from django.db import models

class Archivito(models.Model):
    nombre = models.CharField(max_length=1500)
    contenido = models.TextField()

    def __str__(self):
        return self.nombre

# Create your models here.
