# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   03-Jan-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 08-Jan-2018
# @License: Apache license vesion 2.0


from django import forms
from models import *

class ProveedoresForm(forms.ModelForm):

    class Meta:
        model = Proveedores
        exclude = ["activo"]


class AlbaranForm(forms.ModelForm):
    class Meta:
        model = Albaranes
        exclude = ["cuenta"]



class GastosForm(forms.ModelForm):
    class Meta:
        model = Gastos
        exclude = ["cuenta"]


class CuentasGastosForm(forms.ModelForm):
    class Meta:
        model = CuentasGastos
        exclude = ["activo"]
        widgets = {
            "descripcion": forms.TextInput()
        }

class SaldoReguladorForm(forms.ModelForm):
    class Meta:
        model = SaldoRegulador
        exclude = []

class IngresosForm(forms.ModelForm):
    class Meta:
        model = Ingresos
        exclude = []

class SubCuentaGastosForm(forms.ModelForm):
    class Meta:
        model = SubCuentaGastos
        exclude = ["gastos", "activo"]
