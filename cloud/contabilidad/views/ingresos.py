# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   01-Jan-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 09-Jan-2018
# @License: Apache license vesion 2.0

from django.forms.models import model_to_dict
from django.db.models import Q, Sum
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from contabilidad.models import Ingresos, Proveedores
from contabilidad.forms import IngresosForm
from gestion.models import Arqueocaja, Cierrecaja, Ticket, Ticketlineas, Lineaspedido
from tokenapi.http import JsonResponse
from datetime import datetime, timedelta

import os



@login_required(login_url='login_tk')
def ingresos(request, id=-1):
    id = int(id)
    if not request.method == "POST" and id == -1:
        f = IngresosForm()
        filter_query = Ingresos.objects.filter()
        return render(request, 'contabilidad/ingresos/listado.html',
                      {"form": f,
                       "pk": id,
                       'query': filter_query,
                       "mensaje": "Ingreso nuevo" })

    elif not request.method == "POST" and id > 0:
        f = IngresosForm()
        try:
            obj = Ingresos.objects.get(pk=id)
            f = IngresosForm(instance=obj)
            filter_query = Ingresos.objects.filter()
        except Execiption as e:
            print e
        return render(request, 'contabilidad/ingresos/listado.html',
                      {"form": f,
                       "pk": id,
                       'query': filter_query,
                       "mensaje": "Editar ingreso" })
    elif id > 0:
        f = IngresosForm()
        try:
            reg = Ingresos.objects.get(pk=id)
            f = IngresosForm(request.POST, instance=reg)
        except Execiption as e:
            print e
        if f.is_valid():
            reg = f.save()
            reg.save()
        else:
            print f.errors
        return redirect("Conta:lista_ingresos")
    else:
        f = IngresosForm(request.POST)
        if f.is_valid():
            obj = f.save(commit=False)
            obj.save()
        else:
            print f.errors
        return redirect("Conta:lista_ingresos")


@login_required(login_url='login_tk')
def rm_ingreso(request, id):
    try:
        obj = Ingresos.objects.get(pk=id)
        obj.delete()
    except Exception as e:
        print e

    return redirect("Conta:lista_ingresos")


@login_required(login_url='login_tk')
def lista_ingresos(request):
    f = IngresosForm()
    if request.method == "POST":
        filter = request.POST["filter"]
        filter_query = Ingresos.objects.filter(Q(fecha__contains=filter))
        return render(request, "contabilidad/ingresos/listado.html",
                      {'query': filter_query,
                       "form": f,
                       "pk": -1,
                       "mensaje": "Ingreso nuevo"})
    else:
        filter_query = Ingresos.objects.filter()
        return render(request, "contabilidad/ingresos/listado.html",
                      {'query': filter_query,
                       "form": f,
                       "pk": -1,
                       "mensaje": "Ingreso nuevo" })




@login_required(login_url='login_tk')
def find_ingreso(request):
    if request.method == "POST":
        filter = request.POST["filter"]
        if len(filter) > 0 and filter[0].lower() == 'm':
            filter = filter[1:]
            filter_query = Ingresos.objects.filter(Q(fecha__month=filter))
        else:
            filter_query = Ingresos.objects.filter(Q(fecha__contains=filter))
        return render(request, "contabilidad/ingresos/lista_ajax.html",
                      {'query': filter_query,
                       "opcion": 'find'})
    else:
        filter_query = Ingresos.objects.all()
        return render(request, "contabilidad/ingresos/lista_ajax.html",
                      {'query': filter_query,
                       "opcion": 'find'})


@login_required(login_url='login_tk')
def calcular_ingreso(request, fecha=None):
    fecha = request.GET["fecha"]
    total = 0
    if fecha != "":
        date = datetime.strptime(fecha, "%d/%m/%Y")
        date1 = date + timedelta(days=1)
        cajas = Cierrecaja.objects.filter((Q(fecha=date.strftime("%Y/%m/%d"))
                                           & Q(hora__gte='06:00')) |
                                          (Q(fecha=date1.strftime("%Y/%m/%d"))
                                           & Q(hora__lte='05:00')))


        for c in cajas:
            print "Error tpv "+c.pk
            arq = Arqueocaja.objects.filter(idcierre=c.pk)
            descuadre = 0
            if len(arq) > 0:
                descuadre = arq[0].descuadre
            sum = Ticketlineas.objects.filter(Q(idticket__pk__gte=c.ticketcom) &
                                              Q(idticket__pk__lte=c.ticketfinal))

            idlineas = sum.values('idlinea')
            sum = Lineaspedido.objects.filter(pk__in=idlineas).aggregate(sum_lineas=Sum("precio"))

            total = total + (float(sum['sum_lineas']) + descuadre)

    return JsonResponse({'total':"%.2f" % total})
