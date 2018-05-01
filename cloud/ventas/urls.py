# @Author: Manuel Rodriguez <valle>
# @Date:   04-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 23-Mar-2018
# @License: Apache license vesion 2.0


from django.conf.urls import url, include
from . import views

app_name = "ventas"
ARQUEOS = [
    url(r'^lista_arqueos/$', views.lista_arqueos, name="lista_arqueos"),
    url(r'^arquear/$', views.arquear, name="arquear"),
    url(r'^desglose_arqueo/(?P<id>\d*)/$', views.desglose_arqueo, name="desglose_arqueo"),
]

PEDIDOS = [
    url(r'^pedidos_pendientes/$', views.pedidos_pendientes, name="pedidos_pendientes"),
]

urlpatterns = [
    url(r'^test_ws/$', views.test_ws, name="test_ws"),
    url(r'^$', views.index, name="menu"),
]+ PEDIDOS + ARQUEOS
