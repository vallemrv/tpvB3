# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   07-Mar-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 13-Mar-2018
# @License: Apache license vesion 2.0

from __future__ import unicode_literals
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from ventas.models import Pedidos, LineasPedido, Clientes, Direcciones
from tokenapi.http import JsonResponse, JsonError
from django.template.loader import render_to_string

# Create your views here.

def index(request):
    return render(request, "receptor/index.html")

def get_pedidos(request):
    pedidos = Pedidos.objects.filter(estado__icontains="NO").order_by("fecha")
    for p in pedidos:
        p.estado = p.estado.replace("NO", "SI")
        p.servido = False
        p.save()
    return render(request, "receptor/lista_pedidos_ajax.html", {"pedidos": pedidos})

def all_pedidos(request):
    pedidos = Pedidos.objects.filter(Q(estado__icontains="NO") |
                                     Q(estado__icontains="SI", servido=False)).order_by("fecha")
    for p in pedidos:
        p.estado = p.estado.replace("NO", "SI")
        p.servido = False
        p.save()
    return render(request, "receptor/lista_pedidos_ajax.html", {"pedidos": pedidos})



def change_servido(request, servido, id):
    linea = LineasPedido.objects.get(id=id)
    linea.servido = bool(servido)
    linea.save()
    return JsonResponse(servido)


def servir_pedido(request, id):
    p = Pedidos.objects.get(id=id)
    p.servido = True
    p.save()
    return JsonResponse(p.servido)
