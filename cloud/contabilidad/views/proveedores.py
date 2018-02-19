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
from contabilidad.models import Proveedores
from contabilidad.forms import ProveedoresForm
from tokenapi.http import JsonResponse


# Create your views here.

def index(request):
    return HttpResponse("Estas en contabilidad")

@login_required(login_url='login_tk')
def proveedores(request, id=-1):
    if not request.method == "POST" and id == -1:
        f = ProveedoresForm()
        return render(request, 'contabilidad/proveedores/proveedor.html',
                      {"form": f,
                       "titulo": "Proveedor nuevo" })

    elif not request.method == "POST" and id > 0:
        f = Proveedores()
        try:
            obj = Proveedores.objects.get(pk=id)
            f = ProveedoresForm(instance=obj)
        except:
            pass
        return render(request, 'contabilidad/proveedores/proveedor.html',
                      {"form": f,
                       "titulo": "Editar proveedor" })
    elif id > 0:
        f = Proveedores()
        try:
            reg = Proveedores.objects.get(pk=id)
            f = ProveedoresForm(request.POST, instance=reg)
        except:
            pass
        if f.is_valid():
            reg = f.save()
            reg.active = True
            reg.save()

        return redirect("Conta:lista_proveedores")
    else:
        f = ProveedoresForm(request.POST)
        if f.is_valid():
            proveedor = f.save()
        return redirect("Conta:lista_proveedores")


@login_required(login_url='login_tk')
def rm_proveedores(request, id):
    try:
        p  = Proveedores.objects.get(pk=id)
        p.activo = False
        p.save()
    except Exception as e:
        print e

    return redirect("Conta:lista_proveedores")


@login_required(login_url='login_tk')
def lista_proveedores(request):
    if request.method == "POST":
        filter = request.POST["filter"]
        filter_query = Proveedores.objects.filter(Q(CIF__contains=filter) |
                                                  Q(razon_social__icontains=filter) |
                                                  Q(nombre__icontains=filter) |
                                                  Q(telefono__contains=filter)).exclude(activo=False)
        return render(request, "contabilidad/proveedores/lista_proveedores.html",
                      {'query': filter_query,
                       "opcion": "lista"})
    else:
        filter_query = Proveedores.objects.all().exclude(activo=False)
        return render(request, "contabilidad/proveedores/lista_proveedores.html",
                      {'query': filter_query,
                       "opcion": "lista"})


@login_required(login_url='login_tk')
def find_proveedores(request):
    if request.method == "POST":
        filter = request.POST["filter"]
        filter_query = Proveedores.objects.filter(Q(nombre__icontains=filter) |
                                                  Q(CIF__contains=filter) |
                                                  Q(razon_social__icontains=filter) |
                                                  Q(telefono__contains=filter)).exclude(activo=False)
        return render(request, "contabilidad/proveedores/ajax_proveedores.html",
                      {'query': filter_query,
                       "opcion": 'find'})
    else:
        filter_query = Proveedores.objects.all().exclude(activo=False)
        return render(request, "contabilidad/proveedores/ajax_proveedores.html",
                      {'query': filter_query,
                       "opcion": 'find'})



@login_required(login_url='login_tk')
def set_proveedor(request, id):
    proveedor = Proveedores.objects.get(pk=id)
    request.session["accion_cif"] = proveedor.CIF
    request.session["accion_pk_proveedor"] = proveedor.pk
    return JsonResponse("perfect")

@login_required(login_url='login_tk')
def salir_proveedores(request):
    vaciar_sesison_proveedor(request)
    return redirect("Conta:lista_proveedores")

def vaciar_sesison_proveedor(request):
    if "accion_pk_proveedor" in request.session:
        del request.session["accion_pk_proveedor"]
    if "accion_cif" in request.session:
        del request.session["accion_cif"]
