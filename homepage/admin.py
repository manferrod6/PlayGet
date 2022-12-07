from django.contrib import admin

# Register your models here.

from .models import Producto
from .models import Cliente
from .models import Pedido
from .models import Carro
from .models import ItemCarro
from .models import ItemPedido



admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(Carro)
admin.site.register(ItemCarro)
admin.site.register(ItemPedido)