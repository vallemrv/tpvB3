# -*- coding: utf-8 -*-
from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty, NumericProperty
from kivy.storage.jsonstore import JsonStore

from shared.lineawidget import LineaWidget
from models.lineapedido import LineaPedido

from uuid import uuid1


class Pedido(EventDispatcher):
    add_linea = ObjectProperty(None, allownone=True)
    clear_linea = ObjectProperty(None, allownone=True)
    total = NumericProperty(0.0)

    def __init__(self, **kargs):
        super(Pedido, self).__init__(**kargs)
        self.lineas_pedido = {}
        self.linea_editable = None
        self.clear_linea()
        self.UID = uuid1()
        self.storage = JsonStore('db/pedidos/%s.json' % self.UID)

    def add_modificador(self, obj):
        


    def borrar(self, linea):
        pass
