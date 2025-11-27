from django.db import models
from django.contrib.auth.models import User

class CentroCosto(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    sku = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre


class OrdenCompra(models.Model):
    fecha = models.DateField()
    proveedor = models.CharField(max_length=100)
    centro_costo = models.ForeignKey('CentroCosto', on_delete=models.CASCADE)
    consecutivo = models.CharField(max_length=50, blank=True)
    fecha_autorizacion = models.DateField(blank=True, null=True)
    condiciones_pago = models.TextField(blank=True)
    condiciones_entrega = models.TextField(blank=True)
    factura_folio = models.CharField(max_length=100, blank=True)
    criterios_aceptacion = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    anticipo = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.nombre

class DetalleOrden(models.Model):
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    unidad = models.CharField(max_length=20)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.CharField(max_length=200, blank=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    
    def __str__(self):
        return self.nombre

class Requisicion(models.Model):
    ESTADOS = [
        ("PENDIENTE", "Pendiente"),
        ("APROBADA", "Aprobada"),
        ("RECHAZADA", "Rechazada"),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    descripcion = models.CharField(max_length=200, blank=True)
    area = models.CharField(max_length=100)
    centro_costo = models.ForeignKey(CentroCosto, on_delete=models.CASCADE, null=True, blank=True)
    consecutivo = models.CharField(max_length=50, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default="PENDIENTE")
    fecha_autorizacion = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"REQ {self.consecutivo or self.id} - {self.usuario.username}"

class DetalleRequisicion(models.Model):
    requisicion = models.ForeignKey(Requisicion, on_delete=models.CASCADE, related_name="detalles")
    producto = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    unidad = models.CharField(max_length=20)
    observaciones = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.producto} x {self.cantidad}"