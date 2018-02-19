# @Author: Manuel Rodriguez <valle>
# @Date:   01-Jan-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 09-Jan-2018
# @License: Apache license vesion 2.0

from django.conf.urls import url, include
from . import views

GASTOS = [
    url(r"^gastos/$", views.gastos, name="gastos"),
    url(r"^elegir_cuenta/$", views.elegir_cuenta, name="elegir_cuenta"),
    url(r"^gastos/(?P<id>-?\d*)/$", views.gastos, name="gastos"),
    url(r"^lista_gastos/$", views.lista_gastos, name="lista_gastos"),
    url(r"^find_cuentas/$", views.find_cuentas, name="find_cuentas"),
    url(r"^rm_gasto/(?P<id>\d*)$", views.rm_gasto, name="rm_gasto"),
    url(r"^find_gasto/$", views.find_gasto, name="find_gasto"),

]

INGRESOS = [
    url(r"^ingresos/$", views.ingresos, name="ingresos"),
    url(r"^ingresos/(?P<id>-?\d*)/$", views.ingresos, name="ingresos"),
    url(r"^lista_ingresos/$", views.lista_ingresos, name="lista_ingresos"),
    url(r"^find_ingreso/$", views.find_ingreso, name="find_ingreso"),
    url(r"^rm_ingreso/(?P<id>\d*)$", views.rm_ingreso, name="rm_ingreso"),
    url(r"^calcular_ingreso/(?P<fecha>\d*)$", views.calcular_ingreso, name="calcular_ingreso"),
    url(r"^calcular_ingreso/$", views.calcular_ingreso, name="calcular_ingreso_none"),
]


ALBARANES = [
    url(r"^albaranes/$", views.albaranes, name="albaranes_none"),
    url(r"^al_elegir_proveedor/$", views.al_elegir_proveedor, name="al_elegir_proveedor"),
    url(r"^albaranes/(?P<id>-?\d*)/$", views.albaranes, name="albaranes"),
    url(r"^lista_albaranes/$", views.lista_albaranes, name="lista_albaranes"),
    url(r"^find_albaran/$", views.find_albaran, name="find_albaranes"),
    url(r"^rm_albaran/(?P<id>\d*)$", views.rm_albaran, name="rm_albaranes"),
    url(r"^view_doc_albaran/(?P<id>\d*)$", views.view_doc_albaran, name="view_doc_albaran"),
    url(r"^viewer_img_albaran/(?P<id>\d*)$", views.viewer_img_albaran, name="viewer_img_albaran"),
    url(r"^find_albaran/$", views.find_albaran, name="find_albaran"),
]


PROVEEDORES = [
    url(r"^proveedores/$", views.proveedores, name="proveedores"),
    url(r"^proveedores/(?P<id>\d*)/$", views.proveedores, name="proveedores"),
    url(r"^lista_proveedores/$", views.lista_proveedores, name="lista_proveedores"),
    url(r"^find_proveedores/$", views.find_proveedores, name="find_proveedores"),
    url(r"^rm_proveedores/(?P<id>\d*)$", views.rm_proveedores, name="rm_proveedores"),
    url(r"^set_proveedor/(?P<id>\d*)$", views.set_proveedor, name="set_proveedor"),
    url(r"^set_proveedor/$", views.set_proveedor, name="set_proveedor_none"),
    url(r"^salir_proveedores/$", views.salir_proveedores, name="salir_proveedores"),
]

CUENTAS = [
    url(r"^cuentas/$", views.cuentas, name="cuentas"),
    url(r"^cuentas/(?P<id>\d*)/$", views.cuentas, name="cuentas"),
    url(r"^lista_cuentas/$", views.lista_cuentas, name="lista_cuentas"),
    url(r"^find_cuentas/$", views.find_cuentas, name="find_cuentas"),
    url(r"^rm_cuentas/(?P<id>\d*)$", views.rm_cuentas, name="rm_cuenta"),
    url(r"^set_cuenta/(?P<id>\d*)$", views.set_cuenta, name="set_cuenta"),
    url(r"^set_cuenta/$", views.set_cuenta, name="set_cuenta"),
    url(r"^salir_cuentas/$", views.salir_cuentas, name="salir_cuentas"),
]

SUBCUENTAS = [
    url(r"^subcuentas/$", views.subcuentas, name="subcuentas"),
    url(r"^subcuentas/(?P<id>\d*)/$", views.subcuentas, name="subcuentas"),
    url(r"^lista_subcuentas/$", views.lista_subcuentas, name="lista_subcuentas"),
    url(r"^find_subcuentas/$", views.find_subcuentas, name="find_subcuentas"),
    url(r"^rm_subcuentas/(?P<id>\d*)$", views.rm_subcuentas, name="rm_subcuenta"),
    url(r"^set_subcuenta/(?P<id>\d*)$", views.set_subcuenta, name="set_subcuenta"),
    url(r"^set_subcuenta/$", views.set_subcuenta, name="set_subcuenta"),
    url(r"^salir_subcuentas/$", views.salir_cuentas, name="salir_subcuentas"),
]

urlpatterns = [
    url(r"^$", views.inicio, name="inicio")
]+ PROVEEDORES + ALBARANES + CUENTAS + GASTOS + INGRESOS + SUBCUENTAS
