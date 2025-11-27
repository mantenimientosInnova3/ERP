from django.contrib import admin
from .models import Producto, OrdenCompra, DetalleOrden, CentroCosto

admin.site.register(Producto)
admin.site.register(OrdenCompra)
admin.site.register(DetalleOrden)
admin.site.register(CentroCosto)
