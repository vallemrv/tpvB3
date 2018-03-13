# @Author: Manuel Rodriguez <valle>
# @Date:   03-Jan-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 10-Mar-2018
# @License: Apache license vesion 2.0

from .proveedores import *
from .cuenta_gastos import *
from .alabaranes import *
from .gastos import *
from .ingresos import *
from .subcuentas import *

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login_tk')
def inicio(request):
    return render(request, "inicio/contabilidad.html")
