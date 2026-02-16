from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from home.models import *												# importamos todo
from .forms import *  														# formularios que vamos a crear
from django.contrib.auth import authenticate, login, logout	# authenticate de Django para el login
from datetime import datetime, date, timedelta
from utilidades import utilidades
import time
from django.conf import settings										# para algunas configuraciones
from django.contrib.auth.hashers import make_password		


def acceso_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/') 								#validación si está logueado lo tiro a inicio
    form = Formulario_Login(request.POST or None)				#llamada al fomrulario login
    if request.method == 'POST':											#recibo valores via POST, los valido
        if form.is_valid():
            correo = request.POST['correo']								#obtengo user  y password
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
    pass

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