# @Author: Manuel Rodriguez <valle>
# @Date:   01-Jan-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 06-Jan-2018
# @License: Apache license vesion 2.0

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url='login_tk')
def menu_principal(request):
    return render(request, "inicio/inicio.html")
