from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .models import Carro
from .models import ItemCarro
from .forms import ClienteForm

from django.core.mail import send_mail
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

def sobre_nosotros(request):
    return render(request, 'homepage/sobre_nosotros.html')

def servicios(request):
    return render(request,'homepage/servicios.html')

def producto(request,pk):
    producto = Producto.objects.get(id=pk)

    producto.rango = [*range(1, producto.cantidad)]

    return render(request, 'homepage/producto.html',{'producto': producto })

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
        p.rango = [*range(1, p.cantidad)]


    return render(request, 'homepage/catalogo.html', 
        {'productos': productos, 
        'categorias': categorias, 
        'busqueda': busqueda}
    )

def carro(request, total=0, items_carro=None):
    try:
        carro = Carro.objects.get(id_carro=_id_carro(request))
        items_carro = ItemCarro.objects.filter(carro=carro, esta_activo=True)
        for item in items_carro:
            total += (item.producto.precio * item.cantidad)
    except :
        pass 

    context = {
        'total' : total,
        'items': items_carro,
    }

    return render(request, 'homepage/carro.html', context)

def _id_carro(request):
    carro = request.session.session_key
    if not carro:
        carro = request.session.create()
    return carro


def anade_carro(request, id_producto, numero_producto):
    producto = Producto.objects.get(id=id_producto)
    try:
        carro = Carro.objects.get(id_carro=_id_carro(request))
    except Carro.DoesNotExist:
        carro = Carro.objects.create(
            id_carro = _id_carro(request)
        )
        carro.save()

    try:
        item_carro = ItemCarro.objects.get(producto=producto, carro=carro)
        item_carro.cantidad += numero_producto
        item_carro.save()
    except ItemCarro.DoesNotExist:
        item_carro = ItemCarro.objects.create(
            producto = producto,
            cantidad = numero_producto,
            carro = carro,
        )
        item_carro.save()

    return redirect('/carro')


def decrease_cart(request, id_producto):
    carro = Carro.objects.get(id_carro=_id_carro(request))
    producto = get_object_or_404(Producto, id= id_producto)
    item_carro = ItemCarro.objects.get(producto=producto, carro=carro)

    if item_carro.cantidad > 1 :
        item_carro.cantidad -= 1
        item_carro.save()
    else:
        item_carro.delete()
    return redirect('/carro')

def remove_cart(request, id_producto):
    carro = Carro.objects.get(id_carro=_id_carro(request))
    producto = get_object_or_404(Producto, id= id_producto)
    item_carro = ItemCarro.objects.get(producto=producto, carro=carro)
    item_carro.delete()
    
    return redirect('/carro')


def form_pagar(request, total=0):
    try:
        carro = Carro.objects.get(id_carro=_id_carro(request))
    except Carro.DoesNotExist:
        return redirect('/carro')

    items_carro = ItemCarro.objects.filter(carro=carro, esta_activo=True)

    if items_carro.exists():
        for item in items_carro:
            total += (item.producto.precio * item.cantidad)
    else:
        return redirect('/carro')


    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            for item in items_carro:
                item.delete()

            #Hacer pedido
            #Envía correo
            msg = 'Gracias por comprar con nosotros.\nHas comprado:\n'
            for item in items_carro:
                msg+=str(item.producto.nombre + ' '+ str(item.cantidad)+'\n')
            msg += 'Importe total: '+str(total)+'€\n'
            msg += 'Dirección de entrega: '+ request.POST.get('direccion')
            send_mail(
                'Pedido completado!',
                msg,
                'playget131@gmail.com',
                [request.POST.get('correo')],
                fail_silently=False,
            )

            return redirect('/pedido_completado')


    context = {
        'form' : ClienteForm(),
        'total' : total,
        'items': items_carro,
    }

    return render(request, 'homepage/checkout.html', context)

def pedido_completado(request):
    return render(request, 'homepage/pedido_completado.html', {'msg':'Pedido completado'})

def atencion_al_cliente(request):
    return render(request,'homepage/atencion_al_cliente.html')


def terminos_del_servicio(request):
    return render(request,'homepage/terminos_del_servicio.html')


def aviso_de_privacidad(request):
    return render(request,'homepage/aviso_de_privacidad.html')


