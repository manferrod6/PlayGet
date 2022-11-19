from django.shortcuts import render
from .models import Producto
from django.db.models import Q

# Create your views here.

categorias = [
            'Aire libre',
            'Videojuegos',
            'Juegos de Mesa',
            'Puzzles y Construcciones',
            'Instrumentos Musicales',
            'Electronicos',
            ]
    
def home(request):
    return render(request, 'homepage/index.html')

def index(request):
    return render(request, 'homepage/index.html')

def catalogo(request):
    tipoBusqueda = request.GET.get('tipo-busqueda','')
    busqueda = request.GET.get('busqueda','')
    filtros = request.GET.get('filtros','')
    arr = filtros.split(';')
    
    if filtros == '':
        if busqueda == '':
                productos = Producto.objects.all()
        else:
            if tipoBusqueda == 'nombre':
                productos = Producto.objects.filter(nombre__icontains = busqueda)
            elif tipoBusqueda == 'fabricante':
                productos = Producto.objects.filter(fabricante__icontains = busqueda) 
    else:
        if busqueda == '':
            productos = Producto.objects.filter(categoria__in = arr)
        else:
            if tipoBusqueda == 'nombre':
                productos = Producto.objects.filter(Q(nombre__icontains = busqueda) & Q(categoria__in = arr))
            elif tipoBusqueda == 'fabricante':
                productos = Producto.objects.filter(Q(fabricante__icontains = busqueda) & Q(categoria__in = arr))
    




    for p in productos:
        p.cantidad = [*range(1, p.cantidad)]



    return render(request, 'homepage/catalogo.html', 
        {'productos': productos, 
        'categorias': categorias, 
        'busqueda': busqueda}
    )
