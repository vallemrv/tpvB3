# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   01-Jan-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 07-Jan-2018
# @License: Apache license vesion 2.0

from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from contabilidad.models import CuentasGastos
from contabilidad.forms import CuentasGastosForm
from contabilidad.utils import vaciar_sesison_subcuentas, vaciar_sesison_cuentas
from tokenapi.http import JsonResponse


# Create your views here.

@login_required(login_url='login_tk')
def cuentas(request, id=-1):
    if not request.method == "POST" and id == -1:
        f = CuentasGastosForm()
        return render(request, 'contabilidad/cuentas/cuentas.html',
                      {"form": f,
                       "titulo": "Cuenta nueva" })

    elif not request.method == "POST" and id > 0:
        f = CuentasGastosForm()
        try:
            obj = CuentasGastos.objects.get(pk=id)
            f = CuentasGastosForm(instance=obj)
        except:
            pass
        return render(request, 'contabilidad/cuentas/cuentas.html',
                      {"form": f,
                       "titulo": "Editar cuenta" })
    elif id > 0:
        f = CuentasGastosForm()
        try:
            reg = CuentasGastos.objects.get(pk=id)
            f = CuentasGastosForm(request.POST, instance=reg)
        except:
            pass
        if f.is_valid():
            reg = f.save()
            reg.active = True
            reg.save()

        return redirect("Conta:lista_cuentas")
    else:
        f = CuentasGastosForm(request.POST)
        if f.is_valid():
            obj = f.save()
        return redirect("Conta:lista_cuentas")


@login_required(login_url='login_tk')
def rm_cuentas(request, id):
    try:
        p  = CuentasGastos.objects.get(pk=id)
        p.activo = False
        p.save()
    except Exception as e:
        print e

    return redirect("Conta:lista_cuentas")


@login_required(login_url='login_tk')
def lista_cuentas(request):
    if request.method == "POST":
        filter = request.POST["filter"]
        filter_query = CuentasGastos.objects.filter(Q(nombre__icontains=filter)).exclude(activo=False)
        return render(request, "contabilidad/cuentas/lista.html",
                      {'query': filter_query,
                       "opcion": "lista"})
    else:
        filter_query = CuentasGastos.objects.all().exclude(activo=False)
        return render(request, "contabilidad/cuentas/lista.html",
                      {'query': filter_query,
                       "opcion": "lista"})


@login_required(login_url='login_tk')
def find_cuentas(request):
    if request.method == "POST":
        filter = request.POST["filter"]
        print filter
        filter_query = CuentasGastos.objects.filter(Q(nombre__icontains=filter)).exclude(activo=False)
        return render(request, "contabilidad/cuentas/lista_ajax.html",
                      {'query': filter_query,
                       "opcion": 'find'})
    else:
        filter_query = CuentasGastos.objects.all().exclude(activo=False)
        return render(request, "contabilidad/cuentas/lista_ajax.html",
                      {'query': filter_query,
                       "opcion": 'find'})



@login_required(login_url='login_tk')
def set_cuenta(request, id):
    obj = CuentasGastos.objects.get(pk=id)
    vaciar_sesison_subcuentas(request)
    request.session["accion_pk_cuenta"] = obj.pk
    return JsonResponse("perfect")

@login_required(login_url='login_tk')
def salir_cuentas(request):
    vaciar_sesison_subcuentas(request)
    vaciar_sesison_cuentas(request)
    return redirect("Conta:lista_cuentas")
