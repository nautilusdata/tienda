from datetime import datetime, date, timedelta
from django.conf import settings
import os
from os import remove
from urllib.parse import urlparse, parse_qs
from django.core.paginator import Paginator
from django.template import Context, Template
#token
import jwt
import time
#email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django import template

# método para crear el token
def getToken(json):
	token = jwt.encode(json, settings.SECRET_KEY, algorithm='HS256')
	return token
	
# método para traducir en token
def traducirToken(token):
	return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
	
# método para generar el envío del mail al través de SMTP con los datos del config
def sendMail(html, asunto, para):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = asunto
    msg['From'] = settings.MAIL_SALIDA
    msg['To'] = para
    
    msg.attach(MIMEText(html, 'html'))
    try:
        server = smtplib.SMTP(settings.SERVER_SMTP, settings.PUERTO_SMTP)
        server.starttls() # <--- AGREGA ESTA LÍNEA (Es vital para el puerto 587)
        server.login(settings.MAIL_SALIDA, settings.PASSWORD_MAIL_SALIDA)
        server.sendmail(settings.MAIL_SALIDA, para, msg.as_string())
        server.quit()
        print("¡Correo enviado exitosamente!") # Para que lo veas en tu terminal
    except Exception as e:
        print(f"Error al enviar correo: {e}") # <--- ESTO te dirá la verdad en la terminal
		
# método validador de  extensiones
def getExtension(file):
	extension = os.path.splitext(str(file))[1]
	if extension == ".png":
		return True
	if extension == ".jpg":
		return True
	if extension == ".jpeg":
		return True
	if extension == ".JPG":
		return True
	if extension == ".JPEG":
		return True
	else:
		return False	
		
# paginación no se usará en en la tienda pero igual se deja acá
def get_paginacion(total, request): #total es un recorset a la DB y objeto request para proc param url
	page = request.GET.get('page') # Esto retorna una lista en return
	paginator = Paginator(total, settings.TOTAL_PAGINAS) #definido en settings.py
	datos = paginator.get_page(page) #usamos la instancia paginator de la liena anterior y llamamos get_page #parametro que viene de la url.
	numeros=[]
	if len(datos) >= settings.TOTAL_PAGINAS: #si el largo de datos es > settings.TOTAL_PAG...
		for ultima in range(1, datos.paginator.num_pages): #num_page numero total se paginas
			numeros.append(ultima)  #agregar a la lista los valores que va tomando el for dinámico
		numeros.append(ultima+1)    #agregar la ultima pagina que va a cargar

	return [datos, numeros, page]   #cargamos dato, cargamos numeros y cargamos page. SE CORRIGIO A INT EN capitulo 56, Creación de Buscador.
	
# esta la usaremos más en  elarchivo templatetags personalizado pero igual está acá por si hay que validar algo
def numberFormat(numero):
	if numero == None:
		return 0
	else:
		return "{:,}".format(numero).replace(",",".")
