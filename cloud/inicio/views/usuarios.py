# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   01-Oct-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 02-Jan-2018
# @License: Apache license vesion 2.0

from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.utils.encoding import force_text
from django.utils.http import  urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from inicio.forms import UserForm

import threading

@login_required(login_url='login_tk')
def usuarios(request, id_user=-1):
    if not request.method == "POST" and id_user == -1:
        f_user = UserForm()
        return render(request, 'gestion/empleados/usuarios.html',
                      {"form": f_user,
                       "titulo": "Empleado nuevo" })

    elif not request.method == "POST" and id_user > 0:
        f_user = UserForm()
        try:
            user = User.objects.get(pk=id_user)
            f_user = UserForm(instance=user)
        except:
            pass
        return render(request, 'gestion/empleados/usuarios.html',
                      {"form": f_user,
                       "titulo": "Editar empleado" })
    elif id_user > 0:
        f_user = UserForm()
        try:
            user = User.objects.get(pk=id_user)
            f_user = UserForm(request.POST, instance=user)
        except:
            pass
        if f_user.is_valid():
            user = f_user.save()
            user.active = True
            user.save()

        return redirect("lista_usuarios")
    else:
        f_user = UserForm(request.POST)
        if f_user.is_valid():
            user = f_user.save()
            password = User.objects.make_random_password()
            user.set_password(password)
            user.active = True
            user.save()
            threading.Thread(target=send_mail_alta, args=(request, user)).start()
            return redirect("lista_usuarios")

def send_mail_alta(request, user):
    f = PasswordResetForm()
    setattr(f, "cleaned_data", {})
    f.cleaned_data["email"] = user.email
    f.save(request=request, from_email="info@freakmedia.es",
           email_template_name='email/activate_user.html')

def lista_usuarios(request):
    if request.method == "POST":
        filter = request.POST["filter"]
        filter_query = User.objects.filter(Q(username__contains=filter) |
                            Q(last_name__contains=filter) |
                            Q(first_name__contains=filter)).exclude(pk=request.user.pk)
        return render(request, "gestion/empleados/lista_usuarios.html", {'query': filter_query})
    else:
        filter_query = User.objects.all().exclude(pk=request.user.pk)
        return render(request, "gestion/empleados/lista_usuarios.html", {'query': filter_query})


@login_required(login_url='login_tk')
def rm_empleados(request, id_user):
    try:
        User.objects.get(pk=id_user).delete()
    except:
        pass

    return redirect("lista_usuarios")

@login_required(login_url='login_tk')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('tienda')
        else:
            return render(request, 'gestion/login/change_password.html', {
                'form': form,
                "form_error": form.errors ,
            })

    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'gestion/login/change_password.html', {
        'form': form
    })

def confirm_reset_password(request, uidb64=None, token=None):
    assert uidb64 is not None and token is not None  # checked by URLconf
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'gestion/login/reset_password.html', {
                    'form': form,
                    "form_error": {"mensaje": ["la contraseña se ha establecido con exito"]},
                    "redirect": "login_tk"
                })
            else:
                return render(request, 'gestion/login/reset_password.html', {
                    'form': form,
                    "form_error": form.errors
                })
        else:
            form = SetPasswordForm(user)

            return render(request, 'gestion/login/reset_password.html', {
                'form': form,
            })

    return redirect("tienda")

def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            threading.Thread(target=send_mail_reset_password,args=(request, form)).start()
            return redirect("login_tk")
        else:
            return render(request, 'gestion/login/reset_password.html', {
                'form': form,
                "form_error": form.errors ,
            })
    else:
        form = PasswordResetForm()
        return render(request, 'gestion/login/reset_password.html', {
            'form': form
        })


def send_mail_reset_password(request, form):
    form.save(request=request, from_email="info@freakmedia.es",)
