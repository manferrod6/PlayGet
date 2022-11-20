from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [ 
    path('', views.home),
    path('index', views.index),
    path('catalogo', views.catalogo),
    path('productos/<str:pk>', views.producto),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)