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
    path('carro/form_pagar',views.form_pagar),
    path('pedido_completado', views.pedido_completado),
    path('atencion_al_cliente', views.atencion_al_cliente),
    path('terminos_del_servicio', views.terminos_del_servicio),
    path('politica_de_devolucion', views.politica_de_devolucion),
    path('aviso_de_privacidad', views.aviso_de_privacidad),
    
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

