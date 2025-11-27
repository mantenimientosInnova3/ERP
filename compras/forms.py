# compras/forms.py
from django import forms
from .models import Producto
from .models import OrdenCompra, DetalleOrden
from .models import Requisicion, DetalleRequisicion
from django.forms import inlineformset_factory
from .models import Requisicion

class RequisicionForm(forms.ModelForm):
    class Meta:
        model = Requisicion
        fields = ['descripcion', 'area']

DetalleRequisicionFormSet = inlineformset_factory(
    Requisicion,
    DetalleRequisicion,
    fields=['producto', 'cantidad', 'unidad', 'observaciones'],
    extra=1,
    can_delete=False
)

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'sku', 'cantidad', 'descripcion', 'precio']


class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = ['fecha', 'proveedor', 'centro_costo']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }
class DetalleOrdenForm(forms.ModelForm):
    class Meta:
        model = DetalleOrden
        fields = ['producto', 'cantidad']
