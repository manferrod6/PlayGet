from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [ 
    path('', views.index),
    path('sobre_nosotros', views.sobre_nosotros),
    path('catalogo', views.catalogo),
    path('productos/<str:pk>', views.producto),
    path('carro', views.carro),
    path('anade_carro/<str:id_producto>', views.anade_carro, name='anade_carro'),
    path('remove_cart/<str:id_producto>', views.remove_cart, name='remove_cart'),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

