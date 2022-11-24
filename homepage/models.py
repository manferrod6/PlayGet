from django.db import models
from django.core.validators import RegexValidator

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
        self.producto.nombre


class Cliente(models.Model):
    nombre_completo = models.TextField(max_length=60)
    direccion = models.TextField(max_length=1000)
    codigo_postal = models.CharField(max_length=5,
        validators=[RegexValidator(regex='\d{5}', message='Length has to be 5', code='nomatch')])
    correo = models.EmailField(max_length=50)

    def __str__(self):
        return self.nombre_completo


