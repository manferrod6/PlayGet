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

class Carro(models.Model):
    id_carro = models.CharField(max_length=250, blank=True)
    fecha_añadido = models.DateField(auto_now_add=True)

    def __str__(self):
        self.id_carro


class ItemCarro(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    esta_activo = models.BooleanField(default=True)

    def sub_total(self):
        return self.cantidad * self.producto.precio

    def __str__(self):
        self.producto
