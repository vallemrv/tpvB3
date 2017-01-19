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
        tipo = obj.get("tipo")
        if tipo == 'pizza':
            uid = str(uuid1())
            linea = LineaPedido(UID=uid, producto=obj)
            self.lineas_pedido[str(uid)] = linea
            self.linea_editable = LineaWidget(UID=linea.UID,
                                              texto=linea.getTexto(),
                                              borrar=self.borrar)
            self.add_linea(self.linea_editable)

        if tipo == 'diametro' or tipo == 'menu' or tipo == 'grupo':
            uid = self.linea_editable.UID
            linea = self.lineas_pedido[str(uid)]
            linea.add_modficador(obj)
            self.linea_editable.texto = linea.getTexto()
            if linea.finalizada:
                self.precio_total = self.precio_total + linea.precio

        return (linea.next, linea.finalizada)


    def borrar(self, linea):
        pass
