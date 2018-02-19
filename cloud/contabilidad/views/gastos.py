# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   01-Jan-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 09-Jan-2018
# @License: Apache license vesion 2.0

from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from contabilidad.models import Gastos, CuentasGastos, SubCuentaGastos
from contabilidad.forms import GastosForm
from datetime import datetime
import os

# Create your views here.
@login_required(login_url='login_tk')
def elegir_cuenta(request):
    filter_query = Gastos.objects.filter(Q(fecha__month=datetime.now().strftime("%m")))
    return render(request, "contabilidad/gastos/find_cuentas.html",
                  {'query': filter_query,
                   'cuenta': 'si'})


@login_required(login_url='login_tk')
def gastos(request, id=-1):
    id = int(id)
    p, pk = get_cuenta_activa(request)
    filter_query = Gastos.objects.filter(Q(cuenta_id=p.pk))
    if not request.method == "POST" and id == -1:
        f = GastosForm()
        return render(request, 'contabilidad/gastos/listado.html',
                      {"form": f,
                       "p": p,
                       "pk": id,
                       'query': filter_query,
                       "mensaje": "Gasto nuevo" })

    elif not request.method == "POST" and id > 0:
        f = GastosForm()
        try:
            obj = Gastos.objects.get(pk=id)
            f = GastosForm(instance=obj)
        except Exception as e:
            print e
        return render(request, 'contabilidad/gastos/listado.html',
                      {"form": f,
                       "p": p,
                       "pk": id,
                       'query': filter_query,
                       "mensaje": "Editar gasto" })
    elif id > 0:
        f = GastosForm()
        try:
            reg = Gastos.objects.get(pk=id)
            f = GastosForm(request.POST, request.FILES, instance=reg)
        except Exception as e:
            print e

        if f.is_valid():
            reg = f.save()
            reg.save()
        else:
            print f.errors

        return redirect("Conta:lista_gastos")
    else:
        f = GastosForm(request.POST)
        if f.is_valid():
            obj = f.save(commit=False)
            obj.cuenta_id = pk
            obj.save()
            if 'accion_pk_subcuenta' in request.session:
                p.gastos.add(obj)
        else:
            print f.errors
        return redirect("Conta:lista_gastos")


@login_required(login_url='login_tk')
def rm_gasto(request, id):
    try:
        obj = Gastos.objects.get(pk=id)
        obj.delete()
    except Exception as e:
        print e

    return redirect("Conta:lista_gastos")


@login_required(login_url='login_tk')
def lista_gastos(request):
    obj, pk  = get_cuenta_activa(request)
    f = GastosForm()
    if request.method == "POST":
        filter = request.POST["filter"]
        filter_query = Gastos.objects.filter(Q(cuenta__pk=pk) |
                                             Q(fecha__icontains=filter))
        return render(request, "contabilidad/gastos/listado.html",
                      {'query': filter_query,
                       "form": f,
                       "p": obj,
                       "pk": -1,
                       "mensaje": "Gasto nuevo"})
    else:
        if 'accion_pk_subcuenta' in request.session:
            filter_query = obj.gastos.all()
        else:
            filter_query = Gastos.objects.filter(Q(cuenta__pk=pk))
        return render(request, "contabilidad/gastos/listado.html",
                      {'query': filter_query,
                       "form": f,
                       'p': obj,
                       "pk": -1,
                       "mensaje": "Gasto nuevo" })




@login_required(login_url='login_tk')
def find_gasto(request):
    if request.method == "POST":
        filter = request.POST["filter"]
        filter = request.POST["filter"]
        if len(filter) > 0 and filter[0].lower() == 'm':
            filter = filter[1:]
            filter_query = Ingresos.objects.filter(Q(fecha__month=filter))
        else:
            filter_query = Gastos.objects.filter(Q(fecha__icontains=filter) |
                                                 Q(importe__icontains=filter))
        return render(request, "contabilidad/gastos/lista_ajax.html",
                      {'query': filter_query,
                       "opcion": 'find'})
    else:
        filter_query = Gastos.objects.all()
        return render(request, "contabilidad/gastos/lista_ajax.html",
                      {'query': filter_query,
                       "opcion": 'find'})
    return response



def get_cuenta_activa(request):
    obj = CuentasGastos()
    pk = None
    if 'accion_pk_cuenta' in request.session:
        pk = request.session["accion_pk_cuenta"]
        try:
            obj = CuentasGastos.objects.get(pk=pk)
            pk = obj.pk
        except Exception as e:
            print e
    elif 'accion_pk_subcuenta' in request.session:
        pk = request.session["accion_pk_subcuenta"]
        try:
            obj = SubCuentaGastos.objects.get(pk=pk)
            pk = obj.cuenta.pk
        except Exception as e:
            print e

    return obj, pk
