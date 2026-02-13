from django.db import models							# estandar
from django.contrib.auth.models import User		# extender el modelo de usuario
from autoslug import AutoSlugField					# se crean los slugs auutomáticamente
from datetime import datetime, date				# datetime

# para los estados de la orden de compra
class Estado(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'estado'
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

# estandar
class Genero(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'genero'
        verbose_name = 'Género'
        verbose_name_plural = 'Géneros'

# Paises
class Pais(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'pais'
        verbose_name = 'País'
        verbose_name_plural = 'Países'


class Perfiles(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'perfiles'
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'


class Region(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'region'
        verbose_name = 'Región'
        verbose_name_plural = 'Regiones'


class Comuna(models.Model):
    id = models.AutoField(primary_key=True)
    region = models.ForeignKey(Region, models.DO_NOTHING, default=1)
    nombre = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'comuna'
        verbose_name = 'Comuna'
        verbose_name_plural = 'Comunas'

# la tabla UsersMetadata permite extender el modelo de user
class UsersMetadata(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    estado = models.ForeignKey(Estado, models.DO_NOTHING)
    genero = models.ForeignKey(Genero, models.DO_NOTHING)
    perfiles = models.ForeignKey(Perfiles, models.DO_NOTHING)
    pais = models.ForeignKey(Pais, models.DO_NOTHING)
    comuna = models.ForeignKey(Comuna, models.DO_NOTHING)
    slug = models.CharField(max_length=100, null=True)
    correo = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'Metadata de {self.user.username}'

    class Meta:
        db_table = 'users_metadata'
        verbose_name = 'Metadata de Usuario'
        verbose_name_plural = 'Metadatos de Usuarios'

# para crear/configurar “carrusel” de imágenes en el hero (opcional)
class Slide(models.Model):
    id = models.AutoField(primary_key=True)
    foto = models.ImageField(upload_to="slide", default='edificacion.png')
    link = models.CharField(max_length=100, blank=True, null=True)
    titulo = models.CharField(max_length=100, blank=True, null=True)
    target = models.PositiveIntegerField(default=0) #con click se queda en pestaña o abre nueva

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = 'slide'
        verbose_name = 'Slide'
        verbose_name_plural = 'Slides'


class Proveedor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    slug = AutoSlugField(populate_from='nombre')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'proveedor'
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'


class ProductoCategoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    slug = AutoSlugField(populate_from='nombre')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'producto_categoria'
        verbose_name = 'Producto Categoria'
        verbose_name_plural = 'Productos Categorías'


class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    slug = AutoSlugField(populate_from='nombre')
    descripcion = models.TextField()
    producto_categoria = models.ForeignKey(ProductoCategoria, models.DO_NOTHING)
    proveedor = models.ForeignKey(Proveedor, models.DO_NOTHING)
    estado = models.ForeignKey(Estado, models.DO_NOTHING)
    foto = models.ImageField(upload_to="producto", default='200_200.png') #la de la pag nav
    fecha = models.DateField(auto_now_add=True)
    precio = models.PositiveIntegerField(default=0)
    precio_antes = models.PositiveIntegerField(default=0) # ambos precios como gancho de la caja
    sku = models.CharField(max_length=100, blank=True, null=True, default='1')
    stock = models.PositiveIntegerField(default=1) # para hacer validaciones en la interfaz gráfica

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

#N fotos DETALLE, una tabla que guarda el id del produto y la foto (one to many)
class ProductoFotos(models.Model): 
    id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, models.DO_NOTHING)
    foto = models.ImageField(upload_to="producto", default='200_200.png')

    def __str__(self):
        return self.producto.nombre

    class Meta:
        db_table = 'producto_fotos'
        verbose_name = 'Producto fotos'
        verbose_name_plural = 'Productos Fotos'

# va guardando los items del carrito. Guardar en tabla PERO usuario debe estar logueado (CON)
class Carrito(models.Model):
    producto = models.ForeignKey(Producto, models.DO_NOTHING)
    users_metadata = models.ForeignKey(UsersMetadata, models.DO_NOTHING, default=1)
    cantidad = models.PositiveIntegerField(default=0)
    fecha = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.cantidad} de {self.producto.nombre} en el carrito de {self.users_metadata.user.username}'

    class Meta:
        db_table = 'carrito'
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carrito'


# quien hizo la orden, estado, comuna, token que entrega Transbank, el N tarjeta (4 últimos dígitos), etc, etc....
class OrdenDeCompra(models.Model):
    users_metadata = models.ForeignKey(UsersMetadata, models.DO_NOTHING,default=1)
    estado = models.ForeignKey(Estado, models.DO_NOTHING, default=3)
    comuna = models.ForeignKey(Comuna, models.DO_NOTHING, default=1)
    token_ws = models.CharField(max_length=255, default=0)
    tarjeta = models.CharField(max_length=10, default='0')
    fecha_transbank = models.CharField(max_length=100, default='0')
    estado_transbank = models.CharField(max_length=100, default='0') #peticiones transbank
    suma = models.PositiveIntegerField()
    direccion = models.TextField(default='0')
    observaciones = models.TextField(default='')
    fecha = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"N. {self.id}"

    class Meta:
        db_table = 'orden_de_compra'
        verbose_name = 'Orden de compra'
        verbose_name_plural = 'Órdenes de compra'

# por si se quiere una estructura de encabezado de orden de compra
class OrdenDeCompraDetalle(models.Model): 
    orden_de_compra = models.ForeignKey(OrdenDeCompra, models.DO_NOTHING)
    producto = models.ForeignKey(Producto, models.DO_NOTHING, default=1)
    cantidad = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"N. {self.id}"
    
    class Meta:
        db_table = 'orden_de_compra_detalle'
        verbose_name = 'Orden de compra detalle'
        verbose_name_plural = 'Órdenes de compra detalle'


class Metadata(models.Model):							
    keyword = models.CharField(max_length=255, blank=True, null=True)
    nombre = models.CharField(max_length=255,  blank=True, null=True)					
    description = models.TextField(default='0')
    correo = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.correo

    class Meta:
        db_table = 'metadata'
        verbose_name = 'Metadata'
        verbose_name_plural = 'Metadata'   
