from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.home),
    path('index', views.index),
    path('sobre_nosotros', views.sobre_nosotros),
] 