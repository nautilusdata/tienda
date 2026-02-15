from django.urls import path
from .views import *                    #llamado a la vistas con las que vamos a trabajar

urlspatterns = [
path('login', acceso_login, name='acceso_login'),  #permite crear form para que user se pueda loguear
path('registri', acceso_registro, name='acceso_registro'),
path('salir', acceso_salir, name='acceso_salir'),
]
