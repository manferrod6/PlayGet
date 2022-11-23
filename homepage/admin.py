from django.contrib import admin

# Register your models here.

from .models import Producto
from .models import Carro
from .models import ItemCarro
from .models import Cliente

admin.site.register(Producto)
admin.site.register(Carro)
admin.site.register(ItemCarro)
admin.site.register(Cliente)