from home.models import *
from datetime import date
from django.utils.html import format_html
from utilidades import dreamhost

def getFechaActual():
	return date.today()
	
def get_perfiles_choices():
	return [
		(valve.pk, valve.nombre) for valve in Perfiles.objects.all()
	]
		
def get_paises_choices():
	return [
		(value.pk, value.nombre) for value in Pais.objects.all()
	]


def get_estados_choices():
	return [
		(value.pk, value.nombre) for value in Estado.objects.filter(id_in=[1,2]).all()
	]


def get_estados_obra_choices():
	return [
		(value.pk, value.nombre) for value in Estado.objects.filter(id__in=[3,4]).all()
	]


def get_generos_choices():
	return [
		(value.pk, value.nombre) for value in Genero.objects.all()]


def get_producto_categoria_choices():
	return [
		(value.pk, value.nombre) for value in ProductoCategoria.objects.all()]


def get_proveedor_choices():
	return [
		(value.pk, value.nombre) for value in Proveedor.objects.all()]

#def get_servicios_choices():
#	return [
#		(value.pk, value.nombre) for value in Servicios.objects.all()
#	]

#####HELPER MODELOS

def set_estado(obj):
	return obj.estado.nombre
set_estado.short_description = 'Estado'

def set_genero(obj):
	return obj.genero.nombre
set_genero.short_description = 'Genero'

def set_pais(obj):
	return obj.pais.nombre
set_pais.short_description = 'País'

def set_perfiles(obj):
	return obj.perfiles.nombre
set_perfiles.short_description = 'Perfil'

def set_user(obj):
	return f"{obj.user.first_name} {obj.user.last_name}"
set_user.short_description="Usuario"

def set_users_metadata(obj):
	return f"{obj.users_metadata.user.first_name} {obj.users_metadata.user.last_name}"
set_users_metadata.short_description = 'Usuario'



def set_producto_categoria(obj):
    return obj.producto_categoria.nombre
set_producto_categoria.short_description = 'Categoría'

def set_producto(obj):
	return obj.producto.nombre
set_producto.short_descriptin = 'Producto'

def set_correo(obj):
	return obj.user.username
set_correo.short_description = 'E-Mail'


def get_descripcion(obj):
    return format_html('<div style="word-wrap:break-word;width:200px;">{}......</div>', obj.descripcion[0:100])
get_descripcion.short_description = 'Descripción'


def get_foto_producto(obj):
    if dreamhost.existeArchivo('producto', obj.foto) == False:
        dreamhost.moverArchivoProducto(obj.foto, obj.id)
    
    # Definimos la ruta en una variable para no escribirla tantas veces
    ruta = f"/assets/upload/producto/{obj.foto}"
    
    # Pasamos 'ruta' dos veces para que rellene los dos juegos de llaves {}
    return format_html('<a href="{}" target="_blank"><img src="{}" width="100" height="100" /></a>', ruta, ruta)

get_foto_producto.short_description = "Foto"


def get_foto_producto_galeria(obj):
    if dreamhost.existeArchivo('producto', obj.foto) == False:
        dreamhost.moverArchivoProductoGaleria(obj.foto, obj.id)
    
    ruta = f"/assets/upload/producto/{obj.foto}"
    # El primer {} es para el enlace (href)
    # El segundo {} es para el texto que se ve (el nombre de la foto)
    return format_html('<a href="{}" target="_blank">{}</a>', ruta, obj.foto)

get_foto_producto_galeria.short_description = "Foto"
