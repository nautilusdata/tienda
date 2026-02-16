from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from home.models import *										# importamos todo
from .forms import *  										    # formularios que vamos a crear
from django.contrib.auth import authenticate, login, logout	    # authenticate de Django para el login
from datetime import datetime, date, timedelta
from utilidades import utilidades
import time
from django.conf import settings								# para algunas configuraciones
from django.contrib.auth.hashers import make_password
from slugify import slugify		


def acceso_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/') 						#validación si está logueado lo tiro a inicio
    form = Formulario_Login(request.POST or None)				#llamada al formulario login
    if request.method == 'POST':								#recibo valores via POST, los valido
        if form.is_valid():
            correo = request.POST['correo']						#obtengo user y password
            password = request.POST['password']
            user = authenticate(request, username=correo, password=password)
        if user is not None:
            login(request, user)
            usersMetadata = UsersMetadata.objects.filter(user_id=request.user.id).get()
            request.session['users_metadata_id'] = usersMetadata.id
            return HttpResponseRedirect('/')
        else:
            messages.add_message(request, messages.WARNING, f'Los datos ingresados no son correctos, por favor vuelva a intentar.')
            return HttpResponseRedirect('/acceso/login')
    return render(request, 'acceso/login.html',{'form':form})

def acceso_registro(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    form = Formulario_Registro(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            existe=User.objects.filter(username=request.POST['correo']).count() #existe un usuario con ese correo?
            if existe !=0: #si existe, mensaje de error y redirijo a registro
                mensaje = f"Mail en uso por otro usuario. Intente con otro." #mensaje de error
                messages.add_message(request, messages.WARNING, mensaje) #mensaje de error
                return HttpResponseRedirect('/acceso/registro') #si existe, mensaje de error y redirijo a registro
            else: #recordar que debemos registrar al usuario en la tabla de User y en la tabla de UsersMetadata
                u=User.objects.create_user(username = request.POST['correo'], password = request.POST['password'], email = request.POST['correo'], first_name=request.POST['nombre'], last_name=request.POST['apellido'], is_active=0)
                UsersMetadata.objects.create(correo=request.POST['correo'], telefono='', direccion='', estado_id=2, pais_id=1, perfiles_id=1, user_id=u.id, genero_id=3, slug = slugify(nombre))
                ahora = datetime.now()
                fecha = datetime.strptime(f"{ahora.year}-{ahora.month}-{ahora.day}", "%Y-%m-%d")
                nombre = f"{request.POST['nombre']}-{request.POST['apellido']}"
                token=utilidades.getToken({'id': u.id, 'time':int(time.time())})
                url=f"{settings.BASE_URL}acceso/verificacion/{token}"
                html=f"""Hola {nombre}. Gracias por registrarte en nuestra plataforma.<br>Para completar tu registro, por favor haz clic en el siguiente enlace:<br><a href="{url}">{url}</a><br><br>Si no te has registrado en nuestra plataforma, por favor ignora este mensaje.<br><br>Saludos cordiales,<br>El equipo de Soporte."""
    return render(request, 'acceso/registro.html', {'form': form})

def acceso_salir(request):
    logout(request)
    try:
        #del request.session['perfiles_id']
        #del request.session['perfiles']
        #del request.session['estado_id']
        del request.session['users_metadata_id']
    except KeyError:
        pass
    messages.add_message(request, messages.WARNING, f'Se cerró la sesión exitosamente.')
    return HttpResponseRedirect('/acceso/login')