# -*- coding: utf-8 -*-
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty, StringProperty
from models.lineapedido import Constructor
from models.lineapedido import Linea
from kivy.storage.jsonstore import JsonStore
from copy import deepcopy
import time



class Pedido(EventDispatcher):
    total = NumericProperty(0.0)
    modo_pago = StringProperty('Efectivo')
    fecha = StringProperty('')
    num_avisador = StringProperty('')
    para_llevar = StringProperty('')

    def __init__(self, **kargs):
        super(Pedido, self).__init__(**kargs)
        self.lineas_pedido = []
        self.constructor = None
        self.linea = None
        self.dbCliente = None


    def add_modificador(self, obj):
        db = None
        if not self.linea:
            self.linea = Linea(deepcopy(obj))
            self.linea.obj['cant'] = 1
            self.constructor = Constructor(producto=self.linea)
            self.lineas_pedido.append(self.linea)

            if self.linea.hay_preguntas():
                db = self.linea.get_pregunta()
        else:
            db = self.constructor.add_modificador(obj)
        return db

    def rm_estado(self):
        if self.linea:
            if self.linea.getNumMod() > 0:
                self.linea.remove_modificador()
            else:
                self.lineas_pedido.pop()
                self.linea = None

    def actualizar_total(self):
        self.total = 0.0
        for item in self.lineas_pedido:
            self.total = self.total + item.getTotal()

    def finaliza_linea(self):
        self.actualizar_total()
        self.linea = None
        self.constructor = None

    def borrar(self, linea):
        borrar = False
        obj = linea.obj
        if obj['cant'] > 1:
            obj['cant'] = obj['cant'] - 1
        else:
            self.linea = None
            self.constructor = None
            if linea in self.lineas_pedido:
                self.lineas_pedido.remove(linea)
            borrar = True

        self.total = 0.0
        for item in self.lineas_pedido:
            self.total = self.total + item.getTotal()

        return borrar

    def getNumArt(self):
        num = 0
        for item in self.lineas_pedido:
            num = num + item.getNumArt()
        return num

    def sumar(self, linea):
        linea.obj['cant'] = linea.obj['cant'] + 1
        self.total = 0.0
        for item in self.lineas_pedido:
            self.total = self.total + item.getTotal()


    def get_list_pedidos(self):
        lista = []
        for i in range(len(self.lineas_pedido)):
            obj = self.lineas_pedido[i]
            lista.append({'text': obj.obj.get('text'),
                          'des': obj.getTexto(),
                          'cant': obj.obj.get('cant'),
                          'precio': obj.getPrecio(),
                          'total': obj.getTotal(),
                          'tipo': obj.obj.get("tipo")})
        return lista

    def guardar_pedido(self):
        pedido = time.strftime("%Y_%m_%d_%H_%M_%S")
        fichero = "db/pd/{0}1.00.json".format(pedido)
        self.fecha = time.strftime("%d/%m/%Y_%H:%M:%S")
        num_tlf = ""
        if self.dbCliente:
            num_tlf = self.dbCliente["reg"].get("num_tlf")
            pedidos = self.dbCliente["reg"].get("pedidos")
            nombre = self.dbCliente["reg"].get("nombre")
            dir = self.dbCliente["reg"].get("direccion")
            notas = self.dbCliente["reg"].get("notas")
            list = self.dbCliente["reg"].get("list")
            pedidos.append(fichero)
            self.dbCliente.put("reg", pedidos=pedidos,
                               direccion=dir,
                               nombre=nombre,
                               num_tlf=num_tlf,
                               list=list,
                               notas=notas)
            fichero = fichero.replace("1.00.", "0.00.")

        db = JsonStore(fichero)
        db.put('reg', total=self.total,
               modo_pago=self.modo_pago,
               para_llevar=self.para_llevar,
               fecha=self.fecha,
               num_avisador=self.num_avisador,
               numTicket=time.strftime("%y%m%d%H%M%S"),
               num_tlf=num_tlf,
               lineas=self.get_list_pedidos())
        return db
