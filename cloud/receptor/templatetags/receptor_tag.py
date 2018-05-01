# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   27-Aug-2017
# @Email:  valle.mrv@gmail.com
# @Filename: admin_extras.py
# @Last modified by:   valle
# @Last modified time: 24-Apr-2018
# @License: Apache license vesion 2.0

from django import template
from ventas.models import Direcciones
import json
import sys
register = template.Library()

@register.filter
def tipo_pedido(pedido, dark="bg-dark"):
    if "@" in pedido.num_avisador or "Mesa" in pedido.num_avisador:
        return 'bg-info'
    elif 'Domicilio' in pedido.num_avisador:
        return 'bg-success'
    else:
        return dark

@register.filter
def num_avisador(pedido):
    str = pedido.num_avisador
    if str not in pedido.para_llevar:
        str = str + " - " + pedido.para_llevar
    return str


@register.filter
def telefono(pedido):
    c = pedido.clientes_set.all()
    if len(c) > 0:
        return unicode(c[0].telefono)
    else:
        return "No tiene direccion"


@register.filter(name='direccion')
def direccion(pedido):
    c = pedido.clientes_set.all()
    if len(c) > 0:
        try:
            d = Direcciones.objects.get(id=c[0].direccion)
        except:
            ds = c[0].direcciones_set.all()
            if len(ds) > 0:
                return unicode(ds[0])
            return "Direccion no correcta"

        return str(d)
    else:
        return "No tiene direccion"

@register.filter(name='mostrable')
def mostrable(lineas):
    return lineas.exclude(tipo__in=["postres", "bebidas"])


@register.filter(name='hay_cliente')
def hay_cliente(p):
    c = p.clientes_set.all()
    return len(c) > 0
