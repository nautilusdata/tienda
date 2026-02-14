from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('core/backend/', admin.site.urls),
    path('', include('home.urls'), name="home_urls"),
    #path('acceso/', include('acceso.urls'), name="acceso_urls"),
    #path('productos/', include('productos.urls'), name="productos_urls"),
    #path('carro/', include('carro.urls'), name="carro_urls"),
]
