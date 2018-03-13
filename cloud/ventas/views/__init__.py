# @Author: Manuel Rodriguez <valle>
# @Date:   09-Mar-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 13-Mar-2018
# @License: Apache license vesion 2.0
from .arqueos import *
from .pedidos import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login_tk')
def index(request):
    return render(request, "inicio/ventas.html")


def test_ws(request):
    return render(request, 'ws/test.html')
