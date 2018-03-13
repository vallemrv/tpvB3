# @Author: Manuel Rodriguez <valle>
# @Date:   04-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 08-Mar-2018
# @License: Apache license vesion 2.0


from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'servir_pedido/(?P<id>\d*)$', views.servir_pedido, name="servir_pedido"),
    url(r'change_servido/(?P<servido>.*)/(?P<id>\d*)$', views.change_servido, name="change_servido"),
    url(r'get_pedidos/$', views.get_pedidos, name="get_pedidos"),
    url(r'all_pedidos/$', views.all_pedidos, name="all_pedidos"),

    url(r'^$', views.index, name="index"),
]
