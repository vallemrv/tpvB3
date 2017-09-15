# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 15-Sep-2017
# @License: Apache license vesion 2.0

from kivy.uix.anchorlayout import AnchorLayout
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.clock import Clock
from kivy.lang import Builder
from glob import glob
from datetime import datetime

from valle_libs.tpv.impresora import DocPrint
from models.db.pedidos import Pedidos
from components.labels import LabelClicable
from datetime import datetime, date
import os

Builder.load_file('view/listadowidget.kv')

class ListadoWidget(AnchorLayout):
    tpv = ObjectProperty(None)
    precio = NumericProperty(0)
    des = StringProperty('Pedido')


    def __init__(self, **kargs):
        super(ListadoWidget, self).__init__(**kargs)
        self.selected = None

    def salir(self):
        self.tpv.mostrar_inicio()

    def clear_self_widget(self):
        self.selected = None
        self.precio = 0
        self.pedido.rm_all_widgets()

    def mostrar_lista(self):
        pedidos = Pedidos().getAll(query="estado LIKE 'PG_%'")
        self.lista.rm_all_widgets()
        for db in pedidos:
            btn = LabelClicable(bgColor="#444444",
                                font_size = '20dp',
                                color="#ffffff")
            btn.tag = {"db": db}
            fecha = datetime.strptime(db.fecha, "%Y-%m-%d %H:%M:%S.%f")
            texto = "{0: >25}   Avisador: {1: >6}   Total: {2:5.2f} €".format(
                         fecha.strftime("%H:%M:%S"), db.num_avisador,
                         db.total)
            btn.text = texto
            btn.bind(on_release=self.onPress)
            self.lista.add_linea(btn)



    def onPress(self, btn):
        self.pedido.rm_all_widgets()
        self.selected = btn.tag
        pedido = self.selected.get("db")
        lineas = pedido.lineaspedido.get()

        total = 0
        for item in lineas:
            btn = LabelClicable(bgColor="#444444",
                                font_size = '16dp',
                                color = "#ffffff")
            tl = item.total
            total += tl
            tipo = "" if not item.tipo in ("pizzas", "burger") else item.tipo
            if tipo.endswith("s"):
                tipo = tipo[:-1]
            btn.text = "{0: >4}  {4} {1} {2: <30}  {3:.2f} €".format(item.cant, item.text,
                                                                    item.des.lower(), tl, tipo)
            self.pedido.add_linea(btn)
        self.precio = total

    def imprimir(self):
        self.salir()
        Clock.schedule_once(self.hacer_pedido, .5)

    def imprimirTk(self):
        self.salir()
        Clock.schedule_once(self.imprimirTicket, .5)

    def imprimirTicket(self, dt):
        if self.selected:
            pd = self.selected.get("db")
            llevar = pd.para_llevar
            cl = None
            if llevar == "Domicilio":
                cl = pd.clientes.get()

            docPrint = DocPrint()
            docPrint.imprimirTicket("caja", pd.id,
                                    pd.lineaspedido.get(), pd.fecha,
                                    pd.total, float(pd.entrega),
                                    float(pd.cambio), cl)



    def hacer_pedido(self, dt):
        if self.selected:
            pd = self.selected.get("db")
            pd.estado = "PG_NO"
            pd.save()
            self.salir()
