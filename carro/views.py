from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from home.models import * 						# pegar decorators.py en /acceso
from acceso.decorators import logueado  		# decorador para validar usuario logueado o no
from utilidades import utilidades
import json
from django.conf import settings					# parece que para cargar los datos de webpay


@logueado() # inicio, va a buscar total registro en el carro, validación de suma y pasamos param a home
def carro_inicio(request):
    cuantos=Carrito.objects.filter(users_metadata_id=request.session['users_metadata_id']).count()
    datos=Carrito.objects.filter(users_metadata_id=request.session['users_metadata_id']).order_by('-id').all()
    suma=0
    for dato in datos:
        valor=dato.cantidad*dato.producto.precio
        suma=suma+valor
    return render(request, 'carro/home.html', {'datos':datos, 'suma':suma, 'cuantos':cuantos})


@logueado() #carro crear recibe una petición POST y recibe un id prod para rear reg en tabla carrito
def carro_crear(request):
    if request.method == 'POST':
        try:
            datos=Producto.objects.filter(pk=request.POST['id']).get()
        except Producto.DoesNotExist:
            raise Http404
        Carrito.objects.create(cantidad=request.POST['cantidad'], producto_id=request.POST['id'], users_metadata_id=request.session['users_metadata_id'])
        return HttpResponseRedirect("/carro")
    else:
        raise Http404
    
@logueado()
def carro_vaciar(request):
    Carrito.objects.filter(users_metadata_id=request.session['users_metadata_id']).delete()
    OrdenDeCompra.objects.filter(users_metadata_id=request.session['users_metadata_id']).filter(estado_id=3).delete()


    messages.add_message(request, messages.SUCCESS, f'Se vació tu carrito exitosamente!!!.')
    return HttpResponseRedirect('/carro')
'''
@logueado()
def carro_quitar(request, id):
    try:
        datos=Producto.objects.filter(pk=id).get()
    except Producto.DoesNotExist:
        raise Http404
    Carrito.objects.filter(users_metadata_id=request.session['users_metadata_id']).filter(producto_id=id).delete()
    messages.add_message(request, messages.SUCCESS, f'Se quitó el producto del carrito exitosamente!!!.')
    return HttpResponseRedirect('/carro')
    '''

@logueado()
def carro_quitar(request, id):
    try:
        datos = Producto.objects.filter(pk=id).get()
    except Producto.DoesNotExist:
        raise Http404
    
    # Lógica de siempre: borrar de la base de datos
    Carrito.objects.filter(users_metadata_id=request.session['users_metadata_id']).filter(producto_id=id).delete()
    
    # --- AQUÍ ESTÁ EL CAMBIO HTMX ---
    if request.htmx:
        # No mandamos mensaje de 'messages.add_message' porque no se verá sin recargar
        # Respondemos vacío para que HTMX elimine la fila de la tabla
        return HttpResponse("")

    # Si no es HTMX (comportamiento antiguo), mantenemos el redirect y el mensaje
    messages.add_message(request, messages.SUCCESS, f'Se quitó el producto del carrito exitosamente!!!.')
    return HttpResponseRedirect('/carro')

@logueado()
def carro_modificar_cantidad(request, id, cantidad):
    try:
        datos=Carrito.objects.filter(pk=id).get()
    except Carrito.DoesNotExist:
        raise Http404
    Carrito.objects.filter(id=id).update(cantidad=cantidad)
    messages.add_message(request, messages.SUCCESS, f'Se modificó la cantidad del producto {datos.producto.nombre} exitosamente!!!.')
    return HttpResponseRedirect('/carro')

@logueado()
def carro_pagar(request):
    cuantos=Carrito.objects.filter(users_metadata_id=request.session['users_metadata_id']).count()
    if cuantos==0:
        return HttpResponseRedirect('/carro')
    datos=Carrito.objects.filter(users_metadata_id=request.session['users_metadata_id']).order_by('-id').all()
    
    suma=0
    for dato in datos:
        valor=dato.cantidad*dato.producto.precio
        suma=suma+valor
    usuario=UsersMetadata.objects.filter(id=request.session['users_metadata_id']).get()
    comunas=Comuna.objects.all()
    return render(request, 'carro/pagar.html', {'datos': datos, 'suma': suma, 'usuario': usuario, 'comunas': comunas, 'cuantos': cuantos})