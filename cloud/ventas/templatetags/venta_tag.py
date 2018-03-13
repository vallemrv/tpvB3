# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   27-Aug-2017
# @Email:  valle.mrv@gmail.com
# @Filename: admin_extras.py
# @Last modified by:   valle
# @Last modified time: 10-Mar-2018
# @License: Apache license vesion 2.0

from django import template
from django.db.models import Q, Sum

register = template.Library()


@register.filter(name='efectivo')
def efectivo(arq):
    extras = arq.pedidosextra.filter(modo_pago="Efectivo")
    importe = 0
    for e in extras:
        importe += e.importe
    return arq.efectivo - importe

@register.filter(name='tarjeta')
def tarjeta(arq):
    extras = arq.pedidosextra.filter(modo_pago="Tarjeta").aggregate(Sum("importe"))
    importe = 0 if extras.get("importe__sum") == None else extras.get("importe__sum")
    return arq.tarjeta - importe

@register.filter(name='extra')
def efectivo_extra(arq):
    extras = arq.pedidosextra.filter(modo_pago="Efectivo").aggregate(Sum("importe"))
    return 0 if extras.get("importe__sum") == None else extras.get("importe__sum")

@register.filter(name='tarjeta_extra')
def tarjeta_extra(arq):
    extras = arq.pedidosextra.filter(modo_pago="Tarjeta").aggregate(Sum("importe"))
    return 0 if extras.get("importe__sum") == None else extras.get("importe__sum")


@register.filter(name='total_conteo')
def total_conteo(arq):
    conteo = arq.conteo.all()
    importe = 0
    for c in conteo:
        importe += c.can * c.tipo
    return importe

@register.filter(name='total_extra')
def total_extra(arq):
    conteo = arq.pedidosextra.all().aggregate(Sum("importe"))
    return 0 if conteo.get("importe__sum") == None else conteo.get("importe__sum")


@register.filter(name='total')
def total(lconteo):
    return lconteo.can * lconteo.tipo
