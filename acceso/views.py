from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from home.models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, date, timedelta
from utilidades import utilidades
import time
from django.conf import settings
from django.contrib.auth.hashers import make_password

def acceso_login(request):
    pass

def acceso_registro(request):
    pass

def acceso_salir(request):
    logout(request)
    try:
        del request.session['users_metadata_id']
    except KeyError:
        pass
    messages.add_message(request, messages.WARNING, f'Se cerró la sesión exitosamente.')
    return HttpResponseRedirect('/acceso/login')
