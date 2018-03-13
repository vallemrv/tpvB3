# @Author: Manuel Rodriguez <valle>
# @Date:   09-Mar-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 13-Mar-2018
# @License: Apache license vesion 2.0


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ventas.models import Arqueos


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
