import os
from PlayGet.settings import STATICFILES_DIRS
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .models import Carro
from .models import ItemCarro

from .models import Pedido
from .models import ItemPedido
from datetime import *

from .forms import ClienteForm
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
import braintree
from django.http import HttpResponse
import json

from homepage.mixins import (
    gateway,
    BraintreeAccount,
    BraintreePayment,
    BraintreeData,
    generate_client_token,
    transact,
    find_transaction,
    )

import random
import string

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
        'carrito': carro,
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

def _id_pedido():
    letras = ''.join(random.sample(string.ascii_uppercase,3))
    numeros = random.randint(11111,99999)
    numeros_format = str(numeros)
    res = letras + numeros_format

    try:
        Pedido.objects.get(id=res)
        res = _id_pedido()
    except :
        pass
    
    return res

def seguimiento(request):
    return render(request, 'homepage/seguimiento.html')

def seguir_pedido(request, total=0):
    id_pedido = request.GET.get('id_pedido', '')
    if id_pedido != '':
        
        pedido = get_object_or_404(Pedido, id= id_pedido)
        items_pedido = ItemPedido.objects.filter(pedido=pedido)
        for item in items_pedido:
            total += (item.producto.precio * item.cantidad)
        fecha_entrega = pedido.fecha_entrega()
        context = {
            'total' : total,
            'items': items_pedido,
            'pedido': pedido,
            'fecha_entrega': fecha_entrega
        }
            
        
    return render(request, 'homepage/pedido.html', context)


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

            #Hacer pedido
            
            id_pedido = _id_pedido()
            pedido = Pedido.objects.create(id=id_pedido,carro=carro,estado='PENDIENTE')
            pedido.save()
            items_pedido = []
            for item in items_carro:
                total += (item.producto.precio * item.cantidad)
                item_pedido = ItemPedido.objects.create(
                    producto = item.producto,
                    pedido = pedido,
                    cantidad = item.producto.cantidad
                )
                items_pedido.append(item_pedido)
                item.delete()
            #Envía correo
            msg = 'Gracias por comprar con nosotros.\nHas comprado:\n'
            for item in items_carro:
                msg+=str(item.producto.nombre + ' '+ str(item.cantidad)+'\n')
            msg += 'Su ID de seguimiento de pedido es: ' + str(id_pedido)+'\n'
            msg += 'Importe total: '+str(total)+'€\n'
            msg += 'Dirección de entrega: '+ request.POST.get('direccion')
            send_mail(
                'Pedido completado!',
                msg,
                'playget131@gmail.com',
                [request.POST.get('correo')],
                fail_silently=False,
            )

            agent_account=gateway.customer.find('870104067')
            agent_account_id=agent_account.id

            collection = gateway.customer.search([
                braintree.CustomerSearch.email == request.POST.get('correo')
            ])
            suma=0
            for c in collection:
                suma+=1
            if suma==0:
                agent_account = gateway.customer.create({"email": request.POST.get('correo')})
                agent_account_id = agent_account.customer.id
            else:
                for customer in collection:
                    agent_account_id = customer.id
            
            checkbox=''
            if(request.POST.get('checkbox')):
                braintree_client_token = gateway.client_token.generate({"customer_id": agent_account_id})
                checkbox='True'
            else:
                braintree_client_token = gateway.client_token.generate()

            context = {
                "braintree_client_token": braintree_client_token,
                "direccion":request.POST.get('direccion'),
                "correo":request.POST.get('correo'),
                "customer_id":agent_account_id,
                "checkbox":checkbox,
            }
            return render(request,'homepage/pasarela_pago.html', context)


    context = {
        'form' : ClienteForm(),
        'total' : total,
        'items': items_carro,
    }

    return render(request, 'homepage/checkout.html', context)

def pedido_completado(request):
    return render(request, 'homepage/pedido_completado.html', {'msg':'Pedido completado'})



'''
AJAX function to handle a Braintree payment
'''
def payment(request,total=0):

    if request.method == "POST":

        token = ''
        card_id = request.POST.get("card_id", None)
        paymentMethodNonce = request.POST.get("paymentMethodNonce", None)
        description = request.POST.get("description", None)
        currency = request.POST.get("currency", None)
        set_default = request.POST.get("set_default", None)
        agent_account_id=request.POST.get("customer_id",None)



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

        if (request.POST.get('checkbox')=='True'):
            token = request.POST.get('braintreeToken',None)
            gateway.customer.update(agent_account_id,{"payment_method_nonce":paymentMethodNonce})
            BraintreePayment(
                agent_id=agent_account_id,
                token=token,
                card_id=card_id,
                amount=total,
                description = description,
                currency=currency,
                set_default=set_default
                ).create()    
        else:
            transact({
                "amount": total,
                "payment_method_nonce":paymentMethodNonce,
                "customer_id": agent_account_id,
                'options': {
				"submit_for_settlement": True
			}
            })
        
        

        for item in items_carro:
                item.delete()

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

        return HttpResponse(
            json.dumps({"result": "okay"}),
            content_type="application/json"
            )

    else:
        return HttpResponse(
            json.dumps({"result": "error"}),
            content_type="application/json"
            )

            

def atencion_al_cliente(request):
    return render(request,'homepage/atencion_al_cliente.html')


def terminos_del_servicio(request):
    return render(request,'homepage/terminos_del_servicio.html')


def aviso_de_privacidad(request):
    return render(request,'homepage/aviso_de_privacidad.html')

def politica_de_devolucion(request):
    staticpath = STATICFILES_DIRS[0]
    path = os.path.join(staticpath, 'Politica-de-devoluciones.pdf')
    print(path)
    with open(path, 'rb') as pdf:   
        response = HttpResponse(pdf.read(), content_type='/politica_de_devolucion')
        response['Content-Disposition'] = 'inline;filename=Politica_de_devolucion.pdf'
        return response
    pdf.closed
