from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [ 
    path('', views.index),
    path('sobre_nosotros', views.sobre_nosotros),
    path('catalogo', views.catalogo),
    path('producto/<str:pk>', views.producto),
    path('carro', views.carro),
    path('anade_carro/<str:id_producto>/<int:numero_producto>', views.anade_carro, name='anade_carro'),
    path('decrease_cart/<str:id_producto>', views.remove_cart, name='remove_cart'),
    path('remove_cart/<str:id_producto>', views.decrease_cart, name='decrease_cart'),
    path('productos/<str:pk>', views.producto),
    path('servicios',views.servicios),
    path('pedido/<str:id_carrito>', views.hacer_pedido, name='hacer_pedido'),
    path('seguimiento', views.seguimiento, name="seguimiento"),
    path('seguir_pedido', views.seguir_pedido, name="seguir_pedido"),
    path('seguir_pedido?no_pedido/<str:id_pedido', views.seguir_pedido, name="no_pedido")
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

