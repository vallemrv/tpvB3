# @Author: Manuel Rodriguez <valle>
# @Date:   09-Mar-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 17-Mar-2018
# @License: Apache license vesion 2.0

from django.db.models import Sum
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ventas.models import Arqueos, Conteo, Gastos, PedidosExtra, Pedidos
from tokenapi.http import JsonResponse, JsonError
import json


@login_required(login_url="login_pk")
def lista_arqueos(request):
    query = Arqueos.objects.all().order_by("-fecha")
    return render(request, "ventas/arqueos/listado.html",
                  {'query': query})


@login_required(login_url="login_pk")
def desglose_arqueo(request, id):
    query = Arqueos.objects.get(id=id)
    return render(request, "ventas/arqueos/arqueo.html",
                  {'query': query})


@csrf_exempt
def arquear(request):
    if request.method == 'POST':
        arq = json.loads(request.POST["data"])
        efectivo = Pedidos.objects.filter(estado__contains="PG_")
        efectivo = efectivo.exclude(modo_pago="Tarjeta").aggregate(Sum("total"))
        efectivo = efectivo["total__sum"] if efectivo["total__sum"] != None else 0
        tarjeta = Pedidos.objects.filter(estado__contains="PG_")
        tarjeta = tarjeta.exclude(modo_pago="Efectivo").aggregate(Sum("total"))
        tarjeta = tarjeta["total__sum"] if tarjeta["total__sum"] != None else 0
        caja_dia = float(efectivo) + float(tarjeta) + float(arq['caja_dia']) + float(arq['tarjeta'])
        ef_fisico = float(arq['efectivo']) - float(arq['cambio'])
        tarjeta = float(tarjeta) + float(arq['tarjeta'])
        ef_tickado = float(efectivo) + float(arq['caja_dia'])
        descuadre =  (ef_fisico + float(arq['total_gastos'])) - ef_tickado
        arqueo = Arqueos(**{'caja_dia': caja_dia,
                           'efectivo': ef_fisico,
                           'cambio': arq['cambio'],
                           'total_gastos': arq['total_gastos'],
                           'tarjeta': tarjeta,
                           'descuadre': descuadre,
                           })
        arqueo.save()

        for c in arq["conteo"]:
            conteo = Conteo(**c)
            conteo.save()
            arqueo.conteo.add(conteo)
        for c in arq["extras"]:
            c["importe"] = c["importe"].replace(",", ".")
            e = PedidosExtra(**c)
            e.save()
            arqueo.pedidosextra.add(e)
        for c in arq["gastos"]:
            g = Gastos(**c)
            g.save()
            arqueo.gastos.add(g)
        for c in Pedidos.objects.filter(estado__contains="PG_"):
            c.estado = "AR_SN"
            c.save()
            arqueo.pedidos.add(c)


        desglose = []
        retirar = 0
        for ls in arq["conteo"]:
            if ef_fisico - retirar > 0.1:
                total_linea = ls["total"]
                subtotal = retirar + total_linea
                if subtotal <= ef_fisico:
                    retirar += total_linea
                    desglose.append(ls)
                else:
                    subtotal = ef_fisico - retirar
                    tipo = float(ls["tipo"])
                    num = int(subtotal/tipo)
                    if num > 0:
                        total_linea = num * tipo
                        retirar += total_linea
                        desglose.append({"can": num, "tipo": tipo,
                                         "total": total_linea,
                                         "texto_tipo": ls["texto_tipo"]})

        return JsonResponse({'desglose':desglose})

    return JsonError("NO ESTA AUTORIZADO")
