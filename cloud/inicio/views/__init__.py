# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   01-Jan-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 02-Jan-2018
# @License: Apache license vesion 2.0

from .usuarios import *
from .menu import *

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth import login as login_auth, logout as logout_auth, authenticate
from inicio.forms import UserForm, LoginForm


def login(request):
    if not request.method == "POST":
        form_log = LoginForm()
        return render(request, "inicio/login/login.html", {"form": form_log})
    else:
        form_log = LoginForm(request.POST)
        if form_log.is_valid():
            user = authenticate(username=form_log.cleaned_data['username'],
                                password=form_log.cleaned_data['password'])
            if user != None:
                login_auth(request, user)
                return redirect("menu_principal")
            else:
                return render(request, "inicio/login/login.html",
                              {"form": form_log,
                               "mensaje": "El usuario o la contraseña no son validos"})

def logout(request):
    logout_auth(request)
    return redirect("menu_principal")

@login_required(login_url='login_tk')
def en_construccion(request):
    return render(request, "en_construccion.html")

@login_required(login_url='login_tk')
def not_found(request):
    return render(request, "404error.html")
