# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   02-Jan-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 02-Jan-2018
# @License: Apache license vesion 2.0


from django.contrib.auth.models import User
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre", max_length=200)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput())

class ResetPasswordForm(forms.Form):
    old_password = forms.CharField(label="Contraseña antigua", widget=forms.PasswordInput())
    password = forms.CharField(label="Contraseña nueva", widget=forms.PasswordInput())
    repite = forms.CharField(label="Contraseña nueva", widget=forms.PasswordInput())

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', "first_name",  "is_superuser")
        labels = {
            "is_superuser": "Es administrador",
            "username": "Nombre usuario o NICK",
            "first_name": "Nombre completo"
        }
