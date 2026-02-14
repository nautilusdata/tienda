import os
from os import remove
import shutil
from pathlib import Path
from datetime import datetime, date, timedelta
from django.conf import settings # llama a las rutas ruta1 ruta2 definidas en settings.py
#from home.models import Estado, Genero, Pais, Perfiles, UsersMetadata, ProductoCategoria, Producto, Metadata, Slide, ProductoFotos
from home.models import *

RUTA = settings.RUTA
RUTA2 = settings.RUTA2

#ya sabemos lo que hace
def moverArchivoProducto(file, id):
    nombre = "default.png"  # Assign a default value
    if existeArchivoMedia(file)==True:
        fecha = datetime.now()   												#crea variable fecha
        nombre = f"{datetime.timestamp(fecha)}{os.path.splitext(str(file))[1]}" #split extension
	    # mover de RUTA1 a RUTA2
        shutil.move(f'{RUTA}tienda/media/{file}', f'{RUTA2}assets/upload/producto/{nombre}')
        # filtro pregunta si el id=producto y update. Cambia el nombre en la base de datos.
    Producto.objects.filter(pk=id).update(foto=nombre) 

#ya sabemos lo que hace
def moverArchivoProducto2(file):
    shutil.move(f'{RUTA}tienda/media/producto/{file}', f'{RUTA2}assets/upload/producto/{file}')

#ya sabemos lo que hace
def existeArchivo(carpeta, archivo):
	try:
		ruta=f"{RUTA}tienda/assets/upload/{carpeta}/{archivo}"
		fileObj = Path(ruta)
		return fileObj.is_file()
	except Exception as e:
		return False

#ya sabemos lo que hace
def existeArchivoMedia(archivo):
	try:
		ruta=f"{RUTA}tienda/media/{archivo}"
		fileObj = Path(ruta)
		return fileObj.is_file()
	except Exception as e:
		return False

'''
Estructuralmente, el archivo está bien encaminado para un entorno de hosting, pero tiene un error lógico "invisible" que va a hacer que tu código intente mover el archivo mil veces (y falle a partir de la segunda).

Aquí te digo qué está bien y qué debes corregir para que no te dé dolores de cabeza:
Lo que está BIEN:

    La técnica del Timestamp: Usar datetime.timestamp(fecha) es perfecto. Evita que si dos usuarios suben foto.jpg, se borren entre sí.

    El uso de shutil.move: Es la forma correcta de mover archivos entre carpetas en Python.

    La limpieza de extensiones: Usar os.path.splitext para mantener el .jpg o .png original es lo correcto.

Lo que está MAL (y debes arreglar):
1. El bucle infinito en get_foto_producto

En tu archivo anterior de utilidades, tienes esto:
if dreamhost.existeArchivo('producto', obj.foto) == False: dreamhost.moverArchivoProducto(...)

Pero en dreamhost.py, la función existeArchivo busca en:
ruta = f"{RUTA}tienda/assets/upload/{carpeta}/{archivo}"

¿Ves el problema? Estás moviendo el archivo a RUTA2, pero lo estás buscando en RUTA.

    Resultado: La condición existeArchivo siempre será False.

    Consecuencia: Cada vez que abras el Admin, Django intentará mover un archivo que ya movió, y te dará un error de FileNotFoundError porque el archivo ya no está en la carpeta media original.

2. La importación de Modelos

Tienes from home.models import *. Esto en archivos de utilidades suele causar el error AppRegistryNotReady o importaciones circulares (Django se muerde la cola).
La versión "Blindada" de tu dreamhost.py:

Copia este código, que corrige los slashes y el error de las rutas:
Python

import os
import shutil
from pathlib import Path
from datetime import datetime
from django.conf import settings

# Las rutas de settings.py
RUTA = settings.RUTA
RUTA2 = settings.RUTA2

def moverArchivoProducto(file, id):
    # Importar aquí evita errores de carga de Django
    from home.models import Producto
    
    if existeArchivoMedia(file):
        fecha = datetime.now()
        nombre = f"{datetime.timestamp(fecha)}{os.path.splitext(str(file))[1]}"
        
        # Construcción segura de rutas
        origen = os.path.join(RUTA, 'tienda', 'media', str(file))
        destino = os.path.join(RUTA2, 'assets', 'upload', 'producto', nombre)
        
        try:
            # Creamos la carpeta de destino si no existe (por seguridad)
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            
            shutil.move(origen, destino)
            Producto.objects.filter(pk=id).update(foto=nombre)
            return nombre
        except Exception as e:
            print(f"Error al mover: {e}")
            return None

def existeArchivo(carpeta, archivo):
    try:
        # IMPORTANTE: Buscar en RUTA2, que es donde se movió el archivo
        ruta = os.path.join(RUTA2, 'assets', 'upload', carpeta, str(archivo))
        return Path(ruta).is_file()
    except:
        return False

def existeArchivoMedia(archivo):
    try:
        ruta = os.path.join(RUTA, 'tienda', 'media', str(archivo))
        return Path(ruta).is_file()
    except:
        return False

Conclusión:

Si dejas el archivo como lo tenías, funcionará solo la primera vez que subas la foto. La segunda vez que entres al Admin, el sistema se romperá porque buscará el archivo donde no está. Con mi corrección (usando os.path.join y buscando en RUTA2), el sistema será sólido como una roca.
'''
