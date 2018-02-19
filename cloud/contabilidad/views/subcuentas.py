# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   01-Jan-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 08-Jan-2018
# @License: Apache license vesion 2.0

from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from contabilidad.models import SubCuentaGastos
from contabilidad.forms import SubCuentaGastosForm
from contabilidad.utils import vaciar_sesison_cuentas, vaciar_sesison_subcuentas
from tokenapi.http import JsonResponse


# Create your views here.

@login_required(login_url='login_tk')
def subcuentas(request, id=-1):
    if not request.method == "POST" and id == -1:
        f = SubCuentaGastosForm()
        return render(request, 'contabilidad/subcuentas/cuentas.html',
                      {"form": f,
                       "titulo": "Cuenta nueva" })

    elif not request.method == "POST" and id > 0:
        f = SubCuentaGastosForm()
        try:
            obj = SubCuentaGastos.objects.get(pk=id)
            f = SubCuentaGastosForm(instance=obj)
        except:
            pass
        return render(request, 'contabilidad/subcuentas/cuentas.html',
                      {"form": f,
                       "titulo": "Editar cuenta" })
    elif id > 0:
        f = SubCuentaGastosForm()
        try:
            reg = SubCuentaGastos.objects.get(pk=id)
            f = SubCuentaGastosForm(request.POST, instance=reg)
        except:
            pass
        if f.is_valid():
            reg = f.save()
            reg.active = True
            reg.save()

        return redirect("Conta:lista_subcuentas")
    else:
        f = SubCuentaGastosForm(request.POST)
        if f.is_valid():
            obj = f.save()
        return redirect("Conta:lista_subcuentas")


@login_required(login_url='login_tk')
def rm_subcuentas(request, id):
    try:
        p  = SubCuentaGastos.objects.get(pk=id)
        p.activo = False
        p.save()
    except Exception as e:
        print e

    return redirect("Conta:lista_subcuentas")


@login_required(login_url='login_tk')
def lista_subcuentas(request):
    if request.method == "POST":
        filter = request.POST["filter"]
        filter_query = SubCuentaGastos.objects.filter(Q(nombre__icontains=filter)).exclude(activo=False)
        return render(request, "contabilidad/subcuentas/lista.html",
                      {'query': filter_query,
                       "opcion": "lista"})
    else:
        filter_query = SubCuentaGastos.objects.all().exclude(activo=False)
        return render(request, "contabilidad/subcuentas/lista.html",
                      {'query': filter_query,
                       "opcion": "lista"})


@login_required(login_url='login_tk')
def find_subcuentas(request):
    if request.method == "POST":
        filter = request.POST["filter"]
        filter_query = SubCuentaGastos.objects.filter(Q(nombre__icontains=filter)).exclude(activo=False)
        return render(request, "contabilidad/subcuentas/lista_ajax.html",
                      {'query': filter_query,
                       "opcion": 'find'})
    else:
        filter_query = SubCuentaGastos.objects.all().exclude(activo=False)
        return render(request, "contabilidad/subcuentas/lista_ajax.html",
                      {'query': filter_query,
                       "opcion": 'find'})



@login_required(login_url='login_tk')
def set_subcuenta(request, id):
    obj = SubCuentaGastos.objects.get(pk=id)
    vaciar_sesison_cuentas(request)
    request.session["accion_pk_subcuenta"] = obj.pk
    return JsonResponse("perfect")

@login_required(login_url='login_tk')
def salir_subcuentas(request):
    vaciar_sesison_subcuentas(request)
    vaciar_sesison_cuentas(request)
    return redirect("Conta:lista_cuentas")
