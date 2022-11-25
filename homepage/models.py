from django.db import models
from django.core.validators import RegexValidator

from datetime import timedelta


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

class Pedido(models.Model):
    id  = models.CharField(max_length=8,unique=True,primary_key=True)
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE)

    fecha_pedido = models.DateTimeField(auto_now_add=True)

    def fecha_entrega(self):
        return self.fecha_pedido + timedelta(days=5)
    
    PENDIENTE = 'PEN'
    ENVIADO = 'ENV'
    ENTREGADO = 'ENT'
    ESTADOS = [
        (PENDIENTE, 'Pendiente de envio'),
        (ENVIADO, 'Enviado'),
        (ENTREGADO, 'Pedido entregado')
    ]

    estado = models.CharField(max_length=3,choices=ESTADOS, default=PENDIENTE)

    def __str__(self):
        self.id
    
class ItemPedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def sub_total(self):
        return self.cantidad * self.producto.precio

    def __str__(self):
        self.producto

        self.producto.nombre


class Cliente(models.Model):
    nombre_completo = models.TextField(max_length=60)
    direccion = models.TextField(max_length=1000)
    codigo_postal = models.CharField(max_length=5,
        validators=[RegexValidator(regex='\d{5}', message='Length has to be 5', code='nomatch')])
    correo = models.EmailField(max_length=50)

    def __str__(self):
        return self.nombre_completo



