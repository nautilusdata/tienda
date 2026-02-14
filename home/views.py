from django.shortcuts import render
from home.models import *

def home_inicio(request): 
	#SELECT *FROM productos where estado id=1 order by id desc limit 8    (recordar: estado id1=Activos)
    datos=Producto.objects.filter(estado_id=1).order_by('-id').all()[:8]
    return render(request, 'home/home.html', {'datos':datos})
