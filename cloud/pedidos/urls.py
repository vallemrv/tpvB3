# @Author: Manuel Rodriguez <valle>
# @Date:   04-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 13-Apr-2018
# @License: Apache license vesion 2.0


from django.conf.urls import url, include

from . import views

app_name = "pedidos"
urlpatterns = [
    url(r'^$', views.index, name="p_index"),
    url(r'pedidos/$', views.pedidos, name="pedidos"),
    url(r'set_clase/(?P<id>\d*)/$', views.set_clase, name="set_clase"),
    url(r'set_producto/(?P<id>\d*)/$', views.set_producto, name="set_producto"),
    url(r'corregir/$', views.corregir, name="corregir"),
    url(r'set_pregunta/(?P<id>\d*)/$', views.set_pregunta, name="set_pregunta"),
    url(r'set_promocion/(?P<id>\d*)/$', views.set_promocion, name="set_promocion"),
    url(r'minus/(?P<id>\d*)/$', views.minus, name="minus"),
    url(r'plus/(?P<id>\d*)/$', views.plus, name="plus"),
    url(r'add_comment/(?P<id>\d*)/$', views.add_comment, name="add_comment"),
    url(r'delete/(?P<id>\d*)/$', views.delete, name="delete"),
    url(r'ver_pedido/$', views.ver_pedido, name="ver_pedido"),
    url(r'datos_personales/$', views.datos_personales, name="datos_personales"),
    url(r'datos_del_pedido/$', views.datos_del_pedido, name="datos_del_pedido"),
    url(r'hacer_pedido/$', views.hacer_pedido, name="hacer_pedido"),
    url(r'next/$', views.next, name="next"),
    url(r'pedido_change/$', views.pedido_change, name="pedido_change"),
    url(r'soy_cliente/$', views.soy_cliente, name="soy_cliente"),
    url(r'sel_cliente/$', views.sel_cliente, name="sel_cliente"),
    url(r'sel_dir/(?P<id>\d*)/$', views.sel_direccion, name="sel_dir"),
    url(r'add_dir/$', views.add_dir, name="add_dir"),
    url(r'rm_dir/(?P<id>\d*)/$', views.rm_dir, name="rm_dir"),
    url(r'change_tipo/(?P<tipo>.*)/$', views.change_tipo, name="change_tipo"),
    url(r'lst_dir/$', views.lista_direcciones, name="lista_direcciones"),
    url(r'profile/$', views.profile, name="profile"),
    url(r'load_pedido/$', views.load_pedido, name="load_pedido"),
    url(r'salir/$', views.salir, name="salir"),
    url(r'listado/$', views.mis_pedidos, name="listado"),
    url(r'sel_pedido/(?P<id>\d*)/$', views.load_pedido, name="sel_pedido"),
    url(r'modificar_datos/$', views.modificar_datos, name="modificar_datos"),
    url(r'abrir/$', views.abrir, name="abrir"),
    url(r'cerrar/$', views.cerrar, name="cerrar"),
    url(r'modificar_dir/(?P<id>\d*)/$', views.modificar_direccion, name="modificar_dir"),
]
