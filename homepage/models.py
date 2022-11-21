from django.db import models

# Create your models here.


class Producto(models.Model):
    # id = models.UUIDField()
    nombre   = models.TextField(max_length=200)
    descripcion = models.TextField(max_length=500)
    precio = models.PositiveIntegerField()
    fabricante = models.TextField(max_length=200)
    cantidad = models.PositiveIntegerField()
    categoria =  models.TextField(max_length=200)

    img = models.ImageField(upload_to="media")

    def __str__(self):
        return self.nombre

