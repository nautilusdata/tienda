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
	pass
