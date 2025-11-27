
# compras/views.py
from django.shortcuts import render, redirect
from .forms import ProductoForm
from .models import OrdenCompra, DetalleOrden, Producto
from .forms import OrdenCompraForm, DetalleOrdenForm
from django.http import HttpResponse
from django.db.models import Sum
from .models import CentroCosto
import csv
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import OrdenCompra, DetalleOrden
from decimal import Decimal
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RequisicionForm, DetalleRequisicionFormSet
from .models import Requisicion, DetalleRequisicion, OrdenCompra, DetalleOrden
from .forms import OrdenCompraForm
from django.contrib import messages

@login_required
def crear_requisicion(request):
    if request.method == 'POST':
        form = RequisicionForm(request.POST)
        formset = DetalleRequisicionFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            requisicion = form.save(commit=False)
            requisicion.usuario = request.user
            requisicion.save()
            detalles = formset.save(commit=False)
            for det in detalles:
                det.requisicion = requisicion
                det.save()
            return redirect('mis_requisiciones')
    else:
        form = RequisicionForm()
        formset = DetalleRequisicionFormSet()
    return render(request, 'compras/crear_requisicion.html', {'form': form, 'formset': formset})


@login_required
def home(request):
    usuario = request.user
    es_admin = usuario.is_superuser
    es_compras = usuario.groups.filter(name='Compras').exists()
    total_productos = Producto.objects.count()
    total_productos = Producto.objects.count()
    total_ordenes = OrdenCompra.objects.count()
    ultimas_ordenes = OrdenCompra.objects.order_by('-fecha')[:5]
    
    return render(request, 'compras/home.html', {
        'usuario': request.user,
        'es_admin': es_admin,
        'es_compras': es_compras,
        'total_productos': total_productos,
        'total_ordenes': total_ordenes,
        'ultimas_ordenes': ultimas_ordenes,
    })

def home(request):
    return render(request, 'compras/home.html', {
        'mensaje': '¡Probando la portada nueva!',
        'usuario': request.user
    })

@login_required
def mis_requisiciones(request):
    requisiciones = Requisicion.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'compras/mis_requisiciones.html', {'requisiciones': requisiciones})

def exportar_reporte_pdf(request):
    cc_data = []
    for cc in CentroCosto.objects.all():
        órdenes = OrdenCompra.objects.filter(centro_costo=cc)
        total_gasto = 0
        detalles = DetalleOrden.objects.filter(orden__in=órdenes)
        desglose = []
        for det in detalles:
            costo = det.cantidad * det.producto.precio
            total_gasto += costo
            desglose.append({
                'producto': det.producto.nombre,
                'cantidad': det.cantidad,
                'precio': det.producto.precio,
                'gasto': costo,
            })
        cc_data.append({
            'centro_costo': cc,
            'total_gasto': total_gasto,
            'detalles': desglose
        })
    total_general = sum(cc['total_gasto'] for cc in cc_data)
    template = get_template('compras/reporte_pdf.html')
    html = template.render({'cc_data': cc_data, 'total_general': total_general}, request)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_gastos.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generando PDF')
    return response


def exportar_reporte_excel(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    cc_id = request.GET.get('centro_costo')
    qs_ordenes = OrdenCompra.objects.all()
    if fecha_inicio:
        qs_ordenes = qs_ordenes.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        qs_ordenes = qs_ordenes.filter(fecha__lte=fecha_fin)
    if cc_id:
        qs_ordenes = qs_ordenes.filter(centro_costo__id=cc_id)

    cc_data = []
    for cc in CentroCosto.objects.all():
        if cc_id and str(cc.id) != cc_id:
            continue
        órdenes = qs_ordenes.filter(centro_costo=cc)
        detalles = DetalleOrden.objects.filter(orden__in=órdenes)
        for det in detalles:
            costo = det.cantidad * det.producto.precio
            cc_data.append([str(cc), det.producto.nombre, det.cantidad, det.producto.precio, costo])
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_gastos.csv"'
    writer = csv.writer(response)
    writer.writerow(['Centro de Costo', 'Producto', 'Cantidad', 'Precio', 'Gasto'])
    for row in cc_data:
        writer.writerow(row)
    return response


def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'compras/lista_productos.html', {'productos': productos})

def editar_producto(request, id):
    producto = Producto.objects.get(id=id)
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'compras/editar_producto.html', {'form': form})

