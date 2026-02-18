from django.urls import path
from .views import *

urlpatterns = [
    path('', carro_inicio, name="carro_inicio"),
    path('crear', carro_crear, name="carro_crear"),   							# +creando registros en el carrito
    path('vaciar', carro_vaciar, name="carro_vaciar"),
    path('quitar-de-carro/<int:id>', carro_quitar, name=”carro_quitar”),
]
