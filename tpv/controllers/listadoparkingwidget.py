# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 14-Sep-2017
# @License: Apache license vesion 2.0

from kivy.uix.anchorlayout import AnchorLayout
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.lang import Builder
from glob import glob
from components.labels import LabelClicable
from models.db.pedidos import Pedidos
from datetime import datetime
import os

Builder.load_file('view/listadoparkingwidget.kv')


class ListadoParking(AnchorLayout):
    tpv = ObjectProperty(None)
    precio = NumericProperty(0)
    des = StringProperty('Pedido')


    def __init__(self, **kargs):
        super(ListadoParking, self).__init__(**kargs)
        self.selected = None
        self.file = None

    def salir(self):
        self.tpv.mostrar_inicio()

    def clear_self_widget(self):
        self.selected = None
        self.precio = 0
        self.pedido.rm_all_widgets()


    def mostrar_lista(self):
        self.lista.rm_all_widgets()
        self.pedido.rm_all_widgets()
        listado = glob("../db/parking/*.json")
        for f in listado:
            db = JsonStore(f)
            pedido = db.get("db")
            btn = LabelClicable(bgColor="#444444",
                                font_size="16dp",
                                color="#ffffff")
            btn.tag = {"db": pedido, "fl": f}
            basename = os.path.basename(f).replace(".json","")
            texto = "{0: >25}  Total: {1:5.2f} €".format(basename, pedido['total'])
            btn.text = texto
            btn.bind(on_press=self.onPress)
            self.lista.add_linea(btn)

    def onPress(self, btn):
        self.pedido.rm_all_widgets()
        self.selected = btn.tag
        lineas = self.selected["db"]['lineas']
        total = 0
        for item in lineas:
            btn = LabelClicable(bgColor="#444444",
                                font_size = '16dp',
                                color = "#ffffff")
            tl = item['precio']
            total += tl
            btn.text = "{2: >3} {0}   {1:.2f} €".format(item['text'], tl, item['cant'])
            self.pedido.add_linea(btn)
        self.precio = total

    def cobrar(self):
        if self.selected:
            os.remove(self.selected["fl"])
            self.tpv.recuperar_pedido(self.selected)
