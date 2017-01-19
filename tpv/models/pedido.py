# -*- coding: utf-8 -*-
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty, StringProperty, ListProperty
from models.lineapedido import Constructor
from models.lineapedido import Linea
from kivy.storage.jsonstore import JsonStore
import time

class Pedido(EventDispatcher):
    total = NumericProperty(0.0)
    modo_pago = StringProperty('Efectivo')
    fecha = StringProperty('')
    num_avisador = StringProperty('')

    def __init__(self, **kargs):
        super(Pedido, self).__init__(**kargs)
        self.lineas_pedido = []
        self.constructor = None
        self.linea = None

    def add_modificador(self, obj):
        db = None
        if not self.linea:
            self.linea = Linea(obj)
            self.constructor = Constructor(producto=self.linea)
            self.lineas_pedido.append(self.linea)
            if self.linea.hay_preguntas():
                db = self.linea.get_pregunta()
        else:
            db = self.constructor.add_modificador(obj)

        self.total = self.linea.getTotal()
        return db

    def add_linea(self):
        self.linea = None
        self.constructor = None
        return self.lineas_pedido[-1]


    def borrar(self, obj):
        self.linea = None
        self.constructor = None
        self.lineas_pedido.remove(obj)

    def get_list_pedidos(self):
        lista = []
        for i in range(len(self.lineas_pedido)):
            obj = self.lineas_pedido[i]
            lista.append({'text': obj.obj.get('text'),
                          'descripcion': obj.getTexto(),
                          'total_linea': obj.getTotal()})
        return lista

    def guardar_pedido(self):
        nombre = time.strftime("db/pd/%y_%m_%d_%H_%M_%S.00.json")
        self.fecha = time.strftime("%y/%m/%d_%H:%M:%S")
        db = JsonStore(nombre)
        num = db.count()
        db.put(num, reg={'total': self.total,
                         'modo_pago': self.modo_pago,
                         'fecha': self.fecha,
                         'num_avisador': self.num_avisador,
                         'enviado': 'False',
                         'lineas': self.get_list_pedidos()})
