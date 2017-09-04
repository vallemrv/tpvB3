# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 04-Sep-2017
# @License: Apache license vesion 2.0

from kivy.uix.anchorlayout import AnchorLayout
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.lang import Builder
from glob import glob
from os import rename
from components.labels import LabelClicable


Builder.load_file('view/listadopdwidget.kv')


class ListadoPdWidget(AnchorLayout):
    tpv = ObjectProperty(None)
    precio = NumericProperty(0)
    des = StringProperty('Pedido')


    def __init__(self, **kargs):
        super(ListadoPdWidget, self).__init__(**kargs)
        self.selected = None
        self.file = None

    def salir(self):
        self.tpv.mostrar_inicio()

    def clear_self_widget(self):
        self.selected = None
        self.precio = 0
        self.pedido.rm_all_widgets()


    def mostrar_lista(self):
        files = sorted(glob("db/pd/*[0,4].11.json"))
        self.lista.rm_all_widgets()
        self.pedido.rm_all_widgets()
        for i in range(len(files)):
            btn = LabelClicable(bColor="#444444")
            db = JsonStore(files[i]).get("reg")
            btn.tag = {"db": db, "fl": files[i]}
            btn.font_size = 20
            texto = "{0: >25}     Total: {1:5.2f} €".format(
                         db["fecha"],
                         parse_float(db["total"]))
            btn.texto = texto
            btn.event = self.onPress
            self.lista.add_linea(btn)

    def onPress(self, btn):
        self.pedido.rm_all_widgets()
        self.selected = btn.tag
        lineas = self.selected["db"].get('lineas')
        total = 0
        for item in lineas:
            btn = LabelClicable(bColor="#444444")
            btn.font_size = 16
            tl = item["total"]
            total += tl
            btn.texto = "{0}   {1:.2f} €".format(
                item["des"], parse_float(tl))
            self.pedido.add_linea(btn)
        self.precio = total

    def cobrar(self):
        if self.selected:
            self.tpv.abrir_cajon()
            self.salir()
            db = self.selected["fl"]
            fl = self.selected["fl"]
            fl = fl.replace("0.11.", "1.11.")
            fl = fl.replace("4.11.", "3.11.")
            rename(db, fl)
