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
