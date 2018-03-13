# @Author: Manuel Rodriguez <valle>
# @Date:   09-Mar-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 09-Mar-2018
# @License: Apache license vesion 2.0


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ventas.models import Pedidos


@login_required(login_url="login_tk")
def pedidos_pendientes(request):
    ps = Pedidos.objects.filter(servido=False).exclude(estado__icontains="AR")
    return render(request, "ventas/pedidos/lista_pendientes.html",
                  {'query': ps.order_by("-fecha")})
