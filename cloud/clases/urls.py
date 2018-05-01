# @Author: Manuel Rodriguez <valle>
# @Date:   04-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 23-Mar-2018
# @License: Apache license vesion 2.0


from django.conf.urls import url, include
from . import views

app_name = "gestion"
PEDIDOS = [
    url(r'codigos_postales/$', views.codigos_postales, name="codigos_postales"),
    url(r'codigos_postales/(?P<id>\d*)$', views.codigos_postales, name="codigos_postales"),
    url(r'rm_codigo_postal/(?P<id>\d*)$', views.rm_codigo_postal, name="rm_codigo_postal"),
    url(r'lista_codigos/$', views.lista_codigos, name="lista_codigos"),

    url(r'add_clientes/(?P<id>\d*)$', views.add_clientes, name="add_clientes"),
    url(r'rm_clases_clientes/(?P<id>\d*)$', views.rm_clases_clientes, name="rm_clases_clientes"),
    url(r'lista_clases_clientes/$', views.lista_clases_clientes, name="lista_clases_clientes"),
]

urlpatterns = [
    url(r'^$', views.index, name="menu"),
] + PEDIDOS
