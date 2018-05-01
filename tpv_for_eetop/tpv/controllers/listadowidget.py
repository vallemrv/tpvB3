# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 16-Mar-2018
# @License: Apache license vesion 2.0

from kivy.uix.anchorlayout import AnchorLayout
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty
from kivy.lang import Builder
from glob import glob
from datetime import datetime
import threading

from valle_libs.tpv.impresora import DocPrint
from models.db import Pedidos, QSon, VentasSender
from modals import YesOrNo
from components.labels import LabelClicable
from datetime import datetime, date
import os


Builder.load_file('view/listadowidget.kv')

class ListadoWidget(AnchorLayout):
    tpv = ObjectProperty(None)
    precio = NumericProperty(0)
    des = StringProperty('Pedido')
    pd_lista = ListProperty([])


    def __init__(self, **kargs):
        super(ListadoWidget, self).__init__(**kargs)
        self.selected = None
        self.yesorno = YesOrNo(onExit=self.change_modo)


    def salir(self):
        self.clear_self_widget()
        self.tpv.mostrar_inicio()

    def clear_self_widget(self):
        self.selected = None
        self.precio = 0
        self.pedido.rm_all_widgets()

    def cambiar_formapg(self):
        if self.selected != None:
            pedido = self.selected.tag.get("db")
            if not "NPG" in pedido['estado']:
                self.yesorno.open()

    def change_modo(self, res):
        self.yesorno.dismiss()
        if self.selected != None and res=="SI":
            pedido = self.selected.tag.get("db")
            if pedido['modo_pago'] == "Efectivo":
                pedido['modo_pago'] = "Tarjeta"
                pedido['entrega'] = 0
                pedido['cambio'] = 0
            else:
                pedido['modo_pago'] = "Efectivo"
                pedido['entrega'] = pedido['total']
                pedido['cambio'] = 0
            self.save_pedido()

            self.des = "Pedido      %s" % pedido['modo_pago']
            fecha = pedido['fecha']
            if type(fecha) is datetime:
                fecha = fecha.strftime("%d/%m/%Y %H:%M:%S")
            else:
                fecha = datetime.strptime(fecha.replace("T", " "), "%Y-%m-%d %H:%M:%S.%f")

            texto = "{0: <10}   Avisador: {1: <26}  {2}  Total: {3:5.2f} €".format(
                         fecha.strftime("%H:%M:%S"),  pedido['num_avisador'], pedido['modo_pago'],
                         float(pedido['total']))
            self.selected.text = texto

    def on_success(self, req, result):
        if result["success"] == True:
            result["get"]["pedidos"].reverse()
            self.rellenar_pedidos(result["get"]["pedidos"])


    def rellenar_pedidos(self, pedidos):
        if len(pedidos) < len(self.pd_lista):
            self.pd_lista = []
            self.lista.rm_all_widgets()
        for db in pedidos:
            if db['id'] in self.pd_lista:
                    continue
            self.pd_lista.append(db['id'])
            btn = LabelClicable(bgColor="#444444",
                                font_size = '20dp',
                                color="#ffffff")
            btn.tag = {"db": db}
            fecha = datetime.strptime(db['fecha'].replace("T", " "), "%Y-%m-%d %H:%M:%S.%f")
            texto = "{0: <10}   Avisador: {1: <26}  {2}  Total: {3:5.2f} €".format(
                         fecha.strftime("%H:%M:%S"),  db['num_avisador'], db['modo_pago'],
                         float(db['total']))
            btn.text = texto
            btn.bind(on_release=self.onPress)
            self.lista.add_linea(btn)
        self.tpv.hide_spin()

    def mostrar_lista(self):
        sender = VentasSender()
        qson = QSon("Pedidos", estado__icontains="PG")
        qson.append_child(QSon("LineasPedido"))
        sender.filter(qson)
        sender.send(self.on_success, wait=False)
        self.tpv.show_spin()

    def onPress(self, btn):
        self.pedido.rm_all_widgets()
        self.selected = btn
        pedido = self.selected.tag.get("db")
        lineas = pedido['lineaspedido']
        self.des = "Pedido      %s" % pedido['modo_pago']
        total = 0
        for item in lineas:
            btn = LabelClicable(bgColor="#444444",
                                font_size = '16dp',
                                color = "#ffffff")
            tl = float(item['total'])
            total += tl
            tipo = "" if not item['tipo'] in ("pizzas", "burger") else item['tipo'].upper()
            if tipo.endswith("s"):
                tipo = tipo[:-1]
            btn.text = "{0: >4}  {4} {1} {2: <30}  {3:.2f} €".format(item['cant'], item['text'],
                                                                    item['des'].lower(), tl, tipo)
            self.pedido.add_linea(btn)
        self.precio = total

    def imprimirTk(self):
        if self.selected != None:
            r = threading.Thread(target=self.tpv.imprimir_directo,
                                 args=(self.selected.tag["db"],))
            r.start()
            self.salir()

    def save_pedido(self):
        sender = VentasSender()
        pd = self.selected.tag.get("db")
        qson = QSon("Pedidos", reg=pd)
        sender.save(qson)
        sender.send(wait=False)

    def hacer_pedido(self):
        if self.selected != None:
            sender = VentasSender()
            pd = self.selected.tag.get("db")
            pd["estado"] = pd["estado"].replace("SI", "NO")
            self.save_pedido()
            self.salir()
