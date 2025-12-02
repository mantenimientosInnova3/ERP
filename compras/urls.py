from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Productos
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('productos/<int:id>/movimientos/', views.movimientos_producto, name='movimientos_producto'),

    # Órdenes de compra
    path('ordenes/agregar/', views.agregar_orden_compra, name='agregar_orden'),
    path('ordenes/', views.lista_ordenes, name='lista_ordenes'),
    path('ordenes/detalle/<int:id>/', views.detalle_orden, name='detalle_orden'),
    path('ordenes/recibir/<int:id>/', views.recibir_orden, name='recibir_orden'),

    # Reportes
    path('reporte/gastos/', views.reporte_gastos_centrocosto, name='reporte_gastos_centrocosto'),
    path(
        'reporte/compras/centro-costo/',
        views.reporte_gastos_centrocosto,
        name='reporte_compras_centro_costo',  # este name es el del navbar
    ),
    path(
        'reportes/compras-proveedor/',
        views.reporte_compras_proveedor,
        name='reporte_compras_proveedor',
    ),
    path('reporte/exportar/excel/', views.exportar_reporte_excel, name='exportar_reporte_excel'),
    path('reporte/exportar/pdf/', views.exportar_reporte_pdf, name='exportar_reporte_pdf'),

    # Requisiciones
    path('requisiciones/crear/', views.crear_requisicion, name='crear_requisicion'),
    path('requisiciones/mis/', views.mis_requisiciones, name='mis_requisiciones'),
    path('requisiciones/pendientes/', views.requisiciones_pendientes, name='requisiciones_pendientes'),
    path('requisiciones/aprobar/<int:id>/', views.aprobar_requisicion, name='aprobar_requisicion'),
    path('requisiciones/rechazar/<int:id>/', views.rechazar_requisicion, name='rechazar_requisicion'),
    path('requisiciones/detalle/<int:id>/', views.detalle_requisicion, name='detalle_requisicion'),
    path(
        'requisiciones/generar-oc/<int:id>/',
        views.generar_orden_de_requisicion,
        name='generar_orden_de_requisicion',
    ),
]
