from django.http import Http404
from django.shortcuts import render
from home.models import *

def productos_detalle(request, id, slug):
    try: #para chequear que lo que vienepor la URL es válido
        datos=Producto.objects.filter(pk=id).filter(slug=slug).filter(estado_id=1).get()
    except Producto.DoesNotExist:
        raise Http404
    relacionados=Producto.objects.filter(estado_id=1, producto_categoria=datos.producto_categoria_id).filter(estado_id=1).all()
    fotos=ProductoFotos.objects.filter(producto_id=id).all()
    return render(request, 'productos/detalle.html', {'datos':datos, 'relacionados': relacionados, 'fotos':fotos})