def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)
    if request.method == "POST":
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'compras/eliminar_producto.html', {'producto': producto})


def agregar_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'compras/agregar_producto.html', {'form': form})

def agregar_orden_compra(request):
    if request.method == 'POST':
        orden_form = OrdenCompraForm(request.POST)
        detalle_form = DetalleOrdenForm(request.POST)
        if orden_form.is_valid() and detalle_form.is_valid():
            orden = orden_form.save()
            detalle = detalle_form.save(commit=False)
            detalle.orden = orden
            detalle.save()
            # Actualiza inventario del producto
            producto = Producto.objects.get(id=detalle.producto.id)
            producto.cantidad += detalle.cantidad
            producto.save()
            return redirect('lista_productos')
    else:
        orden_form = OrdenCompraForm()
        detalle_form = DetalleOrdenForm()
    return render(request, 'compras/agregar_orden.html', {
        'orden_form': orden_form,
        'detalle_form': detalle_form
    }) 
def lista_ordenes(request):
    ordenes = OrdenCompra.objects.all()
    return render(request, 'compras/lista_ordenes.html', {'ordenes': ordenes})

def reporte_gastos_centrocosto(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    cc_id = request.GET.get('centro_costo')
    qs_ordenes = OrdenCompra.objects.all()
    if fecha_inicio:
        qs_ordenes = qs_ordenes.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        qs_ordenes = qs_ordenes.filter(fecha__lte=fecha_fin)
    if cc_id:
        qs_ordenes = qs_ordenes.filter(centro_costo__id=cc_id)
    cc_data = []
    for cc in CentroCosto.objects.all():
        if cc_id and str(cc.id) != cc_id:
            continue
        órdenes = qs_ordenes.filter(centro_costo=cc)
        total_gasto = 0
        detalles = DetalleOrden.objects.filter(orden__in=órdenes)
        desglose = []
        for det in detalles:
            costo = det.cantidad * det.producto.precio
            total_gasto += costo
            desglose.append({
                'producto': det.producto.nombre,
                'cantidad': det.cantidad,
                'precio': det.producto.precio,
                'gasto': costo,
            })
        cc_data.append({
            'centro_costo': cc,
            'total_gasto': total_gasto,
            'detalles': desglose
        })
    total_general = sum(cc['total_gasto'] for cc in cc_data)
    return render(request, 'compras/reporte_gastos_centrocosto.html', {
        'cc_data': cc_data,
        'total_general': total_general,
        'centros_costo': CentroCosto.objects.all()
    })

def detalle_orden(request, id):
    orden = get_object_or_404(OrdenCompra, id=id)
    detalles = DetalleOrden.objects.filter(orden=orden)
    subtotal = sum(d.cantidad * d.precio_unitario for d in detalles)
    iva = subtotal * Decimal ('0.16')
    total = subtotal - orden.descuento + iva - orden.anticipo
    return render(request, 'compras/orden_compra_detalle.html', {
        'orden': orden,
        'detalles': detalles,
        'subtotal': subtotal,
        'iva': iva,
        'total': total,
    })

def es_compras(user):
    return user.groups.filter(name='Compras').exists() or user.is_superuser

@login_required
@user_passes_test(es_compras)
def requisiciones_pendientes(request):
    # Aquí puedes filtrar por estatus, área, etc. según tu lógica.
    requisiciones = Requisicion.objects.all().order_by('-fecha')
    return render(request, 'compras/requisiciones_pendientes.html', {'requisiciones': requisiciones})

def generar_orden_de_requisicion(request, id):
    requisicion = get_object_or_404(Requisicion, id=id)
    detalles = requisicion.detallerequisicion_set.all()
    
    if request.method == "POST":
        form = OrdenCompraForm(request.POST)
        if form.is_valid():
            orden = form.save()
            # Copiamos los detalles de la requisición a la orden de compra
            for partida in detalles:
                DetalleOrden.objects.create(
                    orden=orden,
                    producto=partida.producto,  # Usa ForeignKey si corresponde
                    cantidad=partida.cantidad
                )
            messages.success(request, "Orden de compra generada con éxito")
            return redirect('lista_ordenes')
    else:
        form = OrdenCompraForm()
    return render(request, 'compras/generar_orden_de_requisicion.html', {
        'requisicion': requisicion,
        'detalles': detalles,
        'form': form
    })